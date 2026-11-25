---
name: where-we-are
metadata:
  version: 1.0.0
  internal: true
description: Delivery gap report (/where-we-are or "what's implemented vs designed?"). Compares HLD containers vs LLD docs and the codebase. Saves snapshot to docs/System Architecture (LLD)/where-we-are/.
---

The developer wants to see the current delivery gap between Target Architecture (HLD) and System Architecture (LLD). Here is their input:

---

## $ARGUMENTS

---

> ⚠️ Follow every step in order. Do not skip, summarize, or improvise. If you are unsure, ask before deviating.

---

## Overview

This skill produces a **delivery gap report**: what has been designed in Target Architecture (HLD) vs what has been documented in System Architecture (LLD) vs what exists in the codebase (the NX monorepo under `apps/`).

It answers the question: _"Where are we relative to where we want to be?"_

Three dimensions are assessed per container:

| Dimension       | Source                            | Meaning                                   |
| --------------- | --------------------------------- | ----------------------------------------- |
| **Designed**    | `docs/Target Architecture (HLD)/` | Container is defined in the HLD           |
| **Documented**  | `docs/System Architecture (LLD)/` | Container has LLD docs (populated folder) |
| **Implemented** | the NX monorepo under `apps/`     | Code exists for this container            |

Gaps between these three dimensions indicate delivery debt, documentation debt, or both.

---

## Step 1 — Determine scope

Read `docs/Target Architecture (HLD)/README.md` to find the **current active version**.

Parse `$ARGUMENTS`:

- If a version is given (e.g. `MVP`): use that version
- If no argument: use the active version

Present:

> "Generating delivery gap report for **\<VERSION\>**. Confirm? (**yes** / **no**)"

**STOP. Do not read any files or take any further action until the developer confirms.**

---

## Step 2 — Read Target Architecture (HLD)

Read, without summarising to the developer:

- `System Overview.md` — container list and responsibilities
- All files in `Containers/` — one per container
- `Non-Functional Concerns/Requirements.md` — NFR targets

Extract per container:

- Name and stated responsibilities
- Technology choices
- Implementation status as stated in the doc (e.g. "TBD", "not yet built", production-ready)
- Any explicit open questions or gaps noted in the doc

---

## Step 3 — Read System Architecture (LLD)

Read `docs/System Architecture (LLD)/README.md`.

Then inspect each container folder under `docs/System Architecture (LLD)/`. For each folder, determine:

- **Empty** — no LLD docs exist yet
- **Partial** — some docs exist but coverage looks incomplete
- **Present** — docs exist and appear to cover the container

Do not judge quality — only presence.

---

## Step 4 — Delegate code scan to @architect

Invoke `@architect` with this prompt (do not deviate):

> "Scan the NX monorepo under `apps/`. For each NX project, identify:
>
> 1. Name and inferred purpose
> 2. Which HLD container it maps to
> 3. Rough implementation maturity: stub / in-progress / functional
>
> Base your assessment on: file structure, entry points, presence of meaningful logic vs placeholders, test coverage, and any README content.
>
> Return a structured list. Do not write files. Do not make changes."

---

## Step 5 — Build the gap matrix

Combine findings from Steps 2, 3, and 4 into a gap matrix. Populate one row per container discovered from the HLD in Step 2 — do not hardcode container names:

```
| Container      | Designed (HLD) | Implemented (code) | Documented (LLD) | Gap |
| -------------- | -------------- | ------------------ | ---------------- | --- |
| <from HLD>     | ✅             | ✅ / ⚠️ partial / ❌ | ✅ / ❌           | ... |
```

Gap key:

- **LLD missing** — designed and implemented but not documented at LLD level → documentation debt
- **Not yet built** — designed but no implementation exists → delivery debt
- **In progress** — partial implementation → in-flight
- **Undocumented design** — HLD container has significant open questions or TBD sections → design debt
- **—** — fully covered across all three dimensions

---

## Step 6 — Produce the full report

Structure:

```markdown
# Delivery Gap Report — {VERSION}

_Generated: {YYYY-MM-DD}_

---

## Summary

<2–3 sentence narrative: overall delivery posture, dominant gap type, most critical gaps>

## Gap Matrix

<table from Step 5>

## Delivery Debt

Containers designed and coded but not yet documented in System Architecture (LLD):

<list with recommended LLD content for each — what would be most valuable to capture>

## Documentation Debt

<Same containers with LLD as empty or partial — what specifically is missing>

## Design Debt

HLD containers with significant open questions or TBD sections that should be resolved:

{list}

## Recommended next actions

| Priority | Action | Command                                                                              |
| -------- | ------ | ------------------------------------------------------------------------------------ |
| P1       | ...    | `/dev document {TICKET}` or `/design {TICKET}` |
| ...      |        |                                                                                      |
```

---

## Step 7 — Present and offer to save

Present the full report in the console.

After presenting:

> "Gap report complete. Save as a dated snapshot? (**yes** / **no**)"

If yes, use `.claude/skills/where-we-are/report-template.md` as the file structure. Replace all `{{VERSION}}` and `{{YYYY-MM-DD}}` placeholders with actual values, populate the gap matrix with the containers discovered from the HLD (one row per container — do not hardcode), and fill in all report sections.

Save to:

```
docs/System Architecture (LLD)/where-we-are/{YYYY-MM-DD}-gap-report.md
```

Create the `where-we-are/` directory if it does not exist.

---

## Step 8 — Close

After saving (or if developer declined):

> "Saved to `docs/System Architecture (LLD)/where-we-are/{date}-gap-report.md`.
>
> To re-run after new deliveries: `/where-we-are`
> To document a container's LLD: `/dev document {TICKET}`
> To run a full WAF code audit: `/war implementation`"
