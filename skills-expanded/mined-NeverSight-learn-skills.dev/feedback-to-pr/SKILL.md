---
name: feedback-to-pr
description: Add an in-app feedback and bug-report loop that captures a screenshot plus network/console logs, emails the reporter, launches a Cursor Cloud Agent with autoCreatePr, and emails again when the PR opens and when it merges. Use when asked to add feedback, bug reporting, user reports that open PRs, Cursor automation for feedback, or a feedback-to-PR workflow.
---

# Feedback → Cursor Cloud Agent → PR

Wire a product feedback loop end-to-end:

**floating control → DOM screenshot + fetch/console ring buffer → dialog →
`POST /api/feedback` (row per user) → background job emails confirmation and
launches a Cursor Cloud Agent (`autoCreatePr: true`) with the screenshot +
logs → Cursor webhook marks `pr_open` and emails the PR link → GitHub webhook
on merge marks `merged` and emails "shipped".**

Status lifecycle: `submitted → agent_running → pr_open → merged` (or `failed`).

Implement this in the target app. Do not redesign the loop — the gotchas below
are load-bearing.

---

## Prerequisites

- Route handlers (Next.js App Router or equivalent)
- A database that can store a feedback row (Postgres + any ORM is fine)
- Session/auth that yields a user id + email
- A background job runner with retries (Inngest, etc.)
- Transactional email (Resend or equivalent)
- Cursor Cloud Agents API access + GitHub App grant on the target repo

If the app has no organizations concept, omit org fields — everything else stands alone.

---

## What to build

| Piece | Role |
|---|---|
| Shared types | `bug` \| `feedback`; network/console log entry shapes |
| Network recorder | Patch `fetch` + `console.error` into ring buffers. Strip query strings. Never record headers or bodies. |
| Screenshot | DOM capture (e.g. `modern-screenshot`). Optional — try/catch to `null`, never block submit. |
| Widget | Client provider + dialog; snapshot page on open; `POST /api/feedback` |
| Submit route | Auth required; Zod-validate body; rate-limit (~5/hr); persist row; emit job event `{ feedbackId }` only |
| Feedback table | message, pageUrl, userAgent, screenshot (+ dims), networkLogs, consoleLogs, cursorAgentId, branchName, prUrl, status |
| Job | (1) confirmation email, (2) create Cursor agent with prompt + screenshot, (3) store agent id → `agent_running` |
| Cursor client | `POST https://api.cursor.com/v0/agents` with `autoCreatePr: true` and a webhook URL (v0 still owns webhooks in the create body — check current Cursor docs before migrating to v1) |
| Cursor webhook | Verify HMAC over raw body; on `FINISHED`+`prUrl` → `pr_open` + email; on ERROR/CANCELLED or FINISHED without PR → `failed` |
| GitHub webhook | `pull_request` closed+merged → match by `prUrl` (fallback: branch) → `merged` + email |
| HMAC helper | SHA-256 hex, optional `sha256=` prefix, `timingSafeEqual` |

Adaptation points: the app's session helper, design-system dialog/button, Cursor prompt path hint ("work in `apps/web`"), schema migrate, job registration.

---

## Env vars

| Var | Notes |
|---|---|
| `CURSOR_API_KEY` | [Cursor Dashboard → API Keys](https://cursor.com/dashboard/api) |
| `CURSOR_REPO_URL` | `https://github.com/<org>/<repo>` the agent should edit |
| `CURSOR_WEBHOOK_SECRET` | `openssl rand -hex 24` (≥ 32 chars) |
| `GITHUB_WEBHOOK_SECRET` | invent it; same value in the GitHub webhook form |
| `RESEND_API_KEY` / `RESEND_FROM_EMAIL` | verified domain |
| `WEBHOOK_PUBLIC_URL` | public tunnel in dev; falls back to app public URL in prod |
| App public URL (e.g. `NEXT_PUBLIC_APP_URL`) | browser-facing origin — **not** the tunnel |

---

## One-time external setup

1. **Cursor ↔ GitHub** — grant the Cursor GitHub App on the repo. Verify with
   `GET https://api.cursor.com/v0/repositories`.
2. **GitHub webhook** — `${WEBHOOK_PUBLIC_URL}/api/webhooks/github`, secret =
   `GITHUB_WEBHOOK_SECRET`, events: Pull requests only.
3. **Dev tunnel** — HTTPS tunnel to the local app port → `WEBHOOK_PUBLIC_URL`.
   Run the job runner alongside the app.

---

## Hard-won gotchas

1. **Never point the auth/public app URL at the tunnel.** Cross-origin auth dies
   with "Failed to fetch". That is what `WEBHOOK_PUBLIC_URL` is for.
2. **Cursor's "Failed to verify existence of branch 'main'" means no repo
   access**, not a wrong branch. Fix the GitHub App grant.
3. **Confirmation email is the FIRST job step**, before agent creation —
   otherwise a Cursor failure means the user never hears anything.
4. **Job event carries only `{ feedbackId }`.** Payloads/step returns are
   size-capped (~512KB); the screenshot stays in the DB and is re-read in the step.
5. **Webhook signatures verify over the raw body** (`await req.text()` before
   parsing). Status-guarded UPDATEs (`WHERE status IN (...)` + returning) make
   replays no-ops — only email when a row actually transitioned.
6. Cloud agents appear at **cursor.com/agents**, not in the IDE agent list.
7. Screenshot is optional end-to-end (iframes/cross-origin images blank out).
8. Swallow email failures in webhook handlers **after** the DB write, or the
   provider redelivers forever over a mail blip.
9. Cursor `FINISHED` without `prUrl` → mark `failed`, don't leave `agent_running`.

---

## Verification

1. Typecheck/lint clean; job runner reports the new function.
2. Submit feedback → DB row, confirmation email, Cursor agent RUNNING.
3. Simulate webhooks if not tunneled: signed payloads → `pr_open` → `merged`;
   replay idempotent; bad signature → 401; closed-without-merge → no-op.
4. Negatives: unauthenticated → 401; over rate limit → 429.

See `references/architecture.md` for the status machine diagram.
