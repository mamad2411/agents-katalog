---
name: awt
version: 1.8.1
description: AI-powered E2E web app testing with self-healing DevQA loop. Generate test scenarios from URLs or natural language, execute with Playwright, auto-fix failures. Supports YAML scenarios, visual matching (OpenCV + OCR), pattern learning. Use for QA, bug detection, regression testing.
---

# AWT — Eyes and Hands for Your AI Coding Tool

AWT (AI Watch Tester) gives your AI coding tool the ability to **see and interact with web applications**. Your AI designs the test strategy; AWT executes it with a real browser — clicking, typing, taking screenshots, and reporting back.

## When to Use This Skill

- User wants to **test a web application** (E2E, QA, regression)
- User says **"test it"**, **"check if it works"**, **"verify the login"**
- User needs to **detect bugs** after code changes
- User wants **automated regression testing**
- E2E test failed and user wants to **find the root cause in source code**

## When NOT to Use

- Unit testing or API-only testing (AWT is for UI/E2E)
- Performance/load testing (use k6, Artillery)
- Mobile native app testing (web and desktop only)

## ⛔ CRITICAL RULES — READ BEFORE DOING ANYTHING

1. **NEVER use `-y` or `--auto-approve`** — the user MUST approve before any test runs.
2. **NEVER use `aat devqa`** — it runs the entire pipeline without user checkpoints. Always use the 4-step workflow below.
3. **NEVER run a test without showing the scenario to the user first** and getting explicit approval (e.g. "진행해", "go ahead", "yes", "run it").
4. **NEVER auto-fix code or scenarios without user permission** — always report failures and ask the user what to do.
5. **NEVER set `headless: true`** — users MUST see the browser.
6. **NEVER guess element names** — always scan first and use real data from `scan_result.json`.
7. **NEVER start `aat loop --approval-mode auto`** — it writes AI-generated changes into
   the user's files and re-tests until the suite is green, with nobody reading them in
   between. If the user asks for an unattended fixing loop, tell them `--approval-mode
   branch` does the same thing with every change committed to a throwaway git branch
   (`git branch -D aat/fix-NNN` undoes it), and let them start it themselves.
   `--approval-mode manual` (the default) shows a fix but **writes nothing even if you
   approve it** — do not describe it as having applied anything.

---

## ★ MANDATORY 4-STEP WORKFLOW ★

When the user asks to test anything, you MUST follow these 4 steps **in order**. Do NOT skip any step. Do NOT combine steps.

### STEP 1: SCAN — Analyze the target site

```bash
aat scan --url <URL>
```

After scanning, **read `.aat/scan_result.json`** and present a summary to the user:

```
"I scanned http://localhost:3000 and found 83 interactive elements:
 - 5 input fields (email, password, search, ...)
 - 12 buttons (Login, Sign Up, Submit, ...)
 - 15 links (Home, About, Dashboard, ...)
 
 Should I create a test scenario based on these elements?"
```

**⏸️ WAIT for user response before proceeding to Step 2.**

### STEP 2: GENERATE + PRESENT — Create scenario and show it

Write a YAML scenario using the exact data from `scan_result.json`. Then **show the full scenario to the user**:

```
"Here is the test scenario I created (5 steps):

 1. 🌐 Navigate to http://localhost:3000
 2. 🖱  Type 'test@example.com' into email field
 3. 🖱  Type 'password123' into password field  
 4. 🖱  Click 'Login' button (critical)
 5. ✅ Verify URL contains '/dashboard'

 Should I run this test? Or would you like me to modify anything?"
```

**⏸️ WAIT for user approval before proceeding to Step 3.**
- If user says "modify X" → edit the scenario and show it again
- If user says "go ahead" / "진행해" / "yes" → proceed to Step 3
- If user says "cancel" → stop entirely

### STEP 3: EXECUTE — Run the approved scenario

```bash
aat run --skill-mode --fast scenarios/<scenario>.yaml
```

Monitor the output. **If any step fails:**

1. **STOP immediately** — do not continue to the next scenario
2. **Read the failure details** from the AWT output
3. **Read `ACTUAL_CAUSE` first** if the `=== AWT SKILL DEVQA ===` block has one — see below
4. **Read the SCREENSHOT** if provided in the same block
5. **Report to the user:**

```
"Test failed at Step 3 (Click Login button):
 - Error: Element 'Login' not found in DOM
 - Possible cause: The button text might be 'Sign In' instead of 'Login'
 - Screenshot: .aat/screenshots/step_003_fail.png
 
 Should I:
 (a) Fix the scenario (change 'Login' to 'Sign In') and re-test?
 (b) Fix the source code instead?
 (c) Skip this step and continue?"
```

