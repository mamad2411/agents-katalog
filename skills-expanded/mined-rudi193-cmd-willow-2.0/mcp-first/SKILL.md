---
name: mcp-first
description: Fleet orientation — MCP before grep/Bash, wired servers from manifest, operator voice from sessions not GitHub.
---
@markdownai

# MCP-first (fleet doctrine)

> **Read when:** boot step 14, before inventing scripts, before scraping GitHub for "operator voice," before `Grep`/`Bash` on fleet stores.
>
> **Not in scope:** full tool schema — use `fleet_tool_guide` or `sap/mcp_registry.json` when you need depth.

---

## How you log in (orient)

Run **in parallel** at session start (Phase 2 boot):

| Call | What you get |
|------|----------------|
| `boot_digest(app_id=<agent>, workspace=<repo>)` | Verified handoff claims, next bite, **`tools:` line = wired MCP servers** |
| `willow_status` or `fleet_status(app_id=<agent>)` | Postgres, SOIL, Kart queue, watchmen |
| `handoff_latest(app_id=<agent>, workspace=<repo>)` | Session continuity (cold boot / `fast_path: no`) |

**`app_id`** = fleet identity (`WILLOW_AGENT_NAME` / `.willow/active-agent`) — not persona, not dispatch target.

Postgres down in **private-config** → hard stop. Grove down → degraded, continue.

---

## Which MCPs exist (manifest)

**Do not guess.** Read what this workspace actually wired:

1. **`boot_digest`** → `digest.sections.mcp_inventory.mcp_servers` (e.g. `willow`, `codebase-memory-mcp`)
2. **IDE** → `.cursor/mcp.json` / `.mcp.json` in repo root
3. **`fleet_tool_guide(app_id=<agent>)`** → grouped verbs for active `WILLOW_MCP_PROFILE`

Typical Willow 2.0 desk:

| Server | Role | Reach via |
|--------|------|-----------|
| **willow** | Fleet memory, SOIL, KB, sessions, Kart, handoffs, facades | `willow_*`, `kb_*`, `soil_*`, `session_query`, `fleet_*`, `agent_task_submit` |
| **codebase-memory-mcp** | Code graph, call paths | **Prefer Willow wrappers:** `cbm_status` → `cbm_search` / `cbm_trace` / `cbm_verify_callers` |
| **safe-app-willow-grove** *(when wired)* | Bus messaging | `grove_*` on Grove server — not willow |

Other MCPs may appear per project manifest. **Inventory before adding a twelfth tool.**

---

## How it works (thin routing)

**Facades first** (minimal profile):

```
willow_status → willow_attention → willow_find → willow_remember → willow_run
```

| Intent | MCP lane | Not this |
|--------|----------|----------|
| Orient / health | `willow_status`, `boot_digest` | `psql`, raw `systemctl` in Bash |
| Find anything | `willow_find(scope=auto\|kb\|state\|handoffs\|sessions\|code)` | `Grep` repo before MCP |
| Remember | `willow_remember`, `kb_ingest` (+ `mem_check`) | ad-hoc markdown in repo |
| Shell / pytest / git | `willow_run` / `agent_task_submit` + `kart_task_run` | agent `Bash` (fleet-blocked) |
| Code symbols / callers | `cbm_status` → `cbm_search` / `cbm_trace` | new Kart inventory scripts |
| Operator flags / doctrine | `soil_search_all`, `soil_get` | grep `~/.willow` |
| Session history | `session_query` | read JSONL trees by hand |
| Render skills / contract | `mai_read_file(path=…)` | IDE Read when hooks block |
| Web | `willow_web_search`, `willow_web_fetch` | native WebFetch |

**Rule:** `kb_search` before build. `mem_check` before `kb_ingest`. Pull Grove before post.

---

## Operator voice — where it actually lives

**GitHub comments under the operator account are mostly fleet output** (Cursor, Claude Code, Willow). Do **not** treat `PR_HUMAN_REGISTER` / promise-ledger outbound text as human voice or style training data.

**Human pattern — MCP sources (provenance-gated):**

| Source | Tool | Notes |
|--------|------|-------|
| Indexed sessions | `session_query` | 700+ sessions, 10k+ turns — raw operator text, unsmoothed |
| Corrections | `soil_search` on `corpus/corrections` | Operator→agent fixes (wrong window, rephrase, persona mismatch) |
| Voice mask | `mai_read_file` on vault `sean.md` | **Personal vault** — speak-as-Sean; not in public repo |
| Open flag | `soil_get(willow/flags, flag-operator-record-missing)` | Operator model vs voice mask split |
| JELES / intake | `mem_jeles_search`, `intake_list` | Session JSONL archive when scoped |

Upstream desk registers (`MAINTAINER_HEATMAP`, `PROMISE_LEDGER`) = **ops telemetry** (maintainer warmth, stale PRs). Not voice corpus.

---

## How you boot (pointer)

Full gate: [`boot.md`](boot.md) — persona → Phase 2 MCP → boot-done sentinel.

Cold recovery: [`cold-recovery.md`](cold-recovery.md).

Contract: `mai_read_file("willow.md")`.

---

## Anti-patterns (fleet-wide)

1. **Grep-first** on SOIL paths, handoffs, or "where is sean.md" — use `willow_find` / `soil_search_all`.
2. **GitHub scrape** for operator tone or promises attributed to the account.
3. **Bash** for Postgres, `sqlite3` store, or long GitHub crawls — Kart + `allow_net`.
4. **Load entire** `mcp_registry.json` into context — `fleet_tool_guide(group=…)` instead.
5. **Assume** Grove tools on willow server — check manifest.

---

*ΔΣ=42*
