---
name: narrative-epistemic-targeting
description: "Use when planning, drafting, or revising fiction to prevent lore dumps and control what the reader learns now: chapter openings, reveals, mystery clues, worldbuilding, exposition, progression mechanics, fan fiction context, autonomous story generation, and AI writing IDE reasoning loops. Defines a single Epistemic_Goal and filters entities, backstory, lore, and scene evidence through the reader's current mental-model update. Based on Judy Fan's audience-sensitive data visualization work."
---

# Narrative Epistemic Targeting

Use this skill to choose the right story evidence for the reader's current question. The core rule: a scene should update the reader's mental model on purpose.

## Source Protocol

- Read `references/source-notes.md` when the user asks for source grounding or wants the cognitive-science analogy.
- Use Judy Fan's audience-sensitive visualization work as craft guidance: choose the representation that helps this audience answer this question.
- Do not quote long transcript passages.

## Operating Loop

Start every planning or drafting pass with:

```xml
<epistemic_target>
Reader_Current_Model:
Epistemic_Goal:
Target_Update:
Required_Evidence:
Allowed_New_Info:
Withheld_Info:
Misread_Risk:
</epistemic_target>
```

Field meanings:

- `Reader_Current_Model`: what the reader likely believes before the passage.
- `Epistemic_Goal`: the single question this passage should help answer.
- `Target_Update`: how the reader's belief should change by the end.
- `Required_Evidence`: concrete scene evidence needed for that update.
- `Allowed_New_Info`: new entities, lore, backstory, or mechanics that directly serve the goal.
- `Withheld_Info`: interesting material that belongs later.
- `Misread_Risk`: the most likely wrong inference and how to prevent it.

## Filtering Rules

Include a detail only if it does at least one of these:

- Changes danger, cost, status, relationship pressure, available choices, or reader suspicion.
- Lets the reader infer the target insight without being told.
- Prevents a likely misread that would damage the current scene.
- Pays off a prior promise or plants a necessary future one.

Withhold a detail if it is merely:

- Cool lore.
- Authorial explanation.
- Backstory without present pressure.
- A faction, technique, artifact, system rule, or family history that does not affect this scene's target update.
- A reveal that answers a later question too early.

## Representation Choice

Choose the passage form that best serves the `Epistemic_Goal`:

- `direct scene`: readers need to witness a choice, conflict, clue, or irreversible turn.
- `compressed summary`: readers need continuity but not dramatized discovery.
- `dialogue`: readers need conflicting knowledge states or social pressure.
- `object/image`: readers need to infer history or emotion through evidence.
- `flashback`: readers need a past cause that changes the present decision now.
- `exposition`: readers need a rule to understand immediate stakes; keep it short and consequence-bearing.

## Autonomous Writing Loop

For agentic generation:

1. Define one `Epistemic_Goal`.
2. Select only the active story graph nodes needed for that goal.
3. Draft the smallest passage that causes the target update.
4. Check whether any introduced lore creates new unanswered questions.
5. Defer any new question that does not sharpen the current conflict.

## Self Check

```xml
<epistemic_check>
Single goal:
Reader update visible:
Required evidence present:
Unneeded lore removed:
Misread risk handled:
Future tension preserved:
Revision needed:
</epistemic_check>
```

If `Single goal` is no, split the passage or choose the highest-leverage update. If `Unneeded lore removed` is no, cut or defer the material.

## Guardrails

- Do not starve the reader of orientation. Mystery is not the same as confusion.
- Do not answer every question the context window can answer.
- Do not introduce names, systems, or histories because they exist in canon; introduce them when the reader's current inference needs them.
- Fan fiction may rely on shared canon knowledge, but still define what this passage teaches, reframes, or withholds.
