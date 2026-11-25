---
name: multi-agent-git-workflow
description: Multi-agent Git workflow for parallel AI development — repo scanning, micro-task breakdown, dynamic agent spawning (backend-1, backend-2, frontend-1, etc.), continuous test/eval loop, AI-as-judge validation, automated PRs, quality gates. Stops ONLY when feature is complete: all tests pass, evals green, lint/format/type-check clean.
origin: AI Dev Kit
---

# Multi-Agent Git Workflow

Coordinated parallel development with **dynamic micro-task breakdown** and **on-demand agent spawning**. The workflow reads the repo, decomposes the feature into atomic micro-tasks, spawns as many coding agents as needed (backend-1, backend-2, frontend-1, data-1, etc.), coordinates their work, and runs a continuous validation loop. **This workflow stops only when the feature is fully done.**

## When to Use

- A feature requires work across multiple surfaces, files, or domains
- You want **dynamic task decomposition** instead of pre-assigned waves
- You need **multiple coding agents working in parallel** on independent micro-tasks
- You want **continuous test/eval/quality loops** that run until everything is green
- Feature specs live in `docs/features/` (no Git issues required)
- Quality gates: tests pass, evals green, lint/format/type-check clean — then stop

## Core Concepts

### Full Workflow Diagram

```
[Input Source]
  Git Issue #N
  OR
  docs/features/<name>/*.md
            ↓
  [Repo Scanner] → Read entire repo, map surfaces, identify all affected areas
            ↓
  [Web Research Pipeline] → Search docs, blogs, RFCs, GitHub issues, Stack Overflow, Reddit
    ├─ [Web Researcher Agent]       → Search official docs, API refs, release notes
    ├─ [Community Researcher]       → Search Stack Overflow, GitHub issues, Reddit, blogs
    ├─ [Reddit Researcher Agent]    → Deep Reddit analysis: user experiences, war stories, sentiment, consensus
    ├─ [Competitive Analyst]        → Compare alternatives, benchmarks, trade-offs
    └─ [Security Scanner]           → Search CVE databases, advisories, dependency audits
            ↓
  [Micro-Task Decomposer] → Break feature into atomic micro-tasks
    Each micro-task:
      - Single responsibility (one file or one function)
      - Independent or has explicit dependency on another micro-task
      - Has acceptance criteria
      - Has estimated complexity (trivial/small/medium/large)
            ↓
  [Task Queue] → Prioritized list of all micro-tasks with dependencies
    micro-task-001: Create src/cache/schema.py — DEPS: none — TRIVIAL
    micro-task-002: Write tests for schema.py — DEPS: 001 — TRIVIAL
    micro-task-003: Implement Redis cache store — DEPS: 001 — SMALL
    micro-task-004: Implement FAISS similarity lookup — DEPS: 001 — MEDIUM
    micro-task-005: Write tests for cache store — DEPS: 003 — SMALL
    micro-task-006: Write tests for FAISS lookup — DEPS: 004 — SMALL
    micro-task-007: Integrate cache into /v1/chat endpoint — DEPS: 003,004 — MEDIUM
    micro-task-008: Add cache hit indicator to UI — DEPS: 007 — SMALL
    micro-task-009: Add E2E test for cache flow — DEPS: 007,008 — MEDIUM
    micro-task-010: Add cache metrics to observability — DEPS: 007 — SMALL
            ↓
  [Agent Spawner] → Spawn coding agents based on micro-task count and type
    backend-1, backend-2, backend-3  (Python/FastAPI work)
    frontend-1                       (React/UI work)
    data-1                           (Schema/migration work)
    test-1, test-2                   (Test writing work)
    Each agent gets 1-N micro-tasks based on dependency graph
            ↓
  [Parallel Execution] → Agents work on their micro-tasks simultaneously
    Each agent:
      1. Reads its assigned micro-task(s)
      2. Creates/modifies files per task spec
      3. Writes tests for the changes
      4. Runs lint, format, type-check locally
      5. Marks micro-task as DONE or BLOCKED
            ↓
  [Dependency Resolver] → When a micro-task completes, unlock dependents
    micro-task-001 DONE → unlock 002, 003, 004
    micro-task-003 DONE → unlock 005, 007 (if 004 also done)
    micro-task-004 DONE → unlock 006, 007 (if 003 also done)
    Newly unlocked tasks → assign to available agents
            ↓
  [Continuous Validation Loop] → NEVER STOPS until ALL gates pass
    ┌─────────────────────────────────────────────────┐
    │  1. [TDD Guide]     → Ensure every change has  ││
    │                          tests, RED→GREEN cycle ││
    │         ↓                                       │
    │  2. [Lint Check]    → ruff, black, eslint      │
    │         ↓                                       │
    │  3. [Format Check]  → Code formatted correctly  │
    │         ↓                                       │
    │  4. [Type Check]    → mypy, tsc --noEmit        │
    │         ↓                                       │
    │  5. [Test Suite]    → All unit + integration    │
    │                          tests pass             │
    │         ↓                                       │
    │  6. [E2E Tests]     → Playwright flows pass     │
    │         ↓                                       │
    │  7. [Eval Harness]  → Pass@k >= target          │
    │         ↓                                       │
    │  8. [Code Review]   → Quality review complete   │
    │         ↓                                       │
    │  9. [Security Scan] → No vulnerabilities        │
    │         ↓                                       │
    │  ┌───────────────────────────────────────┐      │
    │  │  ALL PASS? ──YES──→ Exit loop, merge  │      │
    │  │       │                               │      │
    │  │       NO                              │      │
    │  │       ↓                               │      │
    │  │  Identify failures                    │      │
    │  │  Route to responsible agent           │      │
    │  │  Agent applies fix                    │      │
    │  │  Return to step 1                     │      │
    │  └───────────────────────────────────────┘      │
    └─────────────────────────────────────────────────┘
            ↓
  [Git Agent] → Create branch, commit, PR, merge when loop exits
```

