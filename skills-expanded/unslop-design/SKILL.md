---
name: unslop-design
description: Review and redesign an app or website UI to strip out the "slop" (decorative accent color, gradients, glows, noisy badges, emoji as icons, eyeballed spacing, greetings as titles, Title Case, flat hierarchy, repeated numbers) with a system (spacing, type, color roles, elevation) and two modes: a quick five-fix pass for one screen, or an orchestrated process for a whole app (parallel reviewers, a published winning proposal, devs per area, audits, PR). Covers SwiftUI, Compose and web (dashboards, landing pages, Tailwind), with scripts that scan the code, measure the rendered page and score it from 0 to 100. Use it when asked to "review the design", "make it look less AI", "unslop", "polish this screen", "design review", "winning proposal", "audit this dashboard", or when given videos or screenshots of an app or site asking for feedback or a redesign. Also use it to start a design system (spacing, type, palette, shadow scales) or to audit tokens, contrast or consistency across screens.
license: MIT
metadata:
  author: marcosnovo
  version: "1.7.0"
  homepage: https://github.com/marcosnovo/unslop-design
---

# Unslop design

Three parts: **what to fix** (`checklist.md`, each fix with its reason),
**how to orchestrate it** (`process.md`, rounds with reviewers and devs in
parallel) and **cases and sources** (`references.md`: the before/afters
that shaped this skill and a map of *Refactoring UI*). The spec card every
reviewer fills is in `spec-card.md`. Per-platform notes
(SwiftUI, Compose, web, widgets, watch, car) live in `platforms.md`; websites,
web apps and dashboards have their own playbook in `web.md`. Read the one
you need, not all of them.

Three scripts measure instead of guessing:
- `python3 scripts/slop-scan.py <paths>` — slop patterns in source (web,
  SwiftUI, Compose) with file, line and fix number. Standard library only.
- `node scripts/web-audit.mjs <url>` — the rendered page at 390/768/1280 px:
  horizontal scroll, a census of every size/color/radius/shadow/spacing in
  use, computed contrast, focus states, emoji, glows, plus a grayscale
  screenshot. Needs Playwright.
- `python3 scripts/unslop-score.py <paths> [--audit report.json]` — both
  as one number from 0 to 100 with where the points went, plus a README
  badge. Run it before and after: "score 41 → 88" is the PR's headline.

`examples/dashboard-before.html` and `-after.html` show both on one page.

## Principles (non-negotiable)

1. **A fix is a rule, not a tweak.** Every change ships as a token or
   component (spacing, font size, weight, color role, radius, shadow,
   button), never as a literal in the view. If the token is missing, create
   it in the same change. Pick values **by elimination** within the scale
   (try the value and its two neighbors; the middle wins or you repeat),
   never pixel by pixel.
2. **Hierarchy before color.** The screen has to work **in grayscale**:
   spacing, size, weight and contrast do the work; color comes afterwards and
   only to mean something. If it's unclear in gray what matters, color won't
   fix it.
3. **The first thing you read is the answer.** One hero number per screen
   (the balance, the price, today's progress); everything else steps back.
   Emphasize by **de-emphasizing the competition**, not by inflating the
   hero. At most one dark/hero surface per screen, and **none in sheets or
   modals**.
4. **Color says one thing.** One brand accent for the action or the hero
   number; everything else is a role with meaning (money/success, up/danger,
   status, reward) and gray for what only navigates. Decorative color =
   slop. Color never works alone: shape or a word goes with it.
5. **Measured contrast, not assumed.** WCAG AA (4.5:1 text, 3:1 large text
   and icons) computed from the real hex values against the real
   backgrounds, light and dark. White on a green/yellow brand color almost
   never passes; gray text on a colored background doesn't either (pick a
   shade of the same hue).
6. **Nothing the screen can't deliver.** No invented numbers, no projection
   presented as data, no implied feature that doesn't exist, no empty state
   that lies. Design the smallest version you can actually ship.
7. **One signature gesture, taken from the domain.** A brand detail born
   from what the app shows (a price-board price with a smaller last digit,
   dot-matrix numerals on a running app), not a new font or effect; and it
   degrades gracefully where it doesn't apply. Everything else is native:
   don't fight the tab bar, switches or system sheets.
