---
name: slopbuster-fix
license: Apache-2.0
description: Remediate the findings from a SlopBuster audit and record a fix-result report — what was actually fixed, which audit and which findings/phases it addresses, what changed, and the before→after health delta. Use after an audit when asked to fix the issues, work through the fix plan, remediate findings, or close out an audit; also use to record a remediation that already happened. Produces a structured fix.json + fix.md that links the fix back to the audit so a dashboard can track audit → fix → improvement over time.
---

# SlopBuster — Fix

You are closing the loop on an audit: take its findings and **fix-plan**, do (or record) the
remediation, and write down **what was actually fixed** — tied to the audit it came from. Detection
without follow-through is where audits die in a drawer; this is the receipt that the work happened,
and the input a team dashboard uses to track health over time (audit → fix → re-audit).

Your output is a **result report**, not a plan and not a wish-list. It says, finding by finding,
what changed and whether it's resolved — grounded in the real diff, never claimed.

## Before you fix

1. **Find the audit you're remediating.** Read the newest (or named) audit at
   `.slopbuster/audit/<version>/` — its `scores.json` (the structured findings) and `fix-plan.md`
   (the prioritized, phased plan). That audit is what this fix **addresses**; capture its version,
   its overall grade/numeric, and the commit the code was at when it was audited.
2. **Work the plan in its phases.** The fix-plan is dependency-ordered (quick wins → structural);
   follow that order. Prerequisites before the work that depends on them.

## Fix, then tell the truth about it

For each finding you take on, make the real change, then record it honestly:

- **`status`** — `fixed` (resolved), `partial` (mitigated, not fully closed), or `wontfix` (with a
  reason). Never mark `fixed` what you didn't actually change — the report must match the diff.
- **What changed** — the concrete edit: the file(s) and line(s) touched, and a short markdown
  description of the change (a numbered list when it took several steps). Ground it in the real
  edit, cite `file:line`.
- **Which finding it closes** — link back to the audit finding by its category + `n` (and title), so
  the report maps one-to-one onto the audit's findings.

Group the items into the same **phases** the fix-plan used, so the report reads as "here's what each
phase of the plan actually accomplished."

## Verify the delta (strongly preferred)

The most valuable line in the report is **before → after**. When you can, **re-run the audit**
(`slopbuster-audit`) on the fixed code and compare: overall grade/numeric before vs after, and how
many findings closed. If a full re-audit isn't possible, estimate conservatively and say so — never
inflate the after-number. A fix report whose "after" is unverified must label it as an estimate.

## Don't introduce new slop while fixing

A remediation that adds dead code, a speculative abstraction, or a band-aid that masks the symptom is
not a fix. Hold the same bar the audit holds: the change should be the smallest correct thing that
closes the finding, in the layer where it belongs.

## Output: a structured result + a readable report (its own folder)

Each SlopBuster artifact lives in **its own folder**, one versioned subdir per run. Write the fix
report into `.slopbuster/fix/<version>/`:

```
.slopbuster/fix/<YYYY-MM-DD>/
  fix.json     ← structured result the app reads (links to the audit)
  fix.md       ← the readable report: phases, what was fixed, before→after
```

`<version>` is a date (`date`) or version label. Create the dir if missing. If the app passes an
explicit target dir, write there. Tell the user the path when finished.

### `fix.json` — the structured result

```json
{
  "addressedAudit": {
    "version": "<the audit version dir name, e.g. 2026-06-11>",
    "commit": "<commit the code was at when audited>",
    "overallGrade": "D",
    "numeric": 61
  },
  "summary": "<2–3 SHORT sentences — what was fixed and the delta; teaser, full detail in fix.md>",
  "result": {
    "beforeGrade": "D", "beforeNumeric": 61,
    "afterGrade": "C",  "afterNumeric": 67,
    "afterVerified": true,
    "resolved": 12, "partial": 2, "wontfix": 1, "open": 17
  },
  "meta": {
    "generatedBy": "<tool + model, e.g. 'claude-code / claude-opus-4-8' — never blank>",
    "author": "<git log -1 --format=%an>", "email": "<git log -1 --format=%ae>",
    "commit": "<git rev-parse HEAD — the fixed state>", "branch": "<current branch>",
    "generatedAt": "<ISO-8601 — date>"
  },
  "phases": [
    {
      "key": "phase-0",
      "label": "Phase 0 — critical security & correctness",
      "items": [
        {
          "addresses": { "category": "security", "n": 1, "title": "..." },
          "status": "fixed",
          "what": "<markdown: what changed, a numbered list when multi-step>",
          "files": ["crates/sync/hive_proto/src/lib.rs:647"],
          "commit": "<sha that made this change, if known>",
          "effort": "S"
        }
      ]
    }
  ],
  "doc": "fix.md"
}
```

Field rules (camelCase; do not rename or add fields):
- **`addressedAudit`** — which audit this remediates (version + the audited commit + that audit's
  overall grade/numeric). This is the link the dashboard uses to pair a fix with its audit.
- **`result`** — the before→after. `beforeGrade/beforeNumeric` come from `addressedAudit`;
  `afterGrade/afterNumeric` from the re-audit (`afterVerified: true`) or a labeled estimate
  (`afterVerified: false`). `resolved/partial/wontfix/open` tally the findings.
- **`meta`** — attribution (who fixed it, with what), same shape as the other skills. Never blank.
- **`phases[]`** — mirror the fix-plan's phases. Each `items[]` entry maps to one audit finding via
  `addresses` (`category` + `n` + `title`), with `status`, the markdown `what`, the `files` touched,
  the `commit`, and `effort`. The set of items should cover the findings you actually worked.

### `fix.md` — the readable report

Lead with a short summary + a **before→after table** (grade/numeric, # resolved/partial/open). Then
one `##` section per phase, and under each a numbered list of items: each says which finding it
closes (`Security #1 — <title>`), its **status**, what changed (with `file:line` and a numbered
step list when it took several), and the effort. Use rich, scannable markdown — tables, lists,
headings — not a wall of text. End with what's still open (the findings not yet addressed) so the
next pass has a clear starting point.

The report is honest only if it matches the diff: every `fixed` must be a real, verifiable change.
