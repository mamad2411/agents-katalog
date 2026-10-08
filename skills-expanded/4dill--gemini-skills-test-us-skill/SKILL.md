---
name: test-us
description: "Generate and run real-infrastructure pytest tests for a User Story.\ \ Reads acceptance criteria from docs/USER-STORIES.md, picks the deepest testable\ \ layer (integration > agent > unit \u2014 E2E only for full scan flows), presents\ \ a test plan for approval, then writes and runs tests against real PostgreSQL,\ \ real Docker, real HTTP \u2014 never synthetic mocks when real infrastructure is\ \ available. This skill should be used when the user wants to prove a US actually\ \ works: real round-trips, real state changes, real assertions. Invoke with /test-us\ \ US-XXX."
---

# Test US (Real Infrastructure Focus)

Generate pytest tests from User Story acceptance criteria. Target the deepest layer that real infrastructure supports. The goal is **proof**: if the test passes, the code provably works — not just that mocks behaved.

## Purpose

Read one User Story from `docs/USER-STORIES.md`, understand the functional goal, pick the correct test layer based on what infrastructure the US exercises, design tests that prove that goal with real data and real services, implement them, and run them.

## Layer Selection Rules

Before building the test plan, classify the US by what it touches:

| US touches | Target layer | Directory | Runs in CI |
|---|---|---|---|
| DB models, queries, migrations, pgvector | **integration** | `tests/integration/database/` | Yes |
| Docker container lifecycle, exec, files | **integration** | `tests/integration/docker/` | Yes |
| LangChain/LangGraph tools (terminal, file, browser, search, graphiti) | **integration** | `tests/integration/tools/` | Yes |
| Graphiti/Neo4j (add + search round-trip) | **integration** | `tests/integration/graphiti/` | Yes |
| Agent graph nodes, barriers, routing logic | **agent** | `tests/agent/` | Yes |
| Pure Pydantic models, parsing, config validation | **unit** | `tests/unit/` | Yes |
| Full scan flow: MCP → Generator → Orchestrator → Scanner → Reporter | **e2e** | `tests/e2e/` | Never (manual) |

**Priority rule**: integration > agent > unit. Never put a test in a lower layer when the US has real infrastructure to exercise. Never put a DB round-trip test in `tests/e2e/` when testcontainers can run it in `tests/integration/`.

## Workflow

### Phase 1: Parse the User Story

1. Read `docs/USER-STORIES.md`.
2. Locate the requested US ID (e.g. `US-013`).
3. Extract:
   - Title and story statement
   - Acceptance Criteria checklist
   - Tests Required checklist
   - Technical Notes and Dependencies
4. Derive the behavior goal in one sentence: "What must provably work after this US?"
5. Classify which infrastructure the US exercises → choose layer per the table above.

If the US is not found, report the error and list available US IDs.

### Phase 2: Build a Real-Infrastructure Test Strategy

Apply these rules to every acceptance criterion and required test:

**For integration targets (DB / Docker / tools / graphiti):**
Every US that stores, retrieves, or transforms data requires at least one mandatory round-trip proof:
1. Insert/create data through the real code path
2. Retrieve/search/read through the real service
3. Assert the exact expected value, ordering, or state
4. Execute cleanup path (delete/remove/archive) and verify the state change

**For agent targets:**
- Use mocked LLM responses with realistic tool call sequences (from `references/real-data-fixtures.md`)
- But execute tools against real DB/Docker where possible — only mock the LLM, not the infrastructure

**For unit targets:**
- Use realistic domain data (CVEs, ports, tool outputs, real URLs) — never `"foo"`, `"ok"`, toy vectors
- Use `respx` to mock HTTP with realistic HTML/JS/headers that match actual detector patterns

**Minimum test set per US:**
1. Happy path: proves the primary behavior goal with realistic inputs
2. Round-trip lifecycle: insert/create → retrieve/assert → cleanup/delete → verify gone
3. Failure path: realistic invalid input rejected with explicit error assertion

If a US is too small to justify three distinct tests, explain why and propose the smallest valid set.

### Phase 3: Present Plan for Approval

Present the plan in this format and **stop for approval** before writing any files:

