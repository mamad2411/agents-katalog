---
name: backend
description: Implement backend services, business logic, API handlers, jobs, integrations, file processing, authentication flows, and server-side fixes. Use for backend coding and debugging in Node, Python, Go, Java, Rust, PHP, or similar stacks.
---

# Backend

## Workflow

1. Locate existing service, handler, repository, job, and test patterns.
2. Validate input at the boundary and keep domain validation close to business rules.
3. Make error handling explicit and preserve useful failure context.
4. Define transaction boundaries and idempotency for mutating operations.
5. Add logs with stable fields for operational diagnosis.
6. Verify with focused tests or the nearest available runtime command.

## Required Checks

- Do not hardcode secrets, environment-specific paths, or credentials.
- Do not swallow exceptions silently.
- Avoid direct shell, SQL, template, or URL interpolation with untrusted input.
- Set timeouts for external calls when the stack supports it.
- Treat retries as state-changing unless idempotency is guaranteed.

## Output

Summarize changed behavior, files touched, and verification. Mention residual risk if external systems or credentials prevent full testing.
