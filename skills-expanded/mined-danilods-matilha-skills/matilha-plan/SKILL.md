---
name: matilha-plan
description: Use when user wants to plan a feature with multiple subprojects or parallel work — generates phase-gated spec.md and plan.md with waves, SPs, merge_order, and exit gates.
category: matilha
version: "1.0.0"
optional_companions: ["superpowers:brainstorming", "superpowers:writing-plans"]
---

## When this fires

User has Phase 10 research (or skips scout) and wants spec + plan artifacts before dispatching work. Produces `docs/matilha/specs/<slug>-spec.md` + `docs/matilha/plans/<slug>-plan.md`.

## Preconditions

- None. matilha-plan lazy-bootstraps project structure as needed.

## Execution Workflow

1. **Lazy bootstrap**: Check for `project-status.md` and `docs/matilha/`. If absent, create minimally:
   - `mkdir -p docs/matilha/specs docs/matilha/plans docs/matilha/research`
   - If `project-status.md` missing, write a minimal stub with frontmatter `current_phase: 10`, `phase_status: in_progress`, `project_slug: <derived from cwd or user-provided>`, `next_action: "matilha-plan in progress"`. User can later run matilha-init for fuller bootstrap.
   - Then read `project-status.md` and any existing research in `docs/matilha/research/`.
2. **Pack-aware brainstorming delegation** (see `matilha-compose` for canonical template):
   - (a) If `superpowers:brainstorming` is available, inspect the ambient skill list for skills with plugin namespace matching `matilha-*-pack` (installed companion packs). Group by plugin namespace.
   - (b) Classify user intent semantically against each installed pack's domain using the pack skills' descriptions visible in the ambient list. Err inclusive — prefer injecting a marginally-relevant pack over omitting it.
   - (c) Build preamble using the canonical template documented in `skills/matilha-compose/SKILL.md` Step 4 (per-pack mini-synthesis + skill list + guidance paragraph for the receiving skill).
   - (d) Emit the preamble in the current turn output, then invoke `superpowers:brainstorming` via the Skill tool.
   - (e) Fallback: if `superpowers:brainstorming` is absent OR zero packs are detected, run the condensed clarifying flow inline (existing behavior — ask 3–5 questions drawing on detected pack skills if any, else use methodology-core heuristics).
3. Write `docs/matilha/specs/<slug>-spec.md` with: purpose, context, design principles, target deliverables, architecture, data flow, open questions, exit criteria.
4. If `superpowers:writing-plans` available, invoke via Skill tool to generate the task-by-task plan. Otherwise, write the plan inline following `methodology/40-execucao.md` conventions.
5. Plan output lands at `docs/matilha/plans/<slug>-plan.md` with: goal, architecture, SPs, per-task steps, exit gates.
6. Update project-status.md: `current_phase: 30`, `phase_status: complete`, `feature_artifacts` appended, `next_action: "Run /matilha-hunt <slug>"`.

## Rules: Do

- Delegate to superpowers when present (their brainstorming + writing-plans are battle-tested).
- Validate plan against `planSchema` before writing.

## Rules: Don't

- Skip the spec (even for small features — the spec is the contract).
- Advance `current_phase` past 30 without user approval.

## Expected Behavior

User gets two artifacts ready for hunt/gather. Plan must be directly executable via subagent-driven-development or manual hunt.

## Quality Gates

- Spec exists at `docs/matilha/specs/<slug>-spec.md`.
- Plan exists at `docs/matilha/plans/<slug>-plan.md` and parses against `planSchema`.
- `current_phase: 30` in project-status.md.
- `feature_artifacts` entry added.

## Companion Integration

Companion-pack awareness is handled via the pack-aware preamble-injection logic in Step 2 of the Execution Workflow. See `skills/matilha-compose/SKILL.md` for the canonical pack detection, intent classification, and preamble template.

- **superpowers:brainstorming** — invoked in step 2 with pack-aware preamble emitted in the current turn output (when installed companion packs classify as intent-relevant).
- **superpowers:writing-plans** — invoked in step 4 for task-by-task plan generation. No preamble needed here (plan-generation is post-spec; pack context is already embedded in the spec).
- **Any skill with plugin namespace `matilha-*-pack`** (e.g., `matilha-harness-pack:*`, `matilha-ux-pack:*`, `matilha-growth-pack:*`) — detected at runtime via ambient skill list, referenced by name in the preamble, available for direct invocation downstream.
- Otherwise: run the clarifying + drafting inline using methodology-core heuristics.

## Output Artifacts

- `docs/matilha/specs/<slug>-spec.md`
- `docs/matilha/plans/<slug>-plan.md`
- Updated `project-status.md`

## Example Constraint Language

- Use "must" for: spec and plan both exist; plan conforms to `planSchema`.
- Use "should" for: invoke superpowers when available; validate disjunction across intra-wave SPs.
- Use "may" for: skip research if user has a clear mental model.

## Troubleshooting

- **"planSchema fails"**: Check frontmatter shape vs `methodology/40-execucao.md`.
- **"research missing"**: Run matilha-scout first, or acknowledge the skip explicitly.

## CLI shortcut (optional)

> If matilha CLI is installed (`matilha --version` succeeds), you can run
> `matilha plan <slug>` to execute this deterministically. The plugin path
> above works without any CLI installation.
