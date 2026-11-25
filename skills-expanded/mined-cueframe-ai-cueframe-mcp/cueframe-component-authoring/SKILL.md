---
name: cueframe-component-authoring
description: "Use when authoring, forking or customizing CueFrame HTML cards, motion-graphics primitives or reusable native components, including a fork of an exact catalog source. Covers cloud MCP, local desktop and CLI project paths using complete versioned source snapshots. For scene-shot devices and cameras use cueframe-scene-shot. Triggers on \"customize the parallax look\", \"make my own animated lower-third\", \"fork a CueFrame template and edit it\", \"author a custom graphic and render it\". Use before hand-writing a component from scratch: forking a built-in is usually the faster start."
---

# CueFrame graphic authoring

Use the [project and capability policy](../composing-video/references/project-policy.md). Preserve the current project and source identities; make the intended visual behavior inspectable and editable.

## Choose the representation

- **HTML card:** authored typography, UI, diagrams and 2D motion with deterministic CSS. It can depict perspective, but does not provide the scene renderer's physical camera, lighting or occlusion.
- **Whole-clip keyframes:** position, scale, rotation and opacity when the entire card or layer moves together. Read the current `clip.setKeyframes` schema; times are relative to the clip.
- **Scene shot:** supported groups, devices, pages, world text, surfaces and cameras. Use `cueframe-scene-shot` and its current schema; author JSON, not the generated wrapper.
- **Native component:** reusable version-4 media-tile scenes with declared inputs, assets and deterministic rendering. Discover a near-fit example before writing one; definitions, presets and recipes carry different editable information. Read the [native source contract](references/native-source-contract.md), then the applicable [MCP, CLI or desktop workflow](references/native-component-workflows.md). This is not an arbitrary browser application runtime.

Search the builtin component library without restricting it to definitions. Use concrete mechanism terms (for example card, shuffle or carousel); the current query matches literal substrings, not semantic synonyms. Inspect the selected poster and motion, and read its exact source/document before deciding fit. An unfamiliar mechanism needs source and evidence inspection; if none fits the inputs, motion or runtime, state that limitation and choose an admitted representation deliberately. Org library filtering can be refused; do not describe an unfiltered page as a matching search.

A definition, preset and recipe are different catalog items. Preserve the selected item's exact scoped identity. A builtin source read needs `componentId`, `sourceVersionId` and `builtinCollection`; unavailable pins do not authorize a different source. Keep the complete template, manifest and definition when forking. On the hosted editor/API, resolve builtin presets and recipes with `resolve_builtin_component` using the selected collection, ID and revision; source-only reads do not recover selected preset values. Insert with `apply_template` using its exact `documentSha256`, explicit start time, unique ID prefix and your own media bindings. A URL is not received pixels: check delivery status and inspect attached poster bytes; open the movie through the current host’s supported viewer or record motion as unobserved.

## Cards: geometry, clock and controls

A card source is `{kind:"card", html, tokens}`. Each token key `x` becomes the CSS property `--cf-x`; read `var(--cf-x)`. Keys have no leading dashes. Missing variables silently invalidate CSS, so inspect returned warnings and actual output. Use literal or supported whole-string brand references and do not overwrite reserved motion variables.

The host injects a clip-local clock each frame: `--cf-frame`, `--cf-t` (seconds), `--cf-fps`, `--cf-duration` (frames), `--cf-progress`, `--cf-ease`, `--cf-enter` and `--cf-exit`. CSS animations, transitions and timers are not the render clock. The built-in entrance/exit ramps span up to 18 frames; use explicit event times when the brief needs other choreography.

Use flex/grid for text and UI reflow, and coordinate-based nested transforms for spatial animation. Parent mounted contents to their object: a moving phone should carry its bezel, screen mask and controls. Use a separate local transform only when that part really moves relative to the object. The [parented motion recipe](references/parented-motion.md) includes a complete editable card with a shared pose and named pointer-contact/response times.

Expose likely revisions as meaningful inputs rather than unrelated constants. A card's text token used by CSS `content` needs a quoted CSS string. Preserve the current token values when changing its HTML. The native component definition declares defaults and input controls; its placement binds media in `execution.assets`, separately from `params`.

## Iterate on the saved result

Keep the same owned component ID while updating its complete source. Saving creates a new immutable source version; existing placements keep their old pins unless explicitly repinned in the intended composition. An isolated preview is not a saved timeline edit. The workflow reference explains scoped repinning and local preview commits.

Use [cueframe-compose-loop](../cueframe-compose-loop/SKILL.md) for isolated, integrated and final evidence. Preserve production duration when previewing duration-dependent motion. Check the relationship that could fail, including screen corners, overlap, pointer contact and the complete ending, rather than only a pleasing middle still. For `needsUpgrade`, use [retired-source recovery](references/retired-projects.md) and replace only the reported clips.

## Detailed guidance

- [Authoring paths](references/authoring-paths.md): the MCP path step by step, when no filesystem is available.
- [Forking and layout](references/forking-and-layout.md): what to fork, flex and grid inside a component, and what to avoid.
