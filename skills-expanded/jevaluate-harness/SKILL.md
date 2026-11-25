---
name: jevaluate-harness
description: Use when running a jevaluate rating round, re-rating after a rubric change, changing the jevaluate rubric, or publishing ratings to the jev-mode ratings folder.
---

# Jevaluate Harness

The maintainer's process for `jevaluate-publish`. One rating is `jevaluate/read.md`; testing the rubric is the `jevaluate-eval` skill. If `$JEVALUATE_OVERLAY` is set, read that file first; its rules override the defaults here.

## Settings (yours, not in this skill)
- `$JEVALUATE_LIBRARY`: the private ratings library (default `~/.claude/jevaluate-library` if it exists, else `~/.jevaluate-library`).
- `$PRIVATE_TERMS`: your never-publish regexes, one per line. `library.py export` reads only `$JEVALUATE_LIBRARY/private-terms.txt`, so keep the file there (or symlink it) and have your pre-push hook read the same file.
- `$JEVALUATE_OVERLAY`: a markdown note of your own rules for these workflows, read first; no required format.

## Two principles
- **Code checks, text explains:** every rule has a row in `jevaluate/enforcement.md` naming the check that refuses a wrong answer, or why it stays judgment.
- **Ask for what is observed:** raters record type, the calls-Jev line, each decision's stakes as read and the verdict; `library.py add` derives kind and every n.a.

## Workflows
Open the file for the workflow and follow it in order; each step names the gate that must pass.

| Workflow | File | Done when |
|---|---|---|
| Change the rubric | `rubric-change.md` | `jevaluate-eval` passes and the owner approves the version |
| Rate or re-rate projects | `rating-round.md` (rater prompt: `rater-brief.md`) | every rating logged by `library.py add`, scan clean |
| Publish ratings | `publish.md` | one pull request, reviewed |

To see where you are: `python3 jevaluate-harness/scripts/harness_status.py <ledger> --workflow rubric|round` (`round` runs through publishing). It reruns the scripted gates it has (the materials check), reads the other steps from the ledger, and names the file to open next. Ledger lines: `done: <step> <YYYY-MM-DD> <evidence>`. Steps: rubric = rules-written, materials-checked, quiz-passed, eval-passed, owner-approved, frozen; round = picked, sized, costs-approved, rated, scanned, adjudicated, final-gate, release-check, published.

Keep a ledger per workflow: each step, each ruling with its cost if wrong, and tokens per agent. Record rulings and handoffs where your overlay says, or in the ledger.

## Enforced by

| Rule | Enforced by |
|---|---|
| A rater never reads the rubric, past ratings or a full-file copy directly | `scan_transcripts.py`; `test_scan.py` |
| A freeze tag goes only on a merged commit whose rubric title carries its version | `freeze_tag_check.py` |
| A workflow's scripted gates are rerun, not read from the ledger | `scripts/harness_status.py`; `test_status.py` |
| Every release check passes before publishing | `scripts/check_release.py`; `test_release.py` |
| Each step followed in order, rulings recorded with their cost if wrong | LLM's judgment following instructions |
