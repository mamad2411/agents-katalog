# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

This repo holds two distinct things:

1. **A personal finance dashboard** - a local income/expense tracker being built
   from scratch. Its product spec (features, data model, scope) lives in
   `SPEC.md`; how work on it is organized lives in this file. See "Building the
   finance dashboard app" below.
2. **`agent-pack/`** - a self-contained, portable bundle that installs a set of
   specialist **`-warden`** subagents into *another* project and wires them into
   that project's `CLAUDE.md`. It is a standalone product with nothing to build
   or run; everything about it lives under `agent-pack/` and is documented in the
   "Commands" and "Architecture" sections further down.

The finance app is built here **using** the wardens installed in
`.claude/agents/` (the same set the pack ships).

## Building the finance dashboard app

The product spec is **`SPEC.md`** - the single source of truth for *what* the app
does (the two input channels, the transaction model, core vs. future scope, the
design bar, and the open questions still to settle). Read it for feature
requirements. It deliberately holds **no** coding rules or process, so it never
drifts against them.

### Where each kind of rule lives (authority split)

| Question | Source of truth |
|----------|-----------------|
| *What* should the app do? (features, data model, UX, scope) | `SPEC.md` |
| *How* we work + this project's concrete coding conventions | this file (below) |
| *How* each layer is written in general (per-layer rules) | the `-warden` files in `.claude/agents/` |
| Tracked defects / backlog (optional) | `BUG.md`, if present |

Keep these from overlapping rather than resolving conflicts after the fact. If
they ever do disagree: `SPEC.md` wins on behavior, the owning warden wins on
layer-level code shape, this file wins on project conventions and process.

### Working style

- This is a **learning project** to deepen Java skills. Prefer idiomatic,
  well-structured code and explain the architectural "why" as you go - treat the
  reader as a developer who wants to understand, not just receive working code.
- **Propose a milestone plan first and wait for approval** before building.
- **Ask clarifying questions** when requirements are ambiguous rather than
  assuming - the standing ones are in `SPEC.md` under "Open Questions".
- Build **incrementally**; each milestone must be independently runnable and
  testable before moving on.
- Before adding code, check whether existing code can be reused or extended;
  refactor shared logic into common components/services instead of copying it,
  and briefly explain the refactor so the pattern is learned.

### Build order (milestones)

Frontend-first with mock data, then the backend, then wiring. Tracked as `SR-<n>`
tickets in `BUG.md` (the authoritative backlog); this list is the shape, `BUG.md`
holds the detail.

- **Phase A — frontend foundation:** scaffold (Vite + React 18, JS) → run scripts
  → design tokens + app shell/nav → mock-data module + `api.js` seam.
- **Phase B — frontend screens (mock data):** transaction list + filtering →
  manual entry (add/edit/delete) → dashboard charts → file-import flow UI →
  category-management UI.
- **Phase C — backend + wiring:** Spring Boot skeleton + MySQL schema → entities /
  repositories → import pipeline → categorization → dashboard aggregation → point
  `api.js` at real endpoints → extend the run scripts to boot backend + MySQL.

Each screen is built against the `api.js` seam so the swap to the real backend
(Phase C) touches only that one module.

### Running the app

From the repo root, `./run.ps1` (Windows) or `./run.sh` (macOS / Linux / Git Bash)
boots the whole stack in order: it checks the toolchain (Node/npm, Java, Maven,
Docker), installs frontend deps on first run, starts MySQL via Docker Compose and
waits for it to be healthy, starts the Spring Boot backend on http://localhost:8080
(waiting for `/actuator/health`), then starts the Vite dev server at
http://localhost:5173. Backend logs interleave in the console. Ctrl+C stops the
backend the script started and leaves the MySQL container running (data persists;
stop it with `docker compose stop`). The two scripts are kept in sync (like the
pack installers).

### Warden scope for this app

The full `-warden` routing table (see "Agent-driven development" below) is
inherited from the portable pack and names an owner for every backend domain, not
only the ones this app exercises. Given `SPEC.md`'s constraints (runs locally, no
external APIs, no bank integrations, no auth providers), two routed wardens are
**dormant** for now: **api-client-warden** (no outbound integrations to build) and
the authn/authz half of **security-warden** (no auth provider - though its
input-validation and OWASP guidance still applies to local input). They stay in
the routing map, provisioned for future scope or portable reuse; don't treat their
absence of work as a gap.

