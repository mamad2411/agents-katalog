---
name: mini-sdd-init-config
description: 'Scaffold or update the mini-sdd configuration file (mini-sdd.config.yml) that defines pre and post hooks for the context, spec, plan, and implement steps. Use when setting up hook customization, configuring hooks, adding new hooks, reviewing or editing hook settings, or when asked to "setup mini-sdd", "configure hooks", "edit the config yml", or "add a pre-hook". Do not use for implementing features, writing specs, or creating project context.'
disable-model-invocation: true
---

Scaffold or update the mini-sdd configuration file at `./{ARTIFACT_MAIN_FOLDER}/mini-sdd.config.yml`.

This file is read by `mini-sdd-context`, `mini-sdd-spec`, `mini-sdd-plan`, and `mini-sdd-implement` to inject custom pre/post instructions into their workflows.

---

## Entry point

1. Check whether `./{ARTIFACT_MAIN_FOLDER}/mini-sdd.config.yml` already exists.
   - **If it exists** → read it, show a summary of configured hooks:
     ```
     📋 Current hook configuration:
     - context.pre:   N hook(s)  → <first instruction, truncated>
     - context.post:  N hook(s)
     - spec.pre:      N hook(s)
     - spec.post:     N hook(s)
     - plan.pre:      N hook(s)
     - plan.post:     N hook(s)
     - implement.pre: N hook(s)
     - implement.post: N hook(s)
     ```
     Then ask:
     > "Do you want to **update the hooks** (I'll walk you through each event) or **reset to the default template** (all current hooks will be replaced)?"
     - **Update** → proceed to **Hook interview**, pre-filling current values
     - **Reset** → proceed to **Hook interview** with empty values (template defaults)
   - **If it does not exist** → proceed to **Hook interview** with empty values

---

## Hook interview

Use the script in [references/hook-interview.md](./references/hook-interview.md) to collect hook instructions. Ask all eight questions in a single numbered message, pre-filling current values where a config already exists. Follow the answer-interpretation rules in the same file.

---

## Write the config

1. Read the template from `assets/mini-sdd.config.template.yml` as the base structure.
2. Build the final YAML: include only hook events that have at least one instruction. Omit empty events entirely (no empty lists in the output).
3. Create `./{ARTIFACT_MAIN_FOLDER}/` if it does not exist.
4. Write (overwrite if updating) `./{ARTIFACT_MAIN_FOLDER}/mini-sdd.config.yml`.
5. Show the final content of the written file to the user.
6. Confirm:
   > "✅ Saved `./{ARTIFACT_MAIN_FOLDER}/mini-sdd.config.yml` — N hook event(s) configured."

---

## Hook instruction guidelines

- Write hooks as imperative sentences: "Check…", "Update…", "Run…"
- Each item should be one atomic action — don't combine unrelated steps in a single item.
- Pre hooks should be non-destructive checks or preparatory steps.
- Post hooks should be follow-up actions after the skill's main work is complete.
- If the project stack uses specific commands or paths, include them explicitly.

---

## Output rules

{SKILL_ASSETS_NOTICE}
- Never silently overwrite an existing config — always show the current state first.
- Always show the final written file content after saving.

## Error handling

- **File not writable / path missing**: create the `./{ARTIFACT_MAIN_FOLDER}/` directory if it does not exist before writing.
- **Invalid YAML produced**: validate the structure before writing. If the YAML would be invalid (e.g., missing colon, bad indentation), fix it automatically and note the correction to the user.
- **User skips all hooks**: write a minimal valid config with only a top-level `hooks: {}` block and note that no hooks are active.
