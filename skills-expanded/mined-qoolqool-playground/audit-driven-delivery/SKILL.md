---
name: add-audit-driven-delivery
description: "End-to-end delivery pipeline for DooD + Docker Compose microservices: AUDIT → DESIGN → PLAN → EXECUTE → HARDEN. Consolidates brainstorming, DDD, SPARC, TDD, and engineering methodology with mandatory phase gates (Gate 1: spec, Gate 2: implementation, Gate 3: security/policy, Gate 4: runtime/integration) and DooD-aware decision trees."
version: 4
created: 2026-05-20
updated: 2026-05-22
---
# ADD — Audit-Driven Delivery Pipeline

The end-to-end delivery workflow that produced the x402 PoC: 9 microservices, 3 network segments, 17 Docker containers, distributed tracing, fault injection, live pcap capture, and multiple guided scenarios — built incrementally with human review at every phase gate.

## When to Use

Use this skill when the user asks to:

- Implement or evolve a phase (Phase 2, Phase 3, …)
- Add services, networks, tests, or infrastructure to the testbed
- Do any non-trivial change under `/workspace` that needs design + plan + review
- Start a new DooD microservices project from scratch (greenfield)
- Produce an audit trail from "what exists" through "shipped and verified"

**Do NOT use** when: fixing a trivial bug (one-line change), performing routine maintenance (version bumps), or doing exploratory prototyping (though prototyping may feed into Phase 0 audit).

**Mandatory gate pre-conditions:** Before writing code (Phase 3), Gate 1 must be PASS. After every implementation batch and before HARDEN, Gate 2 must be PASS. Before HARDEN or any "done" claim, Gate 3 must also be PASS. Before HARDEN or any "done" claim, Gate 4 must also be PASS — the stack must be running, healthy, and E2E tests passing. See the `quality-gates` skill for invocation and action consumption.

## Mandatory Skill Usage

**This skill ORCHESTRATES other skills — it does NOT replace them.** When the audit or design phase identifies a need, you MUST use the appropriate reference skill:

| If the task involves... | You MUST use this skill |
|-------------------------|------------------------|
| DooD + Compose setup on Podman | `dood-compose-setup` |
| Bootstrap CLI + phased bringup | `compose-bootstrap-cli` |
| Multi-network isolation | `compose-multi-network-isolation` |
| Test-runner container | `compose-test-runner-container` |
| Port forwarding (Podman VM) | `dood-port-forwarding` |
| Container discovery (varying names) | `dood-discover-containers-by-pattern` |
| TDD for infrastructure | `tdd-dood-compose-infra` |
| 3-document workflow | `design-impl-result-docs` |
| Observability dashboard | `compose-observe-dashboard` |
| Prometheus metrics | `compose-prometheus-metrics-pipeline` |
| Subagent-driven implementation | `subagent-driven-development` |
| Finishing a branch | `finishing-a-development-branch` |

**DooD-Specific Requirement:** If the user mentions "DooD", "Docker-outside-of-Docker", or the project has a DooD setup, you MUST follow the DooD-specific patterns in this skill and reference the appropriate sub-skills above. Do NOT explore alternative solutions.

**Test-runner decision (small vs large projects):** The test-runner container is the SCDLT pattern for running integration/E2E tests from inside the compose network. For small projects (a few services, the E2E test hits published ports), you may remove the test-runner and run the E2E test directly on the host. This is an explicit decision, not a guess — see the `quality-gates` skill's "Test-Runner Decision" section. When in doubt, ask the user.

## TDD Requirement

**Every implementation task MUST include unit tests:**

