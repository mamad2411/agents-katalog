---
name: architect-propose
description: "Manual-only skill. Use only when the user explicitly invokes the architect-propose skill to turn one already approved design bundle into one new independent sealed plan package under `.architect/`. One approved design bundle may contain multiple D-xxx subdesigns, and one resulting plan may contain multiple T-xxx tasks. Do not auto-trigger from a design or implementation request."
---

# Architect Propose

Use this skill only as the manually selected `architect-propose` stage. Its job is to
store an already approved design bundle as a structured execution package and
initialize the package state and execution log. It does not redesign, implement
code, or invoke sibling skills automatically. It is stage 2 of the one-way
flow `architect-design -> architect-propose -> architect-build`.

## Defined Terms

- `approved design bundle`: the complete approved output from one
  `architect-design` invocation.
- `D-xxx subdesign`: one approved architectural decision inside that bundle.
- `independent plan`: one new future `.architect/<plan-name>/` package created
  from exactly one approved design bundle.
- `T-xxx task`: one recorded execution task inside that independent plan. A
  single independent plan may contain multiple `T-xxx` tasks derived from one
  or more approved `D-xxx` subdesigns.
- `functional boundary completion`: the packaging pass that turns approved
  design intent into target functionality, protected related functionality,
  explicit non-goals, compatibility obligations, and a hard-stop condition.
- `code impact scope`: the expected paths, symbols, configuration, tests, and
  callers likely to be affected. It is a broad execution reference, not a hard
  source modification limit.
- `functional boundary gap`: any missing target functionality, protected
  related functionality, explicit non-goal, compatibility obligation, or
  hard-stop condition that later execution would have to infer.

## Manual Invocation Only

- Run this skill only when the user explicitly asks for `architect-propose`.
- Do not auto-switch into `architect-build`.
- If planning finishes and the user wants to continue, the only forward next
  stage is `architect-build`, invoked manually by the user.

## Strict Boundary

- Create or update only `.architect/<plan-name>/` after user authorization.
- Do not edit application code, tests, runtime configuration, or unrelated
  documentation.
- Do not invent or revise a new core design unit, concept, pattern choice,
  anti-pattern, or architectural rule that changes the approved solution.
- You may add functional-boundary detail and code-impact-scope evidence when
  approved design intent is clear but later execution would otherwise infer
  protected functionality or likely affected code.
- Do not reopen, revise, or repair the approved design from this skill.
- Do not create a task that cannot cite approved `D-xxx` design units and their
  concrete rules.
- Do not seal a package while any required design input, functional boundary,
  state initialization, or log initialization is incomplete.
- Do not leave a known functional boundary gap for `architect-build` to discover
  during execution if it can be resolved from approved design, repository
  evidence, and the current request without changing the approved core design.

## Required Input

Before creating a package, require all of the following:

1. The complete approved design bundle with `D-xxx` identifiers.
2. Recorded approval evidence that covers every referenced design unit.
3. Compatibility intent, objective, functional boundary, non-goals, affected
   code impact scope, and risks.
4. A kebab-case plan name, provided by the user or safely derived from the
   approved design.
5. The user's document language, inferred from the current interaction unless
   the user explicitly requests another language.

## Core Outcome

Create one structured package that later execution can follow without
reinterpreting design intent:

- store the full approved design bundle in stable package files;
- record every approved `D-xxx` subdesign from that bundle inside the new
  independent plan;
- translate the approved `D-xxx` subdesigns into one or more atomic `T-xxx`
  tasks without adding new design decisions;
- act as a mock `architect-build` audit before sealing so every task's
  functional boundary is explicit enough to enforce without guessing;
- fill missing functional-boundary detail when it is required for build,
  consistent with the approved design, and does not alter the core architecture;
- record broad, evidence-based code impact scopes and known uncertainties so
  build can adapt them cautiously without treating them as hard limits;
- order the tasks as one complete execution sequence for one later
  `architect-build` run;
- initialize centralized task state before the `architect-build` stage starts;
- initialize the execution log before the `architect-build` stage starts;
- leave a sealed package whose content, state, and log all agree on what is
  ready to execute.

## Deterministic Package Creation

Use the Python plan tooling bundled with this skill, not manual package
creation, for all initial package structure, identifier allocation, sealing,
and final validation. The agent must not hand-create the initial package
directory tree, the initial package files, task state, or plan digest.

For this section, use these path terms consistently:

- `skill root`: the directory that contains this `SKILL.md`
- `repo root`: the target project root passed to `--repo-root`

