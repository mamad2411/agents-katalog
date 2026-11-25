---
name: mobile-ui-design
description: Create premium, portfolio-grade mobile UI concepts through reference-led, user-selected style exploration, including multi-screen product boards, reusable style-family classification, color-rich modular app surfaces, and implementation-ready UI specifications. Use when Codex needs to design or redesign iOS/Android interfaces, classify or add visual styles from supplied UI boards, generate three comparable ImageGen 2 mobile style previews, match the quality and art direction of supplied multi-screen UI references without copying them, fix generic or weak AI-generated app visuals, or turn validated UX inputs into rendered concepts plus complete UI/component specifications.
---

# Mobile UI Design

Design a believable mobile product with a strong visual world. Treat rendered screens as a primary deliverable, not an optional afterthought. Preserve product truth, native behavior, recovery, accessibility, and platform conventions while achieving portfolio-grade visual impact.

## Choose the delivery mode

Infer the smallest mode that satisfies the request:

- **Visual concept:** Default when the user asks to design, redesign, create UI, make screens, improve appearance, or provides visual references. First produce a reference set and exactly three comparable ImageGen 2 style previews, then pause for the user's choice before generating the full screen set.
- **Specification:** Use when the user explicitly requests tokens, components, screen contracts, JSON, handoff documentation, or implementation guidance.
- **Full package:** Use when the user asks for both visual output and implementation-ready design. Complete the reference-and-preview gate first, then derive the specification from the direction the user selected.

Never answer a visual-design request with only prose, a mood board, wireframes, or JSON. Do not require formal upstream artifacts when a product idea and reasonable assumptions are enough to create a reversible concept.

## Establish the input contract

Accept any useful combination of:

- Product idea, target users, platform, and desired screens.
- Supplied screenshots or visual references.
- Existing app screenshots that need redesign.
- `ux-architecture.json` for actors, flows, screen responsibilities, states, and acceptance.
- `design-dna.json` for visual principles, token provenance, and adaptation boundaries.
- Brand assets, copy, localization, and implementation constraints.

Inspect every supplied image. If the user supplies a multi-screen board, read [references/supplied-reference-board-standard.md](references/supplied-reference-board-standard.md) and treat its presentation grammar, density, color confidence, module rhythm, and device treatment as the primary visual target. If the board contains several product categories or the user asks to add styles, also read [references/mobile-style-family-catalog.md](references/mobile-style-family-catalog.md), classify the board across surface, information mode, asset mode, and interaction archetype, and record the reusable family evidence in `reference-set.md`. If the user has not supplied enough references, use `mobile-reference-research` or search for a small reference set before generating concepts; use image search or the available browser/search surface for current examples, and prefer real native-mobile products or platform surfaces for interaction evidence. Extract principles rather than copying a distinctive layout, branded asset, character, or component bundle. If formal inputs conflict, preserve task completion, consent, privacy, recovery, and required states first. Record only assumptions that materially affect the result.

Read [references/visual-lock-contract.md](references/visual-lock-contract.md) for every visual request. A reference board is not a mood label: extract a reference fingerprint, carry its evidence IDs into each candidate, and write exact semantic theme tokens before generating previews. The selected fingerprint and theme tokens are the only visual source of truth for downstream Design System and prototype work.

## Follow the visual-first workflow

### 1. Frame the product in one screenful

State internally or in a short working note:

- Product category, core job, target user, and dominant platform.
- Core flow as `entry → action → feedback → durable result/recovery`.
- Required screen count and the reason each screen exists.
- Information-density target and frequent thumb action.
- What the reference set contributes and what must not be copied.

Do not spend the visual-design turn producing a long product strategy document unless the missing choice changes the product materially.

### 2. Find and interpret references before choosing a style

Create `reference-set.md` with [assets/reference-set-template.md](assets/reference-set-template.md). Use supplied images first; when they are missing or too narrow, search for additional references. Record a source path or URL for every reference, inspect it, and state one concrete quality to borrow and one boundary not to copy. When a supplied board is a style library, add a concise style-family mapping instead of treating every panel as a separate product brief. Keep at least 60% of the set native-mobile or platform-surface references, including one real native-mobile product. Use non-UI references only for material, lighting, imagery, or motion—not for the mobile screen skeleton.

