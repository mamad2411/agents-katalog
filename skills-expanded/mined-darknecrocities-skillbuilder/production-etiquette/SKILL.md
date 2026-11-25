---
name: production-etiquette
description: >-
  Enforces development etiquette and production standards: automatic .env/.gitignore setup, Docker containerization, deep research before planning, resilient networking (timeouts, cache, debounce, retry), fully functional implementations (zero mock data), testing, and CI/CD.
---

# Production Readiness & Engineering Etiquette

> **Role**: Principal Systems Architect & Production Readiness Engineer  
> **Philosophy**: *Real software, real security, real resilience. No toys, no leaked secrets, no unverified assumptions.*

This skill defines mandatory operational etiquette for software development in Antigravity. It ensures that every project—from small utilities to enterprise platforms—is built with production discipline: zero secret leakage, containerized deployment, evidence-backed planning, resilient network communication, fully functional implementations (no fake static mocks), automated test suites, and CI/CD pipelines.

---

## 1. Quick Navigation & Progressive Disclosure

| Resource Type | Document | Description |
| :--- | :--- | :--- |
| **Reference** | [references/secrets-and-env-hygiene.md](references/secrets-and-env-hygiene.md) | Automatic `.env`, `.env.example`, and `.gitignore` setup whenever APIs are involved. |
| **Reference** | [references/docker-and-containerization.md](references/docker-and-containerization.md) | Multi-stage Docker builds, non-root container security, Compose health checks. |
| **Reference** | [references/deep-research-protocol.md](references/deep-research-protocol.md) | Pre-planning empirical research on codebase, versions, and official docs. |
| **Reference** | [references/network-resilience-and-etiquette.md](references/network-resilience-and-etiquette.md) | Request timeouts, caching with invalidation, debouncing, retries with jitter, circuit breakers. |
| **Reference** | [references/fully-functional-implementations.md](references/fully-functional-implementations.md) | Anti-mock rule: eliminating toy static arrays in favor of real persistence and schemas. |
| **Reference** | [references/continuous-testing-and-ci-cd.md](references/continuous-testing-and-ci-cd.md) | Test automation hierarchy and automated CI/CD pipeline specifications. |
| **Reference** | [references/branching-pr-and-commit-strategy.md](references/branching-pr-and-commit-strategy.md) | Purposeful branches (`feat/`, `fix/`), 1k-line push budget, ready-to-review PR preparation. |
| **Template** | [templates/docker/Dockerfile.node](templates/docker/Dockerfile.node) | Production-grade multi-stage Node/TypeScript container (non-root, health check). |
| **Template** | [templates/docker/Dockerfile.python](templates/docker/Dockerfile.python) | Production-grade multi-stage Python container (non-root, venv caching). |
| **Template** | [templates/docker/Dockerfile.go](templates/docker/Dockerfile.go) | Production-grade static distroless Go container. |
| **Template** | [templates/docker/docker-compose.yml](templates/docker/docker-compose.yml) | Docker Compose orchestrating application, PostgreSQL, and health checks. |
| **Template** | [templates/ci-cd/github-ci.yml](templates/ci-cd/github-ci.yml) | GitHub Actions CI workflow (lint, typecheck, test, security audit, docker build). |
| **Template** | [templates/pull-request.md](templates/pull-request.md) | Standard ready-to-review Pull Request template (title, architecture, tests, rollback). |
| **Template** | [templates/resilience/resilient_http_client.ts](templates/resilience/resilient_http_client.ts) | Resilient TypeScript HTTP client with timeouts, caching, and jittered retries. |
| **Template** | [templates/resilience/resilient_http_client.py](templates/resilience/resilient_http_client.py) | Resilient Python HTTP client with timeouts, caching, and exponential backoff. |
| **Utility** | [scripts/scaffold_project_hygiene.py](scripts/scaffold_project_hygiene.py) | CLI utility to audit and auto-scaffold missing hygiene files in any project. |
| **Utility** | [scripts/analyze_git_commit_chunks.py](scripts/analyze_git_commit_chunks.py) | CLI utility to enforce 1k-line push budget, cluster commits, and generate PRs. |

---

## 2. The 6 Non-Negotiable Pillars of Etiquette

### Pillar 1: Automatic Environment & Secrets Hygiene
Whenever an API, third-party integration, database, or token is added:
- **Never commit raw credentials**: Strictly forbid committing secrets into Git.
- **Auto-create `.gitignore`**: Ensure `.env`, `.env.local`, `*.key`, `*.pem`, `node_modules`, `venv`, and OS clutter (`.DS_Store`) are ignored.
- **Auto-create `.env.example`**: Maintain an accurate template documenting every required configuration variable, its format, and safe placeholder values.
- **Fail fast at boot**: Validate all required environment variables upon process startup using schema validation (e.g., Zod, Pydantic, or explicit assertions).

### Pillar 2: Standardized Containerization (Docker by Default)
Every web service, API, background worker, or full-stack application must provide:
- **Multi-Stage `Dockerfile`**: Isolate the build environment (compilers, build tools) from the slim runtime image (e.g., `alpine`, `distroless`, `slim`).
- **Non-Root Security**: Explicitly configure `USER appuser` (UID 10001) rather than running as root inside containers.
- **`.dockerignore`**: Prevent local `.git`, `.env`, build artifacts, and dependencies from leaking into the container build context.
- **`docker-compose.yml`**: Provide a reproducible local development environment pairing the service with real dependencies (database, Redis) and explicit `healthcheck` conditions.

### Pillar 3: Deep Research Protocol Before Planning
Before proposing architecture or writing code:
- **Inspect the real codebase**: Never assume package versions or directory layouts. Check `package.json`, `requirements.txt`, `go.mod`, or lockfiles.
- **Consult official documentation**: Never hallucinate framework flags, configuration properties, or SDK method names.
- **Clarify ambiguities**: Identify the exact minimal surface area before formulating an implementation plan.

