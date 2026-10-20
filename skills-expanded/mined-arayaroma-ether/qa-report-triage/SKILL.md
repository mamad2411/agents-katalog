---
name: qa-report-triage
description: Use when the user wants to see or act on findings that have piled up in `.ether/qa/jobs/*/report.md` (e.g. "what did the reviews find", "show me the action pipeline", "apply the fixes from the reports"). Reads raw findings written by any local job type built on the `ether job` router, turns them into a triaged action list (bug/warning/note, severity), and applies only the ones the user (or the earned autonomy tier) approves — never invents fixes beyond what a report actually said. Fully offline — no network calls of its own.
allowed-tools: Read, Edit, Write, Grep, Glob, Bash
---

# QA Report Triage

Any job type built on ether's job router (`ether job add/pending/
record-run/should-confirm/status`, backed by `.ether/jobs.db`) can write
raw findings to `.ether/qa/jobs/<jobId>/report.md` as its own convention
for persisting what it found. This skill is the second stage: it reads
what already accumulated, turns it into a reviewable action pipeline, and
applies only what's approved — through the *same* crystallization gate
(`ether job should-confirm`), so triage doesn't become a bypass for the
autonomy state machine.

**No specific job type is assumed.** ether-pro (the networked sibling
harness) has `repo-review-job`/`web-review-job` producing these reports
via `gh`/browser automation — those aren't ported here (they need
network). This skill works with whatever local, offline job type writes
to the same `report.md` convention — a local linter/audit job, a
find-related-code job, anything built on the job router that follows the
`.ether/qa/jobs/<jobId>/report.md` shape.

**Scope discipline**: this skill only acts on what a report explicitly
says. If a report's "Findings" section is `(none)` or a "Follow-up" note
is vague, surface it as a low-severity note, don't infer a fix that isn't
there. Interpreting intent beyond the report text is out of scope — ask
the user instead of guessing.

## Workflow

1. **Collect reports.** For a given target (repo path or "all"), read
   `<target>/.ether/qa/jobs/*/report.md` — every report not yet marked
   triaged (see step 4 for how that's tracked). If none, say so and stop.

2. **Build the action pipeline.** For each report, extract one action
   item per finding/follow-up line, structured as:
   - `severity`: `bug` (correctness issue) | `warning` (drift, risk, or a
     follow-up the report flagged) | `note` (informational, no action
     implied)
   - `summary`: one line, taken from the report's own wording
   - `source`: `report path:section`
   - `proposed fix`: only if the report itself proposed one; otherwise
     `none — needs a decision`

   Present this as a table, most-severe first (bug > warning > note).
   Don't pre-filter — even `note`-severity items go in the table so the
   user sees the full picture, but only `bug`/`warning` items are
   candidates for the "apply" step.

3. **Apply, gated by the existing tier.** For each `bug`/`warning` item
   with a concrete proposed fix that the user selects (or that
   `params.autoApply` on the originating job allows):
   - `ether job should-confirm --type <job type> --actionType write`.
   - `confirm` → **present the fix and stop. Do not run the fix command
     yet.** Wait for the user's explicit reply approving it, in a separate
     turn, before touching any file. Presenting a diff/preview is fine;
     applying it before hearing back is the exact failure this rule
     exists to prevent.
   - `autonomous` → apply it directly with normal file tools.
   - Record via `ether job record-run --jobId <the item's originating
     job id> --agent qa-report-triage --actionType write --outcome
     success|failure [--confirmedByHuman]` — same ledger, so triage
     applications count toward that job type's promotion/demotion same as
     a direct write action would.

4. **Mark triaged.** Append a `## Triage` section to the bottom of each
   processed `report.md` (edit in place) listing what was applied,
   skipped, or left as a decision for later — this is what step 1 checks
   to avoid re-triaging the same report every run.

5. **Report to the user**: how many reports collected, the action table,
   what got applied vs. what's still pending a decision, and which job
   types moved autonomy tiers as a result.

## Not in scope

- Don't triage a report from a job type you don't have registered
  handling for — say so and skip it rather than guessing what "applying"
  means for an unfamiliar job type.
- Don't batch-approve everything because "it's just triage" — severity
  sorting is for the user's benefit, not a shortcut around the confirm
  gate for anything still at tier 3.
- Don't reach for `repo-review-job`/`web-review-job` by name — they don't
  exist in this harness. If the user wants that class of automated
  review, they need a local, network-free job type first (see
  `ether-scope-estimate`/`ether-tdd` for how to build one under TDD).
