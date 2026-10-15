---
name: agent-browser-debug
description: "[INTERNAL TEMPLATE] Debugging execution protocol. Called by agent-browser orchestrator."
---

# Debug Diagnosis — Execution Protocol

> **Internal template.** Entry point: `agent-browser` skill.

---

## NEVER

```
NEVER jump to DOM inspection before checking `errors` — JS errors explain 80% of broken UIs
NEVER assume auth is fine — check `cookies` + `storage local` first when login suspected
NEVER think `inspect` kills CLI — DevTools and CLI work simultaneously
```

---

## Triage Sequence (run in order, stop at first finding)

```bash
agent-browser --headed open <url>
agent-browser wait --load networkidle

# Step 1: JS errors (explains 80% of broken UIs)
agent-browser errors

# Step 2: Console warnings
agent-browser console --pattern "error|warn"

# Step 3: Failed network requests — filter to relevant calls
agent-browser network requests --filter "api"
agent-browser network requests --type xhr,fetch --status 4xx   # 4xx only
agent-browser network requests --method POST --status 5xx      # failed writes

# Step 4: Inspect full request/response body of a failed request
agent-browser network request <requestId>   # get requestId from step 3

# Step 5: Auth state (check first if login/session suspected)
agent-browser cookies         # token cookie present?
agent-browser storage local   # JWT in localStorage?

# Step 6: DOM state
agent-browser snapshot -i
agent-browser is enabled @e5
agent-browser is visible @e3

# Step 7: Form validity (if button appears enabled but won't submit)
agent-browser eval "document.querySelector('form').checkValidity()"

# Step 8: Deep investigation
agent-browser inspect         # DevTools (CLI stays live)
```

---

## Network HAR for Persistent Evidence

```bash
# Record full network trace (start BEFORE navigation)
agent-browser network har start ./debug-trace.har
agent-browser open <url>
agent-browser wait --load networkidle
# ... reproduce the issue ...
agent-browser network har stop
# Open debug-trace.har in browser DevTools → Network → Import
```

---

## Recovery Patterns

| Symptom | Next action |
|:---|:---|
| JS errors found | Report errors → **judgment gate**: continue or stop? |
| Auth token missing | Re-run auth flow, recheck `cookies` |
| Network 4xx/5xx | `network request <id>` for full body → report → judgment gate |
| `is enabled` false | Check form validity via `eval` |
| Issue not reproducible headless | Run with `--headed` to observe visually |

---

## Judgment Gates

Pause when:
- JS errors found (show to user, ask: bug or known?)
- Auth token missing (hard to auto-recover without credentials)
- API returning unexpected errors (user needs to decide next step)
- `network request <id>` reveals sensitive data in response (don't log, ask user)

---

## Pitfalls

| Mistake | Fix |
|:---|:---|
| Skip `errors`, jump to DOM | Errors explain 80% — always check first |
| Auth bug → jump to JS debugging | Check `cookies` + `storage local` first |
| Think `inspect` kills CLI | It doesn't — both work simultaneously |
| Filter `network requests` by URL only | Also filter by `--status 4xx` or `--method POST` to narrow down |
| Miss request body | Use `network request <requestId>` for full payload |
