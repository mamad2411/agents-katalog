---
name: slicing-stories
description: Splits a Feature Brief into an ordered slice map of thin, vertical story slices — each capturing scope and build order, while deferring detailed acceptance criteria to downstream clarifying-intent. Use when a feature is too large for one story and needs to be broken into deliverable increments with a build sequence.
context: fork
allowed-tools: Read, Grep, Glob
---

# Agile Story Slicer

## Overview

Take a Feature Brief and split it into an ordered **slice map** — a sequence of thin, vertical story outlines. Each slice captures what the story covers and where it sits in the build order, but intentionally omits detailed acceptance criteria, tasks, and implementation plans. Those emerge downstream when each slice is specced individually and TDD drives the design.

**Consumes** a Feature Brief (canonically from `clarifying-intent`, or any feature-shaped input — see the Input preflight). **Emits** a slice map. What happens to each slice afterward — per-slice speccing, design, TDD — is downstream and not this skill's concern; the orchestrator sequences it.

## Input

A **Feature Brief** — canonically from `clarifying-intent`, but the gate is on the artifact's **shape, not its provenance**. A Feature Brief carries:

- Problem / why now
- Goal & success criteria
- Scope boundaries (in / out)
- Constraints & risks (if surfaced)
- Open questions (blocking / deferrable)

Pass it inline in the prompt, or as a path/handle this skill should read.

**Preflight — route on shape, not on where the input came from:**

1. **A conforming Feature Brief** (whatever produced it) → slice it directly.
2. **Feature-shaped input that isn't a formal Brief** — a PRD paragraph, an epic description, or a loose feature request that clearly spans several behaviors → synthesize the five Brief fields from what's given, record every inference in the slice map's `meta.assumptions[]`, and set `meta.source` to the real origin (e.g. `"synthesized from user-supplied feature description"`). Then slice. Don't stop merely because the input didn't arrive as a Brief — degrade gracefully and make the gaps visible.
3. **Input too thin to slice** — you cannot even state the feature's goal or name one deliverable behavior → return `## Blocking Questions` with the specific unknowns and stop. This is the only hard stop; reserve it for genuinely un-sliceable input, not for missing Brief formatting.

## Output

Return both inline in the response:

1. A human-readable **Slice Map (Markdown)** for reading/review.
2. A canonical **Slice Map (JSON)** that conforms to `references/slice-map.spec.md` (in a fenced `json` block).

Treat the JSON as the source of truth; the Markdown should be derivable from the JSON.

**Machine-readable status.** The JSON's `meta.status` is the routing signal an orchestrator branches on (`craft` consumes it — see `craft/references/contracts.md`):

- `complete` — a usable slice map was produced (including a single-slice map; see the sizing check in step 1).
- `blocked` — blocking open questions prevent slicing. Return `meta.status: "blocked"` in a minimal JSON object (valid `meta`, empty `slices`) **and** list the questions under a `## Blocking Questions` heading, then stop.

Persistence: the caller decides. When invoked standalone and the map is worth keeping, offer to save the JSON at `.praxis/<slug>/slice-map.json` and the Markdown at `.praxis/<slug>/slice-map.md`.

**Caller-side helpers** (this skill is read-only and does not run them; the caller or CI does, against a persisted JSON path — resolve the plugin root with `${CLAUDE_PLUGIN_ROOT}`):

- `python3 "${CLAUDE_PLUGIN_ROOT}/skills/slicing-stories/scripts/validate_slice_map.py" <path>` — validate the JSON against the spec (a good deterministic gate before trusting a persisted map).
- `python3 "${CLAUDE_PLUGIN_ROOT}/skills/slicing-stories/scripts/render_slice_map_markdown.py" <path>` — render Markdown from the JSON.

## Workflow

1. **Accept the Feature Brief (per the Input preflight).**
   - Trust the brief's scope, constraints, and open questions. Do not re-interview the requester.
   - If you synthesized the brief in preflight branch 2, carry every inference into `meta.assumptions[]` and set `meta.source` accordingly — surface the gaps, don't silently fill them.
   - **Sizing check — don't manufacture splits.** If the brief already describes a single story-sized, INVEST-passing behavior (splitting it would just reproduce the whole as one slice), return a **single-slice map** whose `sequence_rationale` says "already story-sized — no split needed," with `meta.status: "complete"`. This is the honest answer to "is this too big?" being *no*; the caller proceeds straight to speccing that one story. Only split when there are genuine seam lines.
   - If there are blocking open questions that prevent slicing, return `meta.status: "blocked"`, list them under `## Blocking Questions`, and stop. The caller resolves them with the user and re-invokes this skill.

