---
name: accessibility-review
description: Audit UI for keyboard navigation, focus order, screen-reader labels, color contrast, motion preferences, and ARIA correctness against WCAG 2.2 criteria (including Focus Not Obscured 2.4.11, Target Size 2.5.8, Accessible Authentication 3.3.8, Dragging Movements 2.5.7, Redundant Entry 3.3.7). Use automated CI gates via @axe-core/playwright for regression detection alongside manual screen-reader testing. Use when validating user-facing flows before release, after design specs land, or when fixing reported a11y defects.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Accessibility Review

Use this skill with **QA Engineer**, **Frontend Developer**, or **UI/UX Designer** when accessibility conformance must be verified explicitly.

## When to Use

- validating user-facing flows before release
- after design specs land
- fixing reported a11y defects
- running @axe-core/playwright gates + screen-reader checks

## Core Rules

- target WCAG 2.2 Level AA as the default baseline unless the repo documents a different bar; WCAG 2.2 AA is a superset of 2.1 AA, so a 2.1 AA obligation is satisfied by meeting 2.2 AA
- confirm which conformance target actually binds the project before reporting: regulatory regimes lag the latest WCAG release (see the regulatory note below)
- **CI gate mandate**: all PR builds must run `new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag22a', 'wcag22aa']).analyze()` and fail CI if `violations.length > 0` — automated axe scans catch ~30–50% of defects; pair with manual keyboard-only and screen reader testing
- use WAI-ARIA Authoring Practices Guide (APG) 2.2 keyboard interaction patterns as the authoritative reference for widget types (combobox, dialog, menu, tabs, tree) — do not invent ad-hoc keyboard patterns
- audit the Success Criteria added in WCAG 2.2 at Level A/AA:
  - **3.3.8 Accessible Authentication (AA)**: Ensure cognitive function tests (such as memorizing passwords/usernames or solving puzzles) are not required for login processes without alternatives. (3.3.9 is the AAA variant — out of scope for an AA baseline.)
  - **3.3.7 Redundant Entry (A)**: Avoid requiring users to re-enter information previously entered in the same process; instead, auto-populate or provide selectable choices.
  - **2.4.11 Focus Not Obscured (Minimum) (AA)**: Verify the focused component is not entirely hidden by author-created content such as sticky headers, cookie banners, or floating chat widgets. (2.4.12 Focus Not Obscured (Enhanced) is AAA.)
  - **2.4.13 Focus Appearance (AAA)**: Focus indicator minimum area and 3:1 contrast against adjacent colors. This is **Level AAA** — report it as an enhancement, not an AA failure.
  - **2.5.7 Dragging Movements (AA)**: Provide a single-pointer alternative (e.g. click/tap controls) for any functionality requiring dragging.
  - **2.5.8 Target Size (Minimum) (AA)**: Pointer targets are at least 24x24 CSS pixels, or meet one of the spacing/inline/essential exceptions.
- evaluate Cognitive Accessibility (COGA) requirements:
  - **Plain Language**: Keep instructions and UI labels simple and concise.
  - **Error Prevention**: Provide automatic suggestions, warnings, and clear instructions before submission.
  - **Memory Aids**: Avoid placeholder-only labels; maintain persistent context and visual cues.
- audit ARIA annotation roles and attributes on dynamic elements, treating them as progressive enhancement (WAI-ARIA 1.3 is still a Working Draft and support is uneven):
  - Use `suggestion`, `comment`, and `mark` roles for editorial markup and user feedback panels.
  - Use `aria-description` for a detailed text description, and `aria-braillelabel` / `aria-brailleroledescription` for braille readers.
  - Never rely on an annotation role as the only accessible name or state; keep a 1.2-compatible fallback.
- test keyboard-only paths for every primary task in scope; `Tab`, `Shift+Tab`, `Enter`, `Space`, `Escape` must be 100% operable with visible, non-obscured focus indicators (3:1 contrast ratio minimum)
- verify visible focus indicators and logical tab order
- ensure images, icons, and controls have accessible names (text or aria-label)
- check color contrast for text and interactive states; do not rely on color alone
- respect `prefers-reduced-motion` when animations are present
- cite concrete selectors, routes, or component names for every finding
- route visual/IA issues without a11y impact to `design-review`; route logic bugs to `review-code`

## Suggested Process

### 1. Define Scope

- routes, components, or ux-flow-spec screens in scope
- supported browsers and assistive tech assumptions from repo docs
- whether design specs already document a11y behavior

### 2. Static Spec Review

When specs exist:

- copy_per_state includes announcements for dynamic updates
- focus trap and escape behavior documented for modals
- error messages associated with fields (aria-describedby pattern)

### 3. Implementation Review

- semantic HTML landmarks (main, nav, heading order)
- form labels, grouping, and error association
- custom widgets: roles, states, keyboard handlers
- live regions for toasts and async status

### 4. Manual Checks

- tab through primary flow without mouse
- activate controls with Enter/Space where expected
- screen reader spot-check on critical path (if tooling available)

### 5. Report

List violations by severity: critical (blocks task) | serious | moderate | minor.

Recommend fix pattern, not only failure description.

### WCAG 2.2 AA Baseline

