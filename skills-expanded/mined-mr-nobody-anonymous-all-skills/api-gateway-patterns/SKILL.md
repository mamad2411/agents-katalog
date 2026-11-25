---
name: api-gateway-patterns
description: "Design API gateways: routing and path conventions, auth offload, rate limiting, request/response transformation, and observability at the edge."
type: procedural
category: networking
domain: networking
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: medium
level: advanced
triggers:
  - api gateway routing design
  - gateway auth offload
  - edge rate limiting
  - gateway request transformation
  - gateway observability
keywords:
  - api-gateway
  - routing
  - rate-limit
  - auth
  - edge
  - kong
  - envoy
source: custom
enabled: true
---

# API Gateway Patterns

## Purpose

Design API gateways: routing and path conventions, auth offload, rate limiting, request/response transformation, and observability at the edge.

## When to Use

- Multiple services need one stable public entry point.
- Cross-cutting concerns (auth, quotas) should be centralised.
- Traffic shape and observability must be managed at the edge.

## When NOT to Use

- There is one service and a gateway adds a hop without benefit.
- Service-to-service traffic is already handled by a mesh.
- The team cannot operate another critical component.

## Capabilities

- Define route and versioning conventions that stay stable.
- Offload token validation and coarse authorization to the edge.
- Apply per-client quotas with burst handling.
- Emit consistent access logs, metrics and traces at the edge.

## Inputs

- The public API surface and its consumers.
- Authentication mechanism and the identity provider.
- Traffic expectations: peak RPS, tenant isolation requirements.

## Workflow

1. Inventory public endpoints and group them by audience.
2. Define the routing table with explicit versioning and deprecation policy.
3. Decide what the edge enforces (auth, quota, payload limits) and what services own.
4. Add rate limits per client id, not per IP only.
5. Instrument the gateway and confirm trace propagation into services.

## Tools

- Kong / Envoy / AWS API Gateway / nginx
- an identity provider
- OpenTelemetry

## Examples

- `curl -s -I https://api.example/v1/orders`
- `allskills mcp install --harness claude --servers openapi`
- `allskills route "design api gateway routing"`

## Safety

- A gateway misconfiguration can expose internal routes; default-deny unknown paths.
- Rate limits per IP punish NAT'd clients; key on identity where available.
- Never terminate TLS with deprecated protocols at the edge.

## Source

All-Skills canonical library (`skills/networking/api-gateway-patterns`). First-party skill, maintained in this repository.

## Notes

- The gateway is the right place for coarse authorization, not domain rules.
- Trace propagation from the edge is what makes distributed debugging possible.
- Pairs with: `networking/service-mesh`, `integration/third-party-api-resilience`.
