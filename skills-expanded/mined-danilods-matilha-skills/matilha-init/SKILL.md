---
name: matilha-init
description: Use when starting a new project or initializing Matilha in an existing one — scaffolds project-status.md, AGENTS.md, CLAUDE.md/GEMINI.md, and phase 0 artifacts.
category: matilha
version: "1.0.0"
optional_companions: []
---

## When this fires

User is at the start of a project (no `project-status.md`) or wants to bootstrap Matilha into an existing codebase. The skill scaffolds the minimum artifacts for Matilha to work: `project-status.md` with initial phase 0 state, `CLAUDE.md` / `AGENTS.md` / `GEMINI.md` as context primers, and the directory scaffold (`docs/matilha/`, `docs/superpowers/`).

## Preconditions

- Write access to cwd.
- No existing `project-status.md` unless user explicitly confirms overwrite.

## Execution Workflow

1. Verify preconditions via Bash `test -f project-status.md`. If present and user didn't say "force", ask the user before overwriting.
2. Prompt the user for `archetype` (one of: `saas-b2b`, `saas-b2c`, `frontend-only`, `cli`, `library`, `ml-service`, `marketplace`).
3. Compute ISO-UTC timestamp via Bash `date -u +%Y-%m-%dT%H:%M:%SZ`.
4. Write `project-status.md` via Write tool. Frontmatter shape: `schema_version: 1`, `name`, `archetype`, `created: <iso>`, `last_update: <iso>`, `current_phase: 0`, `phase_status: not_started`, `next_action: "Run /matilha-scout to enter Phase 10 discovery."`, `tools_detected: []`, `companion_skills: {impeccable: not_installed, shadcn: not_installed, superpowers: not_installed, typeui: not_installed}`, `active_waves: []`, `completed_waves: []`, `feature_artifacts: []`, `recent_decisions: []`, `pending_decisions: []`, `blockers: []`, `aesthetic_direction: null`, `design_locked: false`.
5. Write `CLAUDE.md` / `AGENTS.md` / `GEMINI.md` if absent (copy from this repo's templates if available via `matilha pull`, else from skeletons).
6. Create directories `docs/matilha/plans`, `docs/matilha/specs`, `docs/matilha/waves` via Bash `mkdir -p`.
7. Emit final message: "Initialized Matilha — current_phase: 0. Next: /matilha-scout".

## Rules: Do

- Respect explicit overwrite confirmation; do not silently clobber.
- Use ISO-UTC timestamps throughout.
- Create docs/ directories idempotently (skip if they exist).

## Rules: Don't

- Overwrite existing `project-status.md` without explicit user confirmation.
- Guess archetype from code (ask).
- Use local-time timestamps.

## Expected Behavior

On success, user has a Matilha-initialized project with the 3 context files + project-status.md. Next skill the user invokes is typically `matilha-scout` (Phase 10) or `matilha-plan` (Phase 20-30) if they already have research.

## Quality Gates

- `project-status.md` exists with valid frontmatter (conforms to `projectStatusSchema`).
- `docs/matilha/` directory tree exists.
- Context files (CLAUDE.md / AGENTS.md / GEMINI.md) exist.
- User can run `matilha-howl` next and see phase 0 state.

## Companion Integration

No companion integrations in Wave 4a. Future packs may extend this skill.

## Output Artifacts

- `project-status.md`
- `CLAUDE.md` (if absent)
- `AGENTS.md` (if absent)
- `GEMINI.md` (if absent)
- `docs/matilha/plans/`
- `docs/matilha/specs/`
- `docs/matilha/waves/`

## Example Constraint Language

- Use "must" for: project-status.md conforms to `projectStatusSchema`; ISO-UTC timestamps.
- Use "should" for: prompt interactively for archetype; skip overwrite of existing context files.
- Use "may" for: scaffold additional directories beyond the required ones if user requests.

## Troubleshooting

- **"project-status.md already exists"**: User confirms overwrite explicitly, or chooses a different directory.
- **"archetype not recognized"**: Must be one of `saas-b2b`, `saas-b2c`, `frontend-only`, `cli`, `library`, `ml-service`, `marketplace`; ask user to pick from the list.

## CLI shortcut (optional)

> If matilha CLI is installed (`matilha --version` succeeds), you can run
> `matilha init` to execute this deterministically. The plugin path
> above works without any CLI installation.
