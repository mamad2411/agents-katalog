> **HISTORICAL (archived 2026-08-04).** Written 2026-05-07 when the repo was documentation-only; its claims (no app, no package.json) and its `pnpm --filter web` commands are wrong for the current repo. Successor: `.cursor/cursor-cloud.md` (environment facts) + `AGENTS.md` (rules).

---
name: cloud-agent-starter
description: Use this skill when a Cloud agent needs to run, test, or manually verify the Area-Scoped Personal Workflow Cockpit codebase.
---

# Cloud Agent Starter Runbook

Use this skill before running or testing this repo in Cursor Cloud. It is practical on purpose: discover what exists, start only the services needed for the changed area, use mocks before real integrations, and preserve the project's safety rules.

## 1. First orientation

The system is a private, one-user, low-cost AI-assisted workflow cockpit. Its core loop is:

```text
Dump -> Diagnose -> Bound -> Slice -> Discover -> Act -> Review
```

The highest-risk invariants are:

- Raw captures must be persisted before AI parsing.
- AI output must validate against strict schemas before becoming app state.
- Google Calendar writes require explicit user approval and an `external_write_events` audit record.
- User-owned data must be protected by Supabase Auth plus RLS.
- Area is a first-class scope object, and learning is area-scoped unless deliberately global.
- Health scores are deterministic; AI may explain them but must not invent scores.

Before changing behavior, read `AGENTS.md`, `docs/PROJECT_STATE.md`, plus the relevant docs:

- Product and scope: `docs/REQUIREMENTS.md`, `docs/PROJECT_STATE.md`, and `docs/adr/0005-staged-evolution-after-v1.md`
- Architecture and data: `docs/ARCHITECTURE.md`, `docs/DATA_MODEL.md`
- UX and tests: `docs/UX_FLOWS.md`, `docs/TEST_PLAN.md`
- Security: `docs/SECURITY_PRIVACY.md`

Update `docs/PROJECT_STATE.md` only when shipped behavior, status, or governance guidance materially changes, following `AGENTS.md`.

The repo is a pnpm monorepo with the Next.js app in `apps/web`. Discover current scripts and services from the checked-out repo; do not rely on scaffold-era assumptions.

## 2. Repository and environment discovery

Run these checks before setup:

```bash
git status --short
test -f package.json && echo "root package.json found" || echo "docs-only or unscaffolded repo"
test -d apps/web && echo "web app found" || true
test -d supabase && echo "supabase folder found" || true
test -f supabase/config.toml && echo "supabase local config found" || true
```

Find the package manager from the lockfile:

- `pnpm-lock.yaml` -> use `pnpm`
- `package-lock.json` -> use `npm`
- `yarn.lock` -> use `yarn`
- `bun.lockb` or `bun.lock` -> use `bun`

Do not create production credentials in Cloud. Use `.env.local`, `apps/web/.env.local`, or `supabase/.env.local` only, and never commit them.

## 3. Common Cloud workflow

For long-running processes, use a named tmux session and leave it running for follow-up testing.

```bash
SESSION_NAME="web-dev"
tmux -f /exec-daemon/tmux.portal.conf has-session -t "=$SESSION_NAME" 2>/dev/null || tmux -f /exec-daemon/tmux.portal.conf new-session -d -s "$SESSION_NAME" -c "$PWD" -- "${SHELL:-bash}" -l
tmux -f /exec-daemon/tmux.portal.conf send-keys -t "$SESSION_NAME:0.0" 'npm run dev' C-m
```

If `tmux -f /exec-daemon/tmux.portal.conf` is unavailable, retry the same command without `-f /exec-daemon/tmux.portal.conf`.

Use the app only with development or local credentials. Never point Cloud-agent testing at production databases or production calendars.

## 4. Codebase area workflows

### 4.1 Documentation and agent rules

Use this area when changing `.md` files, runbooks, scope, or agent instructions.

Validation workflow:

