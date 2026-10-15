---
name: context-acquisition
description: Use when an engineering decision depends on repository, specification, dependency, runtime, or external information that is not already established in active context. Enforce a small task-relevant working set through targeted search, dependency-aware progressive expansion, required-instruction preservation, version-aware source selection, durable findings, and explicit stop conditions.
---

# Context Acquisition

Acquire the smallest working context that preserves the information and relationships required for a correct engineering decision.
When this workflow materially creates or edits durable technical prose, the `technical-writing` skill MUST be applied.
Transient navigation notes MAY be produced without activating `technical-writing` solely because they are prose.
This skill determines how context is acquired.
It MUST NOT replace authority rules owned by `spec-driven-development`, diagnosis rules owned by the applicable debugging workflow, or production-code rules owned by `implementation`.

## Terms

**Required instruction context** is instruction material that governs the task, such as applicable project instructions and the root instructions of an activated skill.

**Working context** is task-specific evidence acquired to make the current decision, such as code, requirements, tests, configuration, dependency definitions, runtime evidence, or external documentation.

A **context question** is an unresolved question whose answer can change the current decision, edit, test, diagnosis, or review finding.

A **logical unit** is the smallest coherent artifact region that can answer a context question, such as a function, type, class, module section, requirement, test case, configuration block, or dependency API definition.

A **material relationship** connects information that can change the interpretation or outcome of the current decision. Examples include call relationships, type relationships, requirement dependencies, configuration precedence, and test-to-contract relationships.

**Progressive expansion** means acquiring the narrowest useful context first and widening only when an unresolved context question requires it.

A **durable finding** is a verified fact that is likely to be needed again during the current task or later work on the same problem.

## Core Invariant

The agent MUST acquire the smallest working context that preserves every material fact and relationship required for a correct decision.
Context efficiency MUST be judged by decision sufficiency, not by token count alone.
Working context MUST be acquired to answer a concrete context question or establish a required authority, contract, dependency, or verification fact.
Working context MUST NOT be loaded only because it might be useful later.

A whole repository, directory, ordinary source file, specification, dependency source tree, or external documentation set MUST NOT be read by default.
Broader working context MAY be acquired when narrower context cannot answer a material question.
Correctness MUST NOT be sacrificed only to reduce context use.

When the active context answers the material questions for the current decision, the agent MUST stop acquiring working context and continue the owning workflow.

## Required Instructions

Required instruction context is not discretionary working context.
Context-minimization rules MUST NOT be used to skip, truncate, or selectively ignore an applicable instruction artifact.

Applicable repository instruction files, such as `AGENTS.md`, MUST be loaded according to the host's instruction-discovery rules.
When an activated skill requires its root `SKILL.md` to be loaded by the agent, the complete root file MUST be read before the skill is applied.
An instruction artifact that is already present in active context MUST NOT be reread only for reassurance.

Supporting skill references SHOULD be loaded progressively when the root skill requires them or when a material question cannot otherwise be answered.
The ordinary whole-file restriction in this skill does not apply to required instruction artifacts.

## Start From Existing Context

Before you search or read additional working context:

1. Identify the decision you are trying to make.
2. State the unresolved context question.
3. Check whether the current conversation, required instructions, active skills, or already-inspected artifacts answer it.
4. Acquire new working context only for the remaining question.

Information already established by a higher-authority instruction or active operational profile MUST NOT be rediscovered through external research merely for reassurance.
A standard or policy already translated into an active skill MUST NOT be searched again unless formal conformance, an uncovered case, a version-sensitive fact, or an exact source definition requires it.

## Targeted Search

Use the narrowest search that can locate the relevant logical unit.
Exact identifiers, symbols, requirement IDs, error text, filenames, import paths, API names, or distinctive terms SHOULD be preferred before broad conceptual searches.
Search results SHOULD be used to locate evidence.
They MUST NOT be treated as sufficient context when omitted surrounding material can change the meaning.

When the target is known, inspect the target logical unit before unrelated neighboring content.
When the target is unknown, use repository structure, indexes, symbol search, or focused text search to locate likely units before reading implementation details.

A broad repository scan MUST NOT replace a targeted search when the task provides a usable identifier or anchor.

Apply `references/search-and-expand.md` when repository navigation is non-trivial.

## Progressive Expansion

After you inspect a logical unit, identify what remains unresolved.
Expand working context only along a material relationship that can answer that question.

