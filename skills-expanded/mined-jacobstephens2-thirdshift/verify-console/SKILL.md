---
name: verify-console
description: "Verify the thirdshift Console and its HTTP API against isolated faux Command records on an ephemeral port. Use when changing src/console.rs, src/console/, src/config/console.rs, src/config/console/, or console/."
---

# Verify Console

Drive the live `thirdshift console` server against isolated faux Command records and a local stub `gh`. Every command runs inside one `( ... )` subshell that binds an OS-assigned ephemeral loopback port, owns its temporary `HOME`, and tears down the server and browser before exiting while keeping proof captures intact.

## Launch

1. Build the binary when `target/debug/thirdshift` (or `$THIRDSHIFT_BINARY`) is missing or stale, and ensure `console/node_modules` is installed:

```sh
cargo build --locked
test -d console/node_modules || npm ci --prefix console
```

2. Run verification inside one `( ... )` subshell with `trap cleanup EXIT` registered *before* starting the server or any browser daemon:

```sh
(
  set -eu
  state_dir=$(mktemp -d "${TMPDIR:-/tmp}/verify-console-state.XXXXXX")
  server_pid=''
  cleanup() {
    if [ -n "$server_pid" ] && kill -0 "$server_pid" 2>/dev/null; then
      kill "$server_pid" 2>/dev/null || true
      wait "$server_pid" 2>/dev/null || true
    fi
    rm -rf "$state_dir"
  }
  trap cleanup EXIT

  node .agents/skills/verify-console/scripts/seed-home.cjs "$state_dir"
  # No host verify-env file is sourced: seed-home.cjs stubs gh and seeds faux local data
  # under HOME="$state_dir" (leave Launch-directory .env files untouched).
  HOME="$state_dir" PATH="$state_dir/bin:$PATH" \
    "${THIRDSHIFT_BINARY:-./target/debug/thirdshift}" console --no-sign-in \
    >"$state_dir/console.out" 2>"$state_dir/console.err" &
  server_pid=$!

  origin=''
  for _ in $(seq 1 100); do
    kill -0 "$server_pid" 2>/dev/null || { cat "$state_dir/console.err" >&2; exit 1; }
    origin=$(head -n 1 "$state_dir/console.out" 2>/dev/null || true)
    case "$origin" in
      http://127.0.0.1:[0-9]*) break ;;
    esac
    sleep 0.1
  done
  case "$origin" in
    http://127.0.0.1:[0-9]*) ;;
    *) echo "Console failed to report ephemeral origin" >&2; cat "$state_dir/console.err" >&2; exit 1 ;;
  esac

  # Pass --sign-in to seed-home.cjs and omit --no-sign-in when verifying sign-in.
)
```

Set `THIRDSHIFT_CONSOLE_ASSETS=src/console/assets` in the server command only when verifying uncompiled CSS/JS asset edits in debug builds.

## Doctor

Run this read-only health check before the first drive and after any failure:

```sh
kill -0 "$server_pid"
# --no-sign-in mode:
whoami_json=$(curl -fsS "$origin/api/v1/whoami")
printf '%s' "$whoami_json" | grep -q '"api_version":"v1"'
inbox_html=$(curl -fsS "$origin/")
printf '%s' "$inbox_html" | grep -q 'acme/widgets'
```

In `--sign-in` mode, replace the `--no-sign-in` HTTP checks above with:

```sh
test "$(curl -sS -o /dev/null -w '%{http_code}' "$origin/")" = 303
test "$(curl -sS -o /dev/null -w '%{http_code}' "$origin/api/v1/whoami")" = 401
sign_in_html=$(curl -fsS "$origin/sign-in")
printf '%s' "$sign_in_html" | grep -q 'Sign in'
```

## Drive

Follow `verify-ui` (Factory: `thirdshift-verify-ui`) for the two-phase verification workflow against [features/README.md](features/README.md). Console-specific rules:

1. **Interactive exploration:** resolve Playwright from `$(pwd)/console/node_modules/playwright` (or drive with `@playwright/cli` / `agent-browser` and stop any daemon in `cleanup`). Keep default CSP enabled during exploration so real CSP regressions surface; on `/waterfall`, clicking `Zoom timeline around this call` / `Zoom out to whole Command` runs `Idiomorph.morph` on inline-styled bars (`src/console/assets/spans.js`), emitting expected `style-src 'self'` console errors — filter those `/waterfall` inline-style zoom messages only when zooming while keeping strict zero-error checks across all other Console routes.
2. **Clean walkthrough pass:** inspect `console/package.json` to follow `verify-ui` / `thirdshift-verify-ui` for recording annotations (`showActions` vs init-script fallback), and pass `bypassCSP: true` on the Phase 2 recording context only so the Console's `style-src 'self'` CSP does not block Playwright's `showActions` overlay.

## Evidence

Create proof paths outside `$state_dir` via `mktemp` (for example `"${TMPDIR:-/tmp}/after-desktop.XXXXXX.png"` and `"${TMPDIR:-/tmp}/after-desktop.XXXXXX.mp4"`) so `Cleanup` preserves them. Record only faux `seed-home.cjs` state (never capture real `~/.thirdshift/console-accounts.json` or live host data), then defer transcoding, capture pairing, and `gh --attach` PR publishing (ADR 0034) to `verify-ui` (Factory: `thirdshift-verify-ui`) and `pr` (Factory: `thirdshift-pr`).

## Cleanup

The single `trap cleanup EXIT` handler stops and waits for `$server_pid` (and any CLI browser daemon), closes Playwright contexts/browser in `finally`, removes `$state_dir` (and any temporary scripts), leaves `$shot` and `$video` intact at their `mktemp` paths, and verifies zero server or browser child processes remain after exit (`kill -0 "$server_pid"` fails).

## Helpers

- `node .agents/skills/verify-console/scripts/seed-home.cjs <mktemp-home-dir> [--sign-in]` — executable helper that seeds `.thirdshift/config.toml` (`port = 0`), faux Command records/logs/traces/spans (`acme/widgets#7`, `#8`, `#9` and `acme/gadgets#10`), a local stub `gh`, and (with `--sign-in`) faux `console-accounts.json` (`owner@example.test` / `browser test password`).
