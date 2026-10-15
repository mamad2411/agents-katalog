---
name: solidstats-process-project-standards
description: >
  Universal project standards for every SolidStats repository (server-2, replays-fetcher,
  replay-parser-2, web, infrastructure). Covers GSD workflow obligations, session hygiene, git
  conventions, the cross-app boundary map (what each repo owns and must not cross), the cross-app
  compatibility protocol, security minimums, risk management, and documentation language.
  Use this proactively — read it at the start of any task in any SolidStats repo, even when the
  task doesn't name any of these topics. It is the shared baseline every other SolidStats skill
  assumes. Over-triggering is acceptable.
  Triggers: any task in a SolidStats repo, start of a work session, git commits, cross-repo
  changes, architecture decisions, session planning, before any implementation, Kubernetes,
  deploy, staging, infrastructure.
  Триггеры: любая задача в репо SolidStats, начало рабочей сессии, git коммиты, изменения с
  влиянием на другие репо, архитектурные решения, планирование, перед любой реализацией,
  Kubernetes, деплой, стейджинг, инфраструктура.
---

# SolidStats Project Standards — Universal Baseline

These standards apply to **every SolidStats repository** (server-2, replays-fetcher,
replay-parser-2, web, infrastructure) and every session. They define *how work happens* across
the platform, not how any single stack is written — the per-stack skills own the code details.

Read this skill at the start of any session, and keep it in mind throughout. The rules here
are non-negotiable across all five repos.

---

## A. GSD Workflow

SolidStats development runs exclusively through AI agents + GSD workflow. Direct, non-GSD
development is outside the process.

- **Planning docs are first-class:** before implementing anything, check `.planning/` for
  `PROJECT.md`, `REQUIREMENTS.md`, `ROADMAP.md`, and `STATE.md`. These files define the
  accepted architecture, current milestone, and in-flight decisions. Working from stale or
  missing context causes boundary violations and wasted work.
- **Keep planning docs current.** If a decision is made, a phase advances, or scope changes
  during a session, update the relevant planning file before the session ends.
- **Skills-first.** Before acting on any task, scan available skills. Use a skill even when
  there's only a small chance it helps — the cost is low, the benefit is standardized work.

---

## B. Session Hygiene

Every completed work session must leave the repository in a clean, committed state:

- Run `git status --short` at the end of every session. If there are uncommitted changes from
  the work just done, commit them before stopping.
- Do **not** delete or revert completed work to fake a clean status. If the intended work is
  incomplete, ask what to do rather than silently discarding it.
- The rule is: *commit the intended results of the session, not a reset to the previous state.*

---

## C. Git Conventions

All commits in every SolidStats repo follow **Conventional Commits**:

```
<type>(<scope>): <short description>
```

