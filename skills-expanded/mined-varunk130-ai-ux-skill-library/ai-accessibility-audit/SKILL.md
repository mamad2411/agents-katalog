---
name: ai-accessibility-audit
description: 'WCAG 2.2 Level AA accessibility audit for AI product surfaces - color contrast, focus order, ARIA usage, keyboard navigation, motion/animation, reduced-motion respect, alt text, and form label association. Use when: accessibility audit, a11y review, WCAG audit, screen reader compliance, keyboard-only navigation, color contrast check, focus management, ARIA review, accessible AI UX.'
---

# AI Accessibility Audit

Catch accessibility regressions in AI product surfaces *before* they ship - chat interfaces, agent dashboards, generated-content panels, streaming output regions, and consent / safety UI. WCAG 2.2 Level AA is the bar; the framework below operationalizes it for AI-specific patterns that the spec doesn't natively cover.

## Core Principle

Accessibility is a property of the *experience*, not just the markup. An AI product can pass an axe-core scan and still be unusable for a screen-reader user if streaming output isn't announced, consent UI traps focus, or "regenerate" controls are unreachable from the keyboard. This skill audits both the static layer (DOM, contrast, semantics) and the AI-specific dynamic layer (live regions, latency, motion).

---

## The CLEAR Audit Framework

| Letter | Dimension | The Question |
|--------|-----------|--------------|
| **C** | Contrast & Color | Does every text/icon/state meet 4.5:1 (or 3:1 for ≥18pt or non-text UI)? Is color the *only* signal anywhere? |
| **L** | Logic of Focus | Can a keyboard-only user reach every action in a sensible order, with a visible focus indicator and no traps? |
| **E** | Equivalents for Non-Text | Do images, charts, generated visuals, and audio have meaningful alternatives - including AI-generated content? |
| **A** | Announcements & Live Regions | Are streaming outputs, status changes, and AI errors announced to assistive tech without spamming? |
| **R** | Respect for User Preferences | Does the product honor `prefers-reduced-motion`, `prefers-color-scheme`, OS-level font scaling, and reduced-data hints? |

---

## WCAG 2.2 AA Coverage Matrix

The skill produces findings against the success criteria most commonly violated in AI product surfaces:

| Success Criterion | What Gets Checked | AI-Specific Gotchas |
|-------------------|-------------------|---------------------|
| 1.1.1 Non-text Content | Alt text on every meaningful image | AI-generated images often ship with empty alt; charts rendered as `<canvas>` lack text equivalents |
| 1.3.1 Info & Relationships | Headings, lists, landmarks, form labels | Markdown rendered from LLM output frequently produces orphan headings (h3 without h2) |
| 1.4.3 Contrast (Minimum) | 4.5:1 on all body text | "Subtle" UI states (disabled, secondary, "thinking…") often dip below threshold |
| 1.4.10 Reflow | No horizontal scroll at 320 CSS px | Long streaming code blocks and tables break this - needs horizontal-scroll container, not body scroll |
| 1.4.11 Non-text Contrast | 3:1 for UI components, focus indicators | Custom focus rings on dark backgrounds frequently fail |
| 1.4.13 Content on Hover/Focus | Tooltips dismissible, hoverable, persistent | "Why this answer?" popovers on AI citations often violate all three |
| 2.1.1 Keyboard | All functionality keyboard-operable | Send button, regenerate, stop-generation, copy-to-clipboard, model picker - audit each |
| 2.1.2 No Keyboard Trap | Focus can leave any component | Modal consent gates and citation popovers frequently trap |
| 2.4.3 Focus Order | Logical, predictable focus order | Streaming content insertion can shift focus or skip newly-rendered actions |
| 2.4.7 Focus Visible | Visible indicator on every focused element | `outline: none` with no replacement is the single most common failure |
| 2.4.11 Focus Not Obscured (2.2 new) | Focused element not hidden behind sticky UI | Sticky composer bars often cover the focused message above |
| 2.5.7 Dragging Movements (2.2 new) | Single-pointer alternative for drag | "Drag to reorder citations" patterns need keyboard alternative |
| 2.5.8 Target Size (2.2 new) | Interactive targets ≥24×24 CSS px | Inline action chips inside chat bubbles routinely fail |
| 3.2.6 Consistent Help (2.2 new) | Help mechanisms consistently located | "Report response" / feedback controls drift across surfaces |
| 3.3.7 Redundant Entry (2.2 new) | Don't make users re-type info in the same flow | Multi-step agent setup flows commonly violate |
| 3.3.8 Accessible Authentication (2.2 new) | No cognitive function test for auth | API-key paste flows that disallow paste fail this |
| 4.1.3 Status Messages | Use ARIA live regions for status without focus shift | Streaming AI output, "Thinking…", and error toasts must use `aria-live="polite"` (not `assertive` for streaming - it spams) |

---

