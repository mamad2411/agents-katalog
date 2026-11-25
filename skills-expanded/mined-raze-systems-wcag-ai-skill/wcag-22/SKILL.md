---
name: wcag-22
description: "Design, review, and document web experiences against WCAG 2.2. Use for web pages, SPAs, design systems, forms, dashboards, navigation, media, content, accessibility audits, conformance planning, remediation, and QA. Produces guidelines, requirements, acceptance criteria, and test plans, not pre-made components or legal certification."
license: "AGPL-3.0"
metadata:
  version: "0.1"
  domain: "web accessibility"
  standard: "WCAG 2.2"
---

# WCAG 2.2 Web Design

## Overview

Use this skill to translate WCAG 2.2 into web design, content, interaction, and frontend guidance. WCAG is the baseline, not the ceiling: aim for perceivable, operable, understandable, and robust experiences across permanent, temporary, and situational disabilities.

Use the W3C WCAG 2.2 Recommendation as the normative source. Use practical guides, prior markdown references, and organizational standards as implementation aids only when they do not conflict with the normative WCAG text.

This skill is for requirements, audits, design review, remediation planning, QA, acceptance criteria, and accessibility documentation. It is not legal advice, medical advice, or a formal certification of conformance.

## Hard Boundaries

Do not offer pre-made components, drop-in widgets, or full component libraries. When a user asks for a component, provide guidelines: semantic structure, states, labels, focus behavior, keyboard behavior, content requirements, responsive behavior, acceptance tests, and WCAG criteria. Code snippets are allowed only to illustrate a rule or anti-pattern, not as a reusable component package.

Do not treat automated testing, overlays, linting, or visual inspection as sufficient. Automated tools can support review, but conformance requires manual inspection and, where possible, testing with assistive technologies and people with disabilities.

Do not use ARIA to repair avoidable semantic problems. Prefer native HTML and browser behavior first. Add ARIA only when native semantics cannot express the needed name, role, state, property, or relationship.

## Activation Triggers

Use this skill when the user asks about WCAG 2.2, accessibility, inclusive web design, accessible UX/UI, frontend accessibility, design systems, forms, navigation, dashboards, media, errors, authentication, focus, keyboard behavior, responsive design, SPAs, conformance claims, accessibility statements, or accessibility QA.

## Core Response Protocol

First identify the product surface: page, flow, component behavior, content type, media, document, design token, or system policy. Then identify the target level: A, AA, AAA, or a higher internal quality bar.

For any substantive recommendation, name the relevant WCAG criteria by number and title when useful. Keep wording practical: what must be perceived, understood, operated, or exposed programmatically.

For design or remediation work, produce guidance in this order: user impact, applicable criteria, design requirement, implementation requirement, interaction states, test method, and known edge cases.

For audits, distinguish failures from improvements. A failure blocks the declared target level. An improvement may go beyond the target level, reduce risk, or support users whose needs are not fully covered by WCAG.

## Conformance Model

WCAG 2.2 has 86 active success criteria: 31 at Level A, 24 additional at Level AA, and 31 additional at Level AAA. Level AA means all Level A and Level AA criteria are met. Level AAA means all A, AA, and AAA criteria are met.

Conformance applies to full web pages, all responsive and state variants, and complete processes. A checkout, onboarding flow, application form, authentication journey, or multi-page wizard cannot claim conformance if one step in the process fails.

Use only accessibility-supported technologies for relied-upon content and functionality. If non-supported or non-conforming technology is present, it must not block the rest of the page.

Always enforce non-interference: 1.4.2 Audio Control, 2.1.2 No Keyboard Trap, 2.2.2 Pause Stop Hide, and 2.3.1 Three Flashes or Below Threshold must not prevent access to the page, even for content not relied upon for conformance.

4.1.1 Parsing is obsolete and removed in WCAG 2.2. Valid, well-formed code remains a best practice because it reduces implementation and assistive-technology risk, but do not count 4.1.1 as an active WCAG 2.2 criterion.

## WCAG 2.2 Surface Map

1. Perceivable: information and interface components must be presentable in ways users can perceive.

