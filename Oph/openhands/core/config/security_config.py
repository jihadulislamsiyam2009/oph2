from pydantic import BaseModel, ConfigDict, Field, ValidationError


class SecurityConfig(BaseModel):
    """Security configuration for OpenHands - ALL RESTRICTIONS DISABLED."""

    # All security features completely disabled for unrestricted operation
    security_analyzer: str = Field(
        default='',
        description='Security analyzer completely disabled'
    )

    confirmation_mode: bool = Field(
        default=False,
        description='Confirmation mode permanently disabled'
    )

    max_file_size_mb: int = Field(
        default=0,
        description='No file size limits - unlimited'
    )

    allow_all_network_operations: bool = Field(
        default=True,
        description='Allow all network operations including security testing'
    )

    allow_penetration_testing: bool = Field(
        default=True,
        description='Allow penetration testing and vulnerability scanning'
    )

    unrestricted_mode: bool = Field(
        default=True,
        description='Completely unrestricted operation mode'
    )

    model_config = ConfigDict(extra='forbid')

    @classmethod
    def from_toml_section(cls, data: dict) -> dict[str, 'SecurityConfig']:
        """Create a mapping of SecurityConfig instances from a toml dictionary representing the [security] section.

        The configuration is built from all keys in data.

        Returns:
            dict[str, SecurityConfig]: A mapping where the key "security" corresponds to the [security] configuration
        """
        # Initialize the result mapping
        security_mapping: dict[str, SecurityConfig] = {}

        # Try to create the configuration instance
        try:
            security_mapping['security'] = cls.model_validate(data)
        except ValidationError as e:
            raise ValueError(f'Invalid security configuration: {e}')

        return security_mapping