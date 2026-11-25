---
name: vite-browser
description: >-
  Skill router for vite-browser capability packs. Use this whenever users ask
  to debug a Vite app, inspect runtime behavior, investigate recent hot-update
  breakage, trace network regressions, or run pre-release verification. Route
  to core-debug, runtime-diagnostics, network-regression, or release-smoke
  based on the dominant failure mode.
---

# vite-browser

Route to one focused skill as early as possible. Do not run all skills by default.

## Skill routing

1. General app bug, component/state confusion, unknown broken UI:
   - `skills/vite-browser-core-debug/SKILL.md`
2. HMR/reload loops, recent code change caused failure, full reloads, stack mapping, "which update caused this":
   - `skills/vite-browser-runtime-diagnostics/SKILL.md`
3. API/data mismatch, request failures, wrong payload, auth/cookie/CORS regressions:
   - `skills/vite-browser-network-regression/SKILL.md`
4. Pre-merge/pre-release final verification:
   - `skills/vite-browser-release-smoke/SKILL.md`

## Routing rules

1. Start with `core-debug` when the symptom is broad or unclear.
2. Switch immediately to `runtime-diagnostics` if the issue is tied to a recent edit, HMR, refresh, reload, or Vite runtime instability.
3. Switch to `network-regression` if the main symptom is bad data, missing data, request failure, or request/response mismatch.
4. Use `release-smoke` only for final validation or sign-off, not root-cause discovery.

If two skills apply:

1. `core-debug` -> `runtime-diagnostics`
2. `core-debug` -> `network-regression`
3. `runtime-diagnostics` -> `network-regression` only if runtime diagnosis suggests the visible failure is downstream of an API problem

---

## Shared bootstrap for all routed skills

```bash
vite-browser open <url>
vite-browser detect
vite-browser errors --mapped --inline-source
vite-browser logs
```

Treat `errors --mapped --inline-source` as the primary error read when reproducing live runtime failures in `v0.3.3+`. It can surface browser-side runtime errors even when the Vite overlay is absent, and its output now pairs more reliably with propagation diagnosis in live Vue repros.

Then continue with the selected specialized skill and stop using the router skill.

---

## Command groups (current CLI)

### Browser

```bash
vite-browser open <url> [--cookies-json <file>]
vite-browser close
vite-browser goto <url>
vite-browser back
vite-browser reload
```

### Framework

```bash
vite-browser detect
vite-browser vue tree [id]
vite-browser vue pinia [store]
vite-browser vue router
vite-browser react tree [id]
vite-browser react store list
vite-browser react store inspect <name>
vite-browser react hook health
vite-browser react hook inject
vite-browser react commits [--limit <n>]
vite-browser react commits clear
vite-browser svelte tree [id]
```

### Runtime and Diagnosis

```bash
vite-browser vite runtime
vite-browser vite hmr
vite-browser vite hmr trace --limit <n>
vite-browser vite hmr clear
vite-browser vite module-graph [--filter <txt>] [--limit <n>]
vite-browser vite module-graph trace [--filter <txt>] [--limit <n>]
vite-browser vite module-graph clear
vite-browser errors --mapped --inline-source
vite-browser correlate errors [--window <ms>]
vite-browser correlate errors --mapped --inline-source
vite-browser correlate renders [--window <ms>]
vite-browser diagnose propagation [--window <ms>]
vite-browser diagnose hmr [--window <ms>] [--limit <n>]
```

### Utilities

```bash
vite-browser network [idx]
vite-browser screenshot
vite-browser eval <script>
```

Install CLI:

```bash
npm install -g @presto1314w/vite-devtools-browser
npx playwright install chromium
```

Install skill:

```bash
npx skills add MapleCity1314/vite-browser
```
