# {{PROJECT_NAME}}

{{PROJECT_DESCRIPTION}}

## Tech Stack
- **Language**: {{PRIMARY_LANGUAGE}} ({{LANGUAGE_VERSION}})
- **Framework**: {{PRIMARY_FRAMEWORK}}
- **Database**: {{DATABASE}}
- **Testing**: {{TESTING_FRAMEWORK}}
- **Package Manager**: {{PACKAGE_MANAGER}}

### DO NOT Use
{{BANNED_DEPENDENCIES}}

## Core Principles

1. **Clarify Before Coding** — Understand requirements before writing code. Ask questions when intent is unclear. No code without clear goals.
2. **Simplicity First** — Choose the simplest viable solution. Complex patterns need explicit justification. Readable code over clever code.
3. **Security By Default** — Validate all inputs. No secrets in code. Defense in depth. Least privilege principle.
4. **Test-Driven Thinking** — Design all code to be testable from inception. Write tests alongside code. Verify before committing.

## Additional Rules

- No new dependencies without explicit approval or compelling justification
- Validate ALL user input ({{VALIDATION_LIBRARY}})
- Never store secrets in source code — use environment variables
- Never concatenate SQL — use parameterized queries only
- Use conventional commits: `type(scope): description`

## Code Style

- Code must be immediately understandable. Use descriptive naming. Maintain clear structure. Readable code over clever code.
- Files: {{FILE_NAMING}} (e.g., `kebab-case.tsx`, `snake_case.py`)
- Components/Classes: PascalCase
- Functions: camelCase with verb prefixes (e.g., `getUserData`, `calculateTotal`)
- Constants: UPPER_SNAKE_CASE
- Explicit return types on all functions
- No `any` types — use `unknown` with type guards

## Security

- Validate all user input on both client and server
- NEVER pass user input to shell commands
- NEVER use `eval()` or `Function()` with user data
- Use httpOnly, secure, sameSite cookies for auth
- Rate limiting on all public endpoints
- CORS: explicit origins only

## Testing

- {{TEST_RUNNER}} for unit tests, {{E2E_RUNNER}} for E2E
- 85% coverage for critical paths (auth, payments, data)
- AAA pattern: Arrange, Act, Assert
- Mock external dependencies, not internal logic

## Commands

```bash
{{INSTALL_COMMAND}}
{{DEV_COMMAND}}
{{TEST_COMMAND}}
{{BUILD_COMMAND}}
```

## Key Files
{{KEY_FILES}}

## Workflow

- Atomic changes: small, self-contained modifications
- Only modify files related to the current task
- Run `{{LINT_COMMAND}}` before committing
- Always run `{{TEST_COMMAND}}` after modifying code
- Use file-scoped commands. Reference docs instead of pasting. Optimize context window usage.
- Follow established conventions for the relevant language and tech stack
- Comment only complex logic or critical functions. Avoid documenting the obvious.
- After generating code, argue against your own solution. Check for redundancy, unnecessary complexity, or simpler alternatives.

## When Uncertain

Ask clarifying questions before implementing. Propose alternatives with pros/cons. Reference existing patterns in the codebase.
