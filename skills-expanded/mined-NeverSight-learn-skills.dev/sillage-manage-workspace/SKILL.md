---
name: sillage-manage-workspace
description: >
  Stands up a new Sillage workspace and safely edits an existing one through the MCP — the write and
  edit engine behind targeting. Runs the setup loop (persona → target accounts → coverage →
  watchlists → agents → signal runs) and the edit loop (read current state → diff → patch), respecting
  the write rules that make each change safe. Use when applying confirmed targeting, changing a live
  workspace, or fixing a half-configured one. Use when you hear: "set up my workspace", "onboard this
  account", "edit my persona", "update my targeting", "add a competitor", "add target accounts",
  "change my keywords", "pause this agent", "re-run the agents", "fix my workspace", "reconcile my setup".
metadata:
  owner: pf@getsillage.com
  version: 1.2.0
  model-tier: sonnet
  provider: Sillage MCP v2 (https://api.getsillage.com/api/mcp/v2)
  pairs-with: [sillage-onboarding, sillage-help]
---

# Manage Workspace — set up and edit a Sillage workspace through the MCP

This is the **hands that write**. `sillage-onboarding` decides _what_ the targeting should be (interview +
expansion); this skill puts it into the workspace and changes it later without breaking it. If the
model of the product is unclear, read `sillage-help` first — this skill assumes you know what a
persona, a target account, coverage, a watchlist, and a signal run are.

There are two jobs, one skill: **set up** a fresh workspace, and **edit** a live one. Editing is the
harder half, because most writes replace rather than patch — get that wrong and you wipe good config.

## Why this skill exists (and is not the MCP server prompt)

The MCP already has the tools and its server instructions script a happy-path onboarding sequence. What
it does **not** carry is the **edit/reconcile loop** and the **write-safety rules**: that the persona
is replaced whole, that the target list only appends, that coverage doesn't refresh itself, that some
writes are destructive. Those are this skill's job. Everything here operates on **one already-connected
workspace** (via `sk_live_` or OAuth) — the MCP can't create a workspace, only run and edit one.

## When NOT to use

- You haven't decided the targeting yet → run `sillage-onboarding` first to shape a sharp persona and agents,
  then come here to write them.
- You just want to read results ("show me this week's content", "list my signals") → call the read
  tool directly; don't run a setup loop.
- You want to understand the product, not change it → `sillage-help`.

## Non-negotiables (read before any write)

These four rules prevent every common way an edit goes wrong. Full detail in
`reference/write-semantics.md`.

1. **Persona is replace-whole (PUT), never patch.** Always `get_persona` → merge your change into the
   full object → `upsert_persona` with the complete object. Send only documented persona fields.
2. **The target account list only appends** (`add_top_accounts`) or **removes by id or identifier**
   (`remove_top_accounts`, destructive). There is no full-replace. Read it with
   `read_top_account_list`.
3. **Coverage doesn't refresh itself.** Changing the persona does not re-map existing companies —
   re-trigger `enrich_company` (by **domain**) for the accounts you want re-covered.
4. **Confirm before writing, poll before reading.** Read back what you're about to change and get a
   yes. After a write that enqueues work (accounts, mappings, runs), poll the matching status tool to
   a terminal state before you read results. `403` from a tool means the feature isn't enabled for the
   workspace — surface it, don't retry.

## Setup — standing up a workspace

Drive it off `get_setup_state`; its four flags tell you the next missing piece. Order matters —
persona defines targeting before lists ingest.

1. `get_setup_state` — see what's missing (`persona_set`, `list_uploaded`, `ingestion_complete`,
   `has_contents`).
2. **Persona** → `upsert_persona` with the confirmed, expanded ICP.
3. **Target accounts** → `add_top_accounts` (by `domain`), then poll
   `get_top_account_list_status` to `completed`.
4. **Coverage** → `enrich_company` per account you want mapped to its people (by domain). Poll via
   `list_company_mappings` / `get_account_mapping_stage`.
5. **Watchlists** → `create_watchlist` per type, `add_watchlist_entities` (LinkedIn URL/handle
   preferred, domain as fallback on company lists, ≤100 per call). Or let a watchlist agent create
   its list for you.
6. **Agents** → `create_agent` per confirmed signal; pass an existing `watchlist_id` to bind a list
   you already populated.
7. **Run** → `launch_signal_run` per agent, poll `get_signal_run` to a terminal stage, then read
   `list_signals` / `get_contents`.

Confirm all four setup flags true at the end. The full tool list with params is in
`reference/tool-map.md`.

## Edit — changing a live workspace

Never write blind into a live workspace. Snapshot, diff, then patch the one axis that's off.

1. **Snapshot the current state:**
   ```
   get_persona()            # the current ICP
   get_agents()             # which agents exist, types, enabled, keywords
   list_watchlists()        # which lists exist and how populated
   read_top_account_list()  # the real target accounts
   ```
2. **Diff each axis** against what it should be — persona, target accounts, watchlists, agents — and
   name each as **match / mismatch / missing**.
3. **Patch only what's off**, using the right write for that axis (merge-then-PUT for persona, append
   for accounts, `configure_agent` for keywords/enabled, `bind_agent_watchlist` for scope). Then
   re-trigger coverage or a signal run if the change should surface new results.

The per-axis reconciliation table and the recipes for the common edits (widen the persona, add a
competitor, tune keywords, pause an agent, add/remove target accounts) are in
`reference/editing-playbook.md`.

## Troubleshoot — few or zero signals

A run that completes with nothing (or almost nothing) is usually **not** a lookback problem. Diagnose
in this order and stop at the first hit:

1. **Coverage.** Are the target account's people actually mapped? `list_company_mappings` /
   `get_account_mapping_stage`. No mapped people → any people-dependent agent finds nobody. This is
   the most common cause — fix it with `enrich_company` (by domain), not with more keywords.
2. **Agent scope.** Keywords too narrow or over-quoted, watchlist empty, or the wrong agent type for
   the signal. Widen or re-mix the keywords; confirm the watchlist actually has entities.
3. **Did the run finish?** `get_signal_run` must be at a terminal stage (`completed` /
   `completed_partial`), and results come from `list_signals`, not the run counters.
4. **Account is simply quiet.** Some accounts barely post — check with `get_contents` filtered to the
   company. A genuinely inactive account won't produce signals; that's the account, not the setup.
5. **Only then, lookback.** A longer `lookback_days` is rarely the real fix — reach for it last.

**`ingestion_complete: true` is workspace-level, not a per-account "all scraped" green light.** The
flag says the list finished processing; a given account can still have zero content and zero mapped
people. Don't read one boolean as "everything's ready for every account" — check coverage per account
(step 1).

## Close with a summary

After a setup or an edit, report plainly what changed and what's now running:

```
## What I changed
<persona / accounts / watchlists / agents — before → after, in plain language>

## What's running now
<agents enabled · runs launched · ingestion/coverage status>

## Waiting on
<anything still ingesting or mapping, and when to re-check>
```