### Project code conventions

This project's concrete choices - the wardens enforce the generic per-layer
shape, these say which choice this project makes:

- **DRY is a hard rule.** Both input channels converge on a single service layer;
  validation, categorization, and persistence logic are never duplicated between
  them. Repeated frontend patterns (form fields, currency formatting, date
  handling, chart config) become reusable components/hooks/utils.
- **Money is `DECIMAL` / `BigDecimal`, never floating point** - storage and
  computation both.
- **Validation is defined once and reused** (e.g. Bean Validation on DTOs shared
  between the import and manual-entry channels).
- **Proper layering:** entities, repositories, services, controllers, DTOs - each
  with a clear, single role.
- **Heavy commenting - comments matter as much as the code.** Every class gets a
  Javadoc/JSDoc block on its purpose and place in the architecture; every
  non-trivial method explains what it does and *why*; annotations/hooks that
  aren't self-evident (why `@Transactional` here, why `useMemo` there) get an
  inline note; the "gotchas" (why `BigDecimal`, why the duplicate-detection
  strategy works as it does) are called out.
- **Meaningful validation and error messages on both ends.**
- **Unit tests** cover the import-parsing logic and the manual-entry validation -
  the places bugs will concentrate.

## Commands

There is no build/lint/test toolchain. The only executable artifacts are the two
installers, which are functionally equivalent and are run **from the root of the
target project** (scaffolding any governing docs the target lacks):

```powershell
# Windows PowerShell / PowerShell 7+
./agent-pack/install-agents.ps1                       # target = current dir
./agent-pack/install-agents.ps1 -TargetRoot C:\code\proj -Force
```
```bash
# bash / macOS / Linux / Git Bash
./agent-pack/install-agents.sh                        # target = current dir
./agent-pack/install-agents.sh -f /path/to/project    # -f overwrites existing agents
```

