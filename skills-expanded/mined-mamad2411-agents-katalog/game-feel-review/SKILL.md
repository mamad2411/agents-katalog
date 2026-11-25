---
name: game-feel-review
description: Review gameplay for responsiveness and tactile quality — input buffering, coyote time, hitstop, camera behaviour, animation cancel windows, and audiovisual feedback. Use when the user says a mechanic feels floaty, mushy, stiff, unresponsive, or "off"; when implementing movement, jumping, or combat; or when they ask why a system that is technically correct still isn't fun.
category: design
---

# Game Feel Review

"It works but it feels bad" is a real, diagnosable bug class. The code is correct and the game is unpleasant. Almost always the cause is on this list, and almost always the fix is small.

## The forgiveness layer

Players are imprecise, and games that punish that imprecision read as unresponsive rather than as difficult. Every one of these is a few lines:

**Input buffering** — a jump pressed slightly before landing should fire on landing, not be dropped. Store the press with a timestamp and consume it if it is within ~100–150ms.

**Coyote time** — allow jumping for a short window after walking off a ledge. Around 100ms. Players almost never notice it exists; they very much notice its absence.

**Corner correction** — nudge the player around a ledge corner they clipped by a pixel rather than stopping them dead. This is the difference between "tight" and "sticky".

**Sticky targeting** — a small snap toward the obvious target beats demanding pixel-accurate aim.

If a movement system has none of these, add them before tuning any numbers. They will change how every other value feels.

## Impact

Hits that connect need to register in more than the health bar:

- **Hitstop** — freeze both parties for 3–8 frames on a heavy hit. The single highest-impact-per-line change in most combat systems.
- **Screenshake** — small, short, and decaying. Over-shake reads as noise and makes players motion-sick. Give it a global multiplier players can lower.
- **Knockback and hitflash** — the target should visibly react. A white flash for 2–3 frames is cheap and enormously effective.
- **Layered audio** — one impact sound is flat; an attack whoosh plus a connect thud plus a material-specific layer is meaty.

## Response curves

Instant acceleration feels robotic; slow acceleration feels floaty. Almost every good-feeling character has asymmetric values:

- Acceleration faster than deceleration, or the reverse depending on genre
- Higher gravity on descent than ascent, so jumps feel snappy rather than mushy
- Variable jump height — release early, rise less

Tune these as exported values in a `.tres` so they can be iterated without a code change. Feel is found by playing, not by reasoning, and anything requiring a recompile per tweak will not get tuned enough.

## Camera

Camera problems get misdiagnosed as character problems constantly. Check:

- Does it lead the direction of movement rather than trailing?
- Is there a dead zone, so small movements don't jitter the whole screen?
- Does it smooth-follow rather than hard-lock?
- Does it pull back at speed to give the player time to react to what's ahead?

## Animation and commitment

- **Cancel windows** — can the player interrupt a recovery, and when? Too rigid feels unfair; too loose removes weight from committing.
- **Anticipation frames** — a wind-up before an attack lands makes it readable and telegraphed.
- **Animation must not gate logic.** The hitbox is driven by state, not by the animation player. Coupling them makes both harder to tune.

## How to run the review

Ask what specifically feels wrong, then map the complaint:

| Complaint | Usually |
|---|---|
| "Floaty" | Gravity too low, or no fall-gravity multiplier |
| "Unresponsive" | No input buffer, or animation gating input |
| "Weightless hits" | No hitstop, no hitflash, thin audio |
| "Sticky" / "clunky" | No corner correction, over-tuned deceleration |
| "Hard in a bad way" | No coyote time, no forgiveness layer at all |

Change one variable at a time and have the user play it. Feel is empirical — a plausible argument about why a value should work is worth less than ten seconds of playing it.
