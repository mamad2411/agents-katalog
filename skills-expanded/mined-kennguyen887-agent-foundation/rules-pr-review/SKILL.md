---
name: rules-pr-review
description: Binding personal rules for reviewing a pull request or diff — load before reviewing any PR (own or others'), writing review comments, or judging datasets/DTOs/API shapes/fetch effects/polls in a change.
---

# rules-pr-review

These rules are binding (moved verbatim from ~/.claude/CLAUDE.md). Each heading names its full-text file in `~/.claude/rulebook/`: **Read that file before acting in its area** — the one-liners are the trigger, not the whole rule.

## PR Review — `04-pr-review-comment-rules.md`
- **Read the task first** (Linear key/link in PR title/body/branch, or Slack): is it solved fully, at root cause, no guessed/workaround fix, safe; flag release prerequisites elsewhere (env/config/migration/flag/companion PR) inline on the related line. Comment voice: dev-casual, short, light natural humour.
- Inline comments on the exact changed line (RIGHT side); never one summary comment. Skip nits; only real bugs/regressions/lost data/broken contracts. Every comment has suggestion code. Short basic English: problem → impact → fix.
- **Review what ships**: for datasets/generated files/API shapes/DTOs/selects/cache entries, walk field-by-field and name each field's reader; no reader = delete it. Check per-consumer projections, derivable duplicate files, and comments that rationalize waste ("unread", "unused", "we only use") — treat as a flag. Cost findings in bytes (min + gzip). Green CI is not evidence.
- **Count requests**: on fetch effects/polls/data hooks/infinite lists — dep array as inputs (no own-output deps, primitive not object deps, booleans whose initial value fires the branch); poll `enabled` names the pending condition, stop covers all terminal states, pauses hidden, has max duration; one owner per resource per page; diff gate comments against code; fix one → grep siblings. Verify by measuring per-endpoint request counts.
