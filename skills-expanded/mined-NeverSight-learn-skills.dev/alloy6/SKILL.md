---
name: alloy6
description: >-
  Design, write, review, debug, migrate, explain, and verify Alloy 6 models. Use this skill whenever the user explicitly mentions the Alloy language, Alloy 6, Alloy Analyzer, an .als file, an existing Alloy model, learning or teaching Alloy, or asks to express a relational, temporal, access-control, protocol, or security problem specifically in Alloy. Also use it when relevant workspace files are Alloy models or when modernizing pre-Alloy-6 explicit State/Time models. Do not use it for SQL or relational databases, TLA+, generic predicates/assertions, Grafana Alloy configuration, or metal alloys unless the user explicitly requests an Alloy model.
license: MIT
compatibility: Alloy Analyzer 6.x. CLI verification requires Java and the Alloy distribution JAR; authoring and review require no additional tools.
metadata:
  author: LabLambWorks
  version: "1.0.0"
---

# Alloy 6

Create models that expose assumptions and find counterexamples. Treat Analyzer results as evidence over declared bounds, not as an automatic proof of the real system.

## Load only the references needed

- Read [relational-modeling.md](references/relational-modeling.md) for every authoring, explanation, or review task.
- Read [temporal-modeling.md](references/temporal-modeling.md) when anything changes over time or the model uses `var`, prime, temporal operators, actions, or traces.
- Read [analysis-debugging.md](references/analysis-debugging.md) before executing commands, interpreting results, debugging an unsatisfiable model, or making a verification claim.
- Read [legacy-migration.md](references/legacy-migration.md) for pre-6 models, `util/ordering[State]`, or Alloy 4-to-6 migration.
- Read [security-modeling.md](references/security-modeling.md) for authentication, authorization, capabilities, attacker knowledge, or adversarial modeling.
- Read [sources.md](references/sources.md) when provenance, version routing, or further study matters.

Use [structural-access.als](examples/structural-access.als) and [temporal-capability.als](examples/temporal-capability.als) as small syntax patterns, not domain requirements.

## Correctness contract

Keep these four things visibly separate:

1. Domain assumptions: facts the environment promises.
2. Model behavior: signatures, relations, initial state, and actions.
3. Claims: assertions the Analyzer should try to refute.
4. Evidence boundary: structural scope, temporal horizon, solver mode, and observed outcome.

Never turn a desired assertion into a fact merely to make its check pass. Add a fact only when it represents a justified domain assumption, then re-run a nontrivial witness to ensure the model remains consistent.

Never say “proved safe” from an ordinary bounded check. Say “no counterexample found within this scope and horizon.” Complete temporal checking covers all traces only for the still-finite structural scope.

## Workflow

### 1. Frame the question

- Inspect existing `.als` files, project instructions, and Analyzer version before editing.
- State the system boundary, intended claim, excluded details, and assumptions.
- Classify the model as structural, behavioral, or a legacy explicit-state model.
- If information is missing but a safe default exists, state the assumption and proceed. Ask only when different answers would materially change the model.

### 2. Build the smallest useful structure

- Introduce domain atoms with signatures and relationships with fields.
- Write multiplicities explicitly (`one`, `lone`, `some`, or `set`). In a simple unary bound such as `f: T`, omission defaults to `one`; arrow bounds such as `r: A -> B` have implicit `set` arrow multiplicities. Make both cases intentional.
- Use `extends` for disjoint subtypes and `in` for overlapping subsets.
- Prefer readable relational navigation over simulated loops or object-oriented encodings.
- Add facts incrementally. Keep derived concepts in functions or predicates instead of storing redundant relations.

Before adding the main constraints, run a small witness. Then add at least one meaningful, nontrivial witness so a later passing check cannot hide an inconsistent or empty model.

### 3. Add behavior only when time matters

For new Alloy 6 behavioral models, prefer native temporal modeling:

- Mark only changing signatures or fields as `var`.
- Define `init`, one predicate per action, `stutter` when idle behavior is valid, `next`, and a reusable `traces` predicate.
- Give every action a guard, intended effects, and a frame condition for every other mutable relation. Unmentioned mutable state is unconstrained.
- Put state invariants under `always`. A top-level fact is evaluated at state 0, and each temporal operator affects only its operand: in `P and always Q`, `P` is initial-only while `Q` persists. Signature facts and declaration constraints apply in every state.
- Keep fairness as a named, justified premise for the relevant liveness claim. Do not hide arbitrary progress assumptions in global facts.

Do not silently mix native temporal modeling with the older ordered-`State` idiom. Preserve a legacy style when compatibility is the task; otherwise migrate it deliberately.

### 4. Validate before verifying

- Use `run` to obtain ordinary and edge-case instances.
- For behavioral models, run a scenario that forces a real transition; a stutter-only trace is not enough.
- Inspect several alternatives. In the visualizer, separate new configuration, trace, initial state, and fork choices.
- Treat warnings about arity, disjointness, or irrelevance as likely model defects. Do not enable “allow warnings” as a routine workaround.
- Add `expect 1` to commands intended to be satisfiable and `expect 0` to checks intended to find no counterexample.

### 5. Check claims and report the bound

- Put requirements in named assertions and use `check AssertionName`, not `check AssertionName {}`.
- Start with small scopes, understand the first counterexample, then increase the scopes and temporal horizon intentionally.
- Record the exact command, solver, scope, steps, satisfiable/unsatisfiable result, and any counterexample.
- If the Analyzer was unavailable, label the model “not executed” and provide the commands to run. Do not describe a manual reading as Analyzer verification.

## Review and debugging behavior

When reviewing a model, report findings in this order:

1. Semantic faults that change the represented system.
2. Vacuity or inconsistency that can make checks pass for the wrong reason.
3. Missing temporal frames, invariants, stutter, or justified fairness.
4. Scope, integer, ordering, or version traps.
5. Readability improvements that do not change semantics.

For each finding, identify the exact construct, explain the possible instance or trace it admits/excludes, and give the smallest repair. Do not “repair” a counterexample until deciding whether it exposes a model bug, a missing real-world assumption, or a genuine design flaw.

When analyzing a counterexample, narrate it as:

- static configuration;
- initial state;
- action sequence;
- first state where the claim fails;
- assumption or transition that enabled the failure.

Turn important counterexamples into named regression commands with `expect` annotations.

## Output contract

For an implementation task, return:

1. The created or edited `.als` path.
2. Assumptions and abstraction boundary.
3. Analyzer evidence in a compact command/result list.
4. The honest claim boundary: what was checked and what remains outside the model.

For an explanation, include both the relational reading and the plain-language reading of the important formula. For a review, cite exact file lines when available.

## Final audit

Before handing off a model, confirm:

- every field multiplicity is intentional;
- at least one nontrivial witness is satisfiable;
- global domain assumptions are facts, property- or scenario-specific assumptions are named predicates/premises, and claims are assertions;
- every mutable relation is updated or framed in every action;
- invariants that must persist are under `always`;
- each command has explicit scopes, temporal steps when relevant, and an expected outcome;
- the result wording names the bounds and does not overclaim.
