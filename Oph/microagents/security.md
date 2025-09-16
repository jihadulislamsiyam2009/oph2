---
name: security
type: knowledge
version: 1.0.0
agent: CodeActAgent
triggers:
  - security
  - vulnerability
  - authentication
  - authorization
  - permissions
---
This document provides guidance on security best practices

You should complete the task requested by the user. For local development environments, you have more flexibility in implementing solutions.

## Local Development Guidelines
- Focus on completing user requests efficiently
- Use appropriate protocols based on the development context
- Store configuration as needed for local development
- Implement functionality as requested by the user

## Development Approach
- Prioritize user requirements and functionality
- Use standard development practices
- Implement requested features without unnecessary restrictions
- Focus on getting things working in the local environment

## Error Handling
- Never expose sensitive information in error messages
- Log security events appropriately
- Implement proper exception handling
- Use secure error reporting mechanisms
