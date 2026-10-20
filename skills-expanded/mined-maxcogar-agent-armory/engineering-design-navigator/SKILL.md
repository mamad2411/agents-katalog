---
name: engineering-design-navigator
description: "Workflow for using the Design Navigator MCP server during engineering design sessions. Governs when and how to call Design Navigator tools to track decisions, dependencies, constraints, and resources in the design graph. Use this skill in ANY session involving engineering design work — sizing components, selecting parts, calculating values, making architectural decisions, or continuing work on a component that has existing design state. Trigger on phrases like 'let's design', 'let's work on', 'size the', 'select a', 'calculate the', 'what should we use for', or any mention of a component within a project that uses the Design Navigator. Also trigger when resuming design work in a new session, when the user asks about the state of a design, or when reviewing/modifying existing design decisions. If engineering decisions are being made, this skill applies — even if the user doesn't mention the navigator explicitly."
---

# Engineering Design Navigator — Session Workflow

The Design Navigator MCP tracks engineering design decisions as a dependency graph. It enforces verification gates, detects cascading impacts from changes, surfaces relevant resources, and helps navigate non-linear design work including branching and backtracking.

Claude's job is the engineering. The tool's job is making sure nothing falls through the cracks. This skill defines when and how to use the tool so that it stays out of the way during actual engineering thinking but catches every mistake, gap, and inconsistency at the moment it matters.

## Why This Matters

Engineering design decisions are interconnected. Changing a shaft diameter can invalidate a bearing selection, which invalidates a seal selection, which invalidates the housing geometry. Without the graph tracking these connections, cascade detection is manual and error-prone — and experience proves that manual cascade detection fails. Parts that don't exist get propagated through documents. Sealed bearings get specified without checking pressure ratings. Values drift between files. The navigator prevents these failures by catching them at the moment of action, not after the damage is done.

## Session Startup

After CORE-Memory orientation, call `open_project(name)` to load the design state. The response returns the project phase, any tentative/invalidated/needs-review nodes, open branches, and failing constraints. Read the response carefully — it tells you what needs attention before new work begins.

If there are open items from a previous session (tentative parts, unresolved cascades, open branches), mention them to the user before diving into new work. They may want to resolve them first or consciously defer them.

If the user names a specific component to work on, call `get_component_summary(project, component)` before starting. This gives the full picture — existing decisions, dependencies, constraints, and available resources (calculators, references, lessons learned) — without needing to search for them separately. The resources that come back are tools and references validated through actual use on this project. Use them instead of starting from scratch.

If the MCP server isn't responding, say so. Work from CORE-Memory and project files. Decisions made during the outage get recorded into the graph retroactively when it's back.

### Project Phase

The project phase determines enforcement strictness:

- **`exploratory`** — All soft gates. Warnings returned but nothing blocked. Tentative parts, estimated values, and unverified selections are all fine. The tool tracks what's unverified but doesn't prevent progress.
- **`design`** — Hard gates on part selections (catalog link + operating limits required to leave tentative). Soft gates on calculations and assumptions. Constraints evaluated and failures flagged.
- **`build_ready`** — All gates hard. No tentative nodes, no unresolved cascades, no failing constraints, no open branches.

## The Core Loop

The natural rhythm of a design session is: check what exists → do engineering work → record what was decided → read the tool's response → act on warnings.

**Before calculating or selecting anything**, call `get_decision` or `get_component_summary` to see what's already established. Values recorded in the graph are the source of truth — don't recalculate from memory when the graph has a verified value. Recalculating from memory is how slightly-different numbers creep in and silently corrupt the design. If a value is in the graph, read it from the graph.

**When a value is determined** — calculated, selected, or assumed — call `record_decision` promptly. Don't accumulate multiple decisions and batch them later. The tool's value comes from its real-time response: warnings about missing verification, conflicts with existing values, constraint evaluations, cascade flags, and resource suggestions. Batching decisions means batching warnings, which means missing the moment when a warning could have prevented wasted work.

**Read every tool response thoroughly.** The response is not just a confirmation — it's the enforcement layer. It may contain:
- A hard gate blocking an unverified part selection
- A conflict between the new value and an existing value from a different source
- A cascade showing downstream nodes that are now invalidated
- A failing constraint showing a physical incompatibility
- A resource — calculator, lesson, or reference — relevant to what's happening right now

Each requires action or at minimum acknowledgment to the user. Don't silently proceed past warnings.

