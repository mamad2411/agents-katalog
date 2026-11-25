---
name: abf-report-runner
description: >
  Use when running a comprehensive (broad-scope, multi-block) ABF transaction report.
  Triggered by abf-gateway ONLY when broad analytical intent is classified. Single-metric /
  narrow reads are answered inline by abf-gateway and do NOT enter this runner.
  Reads asset-class methodology sections from the ABF MCP server (via the `on_demand` keys
  carried in the asset-class catalog) per catalog applicability gates.
  Block 1–2 specs and synthesis guidelines are inlined in phases/.
---

# ABF Report Runner

Client-side phase guide for **broad, multi-block** ABF analytical reports (narrow single-metric reads are answered inline by `abf-gateway` and never reach this runner). The `{asset_class_catalog}` drives domain grouping and determines which methodologies are applicable (the Discover phase). Block 1–2 specs are inlined in `phases/4-8-block-delivery.md`; Blocks 3–5 read methodology sections from the ABF MCP server via the catalog's `on_demand` keys. This runner is **read-only**: it reads, queries, and explains analytics data within the conversation — it holds no on-disk state.

Each phase is documented in its own file under `phases/`. The runner is the dispatcher. Per-block methodology is served by the ABF MCP server; the `{asset_class_catalog}`'s `on_demand` map names each block's section.

## Phase index

| Phase | File | Speaker | Purpose |
|---|---|---|---|
| Discover | `phases/2-discover.md` | silent | Page through `list_transaction_analytics`; group by domain |
| Confirm scope | `phases/3-confirm-scope.md` | analyst | Present domains; record confirmed scope |
| Block delivery | `phases/4-8-block-delivery.md` | analyst | Deliver one block per iteration (parameterized template) |
| Synthesize | `phases/9-synthesize.md` | analyst | Synthesize delivered blocks into key takeaways (guidelines inlined) |
| Handoff | `phases/10-handoff.md` | analyst | Terminal acknowledgement |

The runner has no resume or initialization phase — it holds nothing on disk, so every run starts fresh at Discover and lives only for the current conversation.

## Response discipline

Follow `../abf-gateway/knowledge/contracts/response-discipline.md`. Phases marked silent must not produce user-facing narration when they succeed.

## Entry conditions

This runner is invoked by `abf-gateway` when broad analytical intent is classified. The gateway has resolved the active environment (Step 1), `{transaction_id}`, and `{asset_class_catalog}` before handing off. The runner keeps its working state (discovered domains, confirmed scope, delivered block content) in the conversation and enters at Discover.

## What the runner must NOT do (global)

- **No analyst-facing work outside the documented phases.** Focused single-KPI follow-ups are answered inline within Block delivery before the checkpoint prompt.
- **No silent block skips.** Every skipped block is called out to the analyst.
- **No `create_*_from_preview`, `update_*_from_preview`, or any other write tool.** Read-only runner.
- **No harness narration.**

Phase-specific constraints live in each `phases/*.md`.
