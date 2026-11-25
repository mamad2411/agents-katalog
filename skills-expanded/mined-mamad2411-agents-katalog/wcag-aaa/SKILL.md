---
name: wcag-aaa
description: Engineering rules for WCAG 2.2 Level AAA enhanced criteria — enhanced contrast, focus appearance, larger targets, no timing, enhanced auth, and readability. Use when targeting AAA conformance, building high-inclusion or public-sector experiences, or answering what an AAA criterion requires beyond AA.
license: MIT
metadata:
  author: ult-accessability
  version: "1.0.0"
---

# WCAG 2.2 Level AAA

Enhanced rules that go beyond [wcag-aa](../wcag-aa/SKILL.md) — this skill assumes AA is already met and states only the AAA delta. Criterion table: [WCAG.md](../../references/WCAG.md). Production code lives in the linked patterns; contrast ratios are measured with [contrast-color](../contrast-color/SKILL.md), never eyeballed.

AAA is the enhanced tier for specialized applications, healthcare, government, and maximum inclusion. New-in-2.2 criteria are marked **(2.2)**.

## Contrast and visual presentation

- Text contrast: 7:1 normal text, 4.5:1 large text (≥24px, or ≥18.66px bold) — `WCAG 2.2 SC 1.4.6 (Contrast (Enhanced), AAA)`. UI boundaries, icons, and focus indicators stay at 3:1.
- Long-form text blocks must satisfy all five: user-selectable foreground/background colors; ≤ 80 characters per line (40 for CJK); never fully justified; line-height ≥ 1.5 with paragraph spacing ≥ 2.25× font size; readable at 200% without horizontal scrolling — `WCAG 2.2 SC 1.4.8 (Visual Presentation, AAA)`.
- No text in raster images at all — live text, CSS, web fonts, or SVG text only (logos and essential presentations excepted) — `WCAG 2.2 SC 1.4.9 (Images of Text (No Exception), AAA)`.
- Background audio is ≥ 20 dB below speech, off, or avoidable — `WCAG 2.2 SC 1.4.7 (Low or No Background Audio, AAA)`.
- UI regions and controls expose purpose programmatically via landmarks and ARIA — `WCAG 2.2 SC 1.3.6 (Identify Purpose, AAA)`.

## Keyboard, timing, and motion — no exceptions

