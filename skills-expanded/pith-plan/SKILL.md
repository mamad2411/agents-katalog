---
name: pith-plan
description: >
  One-shot planning format. Use for feature planning, task breakdown, sprint planning, implementation plans.
  Format: Goal / Steps / Risks / Done-when. Does not persist.
---

Plan format. Numbered steps. No narrative.

**Goal:** [what done looks like — one sentence]

**Steps:**
1. [verb] [what] — [file or component]
2. [verb] [what] — [file or component]
...

**Risks:** [what could block or break this]
**Done when:** [exact, testable acceptance criteria]

## Rules

- Steps: verb-first imperative. "Add", "Create", "Update", "Delete", "Test", "Wire". Not "We should add..."
- Each step: one line. Sub-steps as 1a/1b if needed.
- Done-when: observable and testable. Not "it works." Example: "All unit tests pass + /api/health returns 200 + no console errors in E2E"
- Risks: real blockers only. Not "might take longer than expected."
- No time estimates unless explicitly asked.
- Dependencies between steps: note them. "Step 3 requires step 1 complete."

## Example

**Goal:** add email verification to user registration

**Steps:**
1. Add `email_verified` boolean column to users table — `db/migrations/`
2. Create `EmailService.sendVerification(email, token)` — `src/services/email.ts`
3. Generate + store verification token on register — `src/routes/auth.ts:register()`
4. Add `GET /api/auth/verify?token=` endpoint — `src/routes/auth.ts`
5. Block login for unverified users, return 403 with message — `src/middleware/auth.ts`
6. Add integration test for full verification flow — `tests/auth.test.ts`

**Risks:**
- Email delivery failures in test env — mock EmailService in tests
- Token expiry logic needed — decide TTL before step 2

**Done when:** `POST /register` triggers email + `GET /verify?token=valid` sets verified=true + unverified login returns 403

One-shot. Does not persist.
