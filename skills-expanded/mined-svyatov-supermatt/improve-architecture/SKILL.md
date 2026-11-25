---
name: improve-architecture
description: "Assess a codebase's architecture, stop when it is healthy, otherwise find deepening opportunities, design the chosen one, and hand a plan to /implement."
argument-hint: "[module, subsystem, or pain point]"
disable-model-invocation: true
compatibility: Uses git to find hot spots.
license: MIT
---

# Improve Architecture

Explore a codebase, surface architectural friction, and propose **deepening opportunities**: refactors that turn shallow modules into deep ones, for testability and AI-navigability. Starts with an assessment: if the architecture is already healthy, say so and stop. Ends with a plan that `/implement` builds; this skill changes no code.

This skill is built on a shared vocabulary and informed by the project's domain model:

- Load and follow the `codebase-design` skill through the host's skill mechanism first. Use its terms exactly (**module**, **interface**, **depth**, **seam**, **adapter**, **leverage**, **locality**, **information leakage**) and don't drift into "component," "service," "API," or "boundary." Its `RED-FLAGS.md` names structural defects, its `DEEPENING.md` holds the dependency categories and seam discipline, and its `DESIGN-IT-TWICE.md` holds the parallel interface design.
- The domain language in `GLOSSARY.md` gives names to good seams; ADRs record decisions this skill should not re-litigate. `docs/agents/domain.md` gives where both live (by default `GLOSSARY.md` and `docs/adr/` at the root).

**Architecture vs refactoring:** this skill handles structural changes: module boundaries, interfaces, testability. If the problem is code-level (complexity, duplication, naming, dead code within a well-bounded module), that's refactoring: tell the user to run `/refactor` in Claude linked installs or Cursor, `/supermatt:refactor` from the Claude plugin, `$refactor` in Codex, or `/skill:refactor` in OMP. The same applies after an architectural change lands: cleaning up the new module's internals is a separate refactoring pass.

## Guardrails

1. **Deep is not big.** A deep module hides complexity behind a small interface; it does not own every concern it touches. If describing the proposed module requires "and" more than once, it's a god object, not a deep module. Split it. Deep modules can delegate internally to focused collaborators while presenting a simple interface.
2. **Separate, don't combine.** Deepening means consolidating a *single concept* scattered across many files. It does not mean merging unrelated concepts that happen to be called together. Before proposing a merge, ask: "Are these the same concern, or just co-located?"
3. **Architecture has a ceiling.** Not every codebase benefits from restructuring. Small projects (<20 files) with low coupling rarely need architectural intervention. The default verdict is **Healthy**: do not invent structural work.
4. **Every new element must pay for itself.** An interface, an argument, a class, a port: each one adds complexity, because someone has to learn it. To be a net gain it must remove more complexity than it introduces. This applies to anything this skill proposes creating.

## Process

### Step 1: Explore the codebase

#### 1a. Scope before you scan

Deepening a module pays off by making future changes to it easier, so weight the parts that actually keep changing. Decide *where* to look before you look:

- If the user named a direction (a module, a subsystem, a pain point), take it and skip the rest of this step.
- Otherwise, find the hot spots: files that change often and are complex. Count the changes per file over the last year with `git log --since="12 months ago" --name-only --pretty=format:`. Leave out bot commits and bulk reformat or move commits, because they inflate every file they touch. Rank the most-changed files by complexity, and let the top paths pull your attention first.
- If the changes are scattered with no clear hot spot, widen the net to the whole codebase.

Everything below operates on the scoped area, not necessarily the whole repository. Read the glossary and the ADRs that cover it.

#### 1b. Map the structure

Before exploring for friction, have a fresh read-only exploration subagent produce a structural inventory of the scoped area and return only the map. If no independent context is available, produce the map yourself and report that independence gap:

- List all modules/packages in scope with approximate size (file count, rough line count)
- Trace the dependency graph: which modules import which
- Flag circular dependencies
- For each module: number of exported symbols, number of callers, found with a symbol-aware search (LSP find references, CodeGraph) where available; mark grep-based counts `grep-only`

This map is your baseline. It prevents incomplete analysis across multiple sessions. Record the scope you chose in 1a alongside it.

#### 1c. Explore for friction

