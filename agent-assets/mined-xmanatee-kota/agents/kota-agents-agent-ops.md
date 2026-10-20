# Agent Ops Module

This module owns the reflective `kota agent` CLI surface and the
`agents` `KotaClient` namespace.

- `index.ts` — `kota agent list` and `kota agent inspect` commands plus
  the top-level `localClient(ctx)` factory and `controlRoutes` for the
  daemon-control surface.
- `agent-ops-operations.ts` — shared `listAgents` / `inspectAgent` helpers
  that both the local handler and the daemon-control routes call through,
  so the two transports cannot diverge on agent shape.

Keep this module read-only and reflective. It should inspect the loaded
module set (`ctx.getModuleSummaries()`), not maintain a parallel agent
catalog. CLI action handlers consume `ctx.client.agents.<method>()` and
never resolve agent definitions through `ModuleContext` directly.