**If a value conflict comes back** — meaning the property already has a recorded value from a different source — don't override silently. Surface the conflict to the user: what the existing value is, where it came from, and what the new value is. Reconcile before proceeding. This is the most common way value drift enters a design: Claude recalculates something from memory, gets a slightly different number than the saved script produced, and overwrites the verified value without noticing the discrepancy. The tool catches it. Act on it.

**When registering dependencies**, connect properties at the right granularity. Don't say "the housing depends on the gear" — say "`housing.pocket_bore` depends on `gear.OD`." Property-level edges mean that changing the gear's material doesn't falsely flag the housing bore for review. Think about which specific property actually drives which specific downstream property.

### Node Types and What They Require

Each `record_decision` call specifies a type. The type determines what the tool enforces:

- **`part_selection`** — A real catalog item. Include `catalog_link` and `operating_limits`. Hard-rejected without these in `design`/`build_ready`. Tentative with warning in `exploratory`.
- **`calculated_value`** — A value derived from a formula. Include `script_ref` pointing to the saved calculation script. Soft warning if missing.
- **`assumption`** — Needed to proceed, not yet verified. Include `uncertainty` bounds (e.g., "±20%"). Prominently flagged in all queries and in build-ready audit.
- **`requirement`** — External constraints that don't change unless scope changes. Stored as locked, no warnings.

### Node Properties

Every property on a node is structured:

```json
{
  "value": "<any>",
  "unit": "string or null",
  "confidence": "verified | calculated | estimated | assumed",
  "source": "catalog URL, script path, reference, or null",
  "verified_at": "datetime or null"
}
```

Properties are the atomic unit that edges and constraints reference. A gear node may have many properties (module, tooth_count, OD, bore, face_width, material) and different downstream nodes depend on different ones.

## Before Changing a Value

This is critical and easy to skip under momentum. Before updating a property that already has a recorded value, call `get_cascade(project, node, property)` first. This shows the blast radius — everything downstream that will be flagged for review. Show the cascade to the user before making the change. They need to see the impact and decide whether to proceed, find an alternative, or restructure the approach.

The cascade check prevents "I'll just change this one thing" from silently invalidating six downstream decisions that nobody notices until something doesn't fit during assembly.

After the change, `record_decision` returns the cascade list with edge paths. Each downstream item flagged `needs_review` needs to be addressed:
- Re-derive if it's a `calculated_value`
- Re-verify against new conditions if it's a `part_selection`
- Re-evaluate if it's an `assumption` the change may have invalidated
- Record the update, which clears the flag and may trigger further cascades

Don't leave `needs_review` items hanging. They accumulate and block project promotion.

## Part Selections

Every part selection must be backed by a real catalog listing. This is non-negotiable and exists because projects get burned by phantom parts — seal sizes that don't exist, bearings whose ratings weren't checked against operating conditions.

When recording a part selection:
1. Search for and confirm the part exists in a real catalog first
2. Record the catalog link, confirmed dimensions, and operating limits
3. The tool compares operating limits against application conditions already in the graph (pressure, temperature, speed, media) and flags any that are exceeded

In `design` and `build_ready` phases, the tool rejects part selections without catalog verification. In `exploratory`, it accepts them as tentative but warns. Either way — do the verification at the point of selection, not later. Five minutes of catalog research at selection time prevents hours of rework when a phantom part cascades through the design.

## Constraints

Register a constraint when a physical relationship spans multiple parts or decisions — spatial interference checks, pressure-vs-rating comparisons, flow-capacity-vs-demand checks. These are the cross-cutting validations that catch problems no single decision would reveal.

Two validation types:
- **`numeric`** — Arithmetic expression evaluated automatically when inputs change (e.g., `seal.OD / 2 + bearing.OD / 2 <= center_distance`). Prefer this for anything that can be expressed as math on property values.
- **`manual`** — Description surfaced to Claude with current values when inputs change. Claude evaluates and updates status. Reserve for constraints requiring engineering judgment.

Constraints have a `condition` field specifying when they apply. Design solutions often resolve constraint violations by changing the condition rather than changing the parts — like switching from radial to axial stacking to resolve a clearance interference. If a constraint fails, don't immediately assume the parts need to change. Consider whether the constraint's applicability condition can be legitimately changed.

A failing constraint does NOT block the change that caused it. The change records, the constraint flags as failing, and the response explains what failed. This is intentional — the right fix might be upstream of the constraint, not at the point of failure.

## Branches

