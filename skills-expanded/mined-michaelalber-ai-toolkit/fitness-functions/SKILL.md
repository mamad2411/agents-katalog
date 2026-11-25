---
name: fitness-functions
audience: team
description: >
  Author architectural fitness functions and wire them into a target project's CI as
  gatekeepers. Use for "add a fitness function", "wire an arch test as a CI gate", "enforce
  layering in CI", "fail the build when the dependency rule is violated". Per-stack tool selection
  (NetArchTest, import-linter, cargo-deny, Conftest). Do NOT use to run an existing test suite --
  that is tdd-loop. Do NOT use to analyze coupling for insight without gating -- that is dependency-mapper.
---

# Fitness Functions

> "An architectural fitness function provides an objective integrity assessment of some
> architectural characteristic(s)."
> -- Neal Ford, Rebecca Parsons & Patrick Kua, *Building Evolutionary Architectures*

## Core Philosophy

A fitness function turns an architectural intention into an automated, objective check that the CI
pipeline enforces on every push. It is the executable memory of an ADR: the ADR records *why* a
boundary exists; the fitness function makes crossing that boundary *fail the build*. Without the
gate, architectural decisions decay silently between reviews. The mechanism is uniform across
stacks -- a check wired into CI as a gatekeeper -- but the tool is per-stack.

**Non-Negotiable Constraints:**
1. A fitness function is a GATE, not a report -- it exits non-zero and fails CI on violation; a
   check that only prints is not a fitness function
2. TRACEABLE -- every fitness function names the ADR or measurable quality attribute it enforces;
   no orphan checks
3. PROVE it gates -- pass against today's code AND fail against a deliberate violation before you
   declare it done; an untested gate is assumed broken
4. PER-STACK tool, uniform mechanism -- load `references/<stack>.md`; never hardcode a stack's
   tooling into the gate-wiring logic
5. CONTEXT BUDGET: keep utilization under 40%. At 60%, write progress to the target's
   `architecture.md` fitness section and tell the user to start a fresh session.

## Workflow

```
PRE-FLIGHT
    [ ] Identify the target stack (dotnet|python|rust|policy) from architecture.md/the ADRs, or ASK
    [ ] Locate the CI workflow file (.github/workflows/*, .gitlab-ci.yml, etc.)
    [ ] Identify the ADR or quality attribute each fitness function will enforce

SELECT
    Load references/<stack>.md and choose the tool for the rule category (layering/dependency
    direction · coupling · dependency policy · coverage · package rules). For coupling-as-metric,
    reference dependency-mapper (Martin Ca/Ce/I/A/D) rather than re-deriving the math.

AUTHOR
    Write the check as an executable artifact in the target repo (a test, a contract, a policy
    file). It must read the real source/build graph and exit non-zero on violation.

WIRE
    Add the check to the CI workflow as a required step/job that blocks merge on failure.
    Comment the step with the ADR id / quality attribute it gates.

VERIFY
    1. Run it against current code -- must PASS (green)
    2. Introduce a deliberate violation -- must FAIL (non-zero) -- then revert. Observe both.

REPORT
    Each fitness function · the ADR/attribute it gates · CI step location · the violation proof.
```

**Exit criteria:** >= 1 fitness function authored in the target repo; wired into CI as a
merge-blocking gate; verified GREEN today and verified to FAIL on a deliberate violation; each gate
traces to a named ADR or quality attribute.

## State Block

```
<fitness-functions-state>
phase: PRE-FLIGHT | SELECT | AUTHOR | WIRE | VERIFY | REPORT | COMPLETE
target_stack: dotnet | python | rust | policy
ci_workflow: [path to the CI file the gate is wired into]
fitness_functions: [count]
gates_on: [ADR ids / quality attributes enforced]
wired_as_ci_gate: true | false        # MUST be true to COMPLETE
verified_fails_on_violation: true | false   # MUST be true to COMPLETE
context_budget: under-40 | approaching-60 | checkpoint-now
status: in_progress | complete
</fitness-functions-state>
```

## Output Template

See `references/<stack>.md` for the per-stack tool, a minimal check, the CI-wiring snippet, and the
deliberate-violation proof: `dotnet.md` (NetArchTest), `python.md` (import-linter), `rust.md`
(cargo-deny + dependency-direction test), `policy.md` (Conftest/OPA Rego).

## Integration with Other Skills

| Skill | Relationship |
|-------|-------------|
| `qraspi-architecture` | Specifies which fitness functions each ADR requires; this skill authors them. |
| `qraspi-skeleton` | Lands these fitness functions as CI gates when the walking skeleton stands up. |
| `dependency-mapper` | The ready-made coupling fitness function -- Martin Ca/Ce/I/A/D metrics. Reference it for coupling rules rather than re-deriving the math. |
| `tdd-loop` | Different layer: `tdd-loop` gates *behavior* (does the code do the right thing); a fitness function gates *architecture* (is the structure still legal). Do not conflate. |
