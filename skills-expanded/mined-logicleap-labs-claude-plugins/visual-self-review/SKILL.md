---
name: visual-self-review
description: MANDATORY acceptance gate before declaring ANY visual or UI work "done", "good", "working", or before screenshotting an interface and ending the task. Use whenever you build, redesign, restyle, or fix a user-facing screen in ANY stack — Xcode/SwiftUI/UIKit apps, iOS/macOS, web (Next.js/React/HTML), Electron, Flutter, generated design mockups — and whenever you are asked to "review the screenshot", "check what you built", "is this good", "spot the issues", or "look at this design". Forces a structured, written, adversarial inspection of the ACTUAL rendered pixels (not the code, not your memory of intent) so obvious defects — blank/unlabelled elements, dead empty space, duplicated or garbage content, misalignment, inconsistent spacing, truncation, low contrast, leftover placeholders, broken states, and lag/jank — are caught BEFORE you claim completion. Triggers on "done", "looks good", "finished the UI", "here's the redesign", "screenshot", "ship it".
---

# Visual Self-Review — the acceptance gate for anything with pixels

**Read this whole file before you write your review.** This skill exists because of one specific, repeated failure: you build a screen, screenshot it, glance at it, decide "looks like an app → done", and hand over work with defects so obvious a human spots them in two seconds. You are fully capable of seeing those defects. You just don't *look* — you pattern-match. This skill replaces the glance with a forced serial scan.

The rule that makes everything else work:

> **You do not get to judge a screen until you have transcribed it.**
> Describe first. Judge second. A holistic "looks good" is banned as a first move — it is the exact reflex that ships broken UI.

---

## The worked example that triggered this skill (study it)

A redesigned task app ("Cadence") was screenshotted and declared good enough to end the task. When then asked to "review the issues", the obvious ones were *still* missed. Here is what a two-second human look caught and the model didn't:

1. **A sidebar item with NO text.** Under "WORKSPACE" there is a filled pill — and it is completely blank. An interactive nav row rendering zero label. Unmissable the instant you list the sidebar items one by one. Missed because nobody listed them.
2. **A huge dead gradient void at the top of the page.** The entire top band above the stat cards is empty — no page title, no heading, no breadcrumb, nothing. ~15% of the viewport is wasted space that screams "unfinished". Missed because nobody accounted for every region of the screen.
3. **Garbage/duplicated content rendered as if fine.** The timeline shows "prepare the seed round data room" **seven times in a row** (09:00, 09:30, 10:00, 10:30, 11:35, 12:05, 12:35). Obviously broken data being presented as a finished feature. Missed because nobody read the list top to bottom.
4. **Reported lag, never measured.** "Disgracefully laggy" — and no performance pass was ever run.

None of these need design taste. They need *looking*. That is all this skill enforces.

---

## Step 1 — Render the real thing (never review code or memory)

You review **pixels that actually rendered**, never the source you wrote, never your intent. The code can be perfect and the screen still broken (data, layout, async, theme, hit-testing). Capture the actual current state:

- **Web / Next.js / React:** use the preview MCP — `preview_start` if needed, then `preview_screenshot` for visuals and `preview_snapshot` for the accessibility/DOM tree. Use `preview_resize` for the responsive + dark-mode passes. Use `preview_console_logs` / `preview_network` for errors. (Per project rules: never `npm run dev` via Bash — use the preview launch config.)
- **Xcode / iOS / macOS:** build & run, then capture the simulator: `xcrun simctl io booted screenshot /tmp/vsr.png` (or Device → Screenshot, or the SwiftUI preview canvas) and then **Read the PNG back** so you actually see it. A green build is NOT a render check — SwiftUI layout, Auto Layout, dynamic type, dark mode and hit areas all fail at runtime with a clean compile.
- **Generated mockups / image designs:** Read the image you produced.
- **Capture every state you changed:** default, loading, empty, error, the long-content case, light AND dark, and the smallest target width. A screen is not reviewed until each state you touched has a screenshot you have actually looked at.

If you cannot render it, say so plainly and do not claim it works. "Compiles" / "types pass" / "should render" are **not** verification — they never catch CSS, layout, hit-testing, data, or browser/OS-specific bugs.

---

## Step 2 — Transcribe before you judge (the core mechanic — do not skip)

For each screenshot, **write out** a literal inventory. This is serial, not holistic. You are forbidden from writing any verdict until this is done.