---

## Input Sources

### Option A: Git Issues

Read GitHub issue, extract requirements, acceptance criteria, affected surfaces.

### Option B: Feature Specs (`docs/features/<name>/*.md`)

When Git issues are not available, use feature specs:

```
docs/features/<feature-name>/
├── spec.md              # Feature description, requirements, acceptance criteria
├── requirements.md      # Detailed requirements with user stories (optional)
└── constraints.md       # Technical constraints (optional)
```

The coordinator reads from whichever source is available.

---

## Step 1: Repo Scanner

Read the **entire repository** to build a complete surface map:

```python
repo_scan_result = {
    "directories": {
        "agents/": ["planner.md", "architect.md", "code-reviewer.md", ...],
        "skills/": ["tdd-workflow/", "code-review/", "security-review/", ...],
        "commands/": ["build-fix.md", "code-review.md", ...],
        "src/": ["api/", "models/", "services/", "cache/", ...],
        "tests/": ["unit/", "integration/", "e2e/"],
        # ... all directories and files
    },
    "dependencies": {
        "python": ["fastapi==0.109.0", "pydantic==2.5.0", "sqlalchemy==2.0.25", ...],
        "node": ["react@18.2.0", "typescript@5.3.0", "zod@3.22.0", ...],
    },
    "existing_surfaces": {
        "api_endpoints": ["/v1/chat", "/v1/users", "/v1/markets", ...],
        "models": ["User", "Market", "Chat", ...],
        "components": ["ChatMessage", "UserCard", "MarketList", ...],
        "tests": {"unit_count": 142, "integration_count": 23, "e2e_count": 8},
        "coverage": {"line": 0.78, "branch": 0.65},
    },
    "affected_by_feature": [
        "src/api/v1/chat.py",          # needs cache middleware
        "src/cache/",                  # new directory
        "tests/unit/test_semantic_cache.py",  # new test
        "tests/integration/test_cache_endpoint.py",  # new test
    ],
}
```

---

## Step 1b: Web Research Pipeline

After the repo scan, the **web research pipeline** runs in parallel to gather external knowledge. This runs BEFORE micro-task decomposition so that findings inform the task breakdown.

### Parallel Research Agents