```bash
git diff --check
rg -n "silent calendar|disable RLS|service-role|production|autonomous rescheduling|vector database|realtime voice" .
```

Review against `AGENTS.md`, current REQUIREMENTS, and ADR 0005. Owner-ratified data-independent foundations may proceed when structurally ready; do not weaken capability-specific usage/trust gates, approval gates, schema validation, privacy, transactions, or RLS requirements.

### 4.2 Web app, auth, and UI flows

Expected location: `apps/web`.

Setup once scaffolded:

```bash
corepack enable
pnpm install
cp apps/web/.env.example apps/web/.env.local
pnpm --filter web dev
```

If the repo uses `npm`, replace with `npm install` and `npm run dev`.

Login workflow:

- Prefer seeded local test users over auth bypasses.
- If using Supabase local, create or seed two users: `user_a@example.test` and `user_b@example.test`.
- Sign in through the normal login UI; do not disable auth middleware just to test.
- Confirm protected routes redirect anonymous users to login.

UI smoke tests by screen:

- Capture: submit raw text, verify capture persists before parsing, verify parse failure keeps raw text.
- Triage: accept/edit/reject/reassign a draft and verify only accepted items become real objects.
- Calendar/Planning: create local proposals, verify conflict badges and no external write before approval.
- Execute: start one block, record outcome, verify execution session and duration data.
- Review: complete daily/weekly review without external writes.
- Health: verify auth, DB, AI, calendar, and scheduler statuses are separated.

Suggested commands once scripts exist:

```bash
pnpm --filter web lint
pnpm --filter web test
pnpm --filter web e2e
```

For UI changes, run the app and perform manual browser verification in Cursor Cloud.

### 4.3 Feature flags and mocks

Prefer local mocks unless the task explicitly requires a real provider.

Recommended flag names when implementing new toggles:

```bash
AI_PROVIDER=mock
CALENDAR_ADAPTER=mock
GOOGLE_CALENDAR_ENABLED=false
NEXT_PUBLIC_CALENDAR_WRITE_ENABLED=false
NEXT_PUBLIC_ENABLE_REAL_AI=false
NEXT_PUBLIC_ENABLE_REAL_CALENDAR=false
```

Rules:

- Feature flags belong in local env files or test fixtures, not committed secrets.
- Real AI calls must use configured model tiers: `AI_MODEL_CHEAP`, `AI_MODEL_STANDARD`, `AI_MODEL_STRONG`.
- Do not hardcode model names in app logic.
- Do not bypass RLS or auth with a frontend flag.
- Calendar mocks must still exercise approval and audit-log code paths.

### 4.4 Supabase database, migrations, and RLS

Expected locations: `supabase/migrations`, `supabase/seed`.

Local setup once Supabase config exists:

```bash
supabase start
supabase db reset
```

Testing workflow:

- Run migrations from a clean local DB.
- Seed at least two users and default areas.
- Test each user-owned table with User A and User B.
- Assert User A cannot select, insert, update, or delete/archive User B rows.
- Confirm every user-owned table has `id`, `user_id`, timestamps where appropriate, indexes, RLS enabled, and policies.

Useful checks:

```bash
supabase db reset
supabase test db
```

If `supabase test db` is not configured, run the repo's RLS integration tests or add focused tests for touched tables.

### 4.5 Shared schemas, AI contracts, and prompts

Expected location: `packages/schemas`.

Required schema families:

- `ParseCaptureResponse`
- `AmbiguityAssessmentResponse`
- `TriageSuggestionResponse`
- `BlockProposalResponse`
- `WeeklyReviewResponse`
- `PolicySuggestionResponse`
- `HealthNarrativeResponse`

Testing workflow:

- Validate minimal valid fixtures.
- Validate full valid fixtures.
- Reject missing required keys, invalid statuses, invalid dates, invalid confidence scores, hallucinated IDs, and unexpected keys in strict schemas.
- Verify failed validation is recoverable and never commits AI output as final state.
- For prompt changes, run fixture-based contract tests instead of exact wording assertions.

