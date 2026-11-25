---
name: golang-ddd-infrastructure
description: "Support Go services by keeping infrastructure, security boundaries, and automated tests aligned with the application architecture. Use when working on Terraform, Cloud Run, Cloud Build or CI, docker-compose environments, integration or component test setup, repository authorization boundaries, service-to-service authentication, or secure internal operations."
user-invocable: true
license: MIT
compatibility: Designed for Codex, Claude Code, Gemini CLI, Cursor, OpenCode, and similar AI coding agents working with Go services.
metadata:
  author: joeyave
  version: "0.3.0"
---

# Golang DDD Infrastructure

Use this skill when infrastructure or delivery work must reinforce the service architecture instead of leaking into the domain model or weakening safety guarantees.

## Start Here

- Treat infrastructure as support for the service design, not the place where missing application boundaries are patched over.
- Use this skill after the service boundaries are at least roughly clear, or when CI, auth, or repository design is now blocking development.

## Workflow

1. Keep infrastructure declarative.
- Prefer Infrastructure as Code over click-ops.
- Group repeated infrastructure shapes into Terraform modules or similarly clear abstractions.

2. Wire services explicitly.
- Pass service endpoints, credentials, and environment differences through well-named configuration.
- Avoid smuggling infrastructure-specific details into domain packages.

3. Make the test pyramid real.
- Keep domain tests fast and local.
- Use integration tests for adapters and transaction behavior.
- Use component tests for one service with mocked externals.
- Keep end-to-end coverage selective and avoid making it the default safety net.

4. Design for stable CI.
- Run tests automatically in the pipeline.
- Keep non-unit tests parallel-safe and deterministic.
- Avoid `sleep`-based synchronization; wait on explicit readiness or eventual conditions.

5. Keep security explicit.
- Do not use fake users or hidden context values for privileged internal updates.
- Prefer explicit roles, commands, or repository methods with names that signal security implications.
- Keep service-to-service authentication and permissions visible in configuration and adapter code.

6. Preserve architectural boundaries.
- Infrastructure may compose ports and adapters, but it must not force the domain to know about deployment details.
- If a repository or handler needs special internal behavior, name it explicitly instead of adding magic flags.

## Use These References

- Read [references/infra-and-delivery.md](references/infra-and-delivery.md) for Terraform, Cloud Run, and CI patterns that fit this style.
- Read [references/testing-and-security.md](references/testing-and-security.md) for test architecture and secure-by-design repository guidance.

## Deliverables

- infrastructure that can be reviewed as code,
- explicit service wiring and permissions,
- a CI path that runs the right tests automatically,
- integration and component tests that are deterministic,
- internal operations with explicit security boundaries.