```
[Web Research Pipeline] — 5 agents running in parallel:

  1. [Web Researcher Agent]
     Sources: Official docs, API references, release notes, changelogs
     Tools: web_search, web_fetch
     Outputs: .workflow/<feature-name>/research/web-research.md

  2. [Community Researcher Agent]
     Sources: Stack Overflow, GitHub issues, dev blogs, Hacker News
     Tools: web_search, web_fetch
     Outputs: .workflow/<feature-name>/research/community-research.md

  3. [Reddit Researcher Agent]
     Sources: Reddit (r/programming, r/Python, r/typescript, r/webdev, framework-specific subs)
     Tools: web_search, web_fetch
     Outputs: .workflow/<feature-name>/research/reddit-research.md
     Focus: Real user experiences, production war stories, sentiment, consensus

  4. [Competitive Analyst Agent]
     Sources: Alternative implementations, benchmarks, trade-off analyses
     Tools: web_search, web_fetch
     Outputs: .workflow/<feature-name>/research/competitive-analysis.md

  5. [Security Scanner Agent]
     Sources: CVE databases, npm audit, pip-audit, GitHub advisories
     Tools: web_search, Bash (npm audit, pip-audit, trivy)
     Outputs: .workflow/<feature-name>/research/security-audit.md
```

### Web Research Agent

The **Web Researcher Agent** searches for official documentation, API references, and release notes:

```yaml
web_researcher_config:
  search_queries:
    - "<framework> <version> <feature> official documentation"
    - "<library> <feature> API reference"
    - "<framework> <version> changelog release notes"
    - "<problem> best practice <year>"
  sources_trusted:
    - Official documentation sites (docs.djangoproject.com, fastapi.tiangolo.com, react.dev)
    - GitHub repositories (official org repos)
    - RFCs and standards documents
    - Official blogs and release announcements
  sources_distrusted:
    - Random blogs without authorship
    - AI-generated content without citations
    - Outdated content (>2 versions old)
  output_format:
    - Finding: What was found
    - Source: URL
    - Confidence: high/medium/low
    - Relevance: How it applies to our feature
    - Code Example: If applicable
```

### Community Researcher Agent

The **Community Researcher Agent** searches for real-world experience outside Reddit (which has its own dedicated agent):

```yaml
community_researcher_config:
  search_queries:
    - "<framework> <feature> Stack Overflow"
    - "github.com <org>/<repo> issues <feature> bug"
    - "<problem> gotcha pitfall workaround"
    - "<library> production experience lessons learned"
  focus_areas:
    - Common bugs and their fixes
    - Performance gotchas
    - Migration experiences
    - Production war stories
    - Alternative approaches the team didn't consider
  exclude_sources:
    - reddit.com  # handled by dedicated Reddit Researcher Agent
  output_format:
    - Problem: What issue people encountered
    - Solution: How they fixed it
    - Source: URL (Stack Overflow, GitHub issue, blog)
    - Consensus: Do multiple sources agree?
```

### Reddit Researcher Agent

The **Reddit Researcher Agent** does deep analysis of Reddit threads for ground-level practitioner knowledge:

```yaml
reddit_researcher_config:
  search_queries:
    - "site:reddit.com <framework> <feature> experience production"
    - "site:reddit.com <library> real world review"
    - "site:reddit.com <tool-a> vs <tool-b> comparison"
    - "site:reddit.com <framework> gotcha pitfall regret"
    - "site:reddit.com <technology> worth it <year>"
  target_subreddits:
    - r/programming
    - r/Python
    - r/typescript
    - r/webdev
    - r/devops
    - r/machinelearning
    - Framework-specific subs (r/FastAPI, r/reactjs, r/node, r/PostgreSQL)
  analysis_dimensions:
    - Sentiment: positive / neutral / negative
    - Consensus: strong agreement / mixed / strong disagreement
    - Production evidence: yes/no (did commenter deploy this at scale?)
    - Recency: within 12 months / older (flag if outdated)
    - Severity: data loss / security / performance / inconvenience
  output_format:
    - Summary: 2-3 sentence overview of community sentiment
    - Key findings with direct quotes from top comments
    - Gotchas table with severity ratings
    - Community consensus table (Do it / Don't / Depends)
    - Notable dissenting opinions
    - Production war stories
```

### Competitive Analyst Agent

The **Competitive Analyst Agent** compares alternative approaches:

```yaml
competitive_analyst_config:
  search_queries:
    - "<problem> approach A vs approach B"
    - "<library> vs <alternative> comparison benchmark"
    - "<feature> performance comparison"
  analysis_dimensions:
    - Performance (benchmarks, latency, throughput)
    - Developer experience (API ergonomics, learning curve)
    - Maturity (release history, adoption, community)
    - Maintenance (active development, issue resolution time)
    - Licensing (MIT, Apache, GPL, commercial)
  output_format:
    - Comparison table with scored dimensions
    - Recommendation with rationale
    - Trade-offs clearly stated
```

