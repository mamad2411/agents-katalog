---
name: local-webui-troubleshooting
description: Use when a local web UI won't open in the browser.
license: MIT
metadata:
  source_frontmatter:
    version: 1.0.0
    author: hermes
    tags:
    - webui
    - localhost
    - debugging
    - dev-server
    - browser
    - troubleshooting
    - dsh
  imported_from: hermes
---

# Local Web UI Won't Open — Debugging Playbook

## When to Use

User reports a locally-served web UI (dev server, dashboard, agent harness, dockerized app) "won't open" / 打不开, even though the CLI said it started. This is a recurring class: the CLI is often fine and the problem is on the *open* side.

## Golden Rule

**Verify the server side BEFORE any browser/network theory.** In most "打不开" cases the server is healthy and the issue is a client-side expectation (no auto-open, wrong URL, localhost-only binding). Guessing the cause before checking the port is exactly the fabricated-causality the user rejects — always produce measured facts first.

## Step 1 — Is the server actually listening?

```bash
lsof -nP -iTCP:<port> -sTCP:LISTEN
```

- Nothing → the process died or never bound. Check its log for first-run provisioning errors (plugin fetch, profile creation can take 20s+ silently).
- PID present but not the process you started → port conflict; an older instance owns the port.

## Step 2 — Does it answer HTTP?

```bash
curl -sS -o /dev/null -w "%{http_code}" http://127.0.0.1:<port>/
```

- `200` → server healthy; the problem is on the open side. Proceed to Step 4.
- Connection refused → bound elsewhere, died after a delay, or host mismatch.

## Step 3 — Are the assets real?

Fetch one resource referenced by the returned HTML (first JS bundle path in the page source, e.g. a `/plugins/<pkg>/client.js` URL):

```bash
curl -sS -o /dev/null -w "%{http_code} (%{size_download}B)\n" http://127.0.0.1:<port>/plugins/<pkg>/client.js
```

200 with non-trivial size → the app is fully serving; a subsequent blank page is a client-side JS issue, not a server outage.

## Step 4 — The open-side causes, in order of likelihood

1. **CLI doesn't auto-open a browser.** Many CLIs (`dsh web`, various dev servers) print the URL and keep serving but never spawn a tab. Check `--help` for an `--open`/`--launch` flag; if absent, the fix is telling the user to paste the URL manually.
2. **localhost-only binding.** Server listens on `127.0.0.1` → unreachable from other devices/phones. Fix with `--host 0.0.0.0` and give the LAN IP.
3. **Foreground process died.** User closed the terminal or Ctrl+C'd the server; restart it (background/daemon if needed).
4. **Browser/system proxy hijacks localhost.** Some proxies route `localhost` away; try the literal `http://127.0.0.1:<port>` or an off-proxy browser profile.

## Step 5 — Report and confirm

State the verified facts (port listening, HTTP code, asset fetch result), name the most likely open-side cause, and ask for the exact symptom (ERR_CONNECTION_REFUSED / blank page / infinite spinner) before going deeper. Don't end with speculation.

## Reference

- `references/deepseek-harness-dsh.md` — dsh (DeepSeek Harness) install, profiles, web UI specifics

## Pitfalls

- Never conclude "service is broken" from "user can't open it" alone — run lsof + curl first and report the numbers.
- A background process started from an agent session dies with that session. "It's running right now" is not "it will be running when the user looks later" — tell the user to run it from their own terminal for persistence.
- First boot of plugin-based harnesses can take 20–30s with no output while provisioning (pnpm fetch, profile creation). Give it time before declaring it hung.
