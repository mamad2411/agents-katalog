---
name: bmad-core-config
description: >-
  Use this internal skill to load all BMAD project configuration values —
  both core settings and module-specific overrides — making them available
  to the calling skill. Invoked automatically at the start of every BMAD skill
  that needs configuration; never invoked directly by the user. The skill
  derives the calling module from the skill name pattern (bmad-[module]-...),
  reads the core config from _bmad/core/config.yaml (falling back to defaults
  for user_name, communication_language, document_output_language, and
  output_folder if absent), then delegates to the appropriate module config
  skill (e.g. bmad-bmm-config) to layer in module-specific values. Produces no
  user-facing output — all values are silently passed as context. The
  distinction from module config skills is that this skill handles core-level
  values and acts as the discovery and routing layer; module config skills
  handle domain-specific overrides. Do not invoke this skill from user-facing
  requests; it is a configuration loader for internal use only.
metadata:
  internal: "true"
  bmad:
    module: core
    type: task
---

# Load BMAD Config

Load BMAD project configuration by detecting the calling module and delegating to the appropriate module-specific config skill.

## Outcome

All project configuration values — core and module-specific — resolved and available for the calling skill or workflow. The correct module config skill is invoked automatically based on context.

## Silent Execution

This is an internal context-provider skill. Do not produce any user-facing output — no announcements, no status messages, no summaries. Only populate resolved values into context for the calling skill to consume.

## Procedure

1. Detect the calling module.
   - Derive the module from the calling skill's name. Skills follow the naming convention `bmad-<module>-<workflow>` (e.g. `bmad-bmm-create-prd` → module `bmm`).
   - If the calling skill has no module segment (e.g. `bmad-core-party-mode`), treat the module as `core`.

2. Load core configuration.
   - Attempt to read `{project-root}/_bmad/core/config.yaml`.
   - If the file exists, resolve these values from it:
     - `user_name`
     - `communication_language`
     - `document_output_language`
     - `output_folder`
   - If the file does **not** exist, apply these defaults:
     - `user_name` → `"BMad"`
     - `communication_language` → `"English"`
     - `document_output_language` → `"English"`
     - `output_folder` → `{project-root}/_bmad-output`
   - Set `date` to system-generated current datetime.

3. Delegate to module-specific config skill (if module is not `core`).
   - Check if `bmad-<module>-config` skill is installed (e.g. `bmad-bmm-config`).
   - If installed: `Invoke skill: bmad-<module>-config` — pass resolved core values as context.
   - If not installed: proceed with core values only.

4. Record which sources were used (`project` or `defaults` for core, and whether module config was loaded) so the calling skill can decide whether to inform the user.

## Halt Conditions

- HALT if the calling skill's module cannot be determined and cannot be treated as `core`
- HALT if `{project-root}/_bmad/core/config.yaml` exists but is unreadable or contains malformed YAML that cannot be parsed
- HALT if no module-specific config skill (`bmad-<module>-config`) is found and core config alone is insufficient for the calling skill to proceed

## Required Output

- All configuration values resolved and available for use by subsequent steps.
- Source indicators recorded (core source + module source).

## Completion Checks

- Every core configuration value has a resolved value.
- If calling module is not `core`, module-specific config skill was invoked (or warning logged if unavailable).
- Source indicators are set.

## When to Use

Use this skill when:
- Any skill or workflow needs resolved project settings (`user_name`, `communication_language`, `document_output_language`, `output_folder`)
- A skill needs to load core config and delegate to the appropriate module-specific config skill
- A BMM skill (or any `bmad-<module>-*` skill) initializes and needs to resolve all configuration values before proceeding

