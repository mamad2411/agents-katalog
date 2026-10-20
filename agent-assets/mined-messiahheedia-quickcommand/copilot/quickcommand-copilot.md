<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# QuickCommand AI Assistant - Copilot Instructions

This is a Python project that creates an AI-powered command assistant for PowerShell and Python environments.

## Project Context
- **Primary Goal**: Create a natural language to command translator that suggests commands without auto-executing them
- **Target Environments**: PowerShell (Windows), Python scripts
- **AI Integration**: Uses OpenAI API for natural language processing
- **Safety First**: Never auto-execute commands, always require user confirmation

## Code Style Guidelines
- Follow PEP 8 for Python code
- Use type hints where appropriate
- Include comprehensive error handling
- Add docstrings for all functions and classes
- Keep security as a top priority - sanitize all inputs

## Architecture Patterns
- Modular design with separate concerns (AI, commands, shells)
- Configuration-driven approach using YAML and environment variables
- Plugin-style architecture for extending command patterns
- Async/await patterns for AI API calls where beneficial

## Key Features to Maintain
- Command preview before execution
- Support for multiple shell environments
- Extensible command pattern system
- Safe handling of potentially dangerous commands
- User-friendly CLI interface with colors and prompts

When generating code, prioritize:
1. Security and safety
2. User experience
3. Maintainability
4. Performance
