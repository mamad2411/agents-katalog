---
name: discover-companies
description: Discover new target companies (or people) via the Exa Agent API, score them against your thesis, and propose them to your inbox for review
argument-hint: "[preset-name | --query \"...\"]"
user-invocable: true
allowed-tools: Bash(*), Read(*), Write(data/inbox.md), Write(data/discover-presets.yaml)
---

# Discover Companies (Exa Agent API)

Discover *new* companies matching Nick's role-shape thesis, score them
deterministically, and write a review-gated proposal to `data/inbox.md`.
Feeds the front of `/scan-companies` (which scores roles after you promote a
company). This skill does NOT modify `data/scan-targets.yaml`.

## Arguments

`$ARGUMENTS`: a preset name (`lane-a`, `lane-b`), or a freeform `--query "..."`
with optional `--criteria "..."` (repeatable). No argument defaults to `lane-a`.

## Steps

### Step 0: Profile guard

Verify `data/profile.md` and `data/goals.md` exist with real content (not TODOs).
If `data/profile.md` is missing/empty: STOP, tell the user to run `/import-cv`.
If `data/goals.md` is missing/all TODOs: STOP, tell the user to fill it from
`framework/templates/goals.md`.

### Step 1: Resolve the preset

If `data/discover-presets.yaml` is missing, tell the user it needs bootstrapping
and offer to draft `lane-a`/`lane-b` from `data/role-shape-engagement-lead.md` +
`data/goals.md`. Otherwise default to `lane-a` unless the user named a preset or
passed `--query`.

### Step 2: Run the discovery tool

```bash
PYTHONIOENCODING=utf-8 python3 tools/agent_discover.py --preset lane-a \
  --exclude-names-from data/scan-targets.yaml data/job-pipeline.md
```

For a freeform run (fold geo/stage constraints into the query itself):

```bash
PYTHONIOENCODING=utf-8 python3 tools/agent_discover.py \
  --query "AI for restaurants, Bay Area HQ, Series A-C" --entity company \
  --exclude-names-from data/scan-targets.yaml data/job-pipeline.md
```

Discovery runs on the **Exa Agent API** (`tools/agent_discover.py`, engine
`agent_core.py`). It prints JSON: `candidate_count`, `cost`, per-field
`grounding` citations, and a score-sorted `candidates` list. Add `--entity person`
for cross-company people discovery (e.g. `--preset deployment-leads`); people are
surfaced with role/company/location, not scored. Agent runs take ~1-10 minutes;
use `--async` to get a `run_id` back immediately and `--collect <run_id>` later.
If the tool returns a JSON `error` (e.g. EXA_API_KEY unset, run failed), relay it
and stop. (The old Websets path `webset_discover.py` is retired — Websets 401s for
this account and is deprecating in favor of Agent.)

### Step 3: Annotate (judgment layer)

**FIRST, reconcile against the pipeline (MANDATORY, before any annotation).** The discovery
tool reasons from the public web and cannot see `data/job-pipeline.md`, so a company already
closed arrives looking exactly like a fresh lead:

```bash
PYTHONIOENCODING=utf-8 python3 tools/pipeline_reconcile.py --repo-root . --format markdown \
  "Candidate One" "Candidate Two"
```

Pass every candidate. Exit 1 means at least one is already tracked; **exit 2 means the pipeline
could not be read and the result is not an all-clear.** Carry the verdict into the inbox block so
the reviewer sees it:

- **`Previously closed`** — annotate with the stage and date. **Never silently drop it.** A closed
  loop is information the reviewer may still want, and a company that simply vanishes from the
  proposal leaves nothing for anyone to notice.
- **`Mixed history`** — has both closed and live rows. **Never exclude.**
- **`Similar names`** — resolved by nobody. Check by hand before writing anything about it.

Origin: `feedback_diff_agent_recommendations_against_closed_rows`.

Then, for each candidate, add a one-line fit read the deterministic score cannot capture:
- Which lane it fits (A enterprise / B SMB-trades) and why.
- Mission/energy alignment against `data/goals.md` and `data/professional-identity.md`.
- The SF-the-city nuance: a `geo_flag: true` means the HQ is Bay-Area-but-not-SF
  or unknown - call that out (the hard filter is SF in-person/hybrid).
- **Founding-team read (added 2026-08-26) — a RANKING signal, never a rejection.** From public
  data only (LinkedIn, the company site, an Exa `category:people` lookup), answer one question:
  **is there anyone on this team who has done the commercial or delivery craft before?** Report
  what you actually found in one line — approximate headcount, roughly how many non-engineers,
  and the founders' prior roles — then tag the candidate:
  - `bench: yes` — someone has held the seat or an adjacent one (an ex-consultant founder, a
    commercial lead with delivery history, a second-time operator).
  - `bench: thin` — engineer-heavy with one recent commercial hire.
  - `bench: unknown` — public data too sparse to say. **This is a real and common answer. Say it.**

  **Sort `thin` and `unknown` down; do NOT drop them.** Two reasons this is not a filter: public
  data is stale often enough to matter (2026-08-26: Exa reported a target's commercial lead at
  7 months tenure, he said two on the call), and the part that actually decides it — whether the
  guidance is real, whether there is any structure — is not visible from outside and needs the
  conversation. Per the `goals.md` non-negotiable added 2026-08-26. Worked example (2026-08-26): a target
  company would have tagged `bench: thin` and sorted down; it still would have been worth the cold
  email, and the call is what settled it.
- Recommend or hold.

Do NOT re-score; the number is deterministic. You are adding judgment on top — the founding-team
read is a sort key and an annotation, not an input to the score.

### Step 4: Write the proposal (atomic, review-gated)

Prepend a block to `data/inbox.md` **via the locked writer, never a raw Write**:

```bash
PYTHONIOENCODING=utf-8 python3 tools/inbox_lock.py prepend \
  --inbox data/inbox.md --stdin <<'BLOCK'
<the block below>
BLOCK
```

A re-read-then-Write cannot hold the file lock across its read-think-write cycle, so
it can silently revert a concurrent write from the launchd collectors (which fire
every 3 hours and each morning). Hand the CLI just the new block; it does the
read-splice-write inside the lock.

The block to pass:

```markdown
## Discovered Companies - YYYY-MM-DD (preset: lane-a)

Discovered via /discover-companies. Promote winners into data/scan-targets.yaml
(confirm `ats` + `slug`), then /scan-companies scores their roles.

| Score | Company | Lane | SF? | Stage | Fit read | Careers | Slug guess | Rec |
|-------|---------|------|-----|-------|----------|---------|------------|-----|
| 9 | Acme AI | A | SF | Series C | <one-line> | [link](url) | acme-ai | promote |
```

Never write to `data/scan-targets.yaml` from this skill - promotion is the user's
explicit, gated action.

### Step 5: Present

Show the sorted table in chat and report `candidate_count` / `excluded_count`.
If the JSON has `partial: true`, the Webset hit the timeout - say so and note the
results are incomplete (re-run or raise `--timeout`). Free tier caps a run at 25
results; mention that if the count is at the cap. Then suggest: "Promote the ones
you like into scan-targets.yaml, then run `/scan-companies`."

## Hard rules

- No em dashes in any drafted output.
- Review-gated: nothing auto-enters `scan-targets.yaml`.
- If `EXA_API_KEY` is unset, the tool returns a JSON error - relay it and stop.
