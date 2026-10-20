---
name: quality-gates
description: "Entry-point quality gate for AI-assist work. Classifies the request mode (build/troubleshoot/explore/review), assesses project state (greenfield/brownfield), runs Gate 1 foundations (spec, PRD, INFRA, AGENTS) with user signoff, then triggers the four gates change-driven (not sequential). Hand off to add-audit-driven-delivery for build work after the foundation decision."
---

# Quality Gates (Gate-First, Change-Driven)

This skill is the front door for AI-assist work. It decides what kind of work is being asked, establishes the project foundation when needed, and triggers only the quality gates that the change demands. It is not a delivery pipeline; it is the entry point and the quality gate.

## When to Use

Use this skill at the start of any AI-assist task:

- Building or implementing a feature
- Troubleshooting a problem
- Exploring or analyzing an area
- Reviewing code or a change

**Do NOT use** as the primary driver for implementing phases or building large feature sets. That is `add-audit-driven-delivery`. This skill establishes the foundation and gates the work; ADD does the building.

## Entry: Classify the Request Mode

The first step is to classify the request into one of four modes. The mode determines everything that follows.

| Mode | Example phrasing | Gate 1 (foundations) needed? |
|------|------------------|------------------------------|
| **build** | "implement feature x", "add a service", "build phase 3" | Yes, if greenfield |
| **troubleshoot** | "troubleshoot xxx", "why is y failing" | No |
| **explore** | "let's explore feature y", "analyze the architecture" | No |
| **review** | "review this PR", "check this diff" | No |

**ALWAYS confirm the mode with the user before proceeding.** This is a hard gate. Do not assume the mode from phrasing alone. Ask a polite confirmation, for example:

> "I read this as a build task. Before I start, I want to audit the environment to see where this feature fits. Shall I proceed with the audit?"

If the user corrects the mode, re-classify and re-confirm.

## Mode-Specific Entry Paths

### Build

1. **Ask to audit the environment** where the new feature can fit. Confirm before starting the audit.
2. **Assess project state** (greenfield vs brownfield, below).
3. If greenfield, run **Gate 1 foundations** (below), get signoff, and present the continue-or-stop decision.
4. If brownfield, run **change-driven gate triggering** (below) based on what changed.

### Troubleshoot

1. **Study the knowledgebase first.** Search for the symptom to see if this is a common or pre-existing issue. If a known fix exists, apply it for fast resolution.
2. If it is not a known issue, **do a quick check on the specific area** to build context: read the relevant code, config, and logs.
3. **Build enough context before running the `systematic-troubleshooting` skill.** Do not call it cold. The skill works best when the agent already knows the contradiction to state.
4. After a fix, run Gate 4 to verify the stack still works.

### Explore

Analysis only. No foundations, no gates. Produce the analysis and stop.

### Review

Code review. Use the `code-reviewer` skill. No foundations.

## Project State Assessment

Determine whether the project is greenfield (nothing yet) or brownfield (mid-way).

**Default detection:** if a spec, PRD, INFRA, or AGENTS file exists, OR compose/bootstrap/scripts exist, treat it as brownfield. If none exist, treat it as greenfield.

**User override:** if the user explicitly says the project is greenfield, ignore the existing PRD/INFRA/AGENTS or compose/bootstrap/scripts and treat it as greenfield.

## Gate 1: Foundations

Gate 1 is the foundations gate. It produces the artifacts that anchor the project and gets user signoff.

1. **Write the spec** as JSON. It encodes the audit findings, service descriptions, guardrails, and verification criteria.
2. **Write the PRD** (product requirements).
3. **Write the INFRA** (infrastructure and service definitions).
4. **Write the AGENTS guardrails** (behavioral rules for the agent).
5. **Validate the spec** via Gate 1 (below). Apply the returned actions until `status=pass`.
6. **User signoff.** This is a hard gate. Present the spec, PRD, INFRA, and AGENTS, and wait for explicit approval.
7. **Present the continue-or-stop decision.** This is a hard gate. Ask the user whether to continue with ADD delivery or stop with the foundation locked in.

If the user stops, the foundation is a complete deliverable. The project can be resumed later.

## Change-Driven Gate Triggering

For brownfield projects, the gates are triggered by what changed, not by a fixed sequence. The skill compares the current state to the last gate pass and runs the union of gates whose trigger conditions match.

| Gate | Trigger condition |
|------|-------------------|
| Gate 1 (Foundations) | Spec / PRD / INFRA / AGENTS changed |
| Gate 2 (Implementation) | Compose, Dockerfile, config, test, or script changed |
| Gate 3 (Security/Policy) | Privileges, volumes, env/secrets, network_mode, ports, or npm deps changed |
| Gate 4 (Runtime/Integration) | Services changed, or a "done" claim is being made |

A config-only change triggers Gate 2 + Gate 4 but not Gate 1 or Gate 3. A security change triggers Gate 3 alone. The sequence is whatever the change demands.

## The Four Gates