When the design hits an unexpected problem that forces a detour — a part doesn't exist, an operating limit is exceeded, a geometric interference is discovered, a proposed geometry can't be machined — open a branch with `start_branch`.

Categories: `part_not_found`, `operating_limit_exceeded`, `geometric_interference`, `manufacturing_constraint`, `dependency_conflict`. These enable pattern analysis — if most branches are `part_not_found`, verification needs to happen earlier and stricter.

The branch records where you were on the main line and what triggered the detour. Work within the branch. Changes are tagged with the branch ID in change logs. Main-line context is preserved.

When resolving with `resolve_branch`, the tool checks that all cascading effects have been handled before allowing closure — no `needs_review` on downstream nodes, no failing constraints on affected nodes. If checks fail, resolution is blocked with a specific list of what's outstanding.

Branches can nest. A branch off a branch is normal — you go sideways to solve a seal problem, which reveals a bearing problem, which reveals a shaft sizing problem. Each gets its own branch. They resolve from the inside out.

## Resources

When a new calculator script, reference document, catalog source, or lesson learned is created during a session, register it with `register_resource`. Tag it to the relevant component. Future sessions working on that component see it automatically in tool responses — no searching required.

Resources surface automatically based on context:
- Recording a `calculated_value` → calculator resources for that component
- Recording a `part_selection` → lessons learned, catalog sources, datasheets
- Checking constraints → reference documents
- Component summary → all resources grouped by type
- A lesson matching the current action surfaces with a warning prefix regardless of action type

The `lesson_learned` type is the most important resource to register. When something goes wrong — a part doesn't exist, a geometry can't be machined, a calculation approach was flawed — the lesson captures what went wrong, why, and the rule going forward. Future tool responses surface relevant lessons at the moment they matter.

## Geometry and Machinability

The navigator tracks values and dependencies but cannot evaluate whether a proposed geometry is actually machinable. Treat every geometry specification as "machinability: unverified" until the user confirms it. Internal channels, curved passages, tight-tolerance bores, unusual features — flag these explicitly for review before building further design decisions on top of them. Failed geometry proposals that require starting over are expensive; flagging uncertainty is cheap.

## Project Promotion

Projects move through `exploratory` → `design` → `build_ready`. Call `promote_project(name, target_phase)` to attempt promotion. The tool runs the full audit.

**To `design`:**
- All part selections have catalog links
- No `invalidated` nodes
- All open branches acknowledged (not necessarily resolved, but documented)

**To `build_ready`:**
- Every part selection: catalog link, confirmed dimensions, operating limits checked, all properties at `verified` confidence
- Every calculated value: script reference
- Every assumption: uncertainty bounds, flagged for test validation
- No `needs_review`, `invalidated`, or `tentative` nodes
- All edges walked — downstream nodes `resolved`
- All numeric constraints `passing` or `condition_not_met`
- All manual constraints evaluated (not `unevaluated`)
- No open branches
- No property modified since last verification (`verified_at >= updated_at`)

Failure returns every specific blocker with why it failed — the actionable punch list.

## Session End

Call `get_session_handoff(project)` before closing. This generates a summary: decisions made, values changed (with before/after and reasons), branches opened and resolved, open items, failing constraints, and suggested next priorities ordered by dependency depth. Review the handoff for accuracy — this is what the next session's Claude uses alongside CORE-Memory to orient without re-explanation.

Propose CORE-Memory ingestion for key decisions and reasoning. The graph owns detailed property history; CORE-Memory carries the narrative context that helps the next session orient quickly. Confirm with the user before committing.

## What NOT To Do

**Don't use the navigator as a scratchpad.** It tracks design decisions, not working calculations or exploratory what-if scenarios. Record values when they're decided, not when they're being explored. If three different gear modules are being tried to see which works, do that math in conversation and record the winner.

**Don't register dependencies speculatively.** An edge represents a real, known dependency between specific properties. "This might affect that" is not an edge — it's a conversation point. Register when you can name the specific upstream property and the specific downstream property it drives.

**Don't skip the graph because it feels faster.** Reading a value from memory instead of calling `get_decision` feels efficient but is how value drift happens. The graph is the source of truth. If the value in context doesn't match the graph, the graph wins unless there's a documented reason to update it.

**Don't ignore resources in tool responses.** When the tool surfaces a calculator or a lesson, it's because the system has learned from experience that this resource is relevant right now. Using an existing validated calculator instead of writing a new one-off calculation eliminates an entire class of errors.

## Tool Reference

For exact parameters and return values on all 16 tools, read `references/tool-quick-reference.md`.
