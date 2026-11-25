---
name: convert-to-stateful
user-invocable: false
description: Convert existing WireMock stubs to be stateful using the key-value state store. Use when the user wants mock API resources to persist across requests (create, retrieve, update, delete).
argument-hint: "<mock-api-name-or-id>"
allowed-tools:
  - Read(../references/*)
  # @variant:remote
  - "{{WIREMOCK_TOOL_PREFIX}}create_upload"
  # @variant:local
  - "{{WIREMOCK_TOOL_PREFIX}}make_http_request"
  # @endvariant
  - "{{WIREMOCK_TOOL_PREFIX}}who_am_i"
  - "{{WIREMOCK_TOOL_PREFIX}}search_my_mock_apis"
  - "{{WIREMOCK_TOOL_PREFIX}}search_stub_mappings"
  - "{{WIREMOCK_TOOL_PREFIX}}import_stubs_to_mock_api"
  - "{{WIREMOCK_TOOL_PREFIX}}update_stub_mapping"
  - "{{WIREMOCK_TOOL_PREFIX}}delete_stub_mapping"
  - "{{WIREMOCK_TOOL_PREFIX}}search_request_journal"
  - "{{WIREMOCK_TOOL_PREFIX}}reset_request_journal"
  - "{{WIREMOCK_TOOL_PREFIX}}push"
  - "{{WIREMOCK_TOOL_PREFIX}}look_up_documentation"
---

## Prerequisites

This skill requires the **WireMock Cloud MCP** server to be configured and running. If it is unavailable, stop and inform the user before proceeding.

## Reference Documentation

Read these references before converting stubs:

- [Stateful Stubbing](../references/stateful-stubbing.md) - full guide to stateful mocking with the key-value state store, including examples
- [Stub Creation Guidelines](../references/stub-creation.md) - rules for creating and importing stubs
- [Response Template Authoring](../references/response-templating.md) - guidelines for Handlebars response templates and brace collision avoidance
- [Validating and Fixing Stubs](../references/validating-and-fixing.md) - process for validating stubs and fixing errors
- [Transferring Files To and From a Mock API](../references/file-transfer.md) - the upload flow used by `push`

## Instructions

The target mock API is: **$ARGUMENTS**

If `$ARGUMENTS` is empty, ask the user which mock API to convert.

1. Identify the target mock API using `search_my_mock_apis`.
2. Read the [Stateful Stubbing](../references/stateful-stubbing.md) and [Response Template Authoring](../references/response-templating.md) references.
3. Fetch the existing stubs using `search_stub_mappings` and review them.
4. Ask the user which resource collections to make stateful (or all of them).
5. Convert stubs to be stateful following the patterns in the stateful-stubbing reference:
   - Add `serveEventListeners` with appropriate state operations (SET, REQUEST_VAR, DELETE, DELETE_CONTEXT)
   - Enable response templating with `"transformers": ["response-template"]`
   - Create 404 not-found stubs with `require-state` and `"absent": true`
   - Use `jsonMerge` for creating and updating resources
6. Import the new stateful stubs and delete the old non-stateful versions.
7. Validate using the process in [Validating and Fixing Stubs](../references/validating-and-fixing.md).
8. Smoke test by creating and retrieving a resource to confirm the stateful flow works.
# @variant:remote
   Use `curl` via `Bash` — there is no MCP tool for making arbitrary HTTP requests.
# @variant:local
   Use the `make_http_request` tool.
# @endvariant