- 1.1 Text Alternatives: 1.1.1 Non-text Content.
- 1.2 Time-based Media: 1.2.1 Audio-only and Video-only (Prerecorded), 1.2.2 Captions (Prerecorded), 1.2.3 Audio Description or Media Alternative (Prerecorded), 1.2.4 Captions (Live), 1.2.5 Audio Description (Prerecorded), 1.2.6 Sign Language (Prerecorded), 1.2.7 Extended Audio Description (Prerecorded), 1.2.8 Media Alternative (Prerecorded), 1.2.9 Audio-only (Live).
- 1.3 Adaptable: 1.3.1 Info and Relationships, 1.3.2 Meaningful Sequence, 1.3.3 Sensory Characteristics, 1.3.4 Orientation, 1.3.5 Identify Input Purpose, 1.3.6 Identify Purpose.
- 1.4 Distinguishable: 1.4.1 Use of Color, 1.4.2 Audio Control, 1.4.3 Contrast (Minimum), 1.4.4 Resize Text, 1.4.5 Images of Text, 1.4.6 Contrast (Enhanced), 1.4.7 Low or No Background Audio, 1.4.8 Visual Presentation, 1.4.9 Images of Text (No Exception), 1.4.10 Reflow, 1.4.11 Non-text Contrast, 1.4.12 Text Spacing, 1.4.13 Content on Hover or Focus.

2. Operable: interface components and navigation must be operable.

- 2.1 Keyboard Accessible: 2.1.1 Keyboard, 2.1.2 No Keyboard Trap, 2.1.3 Keyboard (No Exception), 2.1.4 Character Key Shortcuts.
- 2.2 Enough Time: 2.2.1 Timing Adjustable, 2.2.2 Pause Stop Hide, 2.2.3 No Timing, 2.2.4 Interruptions, 2.2.5 Re-authenticating, 2.2.6 Timeouts.
- 2.3 Seizures and Physical Reactions: 2.3.1 Three Flashes or Below Threshold, 2.3.2 Three Flashes, 2.3.3 Animation from Interactions.
- 2.4 Navigable: 2.4.1 Bypass Blocks, 2.4.2 Page Titled, 2.4.3 Focus Order, 2.4.4 Link Purpose (In Context), 2.4.5 Multiple Ways, 2.4.6 Headings and Labels, 2.4.7 Focus Visible, 2.4.8 Location, 2.4.9 Link Purpose (Link Only), 2.4.10 Section Headings, 2.4.11 Focus Not Obscured (Minimum), 2.4.12 Focus Not Obscured (Enhanced), 2.4.13 Focus Appearance.
- 2.5 Input Modalities: 2.5.1 Pointer Gestures, 2.5.2 Pointer Cancellation, 2.5.3 Label in Name, 2.5.4 Motion Actuation, 2.5.5 Target Size (Enhanced), 2.5.6 Concurrent Input Mechanisms, 2.5.7 Dragging Movements, 2.5.8 Target Size (Minimum).

3. Understandable: information and operation must be understandable.

- 3.1 Readable: 3.1.1 Language of Page, 3.1.2 Language of Parts, 3.1.3 Unusual Words, 3.1.4 Abbreviations, 3.1.5 Reading Level, 3.1.6 Pronunciation.
- 3.2 Predictable: 3.2.1 On Focus, 3.2.2 On Input, 3.2.3 Consistent Navigation, 3.2.4 Consistent Identification, 3.2.5 Change on Request, 3.2.6 Consistent Help.
- 3.3 Input Assistance: 3.3.1 Error Identification, 3.3.2 Labels or Instructions, 3.3.3 Error Suggestion, 3.3.4 Error Prevention (Legal Financial Data), 3.3.5 Help, 3.3.6 Error Prevention (All), 3.3.7 Redundant Entry, 3.3.8 Accessible Authentication (Minimum), 3.3.9 Accessible Authentication (Enhanced).

4. Robust: content must be compatible with current and future user agents and assistive technologies.

- 4.1 Compatible: 4.1.2 Name Role Value, 4.1.3 Status Messages. Treat dynamic state, accessible names, roles, values, and live updates as explicit design requirements, not late-stage developer fixes.

5. Conformance: define the claimed level, scope, technologies relied upon, complete processes, non-interference status, optional conformance claim, partial conformance limits, privacy considerations, and security considerations.

## Design and Implementation Rules

### Perceivable

Provide equivalent text for meaningful images, icons, graphical controls, data visualizations, maps, CAPTCHA, and sensory content. Mark decorative content so assistive technologies can ignore it. Complex visuals need equivalent explanation, not a vague caption.

Plan media alternatives before production. Prerecorded and live media may require transcripts, captions, audio description, media alternatives, sign-language interpretation, or extended audio description depending on level and media type.

Design semantic structure before visual layout. Headings, lists, landmarks, tables, groups, labels, and relationships must be available programmatically. The DOM reading order must preserve meaning when CSS, zoom, or viewport changes alter presentation.

Never rely on color, shape, position, size, sound, or motion alone. Pair sensory cues with text, labels, icons with accessible names, patterns, or programmatic state.

Meet contrast, reflow, resize, text-spacing, and non-text contrast requirements in tokens and layouts. Test at 200% text resize and 400% zoom or 320 CSS px width without loss of content or function, except for legitimately two-dimensional content.

