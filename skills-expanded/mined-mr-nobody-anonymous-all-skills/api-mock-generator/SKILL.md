---
name: api-mock-generator
description: Derive API mocks and contract tests from schemas or observed interfaces without inventing behavior.
category: development
aliases:
- api
- mock
- test
- contract
- openapi
- swagger
triggers:
- Generate API mocks
- Create mock API
- API testing
- Mock endpoints
keywords:
- api
- mock
- test
- openapi
- swagger
- rest
- contract
dependencies:
- optional:test-framework
risk: low
version: 1.0.0
source: custom
enabled: true
capabilities:
- api-mock-generator
- development
inputs:
- task
- context
outputs:
- result
- report
lifecycle: enabled
author: Mr-Nobody-Anonymous
tags:
- api
- development
- generator
- mock
- openapi
- test
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# Api Mock Generator

## Purpose
Generate API mocks and contract tests from OpenAPI schemas or observed interfaces.
The skill ensures mocks accurately reflect the API contract without inventing
behavior beyond the specification.

## When to Use
- Setting up local development environments
- Writing contract tests
- Mocking external APIs for testing
- Generating API documentation examples

## When NOT to Use
- For production API implementations
- When a real API is available and accessible
- For security testing (use specialized tools)

## Capabilities
- OpenAPI/Swagger schema parsing
- JSON Schema to mock conversion
- Request/response example generation
- Contract test skeleton generation
- Mock server configuration
- Multi-format support (REST, GraphQL)
- Header and authentication simulation

## Inputs
- `source` (required) — OpenAPI file, JSON Schema, or HAR file
- `format` (optional) — mock-server, contract-tests, examples
- `framework` (optional) — jest, pytest, etc.
- `base_url` (optional) — for mock server

## Workflow
1. **Parse** — Load and analyze schema
2. **Generate** — Create mocks from definitions
3. **Validate** — Ensure mocks match schema
4. **Package** — Generate config files and tests
5. **Document** — Provide usage instructions

## Tools
- OpenAPI parsers
- Mock server tools (Prism, Prism, Mockoon)
- Test framework integration

## Examples
**User:** "Generate mocks from this OpenAPI spec"
**Response:**
```
Parsing openapi.yaml...
Found 15 endpoints, 45 schemas

Generated:
- mock-server.js (Prism mock server)
- contracts.test.js (Jest contract tests)
- examples.json (request/response examples)

Run: npx prism mock openapi.yaml
```

## Safety
- Never mock sensitive data
- Clearly label generated code as mocks
- Don't use mocks in place of real integration tests
- Validate mocks against schema

## Source
Auto-generated from openclawskills.net description.

## Notes
Maintained as part of canonical development category.
