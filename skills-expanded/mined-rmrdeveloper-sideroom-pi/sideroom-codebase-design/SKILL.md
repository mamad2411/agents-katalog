---
name: sideroom-codebase-design
description: "Improve an existing codebase for long-term maintainability and scale. Use when asked to review code structure, find refactoring opportunities, reduce coupling, redesign module interfaces, improve testability, or prepare code for growing traffic, data, features, or teams. Survey the relevant code, prioritize evidenced friction, and design incremental improvements in text. Also use during a substantial refactor when module shape is the problem. Skip routine fixes, cosmetic cleanup, and unsettled product requirements; use sideroom-grill for those requirements."
license: MIT
metadata:
  author: RMRdeveloper
  version: "1.1"
---

# Sideroom codebase design

Improve how an existing codebase absorbs change and known growth. Combine a
survey of architectural friction with concrete module design. Deliver prose,
Markdown tables, and code examples when useful. Do not generate diagrams,
graphs, images, SVG, Mermaid, HTML reports, or browser previews.

## Activation and scope

Load for repository improvement, architecture reviews, module redesign,
refactoring, testability problems, or preparation for long-term growth. A user
does not need to name the skill. When a specific module is already chosen,
inspect its callers and dependencies and go straight to design; a whole-repo
survey is unnecessary.

Determine the requested outcome from the conversation:

- **Review:** investigate and recommend; do not refactor or create report files.
- **Design:** propose the shape of a selected improvement and its migration.
- **Implement:** carry out improvements within the already authorized scope,
  including checks. Do not ask again for permission already given.

A review request does not authorize a rewrite. An implementation request does
not require pausing after every recommendation. Ask only about consequential
choices or missing facts that the user and repository have not settled.

## Vocabulary (internal reference)

Use these terms when they make a design clearer. They are not required in text the user reads. Prefer everyday words there, and explain a design term once if it is needed. Do not rename the project's own domain words to match this list.

| Term | Meaning | Avoid |
|------|---------|-------|
| **Module** | Anything with an interface and an implementation. Scale-agnostic: a function, class, package, or tier-spanning slice. | unit, component, service |
| **Interface** | Everything a caller must know to use the module correctly: the type signature, plus invariants, ordering constraints, error modes, required configuration, and relevant performance or resource behaviour. | API, signature |
| **Implementation** | The code inside the module. Distinct from Adapter. | — |
| **Depth** | Leverage at the interface: the amount of useful behaviour a caller (or test) can exercise per unit of interface they have to learn. A module is **deep** when a large amount of behaviour sits behind a small interface, **shallow** when the interface is nearly as complex as the implementation. | — |
| **Seam** | A place where you can alter behaviour without editing in that place (Michael Feathers). It is the *location* at which a module's interface lives. Where to put the seam is its own design decision, distinct from what goes behind it. | boundary |
| **Adapter** | A concrete thing that satisfies an interface at a seam. Describes *role* (what slot it fills), not substance. | — |
| **Leverage** | What callers get from depth: more capability per unit of interface they learn. One implementation pays back across many call sites and tests. | — |
| **Locality** | What maintainers get from depth: change, bugs, knowledge, and verification concentrate in one place rather than spreading across callers. | — |

**Principles that follow from the vocabulary:**
- Depth is a property of the **interface**, not of the implementation size. A deep module can be internally composed of small, mockable, swappable parts; they just aren't part of the interface.
- The **deletion test**: imagine deleting the module. If complexity vanishes, it was a pass-through. If complexity reappears across callers, it was earning its keep.
- The interface is the test surface. Callers and tests cross the same seam. If you want to test past the interface, the module is probably the wrong shape.
- One adapter means a hypothetical seam. Two adapters (e.g. production + test stand-in) means a real one. Don't introduce a seam unless something actually varies across it.

In text the user reads, use an everyday word unless one of these terms is needed to decide. Explain that term once. Respect the project's existing domain vocabulary (`CONTEXT.md` or equivalent) for business concepts. Do not replace established domain names just to impose this design glossary.

## Inspect before recommending