- **New functions/features:** Write the test FIRST (Red), then implement (Green), then refactor
- **Modifying existing code:** Run existing tests before and after to ensure no regression
- **Infrastructure additions:** Use `tdd-dood-compose-infra` pattern — write failing integration tests from test-runner first
- **Test location:** Tests go in `tests/` directory. Unit tests run on the host; E2E tests run from the test-runner container (or directly on the host for small projects — see the `quality-gates` skill's "Test-Runner Decision")
- **Test verification:** Each test must verify specific, observable behavior

**No exceptions:** If a task cannot be tested, it should not be implemented. Document why testing is impossible as a risk.

## Subagent Requirement for Implementation

**Phase 3 (EXECUTE) MUST use subagents for implementation** when:
- Tasks are mostly independent (can run in parallel)
- Each task takes >5 minutes of work
- Multiple files or services are involved

**Subagent pattern:**
1. Dispatch implementer subagent per task (use `subagent-driven-development`)
2. Two-stage review after each task: spec compliance → code quality
3. Fix issues before proceeding to next task
4. Final review after all tasks complete

**Do NOT use subagents for:**
- Trivial one-line changes
- Tightly coupled tasks requiring constant coordination
- Exploratory debugging

## DooD Context

This methodology assumes a **Docker-outside-of-Docker** development environment where:

- A **remote Docker daemon** (often Podman-managed on macOS/Linux) is accessed via `DOCKER_HOST=tcp://<vm-ip>:2375`
- Docker Compose orchestrates services **directly on the remote daemon** (no nested DinD container)
- Services are distributed across multi-network segments for isolation
- A **test-runner container** spans all networks and runs integration tests
- A **bootstrap.sh CLI** manages the lifecycle (`up`, `down`, `status`, `verify`, etc.) with phased bringup
- Source code is mounted via **bind mounts** using host-resolved paths (`HOST_PROJECT_DIR`)
- Port forwarding requires Podman VM awareness — ports are exposed on the VM IP, not localhost

**Podman-specific:** The host may use Podman instead of Docker. This affects socket paths (`DOCKER_HOST=tcp://<vm-ip>:2375`), storage drivers, and port forwarding (ports bind to the VM IP, not localhost). The sub-skills handle the details; ADD just flags the decision points.

**Key sub-skills that handle the technical details (ADD routes to them):**

| Concern | Skill | When to Use |
|---------|-------|-------------|
| DooD + Compose setup on Podman | `dood-compose-setup` | Greenfield setup, Podman configuration |
| Bootstrap CLI + phased bringup | `compose-bootstrap-cli` | Creating or extending bootstrap.sh |
| Multi-network isolation | `compose-multi-network-isolation` | New network segments, ACL services |
| Test-runner container | `compose-test-runner-container` | Cross-network testing setup |
| Port forwarding (Podman VM) | `dood-port-forwarding` | Exposing services to host |
| Container discovery (varying names) | `dood-discover-containers-by-pattern` | Dynamic container name resolution |
| TDD Red-Green-Refactor for infra | `tdd-dood-compose-infra` | Adding Jaeger, Redis, databases |
| 3-document workflow | `design-impl-result-docs` | Full traceability chain |
| Observability dashboard | `compose-observe-dashboard` | Terminal-based health dashboard |
| Prometheus metrics pipeline | `compose-prometheus-metrics-pipeline` | Adding metrics to services |
| Subagent-driven implementation | `subagent-driven-development` | Phase 3 execution with fresh subagents |
| Finishing a development branch | `finishing-a-development-branch` | Merge/PR/cleanup decisions |

**MANDATORY:** When Phase 0 audit or Phase 1 design identifies a need matching the table above, you MUST explicitly invoke the corresponding skill. Do NOT reinvent solutions.

## Mandatory Gate Pre-Conditions (quality-gates)

The `quality-gates` skill provides three quality gates that are non-negotiable pre-conditions of ADD phases. Do not re-implement gate logic here — reference the skill for invocation and action consumption.

| Gate | When It Must Be PASS | What Happens If It Fails |
|------|----------------------|--------------------------|
| **Gate 1** (spec validation) | Before Phase 3 EXECUTE — before writing or changing any file under `/workspace` | Stop. Run `./testbed.sh validate <spec.json>`, apply returned `actions`, re-run until `status=pass`. Do not start implementation. |
| **Gate 2** (implementation validation) | After every EXECUTE batch that touches compose, Dockerfiles, configs, tests, or scripts. Also before Phase 4 HARDEN. | Stop. Run `./testbed.sh gate2 --spec <spec.json> --workspace /workspace`, apply returned `actions`, re-run until `status=pass`. Do not present the batch or claim HARDEN is done. |
| **Gate 3** (security & policy guardrails) | Before Phase 4 HARDEN. Also after any EXECUTE batch that changes security-relevant config (privilege/caps, volumes/mounts, env/secrets, network_mode, ports, guardrails-related settings, **npm dependencies/package.json**). | Stop. Run `./testbed.sh gate3 --spec <spec.json> --workspace /workspace`, apply returned `actions`, re-run until `status=pass`. Do not advance past a red Gate 3. |
| **Gate 4** (runtime & integration verification) | Before Phase 4 HARDEN. Also after any EXECUTE batch that changes services, compose config, or E2E tests. | Stop. Run `./testbed.sh gate4 --workspace /workspace [--skip-up]`, apply returned `actions`, re-run until `status=pass`. Do not advance past a red Gate 4. |

**Hard rules:**
- Do not auto-advance past a failing gate. Treat it like any other blocker: stop, report the GateFeedback, fix, re-validate.
- Before any "done", "ready for review", or HARDEN claim, **all four gates must be PASS**. Run all four if any is stale.
- See the `quality-gates` skill for invocation syntax and how to consume `diagnostics` + `actions`.

## Core Principle: Audit Before You Build

**Never start implementing until you can answer three questions:**
1. **What exists?** — Read the running code, not the documentation.
2. **What's tested?** — Trace each test to what it actually verifies, not what it claims to test.
3. **What's the gap?** — Classify every flow as WIRED, STUB, MISSING, or BLOCKED.

## The 5 Phases

Every phase has a **mandatory ⏸️ gate** at the end. The agent NEVER auto-advances past a gate — it presents the artifact and waits for human review. This is non-negotiable.

```
AUDIT ─[⏸️ show matrix]→ DESIGN ─[⏸️ show design doc]→ PLAN ─[⏸️ show plan]→ EXECUTE ─[⏸️ per batch]→ HARDEN ─[⏸️ done?]→
```

---

### Phase 0: AUDIT — "What exists?"

**Goal:** Understand the current system before proposing any change.

This phase has **two tracks** depending on whether a DooD project already exists.

---

#### Track A: Greenfield — No existing DooD project

**How to detect:** No `docker-compose.yml`, no `bootstrap.sh`, no service directories, no `Dockerfile` files.

**If greenfield, the first design task MUST be the DooD infrastructure itself.** Do not skip to designing application services.

**What to check:**

| Check | How | Action if missing |
|-------|-----|-------------------|
| DooD environment setup | Look for `DOCKER_HOST` env var, `setenv.sh`, or `scripts/bootstrap.sh` | Design DooD environment first (see `dood-compose-setup`) |
| Network topology | Any existing network segments defined | Design multi-network isolation (see `compose-multi-network-isolation`) |
| Bootstrap CLI | `scripts/bootstrap.sh` or equivalent | Design bootstrap CLI (see `compose-bootstrap-cli`) |
| Test-runner | Container that spans all networks | Design test-runner (see `compose-test-runner-container`) |
| Shared library | Common Python package for all services | Design shared library (see `python-shared-library-compose-monorepo`) |
| Observability | Jaeger, Prometheus, Grafana | Optional — design after core infrastructure |

**Artifact:** Audit report stating "This is a greenfield project. Infrastructure design needed first."

**⏸️ GATE:** Present the audit. Say: *"No existing DooD infrastructure found. The first task is designing the Docker-outside-of-Docker environment. Ready to proceed?"*

---

#### Track B: Brownfield — DooD project exists

**How to detect:** `deploy/compose/` directory exists, `scripts/bootstrap.sh` exists, services are running or defined.

**What to check in order:**

**Check 1: Does the feature need a new container/service?**
- Is it a new standalone service? → needs compose file entry, Dockerfile, service directory, network assignment
- Is it an infrastructure addition (Jaeger, Prometheus, database)? → needs compose entry + network placement + port forwarding
- Is it a modification to existing service(s)? → identify which specific service to modify

**Check 2: Network placement (if new container)**
- Which existing network segment does it belong to?
- Does it need to cross segments? → needs to be an ACL/bridge service (multi-homed)
- Does it need host port forwarding? → Podman VM port mapping required
- See `compose-multi-network-isolation` for network topology patterns

**Check 3: Existing infrastructure audit**
- What bootstrap.sh subcommands exist? (up/down/status/verify/observe/profile/review/scenario/loadgen)
- Does the test-runner exist? Is it on all required networks already?
- What verification gates exist? (bootstrap.sh verify passes?)
- What observability stack exists? (Jaeger? Prometheus? Grafana?)

**Check 4: Produce the Audit Matrix** — for each integration point or flow, classify:

| Status | Meaning | Action |
|--------|---------|--------|
| WIRED | Code exists, tests pass end-to-end | Verify, move on |
| STUB | Code skeleton with hardcoded values | Replace with real call |
| MISSING | No code exists at all | Implement from scratch |
| BLOCKED | External dep not available | Document, add workaround, track as risk |

**Check 5: Check what's tested** — trace each test to the actual HTTP calls it makes. If more than 50% of tests bypass the orchestration layer and call downstream mocks directly, the integration is not validated regardless of the pass rate.

**Check 6: Define the scope boundary** — explicitly list what's OUT of scope and why:

| Item | Why Out of Scope |
|------|-----------------|
| ... | ... |

**Check 7: Search existing docs** — look in `docs/sdlc/`, `knowledgebase/` (if available), `docs/gaps/` for prior work on this topic.

**Artifact:** Audit matrix + gap report with greenfield/brownfield classification, new-container decision, and network placement recommendation.

**⏸️ GATE:** Present the audit matrix and decision summary. Say: *"Here's the audit. Ready to proceed to design?"* Do NOT continue to Phase 1 without explicit approval.

---

### Phase 1: DESIGN — "What + Why"

**Goal:** Produce a validated design document covering architecture, decisions, and verification criteria.

**Step 1: Explore approaches**
Propose 2-3 different approaches with trade-offs. Present options conversationally with your recommendation and reasoning. Lead with your recommended option and explain why.

**Step 2: DDD analysis**
- Identify which bounded context(s) the work touches
- Map communication patterns between contexts:
  - Same context → conformist (internal RPC)
  - Different contexts → anti-corruption layer (translation service)
- Network segments are physical bounded context boundaries: a service on `settlement-net` cannot call `internet` directly — the boundary enforces the context.
- Document context mapping: Open Host Service, Published Language, Anti-Corruption Layer, Conformist.
- Reference `compose-multi-network-isolation` for network topology decisions.

**DooD-specific design decisions to document:**
- For new services: network segment, compose file placement, port mappings, environment variables
- For infrastructure: compose config, Podman VM port forwarding (see `dood-port-forwarding`)
- For cross-segment traffic: which multi-homed service acts as the bridge (ACL)
- For bind mounts: `HOST_PROJECT_DIR` resolution strategy (virtiofs translation for Podman on macOS)

**Step 3: Write the design document**
Write to `docs/sdlc/02-design/YYYY-MM-DD-<topic>-design.md` covering:

**MANDATORY:** This path is non-negotiable. Do NOT use a flat `docs/design.md` or any other location. The numbered `docs/sdlc/` tree is the only valid home for SDLC documents.

```markdown
## Overview
One-paragraph description.

## Design Decisions
| Decision | Choice | Rationale | Alternatives Considered |
|----------|--------|-----------|------------------------|

## Architecture / DDD Analysis
Bounded contexts, network placement, anti-corruption layers.

## Verification Criteria
Numbered list of testable outcomes.

| # | Criterion | How to Verify |
|---|-----------|---------------|

## Out of Scope
```

**Artifact:** Design document at `docs/sdlc/02-design/YYYY-MM-DD-<topic>-design.md`

**After writing:** Add an entry for this document in `docs/sdlc/INDEX.md` under the Design section (View A) and the relevant feature track (View B).

**⏸️ GATE:** Present the design document in sections (200-300 words each, asking "does this look right?" after each). After approval, say: *"Design approved. Ready for me to create the implementation plan?"* Do NOT proceed to Phase 2 without explicit approval.

---

### Phase 2: PLAN — "How"

**Goal:** Produce a step-by-step implementation plan with exact file paths, code, commands, and expected outputs. Assume the implementer knows nothing about the project.

**Break the design into bite-sized TDD tasks** (each task is 2-5 minutes of work):

**TDD REQUIREMENT:** Every task MUST include tests:

```markdown
### Task N: [Component Name]

**Test File:** `tests/exact/path/to/test.py`

**Step 1: Write the failing test FIRST**
```python
def test_specific_behavior():
    """Test must verify observable behavior, not implementation."""
    result = function(input)
    assert result == expected
```

**Step 2: Run test to verify it fails**
Run: `docker exec test-runner python3 -m pytest tests/path/test.py::test_name -v`
Expected: FAIL with clear reason (function not defined, import error, etc.)

**Step 3: Write minimal implementation**
```python
def function(input):
    return expected
```

**Step 4: Run test to verify it passes**
Expected: PASS

**Step 5: Commit with test + implementation together**
```

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py`
- Test: `tests/exact/path/to/test.py` (REQUIRED)

**Rules for tasks:**
- Each task is independently verifiable (run a command, see pass/fail)
- Include EXACT code in the plan, not vague descriptions
- Map the dependency chain (which tasks can run in parallel, which are sequential)
- If the plan exceeds ~8 tasks, split into phases with checkpoint tags
- Include the final checklist of all files changed

**DooD-specific planning patterns:**
- **Infrastructure TDD** (new compose service, observability): Use `tdd-dood-compose-infra` pattern — write failing integration tests from test-runner first. Tests should fail with "connection refused" or "DNS doesn't resolve" before adding the service.
- **Container discovery**: Do not hardcode container names — use `docker ps --format` filters (see `dood-discover-containers-by-pattern`). Include discovery commands in the plan.
- **Rebuild order**: `docker compose -f deploy/compose/<file>.yml down`, rebuild images, `docker compose -f deploy/compose/<file>.yml up -d --build` (see `compose-bootstrap-cli` phased bringup section). Include exact commands in the plan.
- **3-document workflow**: Use `design-impl-result-docs` pattern for the full traceability chain. Plan must reference where the implementation result doc will be written.
- **Bind mount paths**: All volume mounts in compose files must use `${HOST_PROJECT_DIR}` (host-resolved path) — the Docker daemon runs on a remote VM and cannot resolve container-internal paths. Plan must include `HOST_PROJECT_DIR` resolution.

**Subagent Planning:** If tasks are independent, plan for subagent execution (see Phase 3). Each task should be self-contained with clear success criteria.

**Artifact:** Implementation plan at `docs/sdlc/03-implementation-plans/YYYY-MM-DD-<topic>-impl.md`

**MANDATORY:** This path is non-negotiable. Do NOT use a flat `docs/` path. The numbered `docs/sdlc/` tree is the only valid home for SDLC documents.

**After writing:** Add an entry for this document in `docs/sdlc/INDEX.md` under the Implementation Plans section (View A) and the relevant feature track (View B).

**⏸️ GATE:** Present the task overview and dependency chain. Say: *"Plan saved. Ready to start executing? I'll process tasks in batches and report after each batch."* Do NOT proceed to Phase 3 without explicit approval.

---

### Phase 3: EXECUTE — "Build it"

**Goal:** Implement the plan incrementally with TDD, using subagents for independent tasks.

**⏸️ GATE CHECK — Gate 1 must be PASS before starting.**
Before writing or changing any file under `/workspace`, confirm Gate 1 is PASS on the approved spec. If not, stop and run `./testbed.sh validate <spec.json>` via the `quality-gates` skill. Do not start implementation until `status=pass`.

**⏸️ GATE CHECK — Gate 2 after every batch.**
After every EXECUTE batch that touches compose, Dockerfiles, configs, tests, or scripts, run `./testbed.sh gate2 --spec <spec.json> --workspace /workspace`. If it fails, apply the returned `actions`, fix, and re-run before presenting the batch for human review.

**⏸️ GATE CHECK — Gate 3 after security-relevant batches.**
After any EXECUTE batch that changes privilege/caps, volumes/mounts, env/secrets, network_mode, ports, guardrails-related settings, **or npm dependencies (package.json)**, also run `./testbed.sh gate3 --spec <spec.json> --workspace /workspace`. If it fails, apply the returned `actions`, fix, and re-run before presenting the batch or advancing.

**⏸️ GATE CHECK — Gate 4 after service-affecting batches.**
After any EXECUTE batch that adds, removes, or reconfigures services (compose changes, new Dockerfiles, config changes), also run `./testbed.sh gate4 --workspace /workspace [--skip-up]`. If it fails, apply the returned `actions`, fix, and re-run before presenting the batch or advancing.

**SUBAGENT REQUIREMENT:**

**Use subagents when:**
- Tasks are mostly independent (can run in parallel without conflicts)
- Each task takes >5 minutes of work
- Multiple files or services are involved
- The plan explicitly marks tasks as "subagent-ready"

**Do NOT use subagents when:**
- Tasks are tightly coupled (require constant coordination)
- Exploratory debugging or investigation
- Trivial one-line changes

**When using subagents, you MUST:**
1. Use the `subagent-driven-development` skill
2. Dispatch one implementer subagent per task
3. Run two-stage review after each task (spec compliance → code quality)
4. Fix all issues before proceeding to next task
5. Run final review after all tasks complete

**Manual Execution (when subagents not appropriate):**

1. **Execute in batches** — default 3 tasks per batch, then pause for feedback.
2. **For each task:** Follow the plan steps exactly (write failing test → verify fail → implement → verify pass → commit).
3. **Root-cause fix on failures** — do NOT fix symptoms. When a test fails: read the error carefully, trace the actual call chain, do not ignore errors.
4. **Incremental-build:** Wire one integration, test it, fix what breaks, THEN wire the next. Do not wire all clients then test.
5. **Document as you go:** Every discovered gotcha, every non-obvious behavior, every workaround — record it.

**TDD ENFORCEMENT:**
- Every task MUST start with a failing test
- Tests must run from the test-runner container
- No task is complete until tests pass
- If a task cannot be tested, STOP and report (do not implement untestable code)

**DooD execution context — ALL commands run directly against the remote Docker daemon (no nested DinD):**

```
┌──────────────────────────────────────────────────────────┐
│  HOST (macOS/Linux)                                       │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Podman VM (Docker daemon at tcp://<ip>:2375)     │   │
│  │  ┌──────────────────────────────────────────────┐ │   │
│  │  │  Docker Compose Network                      │ │   │
│  │  │  ┌──────────┐  ┌──────────┐                 │ │   │
│  │  │  │ service-1│  │ service-2│                 │ │   │
│  │  │  └──────────┘  └──────────┘                 │ │   │
│  │  │  ┌────────────────────────────────────┐     │ │   │
│  │  │  │ test-runner (multi-homed)           │     │ │   │
│  │  │  │ ← ALL tests run from here            │     │ │   │
│  │  │  └────────────────────────────────────┘     │ │   │
│  │  └──────────────────────────────────────────────┘ │   │
│  └────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────┘
```

**Command patterns used in this phase:**

| Action | Pattern |
|--------|---------|
| Run tests | `docker exec test-runner python3 -m pytest tests/ -v` |
| Discover test-runner | `docker ps --format '{{.Names}}' \| grep test-runner \| head -1` |
| Rebuild compose | `docker compose -f deploy/compose/<file>.yml up -d --build` |
| Copy scripts to test-runner | `docker cp /workspace/script.py test-runner:/tmp/script.py` |
| Run inline Python | Single-quote the Python block to avoid host shell expansion |
| Service health check | `docker exec <service> python3 -c "import urllib.request; ..."` |
| Check compose status | `docker compose -f deploy/compose/<file>.yml ps` |
| Bootstrap lifecycle | `./scripts/bootstrap.sh up` / `./scripts/bootstrap.sh down` / `./scripts/bootstrap.sh status` |

**Key gotchas in this environment:**
- `docker cp src/. dest/` flattens directory contents — source goes into dest/ not dest/src/
- Container names vary by compose project prefix — use `--format` filters, not hardcoded names
- Single-quote Python blocks in `docker exec` — double quotes cause shell expansion of `$` and `.get()`
- Environment variables do NOT propagate through `docker exec` — pass them explicitly with `-e`
- Host shell expands variables in `sh -c` strings — use single quotes for container-internal paths
- **Bind mounts require host-resolved paths** — the Docker daemon runs on a remote VM. Use `${HOST_PROJECT_DIR}` in compose files, not `${PWD}` or container-internal paths. The bootstrap.sh auto-detects the host path via `/proc/self/mountinfo` (virtiofs translation).
- **Port forwarding through Podman VM** — ports bind to the VM IP (e.g., `192.168.127.2:8000`), not localhost. Access services via `http://<vm-ip>:<port>`.
- **DOCKER_HOST must be set** — all `docker` and `docker compose` commands require `DOCKER_HOST=tcp://<vm-ip>:2375`. The `scripts/setenv.sh` auto-detects the runtime and sets `D_HOST`.
- Settlement-net services are UNREACHABLE from test-runner by design (network isolation, not a bug)
- **Memory limits are mandatory** — every container MUST have `mem_limit` in compose files. The host has limited RAM (~18G); an uncapped container (solana-test-validator in particular) will OOM the host.

**⏸️ GATE after each batch:** Show what was implemented, show verification output, show test results. Say: *"Batch complete. Ready for feedback, or proceed to next batch?"*

**⏸️ GATE on blockers:** If a task is blocked (missing dependency, test fails inexplicably, plan instruction unclear), STOP. Do not guess or skip. Report the blocker and ask for guidance.

**⏸️ GATE when the plan is wrong:** If you've learned something that makes the remaining plan unworkable, STOP. Report what changed and why the plan needs revision.

---

### Phase 4: HARDEN — "Ship it"

**Goal:** Verify everything works, fix any issues, and present for completion.

**⏸️ GATE CHECK — Gate 2 and Gate 3 and Gate 4 must be PASS before claiming HARDEN is done.**
Before presenting HARDEN as complete, run all three:
- `./testbed.sh gate2 --spec <spec.json> --workspace /workspace`
- `./testbed.sh gate3 --spec <spec.json> --workspace /workspace`
- `./testbed.sh gate4 --workspace /workspace [--skip-up]`

If any fails, return to fixes — do not present HARDEN as done. Only when all three return `status=pass` may you proceed.

1. **Run the full test suite** — from test-runner container
2. **Run verification gates** — via `./scripts/bootstrap.sh verify` (or equivalent health + e2e gate)
3. **Run performance profile** — via `./scripts/bootstrap.sh benchmark` or latency checks from test-runner
4. **Run static analysis** — pre-commit checks (imports, lint, network isolation via `./scripts/bootstrap.sh review`)
5. **Run operational readiness checklist:**
   - [ ] Health endpoints on all services (check via `./scripts/bootstrap.sh status`)
   - [ ] Observability producing data (Jaeger traces, Prometheus metrics)
   - [ ] Verification gates pass (`./scripts/bootstrap.sh verify` scores ≥ threshold)
   - [ ] Gotchas documented somewhere findable
   - [ ] All commits pushed
6. **Write the implementation result** — `docs/sdlc/04-implementation-results/YYYY-MM-DD-<topic>.md` covering what actually shipped, actual commit hashes, test counts, deviations from plan (with reasons). See `design-impl-result-docs` skill. **MANDATORY:** This path is non-negotiable. Do NOT use a flat `docs/` path.
7. **Update INDEX.md** — Add an entry for the result document in `docs/sdlc/INDEX.md` under the Implementation Results section (View A) and the relevant feature track (View B).

**DooD-specific verification:**
- `./scripts/bootstrap.sh status` shows health of all services
- `./scripts/bootstrap.sh verify` runs health checks on all services from inside the compose network
- Both commands use the test-runner container — they verify cross-service reachability, not just individual health
- Expected: settlement-net services show as UNREACHABLE from internet-net services (correct isolation)
- Verify that new services appear in `./scripts/bootstrap.sh status` output
- Verify that `DOCKER_HOST` is correctly set and the daemon is reachable

**Artifact:** Implementation result doc + clean commit history + all gates passing (Gate 1, Gate 2, Gate 3, Gate 4).

**⏸️ GATE:** Show verification summary. Say: *"All gates passing. Ready to finish this branch?"* Reference the `finishing-a-development-branch` skill for merge/PR/cleanup options.

---

## Phase Gate Protocol (Critical)

**These rules apply in EVERY phase:**

1. **Never auto-proceed past a ⏸️ GATE** — always present the artifact and wait for human response.
2. **Artifacts before gates** — the audit matrix, design doc, plan doc, batch results, and verification summary must be PRESENTED to the human. Not just "I wrote it" but showing the content.
3. **If the human gives feedback at a gate, apply it and re-present the artifact** — do not skip to the next phase.
4. **STOP and ask on:** any failure you can't explain, any instruction you don't understand, any discovery that invalidates the current phase.

**Never implement on main/master without explicit consent. Prefer feature branches.**

## Recommended Project Structure

When setting up a new DooD + Docker Compose microservices project, follow this clean folder layout (modeled after the scdlt-x project at `/workspace/git/scdlt-x/`):

```
<project-root>/
├── scripts/
│   ├── bootstrap.sh          # Full-stack lifecycle orchestrator (up/down/status/verify)
│   ├── setenv.sh              # Runtime detection (Docker vs Podman) + DOCKER_HOST setup
│   └── <topic>/               # Domain-specific scripts (e2e/, benchmarks/, etc.)
├── deploy/
│   └── compose/
│       ├── root.yml           # Top-level compose (test-runner, tooling, networks)
│       ├── common.yml         # Shared infrastructure (networks, DNS, NAT)
│       ├── overlay.yml        # Overlay network (VPN/WireGuard peers)
│       ├── platform.yml       # Application services (databases, APIs, engines)
│       ├── observability.yml  # Monitoring stack (Jaeger, Prometheus, Grafana)
│       ├── <domain>.yml       # Per-domain compose files (one per bounded context)
│       └── overlay.*.yml      # Per-node overlay peers
├── src/
│   ├── <service>/             # Per-service source directories (one per microservice)
│   ├── test-runner/           # Test-runner container (spans all networks)
│   ├── infrastructure/       # DNS, certs, shared infra
│   └── <domain>/              # Domain-specific modules (blockchain, HSM, etc.)
├── docs/
│   └── sdlc/                  # SDLC documents (designs, plans, results)
│       ├── INDEX.md
│       ├── 02-design/
│       ├── 03-implementation-plans/
│       └── 04-implementation-results/
└── benchmarks/                # Performance benchmarks
```

**Key conventions:**
- `scripts/bootstrap.sh` is the single entry point for all lifecycle operations
- Compose files are modular and composable — each concerns a specific domain
- `src/` contains all service source code, each in its own subdirectory
- `docs/sdlc/` follows a numbered directory convention for traceability
- `HOST_PROJECT_DIR` is auto-detected by bootstrap.sh for bind mount resolution

## Pitfalls

- **Skipping Phase 0 (Audit) is the most common failure mode** — you will design something that already exists, or miss a critical constraint. Always audit first.
- **Greenfield vs brownfield confusion** — Phase 0 explicitly branches on this. If you don't check, you'll design services for infrastructure that doesn't exist yet.
- **NOT using reference skills** — This skill ORCHESTRATES other skills. When the audit identifies a need (DooD setup, multi-network, TDD for infra, etc.), you MUST use the appropriate reference skill. Do NOT reinvent solutions.
- **NOT using subagents for independent tasks** — Phase 3 requires subagents when tasks are independent. If you're manually implementing multiple independent tasks, you're doing it wrong. Use `subagent-driven-development`.
- **Skipping TDD** — Every task MUST start with a failing test. No exceptions. If a task cannot be tested, it should not be implemented. Report it as a risk.
- **Hardcoding container names** — Docker Compose auto-prefixes names with the project directory. Always discover containers by pattern, not hardcoded names. See `dood-discover-containers-by-pattern`.
- **Writing the plan before the design is approved** wastes effort on a plan for an approach that gets changed in review.
- **Not updating the design/plan after discovery** — if Phase 3 reveals something that invalidates the design, go BACK to Phase 1, don't forge ahead with a bad design.
- **Skipping verification criteria in the design doc** — without testable criteria, there's nothing to verify against.
- **Writing SDLC docs to a flat `docs/` path** — the design, plan, and result docs MUST go in the numbered `docs/sdlc/` tree (`02-design/`, `03-implementation-plans/`, `04-implementation-results/`), each registered in `docs/sdlc/INDEX.md`. A flat `docs/design.md` is wrong even for small or learning projects.
- **Testing all integrations at once instead of incrementally** — wire one, test it, fix, then wire the next.
- **Batch too large** — if a batch exceeds 5 tasks or takes more than 15 minutes, it's too large for meaningful feedback. Default is 3 tasks.
- **Shell quoting in docker exec** — single-quote the Python block, pass env vars with `-e`, avoid double quotes that trigger host shell expansion.
- **Podman VM port forwarding** — ports bind to the VM IP (e.g., `192.168.127.2`), not localhost. Access services via `http://<vm-ip>:<port>`. See `dood-port-forwarding`.
- **Bind mount path resolution** — The Docker daemon runs on a remote VM. Use `${HOST_PROJECT_DIR}` in compose files, not `${PWD}`. The bootstrap.sh auto-detects the host path via `/proc/self/mountinfo` (virtiofs translation for Podman on macOS).
- **Missing DOCKER_HOST** — All `docker` and `docker compose` commands require `DOCKER_HOST` to be set. Source `scripts/setenv.sh` or set it explicitly: `export DOCKER_HOST=tcp://<vm-ip>:2375`.
- **No memory limits** — Every container MUST have `mem_limit` in compose files. An uncapped container (especially solana-test-validator) will OOM the host. See AGENTS.md for per-service limits.

## Verification (of the workflow itself)

After applying ADD, confirm:
1. Audit matrix exists with WIRED/STUB/MISSING/BLOCKED classifications
2. Greenfield vs brownfield decision was made explicitly in Phase 0
3. Design doc exists at `docs/sdlc/02-design/YYYY-MM-DD-<topic>-design.md` with verification criteria and out-of-scope
4. Implementation plan exists at `docs/sdlc/03-implementation-plans/YYYY-MM-DD-<topic>-impl.md` with exact code and commands
5. `docs/sdlc/INDEX.md` updated with entries for all new documents (design, plan, result) in both View A and View B
5. Each SDLC doc landed in the correct numbered `docs/sdlc/` stage directory (design in `02-design/`, plan in `03-implementation-plans/`, result in `04-implementation-results/`), not a flat `docs/` path
6. Each implementation commit corresponds to a plan task (traceable)
6. Human was asked for review at every phase gate — no auto-advance
7. All verification criteria from the design doc are addressed
8. Gotchas discovered during execution are documented somewhere findable
9. For new services: network placement was documented and compose entry was created
10. `./scripts/bootstrap.sh verify` passes after completion
11. **TDD compliance:** Every task has corresponding tests that run from test-runner
12. **Subagent usage:** Independent tasks were executed via subagents with two-stage review
13. **Reference skill usage:** Appropriate reference skills were invoked (documented in plan/result)
14. **DooD environment:** `DOCKER_HOST` is correctly configured, bind mounts use `${HOST_PROJECT_DIR}`, and Podman VM port forwarding is documented
15. **Gate 4 passes:** `./testbed.sh gate4 --workspace /workspace` returns `status=pass` — stack is running, healthy, and E2E tests pass
