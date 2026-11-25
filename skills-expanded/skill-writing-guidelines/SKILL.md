---
name: skill-writing-guidelines
description: Write or review agent skills for predictable invocation and execution. Use when creating a skill, restructuring a skill collection, diagnosing unreliable skill behavior, or pruning an existing skill.
license: MIT
---

# Skill Writing Guidelines

Make the skill's process predictable across runs, without requiring identical outputs. Apply the
active agent platform's native fields and validators; translate patterns from other harnesses
instead of copying their metadata unchanged.

## 1. Establish the behavior contract

Use concrete runs to identify the outcome, trigger branches, near misses, inputs and state, side
effects, success evidence, and failure behavior. Inspect existing callers and artifacts before
changing an existing skill. Treat a user-reported symptom as high-value evidence and the proposed
cause as a hypothesis to verify against files, history, tests, traces, and callers.

**Done when:** every genuine branch has a concrete example and an observable success or failure
condition.

## 2. Assign responsibility

Keep reusable discipline and vocabulary in primitives, end-to-end sequencing in orchestrators,
cross-session facts in narrow artifacts, platform commands behind adapters, and human discovery in
a router. Give each responsibility one owner.

**Done when:** every proposed skill has one coherent contract and shared behavior has one source of
truth.

## 3. Design invocation and hierarchy

Treat a model-facing description as a branch index: front-load the core action and add one trigger
per genuine branch. Inline what every run needs. Move branch-only reference behind a pointer that
says when and why to read it. Use leading words to compress behavior only when they are precise.

**Done when:** invocation mode is deliberate, every conditional resource has a firing condition,
and the main path is legible without irrelevant branches.

## 4. Encode gates and state

Validate cheap shared preconditions before expensive work. End consequential steps with observable,
exhaustive criteria. Separate discoverable facts from user decisions, and persist cross-session
state in purpose-built artifacts. Isolate independent evaluation axes when one can bias another.

**Done when:** another agent can follow every branch without inventing the source order, authority,
stopping rule, or evidence standard.

## 5. Prune and verify

Delete no-op sentences, duplicated meanings, stale layers, and obsolete branches. Prompt the
positive target behavior; pair necessary guardrails with the safe action. Audit consequential
negative space such as source authority, mutation scope, approval, and stop conditions. Run the
platform's structural validator, exercise linked commands safely, and forward-test triggers,
near-misses, main branches, blocked states, and the original regression.

Scale verification to the decision. Use the smallest evidence set that can change the diagnosis,
edit, or claim; expand only when impact, reach, side effects, or uncertainty justify it. Stop when
the next plausible check cannot change the decision. State intentionally skipped checks when their
absence limits the evidence boundary.

**Done when:** structure passes, representative runs follow the intended process without hidden
coaching, the evidence boundary is explicit, and each remaining sentence changes behavior or
supplies required knowledge.

## 6. Engineer the repository when the skill will be shared

For a published skill or collection, design a parallel repository contract. Keep runtime
instructions canonical while human documentation orients readers. Give experimental,
promoted, deprecated, and personal work visible lifecycle states. Use distribution manifests as
explicit allow-lists. Translate invocation and UI metadata with each harness's native fields, and
keep shared environment configuration and provider operations behind named adapters.

Persist architectural decisions, rejected scope, and breaking changes. Report source, version, CI,
remote publication, and installed state separately. Add compilation, structural validation,
regression tests, supported-platform CI, fresh-clone checks, and installation verification only when
the repository's executable artifacts and release risk warrant them. Attribute each gate to the
project that actually implements it.

**Done when:** the intended installable set is explicit, runtime truth has one owner, supported
platform metadata agrees, lifecycle state cannot be mistaken, and every claimed release state has
observable evidence.

## Evidence boundary

This is an independent, cross-platform interpretation inspired by Matt Pocock's public skill
repository. It is not an official Matt Pocock skill. Read
[references/evidence-boundary.md](references/evidence-boundary.md) before attributing any principle
to Matt Pocock or adapting source-harness metadata.