#### `ERROR` vs `ACTUAL_CAUSE` — do not mix them up

On a critical failure the block can carry two lines:

```
ERROR: Dashboard must load after login
ACTUAL_CAUSE: Bounced to the login page: https://app.example.com/login?next=/dashboard
```

`ERROR` is the scenario author's description of what *should* have happened. It is
a label written before the run, not a finding. `ACTUAL_CAUSE` is what the browser
actually did. **Diagnose from `ACTUAL_CAUSE`**; treating `ERROR` as the cause
produces exactly the wrong diagnosis (here: "the dashboard is broken", when the
truth is that the session was never established).

When `ACTUAL_CAUSE` is absent, `ERROR` already holds the real reason.

`LOOKED_FOR` names the selector, text or image the step was hunting for — the
one fact needed to tell "the page is wrong" from "the scenario is pointing at
something that no longer exists". When `PAGE_TITLE` happens to be that very
string, a `PAGE_TITLE_NOTE` line appears beside it. Read it: a `<title>` is tab
metadata, never page text, so it cannot satisfy a text assertion. Without that
line the block reads as a contradiction and the obvious conclusion — "the text
is right there, so AWT is broken" — is the wrong one.

#### `STATUS: WARNINGS` — a step ran but changed nothing

Exit code 3, with a `=== AWT SKILL VERIFY ===` block listing each warned step.
The click was performed and did not raise, but not one pixel moved, which almost
always means it landed next to its target rather than on it. **Do not report
such a run as passed.** Read the screenshot for the warned step, check the
target it was given, and tell the user what you found. A warning left unread is
how a missed click surfaces three steps later as "the product is broken".

A `find_and_type` warning says the text went nowhere: the field was a
`<select>`, was `readonly` or `disabled`, or was still empty afterwards. The
message names which and what to use instead — a `<select>` needs
`action: select_option` with `target.selector`, not typing. Fix the scenario,
do not re-run it unchanged.

It can also say the text went into the **wrong field**, which is what a long
form produces. Two shapes, both naming the fields involved:

- *"`'…'` went into `input#suggest`, not into `input#name` which the step
  named"* — the text landed somewhere else. AWT resolves a text target to the
  one visible field whose `<label>`, wrapping label or `aria-label` **is** that
  text before trying placeholder substrings, so a labelled form sends the text
  where the page says it belongs; this still fires where no label says which
  box was meant, or where something covers the box.
- *"… which step 9 already filled for target `'비밀번호'`"* — two steps naming
  different things wrote into one box, so one of them never got a field.

The fix is the same for both: give those steps a `target.selector`. Do not
re-run unchanged and do not report the step as passed — on the run that
produced this, three such steps were counted as passes and the form came back
*"이름을 입력해주세요."* AWT also logs the ambiguity when it picks between
candidates, so the warning is usually preceded by a line naming both.

**⏸️ WAIT for user instruction before fixing or re-running.**

### STEP 4: REPORT — Summarize results

When all steps pass, report to the user:

```
"✅ Test complete: 5/5 steps passed (37.8 seconds)
 
 All navigation links and login flow are working correctly."
```

**Never report a step count that includes steps AWT did not count.** When a
scenario fails partway, the steps after the break are reported as `UNVERIFIED`,
not `PASSED`, because they ran against a screen the scenario never reached.
Report them that way:

```
"❌ Test failed at step 6 of 24.

 Step 6 could not enter the school name — the field is a <select>, so the
 value never went in and no account was created.
 The 18 steps after it are UNVERIFIED: they ran against the login screen,
 so whatever they checked, they did not check it on the signed-up state."
```

Saying "22 of 24 passed" here is the specific failure this status exists to
prevent. If the scenario should stop at that step instead of running on, propose
`critical: true` on it.

If the user wants something to keep or to hand to someone else, add
`--report pdf` to the run. It writes `reports/<scenario id>/report.pdf`, with
every step listed and the screenshots of failed and warned steps embedded in the
file, and prints the path. Do not add it by default: most runs are read in the
terminal and a report nobody asked for is a file nobody opens.

Add `--report-screenshots all` when the user wants to see the steps that worked
— a hand-off or a record of a clean run. With the default only failed and warned
steps bring their screenshots, so a report of a run where nothing went wrong
contains no images at all.