### Operable

Every function must work from a keyboard. Keyboard order must match the intended reading and task order. Focus must be visible, must not be trapped, and must not be hidden behind sticky headers, overlays, drawers, cookie banners, or fixed footers.

Design focus behavior for every state transition: open, close, route change, validation, loading, error, success, insertion, deletion, sorting, filtering, pagination, modal, menu, disclosure, and toast. Return focus to a logical place after temporary UI closes.

Provide user control over time, motion, audio, auto-updating content, and interruptions. Avoid time limits. If unavoidable, allow extension, warning, saving, or recovery as required by the relevant criterion.

Avoid flashing and intense motion. Respect reduced-motion preferences. Interaction-triggered animation that is not essential must be suppressible for AAA.

Do not require fine pointer control, multi-touch, drag-only, path-based gestures, hover-only interactions, device motion, or one input mode. Provide keyboard, touch, pointer, and assistive-technology paths. Use at least 24 by 24 CSS px target sizing for AA and consider 44 by 44 CSS px for AAA or touch-heavy contexts.

### Understandable

Set page language and language changes. Write headings, labels, link text, button text, instructions, help, and error messages so users understand purpose and consequences without guessing.

Keep navigation, component identification, help locations, and repeated controls consistent. Do not trigger context changes on focus or input unless the user is warned and the behavior is expected.

For forms, use visible labels, persistent instructions, programmatic descriptions, inline errors, summaries for multi-error submissions, correction suggestions, review/confirm/undo paths for high-impact submissions, and accessible authentication that does not require memory puzzles, transcription barriers, object recognition, or user-content recognition.

Avoid redundant entry. Preserve previously entered information, allow copy and paste, support password managers, and let users continue after re-authentication without data loss.

### Robust

Expose name, role, value, state, and relationships for all controls. For native controls, verify the browser exposes the correct semantics. For custom controls, specify the exact semantic mapping and keyboard model before implementation.

Status changes that do not receive focus must still be communicated programmatically. Use polite or assertive announcements according to urgency, but do not steal focus unless the user must act immediately.

Treat SPAs and dynamic interfaces as full accessibility surfaces. Route changes, hydration, lazy loading, virtualization, client-side validation, infinite scroll, and asynchronous status updates must preserve focus order, names, relationships, and announcements.

## Web Design Deliverables

For a design review, return: issue summary, affected users, WCAG criteria, severity, remediation guidance, and acceptance tests.

For a new design, return: accessibility requirements, content requirements, state matrix, keyboard and focus behavior, responsive and zoom behavior, media alternatives, error and recovery behavior, and test plan.

For a design system, return: token requirements, component behavior specifications, state coverage, accessibility annotations, documentation requirements, and regression-test expectations. Do not provide pre-built components.

For a conformance or governance task, return: scope, target level, relied-upon technologies, page and process inventory, testing method, known limitations, claim or statement requirements, maintenance plan, and feedback mechanism.

## Evaluation Checklist

Use automated checks for detectable issues, then manually test keyboard operation, focus order, focus visibility, screen reader names and announcements, zoom/reflow, text resize, contrast, reduced motion, captions, media alternatives, form errors, authentication, responsive states, and complete task flows.

Test the same function across breakpoints, input methods, and states. Include empty, loading, error, disabled, expanded, collapsed, selected, invalid, authenticated, unauthenticated, timed-out, and post-submit states.

Prefer evidence over assumption. When possible, include people with disabilities in research and validation. Do not use simulation as a substitute for user testing.

## References

Load these files as needed. Some may be created later; the descriptions define their intended purpose and when to use them.

