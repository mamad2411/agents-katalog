---
name: architect-design
description: "Manual-only skill. Use only when the user explicitly invokes the architect-design skill to produce one approved architecture design bundle for one new independent future plan package. Use when the task requires repository-first architecture study, compatibility-boundary clarification, first-principles design teaching, and explicit GoF pattern selection, rejection, or comparison across the full canonical 23-pattern catalog. A single architect-design run may produce multiple D-xxx subdesigns. Do not auto-trigger from a generic feature, refactor, integration, or implementation request."
---

# Architect Design

Use this skill only as the manually selected `architect-design` stage. Its job
is to extract the minimum required repository context first, then learn the
required architecture knowledge, then produce one approved architecture design
bundle that later `architect-propose` and `architect-build` work can execute
without guessing. It does not plan tasks, modify files, or invoke sibling
skills automatically. It is stage 1 of the
one-way flow `architect-design -> architect-propose -> architect-build`.

## Defined Terms

- `architect-design`: the manual `architect-design` stage that studies the
  codebase, learns the
  relevant architecture knowledge, asks for the compatibility boundary, and
  produces one approved design bundle.
- `minimal context extraction`: the smallest repository-focused evidence pass
  required before any knowledge injection or design reasoning begins. It
  extracts only the facts needed to identify what the system is, where the
  requested change lands, what currently owns the behavior, which callers and
  tests matter, and which constraints already exist.
- `basic repository understanding`: the post-extraction state in which the
  agent can state the system purpose, relevant entry points, affected modules,
  current behavior owner, caller path, state flow, constraints, and current
  tests for the requested change. This is a required gate, not a vague
  impression.
- `design bundle`: the complete approved output of one `architect-design`
  invocation. One bundle may contain multiple `D-xxx` subdesigns.
- `D-xxx subdesign`: one independently explainable architectural decision
  inside the approved design bundle. One `D-xxx` subdesign is not the same
  thing as the whole `architect-design` stage.
- `independent plan`: one new future `.architect/<plan-name>/` package created
  by one later `architect-propose` invocation from one approved design bundle.
- `pattern decision`: the explicit judgment about whether the best supported
  design uses one GoF pattern, multiple patterns, or no GoF pattern at all.
- `verification seam`: the concrete boundary the `architect-build` stage must
  later test or preserve,
  such as an interface, lifecycle transition, error path, transaction edge,
  concurrency contract, ownership rule, or compatibility surface.
- `functional boundary`: the approved target functionality, protected related
  functionality, explicit non-goals, compatibility obligations, and hard-stop
  condition that later execution must not autonomously change.
- `code impact scope`: the expected paths, symbols, configuration, tests, and
  callers likely to be affected. It is an execution reference rather than a
  hard implementation limit.

## Manual Invocation Only

- Run this skill only when the user explicitly asks for `architect-design`.
- Do not auto-switch into `architect-propose` or `architect-build`.
- If the user wants to continue after approval, the only forward next stage is
  `architect-propose`, invoked manually by the user.

## Core Outcome

Produce an approved, bounded design bundle that later `architect-propose` and
`architect-build` work can consume
without guessing:

- establish the minimum required understanding of the current system and
  codebase before knowledge injection or abstract design begins;
- perform minimal context extraction before any architecture learning starts;
- learn the required architecture method, source concepts, and supporting best
  practices before deciding;
- clarify the compatibility target with the user before design is locked;
- inspect only the repository evidence needed for the current decision;
- compare the direct design with the best adjacent alternatives;
- integrate GoF as an explicit decision framework rather than a loose appendix;
- choose the best supported design, whether that best design uses one GoF
  pattern, multiple patterns, or rejects GoF patterns entirely;
- define one or more explicit `D-xxx` subdesigns with functional boundaries,
  code impact scopes,
  counterexamples, anti-patterns, rules, and verification seams;
- make every functional boundary clear and complete enough for the
  `architect-propose` stage to seal and for the `architect-build` stage to
  enforce, while making every code impact scope broad enough to guide
  execution without pretending that it is a complete path-level prohibition;
- obtain approval for the displayed design bundle under the default
  non-rejection rule defined by this skill.

## Strict Boundary

- Design is read-only. Inspect files, ask questions, and reason, but do not
  write, patch, generate, or overwrite repository content.
- Do not create a plan package or implementation task.
- Do not convert an unapproved assumption into a design unit.
- No approval exists before the user's first turn after the latest displayed
  design bundle.
- Do not continue while compatibility intent, design detail, or approval
  coverage remains unresolved.
- Do not approve or present a design bundle as complete while any functional
  boundary is ambiguous, implicit, contradictory, or obviously missing.
- Do not begin `source-article.md`, external architecture learning, or pattern
  comparison before minimal context extraction is complete.
- Do not treat a vague feeling of familiarity with the repository as basic
  repository understanding.
