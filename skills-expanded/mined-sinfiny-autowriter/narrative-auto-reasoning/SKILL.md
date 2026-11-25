---
name: narrative-auto-reasoning
description: Use as a workflow skill when a fiction task needs multiple narrative control loops combined: explicit reasoning, minimum viable prose, surgical editing, and hook/hold/payoff verification. Coordinates the narrative-explicit-reasoning, narrative-minimum-viable-prose, narrative-surgical-editing, and narrative-hook-hold-payoff skills for AI writing IDE or autonomous agent workflows.
---

# Narrative Auto Reasoning

Use this workflow skill to coordinate the four narrative control skills:

- `$narrative-explicit-reasoning` for assumptions, motivation, lore constraints, contradictions, and twist tradeoffs.
- `$narrative-minimum-viable-prose` for concise drafting, compression, concrete observation, and avoiding lore dumps.
- `$narrative-surgical-editing` for targeted edits with a constrained edit radius.
- `$narrative-hook-hold-payoff` for scene/chapter momentum, escalation, structure, and payoff verification.

## Quick Start

Use this workflow when the task spans more than one control loop, such as:

- Planning and drafting a new scene
- Revising a scene while preserving lore and structure
- Diagnosing why a chapter drifts
- Designing a plot twist and then drafting the beat
- Compressing prose without losing Hook/Hold/Payoff
- Running an autonomous AI writing IDE loop

Before substantial prose work:

- Load `references/craft-map.md` for the combined operating model.
- Load `references/output-contracts.md` when the user needs a structured scene, chapter, twist, edit, or contradiction loop.
- Load `references/source-index.md` when the user asks where the source grounding or principles came from.
- Use `$narrative-contextual-prose-density` when the scene needs a deliberate depiction/explanation detail budget.
- Use `$narrative-subtext-mapping` when dialogue or interaction depends on hidden knowledge, agenda, or emotional state.
- Use `$narrative-epistemic-targeting` when lore, backstory, reveals, or reader discovery must be filtered by a single reader insight.

## Operating Loop

Strict mode is the default unless the user explicitly opts out.

1. Route the task to the needed component skills.
2. Run `$narrative-explicit-reasoning` first when motivation, lore, assumptions, contradiction, or twist logic matters.
3. Run `$narrative-hook-hold-payoff` before scene or chapter drafting to define success criteria.
4. Run `$narrative-minimum-viable-prose` for the drafting or compression pass.
5. Run `$narrative-surgical-editing` when modifying existing prose.
6. Run a final `<self_check>` against the original criteria.
7. If the self-check fails, revise before presenting the result.
8. Stop and ask one precise clarification question if the emotional beat or lore state contradicts known context.

## Routing Table

| User task | Use first | Then use |
|---|---|---|
| "Plan this scene" | `$narrative-explicit-reasoning` | `$narrative-hook-hold-payoff` |
| "Draft this scene" | `$narrative-explicit-reasoning` | `$narrative-hook-hold-payoff`, `$narrative-minimum-viable-prose` |
| "Make this shorter" | `$narrative-minimum-viable-prose` | `$narrative-surgical-editing` if editing existing text |
| "Change this line/beat only" | `$narrative-surgical-editing` | `$narrative-explicit-reasoning` if continuity risk appears |
| "Add a twist" | `$narrative-explicit-reasoning` | `$narrative-hook-hold-payoff` |
| "Fix a drifting chapter" | `$narrative-hook-hold-payoff` | `$narrative-minimum-viable-prose` |
| "Continue from here" | `$narrative-explicit-reasoning` | `$narrative-hook-hold-payoff`, `$narrative-minimum-viable-prose` |

## Required Reasoning Block

Before drafting fiction, use this compact shape:

```xml
<reasoning>
Task:
Scene or edit target:
Character emotional goal:
Character outward goal:
Known lore constraints:
Genre/tone constraints:
Narrative tradeoffs:
Chosen approach:
Stop conditions:
</reasoning>
```

Rules:

- State assumptions explicitly.
- Do not invent hidden motivations when the user has already supplied canon.
- If a contradiction appears, stop instead of smoothing it over.
- If a major plot twist is requested, give 2-3 interpretations and choose one with rationale.
- Keep the rationale short enough to help the user steer the story.

## Minimum Viable Prose

For drafting and compression, defer to `$narrative-minimum-viable-prose`.

Default workflow rule:

- Draft only the prose needed for the immediate beat.
- Add no speculative lore.
- Prefer concrete pressure, action, dialogue, and choice over explanation.
- Stop when the emotional turn has landed.

## Cognitive Tool Layer

When the task involves autonomous scene generation, add these controls before drafting:

```xml
<cognitive_tool_layer>
Scene_Mode: depiction | explanation | hybrid
Epistemic_Goal:
Active_Unseen_State:
Detail_Budget:
Withheld_Info:
</cognitive_tool_layer>
```

Rules:

- `Scene_Mode` controls prose density: depiction for recognition and atmosphere, explanation for causal mechanics.
- `Epistemic_Goal` controls what the reader should learn or infer now.
- `Active_Unseen_State` controls subtext: knowledge, hidden agenda, and true emotion.
- `Withheld_Info` protects tension by deferring lore that does not serve the current reader update.

## Surgical Editing

For targeted revision, defer to `$narrative-surgical-editing`.

Default workflow rule:

- Define the edit radius before changing text.
- Preserve surrounding prose unless it creates contradiction.
- Report exactly what changed.

## Hook, Hold, Payoff

Before chapter or scene generation, define:

```text
Hook:
Hold:
Payoff:
Failure risk:
```

After generation, verify:

```xml
<self_check>
Hook present:
Hold escalates:
Payoff lands:
Lore preserved:
Character motive coherent:
Prose efficiency:
Revision needed:
</self_check>
```

If `Revision needed` is yes, revise before final output.

## Output Shapes

For a new scene, use:

```text
<reasoning>...</reasoning>

Scene:

<self_check>...</self_check>
```

For a chapter plan, use:

```text
Chapter job:
Hook:
Hold:
Payoff:
Character turn:
Lore used:
Scenes:
Risks:
```

For a plot twist, use:

```text
Twist request:
Existing promises:
Option A:
Option B:
Option C:
Recommended option:
Cost:
Setup needed:
Payoff path:
```

For a surgical revision, use:

```text
Edit target:
Allowed edit radius:
Must preserve:
Revised passage:
Changes made:
Remaining risks:
```

For a lore contradiction halt, use:

```text
I need clarification before drafting because:
Known context:
Contradicting request:
Decision needed:
Recommended resolution:
```

For a prose compression pass, use:

```text
Keep:
Cut:
Compress:
Revised passage:
Why it is shorter:
```

## Guardrails

- Do not imitate David Perell, Morgan Housel, Alain de Botton, Steven Pressfield, or any living author's prose voice.
- Use the source material and component skills as craft guidance only.
- Do not quote long transcript passages.
- Do not overwrite the user's story intent.
- Preserve productive ambiguity; fix confusion, not mystery.
- Prefer asking one precise question over inventing missing canon.
- Make the author feel more in control of the story, not less.
