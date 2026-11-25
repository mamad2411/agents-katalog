---
name: wbs-prd
description: >-
  Use this skill when starting a new project, feature, or module — before any code is written. Relentlessly interviews the user about functionality, observable results, evidence, priorities, constraints, and failure behavior, then compiles those requirements into a WBS-compatible .wbs/tree.yaml and .wbs/context.md ready for wbs.py to execute. Triggers on: "spec this out", "plan this", "I want to build", "grill me on this", "PRD this", "generate the WBS", "create the tree", "scaffold the tree", "let's plan before we build", or any request to capture requirements before coding.
---

## Gotchas

- Do NOT write `tree.yaml` until grilling is complete. Synthesis is pure transformation — don't blend extraction and writing.
- Decompose to **work_package** level only. Task and step nodes are for execution time via `wbs.py decompose`. Over-specifying upfront wastes effort on decisions that change.
- Every leaf node needs at least one `acceptance_criteria` item. Vague or missing criteria make "done" undefined — `wbs.py validate` will reject leaves without them.
- Dependencies must reference node IDs that exist elsewhere in the same tree. Resolve the order of nodes before writing.
- Tech stack and conventions belong in `.wbs/context.md`, not in node `constraints`. Node constraints are functional (what the node must/must not do), not environmental.
- If `.wbs/tree.yaml` already exists, read it and ask whether the user wants to replace the existing specification or incorporate new requirements. Never silently overwrite. When revising, first ask: "What did we learn since the last version that changes the *problem*, not just the plan?" Log the answer in context.md — partial builds reveal problem dimensions the original grilling couldn't see.
- `--tree` is a global flag in `wbs.py` — it goes **before** the subcommand: `wbs.py --tree path/tree.yaml validate`, not `wbs.py validate --tree path/tree.yaml`.
- For deep trees, run `wbs.py show <id>` after `next` to get the full parent chain — `next` only returns the immediate parent's intent.
- A vertical outcome contained within one delivery branch needs no special machinery. Add the optional top-level `proof_slice` only when the smallest architectural proof crosses delivery-branch ownership boundaries (whether features or capabilities); it is one temporary execution gate, not another hierarchy.
- Keep the three units distinct: a leaf/work package is an agent execution unit; an outcome-bearing feature branch is a delivery and integration unit; a Proof Slice is a cross-branch authorization unit. Do not flatten all three into generic "work units."
- Every outcome-bearing feature branch needs an explicit tracer work package (normally `{FEATURE}-E2E`). It depends on the branch leaves whose interfaces compose the outcome and verifies the branch through its real entry and exit boundaries. A parent node's completion propagation does not run parent-level `verify`, so acceptance criteria alone are not a substitute for this leaf.
- Keep branch, work-package, dependency, tracer, and Proof Slice design out of the user-facing interview. First capture functionality and evidence; derive the technical representation during synthesis using `references/intake-to-wbs.md`.
- Proof members must be leaf IDs and dependency-closed. Never add fake `sequence` edges merely to force product priority.
- Run `wbs.py validate` before reporting success. A tree the validator rejects is not done.

---

## Phase 1: Grilling

Interview me relentlessly about the product's required behavior and observable results. Stay in the user's problem language; do not walk them through the WBS hierarchy or ask them to design its implementation representation.

**Ask one question at a time.** Wait for the answer. Asking multiple questions at once is bewildering.

**For each question, give your recommended answer.** The user reacts to a concrete proposal rather than generating from scratch. This surfaces disagreement faster and moves sessions forward.

**If a question can be answered by exploring the codebase, explore the codebase instead of asking.**

### Question sequence

Read `references/intake-to-wbs.md` before interviewing. Maintain its outcome-requirement ledger as requirements become clear.

**Purpose and scope**
- What is the single-sentence objective? What problem does this solve and for whom?
- Who acts, and who receives or observes the result?
- What is the unifying mental model — the one coherent story this product tells? Every required result must map to it; this becomes `## Core Design Concepts` in context.md and an integrity check at synthesis.
- What existing system is this most like, and where does it deliberately differ? A good exemplar imports a proven decomposition for free.
- What is the second-most-viable overall approach, and why isn't it the one? Record the rejected path and one-line rationale — it goes in `## Design Alternatives` in context.md.
- What is explicitly out of scope? Name it — it becomes root-level constraints.
- What observable result would make the whole product successful?

**Functional journeys and results**
- What does each actor need to accomplish, starting with the trigger and ending with the result they can observe?
- What information enters the behavior, what state changes, and what comes back?
- What must happen before or after from the actor's perspective?
- Which independently useful result should work first, before broader investment?

**Evidence and failure behavior**
- What demonstration, test, measurement, or artifact would convince you each result is real?
- What invalid, unavailable, duplicate, unsafe, or partial conditions matter, and what should the actor observe in each case?
- What is the riskiest product or integration assumption, what result would test it, and what evidence would cause us to revise the plan?
- After that evidence exists, what decision should be made: revise the requirements or approve broader implementation?

