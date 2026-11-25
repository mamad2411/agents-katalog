---
name: awt
version: 1.4.0
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

## CRITICAL RULES

1. **ALWAYS use `aat devqa`** — this is the ONLY command for testing. It auto-scans, generates scenarios, runs tests, and fixes failures. Do NOT call `aat run`, `aat scan`, or `aat generate` separately.
2. **NEVER call `aat run` directly** — it skips scanning and uses stale/guessed data. Always `aat devqa`.
3. **NEVER set `headless: true`** — users MUST see the browser.
4. **NEVER guess element names** — `aat devqa` scans first and uses real data.

## Auto-Setup

```bash
which aat || (pip install aat-devqa && playwright install chromium)
```

---

## How to Test

When the user asks to test anything, run **exactly one command**:

```bash
aat devqa "test description"
```

**DO NOT** run `aat run`, `aat scan`, or `aat generate` separately. Only `aat devqa`.

`aat devqa` does everything automatically:
1. Detects running app URL (localhost port scan)
2. Scans page elements (DOM + Semantics + OCR)
3. Generates scenario from real scan data (no guessing)
4. Shows scenario, 10s auto-proceed
5. Executes with real-time progress
6. On failure: re-scans, fixes, retries (max 5)
7. On success: verifies final screenshot

Examples:
```bash
aat devqa "login and dashboard test"
aat devqa "회원가입 테스트"
aat devqa "image generation flow" --url http://localhost:8080
```

**If the URL is already known:**
```bash
aat devqa "login test" --url http://localhost:3000
```

---

## Manual Control (Advanced)

For fine-grained control, use individual commands instead of `aat devqa`:

### Step 1: Detect App URL

```
1. Check if a local dev server is running:
   - curl -s http://localhost:3000 → React/Next.js
   - curl -s http://localhost:8080 → Vue/Spring
   - curl -s http://localhost:5000 → Flask/FastAPI
   - curl -s http://localhost:PORT → any known port

2. If no server found, detect project type and start:
   - pubspec.yaml → flutter run -d chrome --web-port=8080
   - package.json → npm start / yarn dev
   - manage.py → python manage.py runserver

3. If URL detection fails → ask user:
   "What URL should I test? (e.g., http://localhost:3000)"
```

### Step 2: Scan (aat scan)

```bash
aat scan --url {detected_url}
```

This captures:
- Full-page screenshot
- All interactive elements (buttons, inputs, links)
- DOM selectors + coordinates + bounding boxes
- Flutter: Semantics labels (auto-activated)
- OCR: visible text positions

Output: `.aat/scan_result.json` — **this is the source of truth for scenario writing**.

If `scan_result.json` already exists:
```bash
aat scan --url {url} --compare .aat/scan_result.json
```
- No changes → reuse existing data
- Changes detected → use new scan

### Step 3: Write Scenario from Scan Data

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
- **First time only**: show scenario to user for approval

### Step 4: Execute

```bash
aat run --skill-mode scenarios/SC-001.yaml
```

Output format:
```
[AWT] Test started: SC-001 (12 steps)
[AWT] ✅ 1/12 Go to login page
[AWT] ✅ 2/12 Enter email
[AWT] ❌ 3/12 Click login button (critical)
[AWT] 🛑 Test stopped — Login failed
```

### Step 5: Fix and Retry

On failure:
1. **Read the SCREENSHOT** file from the `=== AWT SKILL DEVQA ===` block
2. **Re-scan** if element positions may have changed:
   ```bash
   aat scan --url {url} --compare .aat/scan_result.json
   ```
3. **Fix ONE step** in the scenario YAML
4. **Comment the fix**: `# Fixed: button text changed from "Login" to "Sign In"`
5. **Re-run**: `aat run --skill-mode scenarios/SC-001.yaml`
6. **Never repeat the same fix** — if tried before, try a different approach
7. **Max 5 attempts** (tracked by ATTEMPTS counter)

If the failure is a **source code bug** (not a scenario issue):
1. Trace from failed URL → route handler → component → fix code
2. Rebuild the app
3. Re-scan + re-run

### Step 6: Verify Success

When all steps pass, parse the `=== AWT SKILL VERIFY ===` block:
- **Read FINAL_SCREENSHOT** to confirm correct page
- Check **NAV_ZONE_WARNINGS** — clicks in left 20% may be False Positives
- If wrong page → fix scenario → retry
- If correct → report to user:
  ```
  "Test complete: 12/12 passed (2 attempts)"
  ```

