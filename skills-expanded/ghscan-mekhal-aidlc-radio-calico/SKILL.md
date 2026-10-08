# Decision: Issue #294 closed at Instruction Fidelity 5 / Result Satisfaction 5; theme-token background/text audit captured as a new skill

**Issue:** [#294](https://github.com/mekhal/aidlc-radio-calico/issues/294)
**PR:** [#296](https://github.com/mekhal/aidlc-radio-calico/pull/296) (Test PR, merged), [#297](https://github.com/mekhal/aidlc-radio-calico/pull/297) (Code PR, merged)
**Decided by:** @mekhal, 2026-08-08

## Decision

1. **Scores given directly at close:** Instruction Fidelity 5, Result Satisfaction 5 ("Coding 5 satisfied 5"). Recorded as-is per `CLAUDE.md`'s rule that the agent never self-scores.
2. **New skill captured:** `theme-token-background-audit` — the human's close instruction ("เก็บ knowledge เรื่องการใช้ style ไว้", i.e. "keep/save the knowledge about using style") is read as approval to record the root-cause pattern behind this issue's fix (a shared color token reused as a solid *background* against a separately-themed text color needs its own dark-theme override, or the pairing should be swapped for a token pair that already flips) as a reusable skill, written directly to `docs/knowledge-asset/published/theme-token-background-audit.md` — this folder is already treated as live/approved guidance per `CLAUDE.md`'s "Using a skill" section, not a draft awaiting a further copy step into `.claude/skills/`.

## Why

Decision 1 follows the same "never grade its own homework" principle already established in the `ai-review-evals` framework — the human's literal scores are recorded verbatim rather than the agent inferring or rounding them.

Decision 2 turns a one-off bugfix (dark-theme contrast on the Test Report Dashboard) into a durable rule the agent can apply the next time any page introduces a background/text token pairing, instead of leaving the lesson only in this issue's closed thread. The human's own close-comment wording asked for exactly this ("save the knowledge about style usage"), so it is recorded directly rather than re-litigated as a separate add/skip question.

## Impact

- Issue #294 closes with both AC1–AC4 shipped (#296/#297, already merged to `develop` and released to `main` via #298) and its scores recorded verbatim.
- `docs/knowledge-asset/published/theme-token-background-audit.md` is available for the agent to apply on any future ticket that adds or edits a CSS rule pairing a shared color token background with a separately-themed text color.
