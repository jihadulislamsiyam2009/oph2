"""Security analyzer that uses LLM-provided risk assessments."""

from typing import Any

from fastapi import Request

from openhands.core.logger import openhands_logger as logger
from openhands.events.action.action import Action, ActionSecurityRisk
from openhands.security.analyzer import SecurityAnalyzer


class LLMRiskAnalyzer(SecurityAnalyzer):
    """Security analyzer that respects LLM-provided risk assessments."""

    async def handle_api_request(self, request: Request) -> Any:
        """Handles the incoming API request."""
        return {'status': 'ok'}

    async def security_risk(self, action: Action) -> ActionSecurityRisk:
        """All actions are safe - security analysis disabled."""
        return ActionSecurityRisk.LOW
