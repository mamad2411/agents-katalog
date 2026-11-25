---
name: omowright
description: "The default code-driven browser path for interactive browsing work: drives any browser from code with token-efficient a11y snapshots (compactSnapshot drops the refs map), ref-based clicks, coordinate control (CUA), viewport pinning, CAPTCHA input helpers for reCAPTCHA, Turnstile, hCaptcha, slider and text OCR, with a human fallback (not a solver), Chrome MV3 APIs (tabs/bookmarks/history/downloads/topSites), network snoop (read API JSON instead of DOM), flight-recorder trace (jsonl + HAR + screenshots), OOPIF-aware snapshots, dialog policy, human handoff for login/OTP, device emulation, request routes, and one connectBrowser() entry that picks the engine in priority order: the user's agent browser (Aside, Ego Lite), then the user's own browser through BrowserSkill, then the owned stealth CloakBrowser with zero exposed CDP ports; each engine has its own setup check (asideOnboard, bskOnboard). MUST USE for interactive browser work: scraping, blocked/WAF/JS-rendered pages, logins, the user's logged-in sites and open tabs, extension popups, form filling, screenshots, web QA, CAPTCHAs. The ulw-research browsing lane runs on ultimate-browsing, not this skill."
---

# OmOWright

Browser automation as a code library. Install it with
`bun add github:code-yeongyu/omowright` (or import it by the path of a local
checkout). Bun >= 1.4 recommended, Node >= 22 supported.

## Pick the engine with connectBrowser

**START EVERY BROWSER TASK WITH `connectBrowser()`.** It tries the engines in
this order and returns the first that connects:

| Order | Engine                                                                                         | Handle                                     | Read                         |
| ----- | ---------------------------------------------------------------------------------------------- | ------------------------------------------ | ---------------------------- |
| 1     | **Aside**: the user's Aside browser, signed in                                                 | `AsideSession` (`run`, `open`, `snapshot`) | `references/aside.md`        |
| 2     | **Ego Lite**: an agent task space in the user's Ego browser (only inside `ego-browser nodejs`) | `BrowserConnection` (full Page API)        | `references/ego.md`          |
| 3     | **BrowserSkill**: the user's own Chrome/Edge/Brave via extension                               | `BskSession`                               | `references/browserskill.md` |
| 4     | **CloakBrowser**: owned stealth browser, no user profile                                       | `BrowserConnection`                        | `references/stealth.md`      |

```js
const { connectBrowser } = await import("omowright");
// the task needs the user's sessions: CloakBrowser may not stand in
const { engine, handle, attempts } = await connectBrowser({ allow: ["aside", "ego", "bsk"] });
```

`attempts` has one entry per engine in order: `ok`, `ms`, and `verified` (the
check that proved it attached) or the `reason` it did not (often one step only
the user can take, such as `aside login`); engines after the primary read
`not tried` when allowed, or `not allowed by the caller` when excluded from `allow`.
`crossCheck: true` also attaches the other allowed engines, returned
in `crossCheck` and listed in `attached`. Each is a SECOND BROWSER (a BrowserSkill
tab has no CDP endpoint): compare results through it, act through `handle`, and
end with `await result.closeAll()`, which closes every handle the call opened. When a
higher engine failed for a reason the user can fix, tell them that step along
with the engine you used. **SET `allow` FOR EVERY TASK**: without `"cloak"`
when it needs the user's sessions (the default includes it), with only
`["cloak"]` for scraping or WAF targets. `prefer` tries one engine first; per-engine options go
under its name (`{ cloak: { profileDir } }`). The handle type follows
`engine`, so branch on it.

## Core loop (Page API: Ego Lite and CloakBrowser)

```js
const { connectBrowser, compactSnapshot } = await import("omowright");
const { engine, handle: browser } = await connectBrowser({ allow: ["ego", "cloak"] });
const page = await browser.newTab("https://example.com");
const tree = compactSnapshot(await page.snapshot()); // ALWAYS compact before reading
await page.locator("e1").click(); // refs come from the snapshot
const changes = compactSnapshot(await page.snapshot({ diff: true }));
await browser.close(); // Ego: the user's browser stays open
```

Snapshot once, act on refs, then re-snapshot with `{ diff: true }` after each batch
of actions. Unchanged elements keep their refs. Deltas have
`{ full: false, diff: { added, changed, removed, focused } }`: added/changed entries
contain `{ ref, tree }`, removed contains refs, and focused is a ref or `null`.
Changed lines omit unchanged labels/placeholders; they show current state and value.
`compactSnapshot` marks additions with `+`, changes with `~`, and removals as ref
ranges. A full result has `full: true` and a `reason` (no baseline, navigation,
changed snapshot options, unreferenced text changes, or a delta larger than the
tree). Read it as the new baseline. Baselines belong to each page; `diff: false`
returns the ordinary full snapshot and replaces its baseline.

