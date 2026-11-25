---
name: nch-dev
description: 'Implements a ready-for-dev spec produced by nch-spec (or any spec with compatible status frontmatter), producing clean working code that follows the project''s existing architecture, patterns and conventions, hardened by an adversarial review loop. Also handles trivial zero-blast-radius changes directly (one-shot). Use when the user wants to implement a spec, says "implementa esta spec", "dev this", or asks for a small code fix or tweak.'
---

# NCH Dev Workflow

**Goal:** Turn an approved spec into a hardened, reviewable code artifact. The heavy thinking (product discovery, investigation, planning) already happened in `nch-spec` — this workflow executes with discipline and reviews adversarially.

**CRITICAL:** If a step says "read fully and follow step-XX", you read and follow step-XX. No exceptions.

## DIVISION OF LABOR

- `nch-prd` defines the product. `nch-spec` investigates and produces the spec. `nch-dev` implements it.
- This workflow does NOT do product discovery or deep planning. If the intent has no spec and is not trivially safe, route to `nch-spec` — do not improvise a plan.
- Spec statuses (shared contract): `draft` → `ready-for-dev` → `in-progress` → `in-review` → `done`.

## Conventions

- Bare paths (e.g. `step-01-route.md`) resolve from the skill root.
- `{skill-root}` resolves to this skill's installed directory (where `customize.toml` lives).
- `{project-root}`-prefixed paths resolve from the project working directory.
- `{skill-name}` resolves to the skill directory's basename.

## On Activation

### Step 1: Resolve the Workflow Block

Run: `python3 {project-root}/_bmad/scripts/resolve_customization.py --skill {skill-root} --key workflow`

**If the script fails**, resolve the `workflow` block yourself by reading these three files in base → team → user order and applying the same structural merge rules as the resolver:

1. `{skill-root}/customize.toml` — defaults
2. `{project-root}/_bmad/custom/{skill-name}.toml` — team overrides
3. `{project-root}/_bmad/custom/{skill-name}.user.toml` — personal overrides

Any missing file is skipped. Scalars override, tables deep-merge, arrays of tables keyed by `code` or `id` replace matching entries and append new entries, and all other arrays append.

### Step 2: Execute Prepend Steps

Execute each entry in `{workflow.activation_steps_prepend}` in order before proceeding.

### Step 3: Load Persistent Facts

Treat every entry in `{workflow.persistent_facts}` as foundational context for the whole run. Entries prefixed `file:` are paths or globs under `{project-root}` — load the referenced contents as facts. All other entries are facts verbatim.

### Step 4: Load Config

Load config from `{project-root}/_bmad/bmm/config.yaml` and resolve:

- `project_name`, `planning_artifacts`, `implementation_artifacts`, `user_name`
- `communication_language`, `document_output_language`, `user_skill_level`
- If the file or any key is missing, use defaults and never block: `communication_language`/`document_output_language` = Spanish, `planning_artifacts` = `{project-root}/_bmad-output/planning-artifacts`, `implementation_artifacts` = `{project-root}/_bmad-output/implementation-artifacts`, `user_skill_level` = intermediate
- `date` as system-generated current datetime
- `project_context` = `**/project-context.md` (load if exists)
- CLAUDE.md / memory files (load if exist)
- YOU MUST ALWAYS SPEAK in `{communication_language}`, tailored to `{user_skill_level}`

### Step 5: Greet the User

Greet `{user_name}` in `{communication_language}`, in one line.

### Step 6: Execute Append Steps

Execute each entry in `{workflow.activation_steps_append}` in order.

## WORKFLOW ARCHITECTURE

Step-file architecture for disciplined execution:

- **Micro-file Design**: Each step is self-contained and followed exactly
- **Just-In-Time Loading**: Only load the current step file
- **Sequential Enforcement**: Complete steps in order, no skipping
- **State Tracking**: Persist progress via spec frontmatter

### Critical Rules (NO EXCEPTIONS)

- **NEVER** load multiple step files simultaneously
- **ALWAYS** read entire step file before execution
- **NEVER** skip steps or optimize the sequence
- **ALWAYS** halt at checkpoints and wait for human input
- **NEVER** push or perform remote operations without explicit human request
- Content inside `<frozen-after-approval>` in the spec is read-only — only the human can change it

## FIRST STEP

Read fully and follow: `./step-01-route.md` to begin the workflow.
