---
name: 1-grow
description: Research, clarify, shape, and approve an implementation-ready IP and task list. Use whenever the user asks to plan, shape, spec, or scope substantial work ("help me plan X", "how should we build Y") or to revise an existing plan; not for implementation or PR operations.
---

# Grow — shape

Turn a request, ticket, or specification into approved artifacts a fresh Pick agent can
execute without conversation history.

Read the shared [`lifecycle contract`](../../references/lifecycle-contract.md),
[`documentation contract`](../../references/documentation-contract.md),
[`PR deployments`](../../references/pr-deployments.md), and
[`grilling procedure`](references/grilling.md) before acting. Follow grilling for every
human decision until the answer is executable.

## Preconditions

- A request/spec/ticket and repository are available.
- This invocation owns shaping only. After `PASS`, Pick and Roast run the inner loop.

## Inputs

- Request/spec/ticket and linked context
- Existing IP/task files, if revising
- Repository instructions, code, tests, history, and available project skills
- Execution state and prior result, when present

## Procedure

1. **Reconstruct.** Resolve the repository's existing IP/task conventions from its
   instructions and nearby artifacts. If none exists, choose a colocated IP/task pair,
   record the new convention, and avoid creating a shared mutable index. Read prior state
   and verify it against repository reality.
2. **Read architecture docs.** Load the repository's architecture, domain, and operator
   docs for the affected area. Treat them as the current design. If docs are missing or
   contradict the code, the IP must resolve that in this invocation.
3. **Discover supporting skills.** Inspect available repository/project skills and load
   those relevant to the affected domains, including documentation skills. Record
   selected skills for downstream stages.
4. **Research before asking.** Classify uncertainty:
   - **Human decision:** product, architecture, security, data ownership, compatibility,
     rollout, destructive change, or scope → grill and block until answered.
   - **Discoverable fact:** repository convention, library behavior, ownership, tests →
     investigate it.
   - **Low-risk implementation detail:** strongly implied by convention → choose it and
     record the assumption.
5. **Grill.** Follow the grilling procedure. Work the current decision frontier in rounds
   of selectable options with a recommended default, using the harness's structured
   question tool when it has one. Get to the bottom of each reply: vague,
   partial, or conflicting answers stay on the frontier. Wait for explicit
   shared-understanding confirmation before writing. Every wait-for-human or done
   message closes with PR deployment URLs when a PR has them.
6. **Shape.** Prefer contracts/models/APIs before implementation detail where applicable.
   Define scope, non-scope, architecture decisions, risks, human gates, rollout, and
   dependencies.
7. **Specify proof.** Make every acceptance criterion observable and pair it with a
   verification method (test, build, runtime/API/database probe, UI exercise, artifact,
   compatibility/regression case).
8. **Write.** Produce the IP and a dependency-aware tracer-bullet task list. Each task
   names files/seams, acceptance criteria, blockers, verification, docs to create or
   update, and relevant supporting skills when discoverable. Docs updates follow the
   documentation contract and are not deferred.
9. **Approve.** Post the standalone approval brief from grilling: an orientation
   paragraph on where the repository is and where this change takes it, optional
   background on current state, the idea, the plan, then the unbounded Decisions table
   pairing each settled human decision with the question that prompted it. Skip that
   table when grilling settled none. The brief must be readable without the IP, the
   ticket, or the grilling history. Set the repository's approved status only after human
   confirmation. Update execution state and emit the stage result collapsed per the
   lifecycle contract.

## Supporting skills

Follow the shared discovery procedure. Supporting skills may cover API/UI architecture,
data access, schemas, prompts, deployment, testing, or safety. Names are repository-defined;
none is universally required.

## Evidence produced

- Approved IP path and task-file path
- Standalone approval brief: orientation paragraph, background when needed, idea, plan
- Research findings and recorded assumptions (not chain-of-thought)
- Decision log/human gates, listed in full with their prompting questions when any exist
- Acceptance-criterion → verification mapping
- Selected supporting skills
- Docs files named on each task
- Updated execution state and structured Grow result

## Success conditions

- IP/task artifacts are approved, implementation-ready, dependency-aware, and testable.
- A fresh Pick invocation can identify the next unblocked task, applicable criteria,
  decisions, supporting skills, and risks from durable artifacts.
- A reviewer with no prior context can approve or push back from the brief alone.
- Emit `PASS` with `next: pick`.

## Failure conditions

Malformed or contradictory artifacts emit `FAIL` with exact defects,
`next: grow`, and a focused Grow retry. Do not pass incomplete criteria
to Pick.

## Blocked conditions

Unresolved human decisions, unavailable required evidence/access, or unsafe ambiguity emit
`BLOCKED` with `next: null`, options, tradeoffs, and a recommended
default when appropriate.

## Recommended next stage

- `PASS` → Pick
- `FAIL` → Grow with defect evidence
- `BLOCKED` → outer loop routes the named human/external gate