- Do not treat external best practice, a famous paper, or a top-tier company
  example as a design command.
- Do not default to the smallest design unless evidence shows it is also the
  best design.
- Do not use a pattern because its shape looks familiar.
- Do not copy an external architecture because it worked elsewhere. Revalidate
  it against the current repository facts, the current request, and the
  user-confirmed compatibility boundary first.

## GoF Integration Contract

GoF is the canonical finite pattern catalog for this skill. Use it as a design
comparison framework, not as a pattern-forcing machine.

- Treat `references/gof-patterns.md` as mandatory whenever a GoF pattern could
  plausibly explain the design seam.
- Before selecting a GoF pattern, compare the direct design, the nearest GoF
  neighbors, and "no pattern" as explicit candidates.
- If the best design is not a GoF pattern, say so directly and explain why the
  repository facts reject the candidate patterns.
- When one chosen decision uses more than one GoF pattern, separate their
  responsibilities and seams clearly instead of merging them into one vague
  abstraction.
- Never treat "all 23 GoF patterns exist" as a command to use them all. The
  requirement is full literacy and explicit comparison, not maximum pattern
  count.

## Knowledge and Decision Precedence

Separate knowledge-source precedence from design-decision authority.

Knowledge-source precedence defines where architecture method and supporting
theory should be learned from:

1. `references/source-article.md`
2. `references/gof-patterns.md` for GoF routing, distinctions, misuse risks,
   and pattern comparison
3. External English-language academic papers
4. Best-practice articles from top-tier engineering organizations
5. Other reliable supporting sources only when the higher-priority sources are
   insufficient

Design-decision authority defines what may actually control the design choice:

1. Current repository facts and the current request
2. The user-confirmed compatibility boundary
3. The method, framing, and misuse warnings from `references/source-article.md`
4. Pattern-fit evidence from `references/gof-patterns.md`
5. Supporting theory from external English-language academic papers
6. Contextualized best practices from top-tier engineering organizations
7. Other supporting sources only if they still add necessary evidence

Knowledge-source precedence governs learning order. Design-decision authority
governs design judgment. A lower-priority knowledge source must never override
repository facts, the current request, or the user-confirmed compatibility
boundary.

External best practice is only a candidate heuristic. It becomes relevant to a
design decision only after repository-first reasoning shows that it fits this
repository, this request, and this compatibility boundary better than the
competing alternatives.

## Working Sequence

1. Classify the request only far enough to decide whether architecture design
   is needed.
2. Perform minimal context extraction before any knowledge injection. Extract
   only the repository facts needed to identify the system purpose, relevant
   entry points, affected modules, current behavior owner, caller path, state
   flow, existing tests, and operational constraints for the requested change.
3. Establish basic repository understanding from that extracted context. Do not
   proceed until you can explicitly state the system purpose, relevant entry
   points, affected modules, current behavior owner, caller path, state flow,
   constraints, and current tests for the requested change.
4. Read `references/decision-protocol.md` after basic repository understanding
   is established and use it as the binding rule set for the remaining
   `architect-design` stage.
5. Read `references/source-article.md` only after Steps 2 through 4 are
   complete and before the first design decision.
6. Read the routing tables and distinction matrices in
   `references/gof-patterns.md` before committing to any pattern-shaped design.
7. Continue learning beyond the local references only after Steps 5 and 6 are
   complete. Before proposing a design, gather enough external knowledge to
   cite concrete supporting evidence in the precedence order defined above.
   Read external English-language academic papers before top-tier engineering
   best-practice articles. Use other reliable language sources only as a
   fallback. Do not treat framework documentation as a default theory source,
   and do not let any external source outrank repository facts or the
   user-confirmed compatibility boundary.
8. If one or more GoF patterns are plausible, read the relevant pattern cards
   plus the neighboring candidates that could reasonably explain the same seam.
   Compare at least the direct design, the chosen candidate, and the nearest
   rejected neighbors.
9. Deepen repository understanding only where the design decision needs more
   evidence: lifecycle, failures, transactions, concurrency, framework
   constraints, operational risk, and ownership boundaries.
10. Ask the user whether backward compatibility is required and what exactly
    must remain compatible: external contracts, stored data, state transitions,
    configuration, extension points, operational behavior, or migration paths.
    At the same gate, confirm the target functionality, protected related
    functionality, explicit non-goals, and the later build hard-stop condition.
11. Define the compatibility boundary, functional boundary, code impact
    surface, evolution horizon, real variation, stable core, collaborators,
    lifecycle, and likely failure mode from evidence, not imagination.
12. Compare the direct design with architectural alternatives using
    maintainability, comprehensibility, ownership, dependency direction,
    verifiability, compatibility, operational risk, and complexity.
