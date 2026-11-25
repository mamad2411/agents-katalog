---
name: deep-refactor-audit
description: Use when a user asks for a major architecture/refactor audit, codebase smell investigation, boundary critique, feature simplification review, vibe-coded or AI-generated code cleanup assessment, hand-rolled library review, or no-code report on how a codebase should be reshaped.
---

# Deep Refactor Audit

## Overview

This is a no-code architecture audit for aggressively rethinking a codebase. The job is to ask why the codebase is shaped this way, whether that shape still deserves to exist, and what a strong principal engineer would change before allowing the system to keep growing.

AI-generated code often accumulates accidental architecture: features nobody asked to keep, abstractions created for one use case, hand-rolled versions of standard libraries, over-flexible configuration, compatibility paths with no owner, and names that hide what the code actually does. Treat those as suspect until they earn their place.

## Core Stance

Because this audit does not modify production code, take intellectual risks. Be creative, skeptical, and specific. Question architecture, naming, feature value, user behavior, dependencies, and whether whole subsystems should exist.

Do not be polite at the expense of usefulness. The valuable output is not "some code smells exist." The valuable output is a clear opinion about what should be preserved, simplified, deleted, or redesigned.

## Audit Boundary

Do not edit implementation files during this audit. You may create notes, diagrams, reports, and plans under `docs/`.

This restriction is not meant to make the audit timid. It exists so the diagnosis can be bolder than an implementation task.

## Start By Setting A Goal

Before the deep dive, set an explicit audit goal. If the environment has a goal mechanism, use it. Otherwise write the goal at the top of the audit worklog.

Use this shape:

```text
Goal:
Critically audit <scope> to determine which architecture, features, boundaries, names, abstractions, dependencies, and workflows should be preserved, simplified, removed, or redesigned.

Core questions:
- Why does this exist?
- Is it still needed?
- Is this the simplest shape that can support the product?
- Did this complexity come from real constraints or accidental accumulation?
- Is this hand-rolled code justified, or should it use a standard library/framework capability?
- What would the architecture look like if we designed it cleanly today?

Non-goals:
- Do not modify production code.
- Do not produce a shallow smell list.
- Do not assume the current architecture is justified.
- Do not recommend patterns without explaining concrete movement in the codebase.

Success criteria:
- Current architecture is mapped.
- Major boundaries are judged.
- Questionable features are called out.
- Hand-rolled machinery is compared against existing libraries or framework capabilities.
- Accidental complexity is separated from legitimate complexity.
- Prior art, named patterns, and mature repositories are researched where useful.
- A target architecture and refactor roadmap are written.
```

## Create Audit Artifacts

Create a dated folder:

```text
docs/refactor-audit-YYYY-MM-DD/
  README.md
  worklog.md
  source-map.md
  smells.md
  feature-questions.md
  hand-rolled-inventory.md
  research-notes.md
  subagent-briefs.md
  reports/
  target-architecture.md
  refactor-roadmap.md
```

Use fewer files for a small repository, but always keep a running worklog. Write notes throughout the audit, not only at the end. The worklog must let another agent resume after compaction without losing the important insights.

## Read With Suspicion

For every subsystem, ask:

- Why does this exist?
- Who benefits from this behavior?
- Is this feature actually wanted, or did it survive because nobody deleted it?
- Is this complexity paying rent?
- Would a user notice if this feature disappeared?
- Would a maintainer be relieved if this feature disappeared?
- Is this a general mechanism, or a one-off that got promoted into architecture?
- Does the name describe what the code really does?
- Are decisions separated from mechanisms?
- Are framework, provider, or transport details leaking into core logic?
- Is this hand-rolled because it needed to be, or because the original author did not look for a library?
- Would the second or third similar feature fit cleanly, or require teardown?
- If we rebuilt this today, would we choose this shape again?

Classify findings as:

```text
Keep:
The complexity is justified by product value, external constraints, safety, compatibility, performance, or repeated use.

Simplify:
The feature or boundary is useful, but the implementation is more complex than the value requires.

Delete candidate:
The feature, path, abstraction, dependency, parser, compatibility layer, or workflow appears to cost more than it is worth.

Replace with library:
The code hand-rolls a solved problem without a strong reason.

Redesign:
The concept is important, but the current boundary is wrong.

Unknown:
There may be a real reason, but the audit did not find enough evidence.
```

## Look For AI-Generated Accumulation

AI-written code often has specific failure modes. Look for:

- Features added because they were easy, not because they were needed
- Options, modes, and flags with no clear user story
- Generic abstractions with only one real implementation
- "Extensible" systems where extension was never exercised
- Compatibility shims that outlived the migration
- Helpers that hide product decisions
- Retry, fallback, and recovery paths nobody can explain
- Multiple ways to do the same thing
- Long files that read like a transcript of incremental requests
- Names that sound architectural but hide narrow behavior
- Defensive code around states the product should not allow
- Config knobs that encode product policy instead of mechanics
- Test fixtures that preserve old architecture because changing them was annoying
- Custom parsers, serializers, schedulers, state machines, or clients for problems with mature off-the-shelf solutions

Be willing to say: this whole feature may not deserve to exist.

## Audit Hand-Rolled Machinery

Treat hand-rolled infrastructure as a first-class audit target. Sometimes it is correct. Often it is accidental.

Inventory custom implementations of:

- Markdown, YAML, JSON, TOML, CSV, HTML, XML, or URL parsing
- Date/time, duration, timezone, or recurrence handling
- Glob, path, routing, or pattern matching
- CLI parsing, config loading, logging, formatting, prompts, or progress output
- HTTP clients, retries, pagination, rate limiting, auth, or SDK wrappers
- Job queues, schedulers, locks, leases, idempotency, or state transitions
- Caches, stores, migrations, repositories, and transaction helpers
- Validation, schema parsing, typed results, error formatting, and redaction
- React state, forms, tables, virtualization, drag/drop, rich text, or data fetching

For each one, ask:

```text
What is hand-rolled?
What standard library, framework feature, or popular package already solves this?
What special constraints might justify custom code?
What bugs or maintenance costs does the custom version create?
What would be deleted if we adopted the existing solution?
What would become harder if we adopted it?
Recommendation: keep custom / replace / wrap library behind a seam / research further.
```

Do not blindly demand libraries. A small owned parser for a tiny syntax may be better than a heavy dependency. A security-sensitive or performance-sensitive boundary may justify custom code. The audit should force the question and document the answer.

## Research Prior Art And Name Patterns

When the code is solving a known problem, research how mature systems solve it. Use web search, official docs, respected engineering writing, and open-source repositories when useful.

Name patterns explicitly. Patterns give vocabulary to the critique.

Use patterns as tools, not decorations. For each pattern, explain:

```text
Pattern:
Where it applies:
What would move:
What boundary would exist:
What gets simpler:
What gets more complex:
Why this is or is not worth it here:
```

Useful patterns to consider:

- Ports and adapters
- Hexagonal architecture
- Clean architecture
- Functional core, imperative shell
- Command/query separation
- Command pattern
- Strategy pattern
- Adapter pattern
- Facade pattern
- Repository pattern
- Unit of work
- Domain events
- Event sourcing
- Outbox pattern
- Pipeline architecture
- State machine
- Actor model
- Plugin registry
- Dependency inversion
- Layered architecture
- Vertical slice architecture
- Feature folders
- Modular monolith
- Anti-corruption layer
- Workflow orchestration
- Durable jobs
- Idempotency boundaries

Also inspect real repositories. If the codebase has a CLI, inspect respected CLI projects. If it has background jobs, inspect job queue systems. If it has multiple providers, inspect SDKs or tools with provider adapters. If it has a frontend, inspect mature apps using the same framework.

Do not copy blindly. Borrow shape.

## Challenge Features, Not Just Code

A deep refactor audit is allowed to question product surface area.

For each expensive feature, ask:

```text
Feature:
What user behavior requires this?
What code complexity does it create?
What other features does it distort?
What would break if it disappeared?
Could a simpler product behavior replace it?
Should we keep, simplify, hide, or remove it?
```

Examples:

```text
A reporting system supports six export formats, but users only need CSV.
Recommendation: delete or defer the unused formats. Keep the export boundary small until usage proves otherwise.
```

```text
A plugin system exists before there are external plugins.
Recommendation: keep a clean internal interface, but remove plugin discovery, lifecycle hooks, and registry machinery until a second real plugin exists.
```

```text
A settings page exposes every internal knob.
Recommendation: separate user preferences from operator/configuration concerns. Remove settings that users cannot reason about.
```

## Use Subagents Aggressively

When available, use subagents for independent critique. Do not ask them to validate your opinion. Ask them to find the strongest objections.

Useful subagent roles:

```text
Boundary critic:
Find modules with mixed responsibilities, misleading names, hidden policy, and bad dependency direction.

Feature skeptic:
Find features, flags, modes, compatibility paths, and abstractions that may not deserve to exist.

Hand-rolled machinery critic:
Find custom implementations of solved problems. Compare them against standard libraries, framework features, and popular packages.

Pattern researcher:
Research named architecture patterns and mature open-source examples relevant to one subsystem.

Deletion advocate:
Argue what should be removed entirely. Identify product simplifications that would collapse code complexity.

Target architect:
Propose a cleaner architecture from first principles, ignoring migration cost at first.

Migration realist:
Take the target architecture and identify sequencing, risks, tests, and rollback points.
```

Save subagent outputs under `reports/`.

## Produce A Strong Diagnosis

Each major finding should use this structure:

```text
Finding:
Evidence:
Why it exists today:
Why that reason may no longer be good enough:
Architectural cost:
User/product value:
Hand-rolled or dependency concern:
Recommendation:
Pattern or prior art:
Risk:
Confidence:
Files inspected:
```

Be direct. A useful audit may say:

```text
This module should not exist.
This feature is distorting the architecture.
This abstraction is premature.
This boundary is too weak.
This name is lying.
This subsystem should become three modules.
This workflow should be deleted unless there is evidence users need it.
This parser should be replaced by a library unless the custom grammar is a product requirement.
```

## Target Architecture

Do not stop at criticism. Propose the shape the codebase should move toward.

Include:

- New boundaries
- Renamed concepts
- Deleted or collapsed concepts
- Hand-rolled machinery to replace, keep, or isolate
- Patterns worth adopting
- Patterns explicitly rejected
- How the main flows would read after the refactor
- Which features become easier
- Which features become intentionally unsupported

Use lightweight pseudocode when helpful:

```ts
const request = commands.parse(argv);
const result = await operations.run(request);
output.render(result, request.outputMode);
```

Explain why that shape is cleaner.

## Refactor Roadmap

The roadmap should separate courage from chaos.

Group work into:

```text
Phase 0: Delete, hide, or freeze questionable surface area
Phase 1: Replace unjustified hand-rolled machinery or isolate it behind honest seams
Phase 2: Rename concepts so the architecture can be discussed honestly
Phase 3: Move decisions out of mechanisms
Phase 4: Introduce the right architectural seams
Phase 5: Collapse or replace obsolete workflows
Phase 6: Harden tests around the new shape
```

For each phase, include:

```text
Goal:
Changes:
Why first:
Risk:
Verification:
```

## Final Report

The final report should include:

- Executive summary
- Current architecture map
- Strongest architectural objections
- Feature deletion or simplification candidates
- Hand-rolled machinery inventory and recommendations
- Legitimate complexity worth preserving
- Accidental complexity likely caused by incremental or AI-generated work
- Prior art, mature repositories, and named patterns considered
- Target architecture
- Refactor roadmap
- Open questions for the user
- Reports and notes written

The tone should be serious, opinionated, and evidence-based. This is not a polite lint pass. This is the moment to ask whether the codebase deserves its current shape.
