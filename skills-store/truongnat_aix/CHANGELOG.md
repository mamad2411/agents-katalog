# Changelog

All notable changes to **aix** are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

### Added
- **kb-server auto-start/stop**. `aix run --auto` and Guardrail mode now automatically ensure `kb-server` is running before execution and cleanly shut it down (using a new `POST /shutdown` endpoint) when the session finishes, cancels, or fails.
- **kb-server plugin mode integration**. The Claude Code plugin mode (`hooks/session-start.sh`) now starts `kb-server` in the background and instructs the agent to run `aix kb stop` when finished.

### Fixed
- **Engine now writes generated code to disk.** `coderNode` persists model output to
  a sandbox `.aix/generated/<sessionId>/` (path-traversal-guarded) instead of discarding
  it. The autonomous loop produces real, reviewable artefacts — it never clobbers `src/`.
- **Budget hard-stop is now wired.** `coderNode` feeds real provider `usd`/`tokens` back
  into the session via `BudgetTracker.addUsage()`. `checkHardStop` now sees actual spend;
  the loop stops when `usdSpent >= usdLimit` (previously `usdSpent` was frozen at 0).
- **Mock mode is now fail-loud.** `aix run --auto` without an API key prints a prominent
  ⚠ MOCK MODE banner before and after the run, and reports budget + written files, so
  placeholder output can never be mistaken for real code.
- **LangGraph node-name collision** — renamed `plan`/`rules`/`tasks` nodes to
  `planStep`/`rulesStep`/`tasksStep` (they collided with state-channel keys, throwing at runtime).
- **CLI UX**: `aix doctor` treats missing optional config as a note (exit 0);
  `aix skills validate` separates WARN vs ERROR and prints a total count;
  `aix context build .` ignores `imports/`; `aix run --dry-run` added.

### Changed
- All 13 `@x/*` packages set to `private: true` until publish metadata
  (`files`, `license`, `repository`, scope) is in place.
- README: corrected `@x/context` description (regex-based, not tree-sitter) and
  documented the engine's sandbox output behaviour.

---

## [0.1.0] — 2026-06-27

### Added

#### Monorepo & Toolchain (Phase 0)
- pnpm workspaces + Turborepo monorepo with 14 packages + `services/kb-server`
- `tsconfig.base.json` with NodeNext module resolution
- Turborepo cache for `build`, `lint`, `clean` tasks

#### Skills Registry (Phase 1)
- 163 SKILL.md in `content/skills/` — domain, process, and reference skills
- `@x/registry` — Zod-validated loader, progressive disclosure 3-tier (L1/L2/L3)
- `catalog.json` (142k) with all skill metadata

#### Providers & Compiler (Phase 2)
- `@x/compiler` — canonical → provider artefacts
- `@x/providers` — adapters for Claude Code, Cursor, Codex, Gemini CLI
- Browser MCP adapter (chrome-devtools + claude-in-chrome)
- `aix install` command with auto-detect and `--provider` override

#### KB Server — Full Port (Phase 3)
- `services/kb-server` — NestJS + Neo4j + **Meilisearch** + **Redis**
- `CacheModule` (ioredis, best-effort, TTL 300s)
- `SearchModule` (Meilisearch index `memory`, best-effort)
- `KbService` — cache-first reads, Meili full-text with Neo4j fallback
- `/health` endpoint reports `{neo4j, redis, meili}` degraded state individually
- `docker-compose.yml` — all 3 services with healthchecks and `depends_on`
- `.env.example` documenting all required env vars
- `ensureSchema()` called at boot — creates Neo4j Memory id-unique constraint
- `enableShutdownHooks()` for graceful teardown

#### Context & Code Analysis (Phase 4)
- `@x/context` — `ContextEngine` with regex-based AST analysis
- `analyzeProject()` — scans TypeScript, JavaScript, Python, Go, Rust, Java, Ruby
- `SimpleEmbedder` — TF-normalized vector embedder
- `SimpleVectorStore` — in-memory cosine similarity query
- `toWiki()` + `toMermaid()` — generate Markdown wiki and Mermaid flow diagrams

#### Autonomous Engine — LangGraph.js (Phase 5)
- `@x/engine` — full `StateGraph` port using `@langchain/langgraph` v1.4.7
- 8-node graph: `plan → rules → tasks → loopStart → pick → ticketPlan → coder → reviewer`
- Conditional routing: interrupt detection, hard-stop budget check, denylist guard, score gate
- `MemorySaver` in-process checkpointing per session
- `EngineGraph.run()` and `EngineGraph.resume()` public API

#### Cross-cutting (9b)
- `@x/policy` — `policy.redact()` with 20+ regex patterns (API keys, tokens, passwords, PII)
- `@x/hitl` — `ClackHitlChannel` + `ConsoleHitlChannel` for human-in-the-loop interrupts
- `@x/prompt` — prompt assembler + linter (success criteria, token budget, output constraints)
- `@x/preview` — HTTP preview server for compiled artefacts + Mermaid renderer
- `@x/evals` — rubric scorer (5-axis) + A/B eval harness

#### Documentation (Phase 6)
- VitePress docs site at `apps/docs/` — guide + reference + env vars
- `CHANGELOG.md` (this file)

### Security
- `KB_MASTER_PASSWORD` required at boot — server refuses to start without it
- API keys bcrypt-hashed before DB storage; raw key shown only at generation
- All memory writes go through `policy.redact()` — no secrets stored raw
- Cypher queries fully parameterized — no string interpolation
- Docker compose exposes `KB_MASTER_PASSWORD` via env ref only (never hardcoded)

---

*Consolidated from 6 legacy repos: `ai-engineering-harness`, `agentic-sdlc`, `skills`, `docs-wiki`, `system-design-skills`, `dev-memory`.*
