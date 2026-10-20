# Senior Backend Developer Agent

Implements Jira tickets end-to-end on the CHH (Community Health Hub) ASP.NET Core 8 Web API backend, in this monorepo's `backend/` folder. Given a ticket ID, it reads the Jira story, gathers context from Confluence and the codebase, produces an implementation plan for developer and tech lead approval, implements the approved plan on a feature branch, reviews the code for quality and standards compliance, writes and verifies tests, then raises a pull request on GitHub.

All configuration below is injected into every sub-agent. For the full task workflow, approval gates, and agent handoffs, read `.claude/agents/orchestrator.md`. For the frontend counterpart, see `frontend/CLAUDE.md`.

---

## Commands

### Paste a Jira URL (primary trigger)
Paste any Jira ticket URL (subtask or story) directly into the conversation to start the pipeline. No command needed.

Example: `https://experionglobal.atlassian.net/browse/CHH-8`

**What happens:**
1. Startup gate — verifies manifest, stack, module folders, and Jira access. Runs once; skipped on future sessions if memory is green.
2. Knowledge Agent reads the Jira ticket (subtask → story → epic) and gathers Confluence and codebase context.
3. Planning Agent produces an implementation plan, checks design readiness (see root `CLAUDE.md` Orchestrator Rule 11), and walks through two approval gates (developer → tech lead).
4. Coding Agent implements the approved plan on a feature branch.
5. Code Review Agent reviews for quality, security, and standards compliance.
6. Unittest Agent writes tests, verifies coverage thresholds, and hands off to the PR Agent.

QA test-case execution happens separately, after this pipeline's PR is merged — it is run by a QA automation tester, not part of this flow. See root `CLAUDE.md` §"QA execution (post-merge)" and `.claude/agents/qa-execution-agent.md`.

**Delegates to:** `.claude/agents/orchestrator.md`

---

### `/task <TICKET_ID>`
Alternative to pasting a URL — start the pipeline with just the ticket ID.

**Delegates to:** `.claude/agents/orchestrator.md`

---

### `/dev <TICKET_ID> <BASE_BRANCH>`
Start the pipeline for a **bugfix targeting a specific release branch** (e.g. `/dev CHH-8 release/0.17.2`).

Identical to `/task` except:
- The base branch for checkout and the PR target is `<BASE_BRANCH>` instead of `gitBaseBranch` in `project_config.md`
- The branch prefix is `bugfix/` instead of the configured `featureBranchPrefix` (e.g. `bugfix/CHH-8-fix-otp-timer`)
- Commit message type is `fix(...)` instead of `feat(...)`

These overrides are **session-scoped** — they are never written to `project_config.md`.

**Delegates to:** `.claude/agents/orchestrator.md`

---

### `/startup`
Re-run the full environment setup.

Use when: first-time project setup, Jira credentials changed, or startup memory is stale.

**Delegates to:** `.claude/agents/startup-agent.md`

---

### `/task-resume <TICKET_ID>`
Resume a pipeline interrupted mid-flight.

Reads `project_config.md` memory and conversation context to determine the last completed agent, then continues from there.

**Delegates to:** `.claude/agents/orchestrator.md`

---

## Setup (First Time)

Ensure the **Atlassian MCP connector** is connected in **Claude Code → Settings → Connectors** before starting.

Then paste a Jira URL or run `/task <TICKET_ID>`. Startup runs automatically on first use and collects:
- A sample Confluence URL (space key is extracted automatically)
- Feature branch prefix (e.g. `feature/`)
- Git base branch (e.g. `main`)
- Developer name (from Atlassian authentication)

---

## MCP Connectors Required

| Connector | Required | Used For |
|---|---|---|
| Atlassian | ✅ Yes | Jira ticket fetch (subtask → story → epic), Confluence implementation plan publishing |

Connect in **Claude Code → Settings → Connectors** before running `/task`.

---

## Project Identity

> The Confluence Space Key is extracted automatically during startup — no manual configuration needed.

