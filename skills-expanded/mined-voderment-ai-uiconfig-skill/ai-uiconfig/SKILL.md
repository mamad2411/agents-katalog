---
name: AI-UIconfig-skill
description: >
  Refactor an existing SwiftUI project into a governed UI architecture with render-state boundaries,
  tokenized styling, preview mocks, and a debug-only runtime tuning + writeback tool. Use when the user
  wants to improve UI maintainability, live-tune styles, or build a reusable UI debugging workflow
  without changing the product's visual intent.
---

# AI-UIconfig-skill

Turn an existing SwiftUI project into a UI system that is:

- easier to debug
- safer to refactor
- previewable in isolation
- adjustable at runtime in `DEBUG`
- able to write approved style values back into source

This skill is optimized for SwiftUI apps on Apple platforms. It is especially useful when a project already has a meaningful UI but the UI code is mixed with runtime logic, styling is hardcoded across many views, and designers/developers need faster visual iteration.

## Default Principle

The default mode is **preserve mode**:

- Do **not** intentionally redesign the product.
- Do **not** change behavior or visual output unless required to create safe structure.
- Prefer equivalent refactors over aesthetic changes.
- The goal is to improve **control**, not to impose a new design.

Only switch to **extend mode** when the user explicitly wants new UI to be brought into the same system.

## Preserve Mode vs Extend Mode

### Preserve Mode

Use for existing UI that already ships or already has product intent.

In preserve mode:

- keep existing visuals materially unchanged
- keep existing interaction behavior materially unchanged
- extract styles into governed tokens/metrics
- split runtime orchestration from pure UI
- add previews, mocks, tuning tools, and writeback

### Extend Mode

Use when the user has already added new UI or explicitly wants new UI added.

In extend mode:

- this skill does **not** invent the design language for the new UI
- it helps absorb the new UI into the same governed system
- new stable style values should be folded into tokens/metrics
- new view states should get preview mocks and render-state inputs
- new governed values can then be exposed in the runtime tuning tool

## What This Skill Produces

When fully applied, this skill should leave the project with these building blocks:

1. A clear UI directory structure.
2. Runtime/composer views separated from pure UI views.
3. Render-state types for pure UI inputs.
4. Preview mocks and preview galleries for major states.
5. A tokenized style layer.
6. A debug-only runtime tuning tool for governed values.
7. A save/export workspace for tuning snapshots.
8. A writeback service that updates approved source constants.
9. A saved-config list that can explicitly reload prior tuning snapshots.
10. Optional debug-only surface controls that can trigger stable mock scenes and pin governed UI states open for tuning.

## Non-Goals

Do **not** treat this as a generic no-code UI designer.

This skill does not:

- automatically understand arbitrary Swift source via AST scanning
- expose every modifier or every constant as a runtime control
- redesign product UI without explicit user direction
- rewrite entire metrics files when only leaf values need updates
- solve runtime logic bugs that are unrelated to UI structure
- ship debug tuning affordances in release builds

## Best-Fit Conditions

This skill is a strong fit when:

- the app uses SwiftUI
- the project has repeated layout/styling values
- runtime logic and visual code are mixed together
- the team wants faster visual iteration
- the team benefits from Xcode Canvas previews
- the same UI surfaces are revisited often

It is a weaker fit when:

- the UI is highly experimental and not yet structurally stable
- the app is primarily UIKit/AppKit without meaningful SwiftUI surfaces
- the user only wants one small visual tweak

## Execution Contract

Always follow this order unless the user explicitly narrows the scope.

### 1. Inventory the UI

Identify:

- major UI surfaces
- major states per surface
- current runtime/composer files
- current pure UI files
- current metrics/constants files
- hardcoded style clusters worth tokenizing first

Output a concrete map of:

- what should stay runtime-facing
- what should become pure UI
- what should become tokenized
- what should get preview mocks first

### 2. Establish UI Boundaries

Split code into:

- runtime/composer/orchestration layer
- pure UI layer
- shared UI primitives
- preview/mocks layer

Rules:

- runtime/composer layer may read models, side effects, services, polling, bridges
- pure UI layer should only consume render state and style tokens
- preview layer must not trigger real services or side effects

### 3. Introduce Render State

For each major surface or module, define render-state inputs that are:

- UI-only
- preview-safe
- independent from `ObservableObject` internals where practical

Rules:

- pure UI views should not depend directly on runtime models unless the user explicitly accepts that tradeoff
- preview galleries should consume render-state mocks, not real module models

### 4. Tokenize Stable Styling

Extract style values into governed tokens/metrics.

Prioritize:

- spacing
- padding
- corner radius
- opacity
- semantic colors
- animation durations
- common surface dimensions
- module chrome values

Do **not** expose every value automatically.

Only govern values that are:

- stable enough to matter
- likely to be tuned more than once
- meaningful across a component, surface, or module

### 5. Build Preview Support

Create:

- preview mocks
- preview containers
- preview galleries

Required preview goals:

- cover the main states the user actually debugs
- include every materially different visual state for the governed surface
  - for example: `closed`, `peek`, and `expanded` when a shell uses those states
- avoid real polling, bridges, media control, network calls, or system mutations
- make the most important states easy to compare side by side

### 6. Add Debug-Only Live Tuning

Add a debug-only tuning tool that:

- edits the governed tokens/metrics at runtime
- updates the active UI immediately
- keeps a working copy separate from the saved baseline
- can save/export the current working state
- supports reverting the whole session to the saved baseline
- supports reverting a single governed parameter without discarding other current edits
- exposes a saved-config list so prior tuning snapshots can be reloaded explicitly
- can trigger explicit mock presentation states for isolated UI debugging when live runtime data is inconvenient
- can pin peek or expanded states open while tuning so shell surfaces do not auto-collapse mid-adjustment

