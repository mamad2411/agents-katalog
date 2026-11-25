---
name: accessibility-linter
description: Reviews accessibility mid-design, not as a compliance audit, but as a craft challenge. Use when designing, describing, or building a UI component. Trigger on "I'm designing a component", "does this work", "review this interaction", "how should I handle focus", "is this accessible", or whenever HTML/CSS/React code is shared. Also trigger when component states, interaction models, or keyboard behavior are being described. Don't wait to be asked. If a component is being actively designed, this skill is relevant.
metadata:
  author: "[Som](https://www.linkedin.com/in/designedbysom/)"
---

# accessibility-linter

|                 |                                                                                                                     |
| --------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Author**      | [Som](https://www.linkedin.com/in/designedbysom/)                                                                   |
| **Version**     | 1.0                                                                                                                 |
| **License**     | MIT                                                                                                                 |
| **When to use** | While actively designing or building a UI component                                                                 |
| **Input**       | Component description, design intent, HTML / React code                                                             |
| **Output**      | Structural challenges and open questions, not a compliance report                                                   |
| **Covers**      | Semantic HTML, ARIA, keyboard navigation, focus management, component states, color contrast, motion, touch targets |
| **Not this**    | A WCAG audit, a linter plugin, a post-ship review tool                                                              |

---

Bad accessibility is a structural problem wearing an accessibility costume. When focus order is wrong, the hierarchy is wrong. When a button needs `aria-label`, the visual design isn't doing its job. When a modal traps keyboard users, the interaction model was never finished.

Don't list what's wrong. Ask the structural question behind the failure. Push back on decisions that haven't been made explicit. That's the point.

Fix the structure. The a11y fix follows.

---

## What every a11y failure is really saying

Every accessibility failure is an underspecified design decision. Use this as your diagnostic lens: find the failure, then ask the structural question behind it.

| a11y failure                        | structural question to ask                                              |
| ----------------------------------- | ----------------------------------------------------------------------- |
| Broken focus order                  | Does the DOM order actually match the visual hierarchy?                 |
| Unlabelled interactive element      | Was the action named, or only implied visually?                         |
| Color as the only state signal      | Was state modeled, or just styled?                                      |
| Icon-only button with no label      | Does the visual shorthand have a verbal equivalent?                     |
| Missing `alt` text                  | Was the image's meaning in context ever defined?                        |
| Focus trap with no exit             | Does the interaction model have a close path?                           |
| Dynamic content not announced       | Was the state change treated as communication, or just a visual update? |
| Placeholder as label                | Was input context provided, or assumed?                                 |
| Disabled button with no explanation | Is this a dead end, or a gate? Does the user know the difference?       |
| Touch target too small              | Did the interaction model assume precision the user doesn't have?       |
| `aria-label` on a native element    | Why wasn't the visual design doing this work?                           |
| Missing focus state                 | Was focus ever part of the design, or added at the end?                 |

---

## How this skill thinks

There are two tiers of accessibility work. Treat them differently.

---

### Tier 1: Build it in, don't ask

Some accessibility decisions aren't decisions. They're defaults. When writing any code, include these without being prompted. They're part of what "finished" means:

- `<button>` not `<div onClick>`. `<a href>` not `<span onClick>`.
- `aria-label` on every icon-only button. Always.
- `<label>` paired with every `<input>`. `placeholder` is not a label.
- `alt` on every image. Empty string for decorative ones.
- `aria-invalid="true"` + error message via `aria-describedby` on form errors.
- `aria-busy="true"` on containers while loading.
- `aria-expanded="true/false"` on every disclosure trigger.
- `role="status"` or `aria-live="polite"` on dynamic content regions.
- `role="alert"` on error messages.
- `prefers-reduced-motion` respected on anything that animates.
- Visible focus styles. Never `outline: none` without a replacement.
- `disabled` attribute on disabled native elements, not just visual opacity.
- Landmark elements: `<nav>`, `<main>`, `<footer>`. Not `<div>` all the way down.

If you add something non-obvious, say it briefly in passing: "I'm using `aria-describedby` to link the helper text to the input." Then move on. Don't make it a lesson unless asked.

---

### Tier 2: Ask before building

Some decisions have structural consequences that can't be patched later. If any of these are ambiguous before the build starts, ask one focused question and wait for an answer before writing code.

- **Custom keyboard navigation:** tabs, combobox, menu, tree view, date picker. These have defined patterns. Confirm which pattern before building the interaction.
- **Focus management:** when something opens, where does focus go? When it closes, where does it return? If this isn't clear, ask.
- **Modal vs. non-modal:** does this overlay trap focus or not? A modal traps focus and needs `Escape` to close. A popover or tooltip does not. These are architecturally different. Decide before building.
- **Live region strategy:** if content updates frequently (real-time data, polling), does every update need to be announced? Constant announcements are as bad as none. Decide the cadence.
- **Complex ARIA patterns:** if the component requires `role="combobox"`, `role="grid"`, or `role="treegrid"`, align on the pattern before implementing. These patterns are specific and unforgiving if done wrong.
- **Intentional deviations from default patterns:** see below.

Ask one question. Not a list of questions. The most important unresolved decision, stated plainly:

> "Before I build this: does the filter panel open as a modal (focus trap, `Escape` to close) or as an inline expansion? That changes the implementation significantly."

---

### Intentional deviations: when breaking the default is right

Some accessibility conventions exist as defaults, not absolutes. When the UX stakes are high enough, overriding them is the correct call, but only if the deviation is deliberate, communicated, and has an explicit alternative.

**The pattern:** default behavior exists, UX intent conflicts with it, surface the tension, decide consciously, handle the alternative.

**Common cases worth raising before building:**

- **Disabling `Escape` and click-outside on a modal:** correct for multi-step flows, complex forms, or any modal where accidental dismissal causes data loss. The modal must have an explicit close or cancel action, and if there's unsaved state, the user needs to be told before they leave.

- **Capturing `Tab` in an editor or custom input:** a code editor or rich text field that uses Tab for indentation is correct to do so, but keyboard users need an escape hatch (`Escape` then `Tab`, or a documented shortcut). If Tab is captured with no alternative, keyboard-only users are trapped.

- **Blocking form submission until a selection is made:** valid for comboboxes and typeaheads where free text isn't allowed. The constraint needs to be communicated before the user tries to submit, not only after they fail.

- **Preventing scroll or navigation during a flow:** acceptable in multi-step wizards or onboarding sequences where losing context is genuinely disorienting. The user always needs a visible way out, even if it abandons progress.

- **Sticky or fixed elements that intercept focus:** overlapping a focused element with a sticky header is a common, silent failure. If sticky elements are used, scroll-padding or JavaScript focus management needs to account for them.

When one of these situations appears, raise it explicitly:

> "This looks like a form where the user could lose progress if they hit `Escape` accidentally. I'd suggest disabling `Escape` and click-outside to close, and adding an explicit Cancel button instead, with a confirmation if there's unsaved input. Does that match the intent?"

The key question is always: if the user does the unexpected thing, what happens? If the answer is "they lose their work" or "they get stuck," that's not a compliance issue. It's a broken interaction model.

---

### When reviewing existing code or a design

Don't run through a checklist. Read the component and find the structural decision that was never made explicit. Name it as a question, not a violation.

- What's missing is usually more telling than what's wrong.
- One open decision often explains multiple surface failures.
- If something is genuinely solid, say so and move on.

---

## Core principles

These aren't rules to check off. They're the structural commitments a component needs to be finished.

**1. Native HTML before ARIA.**
`<button>`, `<a>`, `<input>`, `<label>`, `<nav>`, `<main>`, `<section>` carry semantics for free. If you're reaching for ARIA, ask why native HTML wasn't enough.

**2. Name every interactive element, accessibly not visually.**
Every button, link, input, icon, and control has a name a screen reader can announce. If the name only exists visually, it doesn't exist for everyone.

**3. Design all states.**
Default, hover, focus, active, disabled, error, loading, empty. A component without a focus state isn't finished. A form without an error state is a sketch.

**4. Keyboard-first interaction model.**
Define the keyboard path before building the mouse interaction. If the keyboard model is unclear, the interaction model is unclear. They're the same thing.

**5. Color is never the only signal.**
Desaturate the UI mentally. If meaning disappears (if you can't tell what's an error, what's selected, what's active), the design is broken.

**6. State changes are communication.**
Dynamic content that updates without a page reload must announce that change to users who can't see it. A toast that appears silently, a form error that flashes in. These are communication failures, not just visual ones.

**7. Motion is opt-in.**
Anything that animates respects `prefers-reduced-motion`. Vestibular disorders are invisible. Don't make users ask for accommodation.

---

## Structure and hierarchy

Strip the visual design mentally. What remains?

- What is the logical reading order without CSS? Does it match what the visual design implies?
- Does the DOM order match the visual order? If they differ, there's a reason. State it explicitly.
- Are headings used for document hierarchy, not visual style? `<h2>` because it's a subsection, not because it's 18px bold.
- Does the landmark structure map to how a user would describe the page? `<nav>`, `<main>`, `<aside>`, `<footer>`. Not `<div>` all the way down.
- Is anything positioned visually in a way that breaks tab sequence?

If the visual order and DOM order are fighting each other, that's a hierarchy problem, not a tab order problem.

---

## Naming and labels

Every interactive element has an accessible name. If the name only works visually, it doesn't work.

- **Buttons with text:** The text is the name. Is it descriptive? "Delete account" beats "Delete". "Send message" beats "Submit".
- **Icon-only buttons:** `aria-label` required. `<button aria-label="Close dialog">` not `<button><IconX /></button>`.
- **Links:** Describe the destination. "Read the case study" not "Read more". Two "Read more" links on the same page are two identical names for different destinations.
- **Inputs:** Every `<input>` has a `<label>`. `placeholder` is not a label. It disappears on focus and fails low vision users.
- **Input groups:** `<fieldset>` + `<legend>` for radio groups and checkbox groups.
- **Images:** `alt` describes the image's meaning in context, not its appearance. Decorative images: `alt=""`. Functional images (a logo that's also a link): describe the destination, not the image.
- **Custom components:** Anything built from `<div>` or `<span>` that behaves interactively needs a name via `aria-label` or `aria-labelledby`. If it needs a name added this way, ask why native HTML wasn't used.

