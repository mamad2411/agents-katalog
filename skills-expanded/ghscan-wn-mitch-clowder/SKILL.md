---
id: 521
title: Practice-play — solo kitten skill rehearsal (motor-pattern play with no partner, builds hunting skill)
status: ready
cluster: life-cycle
initiative: [generational-continuity, world-richness]
orchestration: substrate-sensitive
added: 2026-07-09
parked: null
blocked-by: []
supersedes: []
related-systems: []
related-balance: []
landed-at: null
landed-on: null
---

## Why

The play continuity canary ("play fires ≥1×") is carried today by the joint /
dyadic play substrate (tickets 127 / 276 / 277) — a play-bout needs a *partner*.
That makes the canary fragile to demographic thin-out: a colony with one kitten,
or kittens whose ages don't overlap a play window, can silence play through no
fault of the scoring. Ethologically the real thing is that a lone kitten plays
anyway — pounces at a leaf, stalks its own shadow, ambushes a wind-blown seed —
and that solo motor-pattern play *is* how predation skill is learned. Adding a
solo play affordance makes the play canary robust to pairing failure AND wires a
generational hook (skill acquisition through play), broadening §5 sideways
(play) at the isolated-leisure-action end where it's currently absent.

## Scope

- A solo `PracticePlay` affordance: a low-need kitten (and optionally a low-need
  adult) can elect solo motor-pattern play against an ambient target-of-
  opportunity (a leaf, a shadow, a mote — no partner, no creature required),
  scoring on the **existing** play/mood axis. No new need, no new scoring
  channel.
- A skill-xp side-write: a solo play bout grants a small increment to the
  kitten's hunting/stalking skill, so play reads as learning rather than pure
  idle. Uses the existing skill/xp substrate; no new progression system.
- Narrative templates so the prose surfaces it (`assets/narrative/play.ron` or a
  new solo-play context).

## Out of scope

- Any change to the joint/dyadic play substrate (127 / 276 / 277) — this is an
  additive sibling, not a replacement.
- A new need or scoring channel — reuse the play/mood axis only.
- A general skill-tree or leveling rework — the xp side-write is a small
  increment on the existing skill substrate, nothing more.

## Current state

New. Not started. Provenance: surfaced by the `ideonomy` skill (2026-07-09
tuple `dimension-identification + cross-domain-reinstantiation / chart /
animacy·autonomy·age`) as the empty Self×Informational cell of the §5
autonomy×target chart — the ETHOLOGY re-instantiation of "play is motor-pattern
rehearsal" — then priced with `rank-sim-idea`.

Rank-sim-idea triage (2026-07-09), anchored to shadowfox = 150:

| V | F | R | C | H | Score | Bucket    |
|---|---|---|---|---|-------|-----------|
| 4 | 4 | 4 | 4 | 4 | 1024  | cheap win |

- V=4: hardens the play canary against pairing failure AND feeds skill
  acquisition (generational) — two hooks.
- F=4: kitten play IS predation-motor learning; honest-ecology fit, no director.
- R=4: isolated new leisure DSE scoring on an existing mood axis with a skill-xp
  side-write; no feedback into survival scoring; observable.
- C=4: one DSE + one skill hook, ≲300–400 LOC, one file, no coordination.
- H=4: isolated axis, no scoring feedback loop, play canary already exists (no
  bespoke canary). (H-source: structural tells — none of the five H=1–2 tells
  fire; the isolated-new-axis case.)

## Approach

Add a `PracticePlay` DSE/consideration keyed to a low-play-need kitten with an
ambient target-of-opportunity in range (reuse whatever proximity primitive the
existing play or forage affordance uses — do NOT introduce a creature dependency
like 519's hatch; the target can be a purely notional ambient anchor). Score on
the existing play/mood axis so the play canary counts it. On bout completion,
side-write a small hunting/stalking skill increment through the existing skill
substrate. All tunables (solo-play attraction weight, bout duration, skill
increment) land in `src/resources/sim_constants.rs` — no inline magic numbers.
Substrate-sensitive because it adds a DSE to the L2 catalog; register it through
`score_actions` dispatch (a missing `score_dse_by_id` branch = inert DSE — see
the score_actions dispatch antipattern).

## Verification

- Deterministic scenario: a single-kitten colony (no play partner available)
  advances on a fixed seed; assert ≥1 solo `PracticePlay` bout fires and the
  play canary is satisfied without any dyadic play.
- Focal-cat trace: the kitten's L2 shows `PracticePlay` eligible and winning at
  least once; the skill increment appears after the bout.
- `just verdict` on a full soak: play canary ≥1; hard survival gates unchanged
  (this touches no survival axis); no new balance canary required — if one is,
  H was mis-scored (re-triage).

## Log
- 2026-07-09: opened from an `ideonomy` → `rank-sim-idea` generate-then-price
  pass over the §5 sideways-broadening axes. Scored 1024 (cheap win) — the one
  clear pick-up-next of the pass. Sibling tickets 522 (ectoparasite load), 523
  (the heap), 524 (colony naming rite) came from the same chart's empty cells.
