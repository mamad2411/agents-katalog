---
name: shadow-dom-and-iframes
description: Reach elements hidden inside shadow DOM or iframes when browser_snapshot does not list them.
version: 0.1.0
when:
  keywords: [shadow dom, shadow root, iframe, embedded, web component, not found]
---
# Shadow DOM and iframes via CDP

Symptoms: the element is visible in a screenshot but missing from `browser_snapshot`.

Same-origin iframes and open shadow roots:
1. Run `browser_snapshot` again after `browser_wait`; frames load late.
2. Use `browser_eval` to pierce the boundary, for example
   `document.querySelector('iframe').contentDocument.querySelector('button')` or
   `document.querySelector('my-widget').shadowRoot.querySelector('input')`.
3. Prefer reading values or computing the element position with `getBoundingClientRect()`, then click by coordinates (add the iframe offset).

Cross-origin iframes:
- `contentDocument` is null. Use the accessibility snapshot (CDP builds it across frames) or click by screen coordinates taken from a screenshot.
- Typing: click the field first so it has focus, then use `browser_press` per key or `desktop_type`.

Closed shadow roots cannot be reached from page scripts; fall back to coordinates and keyboard input.

Keep `browser_eval` read-only where possible; it is a last resort and needs approval.
