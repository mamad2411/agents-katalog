# Cursor Rules for Vibes Project

## Project Context
This is a demonstration repository showing AI coding assistant capabilities using dev containers. The project includes:
- Claude Code CLI (@anthropic-ai/claude-code)
- Gemini CLI (@google/gemini-cli)  
- OpenAI Codex (@openai/codex)
- Marp for slide generation

## Coding Standards

### General
- Use TypeScript when possible
- Prefer functional programming patterns
- Write clear, self-documenting code
- Include proper error handling

### File Structure
- Keep related files in logical directories
- Use descriptive filenames
- Create README files for complex directories

### Documentation
- Document all public APIs
- Include usage examples
- Keep documentation up to date with code changes
- Use JSDoc for TypeScript/JavaScript functions

### Dependencies
- Prefer well-maintained packages
- Keep dependencies minimal and focused
- Use exact versions in package.json for reproducibility

## AI Assistant Guidelines

### Prompting Best Practices
- Provide clear context about the project structure
- Specify which CLI tool you're using (Claude, Gemini, or Codex)
- Reference the appropriate prompting guide (CLAUDE.md, GEMINI.md, AGENTS.md)

### Code Generation
- Generate code that follows the project's existing patterns
- Include appropriate TypeScript types
- Add error handling and edge case considerations
- Provide explanations for complex logic

### Testing
- Include tests for new functionality
- Follow existing test patterns in the project
- Test edge cases and error conditions

## Dev Container Specifics
- Use the configured environment variables
- Leverage the pre-installed tools and CLIs
- Follow the setup instructions in README.md

## Commands
- `pnpm slides` - Generate presentation slides using Marp
- `claude` - Start Claude Code CLI
- `gemini` - Start Gemini CLI
- `codex` - Start OpenAI Codex CLI

## Notes
- This project focuses on demonstration and education
- Prioritize clarity and learning over optimization
- Include examples that showcase AI assistant capabilities
- Keep the codebase accessible to developers of all skill levels