Read the scoped hot spots yourself, guided by the map from 1b: the verdict, the candidates, and the interface design briefs (paths + key line ranges) all rest on code you have seen. Read one file per call, so no result goes over the output limit and has to be read a second time from a saved file. Use fresh read-only exploration subagents only for sweeps outside the hot spots. When the host has no independent context, perform those sweeps sequentially and report the gap. Name each friction with a `codebase-design` red flag where one fits, since naming the flag is half the diagnosis. Note where you experience friction:

- Where does understanding one concept require bouncing between many small files?
- Where are modules **shallow**, with an interface nearly as complex as the implementation?
- Where is the same design decision encoded in two or more modules (**information leakage**)? This is the most expensive structural defect to leave in place. Watch especially for *back-door* leakage: knowledge shared between modules without appearing in either interface.
- Where have pure functions been extracted just for testability, but the real bugs hide in how they're called (no **locality**)?
- Where do tightly-coupled modules create integration risk in the seams between them?
- Which parts of the codebase are untested, or hard to test through their current interface?

**Deletion test.** Follow `codebase-design`'s test: if deleting a module makes complexity vanish, it was a pass-through; if complexity reappears across its callers, it was earning its keep. Use this result with the observed friction to decide whether the cluster needs deepening.

**Repairing a leak.** Two options only: merge the modules that share the knowledge, or extract the knowledge into a new module, but extract only if that new module can have a *simple* interface. Otherwise you have moved the leak, not fixed it, and added a module to learn.

**Completeness check:** every module in the map must be visited. Record what you skip and why; this prevents re-examination in future sessions.

**Skip these**, since they are shallow by design: thin adapters, data classes with no logic, configuration loaders, one-liner wrappers.

### Step 2: Assess whether architectural change is warranted

**This step is mandatory.** Evaluate the scoped area against these criteria:

- **Coupling**: are modules tightly coupled (high fan-out, circular dependencies, shared mutable state)?
- **Cohesion**: are modules internally cohesive (single responsibility)?
- **Testability**: are modules hard to test due to structural issues (not code-level issues)?
- **Navigability**: does understanding one concept require reading many files?

**Evidence rule:** every finding on these axes must name the symptom a reader actually experiences because of it:

- **Change amplification**: a simple change touches many places.
- **Cognitive load**: readers must hold a lot in their head to change anything safely.
- **Unknown unknowns**: readers cannot tell what they need to know. Worst of the three: the only check left is reading every line.

A finding that produces none of these three is a structural preference, not a problem. Drop it.

Produce a verdict:

| Verdict | Meaning | Action |
|---------|---------|--------|
| **Healthy** | Sound architecture, minor friction only | Tell the user, name the friction, and **stop**. Suggest `/refactor` in Claude linked installs or Cursor, `/supermatt:refactor` from the Claude plugin, `$refactor` in Codex, or `/skill:refactor` in OMP for code-level cleanup. |
| **Localized** | 1-2 areas have structural problems | Present only those candidates. Max 2 per session. |
| **Systemic** | Widespread structural issues | Present ranked candidates. Recommend tackling 2-3 per session. |

**Idempotency rule:** do not re-propose changes that were already implemented. Reassess the area against Step 2: if the earlier friction is resolved and no new structural problem is evidenced, report Healthy. If the same friction remains, diagnose what went wrong instead of proposing another round.

**Recorded decisions:** a candidate that contradicts an ADR is surfaced only when the friction is real enough to reopen it: say which record it contradicts and why it is worth revisiting. Do not list every refactor an ADR forbids.

**User override:** if the user gives a specific reason to proceed on Healthy code, scope strictly to their request.

### Step 3: Present candidates

Present a numbered list of deepening opportunities, named in the `GLOSSARY.md` vocabulary for the domain ("the Order intake module", not "the FooBarHandler"). For each candidate:

- **Cluster**: which modules/concepts are involved
- **Single responsibility**: one sentence describing what the deepened module does, no "and"
- **What it owns**: logic that moves inside the interface
- **What stays out**: related logic that remains separate, and why
- **Why they're coupled**: shared types, call patterns, co-ownership of a concept
- **Dependency category**: which of the four in `codebase-design`'s `DEEPENING.md` applies
- **Test impact**: which existing tests would be replaced by tests at the new interface
- **Impact**: High / Medium / Low

