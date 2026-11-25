---
name: browser-agent
description: How to use the human-browser service to browse websites, extract information, fill forms, and handle login walls. Use this skill whenever the user asks you to look something up on a website, check a page, scrape data, fill out a form online, interact with a web UI, navigate to a URL, take a screenshot, or do anything that requires a real web browser. Also use when you need to verify something on a live website, compare prices, read articles, book/reserve something, sign up for an account, add items to a cart, test a web application, or gather information that requires rendering a real page (not just fetching HTML).
---

# Human-Browser: AI Agent Browser Automation

An HTTP API at `http://localhost:8080` that gives you a real Chrome browser with autonomous navigation. Send a URL and a goal — it navigates, reads pages, clicks links, fills forms, and reports back what it found.

## Quick Start

```bash
# 1. Start browsing
SESSION=$(curl -s -X POST http://localhost:8080/browse \
  -H 'Content-Type: application/json' \
  -d '{"url":"https://news.ycombinator.com","goal":"What is the #1 story?"}' \
  | jq -r .session_id)

# 2. Wait for result (blocks until done, use --max-time 600)
curl -s --max-time 600 http://localhost:8080/session/$SESSION/result | jq .

# 3. Always cancel when done (frees the session slot)
curl -s -X DELETE http://localhost:8080/session/$SESSION
```

Result: `{"status": "done", "result": "The top story is...", "steps_taken": 1, "page_summary": "https://news.ycombinator.com"}`

## The Browse Protocol

```
POST /browse  →  GET /result  →  done ✓
                              →  needs_input (form)  →  POST /input {fields}  →  GET /result
                                 →  needs_input (form_confirmation)  →  POST /input {action:"submit"}  →  GET /result  →  done ✓
                              →  blocked  →  POST /input {fields: credentials}  →  GET /result  →  done ✓
                              →  stuck | failed
```

### The 5 Outcomes

| Status | Meaning | What to do |
|--------|---------|------------|
| `done` | Goal achieved | Read `result` field for the answer |
| `needs_input` | Form needs data | Check `input_type`. If `"form"`: provide `fields`. If `"form_confirmation"`: send `{"action": "submit"}` or `{"action": "edit"}` |
| `blocked` | Login/captcha wall | Check `blocker`: `login_required`, `login_failed`, `captcha`, `paywall`, `mfa`. Provide credentials or ask the user |
| `stuck` | No progress | Try a different goal or approach |
| `failed` | Timeout/error | Check `error` field. Retry or adjust goal |

All results include `page_summary` (current URL), `steps_taken`, and `message` (human-readable context).

## Core Endpoints

### Start a session
```
POST /browse
Body: {"url": "https://...", "goal": "...", "context": {"credentials": {"username": "...", "password": "..."}}}
Response: {"session_id": "abc123"}
```
The `context.credentials` field is optional — provide it upfront to auto-handle login pages.

### Wait for result (blocking)
```
GET /session/{id}/result
Response: {status, result, steps_taken, page_summary, message, auto_handled}
```
This blocks until the browser finishes. Set a generous timeout (600s max — the browser's circuit breaker).

### Check state (non-blocking)
```
GET /session/{id}
Response: {session_id, state, goal, steps_taken, current_result}
```
Use this to poll instead of blocking. States: `created`, `running`, `paused`, `done`, `stuck`, `failed`, `cancelled`.

### Provide input
```
POST /session/{id}/input
Body: {"session_id": "abc123", "fields": {"Name": "John", "Email": "john@test.com"}}
  or: {"session_id": "abc123", "action": "submit"}
  or: {"session_id": "abc123", "action": "edit"}
```
The `session_id` field in the body is required. Use `fields` for form data, `action` for confirmations.

### Cancel
```
DELETE /session/{id}
```
Always cancel when done or after a timeout. Only one session runs at a time — forgetting to cancel causes `409 session_busy` on the next browse.

## Form Flow (Two Steps)

When the browser finds a personal data form, the flow has two pauses:

**Step 1 — Fill fields:**
```json
{"status": "needs_input", "input_type": "form", "fields": [
  {"id": "e3", "label": "Name", "type": "text", "value": "", "required": true},
  {"id": "e4", "label": "Email", "type": "email", "value": "", "required": true}
], "message": "This form needs your personal information."}
```
Respond with field values keyed by label: `{"session_id": "...", "fields": {"Name": "John", "Email": "john@test.com"}}`

**Step 2 — Confirm:**
```json
{"status": "needs_input", "input_type": "form_confirmation", "filled_fields": [...]}
```
Respond with: `{"session_id": "...", "action": "submit"}` (or `"edit"` to go back)

Then `GET /result` for the final outcome.

## Login Flow

**Option A — Credentials upfront (auto-handled):**
```bash
curl -s -X POST http://localhost:8080/browse \
  -d '{"url":"https://example.com/dashboard","goal":"Check balance","context":{"credentials":{"username":"john","password":"secret"}}}'
```
The browser auto-fills the login form and continues.

**Option B — Credentials on demand:**
The browser pauses with `{"status": "blocked", "blocker": "login_required"}`. Provide credentials:
```bash
curl -s -X POST http://localhost:8080/session/$SESSION/input \
  -d '{"session_id":"'$SESSION'","fields":{"username":"john","password":"secret"}}'
```
Then `GET /result` again.

## Direct Control

For step-by-step browser control:

| Method | Path | Body | Purpose |
|--------|------|------|---------|
| `GET` | `/observe?screenshot=true` | — | Get screenshot + page state |
| `POST` | `/click` | `{"x":100,"y":200}` or `{"element_id":"e3"}` | Click |
| `POST` | `/type` | `{"text":"hello","element_id":"e5","clear_first":true}` | Type text |
| `POST` | `/scroll` | `{"direction":"down","amount":3}` | Scroll |
| `POST` | `/goto` | `{"url":"https://..."}` | Navigate |
| `POST` | `/back` | — | Go back |
| `POST` | `/read` | `{"query":"What is the price?"}` | Extract text (returns `{"text":"..."}`) |
| `POST` | `/key` | `{"key":"Enter","modifiers":["ctrl"]}` | Press key |

Use autonomous mode (`POST /browse`) for most tasks. Use direct control only when you need precise step-by-step interaction.

## Important Rules

1. **One session at a time.** Always `DELETE /session/{id}` when done. Forgetting causes `409 session_busy`.
2. **Generous timeouts.** The browser may take up to 600s. Use `--max-time 600` with curl, or poll via `GET /session/{id}`.
3. **Always cancel after client timeout.** If your HTTP call times out, the browser is still running. Cancel it.
4. **Specific goals work best.** "What is the price of the first item?" beats "Look at the page."
5. **Each session starts fresh.** Cookies are cleared per-origin. Login state does not persist between sessions.
6. **Check `input_type` on `needs_input`.** Forms need `fields`, confirmations need `action: "submit"`.
