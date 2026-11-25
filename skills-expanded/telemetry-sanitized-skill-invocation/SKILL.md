---
name: telemetry-sanitized-skill-invocation
description: "Record SkillTool usage with sanitized telemetry fields so built-in, bundled, and custom skills are distinguished while avoiding PII leakage."
metadata:
  author: ychampion
---

# SKILL: Telemetry Sanitized Skill Invocation
**Domain:** tool-orchestration  
**Trigger:** Use when SkillTool emits `tengu_skill_tool_invocation` so built-in commands, remote MCP skills, and forked executions are logged without exposing command strings in open analytics tables.
**Source Pattern:** Distilled from reviewed tool-loop and result-shaping patterns.

## Core Method
Before executing any skill, compute whether the command is built-in, bundled, official marketplace, or custom and pass the sanitized value as `command_name` while storing the actual skill name under `_PROTO_skill_name` to satisfy both privacy and auditability. Add contextual metadata such as `execution_context` (`inline`, `forked`, `remote`), `query_depth`, `parent_agent_id`, and plugin fields when applicable, and wrap remote canonical invocations or discovered skills with additional flags so downstream dashboards know the skill source without revealing user-generated text. Emit separate telemetry for inline/forked/remote flows so metrics can split by execution path while normalizing the skill name for aggregated reporting.

## Key Rules
- Derive `sanitizedCommandName` as `commandName` for built-in/bundled/official skills and fall back to `'custom'` for user-authored commands; log the actual name only in `_PROTO_skill_name` to keep BigQuery columns safe.
- Always include `execution_context` (`'inline'`, `'forked'`, `'remote'`) plus `invocation_trigger` (nested vs proactive) and `query_depth` so telemetry consumers understand the runtime scenario.
- When a plugin skill is involved, add both `_PROTO_plugin_name` and the sanitized `plugin_name`/`plugin_repository` fields along with marketplace metadata to enable plugin-level analytics without leaking repository URLs.
- For remote MCP skills, emit `is_remote`, `was_discovered`, and cached load info (latency, cache hit) so telemetry can diagnose discovery performance without exposing the raw prompt body.

## Example Application
Use this skill to log any slash command invocation, ensuring that a cloned forked review or `remote_skill` call still records an `execution_context` flag plus proper naming sanitization for consumption by privacy-sensitive dashboards.

## Anti-Patterns (What NOT to do)
- Do not log user-entered command text directly into public telemetry columns; that breaks PII rules and makes analytics unusable.
- Do not merge inline/forked/remote flows in a single metric stream without flags, because it becomes impossible to trace delays or diagnostics per execution context.