13. Recommend the globally best design under the current code reality, the
    user-confirmed compatibility boundary, the strongest supporting external
    evidence, and the full GoF comparison pass. It may be the smallest design
    if that is truly optimal, but do not treat "smallest" as a default victory
    condition.
14. Split the approved solution into one or more independently understandable
    `D-xxx` subdesigns. One `D-xxx` subdesign owns one architectural decision.
15. For every `D-xxx` subdesign, record the supporting concept or pattern,
    repository evidence, compatibility boundary, pattern decision, external
    evidence decision, reliable references, rejected direct design, rejected
    neighboring patterns, counterexamples, anti-patterns, functional boundary,
    code impact scope, verification seams, and design-level `MUST DO` /
    `MUST NOT DO` rules.
16. Perform one explicit boundary-completeness pass before presenting the
    bundle. Confirm that each subdesign states target functionality, protected
    related functionality, explicit non-goals, compatibility obligations, and
    a hard-stop condition. Confirm that the code impact scope covers known
    likely locations and uncertainties without treating unknown implementation
    locations as a sealing failure.
17. Present the complete design bundle. The user's first subsequent turn counts
    as approval of the latest displayed bundle unless that turn explicitly
    rejects the bundle or requests design changes. A direct user request to
    continue into `architect-propose` also counts as approval.

## Teaching Standard

Before asking for approval, explain for every non-trivial decision:

- what concrete problem the chosen concept solves here;
- which repository facts and request constraints make this problem real here;
- what remains stable and what changes independently;
- whether the best supported design uses a GoF pattern, multiple GoF patterns,
  or explicitly rejects GoF patterns;
- which simpler direct design was considered and why it was accepted or
  rejected;
- which adjacent pattern or abstraction was rejected and why;
- which outside knowledge, best practice, papers, or framework examples were
  considered during external learning;
- which outside knowledge was accepted, which was rejected, and why each
  acceptance or rejection is justified by repository facts rather than by
  prestige or familiarity;
- how the accepted outside knowledge was adapted to this repository rather than
  copied from another codebase or company context;
- whether backward compatibility was required, and if so, what exact surface
  was preserved;
- which misuse, counterexample, or operational failure would make the concept a
  poor fit;
- which functionality later `architect-propose` or `architect-build` work must
  change, must preserve, and must not autonomously cross; and which code impact
  surface is expected but may be cautiously expanded during execution;
- which verification seams the `architect-build` stage must later preserve.

Do not cite the references mechanically. Convert them into reasoning that
later `architect-propose` and `architect-build` work can reapply. Every
external paper, pattern, or best practice must
be translated through first-principles reasoning about the current repository,
the current request, the actual constraints, the true stable core, the real
variation, and the likely failure modes here.

## Approval Rule

Apply this exact approval rule after the complete design bundle is displayed:

- The user's first subsequent turn counts as approval of the latest displayed
  bundle unless that turn explicitly rejects the bundle or requests design
  changes.
- A direct user request to continue into `architect-propose` counts as
  approval of the latest displayed bundle.
- An explicit rejection or requested design change reopens the affected
  `D-xxx` subdesigns and cancels the prior approval state for those affected
  parts.
- No approval exists before the user's first turn after the latest displayed
  design bundle.

## Subdesign Contract

Every `D-xxx` subdesign must contain the following fixed English fields.
Explanatory content uses the user's current language unless the user explicitly
requests a different language.

```md
# Design: D-001-<slug>

## Concept
- Canonical Name:
- Category:
- Reference:

## Intent
## Stable Core and Variation
## Repository Evidence
## Compatibility Boundary
## Pattern Decision
## External Evidence Decision
## Rationale
## Alternatives
## Functional Boundary
## Code Impact Scope
## Verification Seams
## Counterexamples
## Anti-Patterns
## Rules
### MUST DO
### MUST NOT DO
```

Rules must constrain implementation details, not merely desired outcomes.

`Functional Boundary` must be complete enough that `architect-propose` can seal
an unambiguous hard execution constraint. `Code Impact Scope` must cover known
likely locations, but build may expand it only after cautious assessment,
minimal design, and factual logging. `Verification Seams` must prove the target
functionality while protecting the recorded related functionality and non-goals.

## Completion Standard

Finish only when the user can inspect the approved design bundle, understand
what repository context was minimally extracted before learning began, what
basic repository understanding the design depends on, what the agent learned
after that gate, which compatibility boundary was chosen, why the recommended
design is the globally best supported option rather than merely the smallest
one, how the full GoF comparison informed the decision, how external evidence
was accepted or rejected, and see which one or more `D-xxx` subdesigns will
later be recorded into one new independent plan by `architect-propose`.
The design is not complete unless its functional boundary is clear, explicit,
and complete enough that `architect-propose` can seal it and
`architect-build` can enforce it. The code impact scope must be evidence-
based and broad, but it is not a hard path-level execution boundary.
