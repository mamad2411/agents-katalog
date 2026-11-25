---
name: bdr-commit
description: "BDR commit discipline: Business/Decision/Rationale format making every commit auditable and falsifiable. Triggers when user says 'bdr commit', asks to commit a feature, or a non-trivial implementation is complete. Never add Co-Authored-By or AI attribution."
---

<!-- Design razor: CONTEXT only. A style guide and decision-documentation framework, not a process. Delete when: commit follows BDR format with all fields completed and verified. -->

# BDR Commit Skill

## Format

```
<type>(<scope>): <one-line summary>

Contract: <observable external behavior>

Acceptance: <how to verify — tests or manual checks>

Rejected: <alternatives considered and why this approach>

Non-scope: <what deliberately isn't addressed>

<optional: detailed context or implementation notes>
```

---

## Field Reference

### `<type>(<scope>): <one-line summary>`
**Conventional commit** prefix. Examples:
- `feat(auth): add OAuth 2.0 Google login`
- `fix(search): handle null query parameters`
- `refactor(database): extract connection pooling`
- `test(api): add rate-limit edge cases`

**Keep under 50 characters.** Lowercase. No period.

---

### `Contract:`
**One sentence**: What externally observable behavior does this commit deliver? What can the user do differently *after* this commit?

Not implementation details — **user-facing promise**.

**Examples**:
- "Users can sign in with Google OAuth credentials instead of email+password only."
- "Database connections reuse a pool instead of creating new connections per query, reducing 503 errors during traffic spikes."
- "Email validation now rejects addresses with `+` character, matching SMTP RFC 5321."

---

### `Acceptance:`
**How to verify this works**: What test passes? What manual check confirms?

Be specific. A reviewer or CI system should run exactly what you write.

**Examples**:
- `npm test -- --grep "google" covers sign-in flow, token refresh, logout (8 tests pass)`
- `npm run performance-test; verify database query time <50ms (was 200ms before pooling). See benchmark/pool-comparison.txt`
- `Integration test 'email validates plus addressing' in email.test.ts line 127. Run: npm test -- email.test.ts`

---

### `Rejected:`
**Why this approach**: What other solutions did you consider? Why did you choose this one instead?

This stops the next engineer from re-proposing the same alternative six months later.

**Examples**:
- "Rejected Passport.js (50KB overhead for single provider), rejected custom OAuth (maintenance burden). Chose Firebase Auth (15KB, Google-maintained)."
- "Rejected Redis pooling (infrastructure dependency), rejected simple queue (no backpressure). Chose native pg pooling (zero deps, proven stable)."
- "Rejected strict RFC 5322 email regex (9KB, too complex), rejected allowing `+` character (breaks downstream systems). Chose RFC 5321 subset (simpler, safer)."

---

### `Non-scope:`
**What deliberately isn't addressed**: What could have been done but wasn't? What does this NOT fix?

Documents deliberate scope boundaries and prevents misalignment.

**Examples**:
- "Not adding OAuth for Microsoft/GitHub (can be next sprint after Google stabilizes)."
- "Not migrating legacy connections to pooling (requires schema migration; new code uses pool, legacy gradually migrates)."
- "Not supporting offline email validation (requires larger regex library; cloud-only for now)."

---

## Example: Full BDR Commit

```
feat(auth): add OAuth 2.0 Google login

Contract: Users can authenticate with a Google account instead of email+password only.

Acceptance: npm test -- --grep "google" — 8 tests pass (sign-in flow, token refresh, logout, error handling). Manual: Visit /login, click "Sign in with Google", complete consent, verify session in database.

Rejected: Passport.js (50KB, overkill for single provider), custom OAuth (maintenance + security patches), Auth0 (external vendor lock-in + cost). Chose Firebase Auth: maintained by Google, <15KB, offline-first, zero additional dependencies.

Non-scope: OAuth for Microsoft/GitHub (TASK-043). SSO federation (requires directory service). Automatic account linking for existing email accounts (manual migration for v1).

Implementation note: Google ID stored in users.google_id. Refresh tokens rotated every 7 days per Firebase defaults. Logout revokes refresh token and clears local session. Error messages generic (no account-exists leakage).
```

---

## Checklist Before Committing

- [ ] **Contract is testable**: Can user/QA verify this works without reading code?
- [ ] **Acceptance is runnable**: Someone can execute exactly what you wrote
- [ ] **Rejected alternatives are real**: You actually considered these (don't fabricate)
- [ ] **Non-scope is honest**: These are deliberate boundaries, not overlooked tasks
- [ ] **No AI attribution**: No `Co-Authored-By`, "Generated with Claude", or similar trailers

If you can't fill in a section, you haven't finished thinking. Stop and clarify before committing.

---

## Why BDR?

**Traditional commits** (`feat: add X`) describe what changed. Useful for release notes.

**BDR commits** document *why* this approach was chosen, blocking re-debate of the same trade-offs later.

This format makes commits **falsifiable**:
- **Contract** is true or false (user can/cannot do X)
- **Acceptance** passes or fails (test runs, result is yes/no)
- **Rejected** is accurate or inaccurate (these alternatives were considered or weren't)
- **Non-scope** is honest or dishonest (this was deliberately left out or was missed)

Result: every commit is **auditable** and reduces:
- Bikeshedding (rejected alternatives documented)
- Context loss (future engineers understand trade-offs)
- Scope creep (explicit non-scope prevents "why didn't you also...")
- Integration errors (acceptance criteria are unambiguous)

---

## When to Use BDR

- Feature work: always
- Bug fixes: yes, if non-trivial (if it's a one-liner, conventional commit is fine)
- Refactoring: yes (especially if it affects multiple modules)
- Tests: yes, if they're adding new coverage for a decision (not routine test updates)
- Docs/chores: conventional commit is fine
