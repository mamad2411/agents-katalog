---
name: podex-webapp-dev
description: Build full-stack PowerShell web apps using the Podex template (Pode backend + htmx + Mustache + Tailwind) with clean feature scaffolding, CRUD flows, error handling, SQLite patterns, and tests.
allowed-tools: "Read,Write,Edit,Glob,Grep,Bash(pwsh *),Bash(npm *),Bash(node *),Bash(git *)"
---

# Podex Web App Development

## 1. Purpose

Use this skill when the user is developing or extending a **Podex-based** web application: a full-stack framework using **PowerShell Core + Pode + SQLite** on the backend and **htmx + Mustache + Tailwind** on the frontend.

This skill focuses on:
- Adding features (pages + htmx partials + endpoints) in the Podex repo structure (`api/`, `views/`, `htmx/`, `errors/`, `public/`, `tests/`).
- Building CRUD flows that “feel native” to htmx (partial swaps, progressive enhancement, clean request/response boundaries).
- Keeping changes maintainable (feature folders, consistent naming, predictable route wiring).
- Creating Pester tests for core logic and route behavior (where practical).

> Reminder: In Codex Skills, the core is a `SKILL.md` with optional `scripts/`, `references/`, and `assets/`.

---

## 2. When to Trigger

Trigger automatically when the user asks to:
- “build a web app with Pode and htmx”
- “extend my Podex app”
- “add a new page/feature/module to Podex”
- “add CRUD for a new entity (SQLite)”
- “add htmx table, search, sorting, pagination, modals”
- “add auth/RBAC, validation, error handling, logging”
- “create scaffolding for a new feature”

Also trigger when the user provides a Podex repository path and requests structure-aware changes.

---

## 3. Operating Rules

### 3.1 Repo-first, structure-aware edits
1. Use `Glob`/`Read` to map what exists: `api/`, `views/`, `htmx/`, `public/`, `errors/`, `tests/`.
2. Follow existing Podex conventions (route registration, template naming, layout usage, static assets).
3. If conventions are unclear, infer from nearest existing feature and be consistent with it.

### 3.2 htmx-first UX patterns
Design interactions so the “default” is:
- A full page route (initial render)
- One or more htmx endpoints returning partial fragments (table body, modal content, toast region, etc.)
- Minimal client JS; use htmx attributes and server-driven HTML

Preferred response patterns:
- Partial HTML for `HX-Request: true`
- Full page for normal navigation
- Use htmx response headers when helpful (`HX-Redirect`, `HX-Trigger`) *only if Podex already uses them; otherwise add carefully and document*

### 3.3 SQLite as an implementation detail
- Keep DB access in a small, testable layer (query functions or a data module).
- Use parameterized queries.
- Prefer simple migrations (idempotent SQL scripts) if the repo has a migrations pattern.

### 3.4 Error handling & correlation
- Return user-safe errors to the UI (inline validation messages, toast area, or dedicated error partial).
- Log technical detail server-side with a correlation/request id if the repo supports it.
- Prefer consistent error DTO shape for JSON endpoints (if any).

### 3.5 Tests
- Add Pester tests for pure functions and any data transforms.
- For routes: test handlers where feasible (unit style) or test the functions the routes call.

---

## 4. Default Feature Blueprint

When the user asks “add a feature”, propose (and implement) this minimal set:

1. **Routes**
   - Page route: `/Feature`
   - Partial routes (examples):
     - `/Feature/Table`
     - `/Feature/Form`
     - `/Feature/Create` (POST)
     - `/Feature/Update` (POST)
     - `/Feature/Delete` (POST)

2. **Views**
   - `views/feature.mustache` (page shell; includes htmx targets)
   - `htmx/feature-table.mustache` (table fragment)
   - `htmx/feature-form.mustache` (form fragment)
   - Optional: `htmx/toast.mustache` region updates

3. **Data**
   - A small set of functions (Get/Create/Update/Delete) that routes call.
   - Optional: a migration SQL file if repo uses migrations.

4. **Pester tests**
   - At least transform/validation tests + a DB function test with a temp sqlite db if practical.

---

## 5. “More” Extensions (Offer Proactively)

If the user’s request hints at a real app (not just a demo), recommend:
- Auth: Basic Auth (quick) → session/cookie auth (better) → OIDC (best)
- RBAC with role-to-route mapping
- Input validation (server-side), plus “inline error partial” rendering
- Pagination + sorting + filtering for tables (htmx query params)
- Optimistic UI patterns (disable buttons, show spinners via htmx indicators)
- Audit logging (who changed what)
- A small component library of Mustache partials (buttons, inputs, badges, alerts)
- Error boundary page + error fragment patterns
- Conventions doc in `references/` so future changes stay consistent

---

## 6. Output Format Expectations

When implementing:
1. Summarize what you will change (files + responsibilities).
2. Provide the exact file contents for new/changed files.
3. Include a quick “how to run” note (npm/pwsh) consistent with Podex setup.

From Podex: npm install + npm start, default URL `http://localhost:8433`.

---

## 7. Quick Commands (Contextual)

Only mention these if relevant to the user’s task:

- Install Node deps:
  - `npm install`
- Install PowerShell modules via build script:
  - `powershell -Command ". ./.build.ps1"`
- Run:
  - `npm start`
- Browse:
  - `http://localhost:8433`
