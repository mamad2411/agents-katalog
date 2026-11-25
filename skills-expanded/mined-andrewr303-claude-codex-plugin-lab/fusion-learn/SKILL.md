---
name: fusion-learn
description: >-
  Inspect and curate what Fusion has learned: provider reliability, who-wins-by-task-type,
  best mode per task type, and the distilled lessons the Conductor reads before routing.
  Use to review the ledger, regenerate lessons.md, record outcome feedback, or prune a
  bad provider. Triggers: "what has fusion learned", "fusion stats", "fusion leaderboard",
  "update lessons", "which model wins".
---

# Fusion — Learn

Surface and steward Fusion's memory. The live store is `~/.fusion/memory/` (`runs.jsonl`,
`lessons.md`; the plugin ships a seed in its own `memory/`, copied in on first use) — plain
files, inspectable and diffable. Read the live digest with `fusion.sh ledger show-lessons`.

## Read what's there
```
fusion.sh ledger stats                 # runs recorded, reliability+fairness rank, mode usage
fusion.sh ledger leaderboard           # who wins overall
fusion.sh ledger leaderboard <task>    # who wins on a task type
fusion.sh ledger winners <task>        # which mode works best for a task type
fusion.sh ledger score <provider>      # Bayesian reliability [0..1]
```
Then explain it in plain language: which panelist is pulling its weight, where a model
family is consistently strongest, whether any mode is over/under-used.

## Curate
- **Regenerate the digest:** `fusion.sh ledger lessons` rewrites the live `lessons.md` (in `~/.fusion/memory`) from
  the run history (preserving the hand-written priors below the `<!-- FUSION:PRIORS -->`
  divider). Do this after a batch of runs or when a durable pattern emerges.
- **Record outcome feedback:** when the user reports a Fusion answer shipped / was wrong,
  reflect it — the run record's `outcome` field is the ground-truth signal that beats the
  judge's own ranking. Add a fresh record or note the correction.
- **Prune / restore a provider:** if a panelist is reliably degraded or wrong on a task
  family, `fusion.sh ledger mark-degraded <prov>` (this session) or add it to the
  allowlist; `clear-degraded` to restore. The 5% fairness floor still resamples it, so a
  one-off slump won't permanently bench a model.
- **Add a hand-written prior:** if you learn something the data hasn't captured yet, append
  it under the `<!-- FUSION:PRIORS -->` divider in `lessons.md` — it survives regeneration.

## The point
This is the compounding loop. Reliability tells Fusion *who to trust*; the leaderboard tells
it *who wins what*; lessons turn both into routing it actually uses next time. Keep the
ranks honest — inflated history poisons the very signal that makes the next run smarter.