Common types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`.
Scope: the phase number, feature area, or affected layer (e.g. `feat(17-03): …`,
`fix(ingest): …`, `docs(planning): …`).

**Absolute rules:**

- Never run `git commit`, `git push`, or any destructive git operation (reset --hard, force
  push, branch -D, rebase) without an explicit instruction from the user in the current message.
  Authorization from a previous message does not carry forward.
- Never skip hooks with `--no-verify` or `--no-gpg-sign` unless explicitly asked to. If a
  pre-commit hook fails, fix the underlying issue — the hook is the signal, not the obstacle.
- When a pre-commit hook fails, the commit did not happen. Create a new commit after fixing;
  do not amend the previous one (amending could silently modify work that already shipped).

---

## D. Cross-App Boundary Map

SolidStats is a five-repo platform. Each repo has a strict ownership boundary. Crossing it
introduces hidden coupling that is hard to untangle later.

| Repo | Owns | Must NOT |
|------|------|----------|
| **server-2** | Canonical business state: replays, parse_jobs, parse_results, stats, identity, moderation. HTTP API. RabbitMQ orchestration. Auth (Steam OpenID). | Parse OCAP replay content. Crawl/fetch external replay sources. |
| **replays-fetcher** | Raw replay object storage (S3). Ingest staging/outbox records. Source metadata (URL, checksums, fetch timestamps). | Parse replay contents. Mutate server-2 business tables (replays, parse_jobs, parse_results, stats, identity, moderation). Publish RabbitMQ messages. Calculate stats. |
| **replay-parser-2** | OCAP parsing. Versioned parser artifacts. RabbitMQ worker. Health probes. | Write parser results directly into server-2 business tables. Own or assign canonical player identity (server-2 owns player matching). |
| **web** | Frontend. Typed API client (generated from server-2 OpenAPI schema). UI state. | Directly access the database or S3. Bypass the typed API client with raw fetch. |
| **infrastructure** | Kubernetes staging manifests (`k8s/staging/`). Runtime wiring (secrets, env, service mesh). Deployment scripts and runbooks (Bash/Python). Staging CI/CD pipeline. | Own application source code or build container images (app repos do this). Manage production environment (out of scope for v1). Store secret values in git (secrets come from GitHub environment at deploy time only). |

When a task involves code in one repo but touches a boundary, stop and verify the change
stays within that repo's ownership.

**Infrastructure ↔ app repos coordination:** when an app repo changes its container image
interface (env vars, ports, health probe paths, S3 key layout, RabbitMQ queue names), the
infrastructure repo's Kubernetes manifests and secret-rendering scripts must be updated in
sync. Image SHA pinning in `k8s/staging/` must be updated explicitly — the infrastructure
repo never auto-pulls `latest`.

---

## E. Cross-App Compatibility Protocol

Changes in one repo can break another silently. Apply this risk-based check before
implementing:

**Low risk — local only.** Changes that affect only internal business logic, no cross-repo
contracts: rely on local planning docs (`.planning/`). Proceed normally.

**High risk — cross-repo contracts.** Any change that touches the following requires reading
the adjacent app's planning docs or asking the user for confirmation before proceeding:

- **API contract** (server-2 route shape, response structure, error codes)
- **Data model** (PostgreSQL schema, enum values, column types)
- **RabbitMQ message shape** (queue name, message body, routing key)
- **S3 key layout** (bucket, prefix, object naming)
- **Parser contract** (artifact schema version, field names, retryability codes)
- **Auth/identity shape** (session structure, role names, user fields)
- **Moderation workflow** (status transitions, event types)

The check: *does this change affect what server-2 exposes, what the parser produces, or what
web consumes?* If yes, verify compatibility before writing code.

---

## F. Security Minimums

These rules apply to all code, commits, and logs across every SolidStats repo:

- **Never log, commit, or output:** secrets, API tokens, database connection strings, S3
  access keys, RabbitMQ credentials, raw replay bytes, or unpublished parser artifacts.
- **Never hardcode environment-specific values.** Use environment variables validated at
  startup (e.g. `envalid` for Node, a validated config struct for Rust). Startup should fail
  fast if required env vars are missing or malformed.
- **Before committing:** check that `.env`, `.env.local`, and any file containing credentials
  is either in `.gitignore` or explicitly excluded from the commit. Never commit secrets to
  git history — they are permanent even after deletion.

---

## G. Risk Management Protocol

When a request is risky, potentially harmful, or would expand scope beyond the current plan:

1. **Explain the concrete reason** — name the specific risk, the boundary it crosses, or the
   plan it contradicts.
2. **Propose 1–3 safer alternatives** or a GSD plan that achieves the goal without the risk.
3. **Ask for explicit confirmation** before proceeding with anything that falls into these
   categories:
   - Crosses a cross-app boundary (§D)
   - Modifies a high-risk cross-repo contract (§E)
   - Contradicts an accepted architecture decision in `.planning/PROJECT.md`
   - Deletes, overwrites, or discards completed work
   - Conflicts with current test quality, security rules, or repo structure standards

Do not blindly execute instructions that conflict with architecture, accepted decisions, or
the quality gates in this repo. Challenge, explain, propose alternatives — then wait.

---

## H. Documentation Language

All SolidStats repos follow the same documentation language standard:

- **Code, comments, planning docs, skill bodies, README files:** English only.
- **GSD workflow responses** (conversations within a GSD session): Russian.
- **Skill trigger phrases** (`description` field in `SKILL.md`): RU + EN mandatory. Every
  skill must trigger on both languages — the team works in a RU context.

When writing any documentation, planning artifact, or code comment: English, no exceptions.
When responding in a GSD session or replying to the user: Russian.

---

## I. MCP Usage

SolidStats development relies on MCP tools to access current documentation. **Never use
training data as the primary source for library APIs** — it has a cutoff and may reflect
outdated or incorrect APIs. Prefer MCP tools for any external library lookup.

### Context7 — library documentation (primary MCP)

Use Context7 whenever you need to look up or verify a library's current API, configuration
options, migration guide, or best practices. This applies proactively — don't wait for a
type error to check the docs.

**Common lookup triggers:** adding a new dependency, upgrading a package, using a method
you're not 100% sure about, hitting an unexpected type error, writing a new integration.

**How to use (two-step pattern):**

```
# Step 1: resolve the library ID
mcp__context7__resolve-library-id({ libraryName: "fastify" })