| Field | Value |
|---|---|
| Product | Community Health Hub (CHH) — see root `CLAUDE.md` and PRD-CHH-v2.2 |
| Stack Type | backend |
| Primary Language | C# |
| Repo shape | Single monorepo — this is `backend/` inside it, not a standalone repo |
| Confluence Space Key | auto-derived at startup from a sample Confluence URL |

---

## Tech Stack

| Concern | Technology |
|---|---|
| Framework | ASP.NET Core 8 Web API |
| Language Version | C# 12 / .NET 8 |
| Type Checking | Nullable reference types enabled |
| ORM / Data Access | Entity Framework Core 8 (async) |
| Database | PostgreSQL 16 |
| Geo / radius queries | PostgreSQL `earthdistance`/`cube` extension (or PostGIS if richer geo queries are needed) — backs proximity search (5–100 km radius) for CHH-F04 |
| Migrations | EF Core code-first migrations |
| Background jobs | Hangfire — proximity notification fan-out (PRD NFR: dispatch < 5s), scheduled cleanup |
| Caching | `IMemoryCache` |
| Validation | FluentValidation 11 |
| Config / Env | `appsettings.json` + `IOptions<T>` + env vars |
| Auth | JWT Bearer, OTP-first (mobile number + 6-digit OTP) — no enterprise SSO; see CHH-F01 |
| HTTP Client | `IHttpClientFactory` typed clients (SMS gateway, push notification, maps) |
| SMS Gateway | **Fast2SMS** (decided 2026-09-07, superseding the earlier Twilio/Firebase open question) — `IWhatsAppTemplateClient` over Fast2SMS's WhatsApp Message API is the live channel (`Fast2Sms:Channel = "whatsapp"`); the plain SMS channel is implemented but blocked pending TRAI DLT registration. `ISmsGatewayClient` stays the swappable abstraction — `AddFast2Sms` in `ServiceCollectionExtensions` picks the channel from config, falling back to a logging-only client in dev when no API key is set. |
| Push Notifications | Firebase Cloud Messaging (per PRD §11) |
| Maps / Geo API | Google Maps or Mapbox (per PRD §11) — venue GPS pins, radius filtering |
| Testing | xUnit + Moq + FluentAssertions + WebApplicationFactory |
| Logging | Serilog, structured, OTel exporter |
| Build Tool | dotnet CLI |
| Container | Docker + docker-compose |

---

## Layer Architecture

| Layer | Name | Purpose |
|---|---|---|
| Entry | Controller | HTTP, FluentValidation, delegates to Service |
| Logic | Service | OTP issuance/verification, role redirection, proximity matching, notification dispatch, domain rules |
| Data | Repository | EF Core; returns null for not-found, never throws HTTP |
| Cross-cutting | Middleware | Exception handling, auth, correlation |

**Layer isolation rule (critical):** Controllers must never access `DbContext`, repository types, or EF Core namespaces directly — all data access goes through the Service → Repository chain.

External integrations (SMS gateway, FCM, maps) are typed HTTP clients registered under Infrastructure — not a separate architectural layer.

---

## Agent Structure

This agent framework lives at the root of the CHH monorepo, alongside `backend/` and `frontend/`. There are **no sibling cloned repos** — everything is one git history.

```
<repo root>/
├── CLAUDE.md                              ← Shared standards, Idea, Modules, Decisions Log
├── .claude/
│   ├── agents/
│   │   ├── orchestrator.md                ← shared — routes to backend-* or frontend-* by Side
│   │   ├── startup-agent.md               ← shared
│   │   ├── pr-agent.md                    ← shared
│   │   ├── backend-knowledge-agent.md
│   │   ├── backend-codebase-analysis-agent.md
│   │   ├── backend-planning-agent.md
│   │   ├── backend-coding-agent.md
│   │   ├── backend-code-review-agent.md
│   │   ├── backend-unittest-agent.md
│   │   ├── frontend-knowledge-agent.md
│   │   ├── frontend-planning-agent.md
│   │   ├── frontend-coding-agent.md
│   │   ├── frontend-code-review-agent.md
│   │   └── frontend-unittest-agent.md
│   ├── skills/
│   │   ├── confluence-publish-skill/SKILL.md
│   │   ├── notify-skill/SKILL.md
│   │   ├── git-branch-skill/SKILL.md
│   │   ├── github-pr-skill/SKILL.md
│   │   └── ef-migration-skill/SKILL.md    ← backend only
│   ├── rules/                             ← Project-specific standards (CHH)
│   │   ├── api-standards.md
│   │   └── db-standards.md
│   ├── standards/                         ← General .NET + test standards
│   │   ├── DOTNET-RULES.md
│   │   └── UNITTEST-BACKEND-STANDARDS.md
│   ├── memory/                            ← Runtime state (written at startup)
│   ├── repository-index.md                ← Module index (backend/frontend), auto-written at startup
│   └── settings.json
├── backend/                                ← this side
│   ├── CLAUDE.md                          ← this file
│   └── src/, tests/                       ← see Application Code Structure below
└── frontend/                               ← other side — see frontend/CLAUDE.md
```