1. **Read every text string** visible, top-to-bottom, left-to-right. Transcribe them verbatim. The moment a clickable/interactive element has **no text where text belongs**, you have found a defect — flag it. (This is what catches the blank sidebar item.)
2. **Account for every region** of the frame: top bar, sidebar, header, main content, each card, footer. For each region state what it contains. If a region contains *nothing*, that empty space is a defect candidate — name it and justify why it's intentional or fix it. (This is what catches the dead void.)
3. **Read every list/repeated element in full.** Do not "..." past them. Repetition, duplication, obviously-fake or placeholder data (lorem, "Title", "prepare the seed round data room" ×7) is a defect. (This is what catches garbage data.)
4. **Note the alignment grid:** do edges line up? Are paddings equal? Are sibling cards the same height? Is type on a consistent scale?

Only after this inventory exists may you evaluate.

---

## Step 3 — Sweep the defect taxonomy (assume defects exist)

Frame it adversarially: **assume there are at least three defects and your job is to find them.** "I found none" almost always means you didn't look — re-scan the regions you skimmed. Walk every class:

| # | Defect class | What you're hunting | The tell |
|---|---|---|---|
| 1 | **Missing / blank content** | interactive element with no label, icon with no glyph, image that didn't load, `undefined`/`NaN`/`null` rendered | a box where text/content should be |
| 2 | **Dead space** | large empty bands, no page title/heading, orphaned whitespace, content not filling its container | "is this region supposed to be empty?" |
| 3 | **Duplicate / garbage data** | repeated rows, placeholder/lorem left in, fake seed data shown as real | reading the list in full |
| 4 | **Misalignment** | edges not aligned, off-grid elements, ragged margins, uneven gutters | trace vertical/horizontal edges |
| 5 | **Inconsistent spacing / sizing** | unequal padding between siblings, mismatched card heights, random gaps | compare sibling to sibling |
| 6 | **Typography** | mixed scales, weights, fonts; orphan/widow lines; ALL-CAPS inconsistency | compare every text size to its neighbours |
| 7 | **Truncation / overflow** | clipped text, "…", content escaping its box, horizontal scrollbars | check long-content + narrow-width shots |
| 8 | **Contrast / legibility** | low-contrast text, text on busy gradient, invisible-until-hover affordances | squint test; check the gradient areas |
| 9 | **Broken states** | empty/loading/error states unstyled or showing raw errors | force each state |
| 10 | **Overlap / z-index** | elements on top of each other, cut-off shadows, modal behind content | look at layering |
| 11 | **Alignment to intent** | does it match what was asked? missing requested feature/section? | re-read the original request |
| 12 | **Performance / jank** | see Step 4 | measure, don't guess |

For each defect: state **where** (region + the transcribed text near it), **what's wrong**, and **severity** (blocker / obvious-to-user / polish). Blockers and obvious-to-user defects MUST be fixed, not noted.

---

## Step 4 — Performance pass (because "laggy" is a real defect)

If you touched anything interactive, measure responsiveness — don't eyeball it once and move on.

- **Web:** check `preview_console_logs` for errors/warnings and `preview_network` for slow/failed/duplicated requests. Watch for re-render storms (the same request firing repeatedly = the data-duplication bug above is often also a perf bug). Exercise the interaction (`preview_click`, scroll) and confirm it's smooth. Look for layout thrash, unthrottled scroll/resize handlers, unmemoised lists, animating `width`/`height`/`top` instead of `transform`.
- **Xcode:** scroll long lists in the simulator; watch for hitches. A laggy list is usually unmeasured `body` recomputation, missing `id`/`Equatable`, heavy work on the main thread, or images decoded on-scroll.
- Lag the user reported is a **blocker**, not a footnote. Find the cause (profile / read the render path), fix it, re-verify.

---

## Step 5 — Fix, re-render, re-review

Every blocker and obvious-to-user defect: **fix it, then re-capture the screenshot and run Steps 2–3 again on the new image.** A fix you didn't re-screenshot is a fix you didn't verify. Loop until a clean pass.

---

## Definition of Done (all required — do not claim "done" until every box is true)

1. The screen was **actually rendered and screenshotted**, and you **looked at the image** (Read it back). Every state you changed has its own shot (default / empty / loading / error / long-content / light + dark / narrowest width).
2. A **written transcription** (Step 2) exists for each shot — every text string read, every region accounted for, every list read in full.
3. The **full taxonomy** (Step 3) was swept; defects listed with location + severity.
4. Every **blocker / obvious-to-user defect is fixed and re-screenshotted** — not just noted.
5. A **performance pass** (Step 4) was run if anything interactive changed; reported lag chased to root cause and fixed.
6. The result was checked **against the original request** — nothing asked-for is missing.
7. Your report **shows the proof** (the screenshots / log output) and states plainly what you checked and what you found. If something is unverified, say which and why.

**"Looks done" is not done. A clean compile is not a render. A glance is not a review.** If a human would spot it in two seconds, missing it is the failure this skill exists to prevent — there is no excuse, because you can see it too. You just have to look, one element at a time.
