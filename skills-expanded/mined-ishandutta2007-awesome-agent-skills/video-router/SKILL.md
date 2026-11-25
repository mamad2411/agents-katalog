---
name: video-router
description: Guides agents to select and lock a video-production route. Use when a brief must be classified as generation, deterministic composition, footage editing, or an end-to-end combination before production, asset creation, editing, or rendering begins.
---

# Video Router

## Overview

Choose the dominant video-production line before work starts. A clear route prevents an agent from silently switching methods, discarding source-media constraints, or producing assets that cannot be assembled into the requested deliverable.

## When to Use

Use this skill when:

- A user asks to create, animate, edit, repurpose, or finish a video.
- A brief combines supplied footage with generated or designed scenes.
- The production approach is ambiguous and must be stated before execution.
- A production runtime is unavailable but the user still needs a complete plan.

Do not use this skill to author a composition, generate media, edit footage, or render output. Route first, then continue with the tool or skill that owns the selected line.

## Process

### 1. Read the delivery constraints

Identify the topic, duration, language, aspect ratio, supplied media, required output, and whether the user expects planned or produced media. Treat supplied media as a constraint: classify its relationship to the result as `reproduce`, `edit`, or `guide`.

### 2. Choose the dominant axis

- **Generate (A)** — AI-generated footage or imagery. Choose this for cinematic scenes, photoreal shots, characters, or b-roll that does not already exist.
- **Compose (B)** — Deterministic HTML composition. Choose this for explainers, kinetic typography, motion graphics, data visualization, title cards, captions, overlays, and transitions. This is the default for designed animation.
- **Edit (C)** — Work on supplied footage. Choose this for cuts, highlights, reframing, captions, audio cleanup, repurposing, or bounded semantic changes to existing video.

Use these primary signals:

| Brief signal | Primary route |
|---|---|
| Explain, teach, animate, motion graphics, kinetic text | Compose (B) |
| Make footage of, cinematic scene, character doing something | Generate (A) |
| Cut, trim, clip, repurpose, highlight, change my video | Edit (C) |

Aspect ratio sets the initial canvas: `16:9` uses `1920x1080`, `9:16` uses `1080x1920`, and `1:1` uses `1080x1080` unless the user specifies another target.

### 3. Select AUTO only for a cross-line deliverable

Choose **AUTO end-to-end** when more than one axis must be woven into the final output, such as:

- Editing supplied footage, then adding composed titles, captions, and narration.
- Generating an opener, editing the user's clips, and composing data scenes.
- Turning a mixed asset set into one finished video rather than returning separate assets.

AUTO sequences the axes; it does not erase them. Name the dominant delivery promise as `source_led`, `motion_led`, `compose_led`, or `hybrid`.

### 4. Lock and state the route

State the primary route in the proposal before production begins. Layers from other axes are allowed, but do not silently replace the primary route. If later evidence makes the lock wrong, explain why and ask the user to confirm the new route.

### 5. Handle an unavailable runtime

If production or rendering is unavailable, still return a complete unexecuted production package:

- Assumptions and delivery constraints
- Script or narration
- Timed storyboard or shot list
- Exact visible copy and captions
- Visual and audio direction
- Rights-safe asset provenance or fallbacks
- Export target
- Preview checklist and final playback/encoding QA

Clearly label planned media as unproduced.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I can start generating and decide later." | Early assets constrain timing, framing, and assembly. Lock the route first. |
| "The brief mentions AI, so Generate must be primary." | Designed explainers and motion graphics are Compose-primary even when they include generated imagery. |
| "Semantic editing means replacing the source with generated footage." | A bounded change to supplied video remains Edit or AUTO and must preserve the stated source boundary. |
| "No renderer is available, so there is nothing useful to deliver." | A complete, clearly unexecuted production package is still actionable. |

## Red Flags

- Production starts before the primary route is named.
- Supplied media is ignored or its requested relationship is not classified.
- A multi-axis deliverable is forced into one line without an assembly plan.
- The primary line changes mid-run without explanation and confirmation.
- Planned media is presented as if it were rendered or generated.

## Verification

Before continuing to production, confirm:

- [ ] Topic, duration, language, aspect ratio, inputs, and output target are known or explicitly assumed.
- [ ] Supplied reference media is classified as `reproduce`, `edit`, or `guide`.
- [ ] Generate, Compose, Edit, or AUTO is named as the primary route.
- [ ] Any supporting axes and their purpose are stated.
- [ ] The route appears in the proposal and remains locked unless the user approves a change.
- [ ] If execution is unavailable, the unexecuted production package is complete and clearly labeled.

## Source and License

Adapted from the OrkasVideoStudio [`video-router`](https://github.com/Orkas-AI/Orkas-VideoStudio/tree/414bb92be588cc3c92357e515805ff969d845cdb/packages/skills/video-router) skill at immutable source commit `414bb92be588cc3c92357e515805ff969d845cdb`. The source is MIT-licensed; its copyright notice is preserved in this directory's `LICENSE` file.
