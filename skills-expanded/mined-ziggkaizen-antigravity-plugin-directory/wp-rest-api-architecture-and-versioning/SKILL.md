---
name: wp-rest-api-architecture-and-versioning
description: Designs WordPress REST API boundaries, resources, namespaces, contracts, compatibility, versioning, and deprecation. Use before adding a new API or making a breaking contract change.
license: MIT
compatibility: "General WordPress REST API guidance; checked against WordPress 7.0.1 documentation."
---

# WordPress REST API Architecture and Versioning

Use this skill before implementation.

## Use this skill when

- Deciding whether to expose data through REST.
- Designing resources, routes, methods, schemas, or error contracts.
- Starting a headless or external integration.
- Adding a new namespace version.
- Planning deprecation or migration.

## Approach

1. Confirm exact WordPress, PHP, client, authentication, hosting, and support requirements.
2. Use the boundary matrix to confirm REST is appropriate.
3. Identify consumers, trust boundaries, data classification, ownership, and side effects.
4. Model resources and relationships rather than mirroring database tables.
5. Define namespace, routes, methods, arguments, response schema, errors, headers, links, and pagination.
6. Classify each operation as safe, idempotent, mutating, or destructive.
7. Define compatibility, deprecation, migration, observability, and rollback.
8. Produce testable acceptance criteria before coding.

## Workflow

Use [rest-api-design-workflow.md](workflows/rest-api-design-workflow.md).

## Resources

- [api-boundary-decision-matrix.md](resources/api-boundary-decision-matrix.md)
- [resource-contract-checklist.md](resources/resource-contract-checklist.md)
- [versioning-and-deprecation-policy.md](resources/versioning-and-deprecation-policy.md)

## Output

Return:

- Boundary decision and rationale.
- Compatibility baseline.
- Consumer and trust-boundary map.
- Resource and route contract.
- Authentication and authorization model.
- Versioning and deprecation policy.
- Test, observability, migration, and rollback plan.
- Explicit out-of-scope items.