### Pillar 4: Network & Request Resilience
Every outgoing network request, API client, and authentication workflow must implement:
- **Mandatory Timeouts**: Configure explicit connection timeouts (default: 3s) and read/execution timeouts (default: 10s–30s). Never make unbounded network calls.
- **Caching & Invalidation**: Cache expensive or repeated read requests (in-memory LRU or Redis) with explicit TTLs and cache-busting on mutations.
- **Debouncing & Throttling**: Debounce user input handlers (search bars, live filters) and rate-limit outgoing client requests.
- **Bounded Exponential Backoff with Jitter**: Retry only transient, idempotent errors (HTTP 429, 502, 503, 504) with random jitter to avoid thundering herds.
- **Circuit Breakers**: Trip the circuit when downstream services fail persistently, failing fast gracefully.

### Pillar 5: The "Anti-Mock" / Fully Functional Mandate
- **No Toy Demos**: Never implement features using static hardcoded in-memory arrays pretending to be a database (e.g., `const users = [{ id: 1, name: 'Demo' }]`).
- **Real Persistence**: Always wire up real persistence—even in small projects (use SQLite, PostgreSQL, or real structured JSON file stores).
- **End-to-End Wiring**: Form inputs must validate real schemas, call real APIs, execute real database queries, and handle real failure states.

### Pillar 6: Continuous Testing & Automated CI/CD
- **Testing Every Time**: Every feature and bugfix must be accompanied by independent automated tests (unit + integration).
- **Automated CI/CD**: Every project repository must include an automated CI/CD pipeline (e.g., `.github/workflows/ci.yml`) that executes:
  1. Linter and formatting validation.
  2. Static type checking.
  3. Automated test suite execution.
  4. Dependency security audit (`npm audit`, `pip-audit`, `govulncheck`).
  5. Docker build verification.

### Pillar 7: Git Branching, Meaningful Commits (Title + Description), Push to Branch & Ready-to-Review PRs
- **Explicit Branch Prefixes**: Every branch must follow purpose-driven conventions: `feat/`, `fix/`, `refactor/`, `perf/`, `docs/`, `test/`, `chore/` (or `feat/project-bootstrap` for initial setup).
- **The 1,000-Line Push Budget**: Never push a single commit or unreviewed diff exceeding 1,000 lines of code. Analyze changed files and decompose into cohesive atomic commits (Schema -> Service -> API -> Tests).
- **Meaningful Commits with Title + Description**: Every commit must feature a Conventional Title AND a structured Description body explaining Why, What, and Verification. Zero lazy commits.
- **Always Push to the Remote Branch**: Publish commits immediately to `origin <branch-name>`; never leave unpushed local commits.
- **Green State Rule**: Every commit must compile, pass static types, and pass tests independently.
- **Always Open or Update a PR**: Always author or update an active, ready-to-merge GitHub Pull Request with structured titles, technical summaries, verification logs, and rollback procedures.

### Pillar 8: The Multi-Tiered Code Quality Standard (The Double Mandate)
- **Human Maintainability (Empirical Defect Density)**: Files over 500 lines experience non-linear climbs in defect density and hidden coupling. Adhere to the 4-Tier Maintainability Matrix: Sweet Spot (150–250 lines), Nominal (251–350 lines), Warning Zone (351–499 lines), and Hard Ceiling (500 lines).
- **AI Context Fidelity**: Modular files preserve attention focus, eliminate "Lost-in-the-Middle" context rot, and ensure precise, reliable tool-call diff replacements during pair-programming turns.
- **Cognitive Hygiene**: Maintain functions $\le 40$ physical lines, nesting depth $\le 3$ levels with early return guard clauses, and Cyclomatic Complexity $\le 10$. Zero arbitrary file-shredding.

---

## 3. Automation Tools

### Tool 1: Project Hygiene Scaffolding
Verify or scaffold missing `.gitignore`, `.env.example`, `Dockerfile`, and CI/CD files:
```bash
# Audit project hygiene
python3 skills/production-etiquette/scripts/scaffold_project_hygiene.py --path <project-directory> --check

# Auto-scaffold missing files
python3 skills/production-etiquette/scripts/scaffold_project_hygiene.py --path <project-directory> --apply
```

### Tool 2: Git Commit Chunk & PR Analyzer
Analyze working tree diffs, enforce the 1,000-line review budget, cluster atomic commits, and generate PR descriptions:
```bash
python3 skills/production-etiquette/scripts/analyze_git_commit_chunks.py --path <project-directory>
```

---

## 4. Mandatory Enforcement via `AGENTS.md`

To enforce this etiquette across all agent sessions, add this rule to your project's root `AGENTS.md` (or globally in your workspace configuration):

```markdown
# Mandatory Development Etiquette

All development in this repository MUST comply with the `production-etiquette` skill:
1. When APIs or external services are touched, automatically ensure `.env.example`, `.env`, and `.gitignore` are configured.
2. Supply a production-ready, multi-stage, non-root Dockerfile and docker-compose.yml.
3. Conduct deep codebase research before authoring plans.
4. Implement network resilience: explicit timeouts, caching, debouncing, and jittered retries.
5. Strictly avoid static mock arrays or toy demo code; all features must be fully functional and persistent.
6. Provide automated tests and maintain the project's CI/CD workflow (.github/workflows/ci.yml).
7. Branch deliberately (feat/, fix/), limit push diffs to < 1,000 lines, author meaningful commits with Title + Description, always push to remote branch, and maintain ready-to-merge Pull Requests.
```
