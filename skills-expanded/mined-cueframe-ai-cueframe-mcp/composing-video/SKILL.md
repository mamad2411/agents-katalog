---
name: composing-video
description: "Use when choosing how to author or assemble a CueFrame video from footage, product actions, typography, diagrams, original motion or mixed media. For a supplied film use cueframe-reference-video; for a narrow existing edit use cueframe-compose-loop. Also use when an agent is asked to make any video with CueFrame: a product launch, announcement, promo, teaser, social clip, reel, short, explainer, animated explainer, concept video, product or dev-tool demo, walkthrough, or founder/talking-head piece. Triggers on \"make a video\", \"launch video\", \"promo\", \"teaser\", \"reel\", \"short\", \"explainer\", \"demo video\", \"talking-head\", or turning long-form footage into clips."
---

# Composing video

Make the requested film in the shared editable project. Start from the user's material, intended experience and current work. A useful creative premise can be a claim, a visible transformation, a character's action, a musical cause or an observation. Choose the form that expresses it; no universal narration, footage share, CTA, pacing or team size applies.

Use the [project and capability policy](references/project-policy.md) for scope, current state and metered work. Use the existing connection and supported tools. The final chat describes the film; the persisted composition is the authored result.

## Start at the right depth

| Request | Read when needed |
|---|---|
| Recreate a supplied film or its motion | `cueframe-reference-video`; keep its observed structure and fidelity anchors |
| New film without structure | `cueframe-storyboard`; keep the brief as small as the creative decision allows |
| Existing edit, preview or review | `cueframe-compose-loop`; preserve approved choices and inspect affected behavior |
| Custom 2D motion or reusable graphic | `cueframe-component-authoring`; select a card, exact reusable source or native component |
| Device, camera or 3D world | `cueframe-scene-shot`; use the current scene contract |
| Real product walkthrough | `cueframe-product-video`; distinguish actual captures from reconstructed artwork |
| Footage selection and speech edits | `clip-a-talking-head`; use source evidence and the saved edited timeline |

For motion relationships read [motion design](references/motion-design.md). For picture/audio synchronization read [sound and timing](references/sound-and-timing.md). For a new film's editorial choices read [format decisions](references/format-decisions.md). Load only the relevant depth; recipes do not add a mandatory production pipeline. `cueframe-cli` owns command mechanics and live discovery.

## Keep the creative decisions inspectable

For substantial new work, retain the intended outcome, useful reference/source IDs, timing landmarks, visual language and what must survive revision in the existing brief or project context. A concise description can be enough. Do not restart intake for an already clear request.

Choose an early preview that resolves the largest uncertainty: the difficult handoff, a readable product action, a physical pose, an unfamiliar material, or a timed visual idea. Prove that behavior before decorating every beat. Keep real captures and factual claims tied to their sources; reconstructed UI and generated scenes are valid authored media when described honestly.

Use meaningful editable inputs for likely revisions: copy, palette, subject identity, action times, pose and hold duration. Keep object relationships together so a change to the camera or device also moves its mounted contents. Current source pins, media bindings and timing contracts remain authoritative.

When layering graphics with media, use the canonical [visual track order](references/tool-map.md#visual-track-order).

## Shared authoring over Convex

Work directly for a small edit. Native peers are useful when independent authorship, specialized judgment or parallel investigation can improve the film. Let the task determine the division. All authors work on the same saved project through existing authenticated tools; their conversation is not a second composition store.

A useful handoff gives a peer the project/composition IDs, relevant sources and reference windows, intended result, current clip IDs or bounded scope, shared visual/timing decisions, neighboring handoff and what to preserve. Request saved contributions and evidence, not just advice. Read peers' saved results before integration; a successful task message alone does not establish authorship or coherence.

Use the observed revision for each atomic batch. After a conflict, reread and reconcile the changed fields with the intended edit; preserve concurrent human work. Never attach a fresh ETag to an old whole-document replacement. Exact revision checks remain appropriate for shared timing or other semantic dependencies; partial guards cover only what the deployed contract explicitly supports.

Inspect connected boundaries together, including parent transforms, backgrounds, masks and sound. A reviewer can help find a weak choice, but the integrated film still needs examination. [cueframe-compose-loop](../cueframe-compose-loop/SKILL.md) owns that evidence and revision loop; `video-craft-standards` supplies brief-specific review questions. Deliver the requested artifact with the remaining limitations stated plainly.

## Detailed guidance

Read only what the task needs.

| When | Read |
|---|---|
| Planning a new film or choosing its spine | [film planning](references/film-planning.md) |
| Writing a card or animating anything you author | [card tokens and the motion runtime](references/card-and-motion-runtime.md) |
| Choosing or placing sound effects | [SFX pack](references/sfx-pack.md) |
| Designing music, voice and sound together | [audio design](references/audio-design.md) |
| Making a launch, social clip, explainer, SaaS demo or founder piece | [format playbooks](references/format-playbooks.md) |
| Finding which tool or primitive delivers an effect | [craft to tool map](references/tool-map.md) |
| Looking for a visual grammar or craft default | [craft principles](references/craft-principles.md) |
| Stating acceptance criteria for new work | [acceptance template](references/acceptance-template.md) |

A card token key `x` is read as `var(--cf-x)`. Never put dashes in the key: `var(--plate)` then resolves to nothing, and CSS silently renders a transparent background with black text.
