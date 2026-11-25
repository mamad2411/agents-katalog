---
name: expert-defect-correction
description: This skill should be used when correcting a defect in the expert-dev-tools plugin itself — an entry from docs/defects/, a crash in the workflow, a control that fires wrongly, or any report that the plugin misbehaves. It covers verifying the report before acting, re-deriving instead of patching, sweeping the class, proving each new check fails on the pre-fix behavior, the review loop and its convergence tripwire, shipping so the fix actually deploys, and closing the defect. Read it before editing any plugin file in response to a defect.
---

# Correcting a defect in this plugin

A correction that is not durable is worse than none: it consumes a review cycle, closes
the reported instance, and leaves the class open — so the same defect returns wearing a
different symptom, and the record says it was fixed.

Every rule here was learned by failing first. The evidence for each is in
`references/why-these-rules.md`; read it when a rule seems like overhead, because the
reason it exists is usually the shortcut being considered.

## Before touching anything

**Verify the report.** A defect entry is a claim, not a fact. Re-derive its premise from
current source — line numbers drift, and a report can name the wrong cause for a real
symptom. If the premise is false, record that with evidence and change nothing. Reports
have been wrong about their own counts and locations in this repo more than once.

**Establish which code is running.** The plugin exists in the working tree and in the
installed cache under `~/.claude/plugins/cache/`. Run
`node scripts/preflight-deployment.mjs expert-dev-tools <worktree>` and read its verdict
before treating any file as the failing code. A defect reproduced against the wrong copy
is not reproduced.

**Reproduce by execution, not by reading.** If the failure cannot be made to happen on
demand, say so rather than shipping a plausible-looking edit. A fix for a defect that was
never reproduced cannot be shown to have fixed anything.

## Making the correction

**Re-derive; do not patch the reported line.** A finding is a symptom. Work out what the
code was supposed to establish, then write that — rather than editing the sentence the
report points at until the symptom stops.

**Sweep the class.** State the pattern searched, the scope searched over, every site
found, and every site changed. A found site that is neither changed nor explicitly
designated is an open defect, not a silence. Corrections that closed the named instance
and left siblings are the single most repeated failure recorded here.

**Do not reason from neighbouring files.** Matching what similar code does is pattern
matching, and this plugin's own standard forbids it. Derive from the standard, not from
the sibling.

**Do not increase hand-maintained data.** If the fix adds a number, a list, or an index
that a human must keep in step with something else, it will drift and become the next
defect. Generate it, or eliminate the form that needed it.

## Proving it

**Every behavior change gets a check that FAILS on the pre-fix behavior.** Not a check
that passes now — one that would have caught this. Prove it: revert the fix on a scratch
copy, confirm the new check goes red, restore.

**Probe on scratch copies or an isolated git-backed worktree, never the working tree.** A
bare directory copy fails a few checks for environmental reasons — the repo-root linter
and the git baselines — so account for that rather than reading it as defect. A
git-backed copy at a short path resolves the baselines.

**State exactly what a check covers.** A check whose label claims more than its predicate
can establish is worse than no check, because it reads as protection. Name the forms it
recognizes and name what it does not cover.

**Run both tiers**: `node tests/structural/check-structure.mjs` and
`node tests/unit/run-unit-tests.mjs`. Never take counts from a commit message or a review
record — run them.

## Review

Corrections go through independent review before shipping. Dispatch a **fresh reviewer
each round**, give it **pointers only** — the diff, the artifacts, the prior records — and
never a summary of what changed or where to look. Author-supplied direction is what
compromised most rounds on the sister project. The reviewer persists its own record and
returns a verdict; findings are never hand-copied through the conversation.

Apply **all** findings from a round, not a chosen subset.

**Track convergence every round**: findings closed, new, regressions, recurring, and the
round-over-round total. Either of these stops the loop:

- new + regressions ≥ closed, for two consecutive rounds, or
- the total not strictly decreasing, for two consecutive rounds.

Either one means further correction rounds are expected to make the artifact worse.
The answer is foundational rework — eliminating the form that keeps producing findings —
not another round. Widening a boundary that has already been widened twice is the shape
this repo has watched fail three times.

## Shipping

**Bump the version in `.claude-plugin/plugin.json`.** The updater compares versions; a fix
shipped without a bump is never installed, and the defect stays live while the record says
it is fixed.

**Verify against the deployed copy, not the working tree.** After the owner updates and
reloads, exercise the fixed behavior from
`~/.claude/plugins/cache/claude-armory/expert-dev-tools/<version>/`. Two defects in this
plugin were invisible to eight review rounds and appeared within a day of deployment,
because each check had been green for a reason unrelated to what it claimed.

**Close the defect**: set `state: corrected` and `fixed_in:` to the shipped version in its
`docs/defects/` file, then re-run `node scripts/derive-defect-index.mjs`. The structural
tier fails if the index is stale.

## Additional resources

- **`references/why-these-rules.md`** — what each rule cost to learn, with the specific
  failures behind it. Read it when a rule looks like overhead.
