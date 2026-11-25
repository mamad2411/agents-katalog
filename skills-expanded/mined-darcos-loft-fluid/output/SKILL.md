---
name: output
description: Execution discipline for shipped UI. Use to make sure generated frontend work is actually complete, with no placeholders, no skipped sections, no half-finished states, every interactive state handled, and the brief honestly met.
license: MIT
---

# Output

The difference between a demo and a shippable build is finish. This is a short checklist the agent runs before calling UI work done.

## No placeholders
- No "lorem ipsum", no "TODO", no "[image here]", no empty `href="#"`. Use real or plausible content.
- No "rest of the component" comments, no skipped sections. Write the whole thing.

## Every state
- Loading, empty, error, and success states for anything that fetches or submits.
- Hover, focus-visible, active, and disabled for every interactive element.
- Responsive: the layout holds at 375px, 768px, and 1280px. No horizontal scroll on mobile.

## Honest completeness
- If the brief lists five sections, build five, fully. Do not stub the last two.
- Every link goes somewhere. Every button does something or is clearly disabled.
- Accessibility: alt text, labels, visible keyboard focus, body contrast 4.5:1.

## Pre-flight
Before saying it is done, re-read the brief and confirm each requirement is actually met, not approximated. Run the `fluid` detector. If anything is stubbed, finish it first.

Pairs with: every other skill. This is the last gate before shipping.
