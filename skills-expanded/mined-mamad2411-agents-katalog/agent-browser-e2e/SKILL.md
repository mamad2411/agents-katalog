---
name: agent-browser-e2e
description: "[INTERNAL TEMPLATE] E2E verification execution protocol. Called by agent-browser orchestrator."
---

# E2E Verification — Execution Protocol

> **Internal template.** Entry point: `agent-browser` skill.

---

## NEVER

```
NEVER assert state before `wait --load networkidle` — page may still be rendering
NEVER reuse refs after navigation — run `snapshot` again after every page change
NEVER leave `set offline on` after offline test — always restore with `set offline off`
NEVER skip `errors` check before test steps begin — pre-existing JS errors invalidate results
```

---

## Execution Sequence

```bash
# 1. Open and wait for stable state
AGENT_BROWSER_NATIVE=1 agent-browser open <url>
AGENT_BROWSER_NATIVE=1 agent-browser wait --load networkidle

# 2. Check for errors before any interaction
AGENT_BROWSER_NATIVE=1 agent-browser errors          # → judgment gate if critical errors found
AGENT_BROWSER_NATIVE=1 agent-browser snapshot -i

# 3. Login — prefer Auth Vault over manual fill
#    First time: save credentials once
AGENT_BROWSER_NATIVE=1 agent-browser auth save myapp --url <login-url> --username admin --password secret
#    Every subsequent run: one command
AGENT_BROWSER_NATIVE=1 agent-browser auth login myapp
AGENT_BROWSER_NATIVE=1 agent-browser wait --load networkidle

# 4. Execute test steps (prefer semantic locators)
AGENT_BROWSER_NATIVE=1 agent-browser find label "Email" fill "test@example.com"
AGENT_BROWSER_NATIVE=1 agent-browser find role button click --name "Sign In"

# 5. After every navigation: re-snapshot + re-wait
AGENT_BROWSER_NATIVE=1 agent-browser wait --load networkidle
AGENT_BROWSER_NATIVE=1 agent-browser snapshot -i

# 6. Assert state
AGENT_BROWSER_NATIVE=1 agent-browser is visible @e3
AGENT_BROWSER_NATIVE=1 agent-browser is checked @e5
AGENT_BROWSER_NATIVE=1 agent-browser get text @e1

# 7. Capture evidence
AGENT_BROWSER_NATIVE=1 agent-browser screenshot --full result.png
```

---

## Recovery Patterns

| Failure | Recovery |
|:---|:---|
| Element ref stale | Re-run `snapshot`, relocate |
| Assertion content mismatch | Screenshot + **judgment gate** |
| Page not loading | `wait --load networkidle` + retry up to 3x |
| Staging cert error | `--ignore-https-errors` (never in production) |
| Slow page | `AGENT_BROWSER_DEFAULT_TIMEOUT=60000` |
| Output truncated on large pages | `--max-output <chars>` to increase limit |

---

## Judgment Gates

Pause and ask user when:
- JS errors found before test steps begin
- Expected content ≠ actual (may be a bug)
- Test step fails after all retries exhausted

---

## Device & Environment Variants

```bash
# Mobile viewport
AGENT_BROWSER_NATIVE=1 agent-browser set device "iPhone 15 Pro"

# Offline / PWA
AGENT_BROWSER_NATIVE=1 agent-browser set offline
AGENT_BROWSER_NATIVE=1 agent-browser reload
# ... assert offline state ...
AGENT_BROWSER_NATIVE=1 agent-browser set offline off   # ALWAYS restore

# Geo-aware
AGENT_BROWSER_NATIVE=1 agent-browser set geo 31.2304 121.4737
```

---

## Pitfalls

| Mistake | Fix |
|:---|:---|
| Assert before page loads | `wait --load networkidle` first |
| Stale refs after navigation | Re-run `snapshot` after every nav |
| `set offline` left on | Always `set offline off` after offline test |
| Staging cert error | `--ignore-https-errors` — never in production |
| `find ref e3 fill "..."` | ❌ `ref` is NOT a valid `find` subcommand. Use `@ref` directly: `fill @e3 "text"` / `click @e3` |
| Ambiguous label in dialogs | When a modal is open, `find label "X"` matches the **first** element on page — may hit background filters instead of the dialog field. Prefer `find placeholder "..."` or scope with `snapshot -s ".dialog-class"` first |
| App opens new tab (`window.open`) | agent-browser stays on original tab. Detect with `tab list`, then switch: `tab 1` (0-based index) |
| `javascript "..."` doesn't exist | JS execution is `eval "JS code"` — not `javascript` |
| Dialog blocking click | `dialog status` to confirm, then `dialog dismiss` or `dialog accept` |
| Waiting for download | `wait --download <path>` after clicking the download trigger — don't rely on fixed `wait 3000` |