1. Read project instructions, existing domain vocabulary (`CONTEXT.md`, or the
   project's equivalent), and relevant ADRs. Respect existing contracts.
2. Start with the area or pain point the user named. Otherwise, use available
   history to find areas with repeated changes, fixes, or coordinated edits;
   verify the friction in current code. History is a lead, not proof. If history
   is absent or uninformative, follow central business flows and their tests.
3. Trace representative behavior from entry point through domain logic and
   persistence or external calls. Inspect real callers, configuration, error
   handling, tests, and operational evidence available in scope.
4. Identify what makes changes costly: knowledge duplicated across callers,
   hidden ordering constraints, leaked internals, coupled release changes,
   brittle test setup, resource bottlenecks, or unclear ownership. Cite actual
   files and behavior. File length, folder count, or a missing pattern alone is
   not an architectural finding.
5. For growth concerns, load [references/growth.md](references/growth.md).
   Separate verified constraints from assumptions. Missing production metrics
   are a limitation, not permission to invent capacity claims.

## Design principles

Apply the vocabulary above. In particular:

- A **module** presents an **interface** and hides an implementation. Its
  interface includes everything callers must understand: inputs, outputs,
  invariants, errors, ordering, configuration, and relevant resource behavior.
- Seek **depth**: useful behavior behind a small, coherent interface. Evaluate
  the knowledge and coordination removed from callers, not implementation size.
  Internally compose focused responsibilities; depth does not justify a god
  object or combining unrelated reasons to change.
- Use the **deletion test**: if removing a wrapper eliminates complexity without
  spreading obligations into callers, consider removing it. If callers must
  each reconstruct important rules, the module is doing useful work.
- A **seam** is a point where behavior can be substituted; an **adapter** is a
  concrete substitute there. Introduce seams for actual variation, isolation,
  or testing needs. Production and test adapters can justify a seam; a generic
  port with one implementation and no demonstrated need does not.
- Improve **locality** by keeping a business rule and its verification in a
  clear place. Improve **leverage** by letting callers use that behavior without
  learning its internal machinery. Explain these benefits in plain words.
- Preserve required validation, failure handling, compatibility, and supported
  behavior. Simplicity is assessed against the full requirements.

Use the project's domain names in code. Explain necessary design terms once;
do not replace established vocabulary just to impose this glossary.

## Prioritize and design

For each worthwhile candidate, state the evidence, current cost, proposed
change, expected benefit, migration cost, and confidence. Rank by avoided
defects and change cost, known growth needs, reach, effort, and reversibility.
Do not invent numerical scores or fill a quota of findings.

Use **Strong** for demonstrated friction with a defensible remedy, **Worth
exploring** when an important fact or experiment is still needed, and
**Speculative** for an unverified future concern. Speculative findings become
measurement or monitoring steps, not implementation tasks. Say when no
structural improvement is justified. Flag a conflicting ADR and explain the
new evidence before proposing to reopen it.

For the selected candidate:

1. State the behavior and compatibility constraints that must survive.
2. Describe the interface and show a representative caller when helpful. Name
   inputs, outputs, errors, ownership, and ordering obligations. State which
   complexity moves inside and which responsibilities remain separate.
3. For a meaningful trade-off, compare genuinely different designs, including
   keeping the current design when viable. Compare caller burden, change
   locality, tests, operational cost, and migration; recommend one. Routine
   improvements need no forced alternatives or subagents.
4. Classify dependencies: computation can be tested directly; local resources
   may use realistic test substitutes; owned remote services need contract and
   failure coverage; external providers need controlled adapters and suitable
   integration checks. Do not expose private implementation details only to
   make tests easier, or claim mocks establish real provider behavior.
5. Plan small coherent steps with their checks and rollback. Keep callers
   working during transition, handle data migrations and mixed versions where
   relevant, and remove temporary compatibility code only when safe.

## Verification and skill composition

Test observable behavior through the interface used by callers. Preserve
regression coverage, failure cases, and compatibility. Replace redundant tests
only after equivalent behavior is covered and obsolete seams are removed;
do not delete tests merely because they inspect a smaller function. For scale
claims, identify the workload and measurement that would validate the benefit.

- Load `sideroom-guidelines` and applicable language guides before edits.
- Use `sideroom-architecture` for unresolved consequential contracts, data,
  dependencies, or operational choices; reuse decisions already accepted.
- Use `sideroom-grill` when the product behavior itself is still open, and
  `sideroom-domain-modeling` for actual naming conflicts. A design review does
  not automatically launch an interview or write a glossary or ADR.
- In the TUI, use `sideroom_ask` for needed decisions. If no interactive question
  tool is available, state the question in the conversation and continue only
  independent investigation; never interpret tool failure as an answer.
- Apply `sideroom-persona` to the report and summary. Run the project's relevant
  checks after implementation and report what they established.

## Output

Lead with the highest-value recommendation or the finding that no change is
justified. A review contains prioritized candidates with file evidence,
before/after behavior in words, benefit, cost, confidence, and a recommended
next step. A design contains the proposed contract, trade-offs, migration,
verification, and unresolved facts. After implementation, report changes,
checks, and remaining limitations. Keep review results in the conversation
unless the user requests a document. No graphic or HTML artifact is produced.

**Use the design vocabulary (module, interface, depth, seam, adapter, leverage, locality) consistently** in all recommendations and designs.

## Attribution

Adapted from Matt Pocock's
[codebase-design](https://github.com/mattpocock/skills/tree/main/skills/engineering/codebase-design)
and
[improve-codebase-architecture](https://github.com/mattpocock/skills/tree/main/skills/engineering/improve-codebase-architecture),
with Sideroom routing, incremental delivery, and growth assessment. The upstream
MIT notice is included in [LICENSE.txt](LICENSE.txt).
