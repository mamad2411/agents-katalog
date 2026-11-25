---
name: orbiads-audit
description: Use for GAM account audits — delivery, inventory, security-baseline, and billing checks plus credit-transaction history, OrbiAds log history and GAM change history (`list_change_events` / `get_change_event`, read-only, active network) — through OrbiAds MCP actions or their orbiads CLI equivalents. Examples: "audit my account security", "check my credit balance", "run an inventory audit". Log and history reads are free; audit scans cost credits (0.5 to 5).
version: 1.0.0
author: OrbiAds
license: MIT
metadata:
  group: audit
  tags: [orbiads, gam, adops, audit, billing]
  related_skills: [orbiads]
  parent_mcp_tools:
    - audit
    - audit_skill
    - billing
  action_count: 13
  cli_coverage: partial
  read_only: true
user-invocable: false
---

<!--
  ⚠️ GENERATED ARTIFACT — generation source lives in the private OrbiAds monorepo.
  Do not hand-edit; open an issue or PR against documentation/examples instead.
-->

# OrbiAds GAM — Account Audits & Billing

_Perform delivery, inventory, security, and billing audits. Track credit transactions and system log histories._

**Mode:** read-only · **Tools included:** 3 · **Total actions:** 13 · **CLI coverage:** partial (5/13 actions)

Parent MCP tools: `audit`, `audit_skill`, `billing`.

## Surfaces

OrbiAds exposes the same backend through two surfaces; **MCP is the default**. A subset of actions also has a CLI command (`cli_coverage: partial` — 5/13 actions here). Per-action availability (MCP command vs `orbiads <command>` vs `MCP-only`) is listed in [`references/actions.md`](references/actions.md).

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

- **No GAM mutation, but not always free.** Every action in this skill is read-only. Log, history and billing reads cost 0 credits; audit scans are billed (e.g. `hygiene_check` 0.5, `standards_baseline` 4 to 5). Check the cost before running a scan.
- **Never invent identifiers.** Do not guess a `tenantId` or `networkCode` — resolve them from the authenticated session first.
- **Never leak raw SOAP/REST traces** to the user — surface the structured `error` object instead.
- These rules apply identically on the MCP and CLI surfaces — a CLI write (`orbiads ... create/deploy`) needs the same preview + explicit user confirmation as an MCP write.

## Full action catalogue

Full action catalogue (costs, write flags, confirmation tokens, CLI equivalents): read [`references/actions.md`](references/actions.md).

## Routing back to the orchestrator

This sub-skill is `user-invocable: false`. The `orbiads` orchestrator ([`../orbiads/SKILL.md`](../orbiads/SKILL.md)) routes intents — and the MCP-vs-CLI surface choice — to these tools based on its routing table. If you load this file directly, you bypass the orchestrator's context intake — re-route through the orchestrator unless you already know exactly which action to call.