Common expansion relationships include:

- caller or callee;
- imported or exported symbol;
- implementing or implemented type;
- governing requirement or schema;
- related conformance or regression test;
- configuration or generated source owner;
- dependency declaration, installed source, or API definition;
- runtime evidence relevant to the observed behavior.

Each material expansion SHOULD have a reason tied to an unresolved context question.
An entire ordinary file MAY be read when file-level initialization, ordering, invariants, generated structure, cross-cutting state, or another file-wide relationship materially affects the decision.
An entire ordinary file SHOULD NOT be read only because one symbol in that file is a possible edit target.

When context is summarized, pruned, or compacted, material definitions, conditions, provenance, and dependency relationships MUST be preserved.
Fixed compression ratios, arbitrary file-count limits, arbitrary line-count limits, and arbitrary tool-call limits MUST NOT replace the sufficiency test.

## Source Selection

Use the source most likely to answer the current context question with the required authority and version fidelity.
The owning skill MUST determine normative authority when authority affects the decision.

For repository behavior, local checked-in artifacts and the current working tree SHOULD be preferred over remembered behavior.
For an adopted dependency, the installed or locked version SHOULD be inspected before unrelated latest-version documentation when version differences can affect the answer.
For generated artifacts, the maintained source SHOULD be located when the task concerns the behavior or definition that generated output represents.

Conflicting artifacts MUST NOT be averaged or silently reconciled.
When a conflict affects required behavior, hand authority resolution to `spec-driven-development` or the applicable owning skill.

Apply `references/source-selection.md` when multiple artifacts could answer the same question.

## External Research

External research SHOULD be used only when local context cannot establish a material external fact, current external semantics matter, or the task explicitly requires external verification.
Primary or governing sources SHOULD be preferred for material technical claims.
Version-sensitive external guidance MUST be matched to the version relevant to the project when the difference can affect the decision.

External research MUST NOT replace inspection of the actual local code, configuration, schema, dependency version, or project instruction when those artifacts determine current behavior.
External research MUST NOT be performed merely to rediscover standards guidance already encoded in an active skill.

Apply the evidence profile from `technical-writing` to sourced claims and `references/external-research.md` when external lookup is necessary.

## Preserve Useful Findings

A durable finding SHOULD be recorded when doing so prevents repeated acquisition or preserves a non-obvious fact needed later in the task.
When a durable finding is recorded, an existing task note, plan, specification, ADR, or other project-approved location SHOULD be used when one exists.
A new documentation artifact MUST NOT be created only to record trivial navigation facts.

A recorded finding MUST distinguish verified fact from inference.
A finding that becomes stale after an edit MUST be revalidated before it controls a later decision.

Apply `references/context-notes.md` for long or multi-stage tasks.

## Stop Conditions

Context acquisition is sufficient for the current decision when the agent can identify, as applicable:

1. the governing behavior or question;
2. the relevant logical unit;
3. the material facts and relationships that can change the decision;
4. the verification or evidence needed by the owning workflow;
5. any unresolved uncertainty that requires handoff to another skill or reporting.

The agent MUST stop acquiring working context when additional material would not reasonably change the current decision.
The agent MUST resume context acquisition when a new material question appears during planning, testing, implementation, debugging, or review.

## Deviations

If targeted inspection cannot establish sufficient context, the search MAY widen incrementally.
If a tool cannot inspect a narrow logical unit, a broader read MAY be used.
The limitation SHOULD be treated as a tool constraint rather than a preferred workflow.
If required context is unavailable, inaccessible, or contradictory, the agent MUST report the limitation or route the conflict to the owning skill instead of guessing.

Time pressure, curiosity, unused context capacity, and a desire for reassurance MUST NOT justify indiscriminate context loading.

## Completion

Before substantial context acquisition is reported complete, `references/review-checklist.md` MUST be applied.
Context acquisition MUST stop when the current decision is sufficiently supported and MUST NOT stop while a material unresolved context question can change that decision.

## References

- `references/search-and-expand.md` — targeted navigation, dependency-aware expansion, and whole-file boundaries.
- `references/source-selection.md` — choosing local, generated, dependency, and normative sources.
- `references/external-research.md` — when external lookup adds material context.
- `references/context-notes.md` — preserving durable findings without creating documentation noise.
- `references/review-checklist.md` — context-acquisition completion review.
- `references/sources.md` — academic evidence, host guidance, provenance, and house-policy boundaries.
