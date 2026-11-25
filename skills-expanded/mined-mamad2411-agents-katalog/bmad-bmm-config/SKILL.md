---
name: bmad-bmm-config
description: >-
  Use this internal skill to resolve BMM module configuration values and layer
  them on top of core config values already loaded by bmad-core-config. Invoked
  automatically by bmad-core-config when it detects the calling skill belongs to the
  BMM module. Reads _bmad/bmm/config.yaml when present, falling back to
  sensible defaults (project name from workspace root, intermediate skill level,
  standard output paths) when the file is absent — so it works without a full
  BMAD installation. Resolved values include project_name, user_skill_level,
  planning_artifacts, implementation_artifacts, and project_knowledge. Produces
  no user-facing output. Do not invoke directly; let bmad-core-config call it as
  part of normal initialization. The distinction from bmad-core-config is that this
  skill handles only BMM-specific overrides, not core settings like user_name
  or communication language.
metadata:
  internal: "true"
  bmad:
    module: bmm
    type: workflow
---

# Load BMM Config

Load BMM module configuration from the installed config file, falling back to sensible defaults.

## Outcome

All BMM module configuration values resolved and available for the calling skill or workflow, layered on top of core config values already loaded by `bmad-core-config`. Works without a full BMAD installation by applying sensible defaults.

## Silent Execution

This is an internal context-provider skill. Do not produce any user-facing output — no announcements, no status messages, no summaries. Only populate resolved values into context for the calling skill to consume.

## Inputs

- Core config values already resolved by `bmad-core-config` (passed as context)
- BMM config at `{project-root}/_bmad/bmm/config.yaml` (optional)

## Procedure

1. Attempt to read `{project-root}/_bmad/bmm/config.yaml`.

2. If the file exists, resolve these BMM-specific values from it:
   - `project_name`
   - `user_skill_level`
   - `planning_artifacts`
   - `implementation_artifacts`
   - `project_knowledge`

3. If the file does **not** exist, apply these defaults:
   - `project_name` → name of the workspace root directory
   - `user_skill_level` → `"intermediate"`
   - `planning_artifacts` → `{output_folder}/planning-artifacts`
   - `implementation_artifacts` → `{output_folder}/implementation-artifacts`
   - `project_knowledge` → `{project-root}/docs`

4. Record which source was used (`project` or `defaults`) so the calling skill can decide whether to inform the user.

## Halt Conditions

- HALT if `{project-root}/_bmad/bmm/config.yaml` exists but is unreadable or contains malformed YAML that cannot be parsed
- HALT if core config values passed from `bmad-core-config` are absent, making it impossible to layer BMM values on top
- HALT if no resolved value can be produced for `planning_artifacts` — this path is required by nearly every BMM skill

## Required Output

- All BMM configuration values resolved and merged with core values.
- Source indicator (`project` or `defaults`) recorded.

## Completion Checks

- Every BMM configuration value has a resolved value.
- BMM values are layered on top of core values (no core values overwritten).
- Source indicator is set.

## When to Use

Use this skill when:
- A BMM skill or workflow needs resolved module-specific settings (`project_name`, `planning_artifacts`, `implementation_artifacts`, `project_knowledge`, `user_skill_level`)
- Invoked by `bmad-core-config` when the calling module is detected as `bmm`
- The calling skill needs BMM config values layered on top of already-resolved core config values