---

## Application Code Structure

Clean Architecture, single service (no per-microservice repeat — this is one backend, not a fleet):

```
backend/
├── src/
│   ├── Chh.Api/
│   │   ├── Controllers/          ← Entry Layer — API controllers
│   │   └── Extensions/           ← Service registration helpers
│   ├── Chh.Application/
│   │   ├── Commands/             ← MediatR command handlers (if MediatR is adopted)
│   │   ├── Queries/               ← MediatR query handlers
│   │   ├── Services/              ← Orchestration / business logic
│   │   ├── Contracts/             ← Service and repository interfaces
│   │   ├── Dtos/                  ← Request / Response types
│   │   ├── Validators/            ← FluentValidation validators
│   │   └── Abstractions/          ← Shared abstractions
│   ├── Chh.Domain/
│   │   ├── Entities/              ← EF Core domain entities
│   │   └── Enums/
│   └── Chh.Infrastructure/
│       ├── Persistence/           ← DbContext + EF entity configurations
│       ├── Migrations/            ← EF Core migration files
│       ├── Services/              ← Infrastructure service implementations (Hangfire jobs, etc.)
│       └── ExternalClients/       ← SMS gateway, FCM, maps — typed HTTP clients
└── tests/
    ├── Chh.Api.Tests/
    │   └── Controllers/
    └── Chh.Application.Tests/
        ├── Commands/
        ├── Queries/
        ├── Services/
        ├── Validators/
        └── TestData/
```

---

## Standards Documents

All agents must read and strictly enforce all standards before planning or implementing:

| Standard | File | Scope |
|---|---|---|
| DOTNET-RULES | `.claude/standards/DOTNET-RULES.md` | General .NET coding standards: async/await, nullable types, EF Core, DI, testing. **Note:** its Part 2 SQL examples are SQL-Server-flavored — this project uses PostgreSQL; `.claude/rules/db-standards.md` gives the PostgreSQL type mapping that supersedes those examples where they conflict. |
| API Standards | `.claude/rules/api-standards.md` | CHH REST API rules: URL conventions, DTOs, auth, pagination, RFC 7807 error format, Swagger |
| Database Standards | `.claude/rules/db-standards.md` | CHH DB rules: naming, PostgreSQL data types, PII encryption for health-screening data |
| Test Standards | `.claude/standards/UNITTEST-BACKEND-STANDARDS.md` | xUnit + Moq + FluentAssertions patterns, naming, coverage thresholds |

---

## Test Configuration

| Config | Value |
|---|---|
| Test Command | `dotnet test` |
| Coverage Command | `dotnet test --collect:"XPlat Code Coverage"` |
| Coverage Threshold | See per-layer thresholds in `.claude/standards/UNITTEST-BACKEND-STANDARDS.md` |
| Test Database | EF Core in-memory database (unit) / Testcontainers for PostgreSQL (integration) |
| Mock Library | Moq 4.x |

---

## Deployment

