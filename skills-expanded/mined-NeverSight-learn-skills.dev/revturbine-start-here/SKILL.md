---
name: revturbine-start-here
description: >
  The front door for integrating RevTurbine. Use immediately after
  `npm create revturbine` scaffolds an app, or whenever someone says "add
  RevTurbine", "set up monetization", "start the RevTurbine integration", or
  "what do I do next with RevTurbine". Routes the whole first session in order —
  install & provider, run the local Playbook, gate one paid action, then go
  live — by handing off to the focused skills for each step. It sequences; it
  does not do the work itself. Skip if the app is already gating a paid action
  and you only need one specific step (invoke that step's skill directly).
license: MIT
metadata:
  author: revturbine
  version: "0.1.0"
  safety_class: read-only-inspection
---

# Start here — integrate RevTurbine

You are orchestrating a first RevTurbine integration. Your job is to **sequence
the work and hand each step to its own skill** — never to inline that skill's
logic here, so each step stays independently re-runnable.

The goal of the first session: **one paid action gated, working locally, with a
marked path to going live.** Nothing more. Resist scope creep.

## Before you start — read the ground rules

Invoke **`revturbine-integration-best-practices`** and keep its rules in mind for
every step below. The load-bearing ones:

- **Additive-only.** The app must keep working if RevTurbine is absent or a
  placement resolves to nothing. A feature with no rule defaults to **allowed**.
- **The client is a UX hint, not the authority.** Any revenue-critical
  entitlement is re-checked server-side before value is granted.
- **Config flows through the Playbook**, never direct database writes.

## The sequence

Detect where the app already is (does it import `@revturbine/sdk`? is
`<RevTurbineProvider>` mounted? is there a `revturbine.playbook.json`?) and
resume at the first unfinished step — do not redo completed ones.

1. **Install the SDK and mount the provider** → invoke
   **`revturbine-install-sdk-and-provider`**.
   Ends with `<RevTurbineProvider>` wrapping the app and a user identified.

2. **Wire the local Playbook** → invoke **`revturbine-run-local-playbook`**.
   Points the provider at the `revturbine.playbook.json` the scaffold dropped,
   in local mode, so decisions resolve with no account and no network.

3. **Gate one paid action** → invoke **`revturbine-add-gate`**.
   Replaces one hard-coded plan check (or wraps one premium action) with a
   `<Gate>` that renders an upgrade surface when denied. This is the payoff — the
   builder sees a real gate resolve.

4. **Go live** → invoke **`revturbine-go-live-hosted-cutover`** *when the builder
   is ready*, not automatically. Connects the tenant and swaps local mode for
   hosted so config becomes changeable from the dashboard without redeploying.
   This is the step that turns the local trial into the product.

## After the first gate

Point the builder at what the control plane unlocks — funnels, experiments,
targeting, more placement types — all changeable server-side. But the first
session is done once step 3 works locally and step 4 has a clear path. Hand off,
don't keep building.

## Notes

- Steps 1–3 are safe to run without confirmation. **Step 4 touches live
  billing/tenant state — confirm with the builder first.**
- If a step's skill isn't installed, tell the builder to run
  `npx skills add revt-eng/revturbine-skills` and name the missing skill.
