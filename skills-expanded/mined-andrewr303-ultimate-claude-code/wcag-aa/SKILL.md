---
name: wcag-aa
description: Engineering rules for WCAG 2.2 Level A and AA conformance across Perceivable, Operable, Understandable, and Robust, plus distilled web-team rules. Use when building or reviewing web UI for AA compliance, answering what an A or AA criterion requires, choosing an accessible component pattern, or grounding audit findings in the standard.
license: MIT
metadata:
  author: ult-accessability
  version: "1.0.0"
---

# WCAG 2.2 Level AA

Rule bullets for all Level A and AA criteria, organized by POUR. Criterion table: [WCAG.md](../../references/WCAG.md). Production code lives in the linked patterns — this skill states rules, it does not duplicate code. Contrast ratios are measured with [contrast-color](../contrast-color/SKILL.md), never eyeballed.

Level A is the minimum; AA is the standard legal and procurement target in most jurisdictions. New-in-2.2 criteria are marked **(2.2)**. `WCAG 2.2 SC 4.1.1 (Parsing, A)` was removed in 2.2 — never cite it as a failure.

## Perceivable

### Text alternatives and media

- Every informative `<img>`, `<svg>`, icon, and canvas needs a meaningful text alternative; decorative elements take `alt=""` or `aria-hidden="true"` — `WCAG 2.2 SC 1.1.1 (Non-text Content, A)`.
- Complex images (charts, infographics) need a longer description via `aria-describedby` or adjacent text, not just a short alt — `WCAG 2.2 SC 1.1.1 (Non-text Content, A)`.
- Icon-only buttons need an accessible name (`aria-label` or visually hidden text); the icon itself is `aria-hidden` — [visually-hidden](../../references/A11Y-PATTERNS.md#visually-hidden), `WCAG 2.2 SC 1.1.1 (Non-text Content, A)`.
- Prerecorded audio-only needs a transcript; video-only needs a text or audio alternative; video with audio needs synchronized captions and audio description — `WCAG 2.2 SC 1.2.1 (Audio-only and Video-only (Prerecorded), A)`, `WCAG 2.2 SC 1.2.2 (Captions (Prerecorded), A)`, `WCAG 2.2 SC 1.2.3 (Audio Description or Media Alternative (Prerecorded), A)`.
- Live synchronized media needs live captions; prerecorded video needs a descriptive audio track — `WCAG 2.2 SC 1.2.4 (Captions (Live), AA)`, `WCAG 2.2 SC 1.2.5 (Audio Description (Prerecorded), AA)`.
- Caption quality bar: 99%+ accuracy, synced within 1s, speaker identification, non-speech audio in brackets (`[applause]`), max ~200 words/minute.

### Structure and adaptability

- Structure conveyed visually (headings, lists, table headers, labels) must also be programmatic — use semantic elements, not styled `<div>`s — `WCAG 2.2 SC 1.3.1 (Info and Relationships, A)`. Disclosure widgets follow the [accordion](../../references/A11Y-PATTERNS.md#accordion) pattern.
- DOM reading order must match logical/visual order — never fix out-of-order DOM with CSS `order` or absolute positioning — `WCAG 2.2 SC 1.3.2 (Meaningful Sequence, A)`.
- Instructions must not rely solely on shape, color, size, location, orientation, or sound ("click the green button") — `WCAG 2.2 SC 1.3.3 (Sensory Characteristics, A)`.
- Never lock orientation to portrait or landscape unless essential — `WCAG 2.2 SC 1.3.4 (Orientation, AA)`.
- Personal-data fields need standard `autocomplete` tokens (`email`, `tel`, `given-name`, …) — `WCAG 2.2 SC 1.3.5 (Identify Input Purpose, AA)`, [forms-and-errors](../../references/A11Y-PATTERNS.md#forms-and-errors).

### Distinguishable

- Color is never the only means of conveying information — pair it with text, icons, borders, or underlines (errors, required fields, link affordances) — `WCAG 2.2 SC 1.4.1 (Use of Color, A)`.
- Audio auto-playing longer than 3s needs pause/stop or independent volume control — `WCAG 2.2 SC 1.4.2 (Audio Control, A)`.
- Text contrast: 4.5:1 normal text, 3:1 large text (≥24px, or ≥18.66px bold) — `WCAG 2.2 SC 1.4.3 (Contrast (Minimum), AA)`. Measure with [contrast-color](../contrast-color/SKILL.md).
- Text must resize to 200% without clipping or loss of function — relative units, no fixed heights — `WCAG 2.2 SC 1.4.4 (Resize Text, AA)`.
- Use live text instead of text baked into images — `WCAG 2.2 SC 1.4.5 (Images of Text, AA)`.
- No two-dimensional scrolling at 320px width (400% zoom at 1280px) — responsive layouts, single column — `WCAG 2.2 SC 1.4.10 (Reflow, AA)`.
- UI boundaries, icons, and focus indicators need 3:1 against adjacent colors — `WCAG 2.2 SC 1.4.11 (Non-text Contrast, AA)`, [focus-rings](../../references/A11Y-PATTERNS.md#focus-rings).
- No clipping with line-height 1.5, letter-spacing 0.12em, word-spacing 0.16em, paragraph-spacing 2em — `WCAG 2.2 SC 1.4.12 (Text Spacing, AA)`.
- Hover/focus-revealed content must be dismissible (Esc), hoverable, and persistent — [content-on-hover](../../references/A11Y-PATTERNS.md#content-on-hover), `WCAG 2.2 SC 1.4.13 (Content on Hover or Focus, AA)`.

## Operable

### Keyboard

- All functionality operable by keyboard alone — prefer native `<button>`, `<a href>`, and form controls, which handle activation, focus, and semantics for free — `WCAG 2.2 SC 2.1.1 (Keyboard, A)`.
- Never `tabindex` greater than 0; `tabindex="0"` sparingly, `tabindex="-1"` for programmatic focus only — `WCAG 2.2 SC 2.1.1 (Keyboard, A)`.
- Focus must always be able to move away — no traps; dialogs trap intentionally and release on Esc — [modal-and-focus-trap](../../references/A11Y-PATTERNS.md#modal-and-focus-trap), `WCAG 2.2 SC 2.1.2 (No Keyboard Trap, A)`.
- Single-character shortcuts must be remappable, disableable, or require a modifier — `WCAG 2.2 SC 2.1.4 (Character Key Shortcuts, A)`.
- SPA route changes must move focus to the new content (H1 or main with `tabindex="-1"`), never leave it on the clicked nav link — `WCAG 2.2 SC 2.4.3 (Focus Order, A)`.

### Timing, motion, seizures

- Time limits must be adjustable, extendable (with warning), or disableable — `WCAG 2.2 SC 2.2.1 (Timing Adjustable, A)`.
- Moving, blinking, scrolling, or auto-updating content needs pause, stop, or hide — `WCAG 2.2 SC 2.2.2 (Pause, Stop, Hide, A)`, [reduced-motion](../../references/A11Y-PATTERNS.md#reduced-motion).
- Nothing flashes more than 3 times per second — `WCAG 2.2 SC 2.3.1 (Three Flashes or Below Threshold, A)`.

### Navigation and focus

- Skip link as the first focusable element, landing on main content — [skip-link](../../references/A11Y-PATTERNS.md#skip-link), `WCAG 2.2 SC 2.4.1 (Bypass Blocks, A)`.
- Every page needs a descriptive unique `<title>`, updated on SPA route changes — `WCAG 2.2 SC 2.4.2 (Page Titled, A)`.
- Tab order preserves meaning and operability — no erratic jumps; modals move focus in and return it on close — `WCAG 2.2 SC 2.4.3 (Focus Order, A)`.
- Link purpose clear from text or programmatic context — no bare "click here" / "read more" — `WCAG 2.2 SC 2.4.4 (Link Purpose (In Context), A)`.
- More than one way to locate pages (nav plus search or sitemap) — `WCAG 2.2 SC 2.4.5 (Multiple Ways, AA)`.
- Headings and labels descriptive, not generic filler — `WCAG 2.2 SC 2.4.6 (Headings and Labels, AA)`.
- Every interactive element shows a visible focus indicator — never bare `outline: none`; use `:focus-visible` — [focus-rings](../../references/A11Y-PATTERNS.md#focus-rings), `WCAG 2.2 SC 2.4.7 (Focus Visible, AA)`.
- **(2.2)** Focused element never entirely hidden by sticky headers, footers, banners, or drawers — [scroll-margin](../../references/A11Y-PATTERNS.md#scroll-margin), `WCAG 2.2 SC 2.4.11 (Focus Not Obscured (Minimum), AA)`.

### Input modalities

- Multipoint/path gestures need single-pointer alternatives (e.g. +/− buttons) — `WCAG 2.2 SC 2.5.1 (Pointer Gestures, A)`.
- Actions fire on the up-event so users can abort by moving the pointer away — `WCAG 2.2 SC 2.5.2 (Pointer Cancellation, A)`.
- Accessible names must contain the visible label text (voice-control match) — `WCAG 2.2 SC 2.5.3 (Label in Name, A)`.
- Shake/tilt-triggered actions need a UI alternative and a disable option — `WCAG 2.2 SC 2.5.4 (Motion Actuation, A)`.
- **(2.2)** Every drag operation needs a single-pointer alternative: up/down buttons, click-to-move, keyboard controls — [dragging-alternative](../../references/A11Y-PATTERNS.md#dragging-alternative), `WCAG 2.2 SC 2.5.7 (Dragging Movements, AA)`.
- **(2.2)** Targets ≥ 24×24 CSS px, or spaced so 24px circles centered on them do not overlap (inline/essential exceptions) — [target-size](../../references/A11Y-PATTERNS.md#target-size), `WCAG 2.2 SC 2.5.8 (Target Size (Minimum), AA)`.

## Understandable

### Language and predictability

- `<html lang="…">` declares the default language (valid BCP 47 tag) — `WCAG 2.2 SC 3.1.1 (Language of Page, A)`.
- Language changes marked inline (`<span lang="…">`); RTL documents use `dir="rtl"`, user-generated content `dir="auto"`, isolated runs `<bdi>` — `WCAG 2.2 SC 3.1.2 (Language of Parts, AA)`.
- Focusing a control never triggers an unexpected context change — `WCAG 2.2 SC 3.2.1 (On Focus, A)`.
- Changing an input never auto-submits or redirects without prior warning — `WCAG 2.2 SC 3.2.2 (On Input, A)`.
- Repeated navigation appears in the same relative order on every page — `WCAG 2.2 SC 3.2.3 (Consistent Navigation, AA)`.
- Same functionality uses the same labels/icons everywhere — `WCAG 2.2 SC 3.2.4 (Consistent Identification, AA)`.
- **(2.2)** Repeated help mechanisms (contact, chat, docs) appear in the same relative order on every page — `WCAG 2.2 SC 3.2.6 (Consistent Help, A)`.

### Input assistance

- Errors described in text, identifying the field and reason — not color alone — [forms-and-errors](../../references/A11Y-PATTERNS.md#forms-and-errors), `WCAG 2.2 SC 3.3.1 (Error Identification, A)`.
- Every input has an explicit associated `<label>`; placeholders are never labels; format requirements stated up front — `WCAG 2.2 SC 3.3.2 (Labels or Instructions, A)`.
- Errors suggest corrections when the expected format is known — `WCAG 2.2 SC 3.3.3 (Error Suggestion, AA)`.
- Consequential submissions (legal, financial, data) are reversible, verified, or confirmed before finalizing — `WCAG 2.2 SC 3.3.4 (Error Prevention (Legal, Financial, Data), AA)`.
- **(2.2)** Previously entered information is auto-populated or selectable — no retyping across multi-step flows (security re-confirmation excepted) — `WCAG 2.2 SC 3.3.7 (Redundant Entry, A)`.
- **(2.2)** Login requires no cognitive-function test unless an alternative exists: allow paste/autofill, offer passkeys/magic links, never a puzzle or CAPTCHA as the only path — [auth-and-paste-friendly-inputs](../../references/A11Y-PATTERNS.md#auth-and-paste-friendly-inputs), `WCAG 2.2 SC 3.3.8 (Accessible Authentication (Minimum), AA)`.

## Robust

- First rule of ARIA: native HTML first — `<button>` beats `<div role="button">`, `<dialog>` beats `<div role="dialog">`. Never add redundant roles to `header`, `nav`, `main`, `footer`, `button`, `a[href]`, `checkbox`, or `select` — `WCAG 2.2 SC 4.1.2 (Name, Role, Value, A)`.
- Custom controls must expose name, role, and state (`aria-expanded`, `aria-checked`, `aria-selected`, `aria-disabled`) — [combobox](../../references/A11Y-PATTERNS.md#combobox), [tabs](../../references/A11Y-PATTERNS.md#tabs), [accordion](../../references/A11Y-PATTERNS.md#accordion), `WCAG 2.2 SC 4.1.2 (Name, Role, Value, A)`.
- Status updates announced via `role="status"` / `aria-live` without moving focus — polite for routine updates, assertive only for errors and critical alerts — [live-regions-and-toasts](../../references/A11Y-PATTERNS.md#live-regions-and-toasts), `WCAG 2.2 SC 4.1.3 (Status Messages, AA)`.

## Web-team rules (distilled)

Specialist guidance condensed to the rules that apply to web work:

- **Keyboard:** trace tab order start to finish — matches visual layout, nothing skipped, skip link first. Grep for `tabindex="[1-9]` and bare `outline: none` — both almost always wrong.
- **ARIA:** incorrect ARIA is worse than no ARIA — it actively breaks screen readers. Multiple `<nav>`s need distinct `aria-label`s. Trigger buttons get `aria-haspopup="dialog"`.
- **Modals:** always native `<dialog>` unless a documented constraint forbids it. Focus landing: least destructive action for confirmations, static content (`tabindex="-1"`) for complex dialogs, first focusable element by default; always return focus to the trigger.
- **Forms:** explicit `for`/`id` labels always (clicking a `<label>` activates its control — `aria-label` does not). `aria-label` only when a visible label genuinely cannot exist. Group related controls in `<fieldset>`/`<legend>`. Move focus to the first error on submit.
- **Tables:** every data table needs `<caption>`, `<th scope="col|row">`, and `aria-sort` on sortable columns. Never layout tables. Merged cells and virtual scrolling need manual screen-reader verification.
- **Links:** rewrite "click here / here / read more / learn more / more / details / go" as purpose-descriptive text. Warn when a link opens a new tab (visually hidden suffix); flag non-HTML targets.
- **Headings/landmarks:** one H1 per page, no skipped levels, `header`/`nav`/`main`/`footer` present. Page titles unique and descriptive.
- **Media players:** play/pause exposes state in its name, volume/seek are sliders with values, captions toggle uses `aria-pressed`, state changes announce via a polite live region.
- **i18n:** logical CSS properties (`margin-inline-start`, not `margin-left`) so RTL flips correctly; directional icons mirror, non-directional stay; email/url/tel inputs stay LTR inside RTL forms.
- **Data visualization:** every chart ships a data-table or text alternative; SVG gets `role="img"` + `aria-label` (static) with keyboard interaction for interactive charts; palettes CVD-safe with labels/patterns beyond color; adjacent series 3:1.
- **Email (HTML mail):** layout tables take `role="presentation"`; all styles inline, 14px minimum, 1.5 line-height; bulletproof buttons; alt text with image-blocking fallbacks. Gmail/Yahoo strip ARIA — semantic HTML alone must carry meaning.
- **Performance conflicts:** skeleton screens are `aria-hidden` with `aria-busy` on the container; lazy images keep `alt` and sized placeholders (no CLS shove of focused elements); infinite scroll always ships a "Load more" button; core content works without JS.
- **Cognitive load:** plain language, one idea per step in wizards, inline definitions for jargon, warnings before timeouts that could lose data, no auto-advance without user control.
- **Mobile web:** same criteria, touch-first — 24px AA targets minimum, no hover-only content, orientation unlocked, pinch-zoom never disabled (`maximum-scale=1` is a failure).

## Anti-patterns (never ship)

`outline: none` without a replacement · positive `tabindex` · placeholder as label · blocked paste in password/OTP fields · CAPTCHA or puzzle as the only auth path · `maximum-scale=1` / `user-scalable=no` · `text-align: justify` on long-form text · auto-submit on select · drag-only reorder · hover-only tooltips · `role` on native semantic elements.
