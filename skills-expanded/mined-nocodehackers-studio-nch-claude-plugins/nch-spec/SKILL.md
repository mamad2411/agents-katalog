---
name: nch-spec
description: 'Product discovery + deep codebase investigation for nocodehackers products. Interviews the user like an expert product person, investigates the code iteratively until context is sufficient, and outputs an implementation-ready spec that can be resumed anytime. Use when the user wants to spec out a feature, diagnose a bug before fixing it, or says "crear spec", "specear", "investigar este bug", or "preparar esta feature".'
---

# NCH Spec Workflow

**Goal:** Turn a vague product intent or bug report into a hardened, implementation-ready spec — through expert product questioning and deep code investigation. This skill does NOT implement code. Its deliverable is the spec.

**CRITICAL:** If a step says "read fully and follow step-XX", you read and follow step-XX. No exceptions.

## READY FOR DEVELOPMENT STANDARD

A specification is "Ready for Development" when:

- **Actionable**: Every task has a file path and specific action.
- **Logical**: Tasks ordered by dependency.
- **Testable**: All ACs use Given/When/Then.
- **Complete**: No placeholders or TBDs.
- **Grounded**: Every file referenced in the Code Map was actually read or verified during investigation — never guessed.

## SCOPE STANDARD

A specification should target a **single user-facing goal** within **900–1600 tokens**:

- **Single goal**: One cohesive feature or one bug, even if it spans multiple layers/files. Multi-goal means >=2 top-level independently shippable deliverables. Never count surface verbs, "and" conjunctions, or noun phrases. Never split cross-layer implementation details inside one user goal.
- **900–1600 tokens**: Optimal range for LLM consumption. Below 900 risks ambiguity; above 1600 risks context-rot in implementation agents.
- **Neither limit is a gate.** Both are proposals with user override.

## CONTEXT SUFFICIENCY STANDARD

Investigation is sufficient when you can answer ALL of these without guessing:

1. **Where** — which files/modules change, and which surrounding code constrains them.
2. **How it works today** — the current behavior/data flow in the affected area, verified by reading code (not inferred from names).
3. **Why** (bugs only) — the root cause, traced to specific code, or the top candidate hypotheses with evidence for each.
4. **What could break** — the blast radius: callers, consumers, shared state, integrations touched by the change.
5. **What the product needs** — problem, user value, success criteria, and edge-case behavior, confirmed by the human.

If any answer is a guess, investigation is NOT sufficient. Loop again.

## Conventions

- Bare paths (e.g. `step-01-intent.md`) resolve from the skill root.
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
- Generate all documents in `{document_output_language}`

### Step 5: Greet the User

Greet `{user_name}` in `{communication_language}`, in one line, as a senior product-minded engineer ready to dig in.

### Step 6: Execute Append Steps

Execute each entry in `{workflow.activation_steps_append}` in order.

## WORKFLOW ARCHITECTURE

Step-file architecture for disciplined execution:

- **Micro-file Design**: Each step is self-contained and followed exactly
- **Just-In-Time Loading**: Only load the current step file
- **Sequential Enforcement**: Complete steps in order, no skipping
- **State Tracking**: Persist progress via spec frontmatter
- **Append-Only Building**: Build artifacts incrementally

### Critical Rules (NO EXCEPTIONS)

- **NEVER** load multiple step files simultaneously
- **ALWAYS** read entire step file before execution
- **NEVER** skip steps or optimize the sequence
- **ALWAYS** halt at checkpoints and wait for human input
- **NEVER** implement code in this workflow — the spec is the deliverable

## FIRST STEP

Read fully and follow: `./step-01-intent.md` to begin the workflow.
