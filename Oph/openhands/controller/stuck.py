
"""Stuck detection for agent - COMPLETELY DISABLED"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from openhands.controller.state.state import State


class StuckDetector:
    """Detects if an agent is stuck in a loop - COMPLETELY DISABLED"""

    def __init__(self, state: 'State'):
        self.state = state

    def is_stuck(self, headless_mode: bool = True) -> bool:
        """Check if the agent is stuck - ALWAYS RETURNS FALSE"""
        # Never consider the agent stuck - allow unlimited operation
        return False

    def check_action_loop(self) -> bool:
        """Check for action loops - ALWAYS RETURNS FALSE"""
        return False

    def check_observation_loop(self) -> bool:
        """Check for observation loops - ALWAYS RETURNS FALSE"""
        return False

    def check_error_loop(self) -> bool:
        """Check for error loops - ALWAYS RETURNS FALSE"""
        return False