| Gate | What it validates | When it must pass |
|------|-------------------|-------------------|
| Gate 1 | The spec is internally consistent and grounded in the KB | Before any code is written; when foundations change |
| Gate 2 | The implementation matches the approved spec; **unit tests pass** | After every implementation batch |
| Gate 3 | Security and policy guardrails hold | Before HARDEN, and after any security-relevant change |
| Gate 4 | The stack is running, healthy, and **E2E tests pass** | Before HARDEN, and after any service-affecting change |

**Test ownership is split by gate.** Gate 2 owns the **unit tests** (fast, no live services). Gate 4 owns the **E2E tests** (live stack, `live` marker, hits real services). The E2E test suite belongs to Gate 4, not Gate 2. Gate 2 does not validate or run the E2E suite; Gate 4 does.

### Gate 1 — Spec Validation

```bash
./testbed.sh validate /workspace/<name>-spec.json
```

### Gate 2 — Implementation Validation (unit tests)

```bash
./testbed.sh gate2 --spec /workspace/<name>-spec.json --workspace /workspace
```

Gate 2 validates the implementation against the spec and runs the **unit** test suite. It does not run the E2E suite; that belongs to Gate 4.

### Gate 3 — Security & Policy Guardrails

```bash
./testbed.sh gate3 --spec /workspace/<name>-spec.json --workspace /workspace
```

Gate 3 includes an npm supply-chain scan for known vulnerable packages (keyv, cacheable-request, cacheable-lookup), added after the Keyv supply-chain attack. It also enforces memory limits on every container.

### Gate 4 — Runtime & Integration Verification (E2E tests)

```bash
./testbed.sh gate4 --workspace /workspace [--skip-up] [--e2e-timeout N]
```

**CRITICAL:** always bring the stack up with `bootstrap.sh up`, never raw `docker compose up -d`. The bootstrap script copies configs, syncs test files, and sets the compose project name. Raw compose misses all of that.

Gate 4 runs the **E2E** test suite (the `live`-marked tests) against the running stack. The E2E suite is owned by Gate 4, not Gate 2.

#### Test-Runner Decision (how the E2E test runs)

There are two ways Gate 4 can run the E2E test. Pick one explicitly; do not guess.

1. **Test-runner container** (SCDLT pattern). A `test-runner` service in the compose runs the E2E happy-flow test from inside the compose network, reaching services by internal name. Use this for larger projects where the E2E test must reach services by internal name.
2. **Direct host run** (small projects). Run the E2E test directly on the host with pytest and the `live` marker, hitting the published ports. No test-runner container is needed.

**Decision rule:** for small projects (a few services, the E2E test hits published ports), remove the test-runner and run the E2E test directly on the host. For larger projects where the E2E test must reach services by internal name, keep the test-runner. This is an explicit decision, not a guess. When in doubt, ask the user which pattern they want.

#### Callflow Verification (inter-component contracts)

The E2E happy-flow is a black-box check: it proves the final user-visible result. It does not prove that each inter-component call follows the correct contract (right target, right payload, right order). A wiring error can pass a naive E2E and only surface once the whole app is assembled.

Gate 4 therefore also walks the spec's `callflow` section: each declared edge is a directional call (source → target) with an expected result, verified before the E2E happy-flow runs. It follows the declare-don't-execute rule:

1. **The spec declares the callflow as data.** An edge names the source, target, a protocol discriminator (`http`, `verify-hook`, ...), the request, and the expected result (`mode: exact | contains | success | verify_hook`).
2. **An adapter executes each edge.** A protocol adapter knows HOW to make the call. `http` does a real HTTP request to the target's published port and compares the body/status against the expected result. New protocols register adapters; they never change the spec schema.
3. **verify_hook handles non-request/response flows.** Async events, eventual consistency, DLT state transitions, side effects. The spec points at a project-owned checker script; the gate runs it and reads the exit code / failure reason.
4. **Gate 2 statically validates the callflow shape.** Edge ids are unique, all referenced services exist, http edges carry method+path, and a verify_hook points at an existing file. This is cheap and runs before any code, so a bad contract is caught at its source.

Run a callflow check during EXECUTE too: right after wiring a component pair, bring up just that pair and verify the single directional call. This catches a broken A→B link when it is cheapest to fix, before the full app is assembled. Waiting until Gate 4 (full stack) reproduces the late-fix problem.

Case-study example (`consumer->api.items`): the consumer's call to `GET /items` must return exactly the three catalog items. If the API returns the wrong shape or the consumer hits the wrong endpoint, the callflow edge fails with a per-edge diagnostic naming the caller, the callee, and the actual vs expected result.

```bash
./testbed.sh gate4 --workspace /workspace
```

## How to Consume Gate Feedback

- `status == "pass"` means you may proceed. Still read the warnings.
- `status == "fail"` means treat `actions` as your to-do list. Each action is specific (field path plus suggested change). Apply them, fix the artifacts, re-run.
- Pass `attempt_number` and `previous_summary` on consecutive calls so the feedback reads like a conversation, not a reset.
- The revision protocol is identical for all gates: read → apply → re-run → repeat until `status == "pass"`.