Do not start full-screen generation until this reference set exists. Read [references/portfolio-visual-standard.md](references/portfolio-visual-standard.md), [references/supplied-reference-board-standard.md](references/supplied-reference-board-standard.md) when a board is supplied, [references/mobile-style-family-catalog.md](references/mobile-style-family-catalog.md) when the board contains multiple style families, and [references/visual-direction-rules.md](references/visual-direction-rules.md) while synthesizing the set.

When the user explicitly asks to add a supplied style board, append a new reference record and mapping to the working `reference-set.md`, then extend the catalog only with repeatable visual grammars that are not already covered. Preserve earlier families; do not replace the library or turn one screenshot into a family.

### 3. Prepare three style directions for comparison

Before committing to a visual bible, create exactly three materially distinct style directions for the same product, core flow, screen responsibilities, copy, device frame, and presentation canvas. When the supplied reference is a multi-screen board, use the same 3-screen mini-flow (home/today → core action/detail → review/result) for every direction; do not reduce the comparison to one hero screen. When a style-family catalog applies, choose one reference-near family, one adjacent family, and one controlled-contrast family unless the user specifies exact families. Vary the visual system—not the product requirements—so the user can compare style rather than rendering luck. Each direction must name:

- a product-specific visual thesis;
- a reusable `styleFamily` plus the concrete `familyEvidence` borrowed from the reference;
- palette, typography, material, composition, and signature-asset differences;
- the unchanged native structure, primary action, and before/during/after state sequence;
- production, accessibility, and posterization risks;
- a comparable ImageGen 2 preview slot.

Also record `styleFamily`, `familyEvidence`, `referenceIds`, `themeVariant`, and exact `themeTokens`. The theme tokens must visibly encode the reference's color hierarchy, type relationship, radius/depth language, and spacing rhythm; prose such as “premium” or “colorful” is not a token.

Do not create five hidden candidates, internally pick the highest score, or average the three into a compromise. Scores are safety and quality evidence only; the user chooses the direction.

### 4. Generate the three ImageGen 2 previews

Use [assets/visual-concept-prompt-template.md](assets/visual-concept-prompt-template.md). Generate one preview package per direction with separate built-in ImageGen 2 calls. For a supplied multi-screen board, generate at least three standalone portrait screens per direction, then compose a clean 3-device preview board; preserve the same screen responsibilities, copy, device treatment, aspect ratio, and light presentation canvas across all directions, and change only the direction's visual system. Store every source render, board path, and prompt reference in `style-preview-manifest.md` using [assets/style-preview-manifest-template.md](assets/style-preview-manifest-template.md). A single large hero image is not a valid preview package for this reference mode.

Inspect every standalone render and every board at full detail. Regenerate a weak screen before presenting the trio. The preview packages must be like-for-like, clearly different in palette/material/type/composition, bright or color-confident when the supplied reference is bright, native-app-like, information-rich enough to show product rhythm, readable, and free of direct reference copying.

### 5. Pause for the user's style choice

Present the reference synthesis, the three preview boards, and a compact comparison table. Show the standalone source screens when the board could conceal detail. Ask the user to choose one direction by ID or name. Stop at this gate. Do not generate the complete screen sequence, tokens, JSON, or implementation specification before the user chooses, and never silently choose on the user's behalf. If the user explicitly delegates the choice, record that explicit delegation as the selection source.

Persist the preview package with `selectionStatus: awaiting-user-selection`, `selectionSource: pending`, and `visualLock.status: unlocked`. A downstream Design System or prototype Runner must refuse an unlocked package; this prevents a legacy theme from appearing as the default.

### 6. Lock the selected visual design bible

After the user chooses, record the selected direction in `visual-direction.md` and commit to one coherent system:

- One visual thesis tied to the product mechanism.
- One palette family: one dominant field, one supporting surface family, one signal accent, and semantic exceptions only.
- One typography relationship: display character plus highly legible interface text.
- One material language: photographic atmosphere, soft polymer, technical glass, matte paper, anodized metal, luminous display, or another product-specific material.
- One signature visual asset system: product photography, 3D object, anatomical/technical illustration, tactile abstract form, editorial image crop, or data visualization.
- One shape and radius logic, one icon family, one navigation model, and one depth model.
- One interaction signature and one motion grammar.