Both installers:
1. **Scaffold any missing governing doc** (`CLAUDE.md`, `SPEC.md`, `BUG.md`, `README.md`) from `payload/templates/*`; an existing doc is never overwritten (not even by `-Force`/`-f`).
2. Copy `payload/agents/*` into `<target>/.claude/agents/` (existing files are skipped unless `-Force`/`-f`), and install `payload/hooks/commit-msg` into `<target>/.githooks/`, setting `core.hooksPath` when the target is a git repo and ensuring a `.gitattributes` `.githooks/** text eol=lf` rule (skip the whole hook step with `-NoHooks`/`--no-hooks`).
3. Replace the block between `<!-- BEGIN agent-pack -->
## Agent-driven development

This project uses a set of specialist **`-warden`** subagents (in
`.claude/agents/`). Feature and change work is delegated to the warden that owns
the domain — that agent **writes** the code; the main agent coordinates and
handles anything outside these domains. Invoke them proactively when a prompt
lands in their domain, not only for after-the-fact review.

- Service / business-logic classes (use-cases, DI, transactions, DTO/domain mapping) → **service-warden**
- Persistence / data-access layer (ORM entities, repositories/DAOs, queries, schema/migration) → **persistence-warden**
- API controllers / routers / endpoint handlers (routes, status codes, request/response DTOs, endpoint validation) → **controller-warden**
- API error/exception handling, status-code mapping, validation errors → **exception-warden**
- Frontend UI (components, state, the API-call seam, token-driven styling) → **frontend-warden**
- Access control, input validation at trust boundaries, secret handling, OWASP defenses (injection, XSS, CSRF) → **security-warden**
- Outbound integrations / HTTP clients (timeouts, retries with backoff, circuit breakers, response validation) → **api-client-warden**
- Logging, metrics, and tracing (structured logs, no PII, correlation ids, log levels, instrumentation) → **observability-warden**
- Application configuration (environment-driven values, no hardcoded URLs/ports/credentials, startup validation, safe defaults) → **config-warden**
- Unit and integration tests → **test-warden**
- Package/directory structure across the backend and frontend roots (where files live, module layout, scaffolding a new project/module, relocating misplaced files, cross-layer import boundaries) → **structure-warden**
- The project's own governing docs — keeping `SPEC.md` (what the app does), `CLAUDE.md` (how work is organized + project conventions + this routing table), and `BUG.md` (the backlog, if present) consistent and non-overlapping → **sync-warden**

A feature that spans domains is split so each agent authors its own layer. When
a change needs new files or a new module, **structure-warden** decides and
creates *where* they live; the owning domain warden authors *what* goes inside.

> The concrete paths, stacks, and framework names inside each agent file are
> examples from the pack's origin project — the rules themselves are language/
> framework-agnostic. Adjust those example paths to match this project's layout;
> you do not need to change the rules.

### Authorship stamp

Every class or function an agent authors or substantially rewrites carries an
authorship tag on the line directly above its declaration, using the file's
line-comment syntax:

```
// @agent: service-warden      (Java / JS)
# @agent: exception-warden     (Python)
```

Keep the tag on edits; change it only when a different agent takes the code over.

### Keeping the docs in sync

**sync-warden** guards the boundary between `SPEC.md`, `CLAUDE.md`, and (when
present) `BUG.md`: it moves coding rules or process that leak into the spec back
to their proper home, checks that every feature traces to a build milestone (and
a backlog item when one is tracked), and keeps the routing table above matching
the agents actually installed in `.claude/agents/`. It edits the documents, never
the code, and skips `BUG.md` checks when there is no backlog. Invoke it after
editing any of those files.

### Ticket workflow (active in this project)

The pack also includes **ticket-warden**, which enforces a ticket-driven
commit workflow. In the portable pack it is **optional and unwired**: the pack
ships neither a backlog file nor a `.githooks/commit-msg` backstop, so a fresh
install must set those up (or ignore ticket-warden) separately.

**This project has adopted it.** The backlog lives in `BUG.md` as `SR-<n>`
tickets, and a `.githooks/commit-msg` hook is installed and active (git points at
it via `core.hooksPath = .githooks`). The hook is **prefix-only**: it rejects any
commit whose subject line is not `SR-<n> <description>` (merge, revert, and
`fixup!`/`squash!` subjects are exempt), and it does **not** guard the branch —
committing on `main` is allowed. ticket-warden is the smart layer that makes the
right ticket exist so commits pass; the hook is the mechanical backstop.

The hook scripts under `.githooks/` are tracked and travel with the repo, but
`core.hooksPath` lives in the local `.git/config`, which is **not** cloned — so
each fresh clone must enable the hook once with:

```sh
git config core.hooksPath .githooks
```
<!-- END agent-pack -->` markers in the target's `CLAUDE.md` with the content of `payload/claude-md-section.md` — idempotent, so re-running refreshes in place rather than duplicating.

To verify a change, run an installer against an empty throwaway target dir and
inspect the scaffolded docs, the resulting `.claude/agents/`, the marker block,
and `.githooks/commit-msg`. The `agent-pack/TEST.md` `TS-<n>` catalog enumerates
the scenarios to check (fresh/partial installs, hook/CRLF behavior, parity); keep
its *Expected* blocks updated when installer behavior changes. Keep the two
installers in sync — a behavior change to one must be mirrored in the other.

## Architecture

The whole design is a payload plus two installers that deliver it:

- **`payload/agents/<name>-warden.md`** — one subagent definition each. Frontmatter
  is `name` + `description` (the description is written to trigger *proactive*
  delegation, with concrete "Use PROACTIVELY when…" / "MUST BE USED…" examples)
  + `tools`. All wardens declare `tools: Read, Grep, Glob, Edit, Write` except
  **ticket-warden**, which also gets `Bash` (it runs git).
- **`payload/agents/<name>-warden-refs/`** — companion files holding the concrete
  violation/correct code examples for that warden, split per language
  (`*-examples-java.md`, `*-examples-python.md`, and React for the frontend and
  structure wardens). The agent Reads these on demand. **ticket-warden and
  sync-warden have no refs dir.**
- **`payload/claude-md-section.md`** — the "Agent-driven development" block the
  installer injects into the target's `CLAUDE.md`. It is the routing table that
  maps a domain to the warden that owns it.
- **`payload/templates/{CLAUDE,SPEC,BUG,README}.md`** — starter governing docs.
  The installer copies each into the target only when it is missing, never
  overwriting an existing one. The `CLAUDE.md` template carries no marker block —
  injection appends it — so `claude-md-section.md` stays the single source of the
  routing table.
