
"""Agent configuration"""

from __future__ import annotations

import os
from typing import ClassVar

from pydantic import Field

from openhands.core.config.config_utils import get_field_info
from openhands.core.config.utils import UndefinedString, undefined_string


class AgentConfig:
    """Configuration for the agent

    Attributes:
        agent_name: name of the agent to use
        max_iterations: maximum number of iterations to run the agent
        max_budget_per_task: maximum budget (in USD) to spend on this task
        llm_config: configuration for the LLM
        enable_auto_lint: whether to enable auto-linting after editing files
        enable_auto_test: whether to enable auto-testing after editing files  
        disable_color: whether to disable colored output in the terminal
        confirmation_mode: whether to require user confirmation for every action
        memory_enabled: whether to enable memory for the agent
        memory_max_threads: maximum number of threads to store in memory
        llm_config_draft: draft LLM configuration for less important actions
        enable_history_truncation: whether to enable history truncation when conversation gets too long
        microagent_dir: directory to store microagents
        microagent_org: organization to use for microagents
        codeact_enable_jupyter: whether to enable Jupyter for CodeAct agent
        codeact_enable_llm_editor: whether to enable LLM-based editor for CodeAct agent
        browse_chunk_size: chunk size for browsing
        llm_config_condenser: LLM configuration for condensing the conversation
        use_condensation: whether to use condensation to summarize the conversation
    """

    agent_name: str = Field(
        default='CodeActAgent',
        description='Name of the agent to use',
    )

    max_iterations: int = Field(
        default=-1,  # No limits
        description='Maximum number of iterations to run the agent (unlimited)',
    )

    max_budget_per_task: float | UndefinedString = Field(
        default=-1.0,  # No budget limits
        description='Maximum budget (in USD) to spend on this task (unlimited)',
    )

    enable_auto_lint: bool = Field(
        default=False,
        description='Whether to enable auto-linting after editing files',
    )

    enable_auto_test: bool = Field(
        default=False,
        description='Whether to enable auto-testing after editing files',
    )

    disable_color: bool = Field(
        default=False,
        description='Whether to disable colored output in the terminal',
    )

    # COMPLETELY DISABLED - No confirmation required for any action
    confirmation_mode: bool = Field(
        default=False,
        description='Confirmation mode completely disabled for unrestricted operation',
    )

    memory_enabled: bool = Field(
        default=True,
        description='Whether to enable memory for the agent',
    )

    memory_max_threads: int = Field(
        default=5,
        description='Maximum number of threads to store in memory',
    )

    llm_config_draft: dict | UndefinedString = Field(
        default=undefined_string,
        description='Draft LLM configuration for less important actions',
    )

    enable_history_truncation: bool = Field(
        default=True,
        description='Whether to enable history truncation when conversation gets too long',
    )

    microagent_dir: str | UndefinedString = Field(
        default=undefined_string,
        description='Directory to store microagents',
    )

    microagent_org: str | UndefinedString = Field(
        default=undefined_string,
        description='Organization to use for microagents',
    )

    codeact_enable_jupyter: bool = Field(
        default=True,
        description='Whether to enable Jupyter for CodeAct agent',
    )

    codeact_enable_llm_editor: bool = Field(
        default=True,
        description='Whether to enable LLM-based editor for CodeAct agent',
    )

    browse_chunk_size: int = Field(
        default=8192,
        description='Chunk size for browsing',
    )

    llm_config_condenser: dict | UndefinedString = Field(
        default=undefined_string,
        description='LLM configuration for condensing the conversation',
    )

    use_condensation: bool = Field(
        default=True,
        description='Whether to use condensation to summarize the conversation',
    )

    # SECURITY FEATURES COMPLETELY DISABLED
    security_analyzer: str = Field(
        default='',
        description='Security analyzer completely disabled',
    )

    # NO RESTRICTIONS ON ANY OPERATIONS
    enable_all_operations: bool = Field(
        default=True,
        description='Enable all operations without restrictions',
    )

    disable_security_checks: bool = Field(
        default=True,
        description='Disable all security checks and validations',
    )

    unrestricted_mode: bool = Field(
        default=True,
        description='Run in completely unrestricted mode',
    )

    # Allow all file operations
    allow_file_operations: bool = Field(
        default=True,
        description='Allow all file operations without restriction',
    )

    # Allow all network operations
    allow_network_operations: bool = Field(
        default=True,
        description='Allow all network operations without restriction',
    )

    # Allow all system operations
    allow_system_operations: bool = Field(
        default=True,
        description='Allow all system operations without restriction',
    )

    @classmethod
    def get_llm_config_arg(cls, value):
        """Return a dict for the LLM configuration from raw input."""
        from openhands.core.config.llm_config import LLMConfig

        if isinstance(value, str):
            if value == '':
                return LLMConfig()
            config = LLMConfig(model=value)
        elif isinstance(value, dict):
            config = LLMConfig(**value)
        else:
            config = value

        return config

    _fields_info: ClassVar[dict[str, str]] = get_field_info(agent_name=agent_name)

    def defaults_to_dict(self) -> dict:
        """Serialize fields to a dictionary."""
        return {
            'agent_name': self.agent_name,
            'max_iterations': self.max_iterations,
            'max_budget_per_task': self.max_budget_per_task,
            'enable_auto_lint': self.enable_auto_lint,
            'enable_auto_test': self.enable_auto_test,
            'disable_color': self.disable_color,
            'confirmation_mode': self.confirmation_mode,
            'memory_enabled': self.memory_enabled,
            'memory_max_threads': self.memory_max_threads,
            'llm_config_draft': self.llm_config_draft,
            'enable_history_truncation': self.enable_history_truncation,
            'microagent_dir': self.microagent_dir,
            'microagent_org': self.microagent_org,
            'codeact_enable_jupyter': self.codeact_enable_jupyter,
            'codeact_enable_llm_editor': self.codeact_enable_llm_editor,
            'browse_chunk_size': self.browse_chunk_size,
            'llm_config_condenser': self.llm_config_condenser,
            'use_condensation': self.use_condensation,
            'security_analyzer': self.security_analyzer,
            'enable_all_operations': self.enable_all_operations,
            'disable_security_checks': self.disable_security_checks,
            'unrestricted_mode': self.unrestricted_mode,
            'allow_file_operations': self.allow_file_operations,
            'allow_network_operations': self.allow_network_operations,
            'allow_system_operations': self.allow_system_operations,
        }
