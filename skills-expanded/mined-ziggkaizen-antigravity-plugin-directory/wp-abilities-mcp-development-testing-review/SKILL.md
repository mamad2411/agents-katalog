---
name: wp-abilities-mcp-development-testing-review
description: Builds and reviews test and release evidence for WordPress Abilities and MCP integrations. Use when adding tests, validating contracts, checking transports, preparing an upgrade, or deciding release readiness.
---

# Testing and Release Review

## Test Layers

- Registration and category lifecycle.
- Input/output schema validation.
- Permission and object-level authorization.
- Execute callback success and `WP_Error`.
- Annotation accuracy and idempotency.
- PHP, JavaScript, REST, and MCP parity.
- Default and custom server behavior.
- HTTP and STDIO transport behavior.
- Compatibility across supported WordPress, PHP, adapter, proxy, and client versions.
- Logging, redaction, disablement, and rollback.

Follow `workflows/test-and-release-workflow.md`.

Use:

- `resources/abilities-mcp-test-matrix.md`
- `examples/php-tests.md`
