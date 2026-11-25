---
name: website-bug-hunt
description: >
  Black-box website bug hunt: take any URL — no codebase access needed — and
  exhaustively audit it in a live browser. Crawls every page, clicks every
  button and link, exercises every form, tests at three viewports (desktop,
  tablet, mobile), and runs visual QA on every capture. Keeps hunting until a
  user-chosen bug quota or full coverage is reached, then produces a markdown
  bug report where every bug has exact reproduction steps, screenshots, a
  severity, and a ready-to-paste fix prompt for a coding agent. Use whenever
  the user gives a URL and asks to "find bugs", "audit this site", "visually
  inspect this website", "QA this URL", "test my deployed app", "click through
  everything", "check the site on mobile", or wants a functional + visual
  sweep of a live website — even if they don't say the word "bug". If the
  request combines a URL with any form of testing, inspecting, or auditing,
  this is the skill.
compatibility: Requires Playwright (default engine, auto-installed by scripts/setup.sh — works in restricted/ARM64 sandboxes) or the agent-browser CLI, plus network access to the target URL. Parallel mode requires subagent dispatch.
---

# Website Bug Hunt

Audit a live website the way a ruthless QA contractor would on day one: no
source code, no insider knowledge — just the URL, a browser, and the
discipline to click everything, look at everything, and write down every
defect with proof.

This skill is **black-box by design**. Everything you learn about the site,
you learn by driving it. That constraint is also the discipline: a bug you
can't reproduce through the browser isn't a finding, and a finding without a
screenshot doesn't go in the report.

## The Iron Rule

```
Interact with the REAL site. Never simulate, assume, or infer an interaction
you didn't perform. Every finding cites evidence you captured yourself:
a screenshot, a console error, a network response, a DOM snapshot.
A bug without reproduction steps + evidence does not exist.
```

## Run-start questions (ASK BEFORE STARTING)

Ask these once, together, then proceed. Don't drip-feed questions mid-run.

1. **Target URL** — if not already given.
2. **What is this site supposed to do?** One or two sentences from the user
   about the site's purpose and the 2-3 most important user journeys. This
   calibrates "bug vs. intentional". If the user doesn't know or doesn't
   answer, infer the purpose from the landing page and state your inference
   in the report header.
3. **Stop condition** — pick one:
   - `full-coverage` *(recommended default)*: stop when every discovered
     page × viewport has been audited and every interactive element exercised
   - `bug-quota <N>`: stop early once N confirmed bugs are logged (coverage
     so far is still reported)
   - `time-box <minutes>`: best-effort within the budget, prioritized P0→P2
4. **Credentials / gated areas** — "If I hit a login wall or paywall, do you
   have credentials for me?" Collect them up front if possible.
5. **Execution mode** — solo or parallel subagents? Recommend parallel when
   the site has more than ~8 pages and subagent dispatch is available;
   otherwise solo. If subagents aren't available, fall back to solo and say so.

## Tooling

**Playwright (chromium headless) is the default engine.** Set it up and read
the script templates in `references/playwright-engine.md` before Phase 1:

```bash
bash scripts/setup.sh ./hunt-workspace   # installs playwright + chromium, patches missing libs, smoke-tests
source ./hunt-workspace/engine/env.sh    # required before every node invocation
```

`setup.sh` is idempotent and handles restricted sandboxes (no root, ARM64,
missing shared libs like `libXdamage.so.1` — it fetches them unprivileged
via `apt-get download`). Do not start the hunt until its smoke test prints
`SMOKE OK`. Playwright is preferred because it runs where `agent-browser`
cannot (no Chrome-for-Testing build on Linux ARM64), crawls in parallel via
multiple pages in one browser, and attaches console/network/page-error
hooks per page (Template 5) — the invisible-bug detectors.

`agent-browser` is the alternative driver when it's already installed and
running on the host (its daemon keeps the session alive between calls). The
core loop there is: `open` → `wait --load networkidle` → `snapshot -i` →
interact via `@eN` refs → re-snapshot after every navigation:

```bash
agent-browser open <url> && agent-browser wait --load networkidle
agent-browser snapshot -i -C        # -C catches divs with onclick/cursor:pointer
agent-browser screenshot --full <name>.png
```

Command examples in the phases below are written driver-neutrally or in
agent-browser syntax; `references/playwright-engine.md` has the 1:1
translation table plus proven templates for crawl, time-to-content, the
three-viewport pass, interaction outcomes, and error capture. Whichever
driver runs, record it in `run-config.md` and the report header.

Set the viewport per pass (see Phase 3). Always capture console errors and
failed network requests — a silent 500 behind a button that "looks fine" is
a classic HIGH bug. And verify hard HTTP status with `curl` when a "Not
Found" page appears: SPAs often serve soft-404s with HTTP 200
(playwright-engine.md Template 6).

