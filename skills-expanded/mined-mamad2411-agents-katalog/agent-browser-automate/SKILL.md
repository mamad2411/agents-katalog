---
name: agent-browser-automate
description: "[INTERNAL TEMPLATE] Task automation execution protocol. Called by agent-browser orchestrator."
---

# Task Automation — Execution Protocol

> **Internal template.** Entry point: `agent-browser` skill.

---

## NEVER

```
NEVER use `fill` when you want to append — it clears first; use `type` to append
NEVER upload a file with `click` then `fill` — use dedicated `upload <sel> <path>` command
NEVER submit a form without showing field values first — judgment gate required
```

---

## Auth Setup (choose one, in priority order)

```bash
# Option 1 (recommended): Auth Vault — encrypted, reusable
agent-browser auth login <vault-name>
agent-browser open <url>

# Option 2: Persistent profile (local only)
agent-browser --profile ~/.myapp open <url>

# Option 3: Token injection
agent-browser open <url>
agent-browser storage local set authToken "<token>"
agent-browser reload

# Option 4: HTTP Basic Auth
agent-browser open <url>
agent-browser set credentials <user> <pass>

# Option 5: Bearer header
agent-browser --headers '{"Authorization":"Bearer <token>"}' open <url>
```

---

## Form Automation Sequence

```bash
agent-browser snapshot -i                                    # get refs
agent-browser find label "Email" fill "user@example.com"
agent-browser find label "Password" fill "<password>"
agent-browser find role button click --name "Submit"
agent-browser wait --load networkidle
agent-browser screenshot --full step-complete.png           # evidence
```

---

## File Operations

```bash
# Upload
agent-browser find label "Attachment" upload ./file.pdf

# Download (triggers on button click, waits for completion)
agent-browser find role button click --name "Export CSV"
agent-browser wait --download ~/report.csv

# Generate PDF
agent-browser pdf ./report.pdf
```

---

## Multi-Tab Flows

```bash
agent-browser tab new
agent-browser open <second-url>
agent-browser tab 0       # switch back to first tab (0-based index)
agent-browser tab list    # see all tabs with URLs
```

---

## Clipboard

```bash
# Read clipboard
agent-browser clipboard read

# Write to clipboard
agent-browser clipboard write "text to copy"

# Copy element text to clipboard
agent-browser clipboard copy @e3

# Paste clipboard into element
agent-browser clipboard paste @e5

# macOS: paste system clipboard into focused element
agent-browser keyboard inserttext "$(pbpaste)"
```

---

## Fine Mouse Control (canvas / Kanban / drawing apps)

```bash
agent-browser mouse move <x> <y>
agent-browser mouse down
agent-browser mouse move <x2> <y2>   # drag
agent-browser mouse up
```

---

## Waiting Patterns

```bash
# Page load
agent-browser wait --load networkidle

# Wait for element to appear
agent-browser wait "#success-toast"

# Wait for element to disappear (loading spinner)
agent-browser wait "#spinner" --state hidden

# Wait for URL to change (after form submit / redirect)
agent-browser wait --url "**/dashboard"

# Wait for text to appear
agent-browser wait --text "Upload complete"

# Wait for download to finish
agent-browser wait --download ./report.xlsx
```

---

## Recovery Patterns

| Failure | Recovery |
|:---|:---|
| Auth expired | `auth login <name>` re-authenticate |
| Auth Vault password changed | `auth delete <name>` then `auth save <name>` |
| Unexpected popup/dialog | `dialog status` to confirm, then `dialog dismiss` |
| `fill` overwrites existing content | Use `type` to append |
| Modal won't scroll | `scroll down --selector ".modal-body"` |

---

## Judgment Gates

Pause when:
- About to submit a form (show field values → ask confirm)
- About to trigger download / delete / payment
- Auth fails after retry (need fresh credentials)

---

## Pitfalls

| Mistake | Fix |
|:---|:---|
| Auth Vault password changed | `auth delete` + `auth save` again — no in-place update |
| `fill` clears content unintentionally | Use `type` to append |
| File upload fails | Use `find label "..." upload <path>`, not `click` then `fill` |
| Can't scroll inside modal | `scroll down --selector ".modal-body"` |
| Download not captured | Use `wait --download <path>` after clicking the download button |
| JS dialog blocks daemon completely | Playwright intercepts at CDP level — `eval "window.confirm = () => true"` does NOT work (JS layer override can't reach CDP). Only reliable fix: `dialog accept` must be called from a second concurrent process while `click` is blocking. |
| Read-only DOM nodes missing from snapshot (`<p>`, `<span>`, `<div>` without ARIA roles) | `snapshot` only exposes the accessibility tree — interactive elements only. Read non-interactive node content with `eval "document.querySelector('#id').textContent"` or `eval "document.querySelector('.class').innerText"`. |