Resolve every helper script from `skill root`, never from `repo root`, the
current workspace, or the user project tree. `--repo-root` only tells the
script which repository to operate on; it does not change where the script
itself is searched for. In this skill's native setup, the required helper
commands are:

```text
python <skill-root>/scripts/make_plan.py --repo-root <repo-root> --plan <name> --language <tag>
python <skill-root>/scripts/plan_control.py add-design --repo-root <repo-root> --plan <name> --slug <slug>
python <skill-root>/scripts/plan_control.py add-task --repo-root <repo-root> --plan <name> --slug <slug>
```

Initialize the package root with `make_plan.py`, allocate design documents and
task documents with `plan_control.py`, seal with `plan_control.py seal`, and
perform final validation with `validate_plan.py`. In another runtime, use an
equivalent repository wrapper only if it preserves the same contract.

The agent may fill only script-created files and script-created document slots.
The agent must not manually create the initial package directory tree, initial
package files, initial task state, or plan digest. Do not add or rename
fields, headings, files, identifiers, or directories manually.

If any required helper script is missing under `<skill-root>/scripts/`, stop
and report a skill installation or runtime issue. Do not search the target
repository for replacement scripts, and do not fall back to manual package
creation.

If any script or validator reports invalid UTF-8, a UTF-8 BOM, or suspicious
encoding markers, immediately correct the corrupted content and rerun the
relevant script until the package is clean.

## Package Contract

The package root is:

```text
.architect/<plan-name>/
```

For a concrete directory-level reference, inspect `templates/example-plan/`.
That example mirrors one complete sealed plan package file-for-file and
directory-for-directory, except that it lives under `templates/` for study
rather than under `.architect/` for live execution.

It must contain these artifacts:

- `00-plan-manifest.md`
- `01-context-and-contract.md`
- `02-design-catalog.md`
- `03-designs/D-xxx-<slug>.md`
- `04-impact-and-boundaries.md`
- `05-task-catalog.md`
- `06-tasks/T-xxx-<slug>.md`
- `07-verification-plan.md`
- `08-execution-log.md`
- `.state/execution-state.json`

Initialize `.state/execution-state.json` and `08-execution-log.md` as part of
package creation. The `architect-build` stage should start from these recorded
artifacts, not infer missing state from memory.

Every `03-designs/D-xxx-<slug>.md` document must preserve the approved design
contract exactly. Each design document must contain the fixed headings
`Concept`, `Intent`, `Stable Core and Variation`, `Repository Evidence`,
`Compatibility Boundary`, `Pattern Decision`, `External Evidence Decision`,
`Rationale`, `Alternatives`, `Functional Boundary`, `Code Impact Scope`,
`Verification Seams`,
`Counterexamples`, `Anti-Patterns`, and `Rules` with both `MUST DO` and
`MUST NOT DO` subsections. Populate those script-created placeholders from the
approved design bundle without inventing new structure or omitting approved
fields.

`04-impact-and-boundaries.md` must record the plan-level functional boundary,
protected related functionality, code impact scope, impact-scope audit
findings, and functional-boundary escalation readiness.

Every `T-xxx` document must state its functional boundary, a broad code impact
surface, approved subdesign and rule references, task-specific rules, atomic
steps, impact-scope adaptation rules, execution-result steps, completion
condition, and a functional-boundary escalation protocol. The protocol must
state when build stops, which analysis it presents, its recommendation, and
a problem-specific numbered set of user options, with no fixed count or predefined paths.

If packaging reveals an incomplete code impact scope, add known evidence and
uncertainty without turning the surface into a hard path limit. If it reveals a
functional boundary gap, resolve it from approved inputs when possible; do not
seal when it remains unresolved. Do not invent new core functionality or record
unapproved functionality as approved.

## Sealing and Validation

After all placeholders are filled, seal the package and validate it:

```text
python <skill-root>/scripts/plan_control.py seal --repo-root <repo-root> --plan <name>
python <skill-root>/scripts/validate_plan.py --repo-root <repo-root> --plan <name>
```

Do not redesign the package after a validation failure. Stop, inspect the
reported evidence, correct the package from approved inputs, correct any
encoding corruption immediately if reported, and validate again.

## Completion Standard

Finish only after validation succeeds. Report the package path, actual
validation result, initialized state/log artifacts, remaining risk, and whether
the user may manually invoke `architect-build` as the next stage for the
selected plan. Do not report the package as `architect-build`-ready unless the
functional-boundary audit confirms that build can enforce the approved
functionality without missing detail and has an explicit decision path for a
true runtime conflict.
