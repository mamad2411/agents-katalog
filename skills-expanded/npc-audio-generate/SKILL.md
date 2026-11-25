---
name: npc-audio-generate
description: "Design and generate NPC dialogue, quests, voices, music, and sound with consent, narrative, localization, audio, and runtime gates."
---

# Npc Audio Generate

## Outcome

Create coherent, consented narrative and audio content that is safe to ship and practical to integrate.

## Required inputs

- narrative and audio bibles
- NPC or quest function
- voice consent, locale, platform, loudness, memory, and streaming constraints

Ask for missing information only when it changes the route materially. Otherwise
state conservative assumptions and proceed with read-only analysis.

## Workflow

1. Define canon, character boundaries, quest state model, prohibited outputs, pronunciation, and audio specification.
2. Verify model, dataset, voice, performer, music, and output rights before generation.
3. Generate structured dialogue and audio into review-only copies with stable identifiers.
4. Validate branching reachability, state consistency, lore, tone, safety, localization, subtitles, peaks, loudness, noise, and loop seams.
5. Integrate only approved content and run in-engine subtitle, playback, mixing, memory, and fallback tests.

## Expected artifacts

- content specification
- dialogue or quest graph
- review audio
- consent and provenance records
- engine integration evidence

## Workflow-specific gates

- Block voice cloning or identity imitation without explicit, documented consent and appropriate rights.
- Preserve text-only and non-generated fallbacks for accessibility and unavailable services.
- Do not expose credentials, private prompts, unreleased narrative, or player data to external services without approval.

## Production completion gate

Before recommending production use, complete and report all seven gates:

1. Rights, consent, code/model/dataset/output license, and generation-provenance checks.
2. Technical format, naming, scale, color, metadata, and target-import validation.
3. Visual and temporal consistency review across representative views and states.
4. Runtime memory, frame-time, draw-call, streaming, and asset-budget checks.
5. Playability and interaction smoke tests in the target runtime.
6. Screenshot, capture, diff, or artifact-regression evidence with reproducible settings.
7. Human approval before replacing source assets or promoting generated output.

Unknown rights, missing consent, unsupported hardware, conflicting host adapters,
or failed quality gates block production promotion. Preserve originals and make
fallbacks explicit.
