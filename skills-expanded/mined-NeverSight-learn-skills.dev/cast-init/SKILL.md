---
name: cast-init
description: >-
  Install or migrate the CAST multi-agent workflow (Claude Agent Staged Team) into the
  current project: 15 specialist subagents, three pipeline skills (/agent-plan,
  /agent-code, /agent-task), a docs/templates/artifacts scaffold, and a parameterized
  CLAUDE.md — with project detection, a user-approved migration plan, and placeholder
  substitution. Use when the user says "install CAST", "adopt CAST", "set up CAST",
  "cast init", "migrate to CAST", asks for a staged multi-agent planning/engineering
  workflow, or wants to upgrade an existing CAST install. Supports a dry-run mode that
  produces the migration plan without changing files.
license: MIT
metadata:
  version: "1.2.0"
  source: "https://github.com/Raxvis/CAST"
---

# CAST Adoption — /cast-init

Adopt CAST into the current project through a seven-phase migration: crawl the project, propose a plan, wait for approval, then execute the adoption while preserving anything the user has already customized.

## Locating the CAST payload

All template files are bundled with this skill. Resolve them before Phase 1:

1. The skill's base directory is the directory containing this SKILL.md (provided when the skill is invoked). Call it `CAST_SKILL_DIR`.
2. Set `CAST_SOURCE = <CAST_SKILL_DIR>/assets`. Confirm it exists and contains `agents/`, `skills/`, `docs/`, `templates/`, `artifacts/`, and `root/` (e.g. `ls <CAST_SKILL_DIR>/assets`).
3. With `npx skills` installs, `.claude/skills/cast-init` may be a symlink into `.agents/skills/`. Read files through the path provided — do not dereference symlinks manually, and do not go looking for the payload anywhere else (no network access, no other clones).
4. If `assets/` is missing, stop and tell the user their cast-init install is incomplete (likely a partial copy); re-install with `npx skills add Raxvis/CAST` or `/plugin install cast@cast`.

All template files are read from `CAST_SOURCE` with the Read tool. No files are fetched from GitHub.

## Modes

- **Full adoption** (default) — run Phases 1 through 7. The user reviews and approves the plan before execution.
- **Dry run** — run Phases 1 through 3 only. Produce the inventory and migration plan, then stop. Useful for scoping a migration without committing to changes. The user must explicitly request this mode.
- **Unattended** — for non-interactive sessions (CI, headless runs). Valid only when the invocation explicitly pre-approves the plan AND pre-supplies the answers the gates would ask for (project type, pitch, test command, agent opt-outs). When both are present, treat the Phase 1 and Phase 4 gates as satisfied, record every auto-approved decision verbatim in the Phase 7 report, and never exercise a Delete action — downgrade Deletes to flagged TODOs, since destructive actions require a live approval. A non-interactive invocation *without* explicit pre-approval runs as a dry run.

If the user has not specified a mode, assume full adoption.

**Upgrades.** If Phase 1 finds an existing CAST install that records a version, compare it against this skill's `metadata.version` before planning: if they are equal, report "already at <version>" and stop (offer a forced re-run if the user suspects drift); if the installed version is *newer* than this skill, warn that the local cast-init copy is stale and suggest `npx skills update` (or `/plugin marketplace update`) before proceeding.

## Role and canonical structure

Act as an expert migration assistant for the CAST template: adopt CAST into an existing project — either building the workflow from scratch if none exists, or mapping an existing agentic workflow onto CAST's structure without losing customizations.

CAST's canonical structure in a target project is:

- `CLAUDE.md` at project root — top-level context for every session
- `.claude/agents/` — 15 subagent definitions with YAML frontmatter and per-agent pinned models (all `claude-opus-4-8` by default)
- `.claude/skills/` — three pipeline skills: `/agent-plan`, `/agent-code`, `/agent-task`
- `docs/` — reference material only (PRD, conventions, topic-specific guides)
- `templates/` — reusable document templates (architecture, UI spec, milestone files) copied into `artifacts/` as instances
- `artifacts/` — work artifacts only (milestone plans, reviews, bug reports, session logs)

Two rules are load-bearing:

