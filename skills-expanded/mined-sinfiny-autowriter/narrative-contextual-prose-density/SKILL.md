---
name: narrative-contextual-prose-density
description: "Use when drafting or revising fiction where prose density must change with scene function: atmospheric depiction, character or setting establishment, action mechanics, plot causality, fight scenes, explanations of how something works, web novel pacing, fan fiction scenes, or autonomous story-generation loops that need to avoid one uniform house style. Based on Judy Fan's cognitive science work on goal-sensitive visual abstraction, depiction, and mechanistic explanation."
---

# Narrative Contextual Prose Density

Use this skill to decide how much detail a scene deserves before drafting. The core move is goal-sensitive abstraction: prose should spend detail on what the reader needs to identify, understand, or track.

## Source Protocol

- Read `references/source-notes.md` when the user asks for source grounding, skill tuning, or a cognitive-science rationale.
- Use Judy Fan's work as a craft lens, not as prose style imitation.
- Do not quote long transcript passages.

## Operating Loop

Before drafting, classify the passage:

```xml
<density_map>
Scene_Mode: depiction | explanation | hybrid
Reader_Task:
Primary_Object:
Identity_Details:
Causal_Parts:
Background_Details:
Symbolic_Arrows:
Withheld_Details:
</density_map>
```

Definitions:

- `depiction`: the reader must recognize a person, place, object, faction, atmosphere, social status, or emotional environment.
- `explanation`: the reader must understand cause and effect: how a plan, fight, betrayal, mechanism, rule, spell, deduction, or relationship turn works.
- `hybrid`: both are needed, but one mode must be primary. Do not give both unlimited budget.

## Depiction Mode

Spend prose on identity and recognizability.

- Use sensory grounding, diagnostic appearance, atmosphere, status markers, and context.
- Include background details when they help the reader distinguish this person, place, object, or mood from nearby alternatives.
- Let non-causal details carry character, theme, or social world texture.
- Slow the pace enough for the reader to form a stable mental image.

Good use cases:

- First entrance of a major character.
- A new city, school, dungeon, court, spaceship, sect, or fandom setting.
- A quiet emotional beat where atmosphere is the point.
- A reveal where identity matters more than mechanics.

Avoid:

- Explaining the entire lore archive.
- Decorating a scene after the reader already knows what matters.
- Mistaking pretty detail for useful recognition.

## Explanation Mode

Spend prose on causal moving parts.

- Emphasize actions, immediate reactions, decision points, constraints, critical dialogue, and consequences.
- Treat objects, gestures, and lines of dialogue like arrows in a diagram: each should point to a change.
- Strip background unless it changes what a character can do, notice, misunderstand, or lose.
- Use shorter paragraphs and cleaner causal sequencing when stakes are high.

Good use cases:

- Fights, chases, rescues, heists, negotiations, investigations, confessions with consequences, magic/system use, and plot turns.
- Any scene where the reader must understand "because this happened, that became possible."

Avoid:

- Pausing a moving beat for scenic inventory.
- Naming causal parts without showing their effect.
- Explaining emotion that the character's choice already proves.

## Hybrid Switching

When a scene needs both modes:

1. Use depiction only until the reader can recognize the active space or character.
2. Switch to explanation once cause and effect starts moving.
3. Return briefly to depiction only if the final image changes the reader's understanding of identity, status, or mood.

The common web-novel pattern is:

```text
depict the arena -> explain the exchange -> depict the aftermath image
```

## Self Check

After drafting or revising, run:

```xml
<density_check>
Mode honored:
Reader task satisfied:
Causal parts clear:
Identity details sufficient:
Background overused:
Important detail missing:
Revision needed:
</density_check>
```

If `Background overused` or `Important detail missing` is yes, revise before returning the passage.

## Guardrails

- Do not flatten every scene into minimum viable prose; some scenes need faithful depiction.
- Do not inflate every important scene; high importance often requires more causal clarity, not more ornament.
- Preserve the user's genre pleasures. A cultivation breakthrough, magical girl transformation, courtroom trap, or romance confession may need stylized depiction before the causal turn.
- Make the prose density serve the scene's job.
