---
name: verify-site
description: "Verify the thirdshift static site (site/ and docs/guide.md) on an ephemeral loopback port. Use when changing site/, docs/guide.md, GLOSSARY.md, src/prompts_page.rs, or prompts/."
---

# Verify Site

Serve `site/` locally on an OS-assigned ephemeral loopback port and drive its static and interactive pages in headless Chromium without external network requests.

## Launch

1. Regenerate derived pages first when sources changed (`npm run docs --prefix site` for `docs/guide.md`, `UPDATE_PROMPTS=1 cargo test prompts_page` for `src/prompt.rs`/`src/prompts_page.rs`/`skills/`), and ensure `site/node_modules` and freshness checks pass:

```sh
test -d site/node_modules || npm ci --prefix site
npm run docs:check --prefix site
```

2. Run verification inside one `( ... )` subshell with `trap cleanup EXIT` registered *before* starting the server or any browser daemon:

```sh
(
  set -eu
  state_dir=$(mktemp -d "${TMPDIR:-/tmp}/verify-site-state.XXXXXX")
  server_pid=''
  cleanup() {
    if [ -n "$server_pid" ] && kill -0 "$server_pid" 2>/dev/null; then
      kill "$server_pid" 2>/dev/null || true
      wait "$server_pid" 2>/dev/null || true
    fi
    rm -rf "$state_dir"
  }
  trap cleanup EXIT

  # Static site/ needs no host credentials (leave Launch-directory .env and verify-env untouched).
  node .agents/skills/verify-site/scripts/serve-site.cjs site \
    >"$state_dir/site.out" 2>"$state_dir/site.err" &
  server_pid=$!

  origin=''
  for _ in $(seq 1 100); do
    kill -0 "$server_pid" 2>/dev/null || { cat "$state_dir/site.err" >&2; exit 1; }
    origin=$(head -n 1 "$state_dir/site.out" 2>/dev/null || true)
    case "$origin" in
      http://127.0.0.1:[0-9]*) break ;;
    esac
    sleep 0.1
  done
  case "$origin" in
    http://127.0.0.1:[0-9]*) ;;
    *) echo "Site server failed to report ephemeral origin" >&2; cat "$state_dir/site.err" >&2; exit 1 ;;
  esac
)
```

## Doctor

Run this read-only health check before driving and after any failure:

```sh
kill -0 "$server_pid"
for path in / /how-it-works/ /architecture/ /docs/ /prompts/ /videos/ /styles.css; do
  curl -fsS "$origin$path" >/dev/null
done
home_html=$(curl -fsS "$origin/")
printf '%s' "$home_html" | grep -q 'Your issues become pull requests overnight.'
```

## Drive

Follow `verify-ui` (Factory: `thirdshift-verify-ui`) for the two-phase verification workflow against [features/README.md](features/README.md). Site-specific rules:

1. **Interactive exploration:** resolve Playwright from `$(pwd)/site/node_modules/playwright` (or drive with `@playwright/cli` / `agent-browser` and stop any daemon in `cleanup`). Test both `javaScriptEnabled: true` and `false` where `<details>` or fragment reveal applies, and abort external `https://**` requests (`route.abort()`) or fulfill YouTube embeds locally so runs never contact external origins.
2. **Clean walkthrough pass:** inspect `site/package.json` to follow `verify-ui` / `thirdshift-verify-ui` for recording annotations (`showActions` vs init-script fallback). Allow expected `https://**` route-abort `requestfailed` events and the missing deploy-only `/commit.txt` request on `/prompts/` (both its 404 `console` error `m.location().url.endsWith('/commit.txt')` and its `net::ERR_ABORTED` `requestfailed` on navigation when `main.js` skips reading the 404 body), asserting zero unexpected `pageerror`, `console` error, or `>= 500` responses.

## Evidence

Create proof paths outside `$state_dir` via `mktemp` (for example `"${TMPDIR:-/tmp}/after-desktop.XXXXXX.png"` and `"${TMPDIR:-/tmp}/after-desktop.XXXXXX.mp4"`) so `Cleanup` preserves them. Defer transcoding, capture pairing, and `gh --attach` PR publishing (ADR 0034) to `verify-ui` (Factory: `thirdshift-verify-ui`) and `pr` (Factory: `thirdshift-pr`).

## Cleanup

The single `trap cleanup EXIT` handler stops and waits for `$server_pid` (and any CLI browser daemon), closes Playwright contexts/browser in `finally`, removes `$state_dir` and temporary scripts, leaves `$shot` and `$video` intact at their `mktemp` paths, and verifies zero server or browser child processes remain after exit (`kill -0 "$server_pid"` fails).

## Helpers

- `node .agents/skills/verify-site/scripts/serve-site.cjs [site-dir]` — executable static HTTP server bound to `127.0.0.1:0`, printing `http://127.0.0.1:<port>` on stdout and shutting down cleanly on `SIGTERM`/`SIGINT`.
