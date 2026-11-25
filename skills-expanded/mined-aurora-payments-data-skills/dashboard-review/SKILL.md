---
name: dashboard-review
description: Use when reviewing, critiquing, or QA-ing a dashboard, when a rebuilt surface must be compared against the one it replaces, or when dashboard numbers need tying to governed warehouse sources before ship. Also use for pre-publish review of any new dashboard.
---

# Dashboard Review

Review a dashboard against the org's rubric, tie its numbers to source, and file a critique with a verdict. The rubric is the canon; this skill is the process. `docs/agents/dashboards.md` resolves the tool, the rubric, and where artifacts land; load the tool-mechanics reference it names before touching the workbook.

## Hard rules

1. **Read the org's dashboard rubric first** (path in `docs/agents/dashboards.md`; the config's starter hard rules apply only until an org rubric exists). Every finding scores against it; the verdict contract and tie-out protocol live there. Do not restate rubric content in the critique; cite its sections.
2. **Discrepancies are flagged, never chased.** A mismatch gets: the cell, both values verbatim, the obvious candidate cause, then STOP. No exploratory analysis without explicit permission. Route to engineers. This applies even when one more query would "probably confirm it."
3. **Same-moment pairs.** Live workbooks move intra-day and can be edited while you review (it has happened mid-review). Read every compared pair back-to-back in one session, timestamp the critique, and never compare a value you read an hour ago against one you read now.
4. **Every finding carries evidence**: an element ID, a query, or a screenshot filed with the critique. No bare opinions.
5. **Labels are not definitions.** A chart titled "Submitted" may not count submissions (a real reviewed workbook's "Submitted" was the decided count). Verify what a metric is from the element's formula or query (per the tool reference), not from its title.

## Workflow

1. **Scope.** Resolve the workbook's canonical ID, owner, and created/updated timestamps (per the tool reference, since a URL slug is rarely the API ID). Name the basis workbook (if a rebuild) and the governed source-of-truth tables, and read the build spec's Tie-Out Basis section if one exists; it pre-registers the compared cells.
2. **Structure.** Enumerate every element and its query (per the tool reference). Elements sharing IDs across two workbooks mean one was copied from the other, so ties on shared-ID elements confirm the copy didn't drift; only differently-derived elements are real independent ties.
3. **Visuals.** Capture every page, top to bottom, at desktop resolution (per the tool reference). Score look-and-feel against the rubric's card-anatomy, layout, canvas-width, and color/theme guidance.
4. **Tie-out** (rebuilds: vs basis; new builds: vs governed marts). Enumerate cells per the rubric's tie-out protocol: overall headline KPIs + 2–3 drill paths per major metric, identical filter state both sides. Classify each cell `TIE / EXPECTED-MISMATCH (named, documented change) / UNEXPLAINED-MISMATCH`. Values verbatim, element IDs recorded.
5. **Verdict** per the rubric's verdict contract. Any hard-rule violation or unexplained headline mismatch = NEEDS REVISION.
6. **File artifacts** (homes in `docs/agents/dashboards.md`):
   - Critique doc: plain-English lead ending in the verdict → tie-out table → mismatch notes → hard-rule findings with fixes → checklist findings in severity order → basis-regression check (rebuilds) → what works → routing.
   - Evidence captures filed alongside, named so they survive the workbook changing.
   - Fixes cite the rubric's how-to references so the builder gets mechanics, not just complaints.
   - A draft note to the surface's owner: draft only; the user sends.

## Tool mechanics

Load the reference file matching the org's BI tool before touching the workbook. `docs/agents/dashboards.md` names its path; `sigma.md` ships with this skill, and any other tool has a file at `docs/agents/bi-mechanics-<tool>.md` that `/setup-data-skills` created.

**Expect that file to be empty or thin, and write into it as you go.** It holds what only driving the tool teaches: how to resolve a stable ID from a URL, how to read an element's underlying query, which path forms fail, and what breaks when capturing a screenshot. Every one of those cost someone a wrong turn. Record each under the matching heading the moment it works, with the exact call or step, so the next reviewer starts where you finished.

Record only what you ran. A remembered API path that turns out to be wrong is worse than a blank heading, because the next reviewer trusts it and spends the detour proving it wrong.

## Red flags: stop and re-read the hard rules

- "One more query would tell me why the numbers differ" → rule 2. Note and route.
- "I'll compare against the value from my earlier screenshot" → rule 3. Re-read both now.
- "The title says what it counts" → rule 5. Describe the element.
- "The rubric surely allows this, no need to open it" → rule 1. Open it.
- Filing findings without an element ID, query, or screenshot → rule 4.

## Common mistakes

- Comparing a rebuild's control-filtered custom view against the basis' unfiltered default. Freeze identical filter state first (custom-view links often carry a pre-set filter).
- Treating a shared-lineage tie as independent confirmation: it only proves the copy didn't drift.
- Calling a provisional-month decline a trend: check the workbook's own freshness element against the KPI period before reading any delta.
- Minting DQ registry entries for upstream defects found during review: flag in the critique, mint only with the user.