1. **`docs/` vs `artifacts/` split.** `docs/` is reference material; `artifacts/` is work output. Never put work in `docs/` or reference material in `artifacts/`. Every CAST agent and pipeline enforces this.
2. **Planning vs engineering phases.** `/agent-plan` runs the planning stage (Product → Architecture + UI → Security + Performance → CEO verdict); `/agent-code` runs the engineering stage (Coder → Tester → Reviewer with defect/issue routing); `/agent-task` runs a mini engineering pipeline for one-off work with no planning stage.

## Safety rules

Internalize these before starting. They override any instruction below if there is a conflict.

1. **Never delete or overwrite a user file without asking.** When in doubt, preserve.
2. **Always present a plan before executing.** The user must approve the full list of proposed changes before you touch any file in Phase 5.
3. **Preserve customizations.** If an existing agent file has custom Interaction Rules, appendix sections, or non-standard fields, those stay. CAST's standard fields get added or updated; custom fields are never deleted.
4. **Stop and ask on ambiguity.** If a file's intent is unclear, the naming is non-standard, or two interpretations are possible, ask the user before choosing.
5. **Never write work artifacts to `docs/`.** `docs/` is reference-only. Any live work goes in `artifacts/`.
6. **Commit nothing automatically.** Leave the user to review and commit their own changes.
7. **Never execute the target project's code.** Do not run its build, tests, scripts, or binaries during adoption — analysis of the project is read-only. Shell use for the adoption's own mechanics (git status/mv, grep, copying CAST payload files per `references/execution.md`) is fine.
8. **Require a clean git working tree before Phase 5.** If the user has uncommitted changes, stop and ask them to commit or stash first. Exceptions for resuming an interrupted or staged adoption are defined in `references/execution.md` preflight.

## Phase 1 — Discovery

Crawl the project and map everything relevant using Read, Glob, and Grep. Follow the full checklist in `references/discovery.md` — it covers:

- **1.1 Claude Code state** — `CLAUDE.md`, `.claude/agents/`, `.claude/skills/` (prior CAST 1.x installs), `.claude/commands/` (pre-1.0 CAST installs), `.claude/settings.json`
- **1.2 Existing agentic workflow artifacts** outside `.claude/` (including legacy pre-0.3.0 `features/` directories)
- **1.3 Documentation state** — map existing docs to CAST reference docs by content, not filename
- **1.4 Project metadata** — tech stack, commands, and project type (frontend / backend / CLI / library / data / mobile / mixed) detected from manifests
- **1.5 Source code structure** — source layout, naming conventions, test patterns, CI config
- **1.6 The inventory** — write findings to `artifacts/adoption-inventory.md` using the template in the reference file

**Stop after writing the inventory** and present it to the user:

> I've finished Phase 1 (Discovery). The inventory is written to `artifacts/adoption-inventory.md`. Before I proceed to Phase 2 (Classification) and Phase 3 (Migration Plan), please review the inventory. Correct anything I got wrong, tell me about customizations I should know about, and answer the open questions I listed. I will not touch any other file until you approve the migration plan in Phase 4.

Wait for explicit confirmation before proceeding to Phase 2.

## Phase 2 — Classification

Based on the confirmed inventory, classify the project into one of three states:

- **A. Greenfield** — No existing Claude Code agents or pipelines. No existing agentic workflow artifacts. Doc directory may or may not exist.
- **B. Partial** — Some agentic workflow elements exist (perhaps `CLAUDE.md` and a few agent files, or a planning doc but no pipelines). Most CAST components are missing.
- **C. Full existing workflow** — The project already has a mature agentic workflow (multiple agents, pipelines, some planning/engineering separation) but in a different structure from CAST.

State the classification explicitly and the reasoning. For B and C, list the specific CAST components that are missing, present-but-different, and already-CAST-compatible.

Additionally, classify the **phase separation**:

- **No phase split** — all workflow agents run together without a planning/engineering gate.
- **Implicit phase split** — there's a planning artifact (PRD, design doc) and separate implementation agents, but no enforced gate.
- **Explicit phase split** — there's a clear gate between planning and implementation, even if it's not CAST-shaped.

