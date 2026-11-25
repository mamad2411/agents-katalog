---
name: architect
description: "Design data shapes, interfaces, ownership, statecharts and module boundaries for substantive features or refactors; use for lifecycle rules, code organization, vertical modules, shared-code extraction, design review before code and design-versus-code drift checks."
---

# Architect

Follow the consuming project's instructions and requested scope; use the
[portable defaults](../orbyn-workflow/references/project-policy.md) only where guidance is missing.
Read the relevant [stack boundaries](../orbyn-workflow/references/project-policy.md#stack-and-ownership)
and trace the current design with [how](../how/SKILL.md). Use
[orbyn-research](../orbyn-research/SKILL.md) for a consequential external unknown.

## Method

1. **Start from one real caller** and a failure it must handle. Write the proposed call and result before drawing directories, then the necessary types, owner, interfaces and lifecycle. Include authority, concurrency, failure, recovery and compatibility when the task affects them.
2. **Inventory the current owner** of identity, mutable state, effects and cleanup. A new interface must take responsibility away from callers rather than merely rename their parameters.
3. **Compare alternatives where the choice is consequential;** a small sketch is enough when an established pattern fits; otherwise follow one normal and one interrupted operation through each alternative's owners, and compare the decisions callers must repeat, compatibility with released consumers and recovery cost. Select a design when that resolves the choice. If a measurement is needed, give the smallest prototype a decision threshold and disposable inputs. Use [arena](../arena/SKILL.md) only when competing candidates would settle a real uncertainty, never as a model panel for every boundary.
4. **Choose the smallest coherent design** and explain its trade-off. Keep domain ownership separate from platform rendering: a task editor can share the update contract while web and mobile keep their own focus and navigation behavior. If escape hatches or duplicated state interpretation keep recurring, reconsider the owner/type design and fix that source of complexity instead of adding wrappers.
5. **Check the interface** against a stale write, revoked access and a retry after an unknown result, where those cases apply.
6. **Return** an owner/interface table, a representative call, state transitions, the rejected alternative and a migration order. Use [orbyn-plan](../orbyn-plan/SKILL.md) when the design needs a delivery sequence. Record a durable rationale only when future maintainers need the decision.
7. **Review a written design before code** when it will drive a substantial build: fresh reviewer children read only the document and its linked files, through zoom-out, comprehension and implementation-readiness lenses ([design review](references/design-review.md)).

**Worked failure.** A proposal-approval design that starts from the Apply button lets web and mobile each invent their own lifecycle. Specify the durable proposal state, authenticated apply, stale-version behavior and shared result shape first ([approving a proposal](examples/proposal-approval.md)).

## Scope and delivery

A design-only request ends with the design contract and reorganizes no files. This skill request does not authorize reorganizing a consuming application. A small clear fix needs no architecture redesign. Keep sketches out of production code unless they are being completed in the same delivery. Implementation checks belong to the resulting change, within the user's scope.

For substantial implementation, the lead delegates against the selected design under the [workflow](../orbyn-workflow/SKILL.md), reviews the returned diff, performs authorized verification and routes repeated design friction back into the contract. A child implements its owned scope directly.

## Design rules

Choose authoritative data, ownership and lifecycle before adding logic. Simplify the affected design before extending it, and remove needless indirection without losing required behavior. Integrate new requirements into that design, and encode a demonstrated recurring failure at the boundary that can prevent it. Migrate controlled callers and retire the old API once compatibility evidence permits it.

When [comparative research](../orbyn-research/references/comparable-implementations.md) informs the design, translate it into this project's owners, interfaces, failure rules and regression checks; a similar upstream design does not establish this project's contract.

When a feature needs both an API and a UI, build the API slice first. A display-only UI built before the routes exist uses fixture or sample data and no guessed client; once they exist, the client follows the real contract, and uses the generated types when the project generates them.

For durable transitions, put the migration owner's concrete writer/admission contract in the design, including stale-writer rejection and current-writer controls. A link to migration guidance alone is not the deliverable.

## Read when needed

- Whole-app folder refactor (giant files, feature cycles, deep imports, duplicated helpers, logic in the transport layer): [folder refactor](references/folder-refactor.md).
- Checked-in designs or READMEs that may not match the code or built app: [design drift](references/design-drift.md). Report only; change nothing without the user.
- Where code belongs, cross-feature imports or shared-code extraction: [vertical code organization](references/vertical-codebase.md). Explaining an existing import path belongs to `how`.
- Statecharts, lifecycle races or behavior a human must inspect: [statecharts](references/statecharts.md); domain artwork over one: [illustrated statecharts](references/illustrated-statecharts.md).
- Deployed services and how they connect, not states over time: [stack-diagram](../stack-diagram/SKILL.md).
- Choosing between candidate shapes: [red-flag screen](references/design-review.md#screen-for-red-flags).
- Caller burden, shallow wrappers, cycles or API longevity: [maintainable modules](references/maintainable-modules.md); across languages: [polyglot example](examples/polyglot-contract.md).
- Unresolved language, framework or storage choice: [stack selection](../orbyn-stack-selection/SKILL.md) first, then own interfaces and lifecycle here. An established project's bounded feature usually keeps its stack.
- Implementation: the relevant [language reference](../language-best-practices/SKILL.md), preserving FFI/transport encoding, ownership and failure contracts.
- Cross-team, independently released or quantitatively constrained systems: [large changes](references/large-changes.md). Never infer deployed adoption from local edits.
- A new service or materially changed operating envelope: [service readiness](references/service-readiness.md).
- Command-interface design or terminal behavior: [CLI contract](references/cli-contract.md). Async admission, recovery, event ordering, duplicate registry keys or stale catalog entries: [runtime boundaries](references/runtime-boundaries.md).
- Expo modules, DOM/native bridges or incremental web migration: [mobile boundaries](references/mobile-boundaries.md).
- Worked examples (reuse the reasoning, not the synthetic owners): [approving a proposal](examples/proposal-approval.md), before designing approve or apply buttons, and [organizing a task editor](examples/vertical-task-editor.md).
- One decision needing a worked check, reading only that method: [foundations](references/principles/foundational-thinking.md), [order of simplification](references/principles/simplify-in-order.md), [subtraction](references/principles/subtract-before-you-add.md), [simplification](references/principles/laziness-protocol.md), [reader load](references/principles/minimize-reader-load.md), [coherent redesign](references/principles/redesign-from-first-principles.md), [structural prevention](references/principles/encode-lessons-in-structure.md), [domain structure](references/principles/model-the-domain.md), [repeated failure](references/principles/attack-the-premise.md), [alternatives](references/principles/exhaust-the-design-space.md) or [API retirement](references/principles/migrate-callers-then-delete-legacy-apis.md).
