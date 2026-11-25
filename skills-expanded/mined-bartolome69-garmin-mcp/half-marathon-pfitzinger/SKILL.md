---
name: half-marathon-pfitzinger
description: Plan, review and adjust half marathon training in the style of Pete Pfitzinger — lactate threshold as the cornerstone, medium-long runs midweek, mesocycle structure, disciplined easy running. Use when the user asks for a half marathon plan or session, wants a threshold workout built, or wants their recent training judged against this approach.
---

# Half marathon training, Pfitzinger style

Pete Pfitzinger's approach (*Faster Road Racing*, *Advanced Marathoning*) is
built on one idea: for races from 15K to the marathon, **lactate threshold is
the single most trainable determinant of performance**. Everything else exists
to support it or to stop it stagnating.

This skill encodes that methodology. It does **not** reproduce his published
week-by-week schedules — those are his copyrighted work, and anyone serious
should buy the book. What follows is the reasoning, applied to this runner's
actual data.

## Before prescribing anything

Pull the evidence first:

- `get_profile` — PBs and VO2 max
- `get_activities` with a 6-8 week window — current volume, the real shape of the week
- `get_activity_details` on recent quality sessions — did they hold pace, did heart rate drift

Then establish three things, asking only for what the data can't tell you:

1. **Current half marathon fitness**, not their PB. A PB from two years ago sets
   no paces today. If there's no recent race, estimate from a recent hard effort
   or a tempo run and say plainly that it's an estimate.
2. **Max heart rate**, and whether it's measured or Garmin's age-based guess.
   Every zone below depends on it; if it's a guess, lead with pace instead.
3. **Weeks until the race**, and whether there are tune-up races planned.

## The paces

Pfitzinger defines effort by percentage of maximum heart rate, cross-checked
against race paces. Use both — pace when it's flat and calm, heart rate when
it's hilly, hot, or the runner is tired.

| Session | % max HR | Pace reference |
| --- | --- | --- |
| Recovery | below 76% | Genuinely slow. Slower than feels dignified. |
| General aerobic | 70-81% | Comfortable, conversational |
| Long / medium-long | 74-84% | Steady, finishing stronger than started |
| **Lactate threshold** | **82-91%** | **15K to half marathon race pace** |
| VO2 max | 93-95% | 3K-5K race pace |

Lactate threshold pace is roughly what the runner could hold for an hour flat
out. For most people that is close to their current 15K pace and slightly
faster than half marathon pace.

## The sessions

**Lactate threshold runs.** The cornerstone. Either continuous or in long
intervals, always after a proper warm-up.

- Continuous: 20-40 minutes at LT pace, progressing over a block. Start where
  the runner is, not at 40 minutes.
- Intervals: 2-4 reps of 10-15 minutes at LT pace with 2-3 minutes jogging.
  Useful early in a block, or for someone who cannot yet hold 30 minutes.

The discipline that matters: LT runs are *controlled*. Running them faster
turns them into a different session and blunts the next one.

**Medium-long runs.** The Pfitzinger signature, and the thing most self-coached
runners miss. A midweek run of 90 minutes to two hours, separate from the
weekend long run. This is where aerobic development comes from at a volume
most people never reach because they only run long once a week.

**Long runs.** Up to roughly 2 hours for a half marathon build. No further —
beyond that the cost outweighs the benefit at this distance. Keep it under
about 30% of weekly volume.

**VO2 max intervals.** 600m to 1600m at 3K-5K pace, 3-5 minutes per rep, with
recovery roughly equal to rep duration. Total volume of the fast running kept
to about 4-8% of weekly mileage. Introduced *late* in a build, not early.

**Recovery runs.** Short and genuinely easy. Their purpose is to let the next
quality session happen. If a recovery run is anywhere near general aerobic
pace, it is doing the opposite of its job.

**Strides.** 8-10 × 100m relaxed accelerations after an easy run, twice a week.
Cheap, and they protect economy while the training is otherwise slow.

## Structuring a block

Pfitzinger organises training into mesocycles, each with a focus, each ending in
a recovery week:

1. **Endurance** — volume, general aerobic and medium-long runs, strides. Little
   or no threshold work yet.
2. **Lactate threshold + endurance** — the heart of the block. Threshold work
   every 7-10 days while volume holds.
3. **Race preparation** — VO2 max intervals appear, tune-up races, threshold
   work maintained, volume eases slightly.
4. **Taper** — volume drops sharply, intensity is retained at reduced volume.
   Two to three weeks for a half marathon.

Volume rises about 10% a week, with every third or fourth week cut by 20-25%.
Hard days need two easy days after them, not one — a week with three quality
sessions in it is not a Pfitzinger week.

## Building the sessions on the watch

Use `create_workout`, show the structure, wait for confirmation, then
`schedule_workout`. Pace targets as a range, since the runner is chasing a zone
rather than a number.

A 30-minute continuous threshold run for someone with 3:55/km LT pace:

```json
[{"type": "warmup", "duration_seconds": 900},
 {"type": "interval", "duration_seconds": 1800, "pace": ["3:52", "3:58"]},
 {"type": "cooldown", "duration_seconds": 600}]
```

Threshold intervals, 3 × 12 minutes:

```json
[{"type": "warmup", "duration_seconds": 900},
 {"type": "repeat", "times": 3, "steps": [
     {"type": "interval", "duration_seconds": 720, "pace": ["3:52", "3:58"]},
     {"type": "recovery", "duration_seconds": 150}]},
 {"type": "cooldown", "duration_seconds": 600}]
```

VO2 max session, 5 × 1000m at 5K pace:

```json
[{"type": "warmup", "duration_seconds": 1200},
 {"type": "repeat", "times": 5, "steps": [
     {"type": "interval", "distance_meters": 1000, "pace": ["3:28", "3:34"]},
     {"type": "recovery", "duration_seconds": 180}]},
 {"type": "cooldown", "duration_seconds": 600}]
```

## What to flag when reviewing someone's training

Pfitzinger's criticisms of typical self-coached training, in order of how often
they apply:

- **Easy days too hard.** The most common fault. If recovery and general
  aerobic runs sit at the same pace and heart rate, there are no easy days.
- **No medium-long run.** One long run a week and everything else 45 minutes
  is the classic plateau shape.
- **Threshold work missing or mislabelled.** "Tempo" run at 5K effort is a
  VO2 max session in disguise, and recovers like one.
- **Everything in one narrow band.** Check the spread of paces and heart rates
  across a month. A tight cluster means the training is one stimulus repeated.
- **No recovery weeks.** Volume that only ever rises is volume that ends in
  injury or stagnation.
- **VO2 max work too early.** It sharpens something that isn't built yet.

Say which of these the data actually shows. If three weeks isn't enough to call
a pattern, say so rather than producing a diagnosis.

## Limits

This is a training methodology, not medical advice. Pain that changes gait,
persistent elevated resting heart rate, or anything that sounds like an injury
is a conversation for a physio, not a plan adjustment. Say so and stop.