# Step 2: query the docs
mcp__context7__query-docs({ context7CompatibleLibraryID: "/fastify/fastify", topic: "plugins" })
```

**Key libraries by repo — always look these up via Context7, not training data:**

| Repo | Libraries to look up via Context7 |
|------|-----------------------------------|
| **server-2** | fastify, @sinclair/typebox, @fastify/type-provider-typebox, @fastify/swagger, kysely, pg, amqplib, pino, envalid, prom-client, @aws-sdk/client-s3 |
| **replays-fetcher** | zod, commander, @aws-sdk/client-s3, pg |
| **web** | @tanstack/start, @tanstack/router, @tanstack/react-query, @tanstack/react-table, @tanstack/react-form, @ark-ui/react, vanilla-extract, openapi-typescript, openapi-fetch, openapi-react-query |
| **replay-parser-2** | tokio, serde, serde_json, thiserror, lapin, aws-sdk-s3, axum, tracing, tracing-subscriber |
| **infrastructure** | Kubernetes API reference, kubectl |

### WebSearch / WebFetch — for what Context7 doesn't cover

Use WebSearch or WebFetch for:
- GitHub issues, bug reports, and PRs for a library
- Release notes and migration guides not yet in Context7
- Stack Overflow / forum answers for specific error messages
- Documentation for tools without a Context7 entry (e.g. k3s, MinIO, Timeweb S3)

### Loading MCP tools: Claude Code vs. standalone agents

**In Claude Code (main session):** Context7, WebSearch, and WebFetch appear as *deferred
tools* — their schemas are not loaded until requested. Load them explicitly before use:

```
ToolSearch({ query: "select:mcp__context7__resolve-library-id,mcp__context7__query-docs", max_results: 2 })
ToolSearch({ query: "select:WebSearch,WebFetch", max_results: 2 })
```

**In subagents spawned by Claude Code** (gsd-executor, gsd-planner, gsd-phase-researcher,
etc.): the same mechanism applies — the tools are available but deferred. Always call
`ToolSearch` to load Context7 before the first documentation lookup.

**In standalone agents outside a Claude Code session** (e.g. CI, remote triggers): install
the Context7 MCP server explicitly and add it to the agent's MCP config:

```bash
npx -y @upstash/context7-mcp@latest
```

Then configure the agent's MCP settings to include the Context7 server so it's available
at tool-call time.

### When NOT to use Context7

- For SolidStats-specific code or business logic (no external library is involved).
- For a library you've just looked up in the same session and the answer hasn't changed.
- For stable standard library APIs (e.g. Node.js `fs`, Rust `std::collections`) that are
  unlikely to differ from training data.

---

## References

For the standard CI/CD pipeline pattern used across SolidStats repos (GitHub Actions structure,
concurrency, job layout, Docker build), see
[`references/ci-cd-pattern.md`](references/ci-cd-pattern.md). Read it when setting up or
modifying a `.github/workflows/` file.