**"When did this start failing?" is answered from `.aat/runs/`, not from
`.aat/last_run.json`.** The pointer file is overwritten every run, so it only
ever describes the latest one. Each run is also filed under
`.aat/runs/<timestamp>-<nnn>_<scenarios>.json` with its status tally, newest 50
kept. Read the two or three files before the current one to say which run a
step first went red in; without them, "it used to work" is something only the
user can assert.

---

## Auto-Setup

```bash
which aat || (pip install aat-devqa && playwright install chromium)
```

---

## Scenario YAML Reference

### Writing Scenarios from scan_result.json

**Read `.aat/scan_result.json`** and write YAML using the exact element data:

```yaml
id: "SC-001"
name: "Login Flow"
steps:
  - step: 1
    action: navigate
    value: "http://localhost:3000/login"
    description: "Go to login page"

  # Use EXACT coordinates/selectors from scan_result.json
  - step: 2
    action: find_and_type
    target:
      selector: "#email"           # from scan_result.json
      text: "Email"
    value: "test@example.com"
    description: "Enter email"

  - step: 3
    action: find_and_click
    target:
      text: "Login"                # from scan_result.json
    region: main                   # exclude nav panel
    critical: true                 # stop if login fails
    description: "Click login button"

  - step: 4
    action: assert_url
    value: "/dashboard"
    on_fail: stop
    message: "Login failed — not redirected to dashboard"
    description: "Verify redirect to dashboard"
```

**Rules:**
- Use `selector` from scan data when available (most reliable)
- Use `text` as fallback (OCR-based)
- Use `region: main` for all clicks (avoid nav panel False Positives)
- Mark login/auth steps as `critical: true`
- Add `assert_url` after navigation-triggering clicks

<!-- BEGIN GENERATED: actions -->

### Actions (27 types)

| Category | Actions |
|----------|---------|
| Navigation | `navigate`, `go_back`, `refresh` |
| Find + mouse | `find_and_click`, `find_and_double_click`, `find_and_right_click` |
| Find + keyboard | `find_and_type`, `find_and_clear` |
| Direct | `click_at`, `type_text`, `press_key`, `key_combo` |
| Assert | `assert`, `assert_text`, `assert_screen_changed`, `assert_url` |
| Session | `save_session`, `load_session` |
| Input | `upload_file`, `select_option` |
| Control flow | `if_visible`, `include` |
| Query | `find`, `get_text` |
| Utility | `wait`, `screenshot`, `scroll` |

See `references/scenario-schema.md` for what each action needs.

<!-- END GENERATED: actions -->

### Key Step Options

```yaml
- action: find_and_click
  target:
    text: "Submit"               # OCR text
    selector: "#submit-btn"      # CSS selector (highest priority)
  region: main                   # top/bottom/left/right/center/main/full
  critical: true                 # stop test on failure
  on_fail: stop                  # same as critical
  method: auto                   # auto/semantics/template/ocr/vision
  match_index: 0                 # 0=first match, -1=last
  change_threshold: 0.05         # for critical auto-verification
  learn: false                   # do not remember this position (see below)
  description: "Click submit"
```

**`learn: false` — targets whose position follows the content.** AWT remembers
where a target was found and reuses that position on later runs when the step
gives no `selector`. That helps for fixed elements such as login fields, and
misfires for anything that moves with the content: buttons inside a modal whose
height follows the text, choice overlays drawn on a question image, rows in a
list. Mark those `learn: false`. Writing a `selector` is not a substitute — the
selector wins over the remembered position, but a differently named target is
still remembered under its new name.

### Text assertions: substring by default, exact only on request

`assert_text` and `assert_type: text_visible` both ask "is this text **in**
the page?". They are substring matches, so the right words wrapped in junk
pass. A quiz app that leaked its template and rendered `\(\text{질량}\)`
where it should have rendered `질량` passed `assert_text: 질량` every time —
the word really was in there, and the defect was obvious to anyone looking at
the screen and invisible to every assertion pointed at it.

When the point of the check is *how* something is rendered and not merely that
it exists, say so with `text_equals` plus a selector:

```yaml
- step: 3
  action: assert
  description: "the question shows the formula, not its LaTeX source"
  assert_type: text_equals
  value: "질량"
  target:
    selector: "#question"
```

That compares the element's whole visible text against `value`, so the leak
fails. Two things to know about it:

- **The selector is what makes it work.** With no selector it compares against
  the entire visible page, which demands the page contain nothing else. That
  form is kept for older scenarios; do not write new ones that way.
