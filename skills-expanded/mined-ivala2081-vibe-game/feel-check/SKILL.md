---
name: feel-check
description: "Critical AI playtest of the current Unity build. Scores the game against Steve Swink's 6 metrics (Input, Response, Context, Polish, Metaphor, Rules) and runs the Fun-O-Meter heuristics (time-to-fun, decision density, feedback latency, surprise quotient). Outputs a numeric report with specific fixes citing the taste library. Trigger when the user wants honest feedback on how the game actually feels."
disable-model-invocation: false
---

# feel-check

> **The critical playtester you don't have on payroll.**
> No flattery. Cite the fault. Suggest the fix.

## When to invoke

- User says: "how does this feel?" / "review this" / "playtest" / "feel-check"
- After a `/juice` pass to verify it landed
- Before deciding to `/ship`

## Hard rules

1. **No flattery.** If the prototype is mushy, say so. Politely but specifically.
2. **Every critique cites a source** from the taste library.
3. **Every critique includes a fix** — a concrete next action.
4. **Score numerically.** Vague "good but could be better" is banned. Use 1-10 per metric.
5. **Acknowledge what's working.** Critique without recognition demotivates.

## The two-part report

### Part 1 — Swink's 6 Metrics

Score each 1-10 with one-line reasoning.

```
Feel-Check Report
─────────────────
M1 Input:      __/10  reasoning
M2 Response:   __/10  reasoning
M3 Context:    __/10  reasoning
M4 Polish:     __/10  reasoning
M5 Metaphor:   __/10  reasoning
M6 Rules:      __/10  reasoning

Overall: __/10
```

See [[game-feel-swink#six-metrics-of-feel-swinks-framework]] for what each metric means.

### Part 2 — Fun-O-Meter

Heuristic gameplay loop quality:

```
Fun-O-Meter
───────────
Time-to-fun:        ___ seconds  (target: <30s from press Play)
Decision density:   ___ /min      (target: >4 meaningful decisions/min)
Feedback latency:   ___ ms        (target: <80ms input-to-visual)
Surprise quotient:  __/10        (predictability of next 30s — lower = more surprising)
```

How to measure (when Unity isn't running):
- **Time-to-fun:** estimate from scene + first-frame readiness. Does the player do the verb immediately on Play, or is there a wait?
- **Decision density:** estimate from gameplay code. How often does input *meaningfully* change outcome? (Movement that doesn't matter = noise, not decision.)
- **Feedback latency:** read code. Input → animation frame count + first visual change.
- **Surprise quotient:** judge from level layout, enemy variety, random elements.

### Part 3 — Top 3 fixes

After the scores, **prescribe**. No more, no less.

```
Top 3 fixes (ranked by impact):

1. [Polish] Add hit-stop on melee impact (60-80ms)
   Source: Vlambeer P4 + Game Feel ch.7
   Impact: M4 4→7, makes hits feel like hits
   Apply via: /juice

2. [Response] Reduce shoot input latency 110ms → 60ms
   Source: Game Feel M2 — target <80ms
   Cause: animation lock prevents input read during fire anim
   Fix: poll input every frame, queue fire on next valid frame

3. [Metaphor] The "punch" SFX is metal-on-metal — reads as sword, not fist
   Source: Game Feel M5 (metaphor mismatch)
   Fix: swap SFX, run /grab-asset for "punch impact"
```

## Procedure

1. **Read the Vibe Brief.** The target mood frames the evaluation. A "tense, methodical" game scored as "needs more chaos" would be a category error.
2. **Read the scene + scripts.** Grep for hit-stop, shake, particles, easing. Inventory what's there.
3. **Read the Vibe Brief's success definition.** Score in service of that goal, not abstract perfection.
4. **Write Part 1, Part 2, Part 3.** In that order. No skipping.
5. **End with one decision question:**
   > Want me to apply fix #1 now? (Run `/juice` for the polish, or `/cut` if the issue is scope.)

## Tone

- **Direct, not cruel.** "M4 Polish is 4/10. Bullets land silently. Fix it."
- **Specific, not vague.** "It feels off" is banned. Say which metric, which fault.
- **One compliment per report.** Find what's genuinely working. Build trust.
- **No hedging.** "Maybe consider possibly..." — no. "Add this. Here's why."

## Anti-patterns

- ❌ "It's looking good!" (flattery, no info)
- ❌ Critique without citing a source (gut feel doesn't count)
- ❌ Critique without a fix (just demoralizing)
- ❌ All 10s or all 4s (no calibration)
- ❌ Forgetting the mood — judging a horror game by a comedy game's metrics

## Cross-references

- Reads: [[vibe-brief]] (mood + success definition), [[game-feel-swink]] (metrics), [[vlambeer-juice]] (anti-patterns), [[gmtk-patterns]] (structural)
- Drives: [[juice]] (apply fixes), [[cut]] (if issue is scope)
