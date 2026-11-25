---
name: translating-mobile
description: Use when applying shared mobile-localization constraints for mobile UI, accessibility strings, screenshots, expansion, truncation, and pseudo-localization.
---

# Translating Mobile

## Overview

Define the engineering contract shared by mobile platforms. Preserve resource semantics and rendering behavior while routing target wording to `translating-core` and installed language or script specialists.

Do not produce unapproved target copy before the orchestrator confirms project setup. This skill is not a linguistic generator.

## Capabilities

- `surface:mobile`
- `mobile-ui`
- `accessibility`
- `pseudo-localization`

## Inspect the Mobile Context

Create a string inventory before translation. For every entry record:

- stable resource key, source text, target locale, platform, screen, component, and UI state
- short-string context: the action or meaning behind terse labels such as “Back,” “Done,” or “Send”
- visible role, accessibility role, neighboring copy, icon meaning, and whether reuse across roles is intentional
- placeholder names, types, examples, runtime formatting owner, markup, and protected terms
- available width and height, wrapping and line limits, dynamic-text behavior, smallest and largest supported device sizes
- screenshot or annotated mock for the relevant state, including LTR or RTL direction when applicable

If a terse source, reused key, or state is ambiguous, return a focused context question to the orchestrator. Never guess target meaning from the key name alone.

## Preserve the Resource Contract

Keep keys, placeholders, types, escapes, markup, identifiers, URLs, product facts, and runtime values unchanged. Format numbers, dates, currency, and units at runtime under the explicit target locale; do not bake sample values into copy.

Send only user-facing prose to core with its complete inventory entry. Allow the installed language specialist to choose grammar, word order, and locale mechanics. Allow the platform specialist to refine resource syntax and platform tests. Reinsert approved wording without changing resource identity or executable structure.

Create distinct visible and accessibility resources when their purposes require different wording. Do not force a compact visual label to serve as a complete screen-reader announcement.

## Shared Mobile Constraints

- Treat expansion as a layout input, not a reason to abbreviate meaning. Prefer adaptable layout, wrapping, or responsive variants before requesting shorter copy.
- Treat truncation, clipping, overlap, hidden controls, and unreadable scaling as defects. Do not silently add ellipses to required actions or status information.
- Test content-driven sizing, orientation, safe areas, keyboard states, dynamic text or font scaling, and the supported device-size range.
- Use logical start/end layout behavior. Route bidirectional content and mirroring decisions to the installed script specialist rather than inserting directional characters by guesswork.
- Keep screenshots tied to resource key, screen state, locale, platform, device class, and build. A screenshot is context and QA evidence, not authorization to infer missing product meaning.
- Run pseudo-localization before linguistic QA: expanded/accented LTR, forced RTL, placeholder preservation, and fallback exposure. Pseudo-localization validates engineering; it is not target copy.
- Test screen-reader names, hints, values, announcements, reading and focus order, touch targets, and text scaling with VoiceOver or TalkBack as applicable.

## Targeted Research

Use bundled and project knowledge by default. Research only a specific unresolved current platform behavior after project configuration and pinned knowledge are insufficient. Prefer authoritative platform documentation, record the decision through the orchestrator, and do not research ordinary wording or grammar.

Never install or download another skill during a translation task.

## Authority Boundary

Follow explicit user requirements, approved project configuration, and core semantic fidelity before mobile layout preferences. Product owns meaning and state; engineering owns resource and runtime contracts; accessibility ownership supplies interaction intent.

This skill owns shared mobile context, protected resource boundaries, layout constraints, and mobile QA. Core owns target meaning and copy; language or script specialists own linguistic mechanics; iOS, Android, or Flutter specialists own platform syntax and behavior; `reviewing-translations` owns final review.

## QA Handoff and Release Gates

Always perform file and structural checks, including:

- keys, placeholders, markup, facts, protected terms, and runtime values preserve parity
- every customer-facing string in the release locale is intentionally localized or explicitly approved to remain; accidental mixed-language output blocks release

Perform the following runtime checks only after the orchestrator supplies a resolved `run` decision. Use the smallest relevant runtime scope for the affected resources and states; do not independently choose the runtime-review budget or expand it to the whole application:

- screenshots cover relevant states, device sizes, text scales, orientations, and LTR or RTL direction
- pseudo-localization exposes no fixed-width assumptions, fallback strings, broken placeholders, clipping, overlap, or inaccessible controls
- visible and accessibility copy preserve their distinct purpose, and announcements occur in the correct state
- approved target copy renders without truncation or meaning loss on every supported platform and required layout

Pass source and target resources, locale pair, inventories, available screenshots, supported device matrix, accessibility intent, build identifier, and applicable results to `reviewing-translations`.

Always block release on resource corruption, accidental mixed-language content, placeholder or runtime-format damage, or unresolved short-string ambiguity. When runtime review runs, also block on unintended fallback language, lost accessibility meaning, or required content hidden by layout. Route the smallest affected resource and evidence to its responsible installed skill.
