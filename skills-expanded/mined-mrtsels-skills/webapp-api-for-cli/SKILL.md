---
name: webapp-api-for-cli
description: Use when adding API+CLI access to a web app you own.
license: MIT
metadata:
  hermes:
    tags:
    - api
    - cli
    - nextjs
    - better-auth
    - architecture
    - same-source
    related_skills:
    - api-endpoint-probing
    - subagent-driven-development
    - cli-install-update-scripts
    - skill-repo-publishing
  source_frontmatter:
    version: 1.0.0
    author: Hermes Agent
    platforms:
    - linux
    - macos
  imported_from: hermes
---

# Web App → API + CLI (same-source architecture)

## When to Use

The user wants a CLI / AI-agent access layer for an **existing web application whose backend you can modify** (you have repo access). Typical ask: "把网站所有功能打包成 CLI + skill"。

This is NOT for third-party APIs with no repo access — that's `api-docsite-to-cli` / `api-endpoint-probing` territory.

## Core Principle (user-verified): Same Source, No Second API

**Never create a `/api/cli/*` namespace or a "CLI-specific" API.** The user's correction, verbatim in spirit: *"让前端和CLI同源"* — the frontend and CLI must share ONE contract.

```
src/lib/*.ts            ← single business-logic source (frontend RSC/Server Actions call this directly)
       │ thin wrapper
generic /api/* endpoints ← both frontend (future) and CLI (now) consume the same routes
       │ HTTPS + session
CLI                      ← pure endpoint consumer, ZERO business logic copy
```

Why this kills the "maintain two sets" problem:
- New feature = change `src/lib/*` once → endpoints reflect it → CLI untouched if contract unchanged
- CLI never holds a logic copy (no `getCourses` re-implemented in Python)
- Contract change = CLI changes only its call layer (field mapping), never its logic

**Anti-pattern:** `/api/cli/canteens` when `/api/canteens` already exists. A "CLI namespace" is the smell that you're building a second API.

## Phase 0: Recon Before Planning (gate — do this FIRST, no subagents)

Probe the real architecture before writing any plan. Checklist:

1. **Existing routes**: `ls src/app/api/**/route.ts` — you will usually find 40-80% of needed endpoints already exist
2. **Lib layer**: grep `export async function|export function` in `src/lib/*` — business logic almost always lives here, called directly by pages (RSC) or Server Actions
3. **Auth mechanism**: check `package.json` for auth lib (better-auth, NextAuth, custom) + how API routes guard (`getAdminUserForApi`-style patterns that return null instead of `redirect()`)
4. **Validation style**: does the project use zod? If not, follow existing hand-written `parseVote`-style validators
5. **Test runner**: vitest vs jest (affects every verify command)
6. **Package manager PATH**: pnpm/npm may not be on PATH in non-interactive shells — find it (`find ~ -maxdepth 4 -name pnpm -type f`) and export before any subagent work

Then write the plan with **generic endpoint paths** (`/api/courses`, `/api/college-picker/recommend`), never `/api/cli/*`.

## Phase 1: Thin-Wrapper Endpoints

