---
name: platform-engineering
description: "Run an internal platform: golden paths, self-service templates, paved-road CI, tenant isolation and measuring developer experience."
type: procedural
category: devops
domain: devops
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: medium
level: advanced
triggers:
  - internal developer platform
  - golden path template
  - platform team responsibilities
  - self service infrastructure
  - developer experience metrics
aliases:
  - idp
  - platform-team
keywords:
  - platform-engineering
  - golden-path
  - self-service
  - idp
  - backstage
  - tenancy
mcp_servers:
  - kubernetes
  - terraform
  - github
source: custom
enabled: true
---

# Platform Engineering

## Purpose

Run an internal platform: golden paths, self-service templates, paved-road CI, tenant isolation and measuring developer experience.

## When to Use

- Teams repeatedly rebuild the same CI, deploy and observability setup.
- Onboarding a service takes days of ticket ping-pong.
- There is a platform team with no measurable product.

## When NOT to Use

- The organisation has two services and one team.
- The mandate is to centralise control rather than reduce friction.
- A single pipeline fix is all that is actually needed.

## Capabilities

- Define one golden path per common workload type and make it the default.
- Ship templates that generate working, observable services.
- Provide self-service with guardrails and quotas rather than ticket queues.
- Isolate tenants and bound blast radius by default.
- Measure time-to-first-deploy and platform adoption, not ticket counts.

## Inputs

- The workload archetypes: web service, batch job, event consumer, static site.
- The current friction inventory from real teams.
- Compliance constraints that must be baked in.

## Workflow

1. Interview teams and measure time-to-first-deploy for a new service.
2. Pick the top two archetypes and build one template each, end to end.
3. Bake in logging, metrics, alerts, security scanning and a deploy pipeline.
4. Expose self-service creation with quotas, and make the generated repo the source of truth.
5. Publish a deprecation and upgrade path for the template.
6. Track adoption and time-to-first-deploy quarterly; retire what nobody uses.

## Tools

- backstage
- terraform
- kubernetes
- github
- argocd

## Examples

- `A template that opens a PR with service, pipeline, dashboards and alerts turns a two-week setup into twenty minutes.`
- `Golden paths work when they are the easiest option, not when they are mandated.`

## Safety

- Self-service must never allow unbounded spend or cluster-wide permissions.
- Centralising a platform centralises the outage; design for per-tenant failure.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `kubernetes` | stdio | full | high | `KUBECONFIG` |
| `terraform` | stdio | full | medium | — |
| `github` | http | standard | medium | `GITHUB_PERSONAL_ACCESS_TOKEN` |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/devops/platform-engineering`). First-party skill, maintained in this repository.

## Notes

- A platform without a product owner becomes a ticket queue.
- Measure the teams' experience, not the platform's feature list.
- Pairs with: `disaster-recovery`, `cloudflare-workers`.