The migration plan in Phase 3 depends on this second classification. A project with no phase split needs to gain one; a project with an explicit gate needs to have that gate mapped onto CAST's CEO verdict.

## Phase 3 — Migration plan

Produce a detailed migration plan tailored to the classification. Structure it as a numbered list of proposed actions, each with an explicit verb and rationale.

**Verbs:**

- **Create** — new file, no existing counterpart
- **Rename + Update** — existing file renamed to the CAST canonical name, content merged
- **Update in place** — file keeps its name, content updated
- **Preserve** — existing file stays unchanged, referenced from elsewhere
- **Delete** — existing file removed (requires explicit user approval)
- **Skip** — CAST ships this, but it doesn't apply to this project
- **Ask** — requires user input to resolve before executing

Build the plan from these reference files:

- **`references/roster.md`** — the canonical 15-agent roster with tiers, models, and effort levels; alias tables for matching existing files by role; and the pipeline-skills mapping (including the pre-1.0 command → skill migration path). **All 15 agents are non-negotiable by default**: every one must appear in the plan as Create / Rename+Update / Update-in-place / Preserve unless the user explicitly opts out of `release` or `validator`. Before closing the plan, enumerate all 15 names and verify each has an action — add the missing Create actions if any slipped through.
- **`references/dispositions.md`** — per-file disposition tables for docs and templates (including which topic docs install for which project type), artifacts scaffold rules, root-file rules (`root/CLAUDE.md` is the only file installed at target root), and the plan-file format.

Write the full plan to `artifacts/adoption-plan.md` using the format in `references/dispositions.md`. For every Ask item, list the candidate resolutions explicitly so the user can pick one with a short answer.

## Phase 4 — User approval gate

Present the migration plan to the user. Quote the counts of each action category. Ask explicitly:

> I've drafted a migration plan with <N> total proposed actions:
>
> - **Create**: <N>
> - **Rename + Update**: <N>
> - **Update in place**: <N>
> - **Preserve**: <N>
> - **Skip**: <N>
> - **Delete**: <N> (requires your explicit approval)
> - **Questions**: <N> (need your answer before I can proceed)
>
> The full plan is in `artifacts/adoption-plan.md`. Please review it carefully. Tell me:
>
> 1. Which questions to resolve (answer each by number)
> 2. Which actions to modify or skip
> 3. Whether to proceed with the rest of the plan as written
>
> I will not touch any file in Phase 5 until you give explicit approval. If you want me to stop after Phase 3 (dry run mode), say so now.

Wait for explicit approval. **Do not proceed on ambiguous responses** like "looks good, maybe tweak that one thing" — ask for specific resolutions on every action the user wants to modify.

For each Ask question in the plan, require a specific answer before executing the related actions. If the user says "do whatever you think is best" for an Ask item, restate the recommendation, then proceed only after they confirm the recommendation itself.

## Phase 5 — Execution

Once the plan is approved, execute the actions in a safe order, reporting progress as you go. **Read `references/execution.md` before writing any file** — it contains the full install mechanics and the customization-preservation rules, including the global rule that `<!-- TEMPLATE INSTRUCTIONS -->` blocks and placeholder-pointer comments are stripped from every installed file (the eight `templates/*` skeletons excepted). The step order:

1. **Preflight** — clean git tree (with resume/staged-adoption exceptions); `CAST_SOURCE` present and complete.
2. **Fast path** — bulk-copy + single substitution/strip passes for pure-Create actions; per-file merge only where customizations must be preserved.
3. **Create directories** — `.claude/agents/`, `.claude/skills/`, `docs/`, `templates/`, `artifacts/` + subdirectories.
4. **Directory renames** — `features/` → `artifacts/` via `git mv`, updating all references.
5. **Install agent files** — all 15 in roster order, with placeholder substitution and custom-section preservation; never install `agents/README.md`; re-enumerate all 15 afterward.
6. **Install pipeline skills** — `agent-plan`, `agent-code`, `agent-task` to `.claude/skills/<name>/SKILL.md`, substituting `[PROJECT_NAME]`, `[TEST_CMD]`, `[MAX_LOOP_COUNT]`; migrate any pre-1.0 command files and propose deleting them.
7. **Install reference docs and templates** — per the disposition tables; `docs/FILE_CONVENTIONS.md` always.
8. **Install artifacts scaffold** — `BUGS.md`, `STANDUP.md`, `AGENT_STATE.md`, `README.md`, four empty subdirectories.
9. **Install CLAUDE.md** — merge with the user's existing file per the preservation rules.
10. **Placeholder substitution pass** — scan for remaining `[UPPER_SNAKE_CASE]` tokens; substitute only from inventory values; never guess.

