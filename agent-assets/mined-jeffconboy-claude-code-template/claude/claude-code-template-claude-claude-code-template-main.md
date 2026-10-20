# Project Instructions for Claude Code

This file contains instructions and context that Claude Code will use when working on this project.

## Project Overview
[Describe your project here - what it does, its main purpose, tech stack]

## Code Standards

### General Principles
- Write clean, readable, self-documenting code
- Follow DRY (Don't Repeat Yourself) principle
- Keep functions small and focused (single responsibility)
- Use meaningful variable and function names
- Add comments only when the "why" isn't obvious from the code

### Language-Specific Conventions
#### JavaScript/TypeScript
- Use `const` by default, `let` when needed, never `var`
- Prefer async/await over promises
- Use optional chaining (`?.`) and nullish coalescing (`??`)
- Follow ESLint recommendations

#### Python
- Follow PEP 8 style guide
- Use type hints for function parameters and returns
- Prefer f-strings for string formatting
- Use list comprehensions when appropriate

#### Go
- Follow standard Go formatting (use gofmt)
- Return errors as the last return value
- Use meaningful package names
- Keep interfaces small

## Project Structure
```
src/           # Source code
tests/         # Test files
docs/          # Documentation
scripts/       # Utility scripts
```

## Testing Requirements
- Write tests for all new features
- Maintain test coverage above 70%
- Tests should be readable and document behavior
- Use descriptive test names that explain what's being tested

## Security Guidelines
- Never commit secrets, API keys, or passwords
- Validate all user inputs
- Use environment variables for configuration
- Follow OWASP guidelines for web applications
- Keep dependencies up to date

## Git Workflow
- Use clear, descriptive commit messages
- Keep commits focused and atomic
- Branch naming: `feature/description`, `fix/description`
- Always test before committing

## Documentation
- Update README when adding new features
- Document all public APIs
- Include examples in documentation
- Keep documentation close to code

## Performance Considerations
- Profile before optimizing
- Consider algorithmic complexity
- Cache expensive operations
- Use lazy loading when appropriate

## Code Organization & Technical Debt Prevention

### Root Directory Rules
**Keep root directory minimal and organized:**
- ✅ Essential files only: README.md, package.json/.gitignore, LICENSE, CHANGELOG.md
- ❌ No loose scripts, documentation, or config files
- ❌ No temporary files, logs, or build artifacts
- ❌ No large assets or data files

### Directory Structure Standards
```
project-root/
├── src/                    # All source code
├── tests/ or __tests__/    # All test files
├── docs/                   # Documentation files
├── scripts/                # Build and utility scripts
├── config/                 # Configuration files
├── assets/ or public/      # Static assets
├── .claude/                # Claude Code configuration
└── [essential files only]  # README, package.json, etc.
```

### File Organization Rules
- **Source Code**: All in `src/` directory with clear module boundaries
- **Tests**: Co-located with source OR in dedicated `tests/` directory
- **Documentation**: All `.md` files except README.md go in `docs/`
- **Scripts**: Build, deploy, utility scripts go in `scripts/`
- **Configuration**: Environment configs, tool configs go in `config/`

### Technical Debt Prevention
- **No TODO items without issue tracking** - Link to GitHub issues
- **Function length limit**: Maximum 50 lines per function
- **File length limit**: Maximum 500 lines per file
- **Complexity limit**: Maximum cyclomatic complexity of 10
- **No magic numbers**: Use named constants
- **No duplicated code**: Extract to shared utilities
- **No dead code**: Remove unused imports, variables, functions

### Dependency Management
- **Regular updates**: Update dependencies monthly
- **Security scanning**: Run vulnerability checks before releases
- **Lock file discipline**: Always commit lock files
- **Minimize dependencies**: Question every new dependency
- **Document why**: Explain non-obvious dependency choices

### Code Quality Gates
Before any commit:
- ✅ All tests pass
- ✅ Linting passes with zero warnings
- ✅ No console.log/print statements in production code
- ✅ No hardcoded secrets or API keys
- ✅ Documentation updated for public API changes

### Refactoring Guidelines
- **Boy Scout Rule**: Always leave code better than you found it
- **Incremental improvements**: Small, safe refactorings over big rewrites
- **Test coverage**: Ensure tests exist before refactoring
- **Single responsibility**: One change, one reason
- **Backward compatibility**: Don't break existing APIs without versioning

## Specific Project Rules
[Add your project-specific rules here]
- Use semantic versioning for all releases
- All public APIs must have comprehensive documentation
- Database migrations must be backward compatible
- 

## Common Commands
```bash
# Development
npm run dev        # Start development server
npm test          # Run tests
npm run build     # Build for production

# Utilities
npm run lint      # Check code style
npm run format    # Auto-format code
```

## Dependencies to Know About
[List key dependencies and their purposes]
- 
- 

## Known Issues / Technical Debt
[List any known issues or areas that need improvement]
- 
- 

## External Resources
- [Project documentation](https://example.com/docs)
- [API documentation](https://example.com/api)
- [Design system](https://example.com/design)

---
Remember: When in doubt, prioritize code clarity and maintainability over cleverness.