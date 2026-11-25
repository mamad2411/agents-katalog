---
name: interrogate
description: >-
  Have reviewers from different model families review the same change independently, then reconcile
  their findings by running code instead of voting. Use for "interrogate this", "adversarial review",
  "cross-model review", "second opinion from Codex/Claude", "stress test this change", "find what I
  missed", and before merging security, data, concurrency, parser or money-handling changes.
---

# Interrogate

One reviewer has blind spots. A second reviewer from the same model family tends to share them.
Reviewers from different families, briefed identically and kept apart, miss different things. The lead
then treats every finding as a claim to check, not a vote to count.

## When it applies

- A non-trivial change that is costly to get wrong: auth, permissions, payments, migrations, storage,
  concurrency, parsers and sanitizers, anything that deletes.
- A change you wrote yourself and now can't see fresh.
- The user asks for a second opinion.

Skip it for small, low-stakes diffs. One good reviewer is enough there, and this costs at least two
full reviews.

## Reviewers

Use two by default and three at most. Pick them from different model families:

| You are running in | Reviewer A | Reviewer B |
| --- | --- | --- |
| Claude Code | a subagent on your strongest Claude model | `codex exec` with a read-only sandbox |
| Codex | yourself, in a fresh context | `claude -p` with read-only tools |
| OpenCode or other | a subagent on one provider | a subagent on another provider |

Use the CLIs you're already logged in to. Don't spend a paid API key on this without the user's okay.
If only one model family is available, use one reviewer per family you do have, and say in the report
that the review isn't cross-family.

## Procedure

### 1. Write one brief and give it to every reviewer, unchanged

```
Review this change for defects: <diff command or file list, base..head>.
Context: <what the change is for, in two sentences>.
Report only defects you can state as a concrete failure: the input or state, what happens, what
should happen. For each: file:line, severity (critical / high / medium / low), the failure scenario,
and how to reproduce it. No style notes. No praise. If you find nothing, say so.
Write the full report to <path>, and return the path plus a one-line summary.
```

Don't tell a reviewer what you suspect, and don't show it another reviewer's output. A hint anchors
it, and the point is independent views.

### 2. Run them in parallel

Start every reviewer at once. A Codex review from inside Claude Code, for example:

```bash
codex exec -s read-only "$(cat brief.md)" > review-codex.md
```

### 3. Reconcile: each finding is a claim

Merge the reports into one list, deduplicating findings that describe the same failure. Then settle
each one:

| Verdict | When |
| --- | --- |
| CONFIRMED | You reproduced it (a failing test, a script, a request), or you read the code path and it fails exactly as described. |
| REJECTED | You showed it can't happen: quote the guard, the type or the test that rules it out. |
| OPEN | You could neither reproduce nor rule it out. Keep it, with what you tried. |

Found by two reviewers is a strong hint, not a confirmation; found by one isn't a reason to drop it.
A finding where the reviewers disagree is the most valuable to settle by running code.

### 4. Report

```
Reviewers: <model A>, <model B>   Diff: <base..head>

| # | Finding | Found by | Verdict | Evidence |
| 1 | <failure, file:line> | A, B | CONFIRMED | test X fails: <output> |
| 2 | <failure, file:line> | B | REJECTED | guarded at file:line |
| 3 | <failure, file:line> | A | OPEN | tried <...> |

Fix first: <confirmed findings, worst first>
```

## Rules

- Same brief for every reviewer, word for word.
- No reviewer sees another's findings before reconciliation.
- Every verdict carries evidence: a command and its output, or a quoted line.
- Fixing the confirmed findings is a separate step. Re-run only the reviewer whose finding you fixed,
  on the fix, not the whole panel.
- ystack's `review-panel` mod picks specialist reviewers by diff; `interrogate` is the cross-model
  pass on top, for the changes where that matters.
