---
name: wp-abilities-mcp-development-javascript-rest
description: Consumes WordPress Abilities from JavaScript or REST safely. Use when checking client availability, authentication, permission behavior, request schemas, error handling, or cross-context parity.
---

# JavaScript and REST Consumption

## Process

1. Verify the target WordPress and package versions.
2. Verify whether `wp.abilities`, a registered script handle, or `@wordpress/abilities` is actually available.
3. Keep the server-side Ability as the authorization and validation source of truth.
4. Use the same documented contract across PHP, JavaScript, and REST.
5. Handle missing abilities, rejected permissions, schema errors, network failures, and `WP_Error` responses.
6. Avoid duplicating authorization in client code as if it were authoritative.
7. Test parity across supported contexts.
8. Follow `workflows/consume-ability-workflow.md`.
9. Review `resources/php-javascript-rest-boundary.md`.

See `examples/javascript-client.md`.
