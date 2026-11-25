---
name: grpc-service-design
description: "Design gRPC services: protobuf evolution rules, streaming choices, deadlines and retries, error model, and load-balancing implications."
type: procedural
category: development
domain: development
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: advanced
triggers:
  - protobuf field evolution
  - grpc streaming design
  - grpc deadline retry
  - grpc error codes
  - grpc load balancing
keywords:
  - grpc
  - protobuf
  - proto3
  - streaming
  - deadline
  - service-mesh
source: custom
enabled: true
---

# gRPC Service Design

## Purpose

Design gRPC services: protobuf evolution rules, streaming choices, deadlines and retries, error model, and load-balancing implications.

## When to Use

- You are defining a new internal service contract with protobuf.
- Streaming versus unary semantics must be chosen deliberately.
- Failures need explicit deadlines, retries and status codes.

## When NOT to Use

- Clients are browsers or third parties without gRPC tooling (use gRPC-Web or REST/JSON).
- The traffic is simple request/response over an existing HTTP API.
- You need long-lived bidirectional sessions where a message broker fits better.

## Capabilities

- Evolve .proto files without breaking wire compatibility.
- Choose unary, server-streaming, client-streaming or bidi with justification.
- Set deadlines, retry policies and idempotency for safe retries.
- Map failures to canonical gRPC status codes.

## Inputs

- The service boundary and its expected request rate and payload sizes.
- Language toolchains in use (protoc plugins, codegen versions).
- The reliability requirement: timeouts, retry budget, idempotency keys.

## Workflow

1. Define messages first; keep field numbers stable and reserve removed ones.
2. Choose the RPC shape from the data flow, not from habit.
3. Add deadlines at every call site and bound retries with jitter.
4. Return canonical status codes with structured error details.
5. Break-check the schema in CI (`buf breaking`) before merging.

## Tools

- protoc / buf
- grpcurl
- service mesh telemetry

## Examples

- `buf breaking --against '.git#branch=main'`
- `buf lint`
- `grpcurl -d '{"id":"1"}' localhost:50051 svc.Orders/Get`

## Safety

- Renaming or renumbering fields breaks wire compatibility silently.
- Streaming without flow control can exhaust memory on either side.
- Retries without idempotency duplicate writes; require idempotency keys.

## Source

All-Skills canonical library (`skills/development/grpc-service-design`). First-party skill, maintained in this repository.

## Notes

- `buf` provides lint, breaking-change detection and generation in one tool.
- Deadlines propagate: an unset deadline can hang a whole call chain.
- Pairs with: `development/graphql-api-design`, `networking/service-mesh`.
