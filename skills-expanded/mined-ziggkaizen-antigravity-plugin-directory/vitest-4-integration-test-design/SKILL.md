---
name: vitest-4-integration-test-design
description: Designs Vitest 4 service-level integration tests with explicit boundaries, local fakes, test projects, tags, setup, teardown, and no accidental external network calls. Use when verifying module interactions or service contracts beyond isolated unit tests.
license: MIT
compatibility: Vitest 4.x, Node.js 20+, and Vite 6+ when Vite integration is used.
---

# Vitest 4 Integration Test Design

Use this skill when a test needs to verify behavior across modules, adapters, services, local protocols, persistence seams, or application boundaries.

## Workflow

- `workflows/integration-test-design-workflow.md`: Use when designing or reviewing integration tests.

## Resource

- `resources/integration-test-boundary-checklist.md`: Use to choose boundaries, dependencies, cleanup, and tags/projects.

## Example

- `examples/service-integration-test-example.md`: Reference example for a local in-process integration test.

## Integration Test Principles

- Define the exact boundary under test.
- Prefer local in-process fakes, local test servers, temporary directories, and disposable test data.
- Do not hit live third-party services in routine integration tests.
- Use explicit setup and teardown.
- Use `test.projects` for separate integration configuration when useful.
- Use Vitest 4.1 tags only after confirming the installed version supports them.
- Keep integration tests slower than unit tests only when the extra confidence is worth it.
