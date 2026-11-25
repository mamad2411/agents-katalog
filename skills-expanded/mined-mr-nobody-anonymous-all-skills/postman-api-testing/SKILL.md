---
name: postman-api-testing
description: "Build API test suites with Postman and Newman: collection structure, environment layering, pre-request auth, assertions and CI runs."
type: procedural
category: testing
domain: testing
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: intermediate
triggers:
  - postman collection tests
  - newman ci pipeline
  - postman environment variables
  - api test assertions
  - postman pre-request script
keywords:
  - postman
  - newman
  - api-testing
  - assertions
  - collections
source: custom
enabled: true
---

# Postman API Testing

## Purpose

Build API test suites with Postman and Newman: collection structure, environment layering, pre-request auth, assertions and CI runs.

## When to Use

- A team already uses Postman and needs the suite to run in CI.
- An API needs executable documentation with assertions.
- Auth and environment handling must be centralised once.

## When NOT to Use

- The project already has a code-based API test suite it can extend.
- The test needs deep database verification beyond HTTP assertions.
- You require contract-schema validation that a dedicated tooling (Dredd, Schemathesis) handles better.

## Capabilities

- Structure collections into folders mirroring the API surface.
- Layer environment and collection variables without hardcoded values.
- Assert status, schema shape and business invariants.
- Run collections headless in CI with Newman and fail on assertion errors.

## Inputs

- The API base URLs per environment and the auth mechanism.
- The endpoints and their expected contracts.
- The CI runner and where reports should be stored.

## Workflow

1. Create one collection per API surface with folders per resource.
2. Keep secrets in environment variables; never commit an environment with tokens.
3. Add a pre-request script to obtain or refresh auth once per run.
4. Assert status code, body shape and at least one business invariant per request.
5. Run `newman run` in CI and publish the HTML/JUnit report.

## Tools

- Postman
- Newman
- CI runner

## Examples

- `newman run collection.json -e staging.postman_environment.json --reporters cli,junit`
- `newman run collection.json --folder orders --bail`
- `newman run collection.json --iteration-data data.csv`

## Safety

- Exported environments can contain live tokens; scan before committing.
- Tests that create or delete resources need cleanup and must never target production without approval.
- Do not assert on volatile values (timestamps, ids) without normalisation.

## Source

All-Skills canonical library (`skills/testing/postman-api-testing`). First-party skill, maintained in this repository.

## Notes

- Collection variables are the right place for derived ids shared across requests.
- `--bail` keeps CI fast by stopping at the first structural failure.
- Pairs with: `testing/load-testing`, `development/api-mock-generator`.
