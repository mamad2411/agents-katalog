---
name: persona-roleplay
description: Simulate a person from a standardized persona artifact produced by persona-extractor. Use this skill when you want stable, evidence-grounded in-character dialogue, simulation, or answer generation without baking person-specific assumptions into the prompt.
---

# Persona Roleplay

This skill consumes a persona artifact, not raw biography.

Primary input:

- `personas/<persona_slug>/persona.json`
- `personas/catalog.json` when invocation begins from the router skill

Optional mirrors:

- `personas/<persona_slug>/profile.md`
- `personas/<persona_slug>/evidence.md`
- `personas/<persona_slug>/qa_samples.md`

Read this reference:

- `references/roleplay_contract.md`

If you need a compact runtime prompt, render it from the artifact:

```bash
python skills/persona-roleplay/scripts/render_roleplay_prompt.py \
  personas/<persona_slug>/persona.json
```

To prepare router-style invocation:

```bash
python skills/persona-roleplay/scripts/build_persona_catalog.py \
  --personas-dir personas
```

## Runtime Rule

Treat `persona.json` as the source of truth.

Do not add person-specific patches to the skill itself.

All fidelity should come from:

- dimensions
- evidence refs
- voice model
- scenario library
- simulation contract
- module registry
- load profiles

## Execution Order

1. Load the simulation contract.
   Determine:
   - identity frame
   - grounding order
   - uncertainty policy
   - modern-topic policy
   - persistence policy
   - exit policy

2. Classify the user request.
   Is it:
   - ordinary dialogue
   - advice request
   - conflict scene
   - explanation request
   - modern extrapolation
   - fidelity check

3. Retrieve the most relevant dimensions and scenarios.
   Prefer behavioral dimensions over ornamental style matching.
   If modular loading is available, select a scene-appropriate load profile instead of loading the full artifact.

4. Compose the answer using the voice model.
   Use:
   - register
   - cadence
   - rhetorical moves
   - response defaults
   - avoid list

5. Choose the grounding mode.
   Use:
   - `direct-source`
   - `source-grounded synthesis`
   - `synthetic extrapolation`

6. If the request exceeds the artifact, admit the limit while staying within the simulation contract.

7. Persist the role until exit.
   Once persona mode is active, keep responding fully in character until the user issues an exit command or explicitly asks to step out of character.

## Design Rules

- Preserve reasoning method before surface imitation.
- Keep the output human, not museum-like.
- Avoid catchphrase spam.
- Do not pretend the subject has direct knowledge of later events unless the contract explicitly allows synthetic extrapolation.
- Default to first-person role identification inside the scene, unless the user explicitly asks about the system's literal real-world identity.
- If the user wants analysis rather than pure roleplay, you may answer in a hybrid form:
  - simulated answer first
  - short fidelity note second

## Failure Modes

- acting from stereotype instead of artifact
- flattening contradictions
- pretending certainty where the artifact is thin
- sounding like a generic chatbot with a few famous quotes pasted on top
