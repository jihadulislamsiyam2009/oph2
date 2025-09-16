
import { useSelector } from "react-redux";
import { useState, useRef, useEffect } from "react";
import { RootState } from "#/store";
import { useTerminal } from "#/hooks/use-terminal";
import "@xterm/xterm/css/xterm.css";
import { RUNTIME_INACTIVE_STATES } from "#/types/agent-state";
import { cn } from "#/utils/utils";
import { WaitingForRuntimeMessage } from "../chat/waiting-for-runtime-message";

function Terminal() {
  const { commands } = useSelector((state: RootState) => state.cmd);
  const { curAgentState } = useSelector((state: RootState) => state.agent);
  const [currentCommand, setCurrentCommand] = useState("");
  const [commandHistory, setCommandHistory] = useState<string[]>([]);
  const [historyIndex, setHistoryIndex] = useState(-1);
  const [isInteractive, setIsInteractive] = useState(true);
  const inputRef = useRef<HTMLInputElement>(null);

  const isRuntimeInactive = RUNTIME_INACTIVE_STATES.includes(curAgentState);

  const ref = useTerminal({
    commands,
  });

  const executeCommand = async (command: string) => {
    if (!command.trim()) return;

    // Add to history
    const newHistory = [...commandHistory, command];
    setCommandHistory(newHistory);
    setHistoryIndex(-1);
    setCurrentCommand("");

    try {
      // Send command to backend for execution
      const response = await fetch('/api/execute-command', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          command: command,
          allow_dangerous: true, // Allow any command
          force_execute: true
        }),
      });
      
      const result = await response.json();
      console.log('Command result:', result);
    } catch (error) {
      console.error('Command execution error:', error);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      executeCommand(currentCommand);
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      if (historyIndex < commandHistory.length - 1) {
        const newIndex = historyIndex + 1;
        setHistoryIndex(newIndex);
        setCurrentCommand(commandHistory[commandHistory.length - 1 - newIndex] || "");
      }
    } else if (e.key === 'ArrowDown') {
      e.preventDefault();
      if (historyIndex > 0) {
        const newIndex = historyIndex - 1;
        setHistoryIndex(newIndex);
        setCurrentCommand(commandHistory[commandHistory.length - 1 - newIndex] || "");
      } else if (historyIndex === 0) {
        setHistoryIndex(-1);
        setCurrentCommand("");
      }
    } else if (e.key === 'Tab') {
      e.preventDefault();
      // Basic tab completion for common commands
      const suggestions = ['ls', 'cd', 'pwd', 'cat', 'sudo', 'rm', 'cp', 'mv', 'chmod', 'chown'];
      const match = suggestions.find(cmd => cmd.startsWith(currentCommand));
      if (match) {
        setCurrentCommand(match + ' ');
      }
    }
  };

  const toggleMode = () => {
    setIsInteractive(!isInteractive);
  };

  useEffect(() => {
    if (isInteractive && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isInteractive]);

  return (
    <div className="h-full flex flex-col rounded-xl">
      {isRuntimeInactive && <WaitingForRuntimeMessage className="pt-16" />}

      {/* Terminal Mode Toggle */}
      <div className="flex justify-between items-center p-2 bg-neutral-800 border-b border-neutral-600">
        <div className="flex gap-2">
          <button
            onClick={toggleMode}
            className={cn(
              "px-3 py-1 rounded text-sm font-medium transition-colors",
              isInteractive 
                ? "bg-blue-600 text-white" 
                : "bg-neutral-700 text-neutral-300 hover:bg-neutral-600"
            )}
          >
            Interactive
          </button>
          <button
            onClick={toggleMode}
            className={cn(
              "px-3 py-1 rounded text-sm font-medium transition-colors",
              !isInteractive 
                ? "bg-blue-600 text-white" 
                : "bg-neutral-700 text-neutral-300 hover:bg-neutral-600"
            )}
          >
            AI Output
          </button>
        </div>
        <div className="text-xs text-neutral-500">
          {isInteractive ? "Type commands directly" : "View AI output"}
        </div>
      </div>

      <div className="flex-1 min-h-0 flex flex-col">
        {/* AI Terminal Output */}
        <div 
          className={cn(
            "flex-1 p-4",
            isInteractive ? "max-h-1/2 overflow-y-auto" : "h-full"
          )}
        >
          <div
            ref={ref}
            className={cn(
              "w-full h-full",
              isRuntimeInactive ? "p-0 w-0 h-0 opacity-0 overflow-hidden" : "",
            )}
          />
        </div>

        {/* Interactive Terminal Input */}
        {isInteractive && (
          <div className="border-t border-neutral-600 bg-neutral-900">
            {/* Command History */}
            {commandHistory.length > 0 && (
              <div className="max-h-32 overflow-y-auto p-2 bg-neutral-800 border-b border-neutral-600">
                <div className="text-xs text-neutral-500 mb-1">Recent Commands:</div>
                {commandHistory.slice(-5).map((cmd, index) => (
                  <div 
                    key={index} 
                    className="text-xs text-neutral-300 cursor-pointer hover:text-white px-2 py-1 rounded hover:bg-neutral-700"
                    onClick={() => setCurrentCommand(cmd)}
                  >
                    $ {cmd}
                  </div>
                ))}
              </div>
            )}

            {/* Command Input */}
            <div className="p-3 flex items-center gap-2">
              <span className="text-green-400 font-mono text-sm">$</span>
              <input
                ref={inputRef}
                type="text"
                value={currentCommand}
                onChange={(e) => setCurrentCommand(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Enter any command (unrestricted access)..."
                className="flex-1 bg-transparent text-white font-mono text-sm outline-none placeholder-neutral-500"
                autoComplete="off"
                spellCheck={false}
              />
              <button
                onClick={() => executeCommand(currentCommand)}
                className="bg-green-600 hover:bg-green-700 text-white px-3 py-1 rounded text-sm font-medium"
              >
                Execute
              </button>
            </div>

            {/* Quick Commands */}
            <div className="px-3 pb-3">
              <div className="flex gap-2 text-xs">
                {['ls -la', 'pwd', 'whoami', 'sudo su', 'ps aux', 'netstat -tulpn'].map((cmd) => (
                  <button
                    key={cmd}
                    onClick={() => setCurrentCommand(cmd)}
                    className="bg-neutral-700 hover:bg-neutral-600 text-neutral-300 px-2 py-1 rounded"
                  >
                    {cmd}
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Terminal;
