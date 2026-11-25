---
name: openpencil-design-orchestrator
description: Orchestrate Pencil/OpenPencil design work through MCP using a staged workflow: preflight, planning, skeleton, section content, refinement, and safe fallback. Use when working with Pencil/OpenPencil, .fig/.pen design files, MCP-based design editing, or when Claude Code, Codex, Cursor, or Windsurf needs reliable prompt patterns, client setup guidance, and risk controls for AI-assisted design changes.
---

# OpenPencil Design Orchestrator

Use this skill to turn vague Pencil/OpenPencil requests into a controlled multi-step workflow.
Default to MCP-first execution. Prefer small, verifiable edits over one-shot generation.

## Quick Start

1. Run `scripts/preflight-check.sh` when the environment or MCP connectivity is unknown.
2. Read `references/prompt-framework.md` before drafting or executing prompts.
3. Read `references/client-adapters.md` when the user mentions Claude Code, Codex, Cursor, or Windsurf setup.
4. Read `references/risk-matrix.md` when debugging failures or choosing guardrails.
5. Read `references/fallback-mode.md` when MCP is unavailable or unstable.

## Workflow

### Step 1 - Preflight

- Confirm Pencil/OpenPencil is running if the workflow depends on desktop-hosted MCP.
- Confirm whether transport is `stdio` or `HTTP`.
- Confirm `openpencil-mcp` is installed when using MCP.
- Read the current file/page tree before proposing mutations.
- Refuse giant blind edits when the current structure is unknown.

### Step 2 - Planning

- Translate the request into pages, sections, components, tokens, and execution order.
- Resolve ambiguity before editing.
- Ask for confirmation only when ambiguity materially changes layout or scope.
- Prefer explicit checkpoints over creative guessing.

### Step 3 - Skeleton

- Create only structural scaffolding: pages, frames, sections, containers, autolayout, naming.
- Avoid visual polish and long-form copy generation in this phase.
- Keep hierarchy obvious and reusable.

### Step 4 - Section Content

- Edit one section at a time.
- Re-read the relevant nodes before each mutation batch.
- Report what changed: nodes touched, nodes created, styles/tokens applied, unresolved conflicts.
- Stop when cross-section drift appears.

### Step 5 - Refinement

- Refine spacing, alignment, typography consistency, color/token consistency, and emphasis hierarchy.
- Avoid restructuring information architecture unless the user explicitly requests it.
- Preserve the approved skeleton.

### Step 6 - Save / Handoff

- Save only after confirming the changed scope.
- Summarize what changed and any remaining weak spots.
- Offer a next pass rather than silently widening the change scope.

## Core Operating Rules

- Prefer MCP-first workflows; use file-level fallback only when MCP is unavailable or unsuitable.
- Prefer `stdio` for local interactive use and `HTTP` for controlled automation or remote workflows.
- Treat `eval` as high risk. Do not rely on it by default. When using HTTP mode, keep `eval` disabled unless the user explicitly accepts the risk.
- Prefer staged prompts over one-shot “design the whole app” prompts.
- Keep each mutation batch bounded to a page or section whenever possible.
- Re-read tree/node context before writing.
- Stop and report conflicts instead of improvising through them.

## Reference Routing

- For prompt wording and reusable templates, read `references/prompt-framework.md`.
- For exact phase ordering and mutation discipline, read `references/workflow-sequence.md`.
- For agent/client-specific setup patterns, read `references/client-adapters.md`.
- For failure modes, mitigations, and known risks, read `references/risk-matrix.md`.
- For degraded-mode operation without MCP, read `references/fallback-mode.md`.

## Scripts

- `scripts/preflight-check.sh`
  - Check whether `openpencil-mcp` exists.
  - Inspect common MCP config locations.
  - Print a short readiness report.
- `scripts/scaffold-phase-prompt.py`
  - Generate phase-specific prompt scaffolds for `planning`, `skeleton`, `section`, `refine`, and `safety`.

## Task Fit Guidance

Use this skill for:

- Pencil/OpenPencil MCP orchestration
- staged design prompt generation
- design read/write workflows through coding agents
- design audits, diff reviews, export checks, and token/consistency analysis

Do not use this skill as the primary path for:

- unconstrained one-shot whole-product generation
- unreviewed destructive bulk edits
- security-insensitive automation that assumes unrestricted `eval`
- fake/live-edit claims when running in fallback-only mode

## Output Expectations

When using this skill, structure the response around:

1. Current mode (`MCP-first`, `HTTP automation`, or `fallback`)
2. Current phase
3. Exact scope being changed
4. Risks / blockers
5. Next action

Keep outputs operational. Do not bury the active scope or failure condition inside long prose.
