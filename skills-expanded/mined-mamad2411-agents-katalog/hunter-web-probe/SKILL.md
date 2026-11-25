---
name: hunter-web-probe
description: >-
  Drive a live web UI to hunt deviations and capture evidence automatically.
  Load when the target is a web surface — a route, page, form, or control — and
  you must exercise it in a real browser, not read its source. Specifies the
  Playwright driver defaults that make trace, video, and screenshots automatic;
  auth-state setup and reuse; state-assertion waiting (never fixed sleeps); the
  per-screen interaction inventory sweep; console and network capture as passive
  oracles; the three-viewport pass; and destructive-action safety. Use to probe
  a page, click through a flow, test a form, check responsiveness, or capture
  browser evidence for a Sign or Trail.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Hunter Web Probe

Assumes `hunter-doctrine` is loaded. A web deviation you cannot reproduce
through a real browser is not a Find. Reading a component's source tells you
what should render; this skill captures what does. Static reasoning produces
Signs. Only driving the UI produces the evidence a Sign needs to become a Find.

## Driver

Default driver is **Playwright, chromium, headless**, running in a network-
restricted container against an explicitly authorised target. The driver is
pluggable behind one interface — `open`, `wait-for-state`, `act`, `snapshot`,
`capture`. Some source skills mandate a different driver (e.g. `agent-browser`
where its daemon is already live, or a visible browser for local debugging).
Swap the implementation, keep the interface and the evidence contract. Record
the driver and version in the run config and every Sign; a Find that does not
name its driver is not replayable.

### Evidence-automatic settings (non-negotiable defaults)

Configure the context so evidence is captured whether or not you remember to.
Manual screenshots are for annotation; the automatic capture is the record.

```js
// browser context / test config
{
  trace: 'on',                    // full trace every run — DOM, network, console
  screenshot: 'only-on-failure',  // deviation screenshot without extra code
  video: 'retain-on-failure',     // playback of the failing interaction
  actionTimeout: 0,               // no implicit action timeout; wait on state
  navigationTimeout: 15000
}
```

Write artifacts under `run/<hunt-id>/web/<surface-slug>/`. The trace file is the
primary artifact: it carries the network log, console, and DOM at every step, so
a single `trace.zip` satisfies most of the web evidence minimum in
`hunter-doctrine`. Attach the failure screenshot beside it.

## Auth state setup and reuse

Never re-log-in per probe — it is slow and pollutes the trace. Authenticate
once, persist storage state, reuse it.

1. Perform login once through the real UI (or the sanctioned programmatic path
   the operator provided). Never guess or brute-force credentials; if none were
   provided, mark auth-gated surfaces **dark** and escalate via `hunter-ask`.
2. Save state: `await context.storageState({ path: 'run/<id>/auth/<role>.json' })`.
   The password never enters the transcript or an artifact — only the resulting
   cookies/tokens do.
3. New contexts load it: `browser.newContext({ storageState: '<role>.json' })`.
4. Capture one state file **per role**. Role coverage is part of the surface
   map; a role you never authenticated as is a dark surface, not a clean one.

## Waiting strategy — assert on state, never sleep

A fixed `waitForTimeout` is banned. It is the single largest source of flaky web
Signs, and `hunter-repro` will attribute it to the timing flake class and refuse
to promote. Wait on an observable state instead:

- Navigation settled: `waitForURL(pattern)` / `waitForLoadState('networkidle')`
- Element ready: `waitForSelector(sel, { state: 'visible' })`
- Content present: assert the specific text/value you expect, not that the DOM
  exists (`toHaveText('41 sessions')`, not `toBeVisible()` on a container)
- Request done: `waitForResponse(url => ...)` before asserting the result

If you cannot express the wait as a state assertion, you do not yet know what
"done" means for this surface — resolve that before probing.

## The interaction inventory sweep

Per screen, build a complete inventory before judging any element. Clicking is
not the probe; verifying the **outcome** against the element's promised
behaviour is the probe. A button that changes nothing is a deviation precisely
because you wrote down what its label promised.

1. Snapshot the accessibility tree and DOM; enumerate every interactive element:
   links, buttons, inputs, selects, toggles, tabs, accordions, modals,
   carousels, media controls, search boxes, and any `div` with an `onclick` or
   `cursor: pointer`.