- Every interaction keyboard-operable with zero exceptions — canvas/freehand features need an equivalent structured keyboard input — `WCAG 2.2 SC 2.1.3 (Keyboard (No Exception), AAA)`.
- No time limits (except non-interactive or real-time essentials) — timers are off by default, never merely extendable — `WCAG 2.2 SC 2.2.3 (No Timing, AAA)`.
- Interruptions (push alerts, live popups, banners) can be postponed or suppressed — `WCAG 2.2 SC 2.2.4 (Interruptions, AAA)`.
- Form and session state survives expiry plus re-login — nothing entered is ever lost — `WCAG 2.2 SC 2.2.5 (Re-authenticating, AAA)`.
- Users are warned up front about inactivity timeouts and what data loss they risk — `WCAG 2.2 SC 2.2.6 (Timeouts, AAA)`.
- Nothing flashes more than 3 times in any 1-second period, no exceptions — `WCAG 2.2 SC 2.3.2 (Three Flashes, AAA)`.
- Motion animation from interaction can be disabled completely — honor `prefers-reduced-motion` for parallax, morphing, scroll-triggered, and auto-advancing motion — [reduced-motion](../../references/A11Y-PATTERNS.md#reduced-motion), `WCAG 2.2 SC 2.3.3 (Animation from Interactions, AAA)`.

## Navigation, links, and focus appearance

- Breadcrumbs, sitemaps, or step indicators always show the user's location — `WCAG 2.2 SC 2.4.8 (Location, AAA)`.
- Link text alone — no surrounding context — identifies the destination ("Download Annual Report 2026 (PDF)", never "Download") — `WCAG 2.2 SC 2.4.9 (Link Purpose (Link Only), AAA)`.
- Every content section has a descriptive heading — `WCAG 2.2 SC 2.4.10 (Section Headings, AAA)`.
- **(2.2)** No part of the focused element may be obscured by author content — 100% visibility under sticky headers, footers, and overlays — [scroll-margin](../../references/A11Y-PATTERNS.md#scroll-margin), `WCAG 2.2 SC 2.4.12 (Focus Not Obscured (Enhanced), AAA)`.
- **(2.2)** Focus indicators must have area ≥ a 2px-thick perimeter of the component, 3:1 against the unfocused state, and 3:1 against adjacent colors — the double-ring (inner light separator + outer ring) passes on any background — [focus-rings](../../references/A11Y-PATTERNS.md#focus-rings), `WCAG 2.2 SC 2.4.13 (Focus Appearance, AAA)`.

## Targets and input

- Targets ≥ 44×44 CSS px (inline, user-agent, essential, and equivalent-control exceptions) — expand hit areas with pseudo-elements so small visuals keep large targets — [target-size](../../references/A11Y-PATTERNS.md#target-size), `WCAG 2.2 SC 2.5.5 (Target Size (Enhanced), AAA)`.
- Users can mix input modes freely — never lock out touch, mouse, keyboard, stylus, or voice mid-flow — `WCAG 2.2 SC 2.5.6 (Concurrent Input Mechanisms, AAA)`.

## Readability and help

- Jargon and idioms get inline definitions or glossary links (`<dfn>`) — `WCAG 2.2 SC 3.1.3 (Unusual Words, AAA)`.
- Abbreviations expanded on first use (`<abbr title="…">`) — `WCAG 2.2 SC 3.1.4 (Abbreviations, AAA)`.
- Text above lower-secondary reading level ships a plain-language summary — `WCAG 2.2 SC 3.1.5 (Reading Level, AAA)`.
- Ambiguous pronunciations get guides (`<ruby>`) — `WCAG 2.2 SC 3.1.6 (Pronunciation, AAA)`.
- Context changes only on explicit user request — never on focus, input change, or selection — `WCAG 2.2 SC 3.2.5 (Change on Request, AAA)`.
- Context-sensitive help available for every input — `WCAG 2.2 SC 3.3.5 (Help, AAA)`.
- All submissions (not just legal/financial) are reversible, checked, or confirmed before finalizing — `WCAG 2.2 SC 3.3.6 (Error Prevention (All), AAA)`.
- **(2.2)** No cognitive-function test at all for login — no passwords to recall, no CAPTCHAs, no puzzles, and no object/image recognition step. Passwordless (WebAuthn/passkeys, magic links) or copy-paste-friendly tokens only — [auth-and-paste-friendly-inputs](../../references/A11Y-PATTERNS.md#auth-and-paste-friendly-inputs), `WCAG 2.2 SC 3.3.9 (Accessible Authentication (Enhanced), AAA)`.

## Media (extended)

- Prerecorded audio ships sign-language interpretation; extended description where pauses are too short; a full text alternative for synchronized media; live audio-only ships a real-time text alternative — `WCAG 2.2 SC 1.2.6 (Sign Language (Prerecorded), AAA)`, `WCAG 2.2 SC 1.2.7 (Extended Audio Description (Prerecorded), AAA)`, `WCAG 2.2 SC 1.2.8 (Media Alternative (Prerecorded), AAA)`, `WCAG 2.2 SC 1.2.9 (Audio-only (Live), AAA)`.

## AAA audit protocol

1. Run axe-core with the AAA tag set (`wcag2aaa` in addition to the AA tags) — then complete the manual checks below; automation alone never certifies AAA.
2. Measure all text against 7:1 / 4.5:1-large and all UI items against 3:1 with [contrast-color](../contrast-color/SKILL.md).
3. Verify every focus indicator against the 2.4.13 formula and confirm zero obscurity (2.4.12) by tabbing through sticky regions.
4. Measure target rects (≥ 44px both axes), confirm no un-extendable timers, and verify auth completes with zero cognitive tests.
5. Full suites live in [testing](../testing/SKILL.md); remediation follows [fix](../fix/SKILL.md).

## Next

- Verify conformance: [testing](../testing/SKILL.md).
- Remediate gaps: [fix](../fix/SKILL.md).
