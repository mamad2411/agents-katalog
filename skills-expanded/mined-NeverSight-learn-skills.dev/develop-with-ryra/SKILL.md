---
name: develop-with-ryra
description: Build a new service, app, API, agent, bot, script, or tool on this ryra machine. Use this WHENEVER the user wants to develop, build, scaffold, make, create, or start a new project here -- it sets up the ryra service layout (service.toml / test.toml) so the thing can be added, run, and upgraded as a managed service.
---

# Developing with ryra

When the user wants to build, make, scaffold, or create something on this machine
(a service, app, API, agent, tool, project), set it up as a ryra service so it can
be deployed and upgraded.

**Where to build:** put every new project under `~/projects/<project-name>` (one
project per directory). Create that folder and `cd` into it before scaffolding, so
all work lives under `~/projects`. Only build somewhere else if the user names an
explicit path.

1. In the project folder (under `~/projects`), run `ryra init` to generate
   `service.toml` and `test.toml`.
2. How it runs:
   - **Simple** project (a single process): run it natively.
   - **More complex** (databases, multiple containers): generate podman quadlet
     files under a `quadlets/` folder.
3. Run `ryra add` in the repo to add it as a service. Later, `ryra upgrade` to
   pull and apply updates.

## Test as you build (red-green, before you run it)

`ryra init` also generates `test.toml`. Get at least ONE test passing BEFORE you run
the service -- a working test is the proof it does what the user asked. Work
test-first, and on **one test at a time** (don't spread effort across several
half-finished tests):

**ALWAYS run tests with `ryra test <path-or-name>`** -- point it at the thing under
test (the service/project dir, or a named test from its `test.toml`). ryra runs the
test in its sandbox, which is the real signal. Do NOT skip this step, and do NOT
substitute the raw runner (`bun test`, `vitest`, `pytest`, ...) for it -- running the
runner directly is not the same as `ryra test` and does not count.

1. **Red**: write a single test for the next bit of behaviour, then RUN
   `ryra test <path-or-name>`. Confirm it FAILS first, for the right reason -- a test
   that was never red proves nothing.
2. **Green**: write the minimum code to make that one test pass; re-run
   `ryra test <path-or-name>` until it actually reports green.
3. **Refactor**: tidy the code if needed, re-running `ryra test <path-or-name>` to
   keep it green.
4. Only then run the service.

Then move to the next test and repeat. A plain test (HTTP / unit level) is enough for
most services -- you usually do NOT need end-to-end Playwright. Reach for a Playwright
e2e test only when an advanced flow (real browser, multi-step UI, auth redirects)
genuinely needs it.

## Deploying on the tailnet (the default deployment model)

A service is loopback-only (127.0.0.1) until you expose it. To make it reachable
from the user's other devices, deploy it on their **tailnet** -- the default
deployment model here. ALWAYS expose it THROUGH ryra so the control plane tracks
the exposure and the dashboard shows the real URL:

- At install:        `ryra add --tailscale`
- Already installed: `ryra config <service> --tailscale`

Both serve it at `https://<service>.<tailnet>.ts.net` (tailnet-only, automatic
HTTPS, not public). This needs a logged-in tailnet with the Tailscale API token
configured (the "publish app addresses" step in onboarding / Settings ->
Tailscale); if it isn't, point the user there first.

Do NOT run `tailscale serve` by hand to expose a service. It appears to work, but
ryra doesn't know about it, so the dashboard still shows the service as "loopback
only" and `ryra upgrade` won't preserve it. Going through `ryra ... --tailscale`
is what keeps exposure tracked and visible.

## Scaffolding a new project

Use the official latest init commands (`bun create` / framework init), not
hand-written boilerplate. Pick the stack by what you're building (all TypeScript):

- **API / service:** Bun + Hono + OpenAPI.
- **Dashboard or interactive web app:** Bun + Hono + OpenAPI backend + a simple
  SolidJS app (use React instead if it needs more standard libraries).
- **Website or marketing platform:** Astro.
- **Both pages and an app:** TanStack Start.