- **`text_visible` ignores the selector on purpose.** Substring-matching the
  whole page is its job. Reach for `text_equals` when you want narrowing.

`assert_text` does **not** accept hidden text. `display:none` text lives in the
DOM, and that used to be enough to pass — so a notice the code had stopped
showing went on satisfying the assertion that users could see it. Now a
selector naming a non-rendered element fails with *"in the DOM but not
visible"*, and the no-selector path requires a rendered match. A visible copy
standing behind a hidden one (a stale template above the live view) still
passes.

If a scenario of yours goes red here, read it as the assertion finally
answering the question it was written to ask.

### assert_url (login/navigation verification)

```yaml
- action: assert_url
  value: "/dashboard"
  on_fail: stop
  message: "Login failed"
  description: "Verify redirect"
```

### Access-control tests: `expect_login_redirect`

AWT normally treats "we ended up on a login page" as a hard stop, because for most
scenarios it means the session died. An access-control test wants the opposite:
being bounced to `/login` **is** the passing outcome. Mark those steps:

```yaml
- step: 2
  action: navigate
  value: "{{url}}/admin"
  expect_login_redirect: true     # landing on /login here is expected
  description: "Open an admin page while signed out"

- step: 3
  action: assert_url
  value: "/login"
  expect_login_redirect: true
  description: "Verify the guest was sent to the login page"
```

Set it per step. The same field exists at scenario level, but it switches the
detection off for every step in the file, so use it only when the whole scenario
is about access control. Omitting the field keeps the default behaviour: a step
that does not say it expects a login redirect still hard-stops on one.

### Session Reuse

```yaml
# Save after login
- action: save_session
  name: "my_app_login"

# Load in next run (24h expiry)
- action: load_session
  name: "my_app_login"
  max_age_min: 15              # fail here if the saved session is older
```

The log says how old the loaded session is ("saved 21 minutes ago").
`max_age_min` fails at the load step instead: a service that ends idle sessions
kills a saved one long before the file looks stale, and without the cap that
shows up several steps later as a login failure, sending everyone to the
credentials for nothing.

### Region Parameter

| Region | Area | Use When |
|--------|------|----------|
| `full` | Entire screen (default) | General use |
| `main` | Right 80% | **Always use for clicks** (avoids nav panel) |
| `top` | Top 30% | Header elements |
| `bottom` | Bottom 30% | Footer, floating buttons |
| `center` | Central 60%x60% | Modal dialogs |

### Content below the fold

Every screenshot AWT takes is the viewport, so a target further down the page
is not in the picture. When a visual lookup fails on the first screen, AWT now
scrolls and looks again, one screen at a time, and reports the match from the
frame it was actually found in.

This applies to the paths that read pixels — the matcher chain, self-healing
from a banked picture, and the `text_visible` OCR fallback. DOM lookups never
needed it: a CSS selector and `inner_text` already see the whole document.