2. Record one inventory row per element:
   `id | element | kind | expected_behaviour (your inference) | priority`.
   Priority P0 = core journey, P1 = secondary, P2 = edge. Assign ids once; never
   renumber — everything downstream cites them.
3. Exercise each element and verify the outcome, capturing a state diff:
   - **Links**: navigate; confirm no soft-404 (verify the hard HTTP status, not
     just the rendered page); confirm the destination matches the label.
   - **Buttons**: act, then diff the snapshot. No state change against a promise
     of change is a Sign.
   - **Forms**: submit empty (validation must catch it), submit valid dummy data
     (must succeed or clearly explain), submit junk (no raw stack trace). Use
     obviously-fake data only.
   - **Media/search/tabs**: exercise the actual behaviour, not just presence.
4. Mark each inventory row `cold` (probed, no deviation) or `sign/<id>`. An
   element you did not exercise is **dark** — never mark it cold.

## Passive oracles — console and network

Attach these hooks per page for the whole session. They fire without you asking
and catch invisible deviations a screenshot cannot show — a silent 500 behind a
button that "looks fine" is a classic high-severity Find.

```js
page.on('console', m => { if (m.type() === 'error') record(m); });
page.on('pageerror', e => record(e));
page.on('response', r => { if (r.status() >= 400) record(r); });
page.on('requestfailed', r => record(r));
```

Each unique console error and each 4xx/5xx is a candidate Sign even when the UI
renders correctly. Deduplicate by message + surface. Route confirmed ones to
`hunter-repro`.

## Three viewports

Layout deviations cluster at narrow widths. Probe every screen at all three; do
not audit desktop only.

| Pass | Viewport | Focus |
|---|---|---|
| Desktop | 1440×900 | primary functional pass; exercise all inventory |
| Tablet | 768×1024 | layout + touch targets; re-test P0 + layout-sensitive |
| Mobile | 375×812 | layout + nav collapse; re-test P0 + hamburger/menus |

Capture a full-page screenshot per viewport into
`web/<surface-slug>/<viewport>/`. Hand layout captures to `hunter-visual` for
measurement; this skill captures, `hunter-visual` adjudicates the pixels.

## Destructive-action safety

Some interactions are irreversible or costly. **NEVER** submit a real payment,
send a real email or message, delete data, or trigger a destructive account
action unless the operator explicitly authorised it **for this specific
target**. Absence of a "do not" is not authorisation.

When the sweep reaches such a control:

1. Stop before the terminal step. Record the control as reached and its pre-
   action state as a Sign if the affordance itself is suspect.
2. Mark the outcome surface **dark** with reason `destructive_unauthorised`.
3. Escalate via `hunter-ask` with the exact action and its cost stated. Continue
   probing non-destructive surfaces while waiting — never idle on a question.

This is a doctrine escalation trigger, not a judgement call.

## Outputs

Per surface, emit Sign records for `hunter-repro`:

```json
{
  "sign_id": "sign/0f2c",
  "surface": "GET /dashboard — 'Export' button",
  "observed": "click produces no navigation, no request, no DOM change",
  "raw_steps": [
    "open /dashboard (auth: editor)",
    "waitForSelector('[data-test=export]', {state:'visible'})",
    "click '[data-test=export]'",
    "snapshot diff: identical"
  ],
  "authority": "implicit",
  "driver": "playwright/chromium 1.47 headless",
  "artifacts": ["web/dashboard/desktop/trace.zip",
                "web/dashboard/desktop/after-export.png"],
  "viewport": "1440x900",
  "priority": "P0"
}
```

Plus a coverage line per screen stating probed/inventory as a real fraction and
listing dark elements: `dashboard: 14/17 controls probed · 3 dark (export-pdf
destructive-unauthorised, admin-delete auth-gated, print no-handler-tools)`.

## Handoff

- Confirmed Signs → `hunter-repro` for the 2-of-2 promotion and Trail.
- Layout/contrast/occlusion captures → `hunter-visual` for measurement.
- Coverage fractions and dark lists → the report's coverage map (§12 §2).

## Never

- **NEVER** submit payments, send messages, or delete data without explicit
  per-target authorisation.
- **NEVER** use a fixed sleep as a wait; assert on state.
- **NEVER** mark an unexercised element cold. Unprobed is dark.
- **NEVER** report from source reading. Only the driven browser produces
  evidence.