2. **Identify seam lines.**
   - Find natural boundaries where the feature can be split into independently deliverable, testable behaviors.
   - Apply slicing heuristics (see `references/templates.md`):
     - Start with a walking skeleton — the thinnest end-to-end path that delivers value to one real user with one real integration. Use real dependencies (a real IdP, a real database, a real API), not stubs or test doubles. The skeleton proves the architecture BY delivering value, not instead of it.
     - Then add: validation/error states, edge cases, permissions/roles, performance/accessibility, telemetry.
     - Split by persona, workflow step, data subset, or capability tier (read → create → edit → bulk).
   - Each slice must be a vertical cut (end-to-end behavior), not a horizontal layer (frontend-only, backend-only).
   - **Spikes are not slices.** If you need to validate a technology or integration before committing, that's a spike — a time-boxed throwaway experiment, not a user story. Don't dress a spike in a user story format with a fake "so that" clause. Capture it in the slice map's `meta.spikes[]` (id, the question it answers, a timebox) so the caller can schedule it as risk-reduction before the dependent slice — the spike stays visible in the artifact instead of being routed off to another skill.

3. **Order the slices.**
   - Sequence so that earlier slices lay foundations for later ones.
   - The first slice should be the walking skeleton: the thinnest end-to-end path that delivers value to one real user with one real integration.
   - For each slice, write a brief `sequence_rationale` explaining why it's in this position.

4. **Produce the slice map.**
   - For each slice, produce:
     - `title`: short, outcome-focused.
     - `story`: "As a X, I want Y, so that Z."
     - `scope_in`: what this slice covers.
     - `scope_out`: what is explicitly deferred to other slices.
     - `sequence_rationale`: why this slice is in this position.
     - `open_unknowns` (optional): deferrable unknowns specific to this slice.
   - Do **not** write acceptance criteria — that's `clarifying-intent`'s job when it specs each slice.

5. **Validate.**
   - **INVEST check** — for each slice, verify:
     - **I**ndependent — can be reprioritized relative to other slices (some sequencing is inevitable, but minimize hard dependencies).
     - **N**egotiable — scope can be adjusted without invalidating the slice.
     - **V**aluable — delivers value to a real user, not just to the team. Apply the litmus test: "If we shipped this slice and stopped, would at least one real user get value from it?" If the answer is "only if combined with a later slice," it's not independently valuable — merge it with the slice it depends on, or restructure so it delivers value on its own.
     - **E**stimable — scope is clear enough to estimate effort.
     - **S**mall — fits within a sprint.
     - **T**estable — acceptance criteria can be written and verified.
   - **Additional checks:**
     - Does the first slice (walking skeleton) deliver value to a real user with a real integration, not just prove architecture with stubs?
     - Are `scope_in` boundaries clear enough that `clarifying-intent` can spec the slice without asking "what are we building?"
     - Do `scope_out` boundaries prevent overlap between slices?
     - Is anything in the `slices` array actually a spike (technology validation, integration proof) rather than a user story? If so, move it to `meta.spikes[]` and remove it from `slices`.

## Downstream Handoff

Each slice is specced individually into a Story-Level Behavioral Spec (canonically by `clarifying-intent`) before implementation. The sequence in the slice map determines build order.

**Feedback loop**: The slice map is a living artifact, not a frozen plan. When speccing or implementing a later slice reveals that the boundaries, ordering, or number of slices need to change — update the slice map. Common triggers:

- Implementing slice N reveals slice N+1 should be split or merged.
- A deferrable unknown becomes blocking and forces reordering.
- A slice turns out to be trivial and should be absorbed into an adjacent slice.
- New behavior is discovered that doesn't fit any existing slice.

When updating, re-validate (step 5) and re-confirm with the requester. Don't treat slice map changes as failures — they're the agile feedback loop working at the planning level.

## References and Tools

- Templates and slicing heuristics: `references/templates.md`
- Output schema: `references/slice-map.spec.md`
- Optional validator (run on a persisted JSON path): `python3 scripts/validate_slice_map.py <path>`
- Optional Markdown renderer (run on a persisted JSON path): `python3 scripts/render_slice_map_markdown.py <path>`
