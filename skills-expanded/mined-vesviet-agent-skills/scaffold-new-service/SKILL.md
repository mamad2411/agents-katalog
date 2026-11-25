---
name: scaffold-new-service
description: Bootstrap a new service or bounded component from repo-local templates and conventions. Use when creating a new service, worker, or deployable unit without assuming a fixed framework or folder layout.
version: 1.0.0
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Scaffold New Service

Use this skill to bootstrap new microservices, workers, or bounded components using Hexagonal Architecture, schema-first contracts, and sandbox isolation.

## When to Use

- creating a brand-new microservice, event worker, or deployable backend unit
- bootstrapping from schema-first contracts (OpenAPI 3.1, Protobuf, AsyncAPI)
- setting up Hexagonal Architecture layers (`api/`, `cmd/`, `internal/biz/`, `internal/service/`, `internal/data/`)
- wiring centralized RFC 9457 error handling, OTel observability, and health probes from commit 1
- establishing sandbox-ready rootless Docker and test harness configurations

## Core Rules

- **Hexagonal Architecture layout**: structure the codebase into decoupled layers (`api/` for contracts, `cmd/` for entrypoints, `internal/biz/` for pure domain logic/ports, `internal/service/` for inbound handlers, `internal/data/` for outbound persistence/clients)
- **Schema-first contract binding from commit 1**: bootstrap the service from an immutable OpenAPI 3.1, AsyncAPI, or Protobuf specification; generate typed models and server stubs directly from the contract
- **Centralized RFC 9457 error subsystem**: wire global error handling middleware, a domain error catalog, and sanitized 5xx problem details with `trace_id` from the initial commit
- **Sandbox readiness**: generate a multi-stage rootless `Dockerfile` (`USER nonroot`, read-only rootfs compatibility) and local test harness compatible with Level 0 air-gapped sandboxes (`--network=none`) per `core/policies/execution-sandbox.md`
- **Observability from commit 1**: implement `/health/live`, `/health/ready` probes and initialize OpenTelemetry tracer bootstrap with trace context propagation
- **Dependency injection**: use compile-time DI (Wire, Fx, or repo standard) for all constructor injection; no global state or `init()` singletons
- **Ousterhout Deep Modules & Seam Discipline**: design thin, stable public interfaces hiding deep implementations; apply *The Deletion Test*, *Design It Twice*, and the Two-Adapter rule (*1 adapter = hypothesis, 2+ adapters = proven seam*), keeping tests anchored to the public interface seam
- **Zero secrets in scaffold**: declare environment configurations and secret bindings via external secret stores; reject hardcoded credentials
- detailed directory layouts, Dockerfiles, and deep-module design guides: [`references/service-scaffolding-guide.md`](references/service-scaffolding-guide.md) and [`references/deep-modules-and-seams.md`](references/deep-modules-and-seams.md)

## Suggested Process

### 1. Define Bounded Context & Freeze Invariant Contract

Specify domain boundaries and service ownership. Author or ingest the invariant interface contract (`api/openapi.yaml` or Protobuf). Validate schemas before scaffolding code.

### 2. Scaffold Hexagonal Directory Layout

Generate the directory structure: `api/` (contracts), `cmd/server/` (main entrypoint), `internal/biz/` (domain entities and port interfaces), `internal/service/` (inbound transport handlers), and `internal/data/` (repositories) per [`references/service-scaffolding-guide.md`](references/service-scaffolding-guide.md).

### 3. Wire RFC 9457 Structured Error Subsystem

Create the domain error catalog. Implement the global RFC 9457 error middleware to ensure deterministic error responses with zero stack trace leaks on 5xx failures.

### 4. Wire Baseline Observability & Probes

Implement Kubernetes lifecycle probes (`/health/live` and `/health/ready`). Bootstrap OpenTelemetry SDK tracing and attach spans to primary service boundaries.

### 5. Configure Sandbox Containerization

Create an unprivileged multi-stage `Dockerfile` (`USER 1000:1000` / `nonroot`) supporting `--read-only` filesystem mounts. Configure test harnesses to execute with `--network=none`.

### 6. Verify in Sandbox & Emit Delivery Result

Use skill: `write-tests`. Verify build compilation, health probes, and initial unit tests inside a Level 0 air-gapped sandbox. Emit `contracts/schemas/implementation-result.json`.

## Checklist

- [ ] bounded context defined and anchored to schema-first contract (OpenAPI 3.1 / Protobuf)
- [ ] Hexagonal / Clean architecture directory layout created (`api/`, `cmd/`, `internal/`)
- [ ] centralized RFC 9457 structured error handling subsystem wired from commit 1
- [ ] baseline observability (`/health/live`, `/health/ready`, OTel SDK bootstrap) wired
- [ ] sandbox-ready rootless Dockerfile (`USER nonroot`, `--read-only` compatible) generated
- [ ] dependency injection configured without global singletons
- [ ] tests executed and passing inside Level 0 air-gapped sandbox (`--network=none`)
- [ ] `implementation-result.json` emitted with valid fields and verified against schema

## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **`contracts/schemas/implementation-result.json`** — Required fields: `change_summary`, `files_touched[]`, and `validation_run`. Set `produced_by_role` to the emitting developer role.

Skip emission for solo refactor work where no downstream handoff is expected.

## Failure Modes

- **Ad-hoc directory freehanding**: scaffolding arbitrary folder structures without layer decoupling. Mitigation: enforce Hexagonal Architecture boundaries.
- **Service scaffolded without observability**: missing OTel or health probes. Mitigation: enforce `/health/live`, `/health/ready`, and OTel bootstrap on commit 1.
- **Root execution in containers**: Dockerfile running as root user. Mitigation: mandate `USER nonroot` in runtime stage.
- **Ad-hoc error responses**: service emitting custom JSON strings or HTML error pages. Mitigation: global RFC 9457 middleware.
- **Hardcoded secrets in template**: committing mock credentials. Mitigation: platform secret management and secret scanner verification.

## Security Guardrails (OWASP ASI)

- **ASI04 Supply Chain**: verify template packages against official registries; reject unpinned dependencies or unofficial scaffolding binaries.
- **ASI05 RCE Guard**: never interpolate untrusted strings into code templates or scaffolding shell scripts.
- **ASI07 Inter-Agent Communication**: emit structured `implementation-result.json` so coordinating and reviewing roles can verify setup deterministically.
- **ASI09 Human-Agent Trust Exploitation**: surface scaffolding completeness, residual configuration needs, and sandbox test results honestly.

## Related Skills

- **create-migration**: Add initial schema changes if the service owns data
- **write-tests**: Add safety-net coverage
- **setup-deployment**: Add deployable source-of-truth config
- **add-telemetry-instrumentation**: Wire baseline observability for the new service
- **review-service**: Check readiness before wider rollout
- **commit-code**: Prepare the new service work for delivery