**Cohesion check:** if a candidate's single-responsibility statement requires "and" more than once, split it into multiple candidates or reject it. The stronger form of the same test: if a complete-yet-simple description is hard to write at all, the design is wrong; the difficulty is the diagnosis, not a writing problem.

End with the candidate you would tackle first and why. Do NOT propose interfaces yet. Ask the user which candidate to explore through the host's live multiple-choice capability, one option per candidate where the schema permits, or in chat when no such capability is usable.

### Step 4: Grill and design

Once the user picks a candidate, load and follow the `grilling` skill through the host's skill mechanism to walk the decision tree with them: constraints, dependencies, the shape of the deepened module, what sits behind the seam, what tests survive, and the "what stays out" boundary from Step 3.

For the interface itself, follow `codebase-design`'s `DESIGN-IT-TWICE.md`: radically different interfaces from parallel independent subagents, each brief carrying the files (paths + key line ranges), the coupling pattern, the dependency category, and the "what stays out" boundary. If parallel independent contexts are unavailable, use sequential fresh sessions; if fresh context is also unavailable, report the independence gap. **Reject any design that creates a god object** (multiple unrelated responsibilities behind one interface) and say why. Give your own recommendation: which design is strongest and why. Be opinionated.

Side effects happen inline as decisions crystallize; load and follow the `domain-modeling` skill through the host's skill mechanism to keep the domain model current as you go:

- **Naming a deepened module after a concept not in `GLOSSARY.md`?** Add the term. Create the file lazily if it doesn't exist.
- **Sharpening a fuzzy term during the conversation?** Update `GLOSSARY.md` right there.
- **User rejects the candidate for a reason a future run would need?** Offer an ADR: _"Want me to record this as an ADR so future architecture reviews don't re-suggest it?"_ Skip ephemeral reasons ("not worth it right now") and self-evident ones.

### Step 5: Write the plan

Once the user picks an interface (or accepts your recommendation), write the plan:

```
## Problem
- Which modules are shallow and tightly coupled
- What integration risk exists in the seams between them
- Which symptom (change amplification, cognitive load, unknown unknowns) it causes

## Proposed Interface
- Interface signature (types, methods, params)
- Usage example showing how callers use it
- What complexity it hides internally

## Cohesion Statement
- Single responsibility: [one sentence, no "and"]
- What this module owns: [bulleted list]
- What stays out: [bulleted list with reasons]

## Dependency Strategy
Which category applies and how dependencies are handled.

## Testing Strategy
- New tests at the interface: behaviors to verify through it
- Old tests to remove: tests on the shallow modules the new tests replace
- Test environment needs: local stand-ins or adapters

## Migration Strategy
Incremental (old and new coexist temporarily) or single switchover?
For high-traffic modules, prefer incremental with a deprecation path.

## Implementation Steps
Concrete, ordered steps. Each names files to modify, what to change,
and any caller migration. Include estimated scope.
```

### Step 6: Hand off to the build

Stay in this session, since the build needs the grilling as it happened, and tell the user the next step:

- **The change takes more than one session**: use `/to-spec`, `/to-tickets`, then `/implement` in Claude linked installs or Cursor; `/supermatt:to-spec`, `/supermatt:to-tickets`, then `/supermatt:implement` from the Claude plugin; `$to-spec`, `$to-tickets`, then `$implement` in Codex; or `/skill:to-spec`, `/skill:to-tickets`, then `/skill:implement` in OMP. The plan is the spec's input.
- **It fits in this session**: use `/implement` in Claude linked installs or Cursor, `/supermatt:implement` from the Claude plugin, `$implement` in Codex, or `/skill:implement` in OMP, with the plan as the spec. It writes the tests at the new interface first through `tdd`, then checks the change with `qa` and `code-review`.

To tackle another candidate later, the user starts a fresh session with `/improve-architecture <cluster>` in Claude linked installs or Cursor, `/supermatt:improve-architecture <cluster>` from the Claude plugin, `$improve-architecture <cluster>` in Codex, or `/skill:improve-architecture <cluster>` in OMP.
