---
name: on-spring
description: Use when implementing, reviewing, or refactoring Spring backend work for Onflou projects; loads the Onflou Spring Guide and Policy from the knowledge vault before changing APIs, services, controllers, persistence, validation, transactions, or backend tests.
---

# Purpose

Reusable workflow for Onflou Spring backend implementation and review.

# Required Knowledge

Read these knowledge resources before generating architecture, implementation, review comments, reports, or automation for Onflou Spring work:

- [Spring standard overview](../../../70-knowledge/company/onflou/internal/SPRING_BACKEND_STANDARD_v1.0/SPRING%20BACKEND%20STANDARD%20%28v1.0%29.md)
- [Spring Guide](../../../70-knowledge/company/onflou/internal/SPRING_BACKEND_STANDARD_v1.0/SPRING%20BACKEND%20STANDARD%20%28v1.0%29/Guide.md)
- [Spring Policy](../../../70-knowledge/company/onflou/internal/SPRING_BACKEND_STANDARD_v1.0/SPRING%20BACKEND%20STANDARD%20%28v1.0%29/Policy.md)
- [Reference assets](../../../70-knowledge/company/onflou/internal/reference-assets/README.md)
- [Miraen Cardtalk BO Spring Boot config reference](../../../70-knowledge/company/onflou/internal/reference-assets/spring-boot-config/miraen-cardtalk-bo-config/README.md) when working on Spring configuration, filters, security, CORS, HTTP clients, or MVC setup.

# Inputs

- endpoint, service, domain flow, or module
- request payload and response model
- auth, permission, validation, and transaction requirements
- persistence or external integration behavior
- test or verification expectation

# Workflow

1. Load the required Onflou Spring knowledge files.
2. Treat `Policy.md` as mandatory rules and `Guide.md` as recommended conventions.
3. If the task touches Spring configuration, inspect the matching reference asset before designing the change.
4. Identify affected backend surface: API, DTO, validation, service, transaction, repository, integration, configuration, filters, security, tests, or documentation.
5. Validate business rules, domain edge cases, error handling, retries, idempotency, and rollback behavior.
6. Implement or review the smallest sufficient change.
7. Verify behavior with the project's existing backend checks.
8. Record unresolved risks, missing knowledge, or convention conflicts in shared state when necessary.

# Output

- backend implementation, review, plan, or report
- verification summary
- related task, artifact, or log references

# Safety Rules

- Never ignore `Policy.md`.
- Treat reference assets as examples, not mandatory standards.
- Preserve existing API contracts unless the task explicitly requires a contract change.
- Validate edge cases before adding service or transaction logic.
- Consider duplicated execution, timeout retry loops, reconnect duplication, partial failures, and rollback paths.
- Do not run database migrations or destructive operations without explicit human approval.

# Incident References

Related incidents:

- Check `ai-workspace/70-knowledge/incidents/` and Onflou domain knowledge before work that may affect retries, duplicated execution, reconnects, timeouts, rewards, or payments.

# Verification

- Confirm required Onflou Spring knowledge was read or explicitly unavailable.
- Confirm implementation or review aligns with Spring `Policy.md`.
- Confirm business rules, edge cases, and operational failure modes were considered.
- Confirm tests, API checks, or manual verification steps are documented.
