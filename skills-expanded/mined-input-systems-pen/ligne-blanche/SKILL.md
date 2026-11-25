---
name: ligne-blanche
description: Boundary and structural integrity review for code or system changes. Use when the user asks whether a branch, diff, implementation, feature, refactor, module, class, file, package, service, or subsystem has crossed an architectural line, gone too far, introduced patchy exceptions, escape hatches, unjustified blast radius, unclear abstractions, or changed core structure without enough justification. Also use for prompts like "did we cross the line", "ligne blanche", "white line", "boundary review", "architecture boundary", "is this worth it", "does this fit the existing system", or "are these changes aligned with the codebase".
---

# Ligne Blanche

## Purpose

Use this skill to decide whether a change respects the existing system's structural boundaries or crosses a line that should be corrected, escalated, or explicitly justified.

The goal is not locally perfect code. The goal is a coherent, readable, navigable system with clear interfaces, explicit ownership, and no hidden pile-up of exceptions.

Apply this skill across languages, stacks, and product types. Let the reviewed system define the vocabulary: classes, modules, functions, traits, structs, packages, routes, jobs, actors, services, components, pipelines, schemas, protocols, scripts, configuration, infrastructure, or documents can all be the relevant unit.

## Core Stance

Treat the existing structure as evidence. Naming, ordering, file shape, imports, symbol shape, initialization shape, public APIs, comments, test placement, and neighboring implementations all carry information about the system's boundaries.

Prefer the smallest change that preserves the system's interface and structure. If the right solution requires changing structure, say so directly and judge whether the task justifies it.

Do not accept patch-layering: exception on top of exception, escape hatch on top of escape hatch, or special-case wiring that avoids the system's intended extension points. A change should either integrate through a designed flexible surface or deliberately reshape the structure.

## Workflow

### 1. Define the Review Scope

Infer the target from the conversation, branch, diff, or user-provided files. If the scope is unclear, choose the narrowest useful scope and state the assumption.

Identify:

- the files and symbols under review
- the user goal or product change
- the changed behavior, not only the changed code
- the surrounding callers, callees, tests, data boundaries, service boundaries, type or schema contracts, runtime flows, framework conventions, and integration points that define the local system

### 2. Reconstruct the Baseline

Before judging the change, describe the previous structure concretely.

Look for:

- file role: single-purpose file, mixed module, registry, adapter, service, renderer, parser, model, schema, repository, utility, command, job, test, or configuration
- exported symbols: classes, functions, methods, types, constants, hooks, components, structs, traits, interfaces, commands, public contracts, or externally consumed names
- internal shape: constructors or initializers, fields or properties, function or method order, private helpers, lifecycle, dependencies, side effects
- inputs and outputs: signatures, data ownership, return shape, validation boundaries, error behavior
- dependency direction: who calls this, who it calls, which layer owns persistence, transport, rendering, orchestration, validation, side effects, or domain behavior
- neighborhood pattern: adjacent files with the same role, naming, ordering, test style, and extension points
- publicness: whether the symbol is a local implementation detail, a shared contract, or a core API

Write the baseline as a strict structural map, not a vague summary.

### 3. Classify Hard and Flexible Surfaces

Separate the system into surfaces:

- **Strict/core surfaces**: foundational contracts, public APIs, storage formats, wire protocols, migration paths, serialization, data diffing, state machines, editor or parser internals, auth/access, domain invariants, shared services, widely imported utilities, and bottom-of-pyramid logic.
- **Flexible/play-doh surfaces**: local composition, feature-specific glue, obvious extension points, narrow adapters, presentation copy/layout, configuration maps, templates, and isolated implementation details.
- **Ambiguous surfaces**: code that looks flexible but has wide blast radius, or code that looks strict but is already designed as a registry or policy point.

Treat changes to strict/core surfaces as expensive. They can be right, but they need explicit justification.

### 4. Compare the New Shape

Describe what the change introduced:

- new symbols, files, exports, dependencies, or layers
- changed signatures, constructor requirements, public contracts, ordering, or ownership
- new conditionals, escape hatches, flags, special cases, or bypasses
- relocated logic, duplicated logic, hidden state, or side effects
- widened blast radius across modules, packages, processes, data boundaries, integration paths, tests, or runtime behavior

Then compare baseline vs new shape. Ask whether the change integrated into an existing extension point, reshaped a structure intentionally, or worked around the structure.

### 5. Identify Crossed Lines

Flag a crossed line when the change:

- modifies a strict/core surface for a narrow feature without explaining why
- adds a special case instead of using or improving the local extension point
- introduces another escape hatch to support a previous escape hatch
- spreads one feature's logic across unrelated layers
- hides domain behavior inside a transport handler, UI surface, utility, callback, script, or adapter that should stay thin
- bypasses the established data boundary, service boundary, type/schema contract, validation path, permission model, or access boundary
- makes a public API less obvious from its name, signature, return type, or file placement
- changes naming, ordering, file shape, or symbol taxonomy in a way that weakens local pattern recognition
- optimizes locally while damaging codebase navigation, ownership, or future maintenance