### Security Scanner Agent

The **Security Scanner Agent** checks for vulnerabilities in any new dependencies:

```yaml
security_scanner_config:
  methods:
    - web_search: "<package> CVE vulnerability <year>"
    - Bash: "npm audit" (Node.js projects)
    - Bash: "pip-audit" (Python projects)
    - Bash: "trivy fs ." (filesystem scan)
    - web_fetch: GitHub Security Advisories for the package
  check_scope:
    - Direct dependencies
    - Transitive dependencies (2 levels deep)
    - Known CVEs in the past 12 months
    - Unmaintained packages (no release in 12+ months)
  output_format:
    - Package: name + version
    - Vulnerability: CVE ID, severity, description
    - Fix: Upgrade path or workaround
    - Risk: high/medium/low
```

### Research Synthesis

After all 4 agents complete, their findings are synthesized:

```markdown
# Research Synthesis: <feature-name>

## Official Documentation (Web Researcher)
- <key findings with URLs>

## Community Knowledge (Community Researcher)
- <common pitfalls, workarounds, edge cases from Stack Overflow, GitHub, blogs>

## Reddit Sentiment (Reddit Researcher)
- <real-world experiences, production war stories, community consensus from Reddit>
- <gotchas with severity ratings>
- <notable dissenting opinions>

## Competitive Landscape (Competitive Analyst)
- <approach comparison, recommendation>

## Security Assessment (Security Scanner)
- <dependency audit results, CVE findings>

## Synthesized Recommendation
Based on all research, the recommended approach is:
  <approach> because <reasons from all 5 agents>.

## Risks to Address in Implementation
- <risk 1> — mitigation: <strategy>
- <risk 2> — mitigation: <strategy>

## References
- [Official docs](URL)
- [Stack Overflow](URL)
- [Reddit thread](URL)
- [Benchmark comparison](URL)
- [CVE advisory](URL)
```

This synthesis feeds directly into the **Micro-Task Decomposer**, ensuring tasks are informed by real-world data, security findings, and the best available approach.

---

## Step 2: Micro-Task Decomposer

Break the feature into **atomic micro-tasks** — each with a single responsibility:

```yaml
# .workflow/<feature-name>/micro-tasks.yaml
feature: semantic-caching
micro_tasks:
  # Phase 0: Foundation (no dependencies)
  - id: MT-001
    description: "Create src/cache/__init__.py with public exports"
    type: create
    files: ["src/cache/__init__.py"]
    deps: []
    complexity: trivial
    surface: python

  - id: MT-002
    description: "Create CacheEntry dataclass with serialization"
    type: create
    files: ["src/cache/schema.py"]
    deps: []
    complexity: small
    surface: python

  - id: MT-003
    description: "Implement Redis-backed cache store with TTL and LRU"
    type: create
    files: ["src/cache/store.py"]
    deps: [MT-002]
    complexity: medium
    surface: python

  # Phase 1: Core logic (depends on foundation)
  - id: MT-004
    description: "Implement SemanticCache class with FAISS similarity"
    type: create
    files: ["src/cache/semantic_cache.py"]
    deps: [MT-002]
    complexity: medium
    surface: python

  - id: MT-005
    description: "Write unit tests for CacheEntry"
    type: test
    files: ["tests/unit/test_cache_schema.py"]
    deps: [MT-002]
    complexity: trivial
    surface: python-test

  - id: MT-006
    description: "Write unit tests for cache store"
    type: test
    files: ["tests/unit/test_cache_store.py"]
    deps: [MT-003]
    complexity: small
    surface: python-test

  - id: MT-007
    description: "Write unit tests for SemanticCache"
    type: test
    files: ["tests/unit/test_semantic_cache.py"]
    deps: [MT-004]
    complexity: small
    surface: python-test

  # Phase 2: Integration (depends on core)
  - id: MT-008
    description: "Add cache middleware to /v1/chat endpoint"
    type: modify
    files: ["src/api/v1/chat.py", "src/middleware/cache_middleware.py"]
    deps: [MT-003, MT-004]
    complexity: medium
    surface: python

  - id: MT-009
    description: "Write integration tests for cache endpoint"
    type: test
    files: ["tests/integration/test_cache_endpoint.py"]
    deps: [MT-008]
    complexity: medium
    surface: python-test

  # Phase 3: Frontend
  - id: MT-010
    description: "Add cache hit indicator badge to ChatMessage"
    type: modify
    files: ["src/components/ChatMessage.tsx"]
    deps: [MT-008]
    complexity: small
    surface: typescript

  - id: MT-011
    description: "Write component test for cache badge"
    type: test
    files: ["src/components/ChatMessage.test.tsx"]
    deps: [MT-010]
    complexity: trivial
    surface: typescript-test

  # Phase 4: Observability
  - id: MT-012
    description: "Add cache metrics (hit_rate, latency, size) to telemetry"
    type: modify
    files: ["src/observability/metrics.py"]
    deps: [MT-008]
    complexity: small
    surface: python
```

