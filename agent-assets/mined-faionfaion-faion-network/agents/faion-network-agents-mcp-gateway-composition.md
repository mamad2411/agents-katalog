# Mcp Gateway Composition

## Summary

**One-sentence:** Designs an MCP gateway composition (virtual-server / federation / per-client visibility) for an agent connected to ≥5 MCP servers and emits a gateway-spec.

**One-paragraph:** When an agent connects to >5 MCP servers the tool catalog explodes past the ~25-tool selection-accuracy cliff. A gateway in front composes them via virtual-server (curated subset), federation (gateway-of-gateways), or per-client visibility (filtered by user/role). This methodology turns a server inventory into a deterministic gateway-spec covering auth, rate limiting, audit, and namespace collisions.

**Ефективно для:** solopreneur whose agent is connected to 8 MCP servers and is starting to mis-call tools.

## Applies If (ALL must hold)

- Agent connects to ≥5 MCP servers.
- Tool count across servers ≥25.
- ≥1 cross-server concern (auth, namespace collision, rate limiting).
- Gateway runtime available (Node/Python/Go).
- Per-server tool list is enumerable.

## Skip If (ANY kills it)

- ≤3 MCP servers — direct connect is fine.
- Stdio-only single-user — no gateway needed.
- Tools < 25 total — no selection cliff.
- No shared auth concern — direct connect is OK.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `server-inventory.yaml` | servers (name, transport, tools_count, auth_scheme), agent_clients (list, role-tags), shared_concerns | author |
| `Gateway runtime` | Node/Python/Go | infra |
| `Per-server tool lists` | JSON | MCP introspect |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| [[mcp-transport-stdio-vs-http]] | Gateways are HTTP-only. |
| [[mcp-resource-vs-tool-vs-prompt]] | Tool selection cliff is about the Tool primitive. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | Rules r1-r2 for composition patterns and the 5-server / 25-tool thresholds, plus the three tree-branch rules (r-advanced, r-default-high, r-default-low) fixing pattern, curation, namespacing and auth per server count. | ~1200 |
| `content/02-output-contract.xml` | essential | gateway-spec schema + examples. | ~800 |
| `content/03-failure-modes.xml` | essential | Tool list still >25 after gateway, namespace collision, gateway-of-gateways loop, auth bypass. | ~700 |
| `content/04-procedure.xml` | recommended | 6-step design procedure. | ~800 |
| `content/06-decision-tree.xml` | essential | Decision tree | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| Profile parsing | haiku | Mechanical. |
| Decision drafting | sonnet | Tradeoffs require sound reasoning. |
| Code/config emission | sonnet | Mechanical but must compile. |
| Failure-mode cross-check | opus | Catches subtle gaps. |

## Templates

| File | Purpose |
|---|---|
| `templates/server-inventory.yaml` | Input. |
| `templates/gateway-spec.md.j2` | Output. |
| `templates/gateway-spec.md` | Output. Generated from `templates/gateway-spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.yaml` | Minimum. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-mcp-gateway-composition.py` | Validates output against the JSON schema. | Pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[mcp-resource-vs-tool-vs-prompt]]
- [[mcp-transport-stdio-vs-http]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Branches on agent_clients_count (1 → virtual-server; many roles → per-client visibility), then on servers_count (>10 → federation), then on shared_concerns (auth → centralise; rate-limit → enforce at gateway). Each leaf cites a rule id in 01-core-rules.xml so the agent always cites which rule drove the choice — and can be replayed for audit.