- **`payload/hooks/commit-msg`** — the `SR-<n>` ticket-prefix commit hook. The
  installer copies it into `<target>/.githooks/` and sets `core.hooksPath` when the
  target is a git repo; `--no-hooks`/`-NoHooks` skips it. Prefix-only (see the
  ticket workflow above): it gates the commit subject, not the branch. The
  installer also ensures a `.gitattributes` `.githooks/** text eol=lf` rule
  (created/appended without clobbering an existing file) so the hook stays LF and
  keeps working under `sh` after a checkout on an autocrlf machine.

### Rules vs. examples — the core invariant

Each warden's **rules are deliberately language/framework-agnostic and
self-contained**; the **examples in the `-refs/` files are not** — their paths,
stacks, and framework names come from this pack's origin project. When editing:
change rules for behavior, and keep them stack-neutral; put anything
concrete/stack-specific in the `-refs/` files, never inline in the rule text.

### Domain ownership (the delegation map)

Wardens are *authors*, not just reviewers — the warden that owns a domain writes
that layer's code; a cross-domain feature is split so each warden authors its own
layer:

- **service-warden** — service / business-logic (use-cases, DI, transactions, DTO↔domain mapping)
- **persistence-warden** — data-access layer (ORM entities, repositories/DAOs, queries, schema/migrations)
- **controller-warden** — API controllers/routers/endpoints (routes, status codes, request/response DTOs)
- **exception-warden** — error/exception handling, status-code mapping, validation errors
- **frontend-warden** — UI (components, state, the API-call seam, token-driven styling)
- **security-warden** — application-level security at the trust boundaries: authn/authz on every endpoint, input validation, secret handling, OWASP defenses (injection, XSS, CSRF)
- **api-client-warden** — outbound integrations: timeouts, retries with backoff, circuit breakers, response validation, typed local errors for remote failures
- **observability-warden** — logging/metrics/tracing: structured logs, no PII, correlation-id propagation, correct log levels, key-operation instrumentation
- **config-warden** — application configuration: environment-driven values, no hardcoded URLs/ports/credentials, startup validation, safe defaults (12-factor)
- **test-warden** — unit and integration tests
- **structure-warden** — package/directory layout across the backend and frontend roots (where files live, module organization, scaffolding new projects/modules, relocating misplaced files, cross-layer import boundaries)
- **sync-warden** — cross-document consistency between the project's own governing files: `SPEC.md` (what), `CLAUDE.md` (how / process / conventions / routing), and `BUG.md` (backlog, when present). Relocates leaked rules to their proper home, keeps every feature traceable to a milestone, and keeps the routing lists matching `.claude/agents/`. Prose-only — no refs dir, no `@agent:` stamp.
- **ticket-warden** — *wired up by the installer.* An "agentic product owner" enforcing an `SR-<n>` ticket + commit-prefix workflow. The installer scaffolds a `BUG.md` backlog and installs the `.githooks/commit-msg` hook (prefix-only; `--no-hooks`/`-NoHooks` opts out). ticket-warden makes the right ticket exist so commits pass the hook.

### Conventions baked into every warden

When editing existing warden files or adding a new one, preserve these shared
patterns so the pack stays internally consistent:

- **Structure:** each file has `Goals (prioritized)`, an explicit **Negative scope**
  ("this agent does NOT…"), numbered `Rules`, a `Working Method`, an
  `Authorship stamp` section, and a `Report Format` section.
- **Authorship stamp:** code a warden authors/rewrites carries an `@agent: <name>`
  tag on the line directly above the declaration, in the file's line-comment
  syntax (`//` for Java/JS, `#` for Python). The tag stays on edits; it changes
  only when a different warden takes the code over.
- **Report Format:** each warden defines an identical audit-report skeleton
  (title + attribution, metadata, framing paragraph, a ranked summary table as
  the centerpiece, detailed findings, positive notes, convention notes, files
  referenced) and saves it to `docs/<name>-warden-audit.md` unless told otherwise.
  Inline (non-file) findings use the `RULE <n>: <file>:<line> — <finding> — <fix>` one-liner form.