### Dependency Graph

```
MT-001 ──→ (done, trivial)
MT-002 ──→ (done, small)
  ├── MT-003 ──→ MT-008 ──→ MT-009
  │                ├── MT-010 ──→ MT-011
  │                └── MT-012
  │
  ├── MT-004 ──→ (merged into MT-008 deps)
  │
  └── MT-005
  └── MT-006 (after MT-003)
  └── MT-007 (after MT-004)
```

---

## Step 3: Dynamic Agent Spawning

Based on the micro-task list, **spawn coding agents dynamically**:

```yaml
# Agent spawning rules
spawn_rules:
  # Count tasks by surface, spawn agents accordingly
  python_tasks > 3:   spawn backend-1, backend-2, backend-3
  python_tasks <= 3:  spawn backend-1
  typescript_tasks > 2: spawn frontend-1, frontend-2
  typescript_tasks <= 2: spawn frontend-1
  test_tasks > 4:     spawn test-1, test-2, test-3
  test_tasks <= 4:    spawn test-1
  data_tasks > 0:     spawn data-1
  infra_tasks > 0:    spawn infra-1

  # Each agent gets micro-tasks it can handle
  agent_assignment:
    backend-1:    python tasks with lowest IDs (start first)
    backend-2:    python tasks not assigned to backend-1
    backend-3:    remaining python tasks
    frontend-1:   typescript tasks
    frontend-2:   remaining typescript tasks
    test-1:       python-test tasks with lowest IDs
    test-2:       remaining python-test tasks
    test-3:       typescript-test tasks
    data-1:       data/migration tasks
    infra-1:      infrastructure/CI tasks
```

### Agent Context (per agent)

```yaml
# Context given to backend-1
agent: backend-1
assigned_tasks:
  - MT-001: "Create src/cache/__init__.py with public exports"
  - MT-003: "Implement Redis-backed cache store with TTL and LRU"
  - MT-008: "Add cache middleware to /v1/chat endpoint"
dependencies_to_wait_for:
  - MT-003 waits for: MT-002
  - MT-008 waits for: MT-003, MT-004
blocking_tasks:
  - MT-003 blocks: MT-006, MT-008
  - MT-008 blocks: MT-009, MT-010, MT-012
files_i_own:
  - src/cache/__init__.py
  - src/cache/store.py
  - src/middleware/cache_middleware.py
  - src/api/v1/chat.py
skills_to_use:
  - python-patterns
  - tdd-workflow
  - backend-patterns
quality_requirements:
  - lint: pass (ruff + black)
  - type_check: pass (mypy)
  - tests: pass (pytest)
  - coverage: >= 80%
```

---

## Step 4: Parallel Execution

Agents execute their micro-tasks in parallel:

```
Time →

backend-1:  [MT-001] ──→ [wait for MT-002] ──→ [MT-003] ──→ [wait for MT-004] ──→ [MT-008]
backend-2:                      [MT-002] ──→ [MT-004]
test-1:                                         [MT-005] ──→ [MT-006] ──→ [MT-007]
test-2:                                                                     [MT-009]
frontend-1:                                                                 [MT-010] ──→ [MT-011]
infra-1:                                                                                [MT-012]
```

### Agent Execution Protocol

Each agent follows this exact protocol for every micro-task:

```
For each assigned micro-task MT-NNN:
  1. Wait for all dependencies to be marked DONE
  2. Read the micro-task spec and affected files
  3. Write tests FIRST (tdd-workflow skill)
  4. Verify tests FAIL (RED gate)
  5. Implement the change
  6. Run tests → verify GREEN
  7. Run lint → fix any issues
  8. Run format → fix any formatting
  9. Run type-check → fix any type errors
  10. Mark micro-task as DONE
  11. Notify the coordinator: "MT-NNN DONE"
```

### Agent Status Reporting

Agents report their status continuously:

```json
{
  "agent": "backend-1",
  "current_task": "MT-003",
  "status": "working",
  "completed_tasks": ["MT-001"],
  "waiting_for": ["MT-002"],
  "blocked": false,
  "last_update": "2026-04-12T14:32:00Z"
}
```

---

## Step 5: Dependency Resolution

When an agent marks a micro-task as DONE:

```
1. Coordinator receives: "MT-003 DONE from backend-1"
2. Coordinator updates task graph:
   - Mark MT-003 status = "done"
   - Check which tasks depend on MT-003:
     - MT-006: deps were [MT-003] → now all deps met → UNLOCK
     - MT-008: deps were [MT-003, MT-004] → MT-004 still pending → still blocked
3. Assign newly unlocked tasks to available agents:
   - MT-006 → assign to test-1 (next in queue)
4. Notify assigned agent: "MT-006 unlocked, start working"
```

---

## Step 6: Continuous Validation Loop (NEVER STOPS)

After ALL micro-tasks are marked DONE, the **continuous validation loop** begins:

```
┌─────────────────────────────────────────────────────────────────┐
│                  VALIDATION LOOP                                 │
│                                                                  │
│  Run in sequence (each must pass before next):                   │
│                                                                  │
│  1. LINT:        ruff check . && black --check . && eslint .     │
│         ↓                                                        │
│  2. FORMAT:      black . && prettier --check .                    │
│         ↓                                                        │
│  3. TYPE CHECK:  mypy src/ && tsc --noEmit                        │
│         ↓                                                        │
│  4. UNIT TESTS:  pytest tests/unit/ --cov=src/ --cov-fail-under=80│
│         ↓                                                        │
│  5. INTEG TESTS: pytest tests/integration/ -m 'not slow'          │
│         ↓                                                        │
│  6. E2E TESTS:   npx playwright test --retries=2                  │
│         ↓                                                        │
│  7. EVAL HARNESS: eval-harness score >= target                    │
│         ↓                                                        │
│  8. CODE REVIEW: code-reviewer agent approves                     │
│         ↓                                                        │
│  9. SECURITY:    security-reviewer + security-scan pass           │
│         ↓                                                        │
│  ┌───────────────────────────────────────────────────┐           │
│  │              ALL 9 CHECKS PASS?                    │           │
│  │                                                    │           │
│  │  YES → EXIT LOOP. Feature is COMPLETE. Proceed.    │           │
│  │  NO  → Identify which checks failed.               │           │
│  │         Route each failure to responsible agent.   │           │
│  │         Agent fixes the issue.                     │           │
│  │         RESTART loop from step 1.                  │           │
│  └───────────────────────────────────────────────────┘           │
└─────────────────────────────────────────────────────────────────┘
```

### Failure Routing

```yaml
failure_routing:
  lint_fail:        → route to agent that owns the failing file
  format_fail:      → auto-fix with formatter, re-check
  type_check_fail:  → route to agent that owns the failing file
  unit_test_fail:   → route to test-1 or the implementation agent
  integ_test_fail:  → route to the integration agent
  e2e_test_fail:    → route to frontend-1 or backend-1 (depending on failure)
  eval_fail:        → route to the primary implementation agent
  code_review_fail: → route to the agent with BLOCKER comments
  security_fail:    → route to the agent that introduced the issue
```

### Loop Exit Conditions

The loop exits when:

```
ALL of the following are true:
  ✓ Lint passes (no ruff/black/eslint errors)
  ✓ Format passes (no formatting issues)
  ✓ Type check passes (no mypy/tsc errors)
  ✓ All unit tests pass
  ✓ All integration tests pass
  ✓ All E2E tests pass
  ✓ Eval harness score >= target threshold
  ✓ Code reviewer approves
  ✓ Security reviewer approves AND security scan is clean

→ Feature is COMPLETE. Stop the workflow. Proceed to merge.
```

### Max Loop Safety

