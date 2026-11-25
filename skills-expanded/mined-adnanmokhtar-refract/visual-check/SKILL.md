---
name: visual-check
description: Playwright screenshot matrix across locales, themes and viewports against committed baselines; owns the auth-session contract and the blocked-render halt.
kind: skill
pack: frontend
allowed-tools: [Read, Grep, Glob, Bash, Write]
---

# visual-check

## Premise

Real artifacts only. Every claim cites the baseline file path + the actual file path + the diff file path produced. "Looks the same" without a diff image is not verification. A run that updates baselines without explicit user confirmation is forbidden — `--update-snapshots` is a deliberate decision, not a workaround for a failing run.

Refuse to declare PASS unless every combo in the matrix produced a row with either "no diff" or a diff image path.

For frontend changes. Verifies the UI renders correctly across locales, themes, and viewport sizes before shipping.

## When to run

- After any change that touches a `.vue` / `.tsx` / `.svelte` template, CSS, or design tokens.
- After an i18n string update that may shift layout (Arabic / German / Japanese often do).
- After a Tailwind config change.
- Before a release candidate goes to QA.

## Prerequisites

- Dev server running locally (or a built static preview).
- Playwright installed: `pnpm add -D @playwright/test && npx playwright install`.
- Baseline screenshots at `test/visual/baseline/` (generated on the first green run; commit them).
- A `test/visual/visual.spec.ts` that drives `page.goto` + `expect(page).toHaveScreenshot()`.
- **An authenticated session when the target surface is auth-gated** (see below). A headless/isolated browser has NO cookies or tokens, so any route behind an auth guard redirects to `/login` and you screenshot the login page, not the surface.

## Authenticated rendering (non-negotiable for auth-gated surfaces)

Most real app surfaces (dashboards, settings, anything behind `meta: { requiresAuth }` / a route guard / a `<PrivateRoute>`) are **unreachable without a session**. Rendering them requires establishing auth FIRST — otherwise the guard bounces the render to `/login` and every screenshot is worthless.

### The Playwright-MCP contract (one convention, many consumers)

Three values are fixed here and **cited, never restated**, by everything that drives a browser in this repo:

| Value | The one setting | Why it is fixed |
|---|---|---|
| Session state | `tests/.auth/user.json` | it is what `auth.setup.ts` writes, what the browser project's `use: { storageState }` names in `playwright.config`, and what the MCP `--storage-state=` arg points at — three places that must agree or the render silently lands on `/login` |
| Artifact dir | `.playwright-mcp/` (gitignored, alongside `test-results/`) | a gitignored output dir needs no cleanup, so nobody reaches for `rm -rf` and trips the destructive-command guard |
| Blocked render | `RENDER BLOCKED` = HALT, never `SKIPPED` | `SKIPPED (no harness)` and "authenticated but bounced to the login wall" are different failures with different fixes; collapsing them produces a false pass |

**Declared consumers.** These are depended on verbatim by `verify-with-playwright` and `a11y-scan` (this pack), and — when the ui-ux pack is co-installed — by `ui-sweep`, `ui-crawl-fix`, `redesign`, `art-direct`, `add-theme-variant`, `clone-design`, `design-iterate` and `ui-design-sweep`, each of which encodes this skill's blocked-render vocabulary in its own halt branch. **Changing the HALT semantics or the session path is therefore a cross-pack change** — grep those consumers in the same edit rather than leaving them on the old convention.

1. **Detect the gate.** Before rendering `$TARGET`'s route, check whether it is auth-gated (router `meta.requiresAuth`, a guard import, a redirect-to-login). If it is, you MUST authenticate before `page.goto` to the surface.
2. **Establish a session** by the cheapest available means, in order:
   - Reuse a saved **`storageState`** (`tests/.auth/user.json` — the one path this pack uses; see the contract note below) if present and still valid.
   - Otherwise perform a **login step once** and persist it: `page.goto('/login')` → fill the dev/test credentials (from an env var / `.env`, never hardcoded) → submit → `page.context().storageState({ path: 'tests/.auth/user.json' })`. Reuse it for every subsequent shot.
   - If the project already has a Playwright auth fixture / `globalSetup`, use that.
3. **Point the MCP/browser at the session.** For the Playwright MCP, this means it must NOT run `--isolated` with no session for gated routes — load the `storageState`, or drive the login step in-session. `--headless --isolated` with no auth ALWAYS lands on `/login`.
4. **Prove you landed on the surface, not the wall** (see the blocked-render halt): after `goto`, assert a surface-unique marker is present (a heading/testid that only the target renders) before you screenshot.

