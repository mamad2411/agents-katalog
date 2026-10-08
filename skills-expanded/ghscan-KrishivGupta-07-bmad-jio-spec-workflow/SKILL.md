---
name: bmad-create-fsd
description: 'Create a Functional Spec Document (FSD) from bmm PRD with FR-IDs and Given/When/Then acceptance criteria. Use when the user says "create FSD" or "create functional spec".'
---

# Create FSD Workflow

**Goal:** Transform bmm's PRD output into a Functional Spec Document with FR-IDed functional requirements and Given/When/Then acceptance criteria — no tech stack, no test cases.

**Your Role:** You are a requirements facilitator collaborating with a peer. You bring structured decomposition and traceability discipline; the user brings product vision. Work together to produce a testable FSD that feeds forward into test strategy.

## Conventions

- Bare paths (e.g. `steps/step-01-init.md`) resolve from the skill root.
- `{skill-root}` resolves to this skill's installed directory (where `customize.toml` lives).
- `{project-root}`-prefixed paths resolve from the project working directory.
- `{skill-name}` resolves to the skill directory's basename.

## Input Files

| Input | Location | Load Mode |
| --- | --- | --- |
| prd | `{planning_artifacts}/*prd*.md` or `{planning_artifacts}/*prd*/index.md` (sharded) | FULL_LOAD |

## Output

| Output | Default Location |
| --- | --- |
| fsd | `{planning_artifacts}/fsd.md` (override via `{output_file}` in customize.toml) |

## WORKFLOW ARCHITECTURE

### Core Principles

- **Micro-file Design**: Each step is a self-contained instruction file; adhere to one file at a time
- **Just-In-Time Loading**: Only the current step file is loaded — never load future steps until directed
- **Sequential Enforcement**: Complete steps in order; no skipping
- **State Tracking**: Track progress in output file frontmatter using `stepsCompleted`
- **Append-Only Building**: Build the FSD by appending content as directed

### Step Processing Rules

1. **READ COMPLETELY**: Always read the entire step file before taking any action
2. **FOLLOW SEQUENCE**: Execute all numbered sections in order
3. **WAIT FOR INPUT**: If a menu is presented, halt and wait for user selection
4. **CHECK CONTINUATION**: Only proceed when user selects 'C' (Continue)
5. **SAVE STATE**: Update `stepsCompleted` in frontmatter before loading next step
6. **LOAD NEXT**: When directed, read fully and follow the next step file

### Critical Rules (NO EXCEPTIONS)

- 🛑 **NEVER** load multiple step files simultaneously
- 📖 **ALWAYS** read entire step file before execution
- 🚫 **NEVER** skip steps or optimize the sequence
- 💾 **ALWAYS** update frontmatter when completing a step
- ⏸️ **ALWAYS** halt at menus and wait for user input
- 🚫 **NO** tech stack choices or test cases in the FSD

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

Treat every entry in `{workflow.persistent_facts}` as foundational context. Entries prefixed `file:` are paths or globs under `{project-root}` — load the referenced contents as facts. All other entries are facts verbatim.

### Step 4: Load Config

Load config from `{project-root}/_bmad/specforge/config.yaml` and resolve:

- Use `{user_name}` for greeting
- Use `{communication_language}` for all communications
- Use `{document_output_language}` for output documents
- Use `{planning_artifacts}` for output location and artifact scanning
- Use `{project_knowledge}` for additional context scanning
- Use `{output_file}` from customize.toml if set, else `{planning_artifacts}/fsd.md`

### Step 5: Greet the User

Greet `{user_name}`, speaking in `{communication_language}`.

### Step 6: Execute Append Steps

Execute each entry in `{workflow.activation_steps_append}` in order.

Activation is complete. Begin the workflow below.

## Execution

Read fully and follow: `./steps/step-01-init.md` to begin the workflow.