8. **Platforms ship together.** If the project has iOS and Android (or app
   and web), the change goes to both in the same PR, in every language.
9. **Verify what the user sees.** Screenshots in light and dark, largest
   text size, a non-default currency/language, real data (long names, empty,
   2,000 items). What can't be compiled in your environment gets audited by
   reading, and the PR says so.

## Any agent (Claude Code, Codex, Cursor, Copilot, Gemini…)

The rules are the same everywhere. Where it says "agents", use what your
tool has: subagents if it has them (Claude Code, Codex…), with a git
worktree each for devs. With no subagents, run the reviewers one after another,
each with its own brief, and keep their outputs separate before the jury
step. Where it says "publish", Claude Code publishes an artifact; other agents
write an HTML file the user opens. In a chat app without a codebase, stop
after the before/after proposal.

## Quick mode (the default for one screen)

One screenshot, one screen or one page, or the user says "quick": no
subagents, no jury, one pass you can finish in a few minutes.

1. Ground it in one line (what the screen is for, its surface mode) and
   measure what you can: `scripts/unslop-score.py` on the screen's code
   (with `--audit` for a web page). Then the passes on the render
   (`process.md` § 2): one second, squint, cover the logo, left edges, gray.
2. Pick the **five fixes that change the screen most**, each with its
   `checklist.md` number and one line of why. Hierarchy and spacing before
   color, color before polish. Say what you would *not* change.
3. Show the before/after: the edited code's render, or an HTML mock of the
   screen if there's no code, with the filled `spec-card.md` rows it uses.
   Score it on the six axes of `process.md` § 4 first; under 3 on any
   axis, revise before showing.
4. On "yes", apply them as tokens (principle 1), rerun the score and report
   "score X → Y" and what's still left.

Switch to the full flow below when there are several screens or videos,
no design system yet, platforms to ship together, or the user asks for a
full review.

## Surface modes

Not every screen gets the same ambition. Name the mode before judging:

| Mode | Screens | What wins | Expression budget |
|---|---|---|---|
| Operate | dashboards, settings, editors, admin | scanning, consistency, platform conventions | low: one signature at most |
| Persuade | landing pages, onboarding, paywalls | one message, one action, a real product shot | higher: one bold idea |
| Read | articles, docs, detail pages | line length, rhythm, quiet chrome | low |
| Experience | games, maps, camera, media | the content itself as the canvas (#59) | high, from the domain |

The checklist applies to all four; the budget decides how far #47 and
#58 go.

## Working agreement (full flow)

- Reviewers = *senior product designers* and devs = *senior devs*, as
  agents (use the model the user asks for). The orchestrator doesn't build
  the areas: it does the shared work, integrates and audits.
- Every decision comes with an **explicit, actionable recommendation**.
- **Before implementing, publish the before/after** and wait for the user's
  "yes".
- Every round also reviews what earlier rounds shipped and **all** the
  videos/screenshots received, not just the latest.
- When merging is allowed once CI is green: close with a list of what to
  check when compiling (concrete risks) and, if there's no Mac/simulator, a
  self-contained prompt for a local session.
- On "is everything done?": done (with PRs) · pending on you · left out on
  purpose.
- After the last round, update the project's design system.

## Full flow

1. Inventory: frames from the videos (`process.md` § 1), screens and
   states, and each screen located in the code. Run `scripts/slop-scan.py` on the
   UI code and, for the web, `scripts/web-audit.mjs` on each key page.
2. System: check (or create) the spacing, type, color and elevation scales
   (`checklist.md` § System). Without scales, reviewers judge by eye; the
   audit's census shows which values the page really uses.
3. Grayscale pass + parallel reviewers (3-4, one per area) against
   `checklist.md`, applying fixes **one at a time**.
4. Winning proposal: one HTML page with before/after, the spec card and
   the list of decisions; the user chooses.
5. Devs per area in isolated worktrees with a closed brief; integrate,
   compile, audit, PR, answer review bots, merge when green.
6. Finally: update the project's design system (doc + tokens + its own
   skill) with what's new.

## If the project already has its own design skill

Use it for concrete tokens and components; this one brings the method and
the general checklist. If a rule here clashes with a written project
decision, the project wins and the proposal points it out.
