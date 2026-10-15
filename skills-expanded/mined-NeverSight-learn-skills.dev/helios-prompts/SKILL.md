---
name: helios-prompts
description: Write effective prompt sequences for Reactor's Helios model, a real-time video frame generation API. Use when creating Helios prompts, video generation prompts, or when the user mentions Helios or Reactor. Covers start prompts, follow-ups, sequence planning, camera anchoring, lighting consistency, and progressive state tracking.
---

# Helios Prompt Writing

Helios generates video sequences through multi-prompt continuation. Each prompt builds on the previous frame state with controlled variations while maintaining visual coherence.

## Start Prompt Structure

Every start prompt follows this exact order:

```
[SUBJECT ESTABLISHMENT]    2-3 sentences. Specific physical details, clothing, posture, name.
[ENVIRONMENT DESCRIPTION]  2-3 sentences. Setting, props, background elements. Concrete details.
[LIGHTING CONDITIONS]      1 sentence. Source + quality. This becomes the "lighting anchor."
[ATMOSPHERE/MOOD]          1 sentence. Emotional tone.
[STYLE (optional)]         1 sentence. Only if non-default (VHS, anime, vintage).
[CAMERA INSTRUCTION]       1 sentence. Shot type + angle + focus. IDENTICAL in every prompt.
```

**Subject**: Not "a lion" but "a majestic lion named Leo." Include name, posture, clothing, key features.

**Environment**: Not "a table" but "a wooden dining table." Include specific props and background.

**Lighting anchor**: Be specific — "warm afternoon sunlight streaming through linen curtains," not just "daylight." This exact description repeats in every follow-up.

**Camera instruction**: This line is copied VERBATIM to every prompt in the sequence. Lock shot type, angle, and focus.

## Follow-Up Prompt Structure

Each follow-up = **Base State + ONE New Action**.

```
[SUBJECT REESTABLISHMENT]       1-2 sentences. Abbreviated restate of position/details.
[NEW ACTION]                    1-2 sentences. Temporal connector + single action.
[ENVIRONMENTAL INTERACTION]     1-2 sentences. How environment reacts (steam, smoke, reflections).
[LIGHTING ANCHOR]               1 sentence. Copied from start, minor wording variations OK.
[ATMOSPHERE (if changed)]       1 sentence. Only if mood shifted.
[CAMERA INSTRUCTION]            IDENTICAL to start prompt. Not one word different.
```

**Reestablishment pattern**: "The [subject] remains/sits/stands [location], [key visuals]. [Clothing reminder]."

**Temporal connectors**: "Suddenly...", "Now...", "As [subject]...", "[Subject] suddenly..."

**Action categories** (pick ONE per prompt):

- Micro-gestures: reaching, turning head, leaning, raising hand
- Object interaction: picking up, setting down, holding
- Facial expression: smiling, eyes widening, mouth opening
- Environmental trigger: breeze starting, something appearing

**Environmental reactions** — always describe how the world responds:

- Objects affected by movement
- Light interacting with surfaces
- Particles (steam, smoke, petals, sparks)
- Reflections changing

## Progressive State Tracking

Track cumulative changes across prompts. Objects and subjects evolve:

- Candles: lit → flickering → extinguished → smoking → smoke dissipated
- Flower: closed bud → separating → half-open → fully bloomed
- Party hat: slightly tilted → crooked → slipped to one side
- Petals: scattered → swirling → covering blanket → landing on face

Each follow-up must reflect the accumulated state from all previous prompts.

## Sequence Planning

**Optimal length: 4-5 prompts.**

| Prompt       | Role                  |
| ------------ | --------------------- |
| 0 (Start)    | Establish scene       |
| 1-2          | Build action          |
| 3            | Climax / payoff       |
| 4 (optional) | Resolution / settling |

Avoid: >6 prompts (coherence degrades), single follow-ups (no arc), unnecessary intermediate steps.

### Common Patterns

Choose one to structure the sequence. See [references/patterns.md](references/patterns.md) for detailed examples.

1. **Environmental Interaction** — Subject experiences active environment (rain, wind, petals, fireworks). Calm → activate → interact → peak → settle.
2. **Object Reveal/Transformation** — Something hidden is revealed or changes state. Initial → transition → reveal → reaction → enjoyment.
3. **Escalating Intensity** — Single element increases in quantity/power. Calm → first → multiple → peak → sustained.
4. **Character Action Sequence** — Subject performs related micro-actions. Rest → prepare → act → result → settle.

## Critical Rules

**DO:**

- Keep lighting consistent (only minor wording variations)
- Reestablish subject (abbreviated) in every follow-up
- Introduce exactly ONE new action per follow-up
- Describe environmental reactions (steam, smoke, reflections, particles)
- Use specific object descriptions ("a plastic cake server with a bright green handle")
- Copy camera instruction verbatim to every prompt
- Use temporal connectors to signal changes
- Track progressive state changes across prompts
- Introduce objects with action verbs (picks up, pulls out, grabs)

**DON'T:**

- Change lighting dramatically (no dawn → noon transitions)
- Stack multiple new actions in one prompt
- Modify the camera instruction between prompts
- Let subjects interact with dangerous elements in motion
- Introduce objects without describing how they appear
- Skip environmental reaction descriptions

## Checklist

Before finalizing any sequence, verify:

- [ ] Start prompt has: subject, environment, lighting, mood, camera
- [ ] Camera instruction identical in every prompt
- [ ] Lighting consistent (minor wording variations only)
- [ ] Each follow-up has exactly ONE new action
- [ ] Subject reestablished (abbreviated) in each follow-up
- [ ] Environmental reactions described
- [ ] Progressive state changes tracked
- [ ] Objects introduced with action verbs
- [ ] No dramatic lighting shifts
- [ ] Temporal connectors used
- [ ] Sequence is 4-5 prompts
- [ ] Final prompt provides resolution or peak moment
