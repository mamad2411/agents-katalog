---
name: contract-testing
description: Consumer-driven contract testing, OpenAPI spec drift validation, and breaking API change detection for microservices.
version: 1.0.0
---

# Contract Testing & OpenAPI Validation Skill

This skill ensures microservices communicate reliably via explicit, version-controlled contracts without breaking downstream consumers.

## Core Architectural Pillars

### 1. OpenAPI & Schema Drift Validation
- **Spec-First & Code-First Sync**: Enforce strict TypeScript/Zod/JSON Schema generation from OpenAPI 3.1 definitions.
- **Breaking Change Detection**: Run `oasdiff` or `openapi-diff` in CI/CD to block backward-incompatible changes (e.g. removed fields, altered types, tightened validation).

### 2. Consumer-Driven Contract Testing (Pact)
- **Consumer Contracts**: Downstream microservices define expected API requests and responses.
- **Provider Verification**: Upstream microservice verifies actual endpoint execution against consumer expectations before deployment.
- **Pact Broker Matrix**: Track deployment status across environments to prevent deploying incompatible service versions.

### 3. Mock Service Worker (MSW) & Integration Mocks
- **Deterministic API Fixtures**: Shared MSW handlers across unit, component, and E2E tests.
- **Network Level Interception**: Mock API traffic at network level to avoid fragile global fetch overrides.

## Checklist for Slices with `needs_contract_testing: true`
- [ ] OpenAPI 3.1 schema defined or updated
- [ ] Breaking change check passes against `main` branch schema
- [ ] Consumer Pact tests generated or MSW handlers synchronized
- [ ] Provider endpoint verification passes end-to-end
