---
name: mcp-integration-business-case
description: Turn "custom integration for every AI-tool pairing" chaos into a quantified MCP consolidation business case — the N×M vs N+M integration-count math, where the savings actually come from (and where the pitch overclaims), and the before/after narrative structure for pitching MCP adoption to a client or internal stakeholder. Use when scoping an MCP integration project, explaining why MCP matters in business (not protocol) terms, or building the ROI case for consolidating point-to-point AI-tool integrations onto MCP servers.
---

# MCP Integration Business Case

Source: reviewed from an uploaded infographic — "MCP · Protocol — The
Universal Connector for AI" (Marios Charalampous / workflows.io), a
Before/After split panel: Before shows every AI client (Claude, ChatGPT,
Cursor) wired directly to every tool (HubSpot, Salesforce, Slack, Apollo,
Clay) in a tangled mesh; After shows all clients routed through one MCP
layer to the same tools. The visual claim — fewer wires — is standard,
accurate MCP positioning. This skill turns it into actual numbers and a
repeatable business-case structure, since the infographic itself is
marketing material for a workflow-automation brand, not a methodology.

## What MCP actually is, in one paragraph

The Model Context Protocol is a standard for how AI applications connect
to external tools and data sources — the same way USB-C standardized
device charging/data cables. It's not a specific product, vendor, or
server; it's a protocol that any AI client (Claude, ChatGPT, Cursor, an
internal agent) and any tool (a CRM, a database, a SaaS app) can both
implement once, instead of every client building a custom connector to
every tool.

## The core math: N×M vs N+M

- **Before (point-to-point):** every AI client that needs a tool gets its
  own custom integration to that tool. Worst case, that's
  `N_clients × M_tools` separate integrations, each with its own auth
  flow, error handling, and maintenance burden.
- **After (MCP hub):** each tool ships *one* MCP server; each client
  implements MCP *once*. That's `N_clients + M_tools` connections total —
  linear instead of multiplicative.

| N clients | M tools | Before (N×M) | After (N+M) | Reduction |
|---|---|---|---|---|
| 3 | 5 | 15 | 8 | 47% |
| 5 | 10 | 50 | 15 | 70% |
| 8 | 20 | 160 | 28 | 83% |

The reduction accelerates as either side grows — this is why the business
case gets stronger, not weaker, the more AI tools and data sources a
client is already juggling. A client with one AI client and two tools
barely benefits (1×2=2 vs 1+2=3 — MCP is *worse* by this count alone);
don't run this pitch on that client.

## Where the savings actually come from

Not "protocol elegance" — three concrete mechanisms:

1. **Maintenance ownership shifts.** One MCP server per tool, maintained
   once (usually by the tool vendor or a platform team), instead of the
   same integration logic duplicated and separately maintained inside
   every AI client that talks to that tool.
2. **New-client onboarding cost drops toward zero.** Adding a 4th AI
   client to a stack that already has 5 MCP-connected tools costs
   approximately nothing extra per tool — the tools are already exposed
   via the standard protocol. Under point-to-point, the 4th client needs
   5 new custom integrations built from scratch.
3. **Auth/permissions centralize per tool.** Each tool's MCP server owns
   its own auth model once, instead of every client-tool pairing
   reimplementing (and re-securing) its own credential handling.

## Where the pitch overclaims — say this part out loud in any real proposal

- MCP does not eliminate the `M` servers. Someone still has to build and
  maintain one MCP server per tool — either the tool vendor ships it
  (increasingly common) or the client has to build/host it themselves.
  Don't present "After" as free.
- Existing custom integrations don't vanish on their own. Migrating off
  them is a real cost (rebuild, test, cut over) that has to be netted
  against the projected savings, not ignored in the pitch.
- If the client only uses one AI client today, the N×M vs N+M gap is
  small — the case is strongest for a client already running ≥2 AI
  tools/clients against several data sources, or one that's about to.
- "Universal connector" is true at the protocol level, not automatically
  true in practice — a given MCP server may only expose a subset of a
  tool's functionality, and quality varies a lot between official and
  community-built servers (see `mcp-integration-scout` for how this repo
  already evaluates that before trusting a connector).

## Business-case structure (the pitch skeleton)

Mirrors the infographic's own Before/After split — use as slide/section
order:

1. **Current-state inventory** — list every AI-client × tool pairing that
   currently has (or would need) a custom integration; count them.
2. **Current-state cost** — build cost + ongoing maintenance cost per
   pairing, summed across the `N×M` count from step 1.
3. **Complexity visualization** — the mesh diagram (every client wired to
   every tool) is the single most effective slide in the source
   infographic; reuse that visual, not just the number.
4. **Target-state via MCP** — the same tools and clients, `N+M`
   connections, hub-and-spoke diagram.
5. **Per-connector build-vs-buy decision** — for each tool, is there
   already an official/community MCP server (buy — adopt it), or does one
   need to be built (build — scope separately, see `mcp-builder` for the
   how-to)?
6. **Migration sequencing** — cut over the highest-maintenance-cost
   pairing first (usually the one duplicated across the most clients),
   not the easiest one first.
7. **Risk/caveats section** — the overclaim list above, stated plainly
   rather than left for the client to discover after signing.

## Related in this repo

- **`mcp-business-case-analyst`** (agent) — runs this skill's N×M vs N+M
  math and drafts the business case for a specific client's actual
  tool/client list.
- **`mcp-integration-scout`** (agent) — checks what's connectable in
  *this* environment right now; use it to populate the build-vs-buy
  decision in step 5.
- **`docs/procedures/mcp-integration-scoping.md`** — the SOP for running
  this end to end on a real client engagement.
- **`Artifacts/business/mcp-integration-business-case.html`** — the live
  before/after calculator and diagram template built from this skill.
- Anthropic's own **`mcp-builder`** skill (global, not vendored here) —
  for actually building an MCP server once step 5 decides one is needed.
