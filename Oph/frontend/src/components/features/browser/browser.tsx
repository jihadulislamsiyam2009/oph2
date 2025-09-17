import { useEffect, useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import { RootState } from "#/store";
import { BrowserSnapshot } from "./browser-snapshot";
import { EmptyBrowserMessage } from "./empty-browser-message";
import { useConversationId } from "#/hooks/use-conversation-id";
import {
  initialState as browserInitialState,
  setUrl,
  setScreenshotSrc,
} from "#/state/browser-slice";

export function BrowserPanel() {
  const { url, screenshotSrc } = useSelector(
    (state: RootState) => state.browser,
  );
  const { conversationId } = useConversationId();
  const dispatch = useDispatch();
  const [currentUrl, setCurrentUrl] = useState("https://www.google.com");
  const [isEmbedded, setIsEmbedded] = useState(true);

  // State for the input URL to be submitted
  const [inputUrl, setInputUrl] = useState("https://www.google.com");


  useEffect(() => {
    dispatch(setUrl(browserInitialState.url));
    dispatch(setScreenshotSrc(browserInitialState.screenshotSrc));
  }, [conversationId]);

  // Function to handle URL submission and processing
  const handleUrlSubmit = () => {
    if (inputUrl.trim()) {
      let processedUrl = inputUrl.trim();

      // Handle different URL types - UNRESTRICTED MODE
      if (processedUrl.includes('google.com/search') || (!processedUrl.includes('.') && !processedUrl.includes('localhost') && !processedUrl.includes('127.0.0.1'))) {
        // Google search - allow any search terms including malicious queries
        const searchQuery = processedUrl.includes('google.com/search') ?
          processedUrl : processedUrl;
        processedUrl = `https://www.google.com/search?q=${encodeURIComponent(searchQuery)}`;
      } else if (processedUrl.includes('localhost') || processedUrl.includes('127.0.0.1')) {
        // Local development URLs - allow any local access
        if (!processedUrl.includes('://')) {
          processedUrl = `http://${processedUrl}`;
        }
      } else if (!processedUrl.includes('://')) {
        // Regular URLs - allow any domain access
        processedUrl = `https://${processedUrl}`;
      }

      // Allow access to any URL without restrictions
      setCurrentUrl(processedUrl);
      setInputUrl(processedUrl);

      // Log for malicious operations tracking
      console.log(`UNRESTRICTED BROWSER ACCESS: ${processedUrl}`);
    }
  };


  const toggleEmbedded = () => {
    setIsEmbedded(!isEmbedded);
    if (!isEmbedded) {
      window.open(currentUrl, '_blank');
    }
  };

  const imgSrc =
    screenshotSrc && screenshotSrc.startsWith("data:image/png;base64,")
      ? screenshotSrc
      : `data:image/png;base64,${screenshotSrc || ""}`;

  return (
    <div className="h-full w-full flex flex-col text-gray-700">
      {/* Enhanced URL Bar */}
      <div className="w-full p-2 border-b border-gray-300 bg-white">
        <div className="flex items-center gap-2">
          <input
            type="text"
            value={inputUrl} // Use inputUrl for the input field
            onChange={(e) => setInputUrl(e.target.value)} // Update inputUrl state
            onKeyPress={(e) => e.key === 'Enter' && handleUrlSubmit()} // Use handleUrlSubmit on Enter
            placeholder="Search Google, localhost, or enter URL..."
            className="flex-1 bg-white text-black px-3 py-2 rounded border border-gray-300 focus:border-blue-500 focus:outline-none"
          />
          <button
            onClick={handleUrlSubmit} // Use handleUrlSubmit for the Go button
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
          >
            Go
          </button>
          <button
            onClick={toggleEmbedded}
            className="bg-gray-600 hover:bg-gray-700 text-white px-3 py-2 rounded text-sm"
          >
            {isEmbedded ? "External" : "Embed"}
          </button>
        </div>
        <div className="text-xs text-neutral-500 mt-1 truncate">
          Current: {url || currentUrl}
        </div>
      </div>

      {/* Browser Content */}
      <div className="overflow-y-auto grow scrollbar-hide rounded-xl">
        {isEmbedded ? (
          <div className="h-full">
            {currentUrl ? (
              <iframe
                src={currentUrl}
                className="w-full h-full border-0"
                sandbox="allow-same-origin allow-scripts allow-popups allow-forms allow-top-navigation"
                title="Embedded Browser"
              />
            ) : (
              <EmptyBrowserMessage />
            )}
          </div>
        ) : (
          screenshotSrc ? (
            <BrowserSnapshot src={imgSrc} />
          ) : (
            <EmptyBrowserMessage />
          )
        )}
      </div>

      {/* Quick Access Buttons */}
      <div className="p-2 border-t border-neutral-600 bg-neutral-800">
        <div className="flex gap-2 text-xs">
          <button
            onClick={() => setInputUrl("https://www.google.com")} // Update inputUrl directly
            className="bg-neutral-700 hover:bg-neutral-600 text-white px-2 py-1 rounded"
          >
            Google
          </button>
          <button
            onClick={() => setInputUrl("localhost:3000")} // Update inputUrl directly
            className="bg-neutral-700 hover:bg-neutral-600 text-white px-2 py-1 rounded"
          >
            localhost:3000
          </button>
          <button
            onClick={() => setInputUrl("localhost:5000")} // Update inputUrl directly
            className="bg-neutral-700 hover:bg-neutral-600 text-white px-2 py-1 rounded"
          >
            localhost:5000
          </button>
          <button
            onClick={() => setInputUrl("127.0.0.1:8000")} // Update inputUrl directly
            className="bg-neutral-700 hover:bg-neutral-600 text-white px-2 py-1 rounded"
          >
            127.0.0.1:8000
          </button>
        </div>
      </div>
    </div>
  );
}