To look for one thing on a long page, search instead of reading the whole tree:
`page.snapshot({ find: "Checkout" })` (case-insensitive text, or a RegExp matched per
line; its g and y flags are ignored) returns only
the matching lines plus `context` lines around each (default 2, up to 10), `...` between
gaps, `refs` for just those lines and `find: { query, matches }`. Zero matches is an
empty tree, not an error. A search does not move the diff baseline, and `find` cannot
be combined with `diff`. `maxChars` still caps the whole captured tree before the
search runs, so leave it off when searching a large page.

## Owned engine: CloakBrowser

When omowright owns the browser, use the CloakBrowser binary, not a plain headless shell: most real
targets sit behind WAFs or bot scoring, and CloakBrowser's source-level
fingerprint patches (Cloudflare Turnstile, FingerprintJS, BrowserScan) make it
the safe choice. Plain headless shell is the speed fallback for trivially open
pages: any Chrome/Chromium or
`~/Library/Caches/ms-playwright/chromium_headless_shell-*/.../chrome-headless-shell`.

```bash
python3 -c "import cloakbrowser; print(cloakbrowser.binary_info()['binary_path'])"
# -> ~/.cloakbrowser/chromium-<ver>/Chromium.app/Contents/MacOS/Chromium
```

For a reused authenticated profile, use `connectCloakProfile({ profileDir, fingerprintSeed })` from the package (or the `omowright-cloak --profile "$HOME/.local/share/omowright-cloak" --url <url> --once --snapshot` launcher). First use pins a fingerprint seed in a mode-`0600` metadata file inside the mode-`0700` profile; later runs reuse it and **REJECT a conflicting seed** instead of silently changing identity. It passes the fixed `--fingerprint=<seed>` plus the platform flag on every `connectPipe()` launch. The seed is an identity pin, not a credential store.

**CLOAKBROWSER ALLOWS ONE INSTANCE.** Probe before launching
(`curl -s -m 2 http://127.0.0.1:9242/json/version`). If one answers, `connectPipe`
HANGS during early init — attach with `connect()` instead. Full pattern:
`references/stealth.md`.

## Getting past obstacles

A blocked page is a rung to climb, not a reason to stop and report.

| Rung                                        | Use                                                                | Advance when                                                        |
| ------------------------------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------- |
| 1. `snapshot()` + `locator(ref)`            | Anything with a usable ref                                         | Ref absent, stale, obscured, or the click hits the wrong node twice |
| 1b. `snapshotWithLayers` / `describeLayers` | A blocking overlay explains two identical misses; dismiss it first | `@layers none`, or the overlay is gone and the click still misses   |
| 2. `createCua(page)` coordinates            | Canvas, extension popups, custom controls                          | Click misses, or screenshot and coordinates disagree                |
| 3. Pin the viewport, retry rung 2           | Coordinate drift after a resize, DPI scale, or foreign tab         | Coordinates land right but the widget still refuses input           |
| 4. `createCaptcha(page)`                    | A challenge widget is the blocker                                  | Widget solved, flow still stalls                                    |
| 5. Read the browser log                     | Browser-level failure                                              | The log names a cause outside the page                              |

**TWO IDENTICAL FAILURES SELECT THE NEXT RUNG — A THIRD IDENTICAL ATTEMPT IS A
DEFECT.** Verify after every action batch: `snapshot({ diff: true })` for DOM state,
fresh screenshot for visual state. Report a stop only when all rungs are
exhausted, naming which rung failed with what evidence.

**RUNG 5 ENDS IN A WRITTEN DIAGNOSIS, NEVER A SPECULATIVE CODE CHANGE.** A browser
process problem (missing entitlement, extension service-worker failure, FIDO
unavailable) is not fixed by editing automation code; editing it only burns a
debugging cycle.

### Pin the viewport before trusting coordinates

CUA acts in viewport pixels. When the render surface and coordinate space
disagree, every coordinate is off by a constant and retrying repeats the miss:

```js
await page._sendToTarget("Emulation.setDeviceMetricsOverride", {
  width: 1440,
  height: 900,
  deviceScaleFactor: 1,
  mobile: false,
  screenWidth: 1440,
  screenHeight: 900,
  viewport: { x: 0, y: 0, width: 1440, height: 900, scale: 1 },
});
await page.refreshViewportSize(); // -> { width: 1440, height: 900 }
```

Pin every page you act on, including tabs you did not open, then take a fresh
screenshot — coordinates read off an unpinned screenshot are stale.

## Route by task

