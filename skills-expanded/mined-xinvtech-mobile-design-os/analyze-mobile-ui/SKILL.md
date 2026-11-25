---
name: analyze-mobile-ui
description: Analyze mobile app screenshots, store listings, and reference products to extract product mechanics, UX patterns, visual Design DNA, platform conventions, and reusable design rules. Use when Codex needs to explain why an iOS or Android interface works, compare mobile UI references, generate an evidence-based design.md or design-dna.json, or adapt proven mobile design principles to a new product without cloning the source app.
---

# Analyze Mobile UI

Turn mobile UI evidence into a traceable design system and adaptation brief. Separate what is visible from what is inferred, and separate reusable principles from source-product identity.

## Select the operating mode

Use one or combine both:

- **Analyze**: explain product mechanics, UX patterns, and visual Design DNA from supplied evidence.
- **Adapt**: translate the findings into a different product brief without reproducing the source app.

If the user asks for reference discovery rather than detailed analysis, use `mobile-reference-research` first. If the user asks for UI generation or implementation, complete the analysis package first and hand it to the appropriate design or coding workflow. Do not invent screens in this skill.

## Collect the minimum input

Establish:

- Reference app, screenshots, URLs, or files.
- Target platform: iOS, Android, or cross-platform.
- Analysis goal: understand, compare, document, or adapt.
- Target product brief when adaptation is requested.
- Evidence date and app version when known.

Proceed with partial input when useful analysis is still possible. Ask for more evidence only when a missing view blocks the requested conclusion. State all unresolved gaps.

## Follow the workflow

### 1. Build an evidence inventory

Assign stable identifiers such as `E1`, `E2`, and `E3` to every screenshot or source. Record the screen, platform, state, source URL or file, capture date when known, and limitations.

Inspect each provided image rather than relying on its filename or surrounding description. For public references, prefer official product pages and current platform documentation. Record access dates for changeable sources.

### 2. Record observations before interpretation

Describe only visible or directly documented facts. Attach at least one evidence ID to every important observation.

Use these labels consistently:

- `Observation`: directly visible or documented.
- `Inference`: a plausible explanation supported by observations.
- `Recommendation`: a decision for the target product.

Do not present inference as fact.

### 3. Analyze the product mechanism

Identify:

- Core user value and job to be done.
- Entry point, activation moment, core loop, and return loop.
- Emotional drivers, social dynamics, and retention mechanisms.
- Monetization or growth patterns only when evidence supports them.
- Product-specific mechanisms that should not transfer blindly.

Read [references/mobile-ux-patterns.md](references/mobile-ux-patterns.md) for the mechanism and state checklist.

### 4. Analyze UX structure

Map navigation, information hierarchy, primary actions, progressive disclosure, feedback, recovery paths, permissions, and device integrations. Include happy path and missing states.

When a widget, notification, Live Activity, complication, lock-screen surface, or other system-managed surface carries product value, define its activation state, freshness contract, tap destination, privacy exposure, unsupported state, and in-app fallback. Do not treat surface visibility as proof of current data or successful delivery.

Read the platform reference that matches the evidence:

- Read [references/ios-patterns.md](references/ios-patterns.md) for iOS and iPadOS.
- Read [references/android-patterns.md](references/android-patterns.md) for Android.
- Read both for cross-platform comparisons; preserve platform differences instead of forcing visual parity.

### 5. Extract Design DNA

Describe the visual system across color, typography, spacing, layout, shape, elevation, imagery, iconography, components, motion, content voice, accessibility, and platform expression.

Read [references/design-dna-schema.md](references/design-dna-schema.md) before creating structured output. Give each claimed token an origin, source, confidence level, and `estimated` flag. Use `specified` for a deliberate new target token so it cannot be mistaken for a value extracted from the reference. Avoid naming a reference font, exact color, spacing value, duration, or curve unless it is measured or documented.

### 6. Adapt without cloning

When a target brief exists, classify each finding as:

- `transfer`: a product-agnostic principle worth carrying forward.
- `transform`: a useful pattern that must change for the new audience, task, or platform.
- `reject`: source identity, copyrighted expression, dark pattern, or irrelevant mechanism.

For every recommendation, include the source principle, target decision, rationale, and meaningful difference from the reference. Do not reuse proprietary character designs, distinctive layouts, branded copy, illustration systems, or trade dress.

### 7. Produce the analysis package

Create these artifacts when the user requests files or the task is part of a larger design workflow:

- `analysis-report.md`: evidence, observations, inferences, mechanics, UX findings, and adaptation decisions.
- `design.md`: concise rules another designer or coding agent can follow.
- `design-dna.json`: structured handoff conforming to [references/design-dna-schema.md](references/design-dna-schema.md).

Use [assets/design-md-template.md](assets/design-md-template.md) as the `design.md` structure. Use [assets/design-dna-template.json](assets/design-dna-template.json) as the JSON starting point. Remove unused optional fields instead of filling them with guesses.

When `design-dna.json` is created as a file, run `python3 scripts/validate_design_dna.py <path-to-design-dna.json>` and fix every error before delivery. Treat warnings as explicit review prompts.

When responding only in conversation, preserve the same section order but do not create unnecessary files.

## Apply evidence discipline

- Cite screenshot IDs next to claims, not only in a source appendix.
- State `unknown` instead of inventing unavailable behavior.
- Mark approximate visual values as estimates and use ranges where appropriate.
- Treat store metrics, rankings, reviews, pricing, and current features as time-sensitive.
- Treat screenshots as a state sample, not proof of the complete product flow.
- Do not infer animation timing from static screenshots.
- Do not infer accessibility support solely from visual appearance.
- Do not claim compliance without contrast, target-size, dynamic-type, or assistive-technology checks.
- Explain disagreements between sources and prefer the most recent first-party evidence.

## Enforce the output contract

Include, in order:

1. Executive summary.
2. Evidence inventory and coverage gaps.
3. Product mechanics.
4. UX and platform patterns.
5. Visual Design DNA.
6. Transfer, transform, and reject decisions.
7. Target-product recommendations when requested.
8. Confidence and unanswered questions.

Make every recommendation actionable. Specify the affected screen or component, intended behavior, reason, and acceptance signal.

## Run the quality gate

Read [references/analysis-rubric.md](references/analysis-rubric.md) and score the draft before completing it. Revise when any blocking criterion fails.

Do not complete the analysis until:

- Important claims trace to evidence.
- Observation, inference, and recommendation remain distinct.
- Product mechanics are not reduced to visual adjectives.
- Exact values are verified or marked as estimates.
- Adaptation changes the expression enough to avoid cloning.
- Platform differences and missing states are explicit.
- Accessibility findings distinguish visible risk from tested fact.