Each new endpoint = small `route.ts` that:
1. Parses query/body (project's existing validation style, no new deps)
2. Calls the existing lib function (never re-implements logic)
3. Maps lib error codes → HTTP status (`RATE_LIMIT_EXCEEDED`→429, `NOT_FOUND`→404, etc.)
4. Returns JSON via a shared `ok()/fail()` helper

Follow the house style of one existing route (`src/app/api/canteens/route.ts` pattern).

## Auth: Reuse the App's Session, Don't Build JWT

- **better-auth (common in Next.js apps)**: enable the built-in `bearer()` plugin — one line — so `Authorization: Bearer <sessionToken>` converts to a session automatically. The CLI then authenticates with a token while the browser keeps using cookies. Details + pitfalls: `references/better-auth-bearer.md`.
- **Do NOT build a parallel JWT system** when the app already has sessions (this is the over-engineering trap).
- API-route guards must return `401/403 JSON`, not `redirect()` — check whether the lib's guard is redirect-based (see pitfall below).

## Pitfalls

- **Redirect-based auth guards break API routes**: lib functions calling `requireAuth()` from `next/navigation` throw/redirect in an API route context. Minimal fix: give the lib function an optional pre-authenticated-user parameter (default behavior unchanged, existing callers unaffected) — don't fork the function.
- **Never fabricate lib signatures**: read the actual exports before writing routes; the plan's assumed schema is often wrong (e.g. college-picker's real `RecommendInput` differs from any simplified plan).
- **Verification gates**: run the project's real gates (`pnpm lint` + `pnpm test` + `pnpm tsc --noEmit`) — not just your new files' tests — before claiming done.
- **patch tool's inline lint is not authoritative**: it doesn't resolve `@/` aliases; trust the project's real `tsc` instead.
- **Rate-limit key = authenticated user ID, not IP**: on serverless hosts (Vercel) CLI callers have no stable IP. After the auth guard, key on `\`<route>:<action>:${user.id}\`` with the write limit — and apply rate limiting to WRITE routes only (read routes stay unlimited — YAGNI).

## Orchestration: Subagent Batches

Proven pattern for this class of work (serial infra → parallel leaves):

1. **Phase 0 recon: parent does it** (read-only, no subagents)
2. **Infrastructure batch: ONE serial subagent** (shared lib layer others depend on)
3. **Route batches: parallel leaf subagents** — up to 3 concurrent, one per module (canteen/courses/picker...)
4. **Pre-seed EVERYTHING**: environment facts (pnpm path!), confirmed lib signatures, house style, expected error mapping, exact commit message. Fully pre-seeded batches finish in ~14 tool calls; research-heavy under-seeded ones hit the ~25-call cap and fail.
5. **Parent verifies every push**: `git fetch origin <branch>` + `git log origin/<branch>` — never trust a subagent's "committed and pushed" self-report.
6. If a subagent hits the tool-iteration cap with files written but unverified, **the parent finishes verification + commit** (cheaper than re-dispatching).
7. **Full code review before opening the PR — parent reads EVERY changed file.** Subagent summaries are not review. Known defect classes this catches:
   - **Dead code written per plan but never wired**: e.g. a rate-limiter built in the infra batch that no route calls, or 4 of 6 hand-written schemas unused because the plan over-specified the surface. Fix = wire the used subset, delete the rest (YAGNI), and prune the corresponding test files.
   - **Routes with ZERO tests**: review every new route and confirm its test file covers at least: auth-fail (401), the lib error-code → HTTP-status mapping table, and the rate-limit 429 branch.
   - Commit the review fixes as their own commit (`refactor(api): …`), re-run all gates, then open the PR.
8. **Parallel leaves writing to the SAME repo race each other**: when 3 leaf subagents each `git add <own files>` + commit + push to the same branch, they can (a) push non-fast-forward rejections, and (b) edit a shared file (e.g. `cli.py` dispatch) concurrently — one leaf's `--json` flag patch landed, another leaf saw the file mid-change and the third never knew. Verified on cupedia-cli Phase 2D. Mitigations: (a) have each leaf commit ONLY its own files and let the parent resolve push order / commit leftovers; (b) if leaves must share a file, say so in the pre-seed and expect a parent merge pass; (c) after the batch, `git log origin/main` and diff-review the shared file once.

## CLI Build Pitfalls (Python consumer side)

The CLI repo has its own trap set, all hit on cupedia-cli (2026-08-07):

- **argparse global flags don't work after the subcommand**: `cupedia --json course list` parses, but `cupedia course list --json` dies with "unrecognized arguments". Fix in TWO places: add `--json` (action="store_true", help=argparse.SUPPRESS) to every subparser, AND in `main()` do `if getattr(args, "json", False) or AGENT_MODE: config.set("output", "json")` so command modules only consult `config.output` — don't scatter `args.json` checks through modules.
- **Next.js 404 pages are HTML, not JSON**: App Router 404 responses return an HTML error page even when the route handler returns JSON for other statuses. CLI error handling must detect non-JSON bodies (`"<" in message` or empty) and print a concise message instead of dumping the page.
- **Deploy lag vs code correctness**: endpoints that exist in the app repo can 404/500 on the live host while the API PR is unmerged. A subagent "discovering" a 404 on production is NOT a code bug — verify against repo route definitions, not just the live server. Don't let subagents "fix" working code for a deployment lag.
- **UUID vs human-slug IDs**: canteen IDs on the live API are UUIDs, not the `uc-can`-style slugs in help text. When a command's help says "如 uc-can" but the API returns UUIDs, update the help text — or resolve by name first (fetch list, match by name).

