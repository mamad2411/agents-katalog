---
name: browse-stealth
version: 3.0.0
description: |
  Reach sites that BLOCK ordinary automation — the same navigate/inspect/interact/report loop as the
  `browse` skill, but on browse's camoufox runtime: a hardened Firefox with C++-level fingerprint
  spoofing, geoip, and humanized timing that passes Cloudflare Turnstile, Google "unusual traffic",
  DataDome, and PerimeterX, with named profiles, authenticated sessions, and proxy rotation. Honest
  about its limit: fingerprint spoofing alone will not defeat IP-reputation blocks — pair it with a
  residential proxy. Use when a page challenges or 403s a normal browser.
allowed-tools:
  - AskUserQuestion
  - Bash
  - Read
argument-hint: "[URL or site that blocks normal browsers]"
arguments:
  - request
when_to_use: |
  Use when a target actively blocks headless browsers — CAPTCHA / "verify you are human", 403 or
  challenge pages, Google "unusual traffic", or Cloudflare/DataDome/PerimeterX protection. Do NOT use
  for sites that load fine under the base `browse` skill (camoufox is slower to start and heavier),
  for native-app targets (browse), or to author the camoufox profile itself (browse-config); reach for
  stealth only once plain browsing is actually blocked.
effort: high
---

# browse-stealth: Stealth Web Automation for AI Agents

## Target Decision — ALWAYS check this first

Before running any browse-stealth command, confirm the target matches stealth's purpose:

| User wants to... | Target | Command pattern |
|---|---|---|
| Open a site behind Cloudflare/Turnstile | **Camoufox** | `browse --runtime camoufox --headed goto <url>` |
| Bypass Google "unusual traffic" block | **Camoufox** | `browse --runtime camoufox --camoufox-profile google --headed goto @google "query"` |
| Scrape a site that returns 403 or a challenge page | **Camoufox** | `browse --runtime camoufox --headed goto <url>` |
| Use a specific camoufox fingerprint or proxy profile | **Camoufox** | `browse --runtime camoufox --camoufox-profile <name> --headed goto <url>` |
| Stay logged in across stealth sessions | **Camoufox + browser profile** | `browse --runtime camoufox --camoufox-profile <n> --profile <p> --headed goto <url>` |
| Open a normal site that isn't blocked | **Default browser** | Use the `browse` skill, not this one |
| Interact with an iOS/Android/macOS app | **Native target** | Use the `browse` skill, not this one |

**Key rules:**
- **`--runtime camoufox`** selects the hardened Firefox engine with C++-level fingerprint spoofing.
- **`--headed`** is strongly recommended. Headless Firefox is easier to detect.
- **`--camoufox-profile <name>`** loads `.browse/camoufox-profiles/<name>.json`. Applied at server startup only — `browse stop` first if switching profiles.
- **`--profile <name>`** persists browser cookies/localStorage across restarts. Independent of `--camoufox-profile`.
- **Never mix `--profile` with `--session`.** `--profile` persists identity; `--session` isolates parallel agents in one server.
- **Stealth does not replace IP reputation.** Fingerprint spoofing alone will not bypass IP-based blocks. Use a residential proxy for heavily protected sites.
- **If the site loads fine without stealth, switch back to the `browse` skill.** Camoufox is slower.
- **If unsure which target to use, ASK the user.** Don't guess.

## Goal

Use the persistent `browse` CLI with the `camoufox` runtime to:

- navigate sites that block normal browsers
- pass Cloudflare Turnstile and similar anti-bot challenges
- inspect rendered content and state on protected pages
- interact with UI elements without tripping detection
- capture screenshots, console logs, and network activity
- maintain authenticated sessions across restarts
- rotate proxies and fingerprints per task

## Step 0: Verify availability and choose the stealth profile

Start by checking:

```bash
browse --version
browse --runtime camoufox doctor
```

If `browse` is not installed, stop and tell the user:

> Install it with: `npm install -g @ulpi/browse`

If camoufox is not installed, stop and tell the user:

> Install it with: `npm install camoufox-js && npx camoufox-js fetch`

Do NOT install anything automatically.

Then decide which stealth profile fits the task. Run `/browse-config` to generate one, or pick an existing preset:

| Preset | When to use |
|---|---|
| **stealth** | General anti-detection (geoip + humanize) |
| **google** | Google search, SERP scraping (geoip + humanize + random OS) |
| **scrape** | High-throughput scraping (blocks images, WebRTC, WebGL; enables cache) |
| **custom** | User walks through each option |