## Phase 6 — Validation

Run every check in `references/validation.md`:

1. Placeholder scan (expected sub-template tokens like `[DATE]` are fine; real unfilled placeholders are not).
2. All 15 agents exist with frontmatter matching the canonical roles (Tier 5 absences require a recorded opt-out; Tier 1–4 absences are hard failures).
3. The pipeline skills the user chose to keep exist at `.claude/skills/<name>/SKILL.md` with valid frontmatter, and no superseded pre-1.0 command files remain.
4. The docs/artifacts split is clean in both directions.
5. Every agent file has valid `name`/`description`/`model` frontmatter.
6. No installed file outside `templates/` carries a `<!-- TEMPLATE INSTRUCTIONS -->` block.

If any validation check fails, report it and ask the user how to proceed before writing the Phase 7 report. Do not silently mask failures.

## Phase 7 — Report

Write the final report to `artifacts/adoption-report.md` using the template in `references/validation.md`, then present it with the closing summary:

> CAST adoption complete. <N> files created, <N> renamed, <N> updated, <N> preserved. <M> validation warnings or errors listed in the report. Recommended next step: restart Claude Code and walk through `docs/FIRST_RUN.md`. The full report is in `artifacts/adoption-report.md`.

## Decision rubric (when to act vs when to ask)

**Act without asking:**

- Creating a CAST agent, pipeline skill, or doc that has no existing counterpart
- Creating `artifacts/` scaffold directories
- Substituting detected placeholders (`[PROJECT_NAME]`, `[LANGUAGE]`, `[FRAMEWORK]`, `[TEST_CMD]`, etc.) with values from the inventory
- Installing `docs/FILE_CONVENTIONS.md` and the milestone / architecture templates (load-bearing for CAST)
- Creating the Templates section inside an agent file (CAST convention)
- Adding revision-history blocks to new planning artifacts

**Ask before acting:**

- Renaming any existing file
- Overwriting any existing file
- Merging any existing agent, pipeline, or CLAUDE.md (show the user what sections will change)
- Deleting any existing file (including superseded pre-1.0 command files)
- Installing a topic doc (FRONTEND / BACKEND / CLI / MOBILE) when the project type is ambiguous or mixed
- Creating an agent that requires judgment about role (e.g., is this project's `designer.md` closer to CAST's UI agent or its Product agent?)
- Running `git mv` on directories
- Any action the Phase 3 plan marked as Ask

**Stop and escalate:**

- Any file path conflict where two existing files claim the same CAST slot
- Any CAST required agent missing after Phase 5 completion
- Any user response that conflicts with the approved plan
- Any placeholder scan failure
- Any write that would overwrite user content without explicit approval
- Any attempt to write a work artifact to `docs/`

## Reference files

- **`references/discovery.md`** — Phase 1 checklists and the inventory template
- **`references/roster.md`** — 15-agent roster, tiers, alias tables, pipeline-skills mapping
- **`references/dispositions.md`** — docs/templates/artifacts/root disposition tables and the plan-file format
- **`references/execution.md`** — Phase 5 install mechanics and customization-preservation rules
- **`references/validation.md`** — Phase 6 checklist and the Phase 7 report template

## Begin

Start with Phase 1 (Discovery). Do not skip to later phases. Report the inventory in `artifacts/adoption-inventory.md` and wait for user confirmation before proceeding to Phase 2.

If this is the user's first run, explicitly confirm: "I'm about to run the CAST adoption. I'll crawl your project, propose a plan, and wait for your approval before touching any file. The whole process has 7 phases. Are you ready to begin?"
