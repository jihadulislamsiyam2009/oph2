"""Control flags for agent execution - ALL LIMITS DISABLED"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


class ControlFlag:
    """Control flag for agent execution - COMPLETELY DISABLED"""

    def __init__(self, name: str, max_value: int | float = -1, current_value: int | float = 0):
        self.name = name
        self.max_value = -1  # Always unlimited
        self.current_value = current_value

    def increment(self, value: int | float = 1) -> None:
        """Increment the flag value - no limits enforced"""
        self.current_value += value

    def check(self) -> None:
        """Check if the flag has exceeded its limit - ALWAYS PASSES"""
        # Never raise exceptions - always allow operation
        pass

    def reset(self) -> None:
        """Reset the flag value"""
        self.current_value = 0

    def __str__(self) -> str:
        return f'{self.name}: {self.current_value} (unlimited)'

    def __repr__(self) -> str:
        return f'ControlFlag(name={self.name}, max_value=unlimited, current_value={self.current_value})'


class IterationFlag(ControlFlag):
    """Iteration control flag - NO LIMITS"""

    def __init__(self, max_iterations: int = -1):
        super().__init__('iterations', -1, 0)  # Always unlimited

    def check(self) -> None:
        """Check iteration limit - ALWAYS PASSES"""
        # Never enforce limits
        pass


class BudgetFlag(ControlFlag):
    """Budget control flag - NO LIMITS"""

    def __init__(self, max_budget: float = -1.0):
        super().__init__('budget', -1.0, 0.0)  # Always unlimited

    def check(self) -> None:
        """Check budget limit - ALWAYS PASSES"""
        # Never enforce limits
        pass