Audit these Success Criteria as the AA baseline. Levels are stated explicitly so AAA enhancements are never reported as AA failures:
- **3.3.8 Accessible Authentication (AA)**: Do not require cognitive tests (e.g., copy-paste blocks, security questions, puzzles) for authentication without a mechanism that does not require one or provides support.
- **3.3.7 Redundant Entry (A)**: Previously entered data in a single multi-step workflow must be auto-populated or selectable (except for security/re-verification inputs).
- **2.4.11 Focus Not Obscured (Minimum) (AA)**: The focused component must not be entirely hidden by author-created content (sticky headers, banners, floating widgets).
- **2.5.7 Dragging Movements (AA)**: Provide click or tap alternatives for dragging functions (e.g. sliders, canvas manipulation).
- **2.5.8 Target Size (Minimum) (AA)**: Pointer targets at least 24x24 CSS px unless a spacing, inline, or essential exception applies.
- **2.4.13 Focus Appearance (AAA)**: Focus indicator minimum area and 3:1 contrast. Report as an enhancement.

### Regulatory Baseline (verify before citing)

Regulatory obligations lag the latest WCAG release. State which version actually binds the project rather than assuming 2.2:
- **ISO/IEC 40500:2025** ratifies **WCAG 2.2** as an international standard.
- **EU European Accessibility Act** has applied since **28 June 2025**; the harmonised standard is **EN 301 549**, whose current version maps to **WCAG 2.1 AA**. The update to WCAG 2.2 is still pending, so do not cite the EAA as a WCAG 2.2 mandate.
- **US DOJ ADA Title II final rule** specifies **WCAG 2.1 AA** and binds state and local government entities only. An interim final rule issued **20 April 2026** extended the compliance deadline to **26 April 2027** (2028 for small entities). It is not a WCAG 2.2 driver.

Targeting 2.2 AA still satisfies all of the above, because 2.2 AA is a superset of 2.1 AA. Cite the binding regime accurately when justifying the bar.

### 2026: Cognitive Accessibility (COGA)
Design and review UIs with COGA guidelines to assist users with cognitive and learning disabilities:
- **Plain Language**: Avoid jargon, keep paragraphs short, and structure text logically.
- **Error Prevention**: Provide contextual help, input format suggestions, and clear error notifications with actionable recovery steps.
- **Memory Aids**: Display persistent labels, ensure context remains visible across steps, and do not rely on short-term memory (e.g. keep instructions visible during input).

### ARIA Annotations (progressive enhancement)

WAI-ARIA 1.3 is a Working Draft and these annotation roles are still marked proposed by implementers. Use them additively, never as the sole carrier of a name, role, or state:
- **suggestion**: Use to mark up proposed additions or deletions in collaborative text fields.
- **comment**: Use to identify user-submitted commentary, annotations, or discussion threads.
- **mark**: Use to indicate text marked or highlighted for relevance or reference.
- **aria-description**: Provide an explicit descriptive string to assistive devices without needing an ID reference.
- **aria-braillelabel** and **aria-brailleroledescription**: Provide braille-optimized label and role description text. These are the only two braille ARIA attributes that exist — there is no `aria-braillevaluedescription`.

## Checklist

- [ ] scope routes/components listed
- [ ] keyboard path completes primary user task
- [ ] focus order is logical and focus visible
- [ ] interactive elements have accessible names
- [ ] images and icons have alt text or are marked decorative
- [ ] color contrast checked for text and controls
- [ ] motion respects reduced-motion preference when applicable
- [ ] findings tied to files or components with severity
- [ ] WCAG 2.2 A/AA new SCs verified (Accessible Auth 3.3.8, Redundant Entry 3.3.7, Focus Not Obscured 2.4.11, Dragging Movements 2.5.7, Target Size 2.5.8)
- [ ] AAA items (2.4.13 Focus Appearance) reported as enhancements, not AA failures
- [ ] binding regulatory target confirmed (EN 301 549 / DOJ Title II map to WCAG 2.1 AA; ISO/IEC 40500:2025 maps to 2.2)
- [ ] Cognitive accessibility (COGA) principles (plain language, error prevention, memory aids) reviewed
- [ ] ARIA annotation roles (suggestion, comment, mark) and attributes (aria-description, aria-braillelabel, aria-brailleroledescription) verified as additive only

## Failure Modes

- **A11y regression undetected**: a UI change introduces a contrast or focus issue. **Mitigation:** run axe-core on every component; surface findings as blocking; require human review for components that fail.
- **WCAG version drift**: the review references a deprecated WCAG criterion. **Mitigation:** validate every reference against the current WCAG version; surface the drift in the review.
- **Screen reader not tested**: a component passes automated checks but fails screen reader. **Mitigation:** require a manual screen reader pass on critical components; surface the missing test in the review.
- **Color-only signal**: a component conveys state by color alone. **Mitigation:** require an alternative signal (icon, text, ARIA); reject components with color-only state.

## Output Contracts

When the a11y review produces a structured handoff (CI gate, pre-merge
audit, or multi-role delivery), emit:

- **`contracts/schemas/code-review-finding.json`** adapted for a11y: each finding gets a `severity`, an `owner` (Frontend or QA), a `category` (perceivable, operable, understandable, robust), and the WCAG criterion.
- For human-readable reports, the markdown findings table already documented is the canonical format.

Skip emission for a single-component a11y walkthrough that does not cross a role boundary.

## Security Guardrails (OWASP ASI)

- **ASI07 Inter-Agent Communication**: a11y findings are consumed by Frontend and QA; emit a structured contract so each role can validate.
- **ASI09 Human-Agent Trust Exploitation**: do not present a component as "WCAG-compliant" without the actual scan output; surface the residual risk honestly.

## Related Skills

- **design-ux-flow**: Add a11y notes to specs when gaps found early
- **design-review**: Visual hierarchy and pattern consistency
- **frontend-testing**: Automate regression tests for a11y fixes
- **review-code**: Broader code review including non-a11y risks
- **write-tests**: Add axe or similar checks when repo supports them
