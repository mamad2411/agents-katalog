---
name: aioproductos-triage
description: >-
  Run Monday-morning product triage on AIOProductOS. Grounds in the product
  spine, surfaces the top 3 customer-evidenced insights, drafts RICE-scored
  tasks (every input traced to real revenue and usage), assigns a named AI
  teammate, and schedules them into the next sprint. Use at the start of a
  planning week, or whenever someone asks "what should we work on next?" on a
  connected AIOProductOS workspace.
---

# AIOProductOS · Weekly Triage

Turn a week's customer signal into 3 scheduled, owned, evidence-backed tasks —
in one pass over the AIOProductOS spine. Insight → feature → task → sprint, with
the revenue and usage that justify each call carried on the same record.

## Before you start

This skill drives the **AIOProductOS MCP connector**. It needs these tools to be
available in the session: `get_pm_playbook`, `get_product_brain`, `list_insights`,
`get_customer_360`, `list_objectives`, `pm_meta`, `create_task`, `update_task`,
`list_sprints` (plus the analytics reads `analyze_nrr`, `analyze_funnel`,
`get_retention`, `analyze_paths`).

If those tools are not present, stop and tell the user to connect the workspace:
**Settings → Connect & Tokens → "Connect to Claude"**, custom connector URL
`https://platform.aioproductos.com/api/mcp`. Don't fabricate the triage — without
the connector there is no spine to ground in.

## The doctrine (load it, don't guess it)

Call `get_pm_playbook` once and follow it. The non-negotiables it encodes:

- **Ground in the brain, then decide.** Never reason about priorities from memory.
- **Keep work on the spine.** Every task links its `insight_id` (the why) and its
  `feature_id` (the bet). No orphans.
- **Resolve names → ids with `pm_meta` before any write. Never guess an id.**
- **Claim only the writes you actually made**, in plain language.

## The flow

### 1 · Ground
Call `get_product_brain` — revenue + top accounts, web + product analytics,
features, recent verbatim signals, open work. This is your whole evidence base for
the session. Pull `list_objectives` too, so every bet you propose ties to a goal
the team is actually trying to move.

### 2 · Surface candidates
Call `list_insights` (open, newest first) — the voice-of-customer backlog. Combine
with the recent signals from the brain. Cluster duplicates: three accounts asking
for SSO is one opportunity with reach 3, not three items.

### 3 · Weigh on real evidence → pick the top 3
For the strongest candidates, quantify the case from the spine, never from a hunch:
- **Revenue at stake** — `get_customer_360` on the accounts each item touches
  (MRR behind them); `analyze_nrr` for what's churning or contracting.
- **Reach / usage** — `analyze_funnel`, `get_retention`, `analyze_paths`, or the
  brain's analytics: how many users actually hit this.
- **Signal strength** — how many distinct accounts, how recent, quantitative vs.
  anecdotal.

Rank by that evidence and take the top 3. Quote the numbers ("$4.2k MRR across 3
accounts; 38% drop on this step"), not adjectives.

### 4 · RICE each (transparently)
Score each of the 3 with **RICE = (Reach × Impact × Confidence) / Effort**, showing
your work — see `rice-method.md` for how each factor maps to a spine
number. Two honesty rules:
- **Effort is an estimate the spine cannot know.** Ask the user for it, or use a
  labeled t-shirt→months guess and mark it `(assumed)`.
- **RICE is the default, not the law.** If the org uses ICE / WSJF / value-effort,
  adapt — and either way, present the evidence so a human can re-rank. You ground
  the call; you don't get the last word on the number.

### 5 · Confirm before writing (HITL)
Present the 3 as a table — *insight → proposed task → R / I / C / E → score → source
links* — and ask the user to confirm or adjust. Do **not** create anything until
they say go. (See the output shape below.)

### 6 · Draft the tasks
For each confirmed item: `pm_meta` to resolve ids, then `create_task` with
- a concrete, pick-up-cold title,
- a description that embeds the RICE breakdown + the evidence + a one-line "because",
- `insight_id` (the why) and `feature_id` (the bet) — link the spine.

### 7 · Assign a named AI teammate
From `pm_meta` members, pick an **AI teammate** (a member that is an agent — e.g.
"Ada · Backend AI"); `update_task` with its id in `assignee_member_ids`. If the org
has no AI teammate configured, say so plainly and leave the assignment to the user —
don't invent a member.

### 8 · Schedule into the next sprint
`list_sprints` → identify the next/active sprint by window and state. For each task,
`update_task` with that `sprint_id`. Confirm the placement.

### 9 · Report
A tight summary: the 3 tasks created (with ids), their RICE scores, the assignee, the
sprint, and the spine links. Claim only what you actually wrote.

## Output shape for step 5

```
This week's triage — top 3 (RICE, evidence-backed). Confirm before I create them.

# | Insight (source)              | Proposed task            |  R |  I |  C  | Effort     | RICE
--+-------------------------------+--------------------------+----+----+-----+------------+------
1 | "Need SAML" — 3 accts, $4.2k  | SSO/SAML for enterprise  | 3  | 2  | 80% | 2mo (assumed)| 2.4
2 | Onboarding drop 38% (funnel)  | Shorten signup form      | 120| 1  | 100%| 0.5mo      | 240
3 | Churned acct cited exports    | CSV export on reports    | 8  | 1  | 50% | 1mo        | 4.0

Want me to create, assign (Ada · Backend AI), and schedule all 3 into Sprint W27?
```

(Reach is "accounts/users affected this period" — keep the unit consistent across
rows or the scores aren't comparable. See `rice-method.md`.)
