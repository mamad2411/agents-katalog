# GitHub Copilot Instructions

## Design
- Use approaches that integrate well with the existing codebase and architecture.
- Keep code organized in the appropriate modules or layers.
- Write code that is clear, logical, and makes sense in its context.
- Avoid hacks or workarounds unless clearly justified and documented.

## Functionality
- Ensure the code does what it is supposed to do.
- Cover common edge cases where applicable.
- Handle errors with appropriate messages and HTTP status codes.
- Avoid obvious performance bottlenecks.
- Code should be runnable, testable, and demonstrable.

## Complexity
- Prefer simple, readable code over overly clever or complex implementations.
- Favor many small, focused functions instead of one large, dense function.
- Avoid both over-engineering and oversimplifying.
- Code should be easy to understand now and in the future.
- Strive for the right level of abstraction — not too hardcoded, not too generic.

## Tests
- Include meaningful unit, integration, or end-to-end tests when appropriate.
- Tests should be clear, correct, and useful — not just present.
- Treat test code with the same level of care and review as production code.

## Naming
- Use names that are descriptive and concise.
- Avoid overly long or overly short names.
- Names should clearly communicate the purpose of the variable, function, or module.

## Comments
- Code should be self-explanatory as much as possible.
- Use comments to explain **why** something is done, especially if it's non-obvious.
- Only explain **what** the code does in complex or unusual cases.
- Avoid excessive commenting; focus on clarity.
- Clearly mark TODOs, and clarify if they are for now or later.

## Security
- Validate all inputs using schema validators or similar tools.
- Sanitize or escape all output to prevent injection vulnerabilities.
- Enforce authorization checks on protected actions.
- Never hardcode secrets, credentials, or API keys.
- Handle errors securely — avoid exposing internal implementation details.
- Apply CSRF and XSS protection where relevant.
- Review new dependencies for security and trust.
- Add appropriate security headers or middleware where needed.
