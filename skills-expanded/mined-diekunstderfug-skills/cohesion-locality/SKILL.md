---
name: cohesion-locality
description: >-
  Designs and reviews code boundaries using cohesion, change locality,
  and shared invariants. Use while designing or implementing features when
  deciding module/class/function responsibilities, code placement, ownership
  of rules/state/lifecycles, or whether to extract or share a helper—even before code exists
  and without an explicit review request. Also use for split/join/move decisions,
  over-splitting, shrinking files, one-class-per-file, catch-all modules,
  Manager/Helper classes, or misplaced knowledge. Public-surface complexity
  and dependency review belong to modularity-review. Skip routine local edits
  that do not involve a responsibility or ownership choice—including executing
  an extraction, split, or move the user has already decided.
metadata:
  targets: [claude, cursor, codex, agents]
---

# Cohesion and Locality

Help the user find boundaries that make code easier to understand, change, and debug. Prefer cohesive units over merely small units. Keep knowledge and behavior together when they share a meaningful invariant, contract, lifecycle, or reason to change; consider separating independent responsibilities when that improves locality.

These are design principles, not a prescribed architecture. Adapt their application to the code, language, project constraints, and requested depth. Exploration can use tentative scenarios and alternative boundaries; a confident recommendation needs stronger support than an exploratory idea.

## Core vocabulary

- **Cohesion:** how strongly code belongs together through shared knowledge, a meaningful invariant, contract, lifecycle, or reason to change.
- **Owner:** the conceptual home responsible for a rule, authoritative state, or work and cleanup. Shared entity names and team boundaries alone do not establish ownership.
- **Change axis:** a separately governed policy or contract that can evolve independently; different steps or verbs do not by themselves imply different axes.
- **Locality:** how much knowledge, editing, coordination, and verification a change or failure requires across the codebase.

These concepts apply to functions, classes, files, and packages. Use the project's terminology where it is more precise. The query's language carries no structural signal: judge the same code the same way regardless of the language it is asked in, and respond in the user's language.

## Choose the useful detail

The main agent first reads the root and nearest applicable `AGENTS.md`, relevant architecture/ADR guidance, and the applicable project-local `SKILL.md` files identified from their descriptions. Use those rules to guide both design and review; forwarding unread paths to a reviewer is not a substitute. For specialized review required by a project skill, the main assigns one dedicated fresh-context reviewer for that domain and scope, reusing an existing assignment if present; that reviewer reads the source rules itself and returns evidence without further delegation.

Read this entrypoint in full whenever the skill applies, including its core principles and all judgment aids, during design as well as review. Apply them with judgment rather than as a prescribed checklist. Detailed references and examples are supplementary: consult them when a boundary is uncertain or additional explanation would help; examples are not required design inputs.

Start with the requested unit or proposed feature, its requirements and contracts, and relevant existing code when available. Use the following references when their detail helps; read the relevant section rather than loading the whole reference set. A straightforward judgment can finish from this entrypoint. For a nontrivial case, start with the most relevant reference; another is useful only if a different question remains. The review checklist is optional, not a prerequisite for every review.

