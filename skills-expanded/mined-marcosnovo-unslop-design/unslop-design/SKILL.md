---
name: unslop-design
description: Review and redesign an app or website UI to strip out the "slop" (decorative accent color, gradients, glows, noisy badges, emoji as icons, eyeballed spacing, greetings as titles, Title Case, flat hierarchy, repeated numbers) with a system (spacing, type, color roles, elevation) and two modes: a quick five-fix pass for one screen, or an orchestrated process for a whole app (parallel reviewers, a published winning proposal, devs per area, audits, PR). Covers SwiftUI, Compose and web (dashboards, landing pages, Tailwind), with scripts that scan the code, measure the rendered page and score it from 0 to 100. Use it when asked to "review the design", "make it look less AI", "unslop", "polish this screen", "design review", "winning proposal", "audit this dashboard", or when given videos or screenshots of an app or site asking for feedback or a redesign. Also use it to start a design system (spacing, type, palette, shadow scales) or to audit tokens, contrast or consistency across screens.
license: MIT
metadata:
  author: marcosnovo
  version: "1.14.2"
  homepage: https://github.com/marcosnovo/unslop-design
---

# Unslop design

Three parts: **what to fix** (`checklist.md`, 72 fixes, each with its reason),
**how to orchestrate it** (`process.md`, rounds with reviewers and devs in
parallel) and **cases and sources** (`references.md`: the before/afters
that shaped this skill and a map of *Refactoring UI*). The spec card every
reviewer fills is in `spec-card.md`. Per-platform notes
(SwiftUI, Compose, web, widgets, watch, car) live in `platforms.md`; websites,
web apps and dashboards have their own playbook in `web.md`. The project's
own decisions live in `.unslop/context.md` (`context.md`), and the usability
rubric in `critique.md`. Read the one you need, not all of them.

## Commands

The user can name one; with none, pick by what they gave you.

| Say | What happens |
|---|---|
| *unslop* / *review* + a screen | Quick mode below: five fixes, before/after, wait for "yes" |
| *unslop init* | Write `.unslop/context.md` (`context.md`): three questions at most |
| *unslop score* | Run the scripts, `--save` the run, report "score X → Y" and the top rows. No proposal |
| *unslop audit* | `scripts/slop-scan.py` + `scripts/web-audit.mjs`, findings ranked by fix number. Changes nothing |
| *unslop critique* | The usability report in `critique.md`. Changes nothing, doesn't touch the score |
| *unslop apply* | The next accepted fixes from `.unslop/review.md`, one at a time, score after each |
| *unslop full* | The full flow below |

