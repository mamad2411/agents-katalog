---
name: morning-sync
description: Daily sync — pull Slack, meetings, DMs from the lookback window; classify; synthesize into ≤1-page report with Hygiene Scorecard + Proposed Updates + Deliverables + categorized Needs Your Input. Triggered by /morning-sync or "let's sync".
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Task
---

Daily sync that scans Slack, meetings, and DMs, then proposes targeted repo updates.

## Configuration

Channel registry, meeting patterns, and DM settings live in `config/morning-sync.md`. Hygiene rules and classifiers live in `config/repo-hygiene.json`. Read both.

---

## PHASE 0 — Pre-run checklist (mandatory; do not skip)

**These steps are non-negotiable. Skipping any of them has caused past critical failures.**

1. **Compute Unix timestamps via `python3` — never by hand.**
   Rationale: hand-calculated Unix timestamps have been off by exactly 1 year in past runs. The DM scan then returned prior-year data, contaminating the whole sync.
   ```bash
   python3 -c "
   from datetime import datetime, timezone
   start = datetime(YYYY, MM, DD, 0, 0, tzinfo=timezone.utc)
   end   = datetime(YYYY, MM, DD, 23, 59, tzinfo=timezone.utc)
   print(f'start: {int(start.timestamp())}  ({start})')
   print(f'end:   {int(end.timestamp())}  ({end})')
   "
   ```
   **Mandatory verification:** run the inverse (`datetime.utcfromtimestamp(...)`) and confirm both lines show the correct year. If either shows YYYY ≠ current year, fix before any Slack API call.

2. **Read `runs.log` — check for overlap.**
   Parse the last few rows. Extract each: date range scanned, channels covered, DMs processed.
   If the user's requested window overlaps a prior completed scan, tell them: "[date] was already scanned on [prior run]. Re-scan, or skip?" Wait for answer.

3. **Read `gotchas.md` — scan every rule before drafting.**
   Every gotcha is a rule you MUST apply this run. When you classify each item later (Phase 2), re-check against gotchas before placing it.

4. **Date validation — if the user gave a day name + date, verify they match.**
   E.g., "Thursday, March 20" — check what day-of-week March 20 is. If mismatch, ask before proceeding.

---

## Phase 1: Gather

### Lookback Window
- **Default:** Previous business day (Monday = Friday, otherwise = yesterday)
- **Custom:** PM can specify: "past 2 days", "Wednesday", "Mar 10-12"

### Parallel Agent Pattern
Launch these concurrently in a single message:
1. **Meeting agent** — list meetings, user triage, pull transcripts + notes
2. **Core channels agent** — scan all core channels + thread replies
3. **Project channels agent** — scan all project + monitor channels + thread replies
4. **DM agent** — scan DMs, apply DM Heuristic Classifier (below)
5. **Auto-discovery agent** — search for new channels not in config

Do NOT scan sequentially. If a scan takes more than 5 minutes, something is wrong.

### Thread Scanning
Default channel reads miss thread replies to older messages. After reading channels, also search for thread replies posted in the lookback window and read full threads for any hits.

### Shared meetings fallback
Some meeting tools' `list_meetings` APIs only return meetings the user created/attended. Meetings shared from others may not appear. **Always ask after listing:** "Any meetings shared with you that aren't in the list above?" If yes, extract the meeting ID from the URL and fetch directly.

---

## Phase 2: Classify & Synthesize

### Pre-Synthesis (MANDATORY)
1. Re-read `gotchas.md` — cross-check proposed updates against known failure patterns.
2. Read `runs.log` — check what the last run covered (already done in Phase 0; verify).

### Channel Role Filtering
Each channel in `config/morning-sync.md` has a **role** tag (pm/eng/ds/monitor). Apply this filter first:

- **pm** — always surface relevant content
- **eng** — scan, but only surface items matching product keywords (see `config/repo-hygiene.json` → `product_keywords_for_eng_ds_filter`). Skip pure implementation, refactors, internal sizing.
- **ds** — scan, but only surface items with product/timeline/customer implications. DS backlog items stay with DS.
- **monitor** — include but flag as context-only (not our primary project)

Engineers and data scientists are expected to update the repo themselves for their own work.

### Chronological Synthesis
Merge ALL inputs (meetings, Slack, DMs) into a single chronological timeline per project. A meeting at T0 and its Slack follow-up at T1 are one narrative. The timeline is internal working material — NOT shown to the PM.

### Deduplication
Before proposing any update, **search the full repo** (`grep -r`) for existing files on the topic. Use key terms — existing coverage may live in `data-science/`, a different project folder, or `reference-docs/`. Propose appending to existing files, not creating new ones.

### DM Heuristic Classifier
For each DM thread, classify as one of four buckets. Only extract bucket C:

| Bucket | Pattern | Action |
|---|---|---|
| A. Logistical/social | "lunch?", "heading to X", "see you at", "ty!" | Skip silently |
| B. Casual idea mention | "maybe we could", "btw", "just curious", "wonder if" | Skip unless repeated ≥2x |
| C. **Concrete decision / timeline / staffing** | "decided", "confirmed", "last day", "joining", "approved", "timeline shift" | **Extract** |
| D. Approval/ack | "sounds good", "lgtm", "+1" | Skip |

Rationale: unfiltered DMs produce 8+ dismissable items per run that the PM has to triage.

### Experiment-Decision Confidence Classifier
When a meeting transcript mentions an experiment's results, classify the source language before writing anything:

- **`confirmed`** — explicit keywords only (from `config/repo-hygiene.json` → `experiment_decision_keywords.confirmed`): "promoting to winner", "confirmed winner", "GTM'd", "approved", "decided to ship", "finalized". Write as **"Decided: X"**.
- **`trending`** — "strong early signal", "looking promising", "preliminary". Write as **"Trending: X (early signal, not decided)"**.
- **`running`** — "still running", "no new data". Write as **"Running: X (no new decision)"**.

Never write "decided" or "winner" without a `confirmed`-tier keyword in the source.

### File Routing
Follow `.claude/rules/document-conventions.md` file boundary rules:
- Decisions → `decisions.md` (NOT inline in CONTEXT.md)
- Design flows/copy → `designs.md` (NOT in CONTEXT.md)
- System/data findings → `truths.md` (NOT in CONTEXT.md)
- Design WIP that will come via Figma → skip
- Chronological meeting content → `updates.md` (NOT as dated sections in CONTEXT.md)
- CONTEXT.md is narrative-only. Update its narrative inline when state changes; never append a dated section.

### Action Item Extraction (PM)
Separately, scan all sources for things the **PM personally needs to do**:
- "I'll [do X]" or "[PM name] to [do X]" from meeting transcripts
- Follow-ups the PM committed to in Slack/DMs
- Questions directed at the PM that need a response
- Meetings to schedule, messages to send, DMs to reply to

NOT action items: tasks assigned to others (those are repo updates), things already done, vague intentions.

Classify execution mode for each: Slack msg / Cal event / Google Doc / DM reply / Manual.

### Status Freshness Check
For every project mentioned today:
1. Read the project's `README.md` header (status, phase, last updated).
2. Compare against what was discussed. Does status match reality?
3. If stale, add a Status update item.
4. If `Last updated` exceeds the phase's SLA (from `config/repo-hygiene.json` → `freshness_sla_days`), flag in the Hygiene Scorecard.

### INDEX.md Drift Check
Cross-check `projects/INDEX.md` against actual README Phase for every project mentioned today. If INDEX shows a different phase, flag in the Hygiene Scorecard.

---

## Phase 2b — Auto-Actions Layer (before Phase 3 report)

Scan the synthesized timeline for these automatable actions. Each becomes a proposal in Section 2 (Deliverables & New Work) — never write without approval, but pre-fill the exact change.

### A. Auto-update `team/people.md` on staffing signals
Keywords: `(depart|departing|last day|leaving)` + name + date, or `(joining|starting|joined|new \w+)` + name + date.

Propose:
```
[path] team/people.md
[change] Mark [Name] as [departing|joining] [date]. Source: [meeting/Slack link].
```

### B. Auto-propose project README Phase change
Scan each project for phase-transition keywords:

| Trigger language | Phase change |
|---|---|
| "brief approved", "brief shipped" | → Designs |
| "design review complete", "design approved" | → Feasibility or RFCs |
| "RFC approved", "implementation starting" | → Coding |
| "ship review passed", "launching" | → Live (pending) |
| "launched", "100% rollout", "GTM'd" | → Live |
| "sunset", "deprecated", "complete" | → Complete |

Propose, don't write:
```
[path] projects/[cat]/[project]/README.md
[change] Phase: [old] → [new]. Source: [link]
```

### C. Auto-append to `projects/INDEX.md` for new projects
If a new project is detected without existing coverage, also propose an INDEX row with the expected columns.

### D. Draft Slack summary (do NOT send automatically)
Draft a ≤150-char summary for posting to a coordination channel:
```
Morning sync [date]: [N] project updates, [M] deliverables proposed, [K] action items. Details: [repo link]
```
Include under "Slack Summary Draft (review before posting)." **Never post without explicit user approval.**

---

## Phase 3: Report

The report has **four sections**. Use this exact structure — do not improvise.