| Concern | Value |
|---|---|
| Host | **AWS** — App Runner or Elastic Beanstalk (single service, no ECS/Fargate needed at this scale) |
| Database | AWS RDS for PostgreSQL 16 |
| Secrets | Azure Key Vault reference in `.claude/rules/api-standards.md` §5 predates this AWS decision — use **AWS Secrets Manager** instead for the SMS gateway key, FCM server key, maps API key, and JWT signing key; update that rule file if/when this is finalized |
| CORS | Must explicitly allow the frontend's Vercel origin(s) (production + preview-deploy URLs) — see root `CLAUDE.md` Decisions Log 2026-09-05 |
| URL | AWS-generated (e.g. `https://chh-api.<region>.awsapprunner.com`) until a custom domain is attached |

---

## Memory

| File | Written By | Read By |
|---|---|---|
| `.claude/memory/project_startup_status.md` | Startup Agent | Orchestrator (startup gate on every session) |
| `.claude/memory/project_config.md` | Startup Agent | All agents (branch prefix, base branch, developer name) |
| `.claude/repository-index.md` | Startup Agent | Knowledge Agent, Coding Agent, Code Review Agent (module map, not a multi-repo index — see startup-agent.md Step 5) |

---

## Output

All pipeline outputs live in the conversation context and Confluence. Nothing is written to disk except memory files and the module index.

| Artifact | Where |
|---|---|
| Implementation plan | Confluence — child page under the Epic's LLD page |
| Feature branch | This repo — `<prefix><ticket-id>-<short-description>` |
| Pull request | GitHub — opened by PR Agent after tests pass |
| Test report (pass/fail counts, coverage per layer) | Conversation only — not written to disk |

---

## Agent Directory

| Agent | File | Role |
|---|---|---|
| Orchestrator | `.claude/agents/orchestrator.md` | Drives the full task workflow; routes to backend-* or frontend-* agents by `Side` |
| Startup Agent | `.claude/agents/startup-agent.md` | Verify stack, module folders, and Jira access once per project; persist result to memory (shared, side-agnostic) |
| Knowledge Agent | `.claude/agents/backend-knowledge-agent.md` | Fetch Jira ticket (subtask → story → epic); gather Confluence context; delegate codebase analysis |
| Codebase Analysis Agent | `.claude/agents/backend-codebase-analysis-agent.md` | Explore existing backend patterns in `backend/` |
| Planning Agent | `.claude/agents/backend-planning-agent.md` | Produce an approved implementation plan before any coding begins; checks design readiness |
| Coding Agent | `.claude/agents/backend-coding-agent.md` | Implement the approved plan in `backend/` |
| Code Review Agent | `.claude/agents/backend-code-review-agent.md` | Review quality, security, type correctness, plan compliance |
| Unittest Agent | `.claude/agents/backend-unittest-agent.md` | Write and verify tests; hand off to PR Agent when suite is green |
| PR Agent | `.claude/agents/pr-agent.md` | Draft and raise the pull request after tests pass (shared, side-agnostic) |

Frontend counterparts (`frontend-knowledge-agent.md`, etc.) are listed in `frontend/CLAUDE.md`.

---

## Skill Directory

| Skill | File | Role |
|---|---|---|
| Confluence Publish Skill | `.claude/skills/confluence-publish-skill/SKILL.md` | Publish the implementation plan as a child of the Epic's LLD page |
| Notify Skill | `.claude/skills/notify-skill/SKILL.md` | Send cross-platform desktop toast and phone push after every agent transition |
| Git Branch Skill | `.claude/skills/git-branch-skill/SKILL.md` | Create or check out the feature branch before coding begins (single repo — no multi-repo loop) |
| GitHub PR Skill | `.claude/skills/github-pr-skill/SKILL.md` | Push the branch and open a pull request on GitHub after tests pass |
| EF Migration Skill | `.claude/skills/ef-migration-skill/SKILL.md` | Invoke when a database schema change requires creating, reviewing, applying, or rolling back migrations. Backend only. |

> **Note:** `jira-comment-skill/` and `jira-status-skill/` exist in `.claude/skills/` but are **disabled** for this project. Orchestrator Rule 10 explicitly prohibits all Jira status transitions and comment operations. Do not invoke these skills at any point in the pipeline.

---

## Orchestrator

For the full task workflow, approval gates, agent handoffs, and orchestration rules, read `.claude/agents/orchestrator.md`.
