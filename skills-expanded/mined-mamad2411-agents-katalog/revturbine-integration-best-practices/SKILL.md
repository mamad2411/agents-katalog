---
name: revturbine-integration-best-practices
description: >
  The rules every RevTurbine integration follows. Read before wiring the SDK,
  gates, slots, or config, and consult when a change might weaken the fallback
  guarantee or move an entitlement check to the client. Use when someone asks
  "how should I integrate RevTurbine", "is this the right way to gate", or before
  reviewing a RevTurbine diff. Reference material — it does not change code.
license: MIT
metadata:
  author: revturbine
  version: "0.1.0"
  safety_class: read-only-inspection
---

# RevTurbine integration — best practices

RevTurbine decides *what a user is entitled to* and *what to render where*; your
app declares *slots and actions*. These rules keep that split safe.

## 1. Additive-only — the app must survive RevTurbine's absence

Every integration point degrades gracefully:

- If `<RevTurbineProvider>` is missing, un-wrapped components still render.
- If a placement resolves to nothing, the call site renders its **baseline UX**,
  never an error or an empty hole.
- A feature with **no entitlement rule defaults to allowed.** Rules take things
  away from a baseline of "works"; they never gate by omission.

The test: disconnect RevTurbine entirely and the product still functions, just
without the paywalls and nudges.

## 2. The client check is a UX hint; the server is the authority

`rt.can(...)`, `useEntitlement(...)`, and `<Gate>` shape the interface — show or
hide, allow or upsell. They run in the browser, so they are **advisory**.

**Any entitlement that gates real value or money** — an export that costs you
compute, a credit spend, a seat, anything a determined user could bypass by
editing client state — **must be re-checked server-side** with `rtServer.can(...)`
before the value is delivered. The gate improves the experience; the server
check protects the revenue.

## 3. Config lives in the Playbook, never in the database directly

Plans, entitlements, rules, segments, and placements are authored as the
Playbook (`revturbine.playbook.json` locally; the control plane in production)
and validated with `revturbine validate`. Never seed or mutate this config with
direct database writes — it always flows through the CLI and the import API, so
it can be reviewed, diffed, and rolled back.

## 4. Local is the trial; hosted is the destination

`local_only` mode is how a builder sees a gate resolve in five minutes with no
account. It is not where a real product stays — hosted mode is what makes config
changeable from the dashboard without a redeploy, and what powers analytics,
experiments, and targeting. Treat local mode as the on-ramp, and finish the
journey with `revturbine-go-live-hosted-cutover`.

## 5. Confirm the irreversible

Going live, promoting config between environments, and anything touching Stripe
or real pricing can move money and cannot be cleanly undone. Prepare and
validate these autonomously; **get explicit human confirmation before pulling the
final lever.**

## 6. Never weaken a guardrail to make something pass

No bypassing checks, no suppressing a surfaced failure, no direct-DB shortcut
"just this once." If a guardrail is in the way, the integration is wrong, not the
guardrail.