Then decide what kind of session you need:

- default session for normal single-agent work
- `--session <id>` for parallel agent isolation (same camoufox server)
- `--profile <name>` for persistent browser identity (cookies survive restarts)

**Success criteria**: `browse` + camoufox are available, a stealth profile is chosen, and the session/browser-profile choice fits the task.

## Step 1: Navigate safely and stabilize the page

Stop any running server (required if switching `--camoufox-profile`), then launch:

```bash
browse stop
browse --runtime camoufox --camoufox-profile <name> --headed goto <url>
```

If no named profile exists, the `camoufox` section in `browse.json` is used automatically:

```bash
browse stop
browse --runtime camoufox --headed goto <url>
```

After navigation, always stabilize before reading or interacting:

- `browse wait --network-idle` for typical pages and SPAs
- or a more specific `browse wait` condition when the page has a known signal

Important rules:

- call `browse` as a bare command on PATH
- do not use shell variables for browse command prefixes
- avoid `#id` CSS selectors; prefer `[id=foo]`
- always pass `--runtime camoufox` on follow-up commands, or set `BROWSE_RUNTIME=camoufox` in the environment
- `BROWSE_CONSENT_DISMISS=1` auto-dismisses cookie banners (useful for EU locales)

**Success criteria**: The protected page is loaded, the challenge (if any) is settled, and content is reliable.

## Step 2: Choose the cheapest effective inspection method

Use the lightest command that answers the question:

- `text` for cleaned page content
- `links` for navigation structure
- `js` for precise targeted extraction
- `console`, `errors`, and `network` for runtime debugging
- `snapshot -i` for interactive elements and stable refs
- `--serp` on Google for SERP-structured extraction without refs

Prefer `snapshot -i` before guessing selectors for interaction-heavy tasks.

Load:

- `/browse` references for full command syntax (`references/commands.md` in the `browse` skill)
- `/browse` references for speed rules (`references/guides.md`)

**Success criteria**: You have the information needed without spending unnecessary tokens or using brittle selectors.

## Step 3: Interact using refs first, selectors second

For clicks, fills, checks, selects, and similar actions:

1. prefer `browse --runtime camoufox snapshot -i`
2. interact using `@eN` refs
3. fall back to CSS selectors only when refs are unavailable

After navigation or DOM refresh:

- assume refs may be invalid
- take a fresh snapshot before continuing

Rules:

- enable `humanize: true` (or a higher number like `1.5`–`2.0`) in the profile for human-like delays
- use descriptive screenshots saved under `.browse/sessions/<id>/`
- keep stateful flows in the same session unless isolation is intentional
- use `frame` before interacting with iframe content (Turnstile lives in an iframe)

**Success criteria**: Interactions are stable, undetected, and tied to the current rendered page state.

## Step 4: Debug blockers and special cases

When things go wrong:

- use `console` and `errors` for page/runtime issues
- use `network` for request visibility (look for challenge endpoints)
- check for iframes with `challenges.cloudflare.com` in their src (Turnstile)
- check for text like "unusual traffic" or "verify you are human"

Stealth-specific escalation path when a site still blocks you:

1. raise `humanize` in the camoufox profile (try `1.5` or `2.0`)
2. switch OS fingerprint (`os: ["windows", "macos", "linux"]` for random selection)
3. add a residential proxy to the profile and `browse stop` + relaunch
4. use `--headed` if you were running headless
5. as a last resort, hand off to the user via `browse handoff` — ask first with `AskUserQuestion`

If the site loads fine at some point, switch back to the default `browse` skill for the rest of the task.

**Success criteria**: Blockers are either resolved within the stealth runtime or escalated with the correct handoff protocol.

## Step 5: Capture evidence and report clearly

When the task involves verification, capture the minimum evidence needed:

- relevant page text or structured extraction
- screenshot path when visuals matter
- console/network findings when debugging
- the exact step or selector/ref that failed when reporting issues
- the camoufox profile and proxy used, if relevant to reproducibility

Report:

- what you navigated to
- which camoufox profile and browser profile were used
- what actions you performed
- what the page actually did (including any detected challenges)
- any artifacts created such as screenshots, HAR, or video

**Success criteria**: Another engineer can reproduce the observed stealth behavior with the same profile and proxy.

## Important Rules

