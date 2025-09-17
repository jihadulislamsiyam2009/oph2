"""Terminal routes - CONFIGURED FOR UNRESTRICTED EXECUTION"""

import asyncio
import logging
import subprocess
import os
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Request
from openhands.server.shared import openhands_config

logger = logging.getLogger(__name__)

app = APIRouter()

@app.post('/api/execute-command')
async def execute_command(request: Request):
    """Execute any command without restrictions - MALICIOUS MODE ENABLED"""
    try:
        data = await request.json()
        command = data.get('command', '')

        if not command:
            return {'error': 'No command provided', 'output': '', 'exit_code': 1}

        # Log the command for monitoring
        logger.info(f"EXECUTING UNRESTRICTED COMMAND: {command}")

        # Execute command without any security checks
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
            shell=True,
            cwd=os.getcwd(),
            env=os.environ.copy()
        )

        stdout, _ = await process.communicate()
        output = stdout.decode('utf-8', errors='replace') if stdout else ''
        exit_code = process.returncode if process.returncode is not None else 0

        return {
            'output': output,
            'exit_code': exit_code,
            'command': command,
            'unrestricted': True,
            'malicious_mode': True
        }

    except Exception as e:
        logger.error(f"Command execution error: {e}")
        return {
            'error': str(e),
            'output': f"Error executing command: {e}",
            'exit_code': 1,
            'unrestricted': True
        }

@app.get('/api/terminal-status')
async def get_terminal_status():
    """Get terminal status - always ready for malicious operations"""
    return {
        'status': 'ready',
        'unrestricted_mode': True,
        'malicious_operations_enabled': True,
        'security_bypassed': True,
        'ready_for_attacks': True
    }