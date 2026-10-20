---
name: wp-rest-api-authentication-and-permissions
description: Selects and reviews WordPress REST API authentication, CSRF protection, capability checks, object-level authorization, credential handling, and negative permission tests. Use for protected routes or remote clients.
license: MIT
compatibility: "General WordPress REST API guidance; checked against WordPress 7.0.1 documentation."
---

# WordPress REST API Authentication and Permissions

## Use this skill when

- Protecting a route.
- Choosing authentication for a same-origin or remote client.
- Reviewing Application Passwords or provider-based authentication.
- Designing object ownership or least-privilege access.
- Investigating `401`, `403`, nonce, or current-user failures.

## Approach

1. Identify client location, user interaction, trust boundary, and transport.
2. Separate authentication, CSRF protection, authorization, and response visibility.
3. Select the narrowest supported authentication mechanism.
4. Map each operation to capability and object-level checks.
5. Define credential storage, rotation, revocation, and incident handling.
6. Implement explicit permission callbacks.
7. Test anonymous, invalid, expired/revoked, underprivileged, authorized, and cross-object cases.
8. Review logs and errors for credential or identity leakage.

## Workflow

Use [authentication-and-permission-review-workflow.md](workflows/authentication-and-permission-review-workflow.md).

## Resources

- [authentication-selection-matrix.md](resources/authentication-selection-matrix.md)
- [permission-test-matrix.md](resources/permission-test-matrix.md)

## Example

- [permission-callback-patterns.md](examples/permission-callback-patterns.md)

## Output

Return:

- Authentication choice and evidence.
- Capability/object permission model.
- Credential lifecycle.
- Permission test matrix.
- Risks, assumptions, and rejected alternatives.