```
## Hygiene Scorecard

[Zero tax if nothing's off. Otherwise, each item is a one-liner with the proposed fix.]

- [ ] [N] projects with Last updated beyond phase SLA: [list with project + days stale]
- [ ] [N] projects/INDEX.md rows don't match project README Phase: [list]
- [ ] [N] open strategic questions that a recent DS analysis may resolve: [list]
- [ ] [N] beliefs with Last challenged older than 60 days: [list]
- [ ] [N] orphaned files not referenced by any INDEX / README / CLAUDE.md: [list]
- [ ] [N] strategic-initiatives.md items with last_meaningful_update older than 2× cadence: [list]

If everything is current: "✓ All hygiene checks pass."

---

## Proposed Updates

### [#]. [Project Name] — `[target file path]` ([create/append/update])
[1-3 sentence synthesized description, written as the actual content to insert.]

---

## Deliverables & New Work

### New Deliverables Detected
- **[Source meeting/DM]** → [What was created / needs creation]. [Link if available.]

### Auto-Actions (from Phase 2b)
- **A (people.md):** [proposed change] — approve?
- **B (Phase change):** [project] Phase: [old] → [new] — approve?
- **C (INDEX append):** [row] — approve?
- **D (Slack summary draft):** "[draft]" — post to #channel?

### Your Action Items

| # | Action | People | Source | How to execute |
|---|--------|--------|--------|---------------|
| A1 | [What to do] | [Who] | [meeting/channel/DM] | [Slack msg / Cal event / Google Doc / DM reply / Manual] |

---

## Needs Your Input (categorized)

### Routing ambiguous (where should this go?)
- [Item + options]

### Decision vs discussion (was this finalized?)
- [Item + transcript language quoted]

### New project or phase change?
- [Item + evidence]

### Design WIP or finalized?
- [Item + Figma status if known]

### Eng-internal but possibly product-relevant?
- [Item + product keyword check]
```

### Report rules

- **Section 0 (Hygiene Scorecard):** checklist-only. Zero items → one line. Do NOT pad.
- **Section 1 (Proposed Updates):** user approves/rejects in seconds. No timelines, no source tables. Group related updates under one project heading.
- **Section 2 (Deliverables & New Work):** only net-new work (not file updates). Auto-Actions subsection shows each pure-add proposal with APPROVE? prompt. Include links.
- **Section 3 (Needs Your Input — categorized):** 5 buckets. Triage by category, not by item. Each item: one line. Empty bucket → omit the header entirely.
- Full report under 1 page.

---

## Pre-Output Linter (run before presenting to user)

Before Phase 4, check the draft against these rules. Fix in place. Do not present a draft that fails any:

1. Every "decided"/"winner" claim has a `confirmed`-tier keyword from source transcript.
2. No items from eng/ds-role channels without a product keyword match.
3. No DMs from bucket A/B/D in any section.
4. No Section 2 items that are actually file updates (belong in Section 1).
5. No Section 3 items with a known home (belong in Section 1 with routing).
6. Section 3: no bucket > 5 items. If one does, you're over-extracting — reapply filters.
7. Report total length ≤ 1 page (~80 lines markdown).
8. Timestamps verified via inverse printing the correct year.

---

## Phase 4: Execute Repo Updates

After PM approves repo updates:
1. `git pull` to ensure latest state.
2. Apply approved updates. Append/merge — never overwrite teammates' content.
3. Cross-check for stale or contradictory info in updated files.
   - If you touched a DS analysis, check `data-science/INDEX.md` — add if missing.
   - If you touched a project file, check `projects/INDEX.md` — update the phase if it changed.
4. Commit with descriptive message. Ask before pushing.

## Phase 5: Execute Action Items

For each approved action item:
1. **Slack message:** Read repo context to draft an informed message. Find the right channel/person. Draft, show to user, send only on approval.
2. **Calendar event:** Create via Calendar MCP with appropriate attendees.
3. **Google Doc update:** Read, propose edit, apply on approval.
4. **DM reply:** Draft and show before sending.
5. **Manual item:** Note it clearly — "This one's on you: [description]."

**Key rules:**
- Always draft before sending — never send without showing first.
- Use repo context to make messages substantive.
- If an action was already done, skip and note "already addressed."

---

## Post-Run

Append to `runs.log`. Include:
- Date range / channels / meetings / DMs / approved count / **rejected count** / status / notes.
- **user_rejection_rate** — approved / proposed. If > 30% for two consecutive runs, stop and analyze — don't keep shipping a broken classifier.

If a new failure pattern surfaced, add to `gotchas.md` **immediately** — don't wait for next run.

**Self-improvement discipline:** Every gotcha is a lint rule. When a new gotcha is added:
1. If codeable, add a check to the Pre-Output Linter above.
2. Every 10 runs, review `gotchas.md` — retire any gotcha whose rule is now encoded (move to a "Retired (codified)" section).
