---
name: retro
description: Retrospective that turns this session's friction into rule improvements — reviews human corrections, rejected approaches, repeated mistakes, and agent-memory learnings, then proposes minimal skill/rule amendments for sign-off. Use at the end of a work session, after a review with many findings, or when the same mistake happened twice. 日本語の依頼例:「振り返りして」「レトロ」「今日の学びをルールに反映」「また同じミスした」。
---

# Retro — turn friction into rules

The rules improve only if what went wrong feeds back into them. This skill is that loop. Output is a PROPOSAL — `.claude/**` edits need human sign-off (the hook will prompt), so never apply silently.

## Gather (in this order)

1. **This session**: moments where the human corrected you, rejected an approach, re-asked something a rule should have answered, or a gate caught something late that a rule should have caught early.
2. **Recent history**: `git log --oneline -20` + PR review comments if accessible — repeated fix-up commits (`fix:` after `feat:` on the same files) are rule-gap evidence.
3. **Agent memory**: learnings your subagents recorded that are team-relevant (memory is machine-local — promotion to a skill is the ONLY way the team gets them).

## Filter — what deserves a rule

- Happened twice, or cost real time once, AND is generalizable beyond today's file. One-off trivia stays out.
- Not already covered: grep the relevant skill first. If covered but didn't fire, the fix is the skill's `description` (trigger), not a new rule — say which.
- Decidable: the rule must be checkable by a reader ("prefer X" is not a rule; "X unless Y, because Z" is).
- Security/a11y candidates go to `frontend-security`/`a11y` and need human security review per `governance`.

## Propose

For each candidate, output:

- **Target file** (one skill/rule — never CLAUDE.md unless it's a floor-level invariant).
- **The 1-3 line addition**, written in the target file's existing voice, with the why in-line.
- **Evidence**: the concrete moment(s) that motivated it.
- **Enforcement**: can ESLint/Stylelint/Semgrep catch it instead (see `tooling`)? A machine check beats a prose rule — propose the config change if so.

Also propose DELETIONS: a rule nobody has hit in months is a pruning candidate (security/a11y rules are exempt — see `governance`).

End with the proposals as ready-to-apply diffs and wait for sign-off. After applying any, add a `CHANGELOG.md` entry.