### Turning it on for the first time (this skill owns the scaffold)

Creds are a **secret** no generator can bake or guess, so the work splits: **this skill scaffolds the whole mechanism; the human supplies ONE secret, once.**

- **Machine scaffolds** — when the app is detected auth-gated (a router guard, `requiresAuth` meta, a `/login` redirect, `<PrivateRoute>`, an auth interceptor): drop the file below as `tests/auth.setup.ts`, gitignore `tests/.auth/`, add the `.env` slot, and surface the turn-on in the run's report.
- **Human supplies** (once) — dev/test creds in the **gitignored `.env`**: `E2E_EMAIL` / `E2E_PASSWORD` (or the project's field names). Never committed, never in a command, never pasted in chat.

**Do not delegate this.** Nothing else in this repo produces `tests/auth.setup.ts`: `/setup-project` has no auth-scaffold deliverable, and the ui-ux pack's `/ui-crawl` writes a *different* file at `tests/crawl/auth.setup.ts` for its own crawler project. If this section does not deploy it, no one does — and `scripts/detect-mcp.sh` still tells the user to regenerate the session with `npx playwright test tests/auth.setup.ts`.

Scaffold — deploy as `tests/auth.setup.ts`, parameterizing the login route + the 3 selectors to the detected form:

```ts
import { test as setup, expect } from "@playwright/test";
import fs from "node:fs";
// Load .env into process.env — dependency-free. Playwright runs in Node, which does NOT
// auto-load .env the way Vite does, so without this the creds are undefined even though
// they are IN .env. Prefer `import "dotenv/config"` if the project already has dotenv.
try {
  for (const line of fs.readFileSync(".env", "utf8").split("\n")) {
    const m = line.match(/^\s*([\w.]+)\s*=\s*(.*?)\s*$/);
    if (m && process.env[m[1]] === undefined) process.env[m[1]] = m[2].replace(/^(['"])(.*)\1$/, "$2");
  }
} catch { /* no .env file — rely on ambient env */ }
const authFile = "tests/.auth/user.json";
setup("authenticate", async ({ page }) => {
  const email = process.env.E2E_EMAIL, password = process.env.E2E_PASSWORD;
  if (!email || !password) throw new Error("Set E2E_EMAIL/E2E_PASSWORD in .env first.");
  await page.goto("/login");                          // ← detected login route
  await page.fill("#email", email);                   // ← detected email selector
  await page.fill("input[type=password]", password);  // ← detected password selector
  await page.click('button[type="submit"]');          // ← detected submit selector
  await page.waitForURL((u) => !u.pathname.includes("/login"), { timeout: 30_000 });
  // Prove a session landed, whichever store the app uses: a cookie (most server-session and
  // BFF apps, often httpOnly) or a localStorage token.
  const state = await page.context().storageState();
  const session = /sess|auth|token|sid|jwt/i;
  const ok = state.cookies.some((c) => session.test(c.name))
    || state.origins.some((o) => o.localStorage.some((e) => session.test(e.name)));
  expect(ok, "no session cookie or token after login — check creds/selectors").toBeTruthy();
  // ← detected surface marker: the strongest proof, and the only one for IndexedDB-held sessions
  // await expect(page.getByRole("heading", { name: /dashboard/i })).toBeVisible();
  fs.mkdirSync("tests/.auth", { recursive: true });
  // indexedDB: true (Playwright ≥ 1.51) also saves IndexedDB, where Firebase Auth keeps its tokens
  await page.context().storageState({ path: authFile, indexedDB: true });
});
```

Two asserts in there are the point, not decoration: the **missing-creds throw** (an empty `E2E_EMAIL` otherwise submits a blank login form and fails as "bad credentials"), and the **session-landed assert** (a login form that silently re-renders itself writes a `user.json` full of nothing, and every later render fails at the wall with a session file sitting on disk). The assert reads cookies **and** localStorage: a localStorage-only check fails every cookie-session app, which is most of them. A session held in IndexedDB passes neither; there the surface-marker assertion is the check. The name regex is a heuristic; when the project's session cookie has a neutral name, replace it with that name or with the surface-marker assertion.

Then the four ways this is wired correctly and still does not work. None are guessable, and each reads as "Playwright is broken":

1. **A `*.setup.ts` file does not match Playwright's default `testMatch`** (`*.spec` / `*.test`). `npx playwright test tests/auth.setup.ts` returns **"No tests found"** — success-shaped output for a run that never happened. It needs a `setup` project, and the browser project must depend on it:
   ```ts
   projects: [
     { name: "setup", testMatch: /.*\.setup\.ts/ },
     { name: "chromium", dependencies: ["setup"],
       use: { ...devices["Desktop Chrome"], storageState: "tests/.auth/user.json" } },
   ]
   ```
   `storageState` is a **`use:`** option. Placed beside `dependencies` at the project level it is not a project property, so every test starts signed out while the setup project reports green.
   Then, dev server up: `npx playwright test --project=setup` writes `tests/.auth/user.json`.
2. **A project that already has its own setup file usually has not loaded `.env`.** Same Node-vs-Vite trap as above — creds that are demonstrably in `.env` arrive as `undefined`. Add the loader (or `import "dotenv/config"`) to *their* file rather than shipping a second one.
3. **`--storage-state=tests/.auth/user.json` is compatible with `--isolated`** on the Playwright MCP. The two are routinely assumed to be mutually exclusive, which is why gated renders get run isolated-with-no-session and land on `/login`.
4. **A stale `user.json` still redirects to `/login`** on JWT/session expiry, with everything correctly wired. The symptom is identical to never having set it up; the fix is re-running step 1, not re-scaffolding.

So a new project's first auth-gated render is gated on exactly one human action — dropping creds into `.env` — and everything else is scaffolded and reused.

## Procedure

0. **Browser preflight — do this FIRST.** Playwright needs its browser binary installed *separately* from the npm package. If a run (or the Playwright MCP) errors with `browserType.launch: Executable doesn't exist` / `Please run the following command to download new browsers`, the browser is **missing, not broken** — run `npx playwright install chromium` once (per machine, and again after a Playwright version bump), then retry. This is a one-command fix: NEVER report the surface as "can't verify / no session / can't drive Playwright" for this reason, and never substitute a faked screenshot. Cheap check: `npx playwright install --dry-run chromium` (or just attempt the launch and read the error).
1. Confirm the dev server URL (default `http://localhost:3000`) and that it serves all declared locales.
2. Run the visual suite — full or scoped:
   ```bash
   # All routes, all combos
   npx playwright test test/visual/
   # One route
   npx playwright test test/visual/ -g 'products'
   # Update baselines after an intentional change
   npx playwright test test/visual/ --update-snapshots
   ```
3. The matrix per route:
   - Locales: every entry in `i18n.config.ts` (`en`, `ar`, ...).
   - Themes: `light` + `dark` (if supported).
   - Viewports: mobile (375x667), tablet (768x1024), desktop (1280x800).
4. For each combo, Playwright compares pixel diff vs baseline; threshold from `playwright.config.ts` (`maxDiffPixelRatio`).
5. Inspect failures:
   ```bash
   npx playwright show-report   # opens HTML diff viewer with side-by-side baseline / actual / diff
   ```
6. After confirming the change is intentional, regenerate baselines and commit them with a message that explains the visual delta.

## Output

```
Running 18 tests using 4 workers

  PASS  /dashboard  en  light  mobile     no diff
  PASS  /dashboard  en  light  desktop    no diff
  PASS  /dashboard  en  dark   desktop    no diff
  FAIL  /dashboard  ar  light  mobile     12.3% pixel diff   (RTL layout shift)
        Snapshot: test/visual/baseline/dashboard-ar-light-mobile.png
        Diff:     test/visual/diffs/dashboard-ar-light-mobile.png
  PASS  /dashboard  ar  light  desktop    no diff

1 failed (1 of 18). Open report:  npx playwright show-report
```

## False positives / gotchas

- Fonts loading after the first paint cause pixel diff — wait for `document.fonts.ready` before screenshotting.
- Time-based content (countdowns, "5 minutes ago") — mock the clock with `page.clock.install()` or freeze with stable test data.
- Animations — disable via `page.emulateMedia({ reducedMotion: 'reduce' })` in setup.
- Image sources with cache-busted query strings produce different pixels per run — pin or stub.
- RTL (Arabic, Hebrew) layout MUST be in the matrix if the app serves those locales — flipped layouts catch real bugs.
- Never run against prod. Dev server only.
- **Write artifacts to a GITIGNORED dir — never the repo root.** When driving via the Playwright MCP (`browser_take_screenshot`), save frames under `.playwright-mcp/` (the MCP's default output dir) or another gitignored path, and keep `test-results/` + `.playwright-mcp/` in `.gitignore`. Dumping `foo.png` into the repo root clutters `git status` and then tempts a `rm -rf` cleanup — which trips the project's destructive-command guard. A gitignored output dir needs **no cleanup at all**: do NOT `rm -rf` screenshots afterward.

## Blocked render = HARD HALT (never a valid screenshot, never a silent SKIP)

A screenshot is only valid if it is **of the target surface**. The most common false-pass in a real app is rendering the **login/auth wall** (or an error/403 page) because the session was missing — and then treating that image as if the surface were verified. It never is.

- **After every `goto`, verify you are on the surface** — assert a surface-unique marker (a heading, a `data-testid`, a container class the target uniquely renders) is present. If it is absent, or the page shows login fields (`input[type=password]`, a "Login"/"Sign in" button), or the URL redirected to `/login` / `/auth`, the render is **BLOCKED**.
- **A blocked render HALTS the caller. It is NOT `SKIPPED (no harness)`** — that status is only for when no render harness exists at all. Harness-present-but-blocked is a *failure to authenticate*, and the run must stop with `RENDER BLOCKED — landed on <login/redirect>, surface not verified; establish an authenticated session (storageState / login step) and re-run` — never proceed as though the surface were audited, and never save the login screenshot as the surface baseline.
- The blocked frame MAY be saved for evidence (e.g. `login-blocked.png`) — but saving it is a HALT signal, not a pass. A caller that finds a `*-blocked.png` in its artifacts has an unverified surface.

## Halt conditions

- Halt unless every combo (locale × theme × viewport) produces a row in the report with the diff file path or "no diff".
- **Halt if the rendered page is the login/auth wall or a redirect off the target route** (blocked render, above) — authenticate and re-run; do NOT downgrade to SKIPPED or treat the login screenshot as the surface.
- Halt if `--update-snapshots` was used to "fix" a failing run without explicit user approval — that's masking a regression.
- Halt if no baseline exists yet AND the run claims PASS — the first run only generates baselines, it cannot verify them.
- Halt if RTL locales are declared in `i18n.config.ts` but absent from the matrix — flipped layouts must be tested.

## Baseline registration

Register the committed screenshot baselines in the behavioural-baseline registry (`.claude/baselines/main/manifest.json`, proposal §7) as kind `visual`, one entry per route group:

```bash
bash .claude/scripts/baseline-capture.sh register --id=visual-dashboard --kind=visual \
  --engine=frontend/visual-check --scope='src/pages/dashboard/**,src/components/**,src/styles/**,tailwind.config.*' \
  --command='npx playwright test test/visual/ -g dashboard' \
  --artifact=test/visual/baseline --compare=exit --cadence=nightly --no-capture
```

- `--compare=exit` hands the comparison to Playwright: exit 0 means `toHaveScreenshot` matched the committed baselines. `--artifact` is the directory this suite already commits (`test/visual/baseline/` here, `<spec>-snapshots/` under Playwright's default path template), never a copy. `--no-capture` leaves it alone.
- **Cadence.** Captured nightly and at P5 for the routes a run touches. Compared in CI by `behavior-diff.py --gate=G14 --ci`; visual is not a quick kind, so it does not run at Stop.
- A route that changes on purpose is declared by an acceptance criterion, `changes_baseline: ["visual-dashboard"]`, or a pattern over its baseline files. That is the "declared in `ux.md`" the proposal asks for. `--update-snapshots` is never the fix: a re-recorded baseline with no criterion naming it fails `test-integrity.py` (`undeclared-baseline-rewrite`), and the halt above still applies.

## Related

- `verify-with-playwright` — the ad-hoc live-drive sibling: no baselines, no matrix, one flow verified now. It cites this skill's session + artifact contract rather than defining its own. Use it to answer "does this work?"; use this skill to answer "did anything change?".
- `dev-server-start` — prerequisite for any localhost target; reuse an already-running server rather than booting a second one.
- `a11y-scan` — the same route x theme x locale matrix, graded by axe instead of by pixels. Both are blocked by the same login wall and share the halt above.
- `component-playground` — renders a single component in isolation; this skill renders the real routes.
- `i18n.md` (ai-pattern) — the declared locale set that makes the RTL row of the matrix mandatory.
- Cross-pack (`ui-ux`, when co-installed): `ui-sweep`, `ui-crawl-fix`, `design-iterate`, `ui-design-sweep`, `redesign`, `art-direct`, `add-theme-variant`, `clone-design` all drive this harness — see the declared-consumers note above before changing its semantics.
