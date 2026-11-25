---
name: zihin-criar-agente
description: Use this guide to create, configure, validate and publish a hosted Zihin agent, including its persona, tools, channels and optional memory settings.
---

# Create and publish an agent

1. Establish the intended role, objective and behavior with the user. Discover available
   models through `zihin://models` and inspect `zihin://schemas/llm_config`.
2. Call `create_agent` with the required fields. Use a valid provider-qualified model ID
   or `auto`. Keep the returned `agent_id` and address plan or model-tier warnings.
3. Create a `persona_config` schema. Read `zihin://schemas/persona_config`; the persona
   belongs under `editor_schema.persona`, not a legacy root-level instructions field.
4. Add optional `skill_config` schemas with clear instructions and unique skill names.
   For external capabilities, read `zihin://skills/tools-de-agente`.
5. Run `validate_agent_schemas`, inspect `list_agent_tools` and review `get_agent_full`.
   Resolve invalid schemas and tools cited outside the available surface. If validation
   reports a surface error, do not interpret an empty result as a successful check.
6. Call `publish_agent` only after validation succeeds. Publication can reject a model
   that exceeds the plan tier even if an earlier save returned only a warning.

Enable native chat with `chat_enabled` when requested. Read the trigger guide before
connecting external channels. Persistent memory requires `memory_enabled`; a skill
alone does not enable it. Keep consumer identities distinct and do not reuse a session
across people. Use dedicated engagement and session controls for operational state.

For updates, read a schema's current version and provide `base_version` when saving.
On `CONFLICT`, reload and reconcile the changes. Schema data replaces the whole document.
Validate and publish again. Use snapshot/version tools for supported rollback operations.