### Step 7: On Repeated Failure (3+ attempts)

Report to user:
- Which step keeps failing
- What fixes were attempted
- Whether the issue is in the scenario or application code
- Suggest manual investigation with `aat scan` screenshot

---

## YAML Reference

### Actions (21 types)

| Category | Actions |
|----------|---------|
| Navigation | `navigate`, `go_back`, `refresh` |
| Find + Mouse | `find_and_click`, `find_and_double_click`, `find_and_right_click` |
| Find + Keyboard | `find_and_type`, `find_and_clear` |
| Direct | `click_at`, `type_text` (supports `verify: true`), `press_key`, `key_combo` |
| Assert | `assert`, `assert_text`, `assert_screen_changed`, `assert_url` |
| Session | `save_session`, `load_session` |
| Utility | `wait`, `screenshot`, `scroll` |

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
  description: "Click submit"
```

### assert_url (login/navigation verification)

```yaml
- action: assert_url
  value: "/dashboard"
  on_fail: stop
  message: "Login failed"
  description: "Verify redirect"
```

### Session Reuse

```yaml
# Save after login
- action: save_session
  name: "my_app_login"

# Load in next run (24h expiry)
- action: load_session
  name: "my_app_login"
```

### Region Parameter

| Region | Area | Use When |
|--------|------|----------|
| `full` | Entire screen (default) | General use |
| `main` | Right 80% | **Always use for clicks** (avoids nav panel) |
| `top` | Top 30% | Header elements |
| `bottom` | Bottom 30% | Footer, floating buttons |
| `center` | Central 60%x60% | Modal dialogs |

---

## Flutter CanvasKit Support

AWT automatically detects Flutter CanvasKit and activates Semantics:

1. After `navigate`, clicks `flt-semantics-placeholder` (3 retries, 3s each)
2. Reads `flt-semantics[aria-label]` for element coordinates
3. Falls back to OCR if Semantics unavailable

**Matching priority on Flutter:**
CSS selector → Flutter Semantics → Playwright text → OCR → Vision AI

**Flutter-specific rules:**
- Always use `region: main` (Canvas OCR picks up nav text)
- Use `verify: true` on `type_text` (Canvas input may not render)
- Add `assert_screen_changed` after clicks
- Use `method: semantics` to force Semantics lookup

---

## Source Code Root Cause Analysis

When a test fails, trace to the source code:

1. **Read test output** — which step, what error, what URL
2. **Search codebase** — grep for the expected text, URL route, component
3. **Read the component** — find why it doesn't render/redirect/respond
4. **Fix the code** — propose a concrete diff
5. **Re-build + re-scan + re-test**

**Key principle:** You have full access to the project source code. Use Grep, Glob, and Read tools aggressively.

---

## CLI Commands

| Command | Description |
|---------|-------------|
| `aat devqa "description"` | **Full auto loop**: scan → generate → test → fix → retry |
| `aat scan --url URL` | Scan page, collect elements to scan_result.json |
| `aat run --skill-mode PATH` | Execute with structured output for AI |
| `aat run --debug PATH` | Execute with OCR candidate debug logs |
| `aat doctor` | Check environment |
| `aat setup` | Configure AI + Vision providers |
| `aat hook install` | Auto-scan on git commit |
| `aat validate PATH` | Validate YAML scenarios |
| `aat cost` | View AI API costs |

### Key Flags

```
--skill-mode    Structured output for AI assistants
--debug         Show OCR candidates and matcher details
--strict        Treat skipped steps as failures
--learn         Record healed steps for pattern learning
--slow-mo N     Slow down actions by N ms
```

---

## Best Practices

1. **Always scan before writing scenarios** — never guess element names
2. **Use `region: main`** on all `find_and_click` — prevents nav panel False Positives
3. **Mark auth steps `critical: true`** — no point testing after login fails
4. **Add `assert_url` after form submits** — verify navigation happened
5. **Use `save_session`/`load_session`** — skip login on repeated runs
6. **Read screenshots on failure** — the SCREENSHOT path is a real PNG file
7. **One fix per retry** — change only the failing step
8. **Use `aat hook install`** — auto-detect UI changes on commit

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
