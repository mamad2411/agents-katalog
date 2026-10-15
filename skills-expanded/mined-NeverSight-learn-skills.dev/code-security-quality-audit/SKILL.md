---
name: code-security-quality-audit
description: "Strict, language-agnostic security and code quality audit + repair loop. Find real issues, fix root causes, verify, pattern-search, repeat."
version: 1.0.0
author: ekasc
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [security, audit, code-quality, review, repair, static-analysis]
    related_skills: [codebase-audit, systematic-debugging, requesting-code-review, github-code-review]
---

# Strict Security and Code Quality Repair Skill

## Purpose

Audit any codebase, find real security, correctness, reliability, and code-quality issues, fix root causes, verify fixes, and repeat until no meaningful issues remain.

This skill is language-agnostic and agent-agnostic.

This is not a cosmetic refactor pass.
This is not a checklist dump.
This is a repair workflow.

## Prime Directive

Find the real issue.
Fix the root cause.
Verify the fix.
Search for the same bug pattern elsewhere.
Repeat.

No hacky fixes. No symptom hiding. No "make the test green" bullshit.

## Non-Negotiables

You must not:

- delete or weaken failing tests
- weaken validation to accept bad input
- bypass authentication, authorization, ownership, tenant, or permission checks
- swallow errors without a real recovery path
- return fake success
- hardcode users, IDs, secrets, paths, URLs, tokens, or magic values
- add arbitrary sleeps, retries, or timing hacks
- silence linters, typecheckers, formatters, or scanners without proof and justification
- hide internal failures behind vague catch-all patches
- change public behavior silently
- rewrite large parts of the codebase unless the structure itself is the root cause
- claim the system is "secure"

A fix is invalid if it only hides the symptom.

## Start Here

Before editing anything, do this in order.

### 1. Identify the System Type

Classify the codebase into one or more of these buckets:

- Web app / API / CRUD app
- SaaS / multi-tenant app
- Auth-heavy app
- File upload / file processing app
- URL fetcher / scraper / importer
- Webhook / callback consumer
- Background job / queue / worker system
- CLI / local developer tool
- Frontend-only app
- Library / SDK / package
- Data pipeline / ETL system
- Realtime / websocket / event-driven app

This classification decides where to audit first.

### 2. Find the Critical Assets

Identify what must be protected:

- user accounts
- sessions/tokens
- private user data
- tenant/workspace/project boundaries
- uploaded files
- database rows
- payments/billing data
- secrets/API keys
- internal network access
- background jobs
- external integrations
- generated/exported data

Do not audit blindly. Audit around assets.

### 3. Find the Trust Boundaries

List where untrusted input enters the system:

- HTTP requests
- forms
- route params
- query params
- JSON bodies
- file uploads
- URLs submitted by users
- webhooks
- CLI args
- environment variables
- background job payloads
- database records later reused as trusted data
- third-party API responses

Every trust boundary needs validation, authorization, safe error handling, and tests.

### 4. Run Baseline Verification

Find and run available checks:

- tests
- typecheck
- lint
- build
- formatter check
- migration/schema check
- security scan, if present

Record pre-existing failures separately.

Do not blame your changes for existing failures.
Do not call a fix verified unless the relevant checks were actually run.

## Triage Decision Tree

Use this to decide where to start.

### Web App / API / CRUD App

Start with:

1. authentication
2. authorization
3. ownership checks
4. input validation
5. data-layer queries
6. error handling

Most serious CRUD bugs are IDOR, missing ownership checks, bad validation, and unsafe query scoping.

### SaaS / Multi-Tenant App

Start with:

1. tenant/workspace/project isolation
2. every query that accepts an ID
3. list/search/filter endpoints
4. analytics/aggregation queries
5. background jobs that process tenant data
6. file access boundaries

Assume every resource ID is hostile until ownership is proven.

### Auth-Heavy App

Start with:

1. session creation
2. session expiry
3. callback/redirect handling
4. logout/invalidation
5. cookie/token storage
6. role/permission enforcement

Client-side auth state is not security.

### File Upload / File Processing App

Start with:

1. file size limits
2. file type validation
3. path traversal
4. public/private file access
5. storage permissions
6. archive extraction
7. cleanup behavior

Never trust filenames, extensions, MIME types, or paths from users.

### URL Fetcher / Scraper / Importer

Start with:

1. SSRF protection
2. protocol allowlist
3. DNS/IP validation
4. redirect validation
5. timeout limits
6. response size limits
7. content-type restrictions

Validate every redirect. The original URL is not enough.

### Webhook / Callback Consumer

Start with:

1. signature verification
2. replay protection
3. idempotency
4. event ordering
5. payload validation
6. safe failure behavior

Unsigned webhooks are attacker-controlled input.

### Background Job / Queue / Worker System

Start with:

1. idempotency
2. retry behavior
3. partial failure handling
4. transaction boundaries
5. concurrency/race conditions
6. poison message handling

Any job that can run twice must be safe to run twice.

### CLI / Developer Tool

Start with:

1. path handling
2. command execution
3. config loading
4. environment variable handling
5. destructive operations
6. filesystem permissions

Local tools can still destroy data or leak secrets.

### Frontend-Only App

Start with:

1. XSS
2. unsafe HTML/markdown rendering
3. token storage
4. stale auth state
5. API error handling
6. cache key scoping
7. optimistic update rollback

Frontend checks improve UX. They do not replace backend enforcement.

### Library / SDK / Package

Start with:

1. unsafe defaults
2. public API misuse risks
3. input validation
4. dependency risk
5. error semantics
6. backward compatibility

A library should make the safe path easy and the unsafe path explicit.

### Data Pipeline / ETL

Start with:

1. untrusted input parsing
2. schema validation
3. malformed records
4. partial writes
5. idempotency
6. data corruption risks
7. retry behavior

Silent bad data is still a production bug.

## Severity Rules

### Critical

Fix immediately:

- auth bypass
- authorization bypass
- cross-user or cross-tenant data leak
- account takeover risk
- SQL injection
- command injection
- code injection
- SSRF to internal/private networks
- arbitrary file read/write
- secret exposure
- forged webhook actions
- privilege escalation

### High

Fix next:

- IDOR
- missing ownership checks
- stored XSS
- unsafe file upload
- unsafe redirects in sensitive flows
- destructive action without authorization
- broken session expiry
- race condition corrupting important state
- sensitive data in logs or responses

### Medium

Fix after critical/high:

- bad validation
- bad pagination/filtering
- missing request limits
- incorrect error mapping
- inconsistent transactions
- missing idempotency
- stale derived state
- unreliable retries
- missing abuse limits

### Low

Fix only when it reduces future risk:

- confusing naming
- dead code
- duplicated logic
- unclear responsibility boundaries
- weak structure
- inconsistent patterns

Naming and dead code are not security issues by default. They become valid findings only when they obscure ownership, validation, state transitions, error behavior, or other important logic.

## Issue Ledger

Track every real issue:

```
ID:
Severity:
Category:
Affected area:
Root cause:
Failure/exploit scenario:
Fix:
Tests:
Verification:
Pattern search:
Status:
```

Do not fix random things without knowing why they matter.

## Repair Loop

Repeat this loop until the stop conditions are met.

### Pass 1: Map

- classify the system
- identify assets
- identify trust boundaries
- identify verification commands
- run baseline checks

### Pass 2: Audit Highest-Risk Flows

Pick the top 3 highest-risk flows based on the decision tree.

Examples:

- login/session flow
- user-owned resource CRUD flow
- file upload/download flow
- URL import flow
- webhook processing flow
- background job retry flow
- payment/billing flow
- admin action flow

For each flow, inspect:

- who can call it
- what input it accepts
- what resource it touches
- how ownership is verified
- what happens on failure
- what gets logged
- what tests exist

### Pass 3: Fix

For each issue:

1. write down the root cause
2. design the smallest clean fix
3. implement the fix
4. add or update regression tests
5. run narrow verification
6. run broader verification

A fix without verification is not complete.

### Pass 4: Pattern Search

After every fix, search for the same bug family.

Examples:

- one missing ownership check means inspect all handlers with resource IDs
- one unsafe query means inspect all queries for that resource
- one missing request limit means inspect all request parsing
- one unsafe redirect means inspect all redirects
- one bad cache key means inspect related cache keys
- one non-idempotent job means inspect all retryable jobs
- one path traversal risk means inspect all file operations

Bugs travel in families. Kill the family.

### Pass 5: Re-Audit Touched Areas

After fixing, re-read the changed code and ask:

- did this introduce a new edge case?
- did this weaken behavior?
- did this create inconsistent patterns?
- is the fix understandable?
- is the security boundary explicit?
- would a future maintainer accidentally undo this?

Then run verification again.

## Valid Fix Standard

A valid fix must:

- address the root cause
- preserve intended behavior
- improve or preserve security
- be narrow but not fragile
- be readable
- include regression coverage where practical
- be verified
- make the same bug harder to reintroduce

Invalid fixes include:

- broad catch-all error handling
- hidden fallback behavior
- fake success responses
- special-casing one test
- disabling failing checks
- weakening validation
- moving the bug somewhere else
- adding comments instead of enforcement

## Testing Requirements

For every fixed bug, add or update tests unless genuinely impractical.

Prefer behavior tests over implementation-detail tests.

Use the project's native tools.

Test intent:

- auth bug means missing/expired/invalid credentials test
- authorization bug means cross-user/cross-tenant access test
- validation bug means malformed/boundary input test
- data bug means persistence/integration test
- retry/job bug means duplicate execution test
- frontend state bug means stale state/cache/rollback test
- file bug means path/type/size/access test
- SSRF bug means private IP/redirect/protocol test

If a test cannot be added, document why and give a manual verification step.

## Stop Conditions

Stop only when all are true:

- critical issues are fixed or explicitly blocked
- high issues are fixed or explicitly blocked
- known correctness bugs are fixed or explicitly blocked
- relevant verification passes, or remaining failures are documented as pre-existing
- touched areas were re-audited
- repeated bug patterns were searched
- remaining risks are documented

Do not stop because the first bug is fixed.

## Blocker Rules

If blocked, report:

- what was attempted
- what failed
- why it blocks progress
- what evidence is missing
- safest next action

Do not guess.
Do not fake verification.
Do not pretend incomplete work is complete.

## Final Report

### Summary

- issues found
- issues fixed
- issues verified
- issues deferred
- remaining risk level

### Fixed Issues

For each issue:

- ID
- severity
- category
- root cause
- fix
- tests added/updated
- verification commands
- similar patterns checked

### Files Changed

For each changed file/module:

- what changed
- why it changed

### Verification

List commands run and results.

### Remaining Risks

List anything unresolved, blocked, uncertain, or out of scope.

Do not say "secure."
Say exactly what was checked and what passed.
