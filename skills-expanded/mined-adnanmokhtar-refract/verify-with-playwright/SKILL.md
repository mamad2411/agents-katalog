---
name: verify-with-playwright
description: Live-drive the running app through the Playwright MCP — three flows from the diff (happy, validation failure, unauthorised), screenshots, console errors, locale via the project's mechanism.
kind: skill
pack: frontend
allowed-tools: [Read, Grep, Glob, Bash]
---

# verify-with-playwright

## Premise

Real artifacts only. Every claim of "works" cites the screenshot file path produced + the URL navigated + the selectors waited on. "I checked it" is not verification. A 0-step run is a failure, not a pass. Console errors on load fail the run even if the screenshot looks fine. Selectors pin to roles + accessible names, not CSS classes — a verification that breaks on the next styling change is worthless.

Refuse to declare PASS without at least 1 `browser_navigate` + 1 render assertion (`browser_wait_for` on the surface's text, confirmed in a `browser_snapshot`) + 1 `browser_take_screenshot` citation.

**And the flow is read out of the diff, not remembered.** A verification composed from memory drives what you remember building — which is the part that already works. Step 2 derives it.

Real-browser verification that the change you just made actually works in the running app, through the `@playwright/mcp` server's tools — not pre-written `.spec.ts` files. Tighter feedback loop than e2e tests; complementary, not replacement.

### The tools this skill calls

Names and parameters are `@playwright/mcp` 0.0.83's own (its README tool list, npm package read 2026-10-05). In Claude Code each is exposed as `mcp__<server-name>__<tool>` — `mcp__playwright__browser_navigate` when the `.mcp.json` entry is named `playwright`. This skill's `allowed-tools` cannot pre-approve them (the repo's tool-name vocabulary has no MCP form yet), so the first call of each asks for permission unless the project's settings allow `mcp__playwright`.

| Need | Tool (core unless marked) | Shape |
|---|---|---|
| open a URL | `browser_navigate` | `{ url }` |
| read the page as roles + names; get element refs | `browser_snapshot` | `{ filename?, depth? }` — returns refs used as `target` |
| locate one element cheaply | `browser_find` | `{ text }` or `{ regex }` over the snapshot |
| wait for render / for a result | `browser_wait_for` | `{ text }`, `{ textGone }` or `{ time }` (seconds, at most 30) — waits on **text**, not a selector |
| act | `browser_click`, `browser_type`, `browser_fill_form`, `browser_select_option`, `browser_press_key` | `target` = a ref from the snapshot or a unique selector; `element` = the human description |
| frame | `browser_take_screenshot` | `{ filename, fullPage? }` — a relative filename resolves against the workspace root |
| console | `browser_console_messages` | `{ level: "error" }` |
| network | `browser_network_requests` | `{ filter }` (URL regexp), `{ static: false }` by default |
| run JS | `browser_evaluate` | `{ function: "() => …" }` |
| viewport | `browser_resize` | `{ width, height }` |
| session | `browser_set_storage_state` / `browser_cookie_set` | storage: opt-in, `--caps=storage` |
| assertions | `browser_verify_element_visible`, `browser_verify_text_visible` | testing: opt-in, `--caps=testing` |

Names from older notes — `wait_for_selector`, `screenshot`, `eval_js`, `set_viewport_size`, bare `navigate` — are not this server's tools; a call by those names fails, and a run that "skipped" them did nothing.

## When to run

- After `/add-feature` / `/add-page` / `/add-component` — confirm the new UI renders + interacts as designed.
- After `/fix-bug` for a UI bug — reproduce the user's flow, confirm it now works.
- After a router change, layout shift, or design-token swap — visually inspect at least one representative page.
- During an `/a11y-audit` — drive the page through keyboard navigation; capture focus order.
- After an i18n string update that may shift layout (Arabic / German / Japanese) — screenshot at each locale.

## When NOT to run

- Pure logic / utility / store changes with no rendered surface.
- Pre-written e2e test work — use `npx --no playwright test` (file-based) for that; this skill is for live ad-hoc verification.
- Performance benchmarking — use `lighthouse-ci` skill instead.

## Prerequisites

- **Playwright MCP server configured** in `.mcp.json` (`detect-mcp.sh --apply` writes this with the project's configured Playwright MCP server entry). Session reuse: `--storage-state=tests/.auth/user.json` on the server args, which works with `--isolated` (`visual-check`).
- **The `visual-check` harness contract** — session state at `tests/.auth/user.json`, artifacts under the gitignored `.playwright-mcp/`, and `RENDER BLOCKED` as a HALT rather than a SKIP. That skill owns those three values; this one cites them. **Do not introduce a second convention** — two session paths in one repo means one of them is always stale, and a stale `user.json` still redirects to `/login`.
- **Dev server running** — invoke `dev-server-start` first; consume its `url` output.
- **Authenticated state** if the route requires auth — either the test user credentials are in `.env.local`, or the verification flow includes login as Step 1.

## Procedure

### Step 1 — Acquire the URL

If no URL provided, invoke `dev-server-start`. Take its `url` + `pid` + `mode` output. If `mode == started-fresh`, take ownership of cleanup; if `already-running`, never kill on exit.

### Step 2 — Derive the flow from the change under test

**2a. Read the change.** `git diff --stat`, then `git diff` scoped to the touched UI files. Take exactly three things out of it:

- **Route(s)** — map each changed component path to a route through the router config or the file-system routing convention. A change with no reachable route is not verifiable here; say so instead of driving the nearest page.
- **Mutation surfaces added or changed** — a form submit, a mutation call, a destructive action.
- **Guards touched** — permission checks, `disabled` conditions, validation-schema rules.

**2b. Emit three flows, not one.** A lone happy path is where verification goes to die: it passes on the day you write it and never fails again.

| Flow | What it drives | Assertion that makes it real |
|---|---|---|
| **Happy path** | the thing the change was for | a success indicator that appears only **after** the server round-trip — not a toast fired optimistically before the response |
| **One validation failure** | submit with the field the new/changed schema rule governs left invalid | the error is rendered **and** associated (`role="alert"` or `aria-describedby` on the field), **and no mutation fired** (`browser_network_requests` shows no POST/PATCH) |
| **One unauthorised case** | the same route as a role the guard excludes | the guard fires **on direct navigation**. A hidden button is not the test — the leak a route guard exists to stop is the direct URL, so `browser_navigate` straight at it |

Where the change genuinely has no validation surface or no guard, print the lane as `n/a` with the reason (`validation flow: n/a — no schema rule changed`). A silently dropped lane and an absent lane look identical in the report, and only one of them is honest.

**2c. Compose the MCP calls.** **Pin to user-visible behavior**, not implementation. Each step is one MCP call:

```
browser_navigate      { url: <url + path> }                          # open the page
browser_wait_for      { text: "<primary heading text>" }             # confirm render
browser_snapshot      {}                                             # heading present with role=heading, name=<text>; take refs
browser_take_screenshot { filename: ".playwright-mcp/<ts>/<feature>-loaded.png" }
... browser_click / browser_type / browser_fill_form with target = the ref of role+name ...
browser_wait_for      { text: "<success text>" }
browser_network_requests { filter: "/api/<resource>" }               # the mutation fired once, with the expected status
browser_take_screenshot { filename: ".playwright-mcp/<ts>/<feature>-success.png" }
browser_console_messages { level: "error" }                          # capture console errors
```

Pin targets to roles + accessible names: read them from `browser_snapshot` (`button "Save"`, `heading "Brands"`) and pass that node's ref as `target`. A ref survives styling changes; a CSS class does not. Avoid CSS-class selectors except where they're stable design-system tokens.

### Step 3 — Execute + collect

Each tool call returns a result; halt on the first failure. When `browser_wait_for` times out, capture:
- The current screenshot (`browser_take_screenshot`, `<feature>-failure-<step>.png`).
- The console messages (`browser_console_messages`).
- The accessibility snapshot to a file (`browser_snapshot { filename }`) — what the page actually rendered.

### Step 4 — Multi-locale / multi-viewport pass

For frontend projects with `i18n` declared (codebase-profile.md § 10), repeat the flow at each locale — but **detect the project's locale mechanism first.** There are four in common use, they switch in four different ways, and a query parameter is the rarest of them:

| Mechanism | Detect it by | Switch, in-run |
|---|---|---|
| **Path prefix** (`/ar/dashboard`) — next-intl, Nuxt i18n prefix strategy | a `[locale]` / `[lang]` segment in the route tree, or a `locales` + `defaultLocale` config | `browser_navigate { url: url + '/ar' + path }` — a real navigation, which is what the router is built for |
| **Cookie or header** — next-intl without a prefix, many server-side setups | a locale cookie name in the i18n config or middleware | `browser_cookie_set { name, value }` (needs `--caps=storage`), then `browser_navigate` the same path |
| **In-app store, URL unchanged** — vue-i18n / react-i18next with a language switcher | a `locale` ref/atom in the i18n module, or a visible language switcher | **drive the switcher**: `browser_click` on the ref of `button "<language>"` from the snapshot. Same code path as a real user, and it keeps the session |
| **Per-locale build** — Angular `$localize` with one output per locale | separate build outputs / a locale-specific base href | a separate server per locale, or report `locale pass: n/a (per-locale build)` and stop |

Then, whichever mechanism was used:
```
browser_wait_for        { text: "<primary heading, translated>" }
browser_take_screenshot { filename: ".playwright-mcp/<ts>/<feature>-ar.png" }
```

**Never switch locale with `browser_evaluate` running `location.assign('/?lang=ar')`.** Two defects in one line: it assumes a `?lang=` convention that three of the four mechanisms above do not have, and `location.assign` is a **hard reload** — a session held in memory (an access token in a store rather than a cookie) does not survive it, so the run logs itself out mid-flow and screenshots the login page in Arabic. If a hard navigation is genuinely required, use `browser_navigate` and re-assert the surface-unique marker afterwards; a translated login page is a blocked render, not a locale pass.

For projects with declared breakpoints (CSS theme detection), repeat at `375px` (mobile), `768px` (tablet), `1280px` (desktop) using `browser_resize { width, height }`.

### Step 5 — Cleanup

If you started the dev server (Step 1 returned `started-fresh`), kill it:
```bash
kill "$(cat .claude/dev-server.pid)" 2>/dev/null && rm .claude/dev-server.pid
```

If `already-running`, leave it alone.

## Output format

```
verify-with-playwright — <feature/route>
  url:       http://localhost:5173/dashboard/brands
  flows:     3 (happy path + validation failure + unauthorised direct-URL)
  derived:   from diff a1b2c3d..HEAD -> src/pages/brands/* -> /dashboard/brands
  locale:    path-prefix detected (next-intl) -> navigated /ar/dashboard/brands
  steps:     22 browser_navigate/click/wait_for/snapshot
  failures:  0
  screenshots:
    - .playwright-mcp/<ts>/brands-list-loaded.png
    - .playwright-mcp/<ts>/brands-edit-saved.png
    - .playwright-mcp/<ts>/brands-delete-confirmed.png
  console:   0 errors, 1 warning ("Vue I18n missing key: Brands.exports.title")
  outcome:   PASS
```

## Failure modes

- **Text or ref not found** — common: framework still hydrating, or the accessible name changed. Capture the screenshot + `browser_snapshot` to a file; surface to the agent for a re-author of the target. Don't loop forever.
- **Console error on load** — fail loudly. UI may render but throw — that's a regression even if the screenshot looks fine. Print the error stack to the report.
- **Auth required, no credentials** — surface the missing-credentials condition; halt. Never log a fake credential or commit one.
- **Network request failure** (XHR 4xx/5xx, read from `browser_network_requests`) — log under `network_errors` in the report. Don't auto-retry — that masks real backend issues.
- **Headless vs headed mismatch** — some flows behave differently headed. `@playwright/mcp` runs **headed by default**; CI and agents pass `--headless`. If a step fails headless, suggest a headed re-run for human inspection.
- **Tool not found** — a call by a name this server does not have (§ The tools this skill calls), or an opt-in tool without its `--caps`. Name the missing capability in the report; never mark the step skipped-and-passed.
- **Locale switch logged the run out** — a hard reload discarded an in-memory session and the "Arabic" screenshot is the login page. Detect the mechanism (Step 4) rather than reloading; if a reload is unavoidable, re-assert the surface marker after it.
- **Happy path only** — the run passes, and keeps passing through every future regression in validation and authorisation because it never drove either. Step 2b's three lanes, or an explicit `n/a` per missing lane.

## Related

- `dev-server-start` — prerequisite for localhost targets.
- `visual-check` — file-based pre-written `.spec.ts`. Persistent regression suite with baselines and a locale x theme x viewport matrix. Slower; runs less often. **It owns the shared harness contract** (session file, gitignored artifact dir, blocked-render HALT) that this skill cites. Distinct premise, not a merge candidate: this skill drives a flow live with no baseline; that one proves nothing changed.
- `a11y-scan` — drives `@playwright/test` with axe-core; this skill drives the MCP tools.

## Hard rules

- **Cite the URL + path in the output.** Anyone reading the report should be able to navigate to the same page in their own browser.
- **Screenshots are ephemeral by default** — write to the gitignored `.playwright-mcp/<timestamp>/` per the `visual-check` contract. Promote a frame to `test/visual/baseline/` only when the agent + user explicitly accept a new baseline; that is a `visual-check` decision, not this skill's.
- **Never commit** `.claude/dev-server.{pid,log}` or screenshot dumps. They're per-developer.
- **Pinned selectors prefer roles + names** over CSS classes. Surfacing the rule explicitly because it's the single thing that determines whether the verification survives a styling refactor.
- **Don't fake success.** A 0-step run is a fail, not a pass. Minimum 1 `browser_navigate` + 1 `browser_wait_for` confirmed by a snapshot + 1 `browser_take_screenshot`.

## Halt conditions

- Halt if no screenshot file path is produced — verification without an artifact is unverified.
- Halt if console errors appeared on load and the report claims PASS. UI rendering is not enough; runtime errors fail the run.
- Halt if targets are CSS classes instead of snapshot refs for a role + accessible name — the verification won't survive the next styling refactor.
- Halt if a step calls a tool name `@playwright/mcp` does not expose (§ The tools this skill calls) — the step did nothing, and reporting it as run is a fabricated pass.
- Halt if the flow set carries fewer than Step 2b's three lanes and the missing ones are not printed as `n/a` with a reason. A dropped lane and an absent lane are indistinguishable in a report; only one is honest.
- Halt if the flow was composed without reading the diff — a verification derived from memory drives the path that already works, and the change under test is not what it exercised.
- Halt if a locale switch used a mechanism the project does not have (a `?lang=` parameter on a path-prefix app, a hard reload on an in-memory session). Detect first; an untranslated or logged-out screenshot is a failed switch, not a locale result.
- Halt if the Playwright MCP server is not configured in `.mcp.json` — do not silently fall back to a different tool. If another instrumented browser MCP **is** configured, name it in the halt message as the alternative the user may wire up, then stop: choosing the harness is the user's call, not the run's. A menu of four tools resolved at runtime is a soft rule wearing a hard rule's clothes.
