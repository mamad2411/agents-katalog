# dev/webapp-testing — skill payload

> Machine-readable contract: [`../webapp-testing.manifest.json`](../webapp-testing.manifest.json).

## What this skill does

Drives a real browser (Playwright) through a structured `scenario` of
steps — navigate, click, type, assert text/element, screenshot, capture
network requests. Returns a structured `report` with pass/fail per step,
screenshots, console messages, and matched network requests.

This is the same harness used to validate the Cowork plugin spike
end-to-end (see `docs/cowork-plugin-limitations.md`).

## When to use it

- You need a smoke test of a deployed web app after a release.
- You need to reproduce a customer-reported UI bug.
- You're running a CI verification job that needs to assert on rendered
  output, not just HTTP responses.

## When **not** to use it

- The system under test is a pure API — use HTTP tooling, not a browser.
- The test needs deep test-runner integration (fixtures, sharding) — use
  a native Playwright project, not this generic harness.

## Determinism and risk

Determinism: **medium** — flake is possible against networked systems;
the harness retries idempotent assertions with backoff. Risk: **medium**
— a scenario that submits forms or clicks "Send" will *actually* submit
and *actually* send. Scope each scenario carefully.

## How it composes

Often invoked after `dev/mcp-builder` (verify the new server) or
`design/frontend` (verify the generated UI renders).