Rules:

- the tuning tool must be `DEBUG` only unless the user explicitly wants otherwise
- release builds must not expose the editor
- editor UI should be safe and inspectable, not magical
- when practical, the tuning tool should inherit the host project's existing design language instead of introducing a generic inspector style
- prefer reusing the project's own tokens, typography, color semantics, spacing scale, corner radii, and shared UI primitives for the editor chrome and controls when those inputs are stable enough
- if the project already has an internal settings, debug, or utility-chrome pattern, follow that pattern first
- fall back to a neutral debug presentation only when the project does not yet have a stable style language worth inheriting
- debug mock scenes and pinning controls must be clearly framed as development aids, not product features
- mock scenes should be backed by stable sample data routed through the same render boundaries as the real UI when practical
- by default, app relaunch should return to the source-defined baseline unless the user explicitly wants auto-restore
- saved configs should remain available as explicit snapshots the user can choose to reload for a new tuning session
- the runtime token baseline must derive from the same source constants that writeback edits; do not keep a second divergent hardcoded default table

### 7. Add Precise Writeback

Writeback should:

- save the current working snapshot externally
- update only mapped leaf constants in source
- preserve hand-written structure, comments, and derived values
- avoid broad file rewrites when unnecessary
- emit syntactically valid source literals for every supported value type
- avoid replacement strategies that can corrupt source text through regex-template escaping or truncated literal serialization
- preserve each source declaration's prefix and suffix and replace only the matched value span

Rules:

- use explicit token-to-source mappings
- do not perform destructive wide rewrites of style files
- fail explicitly when a mapped constant cannot be matched exactly once
- generated external snapshots should not automatically become app target inputs

### 8. Validate

Always finish with:

- compile/build verification
- preview validation when feasible
- a clear report of what is covered vs not covered

If interaction behavior is high risk, explicitly call out what still needs manual runtime regression.

## Output Expectations

When applying this skill, the final result should tell the user:

- which surfaces were governed
- which tokens were added
- which views were split or extracted
- which previews were added
- whether a debug editor was added
- whether writeback exists and what it can touch
- what remains manual or not yet governed

## Naming and Boundary Guidance

Prefer consistent layers such as:

- `UI/`
- `UI/PreviewSupport`
- `UI/<Surface>`
- `UI/Modules/<Module>`
- `UI/DesignTokens`

Type naming guidance:

- `...RenderState` for UI-only inputs
- `...PreviewMocks` for mock builders
- `...Metrics` or `...Tokens` for governed values
- `...Editor...` for debug tuning interfaces
- `...WritebackService` for source update services

## Localization Guidance for Tuning Tools

If the project includes a runtime token editor:

- keep code-facing identifiers readable and stable
- prefer leaving parameter names and module names aligned with source semantics
- localize the **explanatory descriptions**, not the underlying code mapping, unless the user explicitly asks otherwise
- prefer localizing tool chrome and explanatory help, while preserving code-facing token keys as-is
- if the tool supports saved configs, keep snapshot names/code keys stable and human-auditable rather than translating them

This avoids polluting the code-facing layer while still making the tool understandable in the user's language.

## Safety Checklist

Before finishing, verify these constraints:

- existing UI was not intentionally redesigned without explicit approval
- runtime logic is not accidentally triggered in previews
- debug-only tools are not exposed in release
- writeback does not overwrite unrelated code
- tokenized values still resolve to the original visual baseline by default
- relaunch behavior is explicit: source baseline by default, snapshot restore only when deliberately chosen
- the project still builds

## Maintenance Contract

This skill must stay aligned with behavior validated in real projects.

When a project changes any governed UI workflow behavior, explicitly decide whether the skill contract also changed.

Examples that usually require re-evaluating the skill:

- render-state boundary changes
- preview coverage rules
- token scope changes
- runtime editor behavior changes
- save/load snapshot behavior changes
- revert semantics changes
- writeback targeting or path resolution changes
- localization rules for the tuning tool
- baseline/default-session behavior changes

If the change affects how the governed workflow is supposed to work, update the skill definition.

If the skill definition changes, sync it to the public `AI-UIconfig-skill` repository as part of the same maintenance cycle.

Pure project-specific bug fixes that do not change the reusable contract do not always require a skill update, but they must still be checked against this rule.

## Adoption Checklist for New UI

When a new UI surface is added later, fold it in using this order:

1. Build the UI normally.
2. Wait until the structure is stable enough to govern.
3. Extract stable styles into tokens/metrics.
4. Define render-state inputs.
5. Add preview mocks and gallery states.
6. Add selected governed values to the debug editor.
7. Add writeback mapping only for stable leaf values.

## Good Prompt Shapes

This skill works well with requests like:

- "Use AI-UIconfig-skill to refactor this SwiftUI surface into render-state and previewable UI."
- "Use AI-UIconfig-skill to tokenize the stable layout and spacing values for this module."
- "Use AI-UIconfig-skill to add a debug-only runtime editor for the governed UI tokens."
- "Use AI-UIconfig-skill in preserve mode. Keep the existing design, but make the UI easier to iterate on."
- "Use AI-UIconfig-skill to fold this new module into the existing token/preview/writeback system."

## Bad Prompt Shapes

This skill is not the right primary tool for:

- "Invent a completely new visual design"
- "Expose every number in the project as a slider"
- "Rewrite the whole app architecture"
- "Fix a network or persistence bug unrelated to UI structure"

## Working Style

When using this skill:

- preserve existing product intent first
- extract structure before adding tooling
- tokenize only stable values
- keep previews deterministic
- keep the editor understandable
- keep writeback explicit and narrow
- after workflow-related changes, re-evaluate whether the skill and public repo need to be updated
- compile often
