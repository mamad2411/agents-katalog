---
name: architecture
description: Guides architecture decisions using domain rules, cohesive modules, and explicit contracts. Use when changing responsibility boundaries, integrating a foreign model, or designing asynchronous workflows.
---

# Architecture

Choose the smallest design that protects the required behavior. Use this workflow when a change alters responsibility, dependency direction, model meaning, or consistency. Routine changes within an established boundary can follow the repository's implementation workflow directly.

## 1. Establish the current behavior

Read the repository instructions, its domain glossary if present, and relevant architecture decisions. Discover their actual locations. Project-specific architecture guidance takes precedence over these defaults.

Trace the requested operation through its callers, implementation, persistence, and external effects. Read the tests covering that path. State the business rule, its current owner, and the concrete problem motivating a change. Cite files and symbols. Distinguish observed behavior, documented intent, and assumptions when they disagree. Continue independent investigation while asking about unresolved product rules.

**Complete when:** every entry point affected by the rule is accounted for, and the required outcome and failure case are explicit.

## 2. Load the relevant design reference

Read each matching reference before proposing a boundary. Several may apply to one change.

| Decision | Required reference |
| --- | --- |
| Change domain meanings, ownership, invariants, or consistency boundaries | [domain-modeling.md](domain-modeling.md) |
| Extract a module, change dependency direction, or integrate provider data | [boundaries.md](boundaries.md) |
| Introduce or change background work, events, retries, or recovery | [events.md](events.md) |

Apply coupling and cohesion throughout: name the decision a module hides and the business reason its responsibilities change together. Compare change propagation through callers, data formats, availability requirements, and deployment coordination. Folder proximity and fewer imports are evidence to investigate, not proof of better design.

## 3. Compare the boundary with the simpler option

Compare keeping or extending the current module with one proposed boundary. For each, explain which expected change stays local and which new contracts or operational duties it introduces. A direct function call is a valid outcome.

For the selected design, identify the contract owner, inputs, outcomes, failure meanings, and transaction owner. Draw source dependencies separately from runtime calls when proposing dependency inversion. State the permitted delay and recovery owner when work crosses processes.

**Complete when:** each added abstraction protects named behavior, and the simpler alternative has a concrete reason for acceptance or rejection. Preserve existing architecture decisions unless the requested change justifies revisiting them.

## 4. Apply the decision within the requested scope

For design or review requests, return the recommendation with code evidence. For implementation requests, change one complete behavior path and its affected callers. Use the repository's implementation skills and tooling for API wiring, schema changes, and task registration. Read current configuration for commands and generated-code rules.

Keep domain terminology in the project's canonical glossary when one exists. Record lasting tradeoff decisions in its established documentation rather than copying implementation details into this skill. A small decision can stay in the change description.

## 5. Verify the claimed benefit

Exercise the behavior at the selected contract. Test real storage for transaction and concurrency claims; test translation for foreign-model claims. Use the failure cases from the selected reference for asynchronous work. Include a composed check when wiring changes.

**Complete when:** every changed rule has evidence from an appropriate check, affected callers preserve their required outcomes, and relevant repository gates pass. Report unverified operational assumptions explicitly.

Keep the result proportional: problem and evidence, chosen boundary and simpler alternative, verification, remaining tradeoff. A small decision needs a few sentences; a cross-process change needs its failure path explained.
