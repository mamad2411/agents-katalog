---
name: aoa-eval
description: Select or apply an owner-local or cross-repository eval, route a confirmed no-fit to intake/design, or classify supplied session hits as eval candidates. Do not use for central proof bundles, named results or verdicts, source-linked reports, proof lifecycle, ordinary tests, undefined invariants, or generic session harvesting.
---

# aoa-eval

## Intent

Route one evaluation need to the narrowest procedure that preserves its real
owner, input contract, output, and proof limit. Consolidation here is a shared
front door, not a collapse of five different capabilities into generic prose.

## Trigger boundary

Use this skill when:

- an eval surface must be selected or applied
- an established no-fit needs a local intake packet or a bounded suite design
- researched eval-trigger classes and supplied or retrieved session hits need
  eval-owned candidate classification

Do not use this skill when:

- the task is an ordinary test run, the invariant is still unknown, the real
  need is generic session harvesting, or the requested effect is central proof
  promotion

## Inputs

- one mode intent plus its owner, source ref, acceptance target, relevant
  evidence or inventory, effect authority, and required environment details

## Outputs

- one mode-specific result defined by `references/contract.yaml`, including
  owner, evidence class, proof limit, next route, and stop line

## Procedure

Record `<bundle_dir>` as the directory containing this loaded `SKILL.md`.

### Choose exactly one mode

| Mode | Use when | Required procedure |
|---|---|---|
| `select` | No exact evidence surface has been selected. | `references/select.md` |
| `apply` | The exact surface and acceptance contract are explicit. | `references/apply.md` |
| `local-need` | Selection proved no fit and an existing local eval port should receive pressure. | `references/local-need.md` |
| `design` | Selection proved no fit and a stable invariant needs a bounded local suite or report design. | `references/design.md` |
| `session-mining` | Prior research defined eval-trigger classes that need real session examples. | `references/session-mining.md` |

### Mode: select

Read and follow `references/select.md`.

### Mode: apply

Read and follow `references/apply.md`.

### Mode: local-need

Read and follow `references/local-need.md`.

### Mode: design

Read and follow `references/design.md`.

### Mode: session-mining

Read and follow `references/session-mining.md`.

1. Read `references/contract.yaml` and the selected mode reference completely
   before acting. Do not load unrelated mode references.
2. Read the target owner's route law and preserve source, environment,
   freshness, evidence class, effect posture, and proof authority.
3. If a required mode input cannot be obtained from permitted sources, stop as
   `blocked_missing_input`; do not guess, substitute a broader action, or
   relabel absence as an owner-boundary deferral.
   In `apply`, the mode reference's complete dotted-field preflight must be
   observed before reading or executing the selected target; a summary claim
   that the contract is complete is not a preflight.
4. Execute each chosen procedure as one task-local node and return its typed
   output. A request that explicitly asks to find and run may form
   `select -> apply` only after an exact fit provides the complete apply ABI.
   Other later modes remain explicit handoffs, never automatic continuation.
5. When the task asks what an applied observation actually constrains, hand the
   `evaluation-observation` to `aoa-verification`; do not reinterpret command
   success as proof inside this bundle.
6. When the task explicitly asks for central proof meaning, a central verdict,
   admission, or lifecycle interpretation, preserve the observation and its
   source, claim class, environment, and proof limit in a
   `central-proof-review-request`, then hand it to `aoa-evals-skills`. Do not invoke
   that owner merely because an eval ran successfully.
7. When prior-session evidence still must be found, let the session-memory
   evidence route retrieve and ground it, then consume the bounded packet here.
   The evidence route owns retrieval; `session-mining` owns eval-trigger
   classification and its local eval handoff.

## Contracts

- selection, execution, intake, design, session evidence, and proof promotion
  are different effects
- eval discovery/application and interpretation of invariant coverage are
  distinct but composable nodes
- local evidence stays local until a stronger proof owner accepts it
- Eval Forge health, command success, and generated dashboards are not result
  proof
- `.aoa` evidence is optional candidate evidence and never overrides owner
  source truth
- technique records may explain provenance but are not runtime dependencies

## Risks and anti-patterns

- choosing by keyword or replacing the selected action with a broader green
  gate
- collapsing local pressure and executable design into one vague proposal
- mining sessions before trigger classes and owner routes are known
- creating a permanent validator before manual cases establish a durable
  invariant

## Verification

- confirm one mode, exact owner/source/environment posture, required inputs,
  output type, effect, and termination condition
- inspect commands and artifacts manually against the declared acceptance
  target
- state what the result proves, what it does not prove, skipped checks, drift,
  and the next owner route

## Adaptation points

Owners supply local eval ports, schemas, command runners, artifacts, acceptance
criteria, privacy rules, session providers, and proof-promotion workflows.