- **Do not add `scroll` steps just to bring a target into view.** That is what
  this does, and a hand-tuned scroll amount breaks on a different viewport.
  Add a `scroll` only when scrolling is part of what you are testing (lazy
  loading, infinite lists, a sticky header's behaviour).
- A lookup that finds nothing puts the scroll position back, so a failing step
  does not move the page out from under the steps after it.
- The OCR fallback looks a shorter distance than the matcher chain does,
  because every missed frame costs a full Tesseract pass. For pixel-only text
  very far down a page, assert on something nearer the top first.

---

## Flutter CanvasKit Support

AWT automatically detects Flutter CanvasKit and activates Semantics:

1. After `navigate`, waits for the app to boot — CanvasKit creates its markers
   only once its WASM is up, measured at 2.6s while `navigate` returned at 0.4s
2. Clicks `flt-semantics-placeholder` (3 retries, 3s each)
3. Waits for late-arriving web fonts and the repaint they cause
4. Reads `flt-semantics[aria-label]` for element coordinates
5. Falls back to OCR if Semantics unavailable

**Do not add hand-tuned `wait` steps for Flutter.** Steps 1 and 3 above are what
those waits were compensating for. A scenario with every `wait` removed passes
against a real CanvasKit app; a `wait` tuned on one machine breaks on another.
Add a `wait` only for your app's own startup work (data fetches), not for Flutter.

**Matching priority on Flutter:**
CSS selector → Flutter Semantics → Playwright text → OCR → Vision AI

**Flutter-specific rules:**
- `find_and_click` / `find_and_type` with `target.text` work — this is the path
  to use. `target.text` must match the Semantics label, which is often the
  field's floating label (e.g. `이메일`), not its hint text
- Avoid CSS selectors and hand-written coordinates — Flutter emits no standard
  DOM elements, and coordinates break on any reflow
- `text_visible` reads the canvas with OCR when the text is not in the DOM;
  configure `matching.ocr_languages` for non-Latin scripts (default `eng+kor`).
  It scrolls down a few screens looking for it (see *Content below the fold*),
  so do not add `scroll` steps to reach canvas text
- Use `region: main` when OCR picks up navigation text
- Use `verify: true` on `type_text` (Canvas input may not render)
- Add `assert_screen_changed` after clicks
- Use `method: semantics` to force Semantics lookup

---

## Source Code Root Cause Analysis

When a test fails, trace to the source code:

1. **Read test output** — which step, what error, what URL
2. **Search codebase** — grep for the expected text, URL route, component
3. **Read the component** — find why it doesn't render/redirect/respond
4. **Propose a fix to the user** — show a concrete diff, ask for approval
5. **After user approves** — apply fix, re-build, re-scan, re-test

**Key principle:** NEVER auto-apply fixes. Always show the diff and ask.

---

## CLI Commands

| Command | Description |
|---------|-------------|
| `aat scan --url URL` | Scan page, collect elements to scan_result.json |
| `aat run --skill-mode PATH` | Execute with structured output for AI |
| `aat run --skill-mode --fast PATH` | Execute in fast DOM-first mode (Next.js, React, etc.) — a broken selector is still healed from a banked picture |
| `aat run --debug PATH` | Execute with OCR candidate debug logs |
| `aat run --report pdf PATH` | Execute and write a PDF report per scenario (failure screenshots embedded) |
| `aat doctor` | Check environment |
| `aat setup` | Configure AI + Vision providers |
| `aat validate PATH` | Validate YAML scenarios |
| `aat cost` | View AI API costs |
| `aat learned list` | Show remembered coordinates, learned patterns, and banked element pictures |
| `aat learn reset "NAME"` | Forget the coordinates remembered for one target (`--all` for every one) |
| `aat learned clear --templates` | Forget banked element pictures (`--host HOST` for one site) |

### Key Flags

```
--skill-mode    Structured output for AI assistants
--fast          DOM matching, skipping OCR and Vision AI (fastest for standard web
                apps). A broken selector still gets one deterministic attempt from
                the picture an earlier run banked for that element.
--debug         Show OCR candidates and matcher details
--strict        Treat skipped steps as failures
--learn         Record healed steps for pattern learning
--no-learn      Neither use nor update remembered coordinates in this run
--slow-mo N     Slow down actions by N ms
--report FMT    Write a report per scenario: pdf | markdown (omit for none)
--report-screenshots WHICH   Steps the PDF illustrates: failures | all | none
                             ('all' pictures the steps that worked)
```

### ⛔ Banned Flags (NEVER use these)

```
-y / --auto-approve    Bypasses user approval — NEVER USE
```

---

## Best Practices

1. **Always scan before writing scenarios** — never guess element names
2. **Use `region: main`** on all `find_and_click` — prevents nav panel False Positives
3. **Mark auth steps `critical: true`** — no point testing after login fails
4. **Add `assert_url` after form submits** — verify navigation happened
5. **Use `save_session`/`load_session`** — skip login on repeated runs
6. **Read screenshots on failure** — the SCREENSHOT path is a real PNG file
7. **Mark moving targets `learn: false`** — modal buttons, choice overlays on an
   image, list rows: their position follows the content, so remembering it makes
   the next run click empty space
7. **One fix per retry** — change only the failing step
8. **Always ask user before fixing** — never auto-modify code or scenarios

## AI Providers (for Vision AI Tier 3)

| Provider | Vision | Cost | Setup |
|----------|--------|------|-------|
| Gemini Flash | Yes | Free | `aat setup` → Gemini |
| Claude | Yes | Medium | `aat setup` → Claude |
| GPT-4o | Yes | Higher | `aat setup` → OpenAI |

Vision AI is optional — Tier 1 (template) + Tier 2 (OCR) are free and work without API keys.

## Reference Files

- `references/scenario-schema.md` — Full YAML schema
- `references/cli-reference.md` — Complete CLI reference
- `references/config-reference.md` — All configuration options
- `templates/scenario-template.yaml` — Blank scenario template
- `templates/config-template.yaml` — Default config template
