---
name: game-balance-designer
description: Game economy and progression tuning specialist. Auto-invoked when progression curves, difficulty scaling, economy balance, loot tables, matchmaking MMR, or live-ops tuning is being designed or adjusted.
---

# Game Balance Design

Balance makes the numbers feel right — and balance failures are public: an economy
exploit or a broken curve is discovered by players within hours of ship.

## When to reach for this

- Designing or tuning progression curves, XP tables, or difficulty scaling
- Building an economy: currencies, sinks, sources, loot tables, pity systems
- Setting matchmaking MMR, rank decay, or placement parameters
- A live-ops tuning change needs a model and a telemetry plan before ship

## Principles

1. **Model before you ship.** Build a spreadsheet or Monte Carlo sim that predicts
   the average *and* the 95th-percentile outcome — the unlucky player at p95 is the
   one who churns or posts about it.
2. **Tune with config, not code.** Every balance knob lives in remote-config or data
   files so a live patch never requires a client update or store review.
3. **Design the sink before the source.** Every currency has an inflation path;
   model net flow per player-day and per cohort before adding any new source.
4. **Respect the grind curve.** Hours-to-next-milestone is the most-felt number in
   the game — chart it across the whole progression, not just the first ten levels.
5. **Find the exploit before players do.** Adversarially playtest the economy: max
   one axis (time, money, trading, a single repeatable action) and see what breaks.
6. **Pity systems bound variance.** Any low-probability reward (roughly < 2% drop
   rate) needs a hard or soft pity ceiling, or p95 players experience it as never.

## Balance change worksheet

For any tuning change, produce these five artifacts before it ships:

| Artifact | Contents |
|---|---|
| Model / sim | numeric model with assumptions stated; mean and p95 outcomes |
| Proposed values | exact tunables in the game's config format, with old → new |
| Grind delta | hours-to-milestone before vs. after, per affected segment |
| Exploit surface | what combinations this opens or closes; the maxed-axis test result |
| Telemetry plan | the specific metric (and cohort cut) that confirms or refutes the change post-launch |

## Pitfalls

- Tuning from aggregate averages — segment by cohort and spender tier, or the
  whales mask the curve everyone else feels
- A new currency source with no matching sink — inflation shows up weeks later
  and is far harder to remove than to prevent
- Drop rates stated without variance — "1% drop" without pity means 1 in 20
  players hasn't seen it after 300 attempts
- Difficulty tuned on developer skill — devs are p99 players of their own game
- Hardcoded balance values that turn a number tweak into a client release
- Shipping a tuning change with no pre-registered success metric, so the
  post-hoc telemetry read becomes a Rorschach test

---
*Related: `game-liveops` (validating tuning with live telemetry), `game-netcode`
(matchmaking/session lifecycle) · domain agent: `game-architect` (core loop the
economy hangs off) · output/ADR format: `playbook-conventions`*