## AI-Specific Patterns the Spec Doesn't Cover

These are the patterns that pass a generic scan but fail real users of AI products. The skill explicitly checks each:

| Pattern | Failure Mode | Recommended Fix |
|---------|--------------|-----------------|
| **Streaming output** | Each token announced individually → screen reader chaos | Wrap streaming region in `aria-live="polite"` and `aria-atomic="false"`; announce only on sentence boundaries or every N tokens |
| **"Thinking…" indicators** | Animated dots invisible to AT, or announced repeatedly | Single `aria-live="polite"` status text, not a loop; respect `prefers-reduced-motion` for the animation |
| **Stop-generation control** | Only appears mid-stream and steals focus | Reserve a stable focusable slot; toggle `aria-disabled`, don't add/remove from DOM |
| **Citation popovers** | Open on hover only; trap focus when keyboard-opened | Open on focus or click; ESC closes and returns focus to trigger |
| **Regenerate / variant carousel** | Right-arrow cycles, but not announced | Use `role="region"` + `aria-label` + `aria-live` on the active variant |
| **Consent / safety modals** | First-time modals trap focus before user understands | Focus headline (not first input); `Esc` closes only if the action is non-blocking |
| **Generated images** | `alt=""` or `alt="image"` | Caption with the *user's prompt* as a baseline; let users override |
| **Voice / audio output** | No transcript; no captions on TTS | Always render the spoken text; offer scrubbable transcript |
| **Color-coded confidence** | Red/yellow/green badge with no text | Pair every color with a label or icon |

---

## Output

Save to `outputs/a11y-audit-[surface]-[YYYY-MM-DD].md`

The audit produces a prioritized issue list:

| Severity | Definition | Examples |
|----------|------------|----------|
| **Critical** | Blocks a class of users from completing a core task | Send button unreachable by keyboard; modal traps focus; streaming output unannounced |
| **Serious** | Significantly degrades the experience for assistive-tech users | Focus indicator removed; contrast 3.5:1 on body text; missing form labels |
| **Moderate** | Workaround exists but cognitive load is high | Confusing focus order; redundant announcements; small touch targets |
| **Minor** | Polish-level; doesn't block any task | Decorative icons exposed; non-essential heading-level skip |

Every finding includes:
- **Where** - selector, screenshot, or step-by-step reproduction
- **WCAG criterion** - e.g., "2.4.7 Focus Visible (AA)"
- **Why** - the user impact in one sentence
- **Fix** - concrete code snippet or design change, not just "add ARIA"
- **Test** - how to verify the fix (keyboard-only walk, NVDA/VoiceOver script, contrast number)

---

## Process

### Step 1: Scope the Audit
I'll ask:
> "What surface am I auditing? (URL, route, component name, or screenshot.) What user flows must work end-to-end? (e.g., 'send a message and copy the response'.) Any known assistive-tech users I should optimize for?"

### Step 2: Static Layer Pass (CLEAR - C, E)
Walk the rendered DOM and styles for contrast, semantics, alt text, landmarks, and headings. Produce findings against 1.x and 4.1.x criteria.

### Step 3: Keyboard Layer Pass (CLEAR - L)
Tab through every focusable element from `<body>`. Note: focus visibility, focus order vs. visual order, focus traps, missing focus return after dismissals, and 2.2's new criteria (2.4.11, 2.5.7, 2.5.8).

### Step 4: Dynamic / AI Layer Pass (CLEAR - A)
Trigger streaming output, errors, stop-generation, regenerate, citation popovers, and consent modals. Verify announcements (live regions), focus behavior on insertion, and motion respect.

### Step 5: Preference Pass (CLEAR - R)
Confirm `prefers-reduced-motion`, `prefers-color-scheme`, font-size scaling to 200%, and zoom to 400% all degrade gracefully.

### Step 6: Synthesize the Report
Group findings by severity, then by CLEAR dimension. Add a one-page "ship blockers" summary at the top (Critical + Serious only) so the team knows what must be fixed before release.

### Step 7: Acceptance Tests
For each Critical and Serious finding, write a one-line acceptance test the team can paste into their PR template (e.g., "Tabbing from composer → send → response area works in this order; focus visible at every stop").

---

## Tips
1. **Audit the *flow*, not just the page** - a checkbox-clean page with a broken send-message flow is worse than a couple of contrast warnings on a perfect flow.
2. **Test with the OS, not just a browser extension** - turn on VoiceOver / NVDA for at least one full task. Extensions don't catch announcement spam.
3. **Treat 2.2's new criteria as table stakes** - 2.5.8 (target size) and 2.4.11 (focus not obscured) catch ~30% of real-world failures in chat UIs.
4. **Make accessibility part of the prompt** - when generating UI from a model, include "WCAG 2.2 AA, visible focus, semantic HTML, aria-live for streaming" in the system prompt; it raises the floor measurably.