Do not over-report. A line is crossed only when the structure is meaningfully worse or the risk is not justified by the task.

### 6. Judge Justification

For each crossed line, decide whether it is justified.

Justified crossings usually have one of these forms:

- the user goal genuinely requires a broader contract
- the existing system is wrong for the domain and must be reshaped
- the new structure removes a repeated exception path and makes the system simpler
- the change creates or clarifies an extension point instead of bypassing one
- the blast radius is acknowledged, tested, and proportional

Unjustified crossings usually have one of these forms:

- the change makes a core system absorb feature-specific behavior
- the change avoids understanding the surrounding system
- the change introduces a convenient local abstraction that fights established ownership
- the change turns a clean API into a bag of flags, optional callbacks, or implicit modes
- the change adds patchy code where a smaller aligned implementation would work

### 7. Vet Fix Options

Treat proposed fixes as part of the review. A finding can be correct while the suggested fix crosses a different line.

For every meaningful finding, provide at least one fix that fits the local system before proposing broader alternatives.

Check each fix option for:

- local precedent: whether neighboring code already uses this pattern
- layer fit: whether errors, validation, persistence, transport, presentation, orchestration, side effects, or domain behavior stay in their usual layer
- consistency cost: whether applying this pattern once would create an exception that should really apply everywhere
- blast radius: whether the fix changes one path, a shared contract, or the whole subsystem
- structural honesty: whether the fix integrates with the system, deliberately reshapes it, or merely patches around it

Prefer this ordering:

1. **Locally aligned fix**: the smallest change that follows current structure and avoids a new exception.
2. **Structural fix**: a wider but coherent change if the local system is wrong or under-modeled.
3. **External ideal**: what might be cleaner in another codebase or redesigned ecosystem, clearly labeled as not the immediate recommendation.

Do not make an unaligned fix the primary recommendation just because it is technically simple. For example, do not suggest raising a transport-layer error inside a low-level builder, parser, formatter, or query producer if that layer does not already own transport failures. If that approach is attractive, explain that it would require applying the policy consistently across the subsystem or moving the validation to the layer that already owns request or command failures.

### 8. Recommend the Correction

Make the call. Use one of these outcomes:

- **Inside the line**: The change fits the system. Mention any small polish only if it matters.
- **Crossed, justified**: The change crosses a boundary, but the task warrants it. State the risk and required verification.
- **Crossed, not justified**: The change should be reworked to use the existing flexible surface or preserve the baseline structure.
- **Escalate structural change**: The existing system is the problem. Do not patch around it; propose the smallest deliberate restructuring.

When recommending a rework, prefer concrete moves:

- keep logic inside the existing owner instead of adding sibling helpers
- use the existing registry, adapter, service, data-access, protocol, rendering, or orchestration boundary
- preserve the current public signature and add behavior behind it
- extract only when the new name and boundary make ownership clearer
- remove the escape hatch and make the underlying policy explicit
- centralize converging logic when that makes the flow easier to inspect
- reject a locally convenient fix when it would create a one-off pattern in the reviewed system

## Output Shape

Lead with findings. Keep the answer direct.

Use this structure when the review is non-trivial:

```text
Verdict: Inside the line | Crossed, justified | Crossed, not justified | Escalate structural change

Baseline:
- ...

New shape:
- ...

Crossed lines:
- ...

Recommendation:
- Locally aligned fix: ...
- Structural alternative: ...
- External ideal, if useful: ...

What you need to know:
- Attention: 🟢 Skip | 🟡 Skim | 🟠 Read findings | 🔴 Read full review
- Why: ...
- Next action: None | Apply local fix | Decide structural change | Validate risk
```

End with `What you need to know` when the output is more than a short paragraph. Keep it tiny and decisive. It should let the user know whether the detailed review needs their time.

Use:

- **🟢 Skip** when the change is inside the line and no decision is needed.
- **🟡 Skim** when there are small alignment notes but no structural concern.
- **🟠 Read findings** when there is at least one crossed line or meaningful tradeoff.
- **🔴 Read full review** when a structural decision, broad blast radius, or core-surface change needs user judgment.

For small scopes, a short paragraph is enough, but still include the verdict and whether attention is needed.

## Calibration Rules

Do not confuse "different from my preferred design" with "crossed the line." The relevant standard is the local system, the user goal, and the blast radius.

Do not reward cleverness. Prefer code that is boring, explicit, and easy to navigate.

Do not demand extraction by default. A component, class, module, function, script, pipeline, or service can legitimately hold a lot of logic when that centralization makes the flow clearer.

Do not hide behind "best practices." Point to concrete structure: file shape, symbol ownership, dependency direction, signature clarity, or test surface.

When unsure, zoom out one level and inspect the neighborhood before judging.