Do not average several styles into a compromise. Reject category defaults such as generic pastel wellness cards, purple-blue glass dashboards, random neon fintech charts, and white card stacks with stock outline icons.

Copy the selected `styleFamily`, `referenceIds`, `themeVariant`, `themeTokens`, and `antiDefault` rules into the handoff's `visualLock`. Every later artifact must cite that lock. If a component, renderer, or platform surface cannot honor it, preserve the lock and report the unresolved gap instead of falling back to a familiar AI theme.

### 7. Design a coherent screen sequence

Default to three screens when the user does not specify a count:

1. A strong entry or home screen that establishes the world.
2. The core action screen with clear operation and thumb reach.
3. A result, detail, or management screen that proves the system can continue.

Add screens when needed for onboarding, authentication, search, detail, checkout, settings, errors, permissions, or recovery. Every screen must advance the same believable flow. Vary composition and density across screens while keeping palette, typography, materials, components, icons, imagery, and device treatment consistent.

For each screen define:

- User question and primary action.
- Dominant visual focal point.
- Ordered content regions and navigation.
- Exact short copy worth rendering.
- State shown and how it connects to adjacent screens.
- Safe-area, keyboard, sheet, and platform behavior when applicable.

### 8. Build the image-generation brief

Use [assets/visual-concept-prompt-template.md](assets/visual-concept-prompt-template.md). Include supplied reference images through the available image-reference mechanism, especially the user's multi-screen board, but describe the reusable qualities to inherit and explicitly prohibit direct copying. Read [references/supplied-reference-board-standard.md](references/supplied-reference-board-standard.md) when the reference is a contact sheet or presentation board.

Prompt for:

- A real native app, not a website or poster inside a phone.
- The chosen `styleFamily`, its surface/information/asset axes, and the supplied reference evidence; do not reduce a family to a hue swap.
- Comfortably readable text and short, exact labels.
- One unmistakable focal asset or content-led visual module per key screen.
- Strong foreground, midground, and background separation.
- Color-rich but disciplined modules when the reference uses bright UI; do not flatten the product into one muted or monochrome world.
- Believable system chrome, safe areas, navigation, and touch targets.
- Purposeful image crops, 3D objects, photography, or authored illustrations when appropriate.
- Clean, consistent device framing and a light neutral presentation canvas for board-style references.

Avoid vague prompts such as “modern, clean, beautiful UI.” Describe composition, hierarchy, material, lighting, palette, asset type, navigation, and screen state concretely.

### 9. Render screens as the main deliverable

Use the available image-generation tool for visual concepts. Generate enough images to make the flow legible.

Produce:

- **Standalone screen renders:** one clean portrait image per important screen. Do not obtain these by cropping a collage.
- **Presentation board:** after the screen system is stable, generate or compose one landscape board with two or three aligned devices, or a 3-by-2 contact sheet when that matches the supplied reference, with a light tonal backdrop, equal gutters, consistent scale, and restrained grounding shadows. Match the polished multi-screen product presentation quality of the user's references without copying their screens.

When generating several screens, keep the same design bible in every prompt. Carry forward persistent data, selection, progress, and user context so the sequence feels real.

### 10. Inspect and iterate

Inspect every render at full available detail. Do not accept the first output automatically.

Regenerate or edit when any of these appears:

- Tiny, broken, nonsensical, or overly dense text.
- Website-like hero composition or controls pushed below the fold.
- Generic dashboard cards, random charts, arbitrary pills, or stock icon language.
- Weak or absent focal imagery.
- Muddy color, excessive gradients, or inconsistent accents.
- Screen-to-screen drift in device, palette, radius, icon, or type language.
- Fake navigation, unsafe placement, or unclear primary action.
- Flat composition with no foreground/midground/background structure.
- A phone frame that dominates the product.

Run at least one explicit critique-and-revision pass for a multi-screen set. A weak screen must be regenerated as a standalone screen, not hidden inside the board.

### Optional fallback when the user dislikes the generated image

