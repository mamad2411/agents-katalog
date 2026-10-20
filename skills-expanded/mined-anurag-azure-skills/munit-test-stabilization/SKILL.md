---
name: "munit-test-stabilization"
description: "Author and stabilize MUnit tests for MuleSoft flows: mock connectors, set event payloads/attributes, assert payload/status, coverage. Use during build/validation when Mule tests fail."
version: 1
created: "2026-06-27"
updated: "2026-06-27"
---

# MUnit Test Stabilization

- One MUnit suite per flow; use `mock-when` for HTTP/DB connectors (match by processor + attributes).
- Set up the event with `munit:set-event` (payload, attributes, vars) matching real inputs.
- Assert with `munit-tools:assert-that` on payload, attributes.statusCode, and error type for negative paths.
- Cover success + each error branch (e.g. timeout -> 504). Aim for the configured coverage gate.
- Flaky fixes: deterministic fixtures; avoid real network; freeze time/ids where needed.
- Run via `mvn clean test` (mule-maven-plugin + munit-maven-plugin) before declaring build success.
