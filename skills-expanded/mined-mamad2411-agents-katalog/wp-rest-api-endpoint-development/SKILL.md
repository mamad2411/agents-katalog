---
name: wp-rest-api-endpoint-development
description: Implements and reviews WordPress REST API routes, controllers, schemas, callbacks, responses, errors, and custom content exposure. Use when adding or changing endpoint code.
license: MIT
compatibility: "General WordPress REST API guidance; checked against WordPress 7.0.1 documentation."
---

# WordPress REST API Endpoint Development

## Use this skill when

- Registering custom routes.
- Building a `WP_REST_Controller`.
- Exposing a custom post type, taxonomy, metadata, settings, or domain resource.
- Adding request schemas, response schemas, links, or errors.
- Refactoring ad hoc callbacks into a maintainable controller.

## Approach

1. Load the approved resource contract.
2. Verify minimum WordPress and PHP support.
3. Register routes on `rest_api_init`.
4. Use a unique versioned namespace.
5. Add an explicit `permission_callback` to every endpoint.
6. Define argument schemas and validation.
7. Use controller preparation methods for non-trivial resources.
8. Return WordPress REST response/error types.
9. Add collection bounds, field contexts, links, and pagination.
10. Add unit, integration, permission, schema, and regression tests.

## Workflow

Use [custom-endpoint-implementation-workflow.md](workflows/custom-endpoint-implementation-workflow.md).

## Resources

- [controller-and-route-patterns.md](resources/controller-and-route-patterns.md)
- [schema-and-error-contract-checklist.md](resources/schema-and-error-contract-checklist.md)

## Example

- [secure-controller-pattern.md](examples/secure-controller-pattern.md)

## Output

Return:

- Implemented route/controller changes.
- Contract and compatibility evidence.
- Permission and validation decisions.
- Test coverage.
- Known risks and follow-up work.
