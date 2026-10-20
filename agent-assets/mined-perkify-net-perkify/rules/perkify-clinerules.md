# Project Guidelines

## Documentation

- Keep README.md in sync with new capabilities
- Maintain changelog entries in CHANGELOG.md
- Update relevant documentation in /docs when modifying features

## Design Principles

- Prefer composition over inheritance
- Use repository pattern for data access

## Code Style

- Use English comments and documentations by default
- Never disable any lint rules without explicit user approval

## Code Quality & Testing

- Unit tests required for business logic & utility
- Integration tests for contract-driven test on API endpoints
- E2E tests for critical end-user interactions
- Ensure all tests pass before submitting changes
- Before attempting completion, always make sure that any code changes have test coverage

## Security Practices

- DO NOT read or modify any file containing API keys, tokens, or credentials and never commit sensitive files
- Use environment variables for secrets
- Keep credentials out of logs and output