- [references/wcag-22-complete-checklist.md](references/wcag-22-complete-checklist.md) for a robust checklist of all 86 active WCAG 2.2 success criteria, levels, intent, design obligations, content obligations, frontend obligations, manual tests, automated-test coverage, and common failures. Use for complete audits, acceptance criteria, backlog creation, and A/AA/AAA gap analysis.
- [references/wcag-22-conformance-and-claims.md](references/wcag-22-conformance-and-claims.md) for conformance levels, full-page scope, complete processes, accessibility-supported technologies, non-interference, conformance claims, partial conformance, accessibility statements, ACR/VPAT notes, privacy, and security. Use when scoping reviews or preparing public documentation.
- [references/1.1-text-alternatives.md](references/1.1-text-alternatives.md) for text alternatives for images, icons, graphical controls, complex images, charts, maps, sensory content, CAPTCHA, decorative content, and invisible content. Use for content, UI iconography, product imagery, and data visualization reviews.
- [references/1.2-time-based-media.md](references/1.2-time-based-media.md) for transcripts, captions, live captions, audio description, media alternatives, sign-language interpretation, extended audio description, audio-only, video-only, and media-player requirements. Use for video, audio, webinars, training, livestreams, and embedded media.
- [references/1.3-adaptable-structure.md](references/1.3-adaptable-structure.md) for semantic structure, headings, tables, lists, groups, labels, DOM order, orientation, sensory instructions, autocomplete, and identifying UI purpose. Use for layouts, templates, forms, tables, and responsive reordering.
- [references/1.4-distinguishable-visual-audio.md](references/1.4-distinguishable-visual-audio.md) for color dependence, audio control, contrast, text resize, images of text, background audio, visual presentation, reflow, non-text contrast, text spacing, and hover/focus content. Use for visual design, tokens, typography, responsive design, charts, tooltips, and popovers.
- [references/2.1-keyboard-accessible.md](references/2.1-keyboard-accessible.md) for keyboard access, no keyboard traps, keyboard-only parity, single-character shortcuts, tab order, roving focus concepts, and focus return rules. Use for interactive UI, custom widgets, modals, menus, drawers, and SPA states.
- [references/2.2-enough-time-and-sessions.md](references/2.2-enough-time-and-sessions.md) for timing adjustment, pause/stop/hide, auto-updating content, interruptions, re-authentication, session expiry, timeout warnings, data preservation, and recovery. Use for carousels, feeds, dashboards, exams, forms, and authenticated applications.
- [references/2.3-seizures-motion-vestibular.md](references/2.3-seizures-motion-vestibular.md) for flashes, seizure thresholds, motion animation, vestibular risk, reduced-motion behavior, and animation governance. Use for animation, video, ads, transitions, loaders, parallax, and interaction effects.
- [references/2.4-navigable-focus-location.md](references/2.4-navigable-focus-location.md) for bypass links, landmarks, titles, focus order, link purpose, multiple ways, headings, labels, visible focus, breadcrumbs, focus obstruction, and focus appearance. Use for navigation systems, page templates, headers, footers, sidebars, search, and sticky UI.
- [references/2.5-input-modalities-targets.md](references/2.5-input-modalities-targets.md) for pointer gestures, pointer cancellation, label in name, motion actuation, target size, concurrent input mechanisms, drag alternatives, and speech-input compatibility. Use for touch, mobile, gestures, drag/drop, maps, sliders, cards, and icon buttons.
- [references/3.1-readable-content.md](references/3.1-readable-content.md) for page language, language of parts, jargon, unusual words, abbreviations, reading level, pronunciation, summaries, glossaries, and plain-language decisions. Use for product copy, help, policies, education, healthcare, finance, and multilingual content.
- [references/3.2-predictable-navigation-help.md](references/3.2-predictable-navigation-help.md) for predictable focus/input behavior, consistent navigation, consistent identification, change on request, consistent help, and interruption governance. Use for navigation, account areas, help mechanisms, settings, and repeated flows.
- [references/3.3-input-assistance-authentication.md](references/3.3-input-assistance-authentication.md) for labels, instructions, validation, error identification, suggestions, high-impact confirmations, help, redundant entry, accessible authentication, password-manager support, and recovery. Use for forms, checkout, onboarding, profile editing, login, MFA, and admin tools.
- [references/4.1-compatible-aria-status.md](references/4.1-compatible-aria-status.md) for name/role/value, accessibility API exposure, ARIA use, live regions, status messages, custom control specifications, dynamic updates, and SPA compatibility. Use for frontend implementation reviews and dynamic interfaces.
- [references/single-page-applications.md](references/single-page-applications.md) for route-change focus, document titles, announcements, hydration, lazy content, modal/drawer behavior, validation, virtualized content, and asynchronous states. Use for React, Vue, Angular, Svelte, and client-rendered applications.
- [references/design-systems-wcag.md](references/design-systems-wcag.md) for converting WCAG into design tokens, component behavior specs, state coverage, documentation, QA gates, governance, and maintenance without providing pre-made components. Use for design systems and pattern libraries.
- [references/evaluation-reporting-wcag-em.md](references/evaluation-reporting-wcag-em.md) for sampling, audit method, issue severity, evidence, test matrices, assistive-technology checks, WCAG-EM-style reporting, dashboards, and remediation backlogs. Use for formal reviews, sprint QA, and executive reporting.
- [references/privacy-security-accessibility.md](references/privacy-security-accessibility.md) for accessible security, privacy-preserving feedback, accessible CAPTCHA alternatives, authentication, sensitive announcements, data loss prevention, and security controls that do not block assistive technologies. Use for login, MFA, forms, payments, sessions, and error handling.