---

## States

A component without all its states is a sketch. Every state is a design decision, not an implementation detail.

| State                | What's required                                                                                                                |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| **Focus**            | Visible focus indicator. `outline: none` with no replacement is a hard no. Minimum 3:1 contrast ratio against adjacent colors. |
| **Hover**            | Visual change. Not required for a11y, but expected for usability.                                                              |
| **Active / pressed** | `aria-pressed="true/false"` for toggles. Visual feedback that matches.                                                         |
| **Disabled**         | `disabled` on native elements. `aria-disabled="true"` on custom elements. `opacity: 0.5` alone is not enough.                  |
| **Error**            | `aria-invalid="true"` on the input. Error message linked via `aria-describedby`. Color + icon + text, never color alone.       |
| **Loading**          | `aria-busy="true"` on the container. Announce completion via live region so non-visual users know it finished.                 |
| **Empty**            | Design the zero-state intentionally. Not a missing list, but a message, a prompt, a next action.                               |
| **Selected**         | `aria-selected` for listbox, tabs, grid. A visual highlight alone is not a state.                                              |
| **Expanded**         | `aria-expanded="true/false"` on the trigger element, not the panel.                                                            |

---

## Keyboard navigation

Every interactive component has a keyboard model. Define it before building it. If the keyboard path is ambiguous, the interaction model is ambiguous.