## The 6-Phase Protocol

```
Phase 0  Intake & recon           (ask questions, first-load smoke test)
Phase 1  Crawl & inventory        (map every page and interactive element)
Phase 2  Auth & gated areas       (detect walls, ask user, unlock coverage)
Phase 3  Audit sweep              (per page × per viewport: act + inspect)
Phase 4  Bug confirmation         (reproduce twice, capture evidence)
Phase 5  Report                   (markdown report + fix prompts)
```

### Phase 0 — Intake & recon

Ask the run-start questions. Then load the URL once at desktop viewport and
do a 2-minute smoke test: does the page render, does the console stay clean,
what kind of site is this (marketing page, docs, SPA, dashboard, store)?
Write `hunt-workspace/run-config.md` recording URL, stated purpose, stop
condition, mode, and viewports. Create the evidence tree:

```
hunt-workspace/
├── run-config.md
├── inventory.md
├── bugs/            (one directory per confirmed bug)
├── screenshots/     (page-slug/viewport/state.png)
└── REPORT.md
```

### Phase 1 — Crawl & inventory

Goal: a structured map of everything auditable. You can't be exhaustive
about a site you haven't mapped.

1. From the landing page, harvest every same-origin link: nav menus, footers,
   in-content links, buttons that navigate. Check `sitemap.xml` and
   `robots.txt` — free coverage.
2. Breadth-first crawl each discovered page, harvesting links as you go, until
   no new same-origin URLs appear (cap at 50 pages unless the user raises it;
   list the uncrawled remainder in the report).
3. On each page, `snapshot -i -C` and record every interactive element:
   links, buttons, form fields, dropdowns, toggles, tabs, accordions, modals,
   carousels, video players, search boxes.
4. Write `inventory.md` — one row per element:
   `| ID | Page | Element | Kind | Expected behavior (your inference) | Priority |`
   Priority: P0 = core journey (checkout, search, play button), P1 =
   secondary, P2 = edge. Infer expected behavior from labels and context —
   a button labeled "Download" that does nothing is a bug precisely because
   you wrote down what it promised.

Assign element IDs once; never renumber. Everything downstream cites them.

### Phase 2 — Auth & gated areas

When the crawl hits a login form, signup wall, or paywall:

1. Log it in the inventory as a gate.
2. If the user provided credentials, authenticate (prefer
   `agent-browser auth save` / `auth login` so the password never enters the
   transcript; `state save` to persist the session across passes and
   subagents).
3. If not, pause and ask: "I found a login at <URL>. Do you have credentials,
   or should I audit only the public surface?" Continue auditing public pages
   while waiting — never idle on a question.
4. Never brute-force, guess credentials, or bypass access controls. Gated
   areas without credentials are reported as "not covered", not as bugs.

### Phase 3 — Audit sweep (the heart of the hunt)

For every page in the inventory, at **each of three viewports**:

| Pass | Viewport | Size |
|------|----------|------|
| Desktop | 1440×900 | primary functional pass |
| Tablet | 768×1024 | layout + touch-target pass |
| Mobile | 375×812 | layout + nav-collapse pass |

Per page × viewport, in order:

1. **Load & settle** — `open` the page, wait for networkidle, then capture
   `screenshots/<page>/<viewport>/initial.png` (full-page).
2. **Visual inspection** — read the screenshot yourself (never just confirm
   it exists) and walk the `visual-inspection` skill's checklist if
   installed; otherwise apply its core checks inline: overflow/clipping,
   spacing/alignment, contrast (4.5:1 body text), truncation, touch targets
   ≥24px, broken images, empty states, horizontal scrollbars at mobile
   width, nav collapsing into a working hamburger.
3. **Functional pass** — exercise every inventory element on this page.
   Clicking is not enough; verify the *outcome* against the expected
   behavior column:
   - Links: navigate, confirm no 404/500, confirm destination matches label
   - Buttons: click, diff the snapshot (`agent-browser diff snapshot`) —
     a button that changes nothing is a finding
   - Forms: submit empty (validation should catch it), submit valid dummy
     data (should succeed or clearly explain), submit junk (no raw stack
     traces). Use obviously-fake data — never real personal information —
     and don't complete real purchases or destructive account actions.
   - Media: play/pause/seek video and audio; mute; fullscreen
   - Search: query something that exists and something that doesn't
   - Capture `after-<elementID>.png` whenever an interaction changes state
   The full desktop pass exercises everything; tablet/mobile passes re-test
   P0 elements plus anything layout-sensitive (menus, modals, carousels).
4. **Console & network check** — after the functional pass, collect console
   errors and 4xx/5xx responses observed on this page. Each unique one is a
   candidate bug even when the UI looks fine.

