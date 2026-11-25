---
name: create-stubs
user-invocable: false
description: Create and import WireMock stubs for a mock API. Use when the user wants to add new stub mappings to a WireMock Cloud mock API.
argument-hint: "<mock-api-name-or-id>"
allowed-tools:
  - Read(../references/*)
  - "{{WIREMOCK_TOOL_PREFIX}}who_am_i"
  - "{{WIREMOCK_TOOL_PREFIX}}search_my_mock_apis"
  - "{{WIREMOCK_TOOL_PREFIX}}search_stub_mappings"
  - "{{WIREMOCK_TOOL_PREFIX}}import_stubs_to_mock_api"
  - "{{WIREMOCK_TOOL_PREFIX}}search_request_journal"
  - "{{WIREMOCK_TOOL_PREFIX}}reset_request_journal"
  - "{{WIREMOCK_TOOL_PREFIX}}look_up_documentation"
  - "{{WIREMOCK_TOOL_PREFIX}}pull"
---

## Prerequisites

This skill requires the **WireMock Cloud MCP** server to be configured and running. If it is unavailable, stop and inform the user before proceeding.

## Reference Documentation

Read these references before creating stubs:

- [Stub Creation Guidelines](../references/stub-creation.md) - rules for creating and importing stubs
- [Validating and Fixing Stubs](../references/validating-and-fixing.md) - process for validating stubs and fixing errors
- [Transferring Files To and From a Mock API](../references/file-transfer.md) - the download flow used by `pull`

## Instructions

The target mock API is: **$ARGUMENTS**

If `$ARGUMENTS` is empty, ask the user which mock API to create stubs for.

1. Identify the target mock API using `search_my_mock_apis`.
2. Read the [Stub Creation Guidelines](../references/stub-creation.md).
3. Gather requirements from the user about what stubs to create (endpoints, methods, response data, scenarios).
4. If an OpenAPI description is available for the mock API, pull it (see [Transferring Files To and From a Mock API](../references/file-transfer.md) for how `pull` works) and use it to ensure responses conform to schemas.
5. Create the stubs and import them using `import_stubs_to_mock_api`.
6. Validate the imported stubs using the process in [Validating and Fixing Stubs](../references/validating-and-fixing.md).
7. Report the created stubs to the user.