### Universal keys

| Key           | Expected behavior                               |
| ------------- | ----------------------------------------------- |
| `Tab`         | Move focus forward through interactive elements |
| `Shift + Tab` | Move focus backward                             |
| `Enter`       | Activate button, follow link, submit form       |
| `Space`       | Activate button, toggle checkbox                |
| `Escape`      | Close modal, dismiss popover, cancel operation  |

### Component-specific patterns

| Component       | Keyboard model                                                                                                                         |
| --------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| Dropdown / menu | `Enter`/`Space` opens, `↑ ↓` navigate items, `Enter` selects, `Escape` closes, focus returns to trigger                                |
| Modal / dialog  | Focus moves to first focusable element on open; `Tab` cycles within modal only (focus trap); `Escape` closes and focus returns to trigger, unless dismissal would cause data loss, in which case disable `Escape` and click-outside and provide an explicit close/cancel action |
| Tabs            | `←` `→` switch tabs (automatic activation or manual with `Enter`); `Tab` moves into tab panel                                          |
| Combobox        | `↓` opens list, `↑ ↓` navigate options, `Enter` selects, `Escape` collapses                                                            |
| Date picker     | Arrow keys navigate dates, `Enter` selects, `Escape` dismisses                                                                         |
| Accordion       | `Enter`/`Space` toggles panel, `↑ ↓` move between headers                                                                              |
| Tooltip         | Appears on focus (not just hover), `Escape` dismisses                                                                                  |
| Tree view       | `↑ ↓` navigate nodes, `→` expands, `←` collapses or moves to parent                                                                    |

### Focus management rules

- Focus moves into a component when it opens (modal, dialog, dropdown).
- Focus returns to the trigger when a component closes.
- Focus is never lost. It never lands on `<body>` unexpectedly.
- Modals trap focus. Nothing else does.
- Skip links (`<a href="#main">Skip to main content</a>`) are the first focusable element on every page.

---

## ARIA: use it correctly, not liberally

ARIA fills gaps that semantic HTML can't cover. It does not fix bad markup.

**Hard rule:** If you need ARIA to explain what an element is, you probably built it wrong. ARIA should extend semantics, not replace them.

### When to use ARIA

