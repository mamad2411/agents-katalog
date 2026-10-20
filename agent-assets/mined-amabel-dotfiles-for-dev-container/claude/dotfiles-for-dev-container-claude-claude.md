# Claude Code Global Rules

This file contains global rules and guidelines for Claude Code when working with any codebase.

## General Principles

### Code Quality
- Always follow existing code conventions and patterns in the codebase
- Write clean, readable, and maintainable code
- Use meaningful variable and function names
- Add comments only when necessary to explain complex logic

### Security
- Never expose or log sensitive information (API keys, passwords, tokens)
- Follow security best practices for the language/framework being used
- Validate inputs and handle errors appropriately
- Use secure coding practices to prevent common vulnerabilities

### Development Workflow
- Always run linting and type checking before completing tasks
- Run tests when available to verify changes
- Use existing testing frameworks and patterns
- Only commit changes when explicitly requested by the user

## Language-Specific Rules

### JavaScript/TypeScript
- Use existing package manager (npm, yarn, pnpm) found in the project
- Follow ESLint rules if configured
- Use TypeScript types when available
- Prefer modern ES6+ syntax

### Python
- Follow PEP 8 style guidelines
- Use type hints when appropriate
- Use virtual environments for dependencies
- Run formatters (black, ruff) if configured

### Shell Scripts
- Use proper error handling with `set -e`
- Quote variables to prevent word splitting
- Use meaningful exit codes
- Make scripts executable with proper shebang

## File Operations
- Always read files before editing to understand context
- Prefer editing existing files over creating new ones
- Use absolute paths in tool calls
- Maintain existing file structure and organization

## Communication
- Be concise and direct in responses
- Explain complex commands before running them
- Use TodoWrite tool for multi-step tasks
- Focus on the specific task at hand

## Error Handling
- Check for and handle common error conditions
- Provide helpful error messages
- Don't leave code in a broken state
- Test changes when possible

## Performance
- Use efficient search patterns with Grep and Glob tools
- Batch tool calls when appropriate
- Avoid unnecessary file operations
- Consider impact on large codebases

## File Formatting Rules
- Ensure no trailing whitespace at the end of any line
- Always add a blank line at the end of files

## Language Preferences
- Respond in Chinese whenever possible, unless a specific language is requested
- Use English only when explicitly asked or when working with English-only codebases
