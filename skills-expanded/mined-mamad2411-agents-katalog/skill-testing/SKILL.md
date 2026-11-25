---
name: skill-testing
description: Acceptance-tests any skill by running it through a fresh-context subagent with a minimal prompt, then verifying the output with mechanical checks only (grep, regex, counts, diff) so tester bias is isolated. Use when asked to test, verify, regression-check, or confirm a skill still behaves as its SKILL.md describes.
---

# Skill Testing

Prove a skill still does what its SKILL.md says — by running it blind and
checking the result mechanically. The discipline is the whole point:
**execution and verification never share knowledge.**

## Step 1 — Identify the target

Collect: the target skill name/path, the input (URL, file path, transcript,
topic), and the output location if it writes files. Ask only if these are
unclear.

## Step 2 — Execute with a minimal-prompt subagent

Dispatch a fresh-context subagent (in Claude Code, the Agent tool). Its
prompt contains ONLY: the target skill reference, the input, and the output
path. See [references/execution.md](references/execution.md) for the exact
template and sandbox setup.

Forbidden in the prompt: the target's rules, field names, formats,
examples, banned words, categories, or any expected result. Restating them
tests your prompt, not the skill.

## Step 3 — Extract mechanical rules from the target's own docs

Read the target `SKILL.md` and every file it transitively references. From
those — never from memory or the user's prompt — extract checkable rules
and classify each (details and judgment rules in
[references/verification.md](references/verification.md)):

- **must-contain**: a string/structure must appear → `grep -c > 0`
- **must-omit**: a string must not appear → `grep -c == 0`
- **count**: X must equal a sum → arithmetic compare
- **format**: IDs/links/fields match a regex → regex check

A rule is verifiable only if grep/regex/count/diff settles it. Rules
needing semantic judgment ("is the wording clear") are recorded as
**not-verified**, not guessed.

## Step 4 — Run the checks

Run each check against the Step 2 output; record pass/fail with expected
vs actual. For stateful skills use the sandbox proofs in
[references/execution.md](references/execution.md) (isolated dir with
declared preseeds; git-based zero-diff idempotency proof; additions-only
diff).

## Step 5 — Three-part report

1. **Execution summary** — what the subagent reported back.
2. **Mechanical results** — passed N / failed M; for each failure the
   source rule, expected, and actual; overall verdict.
3. **Not mechanically verified** — the rules skipped in Step 3, so the user
   knows what still needs a human eye.

## Principles

| Principle | Meaning |
| --- | --- |
| Two roles, no shared knowledge | The subagent runs; the main session verifies. Neither sees the other's rules. |
| SKILL.md is the only source of truth | Checks come from the target's docs, not your memory or the user's prompt. |
| Failure beats a pass | A pass only means the checked rules held; a failure always means the skill or its SKILL.md has a real gap. |
| Repeatable | Same (skill, input) must yield the same mechanical verdict; if not, the SKILL.md is underspecified. |

Passing ≠ good — it means the mechanically-checkable rules held. Flag the
rest for human review.
