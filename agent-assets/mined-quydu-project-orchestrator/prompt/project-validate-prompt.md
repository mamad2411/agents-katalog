---
mode: agent
description: Validate that a project foundation is ready for governed implementation.
---

# Project Validate

Validate the project foundation before the first implementation objective or after a significant setup change.

## Required process

1. Read repository instructions, the project manifest, blueprint, current handoff, and authoritative reports.
2. Run `/framework-health-check` for framework structure, skill contracts, schemas, profiles, and wiring.
3. Run `/development-environment-readiness` for local tools, runtimes, authentication, debugging, and security gates.
4. Run `/skill-dependency-manager` and confirm all required dependencies resolve without cycles.
5. Confirm source, test, documentation, configuration, and infrastructure boundaries match the blueprint.
6. Run the declared build, test, lint, type-check, and validation commands when they exist; record unavailable commands as blocked, not passed.
7. Run `/security-review` when authentication, authorization, secrets, network exposure, data handling, or deployment configuration is in scope.
8. Write or update the project validation report only after collecting evidence.

## Completion evidence

- Every check is `passed`, `failed`, `blocked`, or `not-applicable` with evidence.
- Missing tools and unresolved placeholders are explicit.
- No secret values are recorded.
- A failed or blocked check prevents a ready decision.
- The next action and owning skill are recorded in the project handoff.
