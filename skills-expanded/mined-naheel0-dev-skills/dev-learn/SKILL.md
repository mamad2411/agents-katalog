---
name: dev-learn
description: >-
  Close the dev.to feedback loop after an audit - promote winning title
  formulas and tags, demote losers, and feed the updated weights back into
  the next dev-post draft. Run after /dev-audit once the post log has data.
---

# dev-learn

Turns what `/dev-audit` found into weights the next `/dev-post` draft actually uses.

`analytics + ~/.claude/devto/log.md` -> `/dev-audit` -> `dev-learn.py audit --apply` -> reweighted formulas/tags -> next draft.

## When to run

After `/dev-audit` has filled `engagement_rate` for the logged posts. The script
needs at least 10 audited posts; below that it reports the count and changes nothing.

## Run it

```bash
python3 ~/.config/opencode/skills/dev-learn.py audit           # dry-run: show proposed changes
python3 ~/.config/opencode/skills/dev-learn.py audit --apply    # write them
```

`status` is an alias for `audit` if you only want the current weights.

## What changes

- `dev-post/title-formulas.json` - +0.1 weight when a formula's mean engagement >= account mean, -0.1 when <= half the mean. Weight 0 moves to `archive`.
- `dev-post/tag-suggestions.json` - same rule for `broad` and `niche` tags, matched against the log's `tags` field.
- `dev-human/slop.json` - untouched. Slop words are voice-specific; review them manually from `humanize.py --report`.
- `dev-profile/rubric.json` - flagged only. Rebalancing needs follower-growth data the log does not capture yet.

## Rules

- Never delete a formula, tag, or item. Demote to weight 0 and move to `archive`.
- Dry-run first and show the user the proposal before `--apply`.
- Demotion is relative to this account's own mean, not an absolute threshold.
- After `--apply`, hand off to `/dev-post` so the next draft picks up the new weights.

## Skipped (ponytail)

- No auto-fetch of dev.to analytics (needs an API key and setup); `/dev-audit` supplies the numbers.
- No new learning file format - reuses the JSON files `/dev-post` already reads.