| Current question | Reference |
| --- | --- |
| How to inspect, explore alternatives, challenge a cut, or report a finding? | [Review and exploration](references/review-checklist.md) |
| Does this function mix concerns, or is it cohesive orchestration? | [Function design](references/unit-boundaries.md#function-design) |
| Do this class's state, collaborators, and lifecycle belong together? | [Class design](references/unit-boundaries.md#class-design) |
| Split this file, move helpers, or reorganize a package? | [File design](references/unit-boundaries.md#file-design) and [package boundaries](references/unit-boundaries.md#module-and-package-boundaries) |
| Who determines a rule, or do same-named concepts mean the same thing? | [Rules and meaning](references/ownership-locality.md#rules-and-meaning) |
| Who owns state, copies, tasks, cleanup, or synchronization? | [State and consistency](references/ownership-locality.md#state-and-consistency), [lifetimes](references/ownership-locality.md#work-and-resource-lifetimes), or [synchronization](references/ownership-locality.md#shared-state-and-synchronization) in the same reference |
| Will a proposed boundary improve change/failure locality enough to justify its cost? | [Locality](references/ownership-locality.md#change-and-failure-locality) and [boundary cost](references/ownership-locality.md#boundary-cost) |

These routes can combine when the question crosses levels. To locate detail cheaply, list headings with `rg '^##' references/*.md` or search the relevant concept. References supply judgment aids, not another set of independently invoked skills. [Examples](references/examples.md) are a separate optional lookup: use a matching section when a concrete contrast helps, rather than loading them by default.

## During code design

Apply this reasoning when designing new code or extending a feature requires choosing responsibilities or owners; the user need not explicitly ask for a cohesion review. Use requirements, business invariants, resource lifetimes, and existing module contracts as evidence before code exists. For an existing project, inspect likely owners and nearby conventions before introducing a new unit; for a new project, state the assumptions supporting the proposed boundary.

Decide which rules, state, operations, and cleanup obligations belong together, and what can vary independently. Prefer placing knowledge with an existing suitable owner; create a new boundary when its responsibility and benefit justify the coordination cost. Use plausible changes to challenge the design, not as proof that hypothetical future needs require interfaces, layers, or a shared framework.

Give the proposed ownership, reasons, constraints, and consequential open questions at the depth needed. Then continue the requested interface design or implementation using that result. A small ownership choice can be resolved inline; routine local work within an established boundary does not require a separate structural exercise.

## Default approach

A useful path is **inspect → hypothesize → challenge → recommend**; adapt or revisit it as needed. Ground a design proposal in requirements and known contracts, and a finding about existing code in that code and its contract, consider the most relevant counterevidence, and explain the practical benefit and cost of the proposed boundary. Distinguish facts, inferences, and exploratory ideas. Hypothetical changes are welcome as probes, not proof that a refactor is required.

Lead with the useful conclusion, including keep-together when appropriate. Optional priorities are **Required** for demonstrated correctness or hard-rule violations, **Recommended** for supported maintenance improvements, and **Explore** for promising conditional alternatives. Use only the report detail the decision needs; uncertainty need not prevent useful exploration.

## Principles

- **Size and naming:** long functions, many methods, `Manager`, `helpers`, or “and” in a description are inspection clues, not verdicts. A cohesive file can remain large; a tiny helper can still belong elsewhere.
- **Thin boundaries:** a one-use pass-through may add nothing, or may protect an actual compatibility contract or test boundary. Evaluate what it isolates and what removing it would expose.
- **Rule ownership and meaning:** place interpretation with whoever or whatever determines the contract. Compare meaning, identity, valid states, and units before sharing a concept. The same entity name or team boundary does not settle ownership; distinct meanings do not require separate services or a DDD framework.
- **State and copies:** make authoritative state, allowed writers, derived values, and consistency obligations clear. Derive values when cheap and reliable; intentional caches, snapshots, drafts, and replicas may have different lifetimes. Define propagation, refresh, invalidation, and allowed staleness rather than eliminating every copy. Shared ownership needs an explicit coordination protocol, not necessarily a singleton.
- **Work ownership:** associate starting work, observing failures, cancellation, and cleanup with the activity that needs it. Longer-lived work can outlive its caller through an explicit transfer to a responsible owner.
- **Lifecycle and sequence:** grouping only by `init/process/finish` often hides ownership. A lifecycle with legal states, resource ownership, and cleanup obligations can itself be a cohesive responsibility.
- **Orchestration and abstraction level:** coordinating validation, storage, and notifications can be one use case. Keep its main level coherent and examine interleaved policy or protocol internals when they force unrelated knowledge on the reader. Neither multiple steps nor a short responsibility sentence proves a need to extract functions.
- **Atomicity and synchronization:** keep protected state, its protection protocol, and invariant-preserving operations under clear responsibility. Conceptual, file, and runtime consistency boundaries need not coincide: independent policies may share one transaction, and extracted helpers may preserve one atomic operation. Co-location alone does not prove correctness; use the actual synchronization contract without automatically adding locks.
- **Change and failure locality:** probe a plausible change or failure and compare the unrelated knowledge and coordination required before and after a proposed boundary. Prefer known requirements; label hypothetical probes. Many changed files may be necessary contract representations, and mechanical co-change does not prove shared responsibility.
- **Placement across scales:** organize functions, classes, files, and packages around coherent duties and shared implementation knowledge. Keep code read and changed together near its owner; move independently governed concerns when that improves locality. A new unit needs a meaningful responsibility and name, not merely fewer lines. Genuinely generic tools may remain shared.
- **Duplication:** identical text can encode different rules. Conversely, different-looking code can repeat one contract. Judge shared knowledge and its owner before joining or extracting.
- **Boundary cost:** consider moving knowledge to an existing owner or removing a redundant facade before adding new machinery; favor changes whose benefit exceeds their new names, imports, public contracts, coordination, and testing cost. Small edits are a good default, not a prohibition on a broader design when the problem or user calls for it.

## Review execution

When a manual review request leaves its scope unspecified, the main asks one concise scope question and waits before reviewing code or dispatching reviewers: uncommitted changes, the latest commit or a specified commit range/PR, or a named project/module (these are suggestions, not an exhaustive menu). Reuse any scope already clear from the current or prior conversation, including the parent's assignment; ask only for missing details. Resolve the repository/path and revisions from the answer: uncommitted includes staged and unstaged changes plus relevant untracked files; the latest commit means its diff from its parent; “recent commits” needs a count or range; project/module review covers the named area, not an assumed diff. Do not silently choose HEAD~1, the current repository, or the whole project when those choices are unresolved. Only the main asks; reviewers receive the resolved scope. A bare skill invocation with unclear design-versus-review intent needs a task clarification, not an automatic diff review. Design requests remain design requests.

For reviews, use parallel subagents when available and useful for independently inspectable areas or a consequential boundary needing an independent read. Choose by responsibilities, shared contracts, and risk, rather than line count or a fixed reviewer quota; a focused review can stay with the main agent. Before delegating, read [Parallel review](references/review-checklist.md#parallel-review). Each reviewer reads this entrypoint in full and may inspect related code beyond its assigned area. One main agent verifies and synthesizes the results. Delegated reviewers report to that main without spawning further reviewers. Design and implementation continue under their existing guidance; this review mechanism does not automatically activate for them.

## Boundary result and task scope

This skill independently owns boundary judgment: explain the owner, the proposed placement or split/join/move/keep conclusion, its evidence and tradeoffs, relevant contracts, and any unresolved question at the depth the task needs. Reuse established conclusions and inspected evidence; revisit them when new evidence, a useful counterexample, or an exploratory alternative could change the judgment. If information is missing, distinguish conditional alternatives from supported recommendations, complete unaffected analysis, and ask only when the missing answer materially blocks progress.

If the boundary result answers the request, finish. If requested work remains, use the result as input and continue; public-surface analysis belongs to `modularity-review` when available, which selects its own mode. Neither this skill nor its result depends on the optional `module-structure` selector. A missing companion does not prevent supported work or clearly labeled design exploration; identify the limitation without claiming to have used an unavailable skill.

Respect the user's requested scope and applicable hard project rules. A review or exploration does not authorize code edits. Existing implementation authorization remains valid through continuation. Preserve behavior and public contracts unless the user authorizes changing them, and report evidence and validation honestly. If implementation is requested, check relevant callers and behavior tests, choose validation appropriate to the change, and report any checks that could not run.

## Maintenance

Keep shared scope and core judgment principles here; maintain detailed criteria and examples in the routed references. Consolidate repeated guidance without discarding useful detail merely to shorten this file. Behavioral evaluation cases and instructions live in [evals/README.md](evals/README.md); they are not review-time reference material.