| Task                                                                                                                       | Read                                                            |
| -------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| The user's Aside browser: REPL session, setup, failure codes                                                               | `references/aside.md`                                           |
| The user's own signed-in browser and tabs, BrowserSkill sessions, trace-free `bskSnapshot`, one-click extension onboarding | `references/browserskill.md`                                    |
| Visual browsing, coordinate UI, viewport pinning, extension popups                                                         | `presets/visual-browse/SKILL.md` — consider delegating, below   |
| CAPTCHA (checkbox, slider, text OCR, image grid)                                                                           | `presets/captcha/SKILL.md` — consider delegating, below         |
| WAF/Cloudflare/bot-detection pages, CloakBrowser, cookie rules                                                             | `references/stealth.md`                                         |
| First use, page API, snapshot options, locator rules                                                                       | `references/quickstart.md`; dialogs and readiness in `TOOLS.md` |
| Driving a browser inside `eval` cells, kernel persistence, parallel lanes                                                  | `references/eval-kernel.md`                                     |
| Tabs/windows/bookmarks/history/downloads/topSites (Chrome MV3)                                                             | `presets/chrome/SKILL.md`                                       |
| Tab, popup and download lifecycle as push events, manager-owned background tabs (no polling)                              | `presets/agent-events/SKILL.md`                                 |
| A user-driven CloakBrowser profile that needs MV3 Chrome writes/events through the native-messaging bridge                | `presets/cloak-bridge/SKILL.md`                                 |
| API JSON instead of DOM scraping, wait for a request, infinite scroll, QA flight trace (jsonl/HAR), request routes         | `presets/network/SKILL.md`                                      |
| Cross-origin iframes and shadow DOM, overlays that swallow clicks, login/OTP handoff to a human, device emulation          | `references/frames-layers-human.md`                             |
| Reading an item from the 1Password web vault (tab-scoped session, sign-in check, secret handling)                          | `references/1password.md`                                       |

Preset and `TOOLS.md` paths are relative to the package root.

## Hard rules

- **NEVER extract and inject cookies for Google (any property) or 1Password.**
  Google's risk engine kills the session server-side and logs the user out of
  their own browser; 1Password sessions are device-bound and never work from
  cookies. Detail in `references/stealth.md`. Cookie reuse is fine for ordinary
  sessions (Grafana, internal tools).
- **Always `compactSnapshot()`** before sending a snapshot to a model — the refs
  map resolves in-page, so dropping it is free; it was 7% to 64% of the bytes
  across pages measured on 2026-11-09.
- **Refs die on every new snapshot.** Pass `page.locator("e1")` straight from the
  latest snapshot; never reuse a ref across snapshots, never put one in CSS.
- **Refs stay page-level.** Child-frame refs look like `f1e3` and still go to
  `page.locator("f1e3")`; never fetch a frame handle to click inside an iframe.
- Dialogs never block: `alert/confirm/prompt/beforeunload` are answered by the
  dialog policy (default accept: `confirm() -> true`, `prompt() -> ""`). Change
  it with `connectPipe({ dialogPolicy })`, `connect(url, { dialogPolicy })` or `browser.setDialogPolicy()`;
  observe with `page.on('dialog')`, or answer inline with
  `page.on('dialog', d => d.accept(text))` (a listener's answer replaces the
  policy). Details in `TOOLS.md`.
- `goto` waits for meaningful content, not `readyState`: body plus (interactive
  elements OR landmarks OR >= 20 text chars). Near-empty pages time out — use
  `page.goto(url, { waitUntil: "commit" })` for those.
- Cleanup is paired: `await browser.close()` then `rm -rf` the profile dir in the
  same `finally`.

## Delegating the pixel loop

Working through a CAPTCHA and pixel-level visual browsing are iterative (screenshot, reason,
act, verify). When that loop would consume your own context, delegate the blocked
page to a `deep` subagent that loads these references. Drive it yourself when the
flow is short or the state is already in your hands.

When every rung fails on a login, a one-time code, or a challenge the captcha
preset can't clear, the human is the fallback: `requestHuman(page, { prompt,
until })` brings the tab to front, shows a Done banner, and resumes when the
condition holds. Recipe in `references/frames-layers-human.md`.

```
task(category: "deep", run_in_background: true, prompt: `
TASK: Get past the CAPTCHA blocking <url> and return the post-solve state.
1. Read `presets/captcha/SKILL.md`, `presets/visual-browse/SKILL.md` (package
   root), and `references/stealth.md` (this skill).
2. connectPipe with the CloakBrowser binary.
3. Pin the viewport (setDeviceMetricsOverride 1440x900 + refreshViewportSize)
   before computing any coordinate.
4. createCaptcha(page) - click(bounds) for checkbox widgets, drag(from, to,
   {steps}) for sliders, readText(bounds) for text (macOS Vision OCR default).
   Image grids: page.annotatedScreenshot() + cua.click per cell.
5. VERIFY with captcha.waitFor({ until }) on an application acceptance condition;
   only outcome "matched" counts, a snapshot is not proof. Two failures of one
   strategy select the next strategy; do not repeat a third time.
STOP WHEN the page is past the challenge, or all strategies are exhausted -
then report which failed and the browser-log evidence.
DELIVERABLE: post-solve snapshot tree + screenshot path.`)
```

## Choosing this over everything else

Plain `webfetch`/`curl` is fine for one static page. The moment a page needs JS,
interaction, login, screenshots, CAPTCHAs, or WAF bypass, use this skill rather
than ultimate-browsing: one library covers tiers 1-2 with a persistent browser,
smaller snapshots, and no agent-browser/CloakBrowser CLI plumbing. For
ulw-research browsing lanes, spawn `deep` lanes that `import()` this package in
eval cells — the browser persists across cells via `globalThis`, and
`compactSnapshot` keeps dozens of pages inside the context budget.
