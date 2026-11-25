---
name: quality-github-issues
description: Use this skill when you need to triage, draft, or improve a GitHub issue with strong repro steps and acceptance criteria; use runSubagent to gather evidence and pre-fill the issue.
allowed-tools: runSubagent, mcp_github_issue_read, mcp_github_issue_write
---

# Quality GitHub Issues (Freelancerino)

Use this skill when you need to file (or help someone file) a GitHub issue that is easy to understand, easy to reproduce, and easy to validate after the fix.

This skill is optimized for this repo’s stack:

- Next.js App Router (Next.js 16) + React 19 + TypeScript
- Bun workflow
- Drizzle ORM + Postgres
- Clerk auth + per-workspace tenancy
- next-intl locale routing (`/{locale}/...`)

## What “good” looks like

A quality issue:

- States the problem and impact in one sentence.
- Is scoped to **one** user-facing bug/feature/change.
- Includes a minimal reproduction or exact steps.
- Separates **Expected** vs **Actual**.
- Includes enough context to debug (routes, IDs _only if safe_, logs, screenshots).
- Defines **acceptance criteria** so the fix can be verified.

## Before you file

### 1) Check for duplicates

Search existing issues and PRs with a few keywords:

- Feature name (e.g. “invoice snapshot”, “client duplicates”, “workspace settings”)
- Error message substring
- Route (e.g. `/en/(dashboard)/clients`)

If it’s a duplicate, comment on the existing issue with your additional repro/context instead of creating a new one.

### 2) Confirm scope (bug vs feature vs chore)

- **Bug**: Something is wrong/broken compared to intended behavior.
- **Feature**: New behavior or capability.
- **Chore/Refactor**: Internal improvement, no user-facing change.

### 3) Sanitize data

Do **not** paste:

- Secrets (API keys, webhook secrets, database URLs)
- Session tokens, cookies, JWTs
- Personal data that shouldn’t be public

If needed, redact values and keep structure (e.g. `userId: "user_***"`).

## Issue title guidelines

Format (pick one):

- Bug: `Bug: <short symptom> in <area>`
- Feature: `Feature: <capability> for <persona/area>`
- Tech: `Tech: <component> <change>`

Good:

- `Bug: Client duplicates dialog crashes on empty lastName`
- `Feature: Finalized invoice PDF uses immutable snapshot`

Avoid:

- `Broken`
- `Help!!!`
- `It doesn’t work`

## Copy/paste issue template

Use this template in a new issue body.

### Summary

One sentence describing what’s wrong / what you want.

### Impact

Who is affected and how badly? (blocker / annoying / cosmetic)

### Area

Check all that apply:

- [ ] Clients
- [ ] Projects
- [ ] Time
- [ ] Invoices / PDFs
- [ ] Expenses
- [ ] Auth / Clerk
- [ ] i18n / locales
- [ ] DB / Drizzle
- [ ] UI / styling

### Expected behavior

What should happen.

### Actual behavior

What happens instead.

### Reproduction steps

Provide the smallest reliable sequence:

1. …
2. …
3. …

If this is flaky/intermittent, describe frequency and any patterns.

### Screenshots / recordings

Attach visuals if it’s UI-related.

### Logs / errors

Paste relevant logs/errors (redact secrets/PII). If it’s a Next.js error overlay, include the stack trace.

If this is a performance/cost issue, include (if you can):

- Approx request count / “how often” it happens
- What is slow: initial load vs action submit vs navigation
- Any evidence of **N+1** (same query repeated)
- Whether broad revalidation might be happening (`revalidatePath` on large paths)
- Vercel angle: likely driven by **invocations** (too many renders/actions) or **duration** (slow DB / sequential awaits)

### Environment

- OS: Windows/macOS/Linux
- Runtime: Bun version
- Node: (if relevant)
- Browser: (if relevant)
- App area/route: `/{locale}/(dashboard)/...`

### Tenancy / workspace context (if applicable)

- Workspace: personal workspace (Clerk user)
- Confirm this affects only your workspace or multiple? (if known)

### Acceptance criteria

List verifiable outcomes. Example:

- [ ] The crash no longer occurs when lastName is empty
- [ ] An inline validation error is shown instead
- [ ] Tests added/updated to cover the case

If it’s a perf/cost issue, add acceptance criteria like:

- [ ] Query count reduced on route X (no obvious N+1)
- [ ] Independent reads parallelized
- [ ] Revalidation narrowed (tags preferred over broad paths)
- [ ] No tenant-safety regression (workspace-scoped keys/tags)

### Notes / suspected cause (optional)

Links, code pointers, or hypotheses.

## Repo-specific “extra context” that helps a lot

Include these when relevant:

### For Server Actions / mutations

- The action name and file path if you know it (e.g. `actions/clients/mutations.ts`)
- The input payload shape (redacted)
- Whether the issue is authorization/tenancy related (workspace scoping)

### For DB issues (Drizzle/Postgres)

- Migration name (if newly introduced)
- Table(s) involved (`db/schema/...`)
- The failing query or constraint error

### For invoices/PDF/snapshots

- Draft vs finalized status
- Currency + locale
- Whether the snapshot should be immutable

### For i18n / routing

- Locale in URL (`/en` vs `/de`)
- Whether copy is missing from `messages/en.json` or `messages/de.json`

## Using runSubagent to triage and pre-fill issues

Use `runSubagent` when you want help gathering evidence fast **without** making changes.

## Using GitHub issue tools (issue_read / issue_write)

When you *do* want to interact with GitHub issues directly (instead of only drafting text), use:

- `issue_read`: fetch issue details, labels, comments, and sub-issues to confirm scope and avoid duplicates.
- `issue_write`: create a new issue or update an existing one (e.g., improve repro steps, add acceptance criteria, close as duplicate).

In this repo’s tooling, these map to the GitHub MCP tools `mcp_github_issue_read` and `mcp_github_issue_write`.

Good subagent tasks:

- Search the repo for a symbol, route, or error string
- Locate the most likely file(s) responsible
- Identify existing tests or where to add one
- Check for duplicate issues (if GitHub access is available in your environment)
- Draft a strong issue title + body from your notes

### Example subagent prompt (copy/paste)

Provide:

- What you observed
- The route/screen
- Any error message
- Your best repro steps

Ask the subagent to return:

- Suspected code locations
- Minimal repro
- Suggested acceptance criteria
- Suggested labels

### What to do with the result

- Paste the drafted body into a new issue
- Attach screenshots/logs you have locally
- Make sure the final issue contains **Expected vs Actual** and **Acceptance criteria**

## Labels and severity (recommended)

Use consistent labels (adapt to repo’s label set):

- Type: `bug`, `feature`, `chore`
- Area: `clients`, `projects`, `time`, `invoices`, `pdf`, `i18n`, `auth`, `db`
- Priority: `p0-blocker`, `p1-high`, `p2-medium`, `p3-low`

If labels don’t exist yet, include your suggestions in the issue body.

## Validation mindset (write it in the issue)

A fix is “done” when:

- Repro steps no longer reproduce the problem
- Acceptance criteria are satisfied
- A test is added/updated (when practical)
- There’s no tenant data leakage (workspace scoping stays correct)

## References (repo)

- Product spec: `docs/PRD.md`
- DB schema: `db/schema.ts` and `db/schema/`
- i18n messages: `messages/en.json`, `messages/de.json`
- Actions: `app/actions/*`
- Tests: `tests/*`