Suggested commands once scripts exist:

```bash
pnpm --filter schemas test
pnpm test -- --run schema
pnpm test -- --run ai-contract
```

### 4.6 Supabase Edge Functions

Expected location: `supabase/functions`.

Function-specific workflows:

- `parse_capture`: persist raw capture first, then call mock AI, validate drafts, route low confidence to triage.
- `triage_apply`: accept/edit/reject/reassign drafts, create user decisions and correction logs.
- `propose_blocks`: generate local proposals only; no Google write.
- `approve_calendar_write`: require explicit approval, use mock calendar first, write audit event, prevent duplicates.
- `mark_block_result`: persist execution session and area-scoped duration/productivity signals.
- `generate_review` or `weekly_review`: summarize by area and require approval for policy changes.
- `health_check`: compute deterministic scores and create actionable incidents.

Local serve pattern once configured:

```bash
supabase functions serve parse_capture --env-file supabase/.env.local
```

Integration tests should invoke the function through its HTTP boundary with a real local JWT when possible.

### 4.7 Calendar integration

Calendar is a dangerous area. Use mocks first and ask for human review before changing OAuth scopes, service-role usage, external adapters, or write behavior.

Mock test workflow:

- Start with `CALENDAR_ADAPTER=mock`.
- Approve a proposal through the normal UI or function boundary.
- Assert the calendar event is created once in the mock.
- Assert `google_event_id` or mock provider ID is stored.
- Assert `external_write_events` has provider, operation, target, request summary, result status, and error details if failed.
- Retry the same approval and verify duplicate writes are prevented.
- Simulate provider failure and verify the block is not marked scheduled.

Real calendar testing is only after mock tests, RLS tests, and scope review pass. Use a dedicated test calendar, not a personal primary calendar.

### 4.8 Health, review, and meta-learning

Testing workflow:

- Seed representative area data for Main Job, Personal, and Volunteer Work.
- Verify duration, time preference, triage, and priority signals stay area-scoped.
- Verify weekly review suggestions cite observed signals and require approval for policy changes.
- Verify health scores come from deterministic rules, while AI text is only narrative.
- Force AI/calendar/DB failures one at a time and verify distinct incidents and repair guidance.

## 5. End-to-end smoke workflows

Run these when the touched area affects user flows.

Happy path:

```text
Create area -> capture text -> parse into task -> accept task -> propose block -> approve local proposal -> write calendar event with mock adapter -> execute block -> complete session -> view review -> view health
```

Ambiguous work:

```text
Capture ambiguous project -> sense-making assessment -> discovery questions -> convert first move into task -> schedule first move -> execute -> review assumption
```

Missed block recovery:

```text
Scheduled block -> mark missed -> choose reschedule -> generate proposal -> edit proposal -> approve with mock calendar
```

Every E2E pass should verify no unexpected external write occurred and all created records have the correct `user_id` and `area_id`.

## 6. When setup fails in Cloud

Try these before giving up:

- Confirm the repo is scaffolded; if only Markdown exists, document that no runnable app exists yet.
- Install dependencies with the detected package manager.
- Copy `.env.example` files to local env files and set mock flags.
- Start Supabase local only if `supabase/config.toml` exists.
- Run the narrowest relevant test script instead of the whole suite.
- Check dev server logs and Edge Function logs for missing env vars.

Do not patch unrelated production code only to work around a local Cloud setup problem.

## 7. Updating this skill

Whenever a Cloud agent discovers a reliable setup trick, missing env var, seed command, test command, mock flag, login path, or provider-specific runbook step:

1. Add it to the matching codebase area above.
2. Include the exact command or env var name.
3. State the precondition, for example "after `supabase start`" or "only when `apps/web` exists".
4. Keep production-safety warnings near the risky command.
5. Remove obsolete commands when scripts or folders are renamed.

Treat this skill as the first place future Cloud agents should learn how to run the repo.
