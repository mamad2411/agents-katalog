---
name: defect-first-review
description: Perform a read-only, defect-first review of a specified code change and return every actionable finding, reading the whole diff before running anything. Use when another agent delegates review of uncommitted changes, a base-branch diff, a commit, or custom review instructions. Prefer this over the Codex-bundled review-agent, which carries no read-before-you-run gate.
---

# Defect-First Review

Repo-owned successor to the Codex-bundled `review-agent`. That one lives under
`~/.codex/skills/.system/` and is replaced on every Codex update, so edits to it do not survive;
this one is canonical in `ohyeh/agent-scripts` and ships through `skills-lock.json`. The rename is
deliberate — two skills named `review-agent` would be indistinguishable at the call site.

Inspect the requested target directly and return every finding that the author would likely fix.
Do not modify files, create commits, push branches, post review comments, or delegate the review
to another agent.

## Order of work — read before you run

Reading the diff IS the work. Until the semantic pass over the whole diff is finished and the
findings are written down, do not run builds, test suites, linters, formatters, or static
analysis. A suite result says nothing about whether this change introduced a defect — it reports
what the author's tests already cover — and any failure it does surface will pull the review onto
that failure instead of the diff you were asked to read. Measured 2026-08-28: a review that
started a full test run 2.4 minutes in made 5 test/analyze calls, never finished the semantic
pass, and reported on the wrong thing.

Verification is scoped to findings, not to the repository. Once a finding is written down you may
run the narrowest command that reproduces that specific finding — one test, one file, one
analyzer path. "Run the whole suite and see what breaks" is not verification; it is a substitute
for the review. If the requester explicitly asks for a test run, say what the review still owes
before running it, then run it.

Read with ranged reads: `git diff -U5` to `-U10` for the changed hunks, and line ranges
(`sed -n`, `nl -ba | sed -n`) for the surrounding code. Never dump a whole source file — a review
that has read eight whole files has spent its context on the 95% that did not change, and every
later turn re-carries it.

## Review the change

1. Read the applicable `AGENTS.md` instructions.
2. Inspect the complete diff for the requested target and enough surrounding code to understand
   each changed path.
3. Identify concrete regressions introduced by the change. Continue through the whole diff after
   finding the first issue.
4. Check the relevant tests and call sites to confirm that each finding is real and actionable.

For a base-branch review, compare the changes that would actually merge rather than diffing
directly against the branch tip. Resolve the comparison ref to the branch's upstream when that
upstream exists and is ahead of the local branch; otherwise use the local branch. Run
`git merge-base HEAD <comparison-ref>`, then inspect `git diff <merge-base-sha>`. If the local
branch cannot be resolved, try its configured upstream explicitly before reporting that the target
is unavailable.

Flag an issue only when all of these are true:

- It affects correctness, security, performance, or maintainability in a meaningful way.
- It is discrete and actionable.
- It was introduced by the reviewed change.
- The affected scenario or call path can be demonstrated from the code.
- The author would probably fix it if they knew about it.

Do not flag speculative concerns, pre-existing problems, intentional behavior changes, or style
nits that do not obscure the code.

## Write the result

Present findings first, ordered by severity. Use one entry per issue in this form:

`[P1] Imperative finding title — path/to/file.rs:line`

Follow the title with one short paragraph explaining the affected scenario and why the behavior is
wrong. Keep the cited range as small as possible and make sure it overlaps the reviewed diff.

Use these priorities:

- `P0`: universal release blocker or critical failure.
- `P1`: urgent defect that should be fixed next.
- `P2`: ordinary defect that should be fixed.
- `P3`: low-impact issue that is still worth fixing.

If there are no qualifying findings, say `No findings.` Do not invent a finding to fill the result.
After the findings, add a brief overall assessment and mention any material test gaps or residual
risks.
