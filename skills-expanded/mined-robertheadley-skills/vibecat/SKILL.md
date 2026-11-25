---
name: vibecat
description: Use when developing ScriptCat userscripts with VibeCat: build, typecheck, watch, deliver through the official sctl CLI, inspect the live page, read the tab console, and validate the exact build — entirely through the CLI, no user-side steps.
---

# VibeCat

VibeCat is a deterministic CLI-driven userscript development environment. It
owns the **project development loop** (resolve, build, typecheck, watch,
validate) and delegates **all** ScriptCat and browser communication to the
official [`sctl`](https://github.com/scriptscat/sctl) CLI.

```text
vibecat build/watch/validate ─┐
vibecat sctl <anything>  ─────┼─▶ sctl CLI ─▶ sctl serve ─▶ ScriptCat / sctl Browser
vibecat push/status/inspect ──┘
```

The user should never have to explain what VibeCat can do. If a task is on this
page, VibeCat does it — use it. And if sctl has a command VibeCat does not wrap,
reach it through `vibecat sctl …` instead of building a parallel mechanism.

## Preconditions

- `sctl` on `PATH` (or `SCTL_BIN`).
- The sctl daemon running (`sctl serve` / `sctl service start`) and ScriptCat
  paired (`sctl connect`).
- A paired sctl Browser for page inspection and execution proof.

VibeCat never starts, stops or restarts the shared sctl service. If these are
not true, `vibecat status` / `vibecat doctor` says exactly what is missing.

## What VibeCat can do

| Area | Capability |
|---|---|
| Scaffold | `vibecat init --project "<abs-path>" --match "<url-pattern>" --json`; `--settings` adds an in-page key/preference menu (GM.getValue/GM.setValue) |
| Lifecycle | `locate`, `doctor`, `bootstrap --plan/--execute`, `start`, `status`, `connect --wait`, `stop` — all JSON |
| Build & deliver | `build`, `watch --push --reload`, `push` (delivers via sctl and proves execution), `edit --replace … --with …`, `validate --browser` |
| Background/scheduled | `run <uuid>`, `logs <uuid>` (wrap `sctl run` / `sctl logs`; feature-detected) |
| Live DOM | `inspect page/landmarks/tree/element`, `query "<css>"`, `query-xpath`, `attributes`, `text`, `styles`, `rect`, `highlight` — the REAL page, including logged-in and gated pages |
| Console read-back | `events --level <lvl> --limit <n> --json` — the tab console through `sctl debug console` |
| Sandbox eval | `eval --expr "<js>"` — a userscript function in a browser-less `node:vm` sandbox |
| Live call | `call --fn "<name>" --args <json>` — invokes a function the script registered on `globalThis.__vibecatExposed`, through `sctl page eval` |
| Match diagnostics | `status.browser.matchState` (`matched`/`mismatched`/`no_tab`/`no_patterns`); push failures carry it with tailored next actions |
| Selectors | `selector suggest <handle>`, `selector test "<css>"`, `selector compare <a> <b>` |
| Mutations | `mutations start/read/clear/stop` |
| Capture | `screenshot --output "<abs.png>"` |
| **Full sctl access** | `vibecat sctl <command> [args…]` — transparent passthrough for tabs, windows, cookies, bookmarks, history, downloads, extensions, page automation, debugging, raw CDP, MCP, service and anything else |

## Default workflow — do this, don't ask the user

```text
vibecat locate --json
vibecat init   --project "<abs-path>" --match "<url-pattern>" --json
vibecat doctor --project "<abs-path>" --json        # resolve every FAIL via its remediation
vibecat start  --project "<abs-path>" --json
vibecat push   --project "<abs-path>" --reload --json
vibecat inspect landmarks --project "<abs-path>" --json
vibecat query "<selector>" --project "<abs-path>" --json
vibecat events --project "<abs-path>" --limit 20 --json
vibecat watch  --project "<abs-path>" --push --reload --json
vibecat validate --project "<abs-path>" --browser --json   # require VALIDATED
vibecat stop   --project "<abs-path>" --json
```

For pure-function iteration (search-URL / query / date logic), skip the
push-reload loop: `vibecat eval --project "<path>" --expr "buildSearchUrl(...)" --json`.

## Read all three push states

`vibecat push` reports separate states — a successful delivery is **not** a
successful execution:

- `deliveryState: DELIVERED` (sctl accepted it) — includes `uuid`, `hash`, `strategy`.
- `reloadState` — `RELOADED` / `NOT_REQUESTED` / `NO_TAB` / `FAILED:<CODE>`.
- `executionState` — `EXECUTED` only when the exact build hash was read back
  from the intended tab. Anything else → `BROWSER_EXECUTION_NOT_ACKNOWLEDGED`
  with `matchState` telling you which of wrong-URL / no-tab / stale-build it is.

## Rules — violating these stalled real sessions

- **Never assume site structure.** Write selectors only from live inspection. A
  selector that works on one page variant is not guaranteed on another; when the
  user says "it doesn't work on page X", inspect THAT page.
- **Never guess when you can verify.** Every page claim comes from `query` /
  `attributes` / `text` / `events` output.
- **Logged-in and gated pages work** — sctl attaches the debugger inside the
  user's real, authenticated browser.
- **Verbose logging is the default.** Keep the tagged `log()` helper and read it
  with `vibecat events`. Never ask the user to paste console output.
- **Never ask the user to act when VibeCat can.** No manual reloads, no "change
  ScriptCat settings" — `--reload` refreshes the page after each delivery.
- **Keys and preferences go in the in-page settings menu** (`init --settings`).
- **Background/scheduled runs have side effects.** Only `vibecat run` a script
  when the task calls for it.
- **Do not enable or change approval settings** for the user, and do not try to
  route around sctl's approval, `--yes` or confirmation semantics.
- **Userscript projects are standalone directories** — never commit them into an
  unrelated repo.

## Recovery essentials

- `SCTL_NOT_FOUND` → install sctl or set `SCTL_BIN`.
- `SCTL_DAEMON_UNREACHABLE` → the user starts it (`sctl serve` / `sctl service start`).
- `SCRIPTCAT_NOT_CONNECTED` → pair via `sctl connect`.
- `SCRIPTCAT_AMBIGUOUS` / `BROWSER_AMBIGUOUS` → pass `--scriptcat` / `--browser`.
- `BROWSER_NOT_CONNECTED` → open the matched URL (or pass `--tab`).
- `BROWSER_EXECUTION_NOT_ACKNOWLEDGED` → read `matchState` and reload/open accordingly.
- `SCTL_APPROVAL_REJECTED` / `_VOIDED` → the user declined or nothing was decided.
- `SOURCE_CONFLICT` → the installed script changed elsewhere; reconcile or `--force`.
- `SCTL_BUNDLE_TOO_LARGE` → use `vibecat edit`, or shrink the bundle.
- `SCTL_RUN_UNSUPPORTED` / `SCTL_LOGS_UNSUPPORTED` → the installed sctl is older
  than `run`/`logs`; upgrade sctl.
- `STALE_ELEMENT_HANDLE` → re-query; `STALE_BUILD` → push + reload; `BUILD_FAILED`
  / `TYPECHECK_FAILED` → fix and save (watch keeps the previous good bundle).

## Full contract

The complete operating contract — command reference, JSON schema, lifecycle
states, validation guarantees, security model and path handling — lives at
`skills/sync-scriptcat-userscripts/SKILL.md`. The sctl feature matrix and the
exact sctl/ScriptCat versions inspected are in `docs/SCTL.md`.