```yaml
loop_safety:
  max_global_iterations: 30
  on_max_reached:
    1. Log all remaining failures with context
    2. Create escalation report
    3. Notify Project Manager agent
    4. Project Manager escalates to human with:
       - Feature name
       - Which gates are still failing
       - How many iterations ran
       - What fixes were attempted
       - Recommended action (abort, extend loop, manual fix)
```

---

## Step 7: Git Operations

When the validation loop exits (feature complete):

```bash
# Create feature branch
git checkout -b feat/<feature-name>

# Commit all changes with structured message
git add -A
git commit -m "feat: <feature description>

- List all micro-tasks completed
- Reference feature spec: docs/features/<name>/spec.md
- All quality gates passed:
  - Lint: ✓
  - Format: ✓
  - Type check: ✓
  - Unit tests: ✓ (coverage: XX%)
  - Integration tests: ✓
  - E2E tests: ✓
  - Eval: Pass@k = X.XX
  - Code review: ✓
  - Security: ✓"

# Push and create PR
git push origin feat/<feature-name>
gh pr create \
  --base main \
  --head feat/<feature-name> \
  --title "feat: <feature description>" \
  --body-file .workflow/<feature-name>/PR_BODY.md

# Merge (all gates already passed locally)
gh pr merge --squash --delete-branch
```

---

## Anti-Patterns

- **No micro-task breakdown** — agents work on vague, large tasks instead of atomic units
- **Agents stepping on each other** — no file ownership assignment, causing conflicts
- **Stopping the loop early** — merging before ALL 9 quality gates pass
- **Ignoring dependencies** — starting tasks before their deps are done
- **No RED gate** — implementing before verifying tests fail
- **Infinite loops** — hitting max iterations without escalation
- **No status reporting** — agents work silently with no visibility
- **Skipping the repo scan** — not reading the full repo before breaking down tasks
- **Skipping web research** — implementing without checking official docs, community experience, or security advisories
- **Trusting unverified sources** — using random blogs instead of official documentation
- **Ignoring CVE findings** — adding dependencies with known vulnerabilities

## Best Practices

1. **Scan the full repo first** — understand all surfaces before breaking down tasks
2. **Run web research in parallel** — check official docs, community experience, benchmarks, and CVEs before micro-task decomposition
3. **Trust verified sources only** — official docs > community blogs > random posts
4. **Audit all new dependencies** — security scanner must clear every new package
5. **Atomic micro-tasks** — each task should be completable by one agent in one session
6. **Explicit dependencies** — every task lists what it waits for
7. **Tests first** — every micro-task follows RED → GREEN
8. **Report status continuously** — agents must be queryable at any time
9. **Never stop the loop early** — ALL 9 gates must pass before merging
10. **Escalate on max iterations** — don't spin forever, escalate to human
11. **Use feature specs when no issues exist** — `docs/features/<name>/spec.md`
12. **One feature, one workflow** — don't mix features in the same workflow
13. **Clean up after merge** — remove worktrees, branches, temp files

## Related Skills

- **code-reviewer** — code review as part of the validation loop
- **security-reviewer** — security validation in the validation loop
- **security-scan** — automated vulnerability scanning
- **ai-judge** — validates design packages before implementation
- **tdd-guide** — test-driven implementation for each micro-task
- **planner** — breaking large features into micro-tasks
- **eval-harness** — scoring implementation quality in the loop
- **verification-loop** — continuous quality gate enforcement
- **deep-research** — in-depth research methodology
- **exa-search** — neural web search for research
- **search-first** — search-before-implement pattern
- **technical-debt-analyzer** — comprehensive debt analysis across 8 dimensions
- **codebase-analyzer** — deep architecture, data flow, and pattern analysis
- **codebase-learner** — systematic codebase study for onboarding and conventions
- **codebase-report** — unified codebase analysis report
- **technical-debt-report** — unified technical debt report with phased remediation
- **multi-agent-project-manager** — coordinating multiple concurrent workflows

## Related Agents

- **reddit-researcher** — deep Reddit analysis for user experiences, war stories, consensus
- **web-researcher** — official documentation and API reference lookup
- **community-researcher** — Stack Overflow, GitHub issues, dev blogs
- **competitive-analyst** — alternative approach comparison and benchmarking
- **security-scanner** — CVE and dependency audit