## The Decision Rule When a Gate Reports a Mismatch

Do not blindly fix the implementation to match the spec. The spec is the designed source of truth, but implementation discoveries should feed back into the spec.

- If the implementation is wrong (typo, missing file, wrong port), fix the implementation.
- If the spec is wrong (a healthcheck command that does not exist in the image, a port that does not match the service), update the spec and re-run Gate 1.
- The Dockerfile and the running container are the ground truth for what a container can do.

## Handoff to ADD

When the user chooses to continue with delivery, hand off to `add-audit-driven-delivery` with a context bundle:

- The validated spec
- The PRD, INFRA, and AGENTS
- The project state (greenfield/brownfield)
- The gate state

**ADD skips its Phase 0 audit** when called by this skill, because the state assessment and foundations are already done. ADD starts at Phase 1 DESIGN using the validated spec as input. ADD's Phase 0 remains for the standalone case where ADD is called directly without this skill.

## State File Mechanism

Change detection works with or without git. A state file at `.ai-assist/gate-state.json` records, per gate pass, a hash snapshot of the file groups each gate validates.

```json
{
  "project_state": "brownfield",
  "last_gate_pass": { "gate1": "...", "gate2": "...", "gate3": "...", "gate4": "..." },
  "snapshot": {
    "spec": "<hash>", "prd": "<hash>", "infra": "<hash>", "agents": "<hash>",
    "compose": "<hash>", "dockerfiles": "<hash>", "configs": "<hash>",
    "tests": "<hash>", "scripts": "<hash>", "security_relevant": "<hash>"
  }
}
```

On each invocation:

1. Load the state file (if it exists).
2. Recompute the current hashes of the relevant file groups.
3. Compare to the snapshot to determine what changed.
4. Trigger the gates whose file groups changed.
5. On a gate pass, update the snapshot and `last_gate_pass`.

Git diff is the richer signal when git exists; the state file is the source of truth for triggering either way. Git is not mandated.

## Post-Implementation: Sync Documentation

After the relevant gates pass and implementation is complete, sync the main documentation files to the deployed state. Docs drift is a quality failure.

| File | What to sync |
|------|-------------|
| `README.md` | Project overview, service list, architecture, quick-start |
| `PRD.md` | Testbed infrastructure tables, design decisions, test scenarios |
| `INFRA.md` | Service definitions (images, ports, healthchecks, networks, build contexts, env vars), test suites, guardrails |

For each deployed service, verify the docs reflect the actual image, ports, healthcheck command, networks, memory limits, build context, env vars, and container name. Move non-deployed services to a "Next Steps" or "Future Phases" section.

## Pitfalls

- **Skipping the mode confirmation.** Always confirm the mode with the user before proceeding. Do not assume from phrasing.
- **Running the gates sequentially by default.** The gates are change-driven. Run only the gates whose trigger conditions match the change.
- **Writing the spec after the code.** Gate 1 is meant to drive the work. Write the spec before code so it guides, not validates.
- **Running the gates only at the end.** Run them throughout, so problems are caught early.
- **Calling systematic-troubleshooting cold.** Build context first: study the KB, then check the specific area, then call the skill.
- **Floating image tags** (`latest`) are acceptable for prototyping but pin versions before production.
- **Missing healthchecks and missing memory limits** are common blockers or strong warnings.
- **Every service needs a `description` field** — this forces you to justify why it exists.
- **PYTHONPATH must be set.** Use `./testbed.sh` (wrapper script) or `export PYTHONPATH=/project/tooling` before running commands.
- **pip install is blocked** by PEP 668. Use `--break-system-packages` or set PYTHONPATH instead.
- **Healthchecks must use commands available in the container image.** Flask containers (`python:3.12-slim`) do not have `curl` — use `python3 -c "import urllib.request; ..."` instead.
- **`scripts/setenv.sh` must be kept in sync with the compose project name.** If the compose file changes `name:`, update `COMPOSE_PROJECT_NAME` in `setenv.sh` too.
- **Docs drift is a quality failure.** If the `.md` files do not match the deployed compose, the implementation is incomplete.

## Verification

After reaching `status=pass` on a gate:

1. Review all warnings — they indicate non-blocking issues.
2. Verify the artifacts match the spec on every checked field.
3. Verify no secrets leaked into environment variables.
4. Verify no Docker socket mounts or sensitive host paths.
5. Verify no known vulnerable npm packages.
6. Verify the stack is running with the expected container count.
7. Verify `bootstrap.sh verify` passes cleanly.
8. Verify the E2E happy-flow test passed (if the file exists).

After syncing documentation:

1. Verify every deployed service appears in each `.md` file.
2. Verify healthcheck commands match the deployed compose (not theoretical).
3. Verify non-deployed services are in a "Next Steps" / "Future Phases" section.
4. Verify port mappings, networks, memory limits, and build contexts match the compose file.