```text
## Test Plan for US-XXX: {title}

### Goal
{one-sentence behavior goal}

### Layer: {integration | agent | unit | e2e}
{reason: what infrastructure this US exercises}

### Tests ({tests/layer/path/test_file.py})

1. **test_name_here** 🔁
   - Tests: {acceptance criterion / tests required item}
   - What it does: {plain behavior description}
   - Real data: {realistic payload — e.g. "flow with CVE title, model claude-sonnet-4-6"}
   - Real infrastructure: {testcontainers PostgreSQL | real Docker daemon | real HTTP | mocked LLM}
   - Round-trip: {create → retrieve → assert exact value → delete → assert gone}

2. **test_name_here**
   - Tests: ...
   - What it does: ...
   - Real data: ...
   - Real infrastructure: ...

3. **test_name_here** (failure path)
   - Tests: ...
   - What it does: ...

---
Total: X tests | Layer: {integration/agent/unit/e2e} | Runs in CI: {Yes/No}

Approve this plan? (approve / modify / skip tests)
```

### Phase 4: Implement Tests

After approval:
1. Read `references/test-patterns.md` — copy the round-trip pattern for the target layer.
2. Read `references/real-data-fixtures.md` — use ready-made realistic payloads, never invent toy data.
3. Read `references/test-stack.md` — match imports, fixtures, and async style.
4. Read existing files in the target test directory to match conftest fixtures and style.
5. Read source modules under test to craft realistic inputs that hit real logic paths.
6. Append to existing test file if one exists, or create a new one at the planned path.

Each test must have:
- Docstring tied to the acceptance criterion it covers (include 🔁 for round-trip proofs)
- Correct pytest marker: `@pytest.mark.integration`, `@pytest.mark.agent`, or `@pytest.mark.e2e`
- Realistic domain data: CVEs, ports, scan results, real model names, real URLs
- Assertions that prove behavior: exact field match, ordering, state transition — not just `assert result is not None`
- Cleanup in `finally` or via fixture teardown — leave infrastructure clean

**Never:**
- Use `pytest.skip()` for core proof scenarios — fail loudly so infrastructure problems are visible
- Use placeholder data like `"ok"`, `"foo"`, `1234`, or zero-vectors when realistic domain data is available
- Mock a database when testcontainers can spin up a real one
- Mock Docker when a real daemon is available
- Write assertions that only check "no exception was raised"

### Phase 5: Run and Report

Run only the generated tests:

```bash
pytest {test_file_paths_or_nodeids} -v --tb=short
```

For integration tests, Docker must be running. For agent tests, no external deps needed.

Report:

```text
## Results for US-XXX

Layer: {integration | agent | unit | e2e}
PASSED ({X}/{Y}) | Runs in CI: {Yes/No}
FAILED ({Z}/{Y})

Failed tests:
- test_name: {error summary}

Next steps:
- {concrete fix}
```

If failures indicate missing implementation, report:

```text
NOT IMPLEMENTED ({X}/{Y}) — these tests define required behavior, fix the production code
```

**Rule: never change a failing test to make it pass.** If the test correctly describes what the US requires and the code is wrong, fix the code. If the test assertion is wrong, explain why and ask before changing it.

## Rules

- Never invent acceptance criteria.
- Never skip the approval step.
- Integration first: if real infrastructure is available, use it — do not fall back to mocks.
- E2E only for full scan flows; individual US features belong in integration/agent/unit.
- Minimum 3 tests per US (happy path, round-trip lifecycle, failure path), or justify a smaller set.
- Use realistic domain data: CVEs, real hostnames, nmap output, model names, DB states.
- Fail loudly: never hide missing infrastructure behind `pytest.skip()` for proof-critical tests.
- Read source code and existing tests before writing anything.
- Append to existing test files rather than replacing them.
- Tests that run in CI prove more than tests that run manually — prefer layers that run in CI.

## Real Data Requirements

- Flows: use real titles like `"scan https://juice-shop.local"`, model `"claude-sonnet-4-6"`
- Vectors: use 1536-dim embeddings from realistic security text (CVEs, service banners, findings)
- Docker: use `alpine:3.20` or `kali-linux/kali-rolling` — real images, real exec commands
- Agents: use realistic tool call sequences (nmap commands, actual file paths, real finding text)
- Assertions: check exact field values, ordering, state transitions — not just `assert result`

## Argument Handling

- `/test-us US-013` — generate tests for one US
- `/test-us US-008 US-009` — process sequentially, one plan per US
- `/test-us` — ask for US ID

## References

- `docs/USER-STORIES.md` — acceptance criteria source of truth
- `references/test-patterns.md` — round-trip and layer-specific patterns
- `references/real-data-fixtures.md` — realistic payload fixtures
- `references/test-stack.md` — pytest stack, markers, conftest structure
- `references/test-layers.md` — layer boundaries and module mapping
- `docs/EXECUTION-FLOW.md` — end-to-end runtime phases
- `docs/AGENT-ARCHITECTURE.md` — behavior context for agent-layer validation
