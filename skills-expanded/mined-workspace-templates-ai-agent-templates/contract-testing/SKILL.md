---
name: contract-testing
description: Adds consumer-driven contract tests between services so a breaking API change fails in CI before it ships to the service that depends on it.
---

# Contract testing

The consumer writes down what it relies on. The provider proves it still delivers that.

## Steps

1. Identify the pair: one consumer, one provider, one interface (HTTP endpoint or message). Do one pair at a time.
2. Check what the project already uses (Pact, Spring Cloud Contract, schema files). Reuse it. If nothing exists, default to Pact for HTTP and message interactions.
3. Consumer side: record each interaction the consumer code really performs, using its real client. Include the request, the status and only the response fields the consumer reads. Use matchers for types and formats, not literal values.
4. Cover failure responses the consumer handles: 404, 409, 422, 500 with an error body.
5. Publish the contract with the consumer version and branch, to a broker or a shared folder.
6. Provider side: replay every pending contract against the real provider with seeded state through provider states ("order 42 exists"). Fail the build on any mismatch.
7. Gate deploys: before releasing either side, check that the pair is compatible.

## Rules

- Never assert fields the consumer ignores. Over-specified contracts block safe changes.
- Never point contract tests at a shared staging environment.
- Additive changes must pass. Removing or retyping a used field must fail.

## Report

The interactions covered, the files added, the CI step, and one demonstration: rename a field in the provider and show the verification fail.
