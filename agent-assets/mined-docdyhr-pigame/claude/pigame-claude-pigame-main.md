# CLAUDE.md - Guidelines for Claude Code Assistant

## Build & Run Commands
- Run program: `./pigame [OPTIONS] [YOUR_PI]`
- Lint all code: `./scripts/lint.sh`
- Run all tests: `./scripts/run_tests.sh`
- Setup development environment: `./scripts/setup.sh`
- Install: Copy `pigame` to your $PATH (e.g., `cp pigame ~/bin`)

## Code Style Guidelines
- **Shell**: Use Bash with shebang `#!/usr/bin/env bash`
- **Formatting**: 4-space indentation, proper spacing for conditional expressions
- **Variables**: Use ALL_CAPS for constants, lowercase for local variables
- **Functions**: Use snake_case for functions, add comments describing purpose
- **Error Handling**: Use `>&2` for error messages, exit with non-zero status
- **Input Validation**: Always validate arguments before processing
- **Comments**: Add TODO comments for improvements, use clear comments for complex logic
- **Quoting**: Always quote variable references to prevent word splitting
- **Shell Check**: Follow shellcheck guidelines (see references in code)
- **Portability**: Ensure code works on various Unix-like systems

## Dependencies
- Requires `bc` (arbitrary precision calculator) installed on the system
- Development requires Python 3.x and optionally ShellCheck, clang-format if developing Bash/C code
- All Python dependencies are managed through the setup script `./scripts/setup.sh`