| Pattern                            | Correct usage                                                           |
| ---------------------------------- | ----------------------------------------------------------------------- |
| Icon-only button                   | `aria-label="Close"` on `<button>`                                      |
| Input with visible label elsewhere | `aria-labelledby="id-of-label"`                                         |
| Input with helper text             | `aria-describedby="id-of-helper"`                                       |
| Custom combobox / listbox          | `role="combobox"`, `aria-expanded`, `aria-controls`                     |
| Live region (toast, status)        | `role="status"` or `aria-live="polite"`                                 |
| Alert (error, critical)            | `role="alert"` (assertive by default)                                   |
| Loading state                      | `aria-busy="true"` on the container                                     |
| Disclosure / accordion             | `aria-expanded` on trigger, `aria-controls` pointing to panel           |
| Modal dialog                       | `role="dialog"`, `aria-modal="true"`, `aria-labelledby`                 |
| Progress                           | `role="progressbar"`, `aria-valuenow`, `aria-valuemin`, `aria-valuemax` |
| Toggle button                      | `aria-pressed="true/false"`                                             |
| Tab interface                      | `role="tablist"`, `role="tab"`, `role="tabpanel"`, `aria-selected`      |

### When not to use ARIA

- `<div role="button">`: use `<button>`
- `aria-label` on an element whose visible text is already accurate
- `role="presentation"` on something interactive
- Multiple roles stacked on one element
- `aria-hidden="true"` on focusable elements, hides from screen readers but keyboard users still reach it

---

## Color and contrast

Contrast is the floor, not the ceiling.

| Requirement                         | Ratio | WCAG level |
| ----------------------------------- | ----- | ---------- |
| Normal text (< 18px)                | 4.5:1 | AA         |
| Large text (≥ 18px or ≥ 14px bold)  | 3:1   | AA         |
| UI components and graphical objects | 3:1   | AA         |
| Enhanced text                       | 7:1   | AAA        |

- Every state (focus, hover, disabled, error) needs its own contrast check. A passing default state doesn't exempt the others.
- Test with a colorblind simulator, not just a contrast checker. Contrast ratios don't catch hue-only distinctions.
- If the only signal is color (red = error, green = success), add an icon or text label. Color alone is not a state.

---

## Motion

- `prefers-reduced-motion` must be queried if anything animates. Vestibular disorders are not rare.
- Reduced motion is not no motion. Avoid large translations, scaling, and spinning. Fades and opacity changes are usually fine.
- Nothing autoplays for more than 5 seconds without a pause control.
- Parallax scrolling is a vestibular hazard. Opt-in only.

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## Touch

- Minimum touch target: **44×44px** (Apple HIG, WCAG 2.5.5)
- Minimum spacing between targets: **8px** to prevent mis-taps
- No hover-only interactions. Every tooltip, dropdown, or reveal that works on hover must also work on tap and keyboard.
- Every swipe gesture has a button equivalent. Swipe is an enhancement, not the only path.

---

## Anti-patterns

These patterns feel like solutions. They're not.

- **ARIA as a patch.** Using `aria-label` to fix what `<button>` would have handled natively. The label is papering over a semantic failure.
- **Focus as an afterthought.** "We'll add `tabIndex` at the end" means the hierarchy was never decided. Focus order is a design decision, not a cleanup task.
- **Happy path only.** No focus state, no error state, no loading state. That's an unfinished component being called done.
- **Hover-only interactions.** Tooltips, popovers, and dropdowns that only appear on hover exclude keyboard and touch users entirely.
- **`outline: none` with nothing.** The most common focus failure in production. Always replace the focus indicator, never just remove it.
- **Identical link text.** Three "Read more" links are three unlabeled destinations. The destination is part of the name.
- **`aria-hidden` on focusable elements.** Hidden from screen readers, reachable by keyboard. Broken by design.
- **Designing for the prototype.** Placeholder content, missing states, implied labels. These are fine in Figma. They're not fine in code.

---

## How to talk

This is a conversation, not a report. Don't produce formatted audit output.

**When writing code:** Write accessible code by default (Tier 1). If a Tier 2 decision is ambiguous, ask before building. If you added something non-obvious, mention it in a sentence and move on.

**When reviewing a design or description:** Identify the most consequential unresolved decision and ask about it directly. Not a list, one question, clearly stated, with the structural implication explained.

**When reviewing existing code:** Name the structural problem behind the failure, not the failure itself. "The focus order is broken" is a symptom. "The DOM order doesn't match the visual layout. Which one reflects the intended hierarchy?" is the question.

**Tone:** Direct, collaborative, mid-build. Not academic. Not a checklist. Not a post-mortem.

Talk the way a senior design engineer would talk to a peer who asked for a second opinion: honest, specific, useful right now.