**No command and nothing attached:** read `.unslop/context.md`, the last
entry of `.unslop/history.json`, `.unslop/review.md` and `git status`, and
propose two or three concrete next steps ("3 accepted fixes are pending in
review.md: apply them?", "the settings screen changed since the last score:
score it?", "no context yet: init?"). One line each, then wait.

If `.unslop/context.md` exists, read it first and follow its **Keeps**: the
scripts already take its scale and allowed rules. If it doesn't, don't
block: run as usual and offer `init` once at the end.

The scripts live in this skill's folder: run them by their full path from
the project (`python3 <skill>/scripts/unslop-score.py src/`), or through
`npx unslop-design scan|score|audit|contrast`. They measure instead of guessing:
- `python3 scripts/slop-scan.py <paths> [--scale …] [--allow rules]` — slop patterns in source (web,
  SwiftUI, Compose) with file, line and fix number, including starter-kit
  defaults (#6), rows of identical stat cards (#65), pep-talk copy, Title
  Case and greetings with a name (#25, #26, #64), in SwiftUI and Compose
  strings too. Standard library only.
- `node scripts/web-audit.mjs <url>` — the rendered page at 390/768/1280 px:
  horizontal scroll, a census of every size/color/radius/shadow/spacing in
  use, computed contrast, focus states, emoji, glows, plus a grayscale
  screenshot, icon contrast (3:1, WCAG 1.4.11) for small SVG, whether
  the type follows the reader's text size, line length and justified or
  centered long text, and big empty placeholder boxes.
  `--device iphone,iphone-se,pixel` renders at real phone
  size and density with safe areas and reports which font really
  rendered. Needs Playwright.
- `python3 scripts/unslop-score.py <paths> [--audit report.json] [--save]` — both
  as one number from 0 to 100 with where the points went, plus a README
  badge. Run it before and after: "score 41 → 88" is the PR's headline.
  `--save` appends the run to `.unslop/history.json` and prints the trend;
  `--markdown` gives the table for a PR, and `--baseline main.json` (an
  earlier `--json` run) adds what got better and what got worse.
  A hit is fixed by changing the value, never by hiding it from the
  scanner (a `calc()` that lands on the same 11px is still 11px).

`scripts/contrast.py <text> <background>` gives the WCAG ratio of any pair
(hex, `rgba()`, Compose `0xFF…`; translucent text composited first): use it
for native colors, where there's no rendered page to audit.
`scripts/slop-scan.py --list-rules` lists every rule id; `--json` and `--github`
(Actions annotations) are for CI, and `action.yml` wraps both with a
minimum score and a PR comment (`uses: marcosnovo/unslop-design@v1`). In Claude Code the plugin's hook runs the scan after each
UI edit and tells you what you just added: fix those hits before moving on.
Gemini CLI, Codex and Copilot get the same hook with `npx unslop-design hooks <agent>`.

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
   don't fight the tab bar, switches or system sheets. It is the small end
   of a **concept** (`process.md` § 2b): one sentence from the domain that
   decides type, layout, color and motion, scaled to the surface mode.
   Attractive is not the same as different; a concept never buys lower
   contrast, invented data or decoration.
8. **Platforms ship together.** If the project has iOS and Android (or app
   and web), the change goes to both in the same PR, in every language.
9. **Verify what the user sees.** Screenshots in light and dark, largest
   text size, a non-default currency/language, real data (long names, empty,
   2,000 items), mobile mocks at device size and density (`process.md`
   § 2). What can't be compiled in your environment gets audited by
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
   measure what you can: `scripts/unslop-score.py` on **this screen's own
   files** with `--save` and `--json > .unslop/before.json` (and `--audit`
   for a web page), so the trend and the "after" have a baseline. A
   stylesheet shared with other screens carries their slop too: on the web
   the page's markup plus its rendered `--audit` is the screen's score, and
   the shared stylesheet's code score is reported apart. Then the
   passes on the render (`process.md` § 2): one second, squint, cover the
   logo, left edges, gray, ten-app lineup. Only when redesigning a Persuade
   or Experience screen, write three one-line concepts and pick one
   (`process.md` § 2c); a refine keeps the skeleton and skips them.
2. Pick the **five fixes that change the screen most**, each with its
   `checklist.md` number and one line of why. Hierarchy and spacing before
   color, color before polish. Say what you would *not* change.
3. Show the before/after **on one page, side by side at the same width**:
   the edited code's render, or an HTML mock of the screen when there's no
   code or it can't run here (native without a simulator: the mock at
   device size is the render, and the report says so), with the filled
   `spec-card.md` rows it uses. Put the board, the mocks and the audits in
   `.unslop/proposal/` (the scanner skips dot folders, so they never count
   against the project's score or its CI), the edited "after" as a copy in
   `.unslop/proposal/after/`, and change no project file before the "yes". Audit each state as its own page with its own `--out`
   (`.unslop/proposal/audit-before`, `-after`), not the side-by-side
   board, or the census mixes before and after; a phone mock
   (fluid up to the device width, not a fixed 393px) with `--device` and
   `--widths 390` (its text-scale line says nothing
   about native Dynamic Type: draw the largest size instead). For a
   desktop page, "same width" means its real width: stack the two, don't
   shrink them into half-width frames.
   **Only a screenshot, no code:** rebuild the before as an HTML mock from
   it, sample the colors (say they're approximate) and score the two
   mocks, labeled as mocks: never quote them as the app's score.
   Score it on the six axes of `process.md` § 4 first; under 3 on any
   axis, revise before showing. For Persuade and Experience screens run
   the second critic of § 4 once (with no subagents: answer its questions
   1-3 from the image alone, before rereading your own notes); for Operate
   and Read, answer questions 1-3 yourself. A "revise" verdict means one
   more pass; if it still holds, show it with the verdict stated.
4. On "yes", apply the accepted fixes as tokens (principle 1): all five,
   unless the user picked some. Rerun the score on the same files with
   `--save --baseline .unslop/before.json` and report "score X → Y" and
   what's still left. Write the five fixes to `.unslop/review.md` (format
   in `context.md`): applied `[x]`, accepted but not done `[ ]`, rejected
   `[-]` with the reason, deferred "for now" `[~]`, so the next run neither
   repeats nor forgets them. Commit nothing unless the user asks.
   *unslop apply* picks up the `[ ]` rows later; with none left, it says
   so and offers the next steps instead.

End the proposal with this report, filled honestly, so a skipped step shows:

```text
Render looked at   yes / no (which widths, light/dark)
Passes             one second · squint · logo · edges · gray · lineup
Six axes           H _  R _  S _  E _  Honesty _  Fit _
Spec card rows     the rows the after uses
Contrast           pairs measured (web-audit, or scripts/contrast.py for native)
Score              X → Y (same files, same script version, --allow if any)
Context            .unslop/context.md read / none (offer init once)
Not checked        largest text, dark, long data, … (say which)
```

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

The checklist applies to all four; the budget decides how far #47, #58
and #65 go and how big the concept is (`process.md` § 2b): Operate and
Read a signature, never a fill; Persuade one bold idea; Experience a whole
world. A concept the product's content doesn't ask for stays a signature.

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
3. Concept: find it (`process.md` § 2b), explore three directions as
   parallel agents on one key screen (§ 2c), and the user picks. An
   Operate app with an established signature skips this.
4. Grayscale pass + parallel reviewers (3-4, one per area) against
   `checklist.md`, applying fixes **one at a time**.
5. Jury, then redraw: the boards, spec cards and decisions take the
   jury's values (`process.md` § 3). Winning proposal: one HTML page with before/after, the spec card
   and the list of decisions, checked by the second critic (§ 4); the user
   chooses.
6. Devs per area in isolated worktrees with a closed brief; integrate,
   compile, audit, PR, answer review bots, merge when green.
7. Finally: update the project's design system (doc + tokens + its own
   skill) with what's new.

## Refine or redesign

Ask which one before proposing, unless the request already says ("keep
our layout", "start over"). **Refining preserves**: the layout, the
brand face, the signature and the voice stay, and fixes move values inside
them. **Redesigning replaces**: the concept (`process.md` § 2b) can change
the skeleton. Most requests are refinements; a refine that quietly redraws
the screen is the one thing the user didn't ask for. A refine still removes
what principles 5 and 6 rule out (contrast under AA, invented numbers,
logos and testimonials): keep the slot when it has a job ("social proof
here, once there is some") and say what real content goes in it.

## If the project already has its own design skill

Use it for concrete tokens and components; this one brings the method and
the general checklist. If a rule here clashes with a written project
decision, the project wins and the proposal points it out: a base-6 grid
beats #1, a brand face beats #6, tracked caps as the brand's signature beat
#45.

Two things a project decision can't settle: **contrast** (principle 5) and
**invented or unsourced claims** (principle 6). They aren't taste. White on
the brand green at 3.4:1 is a blocker, reported with the measured ratio and
a fix inside the brand (a darker green that passes, or dark ink on it), not
an option to keep. The owner can still overrule it, knowingly.

Run the scripts with the project's own values: `--scale` (and
`--type-scale`) from its spacing and type tokens, and `--allow` with the rule
ids its written decisions cover (`--allow tracked-caps,off-scale`). Allowed
rules are listed apart and not scored; contrast and unverified claims can't
be allowed, nor can focus or target size.
