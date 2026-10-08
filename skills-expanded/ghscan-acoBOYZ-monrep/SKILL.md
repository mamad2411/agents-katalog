---
name: effect-services
description: >
  Effect services and Layers for backend code—Context Tag, Layer composition,
  injecting SQL/clients and dependencies. Use when wiring services, Layers, or
  when the user mentions effect-services, Context.Tag, or Layer. Backend only.
metadata:
  type: core
  library: agent-skills
  library_version: '0.5.2'
sources:
  - 'monrep/monrep-mono:packages/agent-skills/skills/effect-services/SKILL.md'
  - 'monrep/monrep-mono:packages/effect-solutions/upstream/packages/website/docs/04-services-and-layers.md'
---

# Effect services & Layers (backend only)

**Backend only** (`services/*`, `@core/*`). Do not edit
`packages/effect-solutions/upstream/`.

After load, read **one** doc:

[`packages/effect-solutions/upstream/packages/website/docs/04-services-and-layers.md`](packages/effect-solutions/upstream/packages/website/docs/04-services-and-layers.md)

Use Tags + Layers for injectable dependencies (SQL pools, Redis, clients)
instead of threading globals through every handler.