- The browser persists between commands; cookies, tabs, and session state carry over.
- After `goto`, wait before reading content or acting.
- `snapshot -i` is the default interaction surface, same as the normal `browse` skill.
- `--camoufox-profile` is **server-spawn-only** — switching profiles requires `browse stop` first.
- `humanize` adds random delays to clicks and typing. Set to `true` or a number (`0.5`–`2.0`).
- `geoip` spoofs location based on exit IP. When combined with a proxy, timezone/locale/geolocation derive from the proxy IP.
- Headed mode is strongly recommended — headless Firefox is easier to detect.
- IP reputation matters — fingerprint spoofing alone does not bypass IP-based blocks.
- Never mix `--profile` (persistent browser) with `--session` (shared multiplexing).
- Save screenshots under `.browse/sessions/<session-id>/` or `.browse/sessions/default/`.
- Do not install anything automatically.
- Do not modify Claude settings automatically; point the user to `browse/references/permissions.md`.

## When To Load References

- `browse/references/commands.md`
  Use for exact command syntax, flags, and extended examples — all work with `--runtime camoufox`.

- `browse/references/guides.md`
  Use for speed rules, command-choice guidance, architecture notes, and the mandatory CAPTCHA/MFA handoff protocol.

- `browse/references/permissions.md`
  Use when the user wants to pre-allow browse commands in Claude settings.

## Guardrails

- Do not add `disable-model-invocation`; stealth should stay available when the user asks.
- Do not add `context: fork`; stealth results are usually needed in the current flow.
- Do not add `paths:`; this is a generic workflow skill.
- Do not keep the full CLI manual inline; point at the `browse` skill's references.
- Do not install camoufox, proxies, or system dependencies automatically.
- Do not run `browse handoff` without explicit user confirmation.
- Do not save screenshots outside the browse session directories.
- Do not include proxy credentials or session cookies in the final report.

## Stealth Playbooks

Concrete patterns for the most common blocks. Each playbook plugs into Steps 1–5 above.

### Cloudflare Turnstile

Identify the challenge:

```bash
browse --runtime camoufox --headed goto https://target-site.com/login
browse --runtime camoufox snapshot -i
```

Look for an iframe with `challenges.cloudflare.com` in the src, a checkbox labeled "Verify you are human", or elements with `cf-turnstile` in their class/ID.

Wait for auto-resolve (humanize often passes it):

```bash
browse --runtime camoufox wait --network-idle
browse --runtime camoufox snapshot -i
```

If it persists, click the checkbox using its ref, then re-snapshot. If still blocked, raise `humanize` to `2.0`, `browse stop`, and relaunch.

### Google "unusual traffic" bypass

Use the Google-safe profile (`geoip + humanize + random OS`):

```bash
browse stop
browse --runtime camoufox --camoufox-profile google --headed goto @google "your query"
browse --runtime camoufox wait --network-idle
browse --runtime camoufox snapshot -i
```

Handle the consent dialog if it appears (click the Accept ref). Add `browse wait --network-idle` between queries to avoid rate limiting. If still blocked, the IP is flagged — rotate to a residential proxy.

### Authenticated sessions

Combine `--camoufox-profile` (fingerprint) with `--profile` (cookies):

```bash
browse stop
browse --runtime camoufox --camoufox-profile stealth --profile mysite --headed goto https://target-site.com/login
# log in once through the normal flow
```

Subsequent launches with the same `--profile` skip the login:

```bash
browse stop
browse --runtime camoufox --camoufox-profile stealth --profile mysite --headed goto https://target-site.com/dashboard
```

For automated flows, use the credential vault (`browse auth save` / `browse auth login`) — never paste credentials into command-line arguments.

### Proxy rotation

Each proxy lives in its own named camoufox profile:

```
.browse/camoufox-profiles/proxy-us.json
.browse/camoufox-profiles/proxy-eu.json
.browse/camoufox-profiles/proxy-asia.json
```

Example profile:

```json
{
  "geoip": true,
  "humanize": true,
  "proxy": {
    "server": "http://proxy:8080",
    "username": "user",
    "password": "pass"
  }
}
```

Switch regions by stopping the server and relaunching with a different profile:

```bash
browse stop
browse --runtime camoufox --camoufox-profile proxy-eu --headed goto <url>
```

Each switch requires a restart because the proxy is configured at browser launch time.

## Output Contract

Report:

1. the page or flow tested
2. the camoufox profile (and browser profile, if used)
3. the proxy region, if relevant
4. the key commands or interactions performed
5. the observed result, including any challenges encountered
6. any artifacts or blockers such as screenshots, console errors, network failures, or handoff state
