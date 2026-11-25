---
name: divorce
description: Write and check web front-end code (HTML, CSS, JS, ARIA, templates, builder widgets) against the web platform specs (WHATWG HTML, W3C CSS, WAI-ARIA, WCAG 2.2) with the least code that works. Use when building or reviewing a page, component or template, and always before saying web UI work is done. The pass/fail verdict comes from a script (Nu HTML Checker + axe-core), not from the model.
license: MIT
---

# divorce

> Your agent is in a toxic relationship with `<div>`. It's not you, it's the spec.

Two halves. Before writing: a short ladder that picks the smallest standard solution. Before saying "done": a gate
that validates the HTML the browser actually gets and the rendered DOM, and returns a verdict built by code.

It applies to any web stack (React, Vue, PHP, WordPress/Elementor, plain HTML): the gate checks the **output** (served
HTML and live DOM), not the source language. It does not check business logic, performance or visual design.

## 1. Before writing: the ladder

Stop at the first rung that holds (adapted from DietrichGebert/ponytail, MIT):

1. Does it need to exist? If not, don't write it.
2. Does the project already have it? A house component beats a native widget, and both beat a new one.
3. Is there a native element for it? (table below)
4. Can CSS do it without JavaScript?
5. Is there a dependency already installed that covers it?
6. Only then: the smallest code that works, plus a small test if it has logic.

Never trimmed for minimalism: accessibility, input validation at trust boundaries, error handling that loses data.

## 2. Pick the element by what it does

| it… | use | not |
|---|---|---|
| performs an action | `<button type="button">` | `<div onclick>`, `<span role="button">` |
| goes somewhere | `<a href>` | a button or div that routes in JS |
| shows/hides related content | `<details>`/`<summary>` | a custom disclosure with hand-written keys |
| opens a temporary task on top | `<dialog>` or the Popover API | a modal div fighting focus |
| collects input | native controls inside `<form>`, each with a `<label>` | clickable rows that ignore Enter/Space/disabled |

- ARIA refines native semantics; it does not rebuild them on a `div`. No ARIA is better than wrong ARIA.
- A button with `popovertarget` must not carry `aria-expanded`: the browser already exposes its state ([spec](https://w3c.github.io/html-aria/#el-button)).
- Do not put `aria-label` on a `<div>` or `<span>` without a role: give it the appropriate role or use the native element with a visible name ([spec](https://w3c.github.io/html-aria/#docconformance-naming)).
- Style state with native pseudo-classes (`:disabled`, `:checked`, `:open`, `:invalid`, `:focus-visible`) before a
  parallel `data-*` state system.
- A library primitive must still render the real element in the DOM: check it.
- Headings in order (one `h1`, no skipped levels); landmarks (`header`, `nav`, `main`, `footer`) once each.

(Element table and pseudo-class rule adapted from kemiljk/skills `semantic-html-first`, MIT.)

## 3. CSS defaults

- Layout: `gap`, `inset`, `aspect-ratio`, grid/`subgrid`, container queries, logical properties
  (`margin-inline`, `padding-block`) for anything direction-sensitive, `100dvh` for full-height on mobile.
- Colour: tokens on `:root`; `color-mix()` for states; `light-dark()` with `color-scheme` for themes.
- Motion: animate `transform`/`opacity`; every animation has a `prefers-reduced-motion` path.
- Support policy: features shipped in both Blink and WebKit go in by default; newer ones behind `@supports`; a
  single-engine feature only as an optional enhancement with a fallback.

(Adapted from kemiljk/skills `modern-css-html`, MIT.)

## 4. Spec or convention? Say which

When a choice rests on a spec, cite the section. When it is a convention, say so and follow the project's existing one
instead of flipping it on your own.

Example: CSS Basic User Interface Level 4 defines `cursor: pointer` as "a pointer that indicates a link"
(https://drafts.csswg.org/css-ui-4/#cursor). Giving `<button>` the arrow (`cursor: default`), as desktop OSes do, follows
from that text; giving it the hand is common web practice. Neither is a validity error and no checker flags it, so
keep whatever the project already does unless its owner decides otherwise.

Source order: WHATWG HTML Living Standard → W3C/CSSWG specs → WAI-ARIA and the ARIA Authoring Practices Guide →
WCAG 2.2 → MDN. Blog posts and Q&A sites are not sources.

## 5. Before saying done: the gate

```bash
G=<this skill>/scripts/gate.py
python3 $G html <file-or-URL> [...]                    # Nu HTML Checker on the HTML as served
agent-browser eval "$(python3 $G axe-snippet)" > axe.json   # axe-core on the rendered page, WCAG 2.2 AA + best practice
python3 $G axe axe.json
python3 $G check --html <file-or-URL> --axe axe.json --axe-max-impact serious
agent-browser eval "$(python3 $G keyboard-snippet)" > keys.json  # optional: keyboard facts on the same rendered page
python3 $G check --html <file-or-URL> --axe axe.json --keyboard keys.json
```

- Exit **0** pass · **1** fail (HTML errors, axe violations rated `serious`/`critical`, or keyboard findings) · **2** not measured
  (validator missing, unreadable axe output, URL down). A 2 is never a pass.
- The JSON it prints is the evidence: quote the counts and the messages, not your impression.
- Install the validator once with `scripts/install-vnu.sh` (downloads the official release and checks its hash).
- Validate the **served** page (URL or built file), not the template source: builders and frameworks add markup.
- The keyboard check reads the rendered DOM, it does not press keys. It lists the visible controls in the Tab order
  (`tabIndex` ≥ 0, not disabled, not inert) and fails on an element that reacts to clicks but has no keyboard path,
  or a custom `role="button"`-style control outside the Tab order. Click handlers added with `addEventListener` are
  only seen if the page loads with that init script first (`python3 $G keyboard-init > init.js`, then
  `agent-browser --init-script init.js open <url>`); the JSON says `listeners_tracked`.
- The same check warns, without failing, on a button whose own click handler assigns `location` or calls
  `location.assign`/`replace` or `window.open`: going somewhere is `<a href>` (section 2). A handler on a parent or a
  helper function it calls is not seen.
- Automated checks catch part of WCAG, not all. Tab order, Enter and Space, Escape, focus return and a visible focus
  ring (the keyboard check's `not_measured` list) and a look at the page are still yours: list what you did not check.

## 6. Closing report

What the gate returned (exit code and counts), what was checked by hand, what was not checked, and the risk left.
