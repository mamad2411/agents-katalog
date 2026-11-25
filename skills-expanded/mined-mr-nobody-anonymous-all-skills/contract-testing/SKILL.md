---
name: contract-testing
description: "Test service boundaries with contracts: consumer-driven pacts, provider verification, schema compatibility and versioning without coordination meetings."
type: procedural
category: testing
domain: testing
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: advanced
triggers:
  - consumer driven contract testing
  - pact broker setup
  - provider verification contract
  - api schema compatibility breaking
  - microservice contract test
aliases:
  - pact
keywords:
  - contract-testing
  - pact
  - consumer-driven
  - provider
  - schema
  - compatibility
mcp_servers:
  - github
  - openapi
  - postman
source: custom
enabled: true
---

# Contract Testing

## Purpose

Test service boundaries with contracts: consumer-driven pacts, provider verification, schema compatibility and versioning without coordination meetings.

## When to Use

- Services deploy independently and integration breaks at runtime.
- End-to-end environments are too slow or too shared to trust.
- A provider cannot know what consumers actually rely on.

## When NOT to Use

- There is a single deployable with no separate consumers.
- The team cannot publish or version contracts anywhere shared.
- The integration is a third-party API you do not control.

## Capabilities

- Capture consumer expectations as executable contracts.
- Verify providers against every registered consumer contract.
- Detect breaking schema changes before deploy.
- Version contracts and retire obsolete interactions.
- Replace fragile shared-staging tests with contract checks plus a few E2E smoke tests.

## Inputs

- The consumer/provider pairs and their deployment independence.
- A contract broker or a versioned repository for pacts.
- The API versioning policy.

## Workflow

1. Identify real consumer interactions, not the full API surface.
2. Write the consumer test so it generates a pact on each run.
3. Publish pacts with version and branch/environment tags.
4. Verify the provider in CI against the deployed consumer versions.
5. Block deploys that break a verified consumer, not everything that changes.
6. Prune interactions for consumers that no longer exist.

## Tools

- pact
- pactflow
- schemathesis
- openapi-diff

## Examples

- `Verifying six consumer pacts takes seconds; a shared staging environment takes an hour and lies.`
- `A schema diff catching a removed field is cheaper than a runtime 500 in production.`

## Safety

- Contracts are not a security control; authorisation still needs its own tests.
- Never let a provider mark a consumer's contract as obsolete without the owner's confirmation.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `github` | http | standard | medium | `GITHUB_PERSONAL_ACCESS_TOKEN` |
| `openapi` | stdio | full | medium | `OPENAPI_SPEC_PATH` |
| `postman` | stdio | full | medium | `POSTMAN_API_KEY` |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/testing/contract-testing`). First-party skill, maintained in this repository.

## Notes

- Contract tests complement E2E; they do not prove business flows.
- Version the pact, not just the API.
- Pairs with: `mutation-testing`, `api-security-testing`.