**Parallel mode**: dispatch one subagent per page group, each with its own
`--session <name>` so browser state never collides. Sessions are exclusive
per subagent; screenshots and inventory rows are append-only and
parallel-safe. The lead merges findings and personally reads every
screenshot cited by a subagent before accepting its findings — subagents
report, the lead verifies. Auth-gated pages share one authenticated state
file created in Phase 2.

### Phase 4 — Bug confirmation

Candidate finding → confirmed bug only after:

1. **Reproduce it a second time**, from a fresh page load, following your own
   draft steps exactly. Flaky-once issues get logged as `INTERMITTENT` with
   both attempts described.
2. **Minimal repro steps** — trim to the shortest numbered path from URL to
   defect. A stranger with a browser must be able to follow them.
3. **Evidence bundle** in `bugs/BUG-NNN/`: the "before" screenshot, the
   defect screenshot (annotated where the driver supports it), console or
   network captures when relevant.
4. **Severity**:
   - `CRITICAL` — data loss, crash, broken core journey (can't buy, can't
     log in, can't play), security-relevant exposure
   - `HIGH` — feature doesn't work as labeled, dead P0/P1 controls, broken
     layout that blocks reading or tapping
   - `MEDIUM` — wrong-but-usable: misalignment, contrast failures,
     truncation, console errors with no visible symptom
   - `LOW` — cosmetic polish
5. **De-duplicate** — same root symptom on many pages is one bug with an
   "affected pages" list, not ten bugs. (Bug-quota runs count it once.)

### Phase 5 — Report

Write `REPORT.md` using the exact structure in
`references/report-template.md` (read it before writing). The essentials:
a summary table (pages audited, elements exercised, coverage %, bugs by
severity), then one section per bug containing — in this order — title with
severity, affected URL(s) and viewport(s), numbered reproduction steps,
expected vs. actual, embedded screenshot references, and a **fix prompt**:
a self-contained, copy-pasteable prompt written for a coding agent that has
the codebase, restating the repro, evidence, and acceptance criteria (the
template has the format). Close the report with the not-covered list (gated
areas, uncrawled pages) and an intake note recording the user's stated
purpose or your inference.

Before delivering, verify: every bug has ≥1 screenshot that you personally
read, repro steps that start from a URL, and a fix prompt. Every inventory
row is marked PASS / BUG-NNN / NOT-COVERED. If the stop condition was
`bug-quota` or `time-box`, state plainly what was not audited.

## Anti-patterns

| Pattern | Why it's wrong | Instead |
|---------|----------------|---------|
| Screenshotting pages without interacting | Most bugs live behind clicks, not on first paint | Exercise every inventory element; diff snapshots |
| Marking a button PASS because the click "worked" | A click that changes nothing is the bug | Verify the outcome against expected behavior |
| Auditing desktop only | Layout bugs cluster at tablet/mobile widths | Three viewports per page, no exceptions |
| Reporting a bug seen once | Flaky repros burn the reader's trust | Reproduce twice or label INTERMITTENT |
| Padding the count with duplicates | Ten symptoms of one root cause is one bug | De-duplicate with an affected-pages list |
| Guessing credentials or probing auth | Out of scope and potentially hostile | Ask the user; report gates as not-covered |
| Trusting subagent PASS reports | Subagents summarize; evidence is the truth | Lead reads every cited screenshot personally |
| Filing "no dark mode" style absences as bugs | Absence of a feature isn't a defect on a black-box audit | Note as observation, not a bug, unless the site advertises it |

## When NOT to use

- You have the codebase and want fixes applied — use `full-ui-experience-audit`
- Single page or single screenshot review — use `ui-experience-audit` or `visual-inspection`
- API-only testing with no UI — use `functional-validation` / curl
- Performance profiling, SEO audits, or security pentesting — out of scope

## Related skills

- `agent-browser` — alternative driver; read it for command syntax and auth vault
- `visual-inspection` — the per-screenshot checklist invoked in Phase 3
- `full-ui-experience-audit` — white-box sibling that also remediates
- `ui-experience-audit` — single-screen depth protocol

## Reference files

- `references/playwright-engine.md` — default-engine setup (`scripts/setup.sh`),
  six battle-tested script templates (crawl/inventory, SPA time-to-content,
  three-viewport pass, interaction outcomes, console/network capture,
  soft-404 curl check), and the agent-browser↔Playwright translation table.
  **Read before Phase 1 when running the Playwright engine.**
- `references/report-template.md` — the exact REPORT.md and fix-prompt
  format. **Read before writing the report.**
- `references/parallel-team.md` — subagent prompts, session isolation, and
  the merge protocol. Read only when parallel mode is chosen.

## Security

- Never bypass, brute-force, or probe authentication; use only user-supplied credentials
- Never submit real personal data, complete real purchases, or trigger destructive account actions
- Redact any personal data that appears in screenshots before the report
- Never fabricate evidence — no screenshot, no bug
