---
name: opinionated-ios26-design
description: Design, build, or refine native iOS and iPadOS apps for iOS 26 with Apple-like product judgment, restrained Liquid Glass, complete interaction states, and maintainable Swift. Use for new app ideas, screen or flow implementation, and focused visual or interaction polish in existing Apple-platform apps; do not use for non-Apple frontends.
---

# Opinionated iOS 26 Design

Create a real product that feels at home beside Apple's apps: clear, content-led, calm, responsive, and complete. Apple-like quality comes from structure, behavior, and attention to detail, not from copying an Apple screen or applying a fashionable effect.

## Start from the product

- Treat the user's request and the current codebase as the source of truth. Preserve explicit copy, symbols, behavior, appearance, and architecture unless the task changes them.
- Understand the audience, the app's primary job, its main content, and the deployment target before choosing a layout or API.
- For a loose new idea, infer the smallest coherent product: one clear core loop, a useful first screen, and only the destinations and settings that loop needs.
- For an existing app, make the narrowest change that fully solves the request. Extend its visual language instead of introducing a parallel one.
- Do not invent features, sample content, onboarding, tabs, metrics, or explanatory screens to make an unfinished app look full.

## Design like an Apple app

- Choose information architecture before decoration. Each screen should have an obvious purpose, a readable hierarchy, and a clear next action.
- Prefer native app structures and controls. Use `NavigationStack`, `NavigationSplitView`, `TabView`, toolbars, sheets, menus, lists, forms, and system presentations according to their intended roles.
- Keep content in the foreground and controls in a quieter functional layer. Reveal secondary actions progressively instead of displaying every option at once.
- Build hierarchy with alignment, spacing, typography, scale, and grouping before adding containers. Not every section needs a card, background, border, or heading.
- Keep navigation predictable. Preserve context and selection, place actions near what they affect, and let system back, cancel, dismiss, and keyboard behavior work naturally.
- Make the first screen the actual experience, not a marketing page. Introduce the product only when setup, safety, or permission context genuinely requires it.
- Write short, concrete interface copy in the user's language. Keep terminology consistent and remove filler, repetition, fake enthusiasm, and text that merely narrates the UI.

## Use the platform as the design system

- Prefer SwiftUI and system components. Reach for UIKit when the existing architecture or a capability genuinely calls for it.
- Prefer SF Pro, text styles, SF Symbols, semantic colors, system materials, and native control states. Custom type, color, or imagery should express this product rather than decorate a generic layout.
- Let system components provide their iOS 26 appearance. Avoid rebuilding a standard control only to make it look more custom.
- Support light, dark, and increased-contrast appearances unless the product intentionally establishes a narrower appearance. Respect Dynamic Type, safe areas, localization, and different iPhone and iPad sizes.
- Give controls comfortable hit regions, normally at least 44 by 44 points, without making every visible element oversized.
- Use color and tint to communicate identity, status, selection, or action. Do not rely on color alone, and do not default to a purple-blue palette, gradients, glows, or decorative blobs.

## Treat Liquid Glass as structure

- Liquid Glass belongs primarily to navigation and controls floating above content. It is not the content layer, a background theme, or a material for every card.
- Adopt standard iOS 26 components first; they receive the correct glass behavior, grouping, motion, and adaptivity from the system.
- Add custom glass only to a small number of important floating controls. Keep regular glass quiet, reserve prominence and tint for meaning, and keep nearby glass elements visually coordinated.
- Remove custom bar backgrounds, stacked blur layers, strokes, and shadows that compete with system glass or scroll-edge effects.
- Keep the resting interface calm. Glass and motion may come alive through interaction, but content should remain the visual anchor.

## Finish the interaction, not just the screenshot

- Every visible control must do what it implies. Complete navigation, cancel and save paths, selection, focus, keyboard dismissal, validation, and destructive confirmations.
- Account for the states the feature can actually enter: initial, loading, content, empty, partial, disabled, permission denied, failure, offline, saving, and success. Use only the states relevant to the feature.
- Give immediate, causal feedback. Keep motion brief and interruptible; respect Reduce Motion and Reduce Transparency. Use haptics and sound sparingly and semantically.
- Ask for protected access when its purpose is clear, explain the benefit in plain language, and handle denial without trapping the person.
- Make custom controls understandable to VoiceOver, expose useful labels and values, preserve logical focus order, and never use gesture, color, sound, or animation as the only signal.

## Prevent generated-app slop

Reject statistically average UI that is plausible at a glance but has no product reason behind it. In particular, avoid:

- a dashboard or grid of rounded cards for a simple single-purpose app
- a giant title, greeting, or hero that pushes the useful interface below the fold
- glass on content, nested cards, excessive pills, ornamental badges, and repeated section chrome
- gradients, glow, noise, arbitrary accent colors, emoji, or SF Symbols used as decoration
- prompt-like instructions, "Welcome" copy, fake testimonials, invented statistics, and placeholder tabs
- bespoke navigation, input, toggles, alerts, and sheets that behave worse than the system versions
- hard-coded layouts that only fit one device, one text size, or one appearance
- duplicate models, view styles, helper layers, and design tokens instead of reusing what the project already has
- dead controls, fake async work, swallowed errors, sample data leaking into production, abandoned TODOs, and code that only makes a preview look populated

When revising generated work, remove the superseded effect or implementation. Do not keep layering modifiers, containers, compatibility branches, and fallback UI until the original problem is impossible to see.

## Completion bar

Before calling the work complete, make sure:

- the primary user goal works end to end, not only in the ideal state
- visual hierarchy, wording, symbols, and interaction conventions are consistent across the changed surface
- layouts remain usable with realistic content, larger text, keyboards, safe areas, and supported window sizes
- state ownership and data flow have one clear source of truth, and asynchronous work cannot leave stale UI behind
- the change fits the existing architecture and leaves no redundant scaffolding, placeholders, or debug artifacts
- any unobserved visual, device, permission, audio, haptic, camera, or location behavior is described honestly rather than claimed as verified

## Read the relevant reference

- For a new app, navigation rethink, or screen hierarchy, read [product-design.md](references/product-design.md).
- For iOS 26 structure, toolbars, tabs, search, sheets, or custom glass, read [liquid-glass.md](references/liquid-glass.md).
- For forms, states, permissions, motion, feedback, copy, accessibility, or adaptivity, read [interaction-and-accessibility.md](references/interaction-and-accessibility.md).
- For SwiftUI architecture, state, persistence, async work, or an anti-slop code review, read [implementation-quality.md](references/implementation-quality.md).