See `references/cli-python-build-patterns.md` for full recipes.

## Deliverables Layout (repo boundary)

> 三仓库边界细则（fork/PR 流程、共享仓 PLAN gitignore）见 `skill-repo-publishing`——本节只给要点。

- **Frame the issue around the platform's own gap, NOT around the CLI** (user-verified correction, cupedia #534): the problem statement is "core features have no standard REST export — data is locked behind RSC / Server Actions / pure client imports, so non-browser consumers can't reach them". That is a deficiency of the component itself. Do NOT write "the CLI needs these endpoints" as motivation — the CLI is just the first consumer, not the reason, and naming it in the title or body invites scope objections. Title and body should stay consumer-agnostic.
- **App repo**: only the API routes + lib changes (PR into shared repo; each issue → its own PR with `Issue Number:` line)
- **Issue linking — `ref #<id>` vs `close #<id>`**: the user prefers `ref` (keeps the issue open; the PR's `Issue Number: ref #534` line satisfies the repo's PR-format rule and creates a cross-reference on the issue page). But GitHub's PR-sidebar "Linked issues" panel is ONLY populated by closing keywords (`closes/fixes/resolves`) — `ref` leaves `closingIssuesReferences` empty. Don't silently "upgrade" to `closes`; if the user asks about linking, verify with `gh pr view <n> --json closingIssuesReferences` and explain the trade-off (sidebar link ⇔ auto-close on merge).
- **CLI repo**: own public repo (`install.sh` + stdlib-only Python per `cli-install-update-scripts`). **Create the repo BEFORE Phase 2 coding starts**, not at the plan's final "publish" step — a plan that defers `gh repo create` to the end forces either un-pushed local commits or a mid-plan workflow break. Sequence: `gh repo create mrtsels/<name> --public` → clone to `~/<name>` → push per-batch from day one; the final "publish" step then reduces to skill-library cloning + e2e.
- **PR body should tell the code owner exactly what to do**: once the CLI repo
  is built and published BEFORE the app-repo PR merges, append two sections so
  the maintainer isn't left guessing (verified cupedia #535, 2026-08-07):
  - `## 外部交付物（已就绪，不在此 PR 内）` — link the CLI repo, note what was
    live-tested against existing endpoints, and state that the CLI degrades
    gracefully (clean 404 message, not a crash) until this PR deploys.
  - `## 需要 code owner 配合` — numbered: review+merge this PR, deploy it, and
    "nothing required before merge". This converts a passive PR into an
    actionable handoff and pre-empts "the CLI reports 404" issues.
- **Delete the fork when done**: if the workflow created a fork
  (`gh repo fork`) just to mirror the PR branch, the user may want it removed
  once the branch is on the shared origin. `gh repo delete <user>/<repo> --yes`
  requires the `delete_repo` OAuth scope — if `gh auth status` shows only
  `repo`, run `gh auth refresh -h github.com -s delete_repo` (interactive,
  browser code) first. Also `git remote remove fork` locally afterwards.
- **SKILL.md**: NOT in the app repo — lives in the CLI repo / skill library, published later
- **PLAN.md**: gitignored local working doc, never committed to the shared app repo

## References

- `references/better-auth-bearer.md` — enabling better-auth `bearer()` for CLI token auth, redirect-guard fix, error-code mapping pattern
- `references/cli-python-build-patterns.md` — argparse global-flag-after-subcommand fix, Next.js HTML 404 handling, deploy-lag vs code-correctness, parallel-leaf git races, ApiError contract mapping
