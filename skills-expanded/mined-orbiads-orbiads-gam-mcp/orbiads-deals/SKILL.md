---
name: orbiads-deals
description: Use for GAM programmatic deals — PMP deals, proposals, private auctions, marketplace buyers, advertiser/agency companies, and ADCP products — through OrbiAds MCP actions or their orbiads CLI equivalents. Examples: "create a programmatic deal", "list marketplace buyers", "set up a proposal". Enforces preview-before-write and billing-guard rules.
version: 1.0.0
author: OrbiAds
license: MIT
metadata:
  group: deals
  tags: [orbiads, gam, adops, deals, programmatic]
  related_skills: [orbiads]
  parent_mcp_tools:
    - companies
    - dai_skill
    - deals
    - prebid_skill
    - products
    - yield_skill
  action_count: 92
  cli_coverage: partial
  read_only: false
user-invocable: false
---

<!--
  ⚠️ GENERATED ARTIFACT — generation source lives in the private OrbiAds monorepo.
  Do not hand-edit; open an issue or PR against documentation/examples instead.
-->

# OrbiAds GAM — Programmatic Deals, Products & Companies

_Configure PMP deals, private auctions, programmatic buyer accounts, advertiser/agency company profiles, and ADCP product catalogs._

**Mode:** mixed (read + write) · **Tools included:** 6 · **Total actions:** 92 · **CLI coverage:** partial (47/92 actions)

Parent MCP tools: `companies`, `dai_skill`, `deals`, `prebid_skill`, `products`, `yield_skill`.

## Surfaces

OrbiAds exposes the same backend through two surfaces; **MCP is the default**. A subset of actions also has a CLI command (`cli_coverage: partial` — 47/92 actions here). Per-action availability (MCP command vs `orbiads <command>` vs `MCP-only`) is listed in [`references/actions.md`](references/actions.md).

**Rule:** if an action is marked `MCP-only` in that table, fall back to the MCP surface (or the web app) for it — never improvise a raw REST call or shell around the CLI.

## CLI usage

```bash
pip install orbiads-cli
orbiads auth status --json     # verify you are authenticated first
orbiads network info --json    # confirm the active tenant / network
```

- Always pass `--json` so the agent parses structured output, never scraped text.
- **CLI gap → fall back to MCP for that action; never shell out around the CLI.**

## Safety Contract

- **Most reads are free; writes and heavy reads cost credits** (e.g. a report run or export costs 0.5 credit). Call free reads liberally for state discovery before any mutation.
- **preview → confirm → execute.** Every write runs once with `dry_run=true` (or no `confirmation_token`) to return a preview + token + cost, then again with the same payload + `confirmation_token`. Get explicit user consent between the two calls.
- **Never bypass `billing_guard`** and never reuse a stale token — payload drift returns `IDEMPOTENCY_KEY_MISMATCH`; refresh the preview.
- **Never invent identifiers.** Do not guess a `tenantId` / `networkCode` / advertiser / order id — resolve them from the session or a read first.
- **At most 2 write retries**, then stop and report.
- **Never leak raw SOAP/REST traces** to the user — surface the structured `error` object instead.
- These rules apply identically on the MCP and CLI surfaces — a CLI write (`orbiads ... create/deploy`) needs the same preview + explicit user confirmation as an MCP write.

## Full action catalogue

Full action catalogue (costs, write flags, confirmation tokens, CLI equivalents): read [`references/actions.md`](references/actions.md).

## Routing back to the orchestrator

This sub-skill is `user-invocable: false`. The `orbiads` orchestrator ([`../orbiads/SKILL.md`](../orbiads/SKILL.md)) routes intents — and the MCP-vs-CLI surface choice — to these tools based on its routing table. If you load this file directly, you bypass the orchestrator's context intake — re-route through the orchestrator unless you already know exactly which action to call.