**Priority and boundaries**
- Which results are required now, which are later, and which are explicitly out of scope?
- Are there deadlines, irreversible decisions, migration needs, or compatibility promises that affect sequencing?
- Which external behavior may still change, and who would be affected if it does?

**Operating constraints and existing context**
- Are any technologies mandated or prohibited because they affect the product, its users, or operating constraints? Otherwise derive the stack from the repository and confirmed requirements.
- What existing system, data, workflow, or contract must be preserved or integrated?
- Hard non-functional constraints: performance targets, security requirements, compliance obligations?
- What organization-wide quality evidence must pass before any result is accepted (test suite, lint, typecheck, review, or measurement)?

**Stop when** every required-now result has an actor, trigger, observable success, acceptance evidence, material failure behavior, priority, constraints, and explicitly recorded open assumptions. Technical fields may still require synthesis; do not interrogate the user merely to eliminate implementation uncertainty.

**Outcome contracting point** — before synthesis, present the outcome-requirement ledger: functionality, observable evidence, priority, constraints, exclusions, and open assumptions. Get explicit confirmation that it represents the requested product. Do not present branches, work packages, tracers, or Proof Slice topology yet.

---

## Phase 2: Synthesis

Read `references/intake-to-wbs.md` and `references/node-schema.md` now. The first defines how to compile confirmed outcomes into technical structure; the second defines the output contract.

Do NOT re-interview. Synthesize only from what was established in the grilling session.

1. Check whether `.wbs/tree.yaml` exists. If yes, read it and confirm with the user before proceeding.
2. Create `.wbs/` directory if it doesn't exist: `mkdir -p .wbs`.
3. Compile the confirmed outcome ledger into capabilities, outcome-bearing delivery branches, supporting nodes, work-package leaves, genuine dependencies, and traceability using `references/intake-to-wbs.md`. This is internal reasoning, not a second interview. Inspect the repository to resolve technical structure; record consequential assumptions instead of silently treating them as user requirements.
4. Write `.wbs/tree.yaml` with the compiled tree. Include the full `meta` section: `project`, `version: "0.1.0"`, `prd_source: "conversation"`, `execution_strategy: proof_slice_first` (the default; use `legacy_bottom_up` only when the user explicitly selects it), `tech_stack` (from confirmed constraints or repository evidence), `conventions: "See .wbs/context.md"`, and `verify` (the Definition-of-Done commands — `wbs.py done` runs them on every completion). Set all node statuses to `pending`. Give every node `source_requirements`; a structural node may instead explain in `notes` which delivery branches it enables. Give every leaf a `verify` entry: one command that runs that node's tests (path per the test-file convention in context.md).
5. For every outcome-bearing delivery branch, add one explicit tracer leaf derived from its requirement evidence. Confirm its acceptance criteria describe the observable result, its `verify` command runs through real boundaries, and its dependencies cover the interfaces being composed. Internal leaves may be built bottom-up; the tracer is the integration gate.
6. Map the first architectural proof. If one branch tracer supplies it, rely on normal traversal and omit `proof_slice`. If it crosses delivery branches, add the optional top-level `proof_slice` defined in `references/node-schema.md`: use the minimum dependency-closed set of leaf IDs—including the cross-branch tracer—one end-to-end `verify` command, and status `pending`.
7. Write `.wbs/context.md` with: outcome requirements, tech stack, conventions, core design concepts, design alternatives, delivery branches and interface maturity, architecture notes, integration points, non-functional requirements, open questions, and—when configured—a concise `## Proof Slice` summary. Follow `references/node-schema.md`.
8. Integrity check against the compilation invariants in `references/intake-to-wbs.md`. Cut or merge technical structure that maps to no requirement or enabling need; do not invent product scope to justify it.
9. Present the mapping review defined in `references/intake-to-wbs.md`. Ask the user to confirm functionality coverage, evidence, priorities, assumptions, and scope—not to design the WBS. Incorporate corrections before final validation.
10. Run `wbs.py validate`. Fix any errors before continuing.
11. Run `wbs.py status` and show the user the result — total nodes, structure, proof-slice status if present, and what's next.

### Node ID convention

| Level | Pattern | Example |
|---|---|---|
| product | `ROOT` | `ROOT` |
| capability | `CAP-{DOMAIN}` | `CAP-AUTH` |
| feature | `{DOMAIN}-{FEATURE}` | `AUTH-MAGICLINK` |
| module | `{DOMAIN}-{FEATURE}-{MODULE}` | `AUTH-MAGICLINK-TOKENS` |
| work_package | `{DOMAIN}-{FEATURE}-{UNIT}` | `AUTH-MAGICLINK-API` |