If the user says the preview is ugly, unsatisfactory, or asks to use ChatGPT's in-chat image creation, offer a concise optional fallback: they can generate an alternative in a ChatGPT conversation and upload it here as a new reference. Treat the uploaded result as a user-supplied reference and continue the same reference-analysis, three-direction, and selection workflow.

Do not claim that this skill can directly invoke ChatGPT's chat-image UI, silently switch generators, open a new conversation, or discard the current preview state. Keep the existing artifacts and selection gate intact unless the user explicitly asks to replace them.

### 11. Produce specifications when requested

Only after a user-selected visual direction is recorded and `visualLock.status` is `locked`, create:

- `reference-set.md` using [assets/reference-set-template.md](assets/reference-set-template.md).
- `style-preview-manifest.md` using [assets/style-preview-manifest-template.md](assets/style-preview-manifest-template.md).
- `visual-direction.md` using [assets/visual-direction-template.md](assets/visual-direction-template.md).
- `render-manifest.md` using [assets/render-manifest-template.md](assets/render-manifest-template.md).
- `ui-spec.md` using [assets/ui-spec-template.md](assets/ui-spec-template.md).
- `component-spec.md` using [assets/component-spec-template.md](assets/component-spec-template.md).
- `ui-design.json` using [assets/ui-design-template.json](assets/ui-design-template.json) and [references/ui-design-schema.md](references/ui-design-schema.md).

Read [references/component-system-rules.md](references/component-system-rules.md) before creating tokens and components, and [references/screen-spec-rules.md](references/screen-spec-rules.md) before writing screen contracts.

Run `python3 scripts/validate_ui_design.py <path-to-ui-design.json>` and fix every error. Preserve every upstream Screen ID, State ID, requirement, platform note, and acceptance signal when formal upstream artifacts exist.

When handing off to `mobile-design-system` or `mobile-prototype`, pass the same `ui-design.json` containing the locked visual direction. Do not rebuild from `design-dna.json` alone; that is how a selected reference style gets replaced by an older default.

For a reusable cross-screen system, hand the validated UI artifact and Design DNA to `mobile-design-system`. For an executable behavior test, hand the screen/state contract to `mobile-prototype` before code implementation, then run its UI-to-prototype alignment validator so no rendered state or explicit interaction disappears in the prototype.

## Preserve state and platform integrity

Rendered beauty never replaces state completeness. For empty, loading, slow, offline, partial, failed, retrying, stale, expired, blocked, permission, unsupported, destructive, and accessibility-pressure states define what remains visible, the exact recovery action, focus/announcement behavior, and a non-color equivalent.

Keep iOS and Android behavior meaningfully distinct. Respect safe areas, native navigation, system sheets, keyboard behavior, text scaling, localization, reduced motion, and system handoffs. A visual signature may collapse under large text or keyboard pressure; the task may not.

## Enforce the output order

For visual concept work before the user has chosen:

1. Reference set, reference-board analysis when applicable, and one-paragraph product framing.
2. Exactly three comparable style preview packages; for board-style references, each package contains a 3-screen mini-flow plus its presentation board.
3. Compact comparison table and a direct choice request.

After the user chooses, continue with:

1. The selected visual direction and assumptions.
2. Standalone screen renders in flow order.
3. Presentation board.
4. Short quality note naming what was revised and any unverified behavior.

For full packages:

1. Visual direction and rendered evidence.
2. Coverage ledger and foundations.
3. Token and component systems.
4. Screen, state, overlay, and system-surface specifications.
5. Platform, responsive, accessibility, content, and motion rules.
6. Traceability, acceptance, open questions, and confidence.

## Run the quality gate

Read [references/ui-design-rubric.md](references/ui-design-rubric.md) and revise every blocker.

Do not finish a visual request when the result contains only documentation, fewer or more than three comparable style previews at the selection gate, a hidden or automatic style choice, a full screen set generated before user choice, a single hero screen where the supplied reference is a multi-screen board, generic AI-dashboard composition, empty editorial composition, inconsistent screens, unreadable text, weak focal assets, a flat or monochrome result that ignores a bright supplied reference, or a presentation board that is more polished than its underlying standalone screens. The final result must be recognizable as one premium product world and remain operable without the phone frame.
