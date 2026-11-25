---
name: data-qa
description: Interactive QA session where user reports data problems conversationally, and the agent verifies each claim with a pinned query and files GitHub issues. Use when the user says numbers look wrong, rows are missing or duplicated, a dashboard is stale, a pipeline output changed unexpectedly, or mentions "data QA". For a behavior bug with no wrong number, such as a job that crashes or a UI that misbehaves, this is the wrong skill.
---

<!-- Forked from Pocock suite qa v1.1, 2026-07-13. Upstream deleted `qa` in v1.2.0 (successor: `triage` + tracker config); this fork owns the loop outright and has no upstream to sync against. Suite upgrades must not overwrite this folder. -->

# QA Session

Run an interactive QA session. The user describes data problems they're seeing. You clarify, reproduce each claim against the warehouse, pin the evidence before it rots, and file GitHub issues that are durable, consumer-focused, and use the project's domain language.

## For each issue the user raises

### 1. Listen and lightly clarify

Let the user describe the problem in their own words. Ask **at most 2-3 short clarifying questions** focused on:

- What they expected vs what they actually saw, and the axis of the mismatch: which measure, at which grain, under which filter
- Where they saw it (which dashboard, report, or table) and as of when
- Whether it's scoped or everywhere (one partition, one source, one segment, or all history), and whether it was wrong once or is wrong again after each rebuild

Do NOT over-interview. If the description is clear enough to reproduce, move on.

### 2. Reproduce the claim and pin the evidence

Production tables mutate while you talk. An unpinned wrong number is a wrong number you can't file. Before filing:

- **Run the claim as a query.** Query the surface the user named and confirm the number they saw. If you can't confirm it, say so, because that is itself a finding (stale cache, wrong filter, permissions).
- **Pin it.** Re-run with the warehouse's time-travel clause at a fixed timestamp so the evidence is replayable; materialize a scratch snapshot if the issue may outlive the time-travel window. See [pinning-evidence.md](pinning-evidence.md) for syntax and the snapshot rule.
- **Record both versions.** The data version (the as-of timestamp) and the code version (whatever last built the table, which is not necessarily HEAD).

Run these in the background (background Bash or a subagent) and keep talking, clarifying the next report while the queries round-trip. Scope assessment (step 3) can start from the user's description; the completed pin gates filing (step 4), never the conversation.

Meanwhile, kick off a read-only exploration sub-agent in the background to learn the domain language for the area (check UBIQUITOUS_LANGUAGE.md) and walk the lineage, meaning which upstream sources feed this surface and which downstream assets consume it. That context shapes the issue; the pinned query and its numbers ARE the issue.

### 3. Assess scope: single issue or breakdown?

Before filing, decide whether this is a **single issue** or needs to be **broken down** into multiple issues. Data symptoms fan out: one upstream defect shows on every downstream surface, and one surface can carry several independent defects.

Break down when:

- The delta segments by dimension: sliced by source, segment, or time period, the anomaly concentrates in more than one place, and each concentration is a separate entry point
- The lineage walk shows independent upstream causes for different parts of the symptom (e.g. "the totals are wrong AND rows are missing AND the freshness stamp is stale")
- Different slices could be fixed and verified in parallel

Keep as a single issue when:

- Every downstream symptom traces to the same most-upstream node: file the upstream defect once and list the affected surfaces in it
- It's one measure wrong at one grain

When breaking down, the most upstream issue blocks the downstream ones: the fix lands upstream, backfills down, and only then can the surfaces be re-verified.

### 4. File the GitHub issue(s)

Create issues with `gh issue create`. Do NOT ask the user to review first; just file and share URLs.

Issues must be **durable**: they should still make sense after major refactors. Write from the user's perspective.

#### For a single issue

Use this template:

```
## What's wrong

[The problem in plain language: which measure, at which grain, under which filter]

## Expected vs actual

[Both numbers verbatim, with the axis named on every pair: e.g. "row count
for the March partition: expected 41,209 (source extract), actual 38,514 (mart)"]

## Evidence

[The pinned query verbatim, with its as-of timestamp. Link the snapshot table
or stored-failures table if one exists. No screenshots.]

## Affected scope

[The grain and cohort as a verbatim predicate, plus the downstream assets
that consume the wrong cells]

## Versions

[Code version that last built the table + the data as-of timestamp]

## Additional context

[Observations from the user or the lineage walk that frame the issue: use
domain language]
```

#### For a breakdown (multiple issues)

Create issues in dependency order (blockers first) so you can reference real issue numbers.

Use this template for each sub-issue:

```
## Parent issue

#<parent-issue-number> (if you created a tracking issue) or "Reported during QA session"

## What's wrong

[This specific slice: one measure, one grain, one entry point; not the whole report]

## Expected vs actual

[Both numbers verbatim for this slice, axis named]

## Evidence

[The pinned query for THIS slice, with its as-of timestamp]

## Blocked by

- #<issue-number> (an upstream defect this slice can't be verified until it's fixed and backfilled)

Or "None: can start immediately" if no blockers.

## Additional context

[Any extra observations relevant to this slice]
```

When creating a breakdown:

- **Prefer many thin issues over few thick ones**: each should be independently fixable and verifiable
- **Mark blocking relationships honestly**: if issue B genuinely can't be tested until issue A is fixed, say so. If they're independent, mark both as "None, can start immediately"
- **Create issues in dependency order** so you can reference real issue numbers in "Blocked by"
- **Maximize parallelism**: the goal is that multiple people (or agents) can grab different issues simultaneously

#### Rules for all issue bodies

- **The pinned query verbatim is mandatory**: the query plus its as-of timestamp are the reproduction steps; if you couldn't reproduce, the issue says so explicitly
- **Magnitudes verbatim**: never round a row count or a dollar figure; the exact number is the audit trail
- **Name the axis on every expected-vs-actual pair**: measure, grain, filter; a bare "755 vs 290" is noise
- **Use the project's domain language** (check UBIQUITOUS_LANGUAGE.md if it exists)
- **Tables, columns, and predicates are the contract; file paths are not**: name models and queries freely, never source files or line numbers
- **Keep it concise**: a developer should be able to read the issue in 30 seconds

After filing, print all issue URLs (with blocking relationships summarized) and ask: "Next issue, or are we done?"

### 5. Continue the session

Keep going until the user says they're done. Each issue is independent: don't batch them.
