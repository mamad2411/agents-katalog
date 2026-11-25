# Fixture: apply-pack-adaptation (abridged)

Decision-log owner. Reads `.claude/_phase-4-6-decisions.md`, writes `.claude/_phase-4-8-decisions.md`.

## Round-one action tokens
CHANGE-anchor / CHANGE-anchor-with-warn / LEAVE-with-redirect / LEAVE-delete.
`[EXTRACTION-WEAK]` = no signal for the topic -> thin anchor, track falls back to COPY mode.

## Sampled-source downgrade
When the source section carries `[SAMPLED: <seen>/<present> <unit>]`, the anchor is written at
full length and every line that generalizes beyond the sample is downgraded to
`[inferred: <basis>; sampled <seen>/<present> <unit>]` -- never `[found:]`. Phase 4 generators
may not anchor to `[inferred:]` without re-verifying against source, so the qualification has
teeth. `SAMPLED-sourced anchors: <M>` is reported in the round-one summary.

## DEEP tokens
ANCHOR-DEEP, NEW-FILE, LEAVE-DEEP, LEAVE-DEEP-IDEMPOTENT, ROLLBACK-MARKER-DRIFT,
MARKERS-INJECTED, RE-TRANSLATED, INDEX-REFRESHED, NO-OP, SKIPPED-NO-CHANGES.

## Phase 4.8-DEEP decision table
| Adapter | Output file | Action | Triggered by | Notes |
|---|---|---|---|---|

## Phase 5.3 audit helpers
`lookup_phase_4_6_decision`, `DECISIONS_FILE`, `EXTRACTION_FILE`, `IDIOMS_FILE`.

## Halt tokens
`MISSING_PHASE_4_6_DECISIONS_FILE`.
