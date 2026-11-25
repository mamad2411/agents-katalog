---
name: ui-visual-self-review
category: frontend
description: Use when you are about to hand off any UI change - the four-width check and the screenshot checklist that decide whether the screen is really done.
source: wshobson/agents (MIT), pbakaus/impeccable (Apache-2.0), adapted
---

# UI Visual Self-Review

## Overview

A change that compiles and passes its tests has not been looked at. The UI you're about to hand off is not done because the build is green or because you read the JSX and it looked right — it is done when you have screenshots at four widths that prove it.

**Core principle:** Default assumption: the change is NOT done until the screenshots prove it. Be the skeptic here, not the advocate — look for what's still wrong, not for confirmation that it's fine.

## The procedure (exact tool calls)

1. Start the dev server detached, as your main instructions' "Seeing the change" section describes: `mkdir -p /tmp/tt-<task key> && npm run dev > /tmp/tt-<task key>/dev.log 2>&1 &`, then `sleep 5; cat /tmp/tt-<task key>/dev.log` to read the port.
2. `browser_navigate` to the changed page.
3. `browser_wait_for` the content that proves the page actually rendered (not a spinner, not a blank shell).
4. For each width in the four-width table, in order:
   - `browser_set_viewport` with the exact args from the table below.
   - Read its response: whether the page scrolls horizontally, and which elements overflow. That response is itself a finding — don't discard it once you've glanced at the screenshot.
   - `browser_screenshot` with `full_page: true` and **no** `width` argument (passing `width` here re-emulates the viewport and silently throws away the size you just set).
   - Look at the screenshot against the checklist below.
5. `browser_read_dom` with `contains: "..."` for each new element, to confirm it's actually present (and whether hidden) — this is not a substitute for looking at the screenshot, it's a second signal.
6. Drive the interactive states at phone width at minimum: open the mobile menu, an accordion, a dialog; submit a form with empty required fields and look at the errors.

| Name | Width | `browser_set_viewport` call | Tailwind band |
|---|---|---|---|
| phone | 360 | `{device: "mobile", width: 360}` | below `sm` |
| tablet | 768 | `{device: "tablet"}` | `md` |
| laptop | 1024 | `{device: "desktop", width: 1024}` | `lg` |
| desktop | 1440 | `{device: "desktop"}` | `xl`+ |

Phone is 360, not 390, on purpose — most real overflow bugs show up between 320 and 375, and 390 is wide enough to hide some of them.

## Batch, then fix, then one re-check

Collect every finding from every width before you touch any code. Fixing after each screenshot means re-screenshotting after each fix, which is slower and hides whether one fix broke another width. Fix everything from the batch in one pass, then re-run the full four-width check once. At most two rounds total — whatever is still open after round two goes into the closing message, honestly, rather than triggering a third silent pass.

## The checklist

Each item is a yes/no question with a concrete threshold — "looks okay" is not an answer to any of them.

**Layout & overflow**
- Does `browser_set_viewport` report zero horizontal scroll and zero overflowing elements at all four widths?
- Is anything clipped, overlapping, or cut off in the screenshot that wasn't in the report (decorative elements near an edge, a dropdown that opens off-screen)?
- Do flex/grid rows with text children carry `min-w-0`, and are long words `break-words` not `break-all`?

**Hierarchy & rhythm**
- Is there exactly one visually primary action per view, and is it the most prominent thing on screen?
- Is spacing tighter inside a group than between groups, with more space above a heading than below it?
- **Squint test**: blur your eyes (or back away from the screenshot) — is the primary action still the first thing you'd tap?

**Typography**
- Is body measure 60–75ch (`max-w-prose`), are headings `text-balance` and body `text-pretty`, are numbers/prices `tabular-nums`?
- Does every heading step correctly per breakpoint, with no heading wrapping to an awkward single orphan word?

**Colour & contrast**
- Only semantic tokens (`bg-primary`, `text-muted-foreground`) — no raw palette class, no hex, in the diff?
- Body text ≥4.5:1 contrast, large text ≥3:1, in both themes if the project has dark mode?
- Is status (error/success/warning) carried by an icon or text, never colour alone?

**States & content resilience**
- Loading: does the skeleton match the final layout's shape, not a generic spinner?
- Empty: is there a message and one clear next action, not a blank rectangle?
- Error: is there a recovery action, not just red text?
- Hover, `focus-visible`, active, and disabled all styled on every control you touched?
- Did you feed the longest realistic string and an empty list/value to anything you added, and look at both?

**Navigation & touch**
- Below `md`, does ≥5 links collapse into a menu button with `aria-expanded`/`aria-controls`, and does the panel close on link click and `Escape`?
- Are touch targets ≥44×44px on phone, ≥24px on desktop, with no function that only works on hover?

**Consistency**
- Does the same kind of control (a primary button, a card, a badge) look identical everywhere it appears, built from the same atom, not a local re-implementation?

**Copy**
- Correct locale, no leftover `lorem ipsum`/placeholder text, no `TODO`/`FIXME` visible in the UI?

## Content stress

Before calling it done, put the component under realistic stress — not just the one happy-path string from the task description: the longest name/title/URL you can plausibly expect, a zero-item list, an empty string in an optional field. If a co-located test already asserts this, reading that test counts; if not, feed it manually and look.

## Closing message

State, for each width checked: what you set it to, what the viewport report said, and what the screenshot showed. Name any residual issue honestly rather than omitting it — a known gap reported is not a failure, an unverified claim of "done" is.

## Red Flags

- "Looks fine" without ever having set the viewport to phone width.
- A screenshot taken with a `width` argument after `browser_set_viewport` — it silently re-emulates desktop, so the screenshot is not of the size you think it is.
- Judging the result from `browser_read_dom` text alone, with no screenshot actually looked at.
- Re-screenshotting the same unchanged page and calling it a new check.
- More than two rounds of screenshot → fix → screenshot on the same page.
