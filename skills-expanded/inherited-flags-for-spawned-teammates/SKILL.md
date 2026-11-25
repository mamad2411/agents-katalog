---
name: inherited-flags-for-spawned-teammates
description: "Propagate CLI flags/environment variables from the leader into tmux teammates so they share permission mode, plugins, and env configuration."
metadata:
  author: ychampion
---

# SKILL: Inherited Flags For Spawned Teammates
**Domain:** multi-agent  
**Trigger:** Apply whenever a teammate or tmux-based sub-agent is spawned and it must inherit the parent’s CLI flags and environment to stay aligned.
**Source Pattern:** Distilled from reviewed multi-agent coordination and child-runtime patterns.

## Core Method
Collect the leader’s active CLI options (permission mode, model override, settings path, inline plugins, teammate-mode, chrome override) via `buildInheritedCliFlags`, rendering them into `--flag value` strings that the spawned command receives. Parallelly, spool key environment variables (provider overrides, upstream proxy, credential markers) into `buildInheritedEnvVars`, giving the new process `CLAUDECODE=1`, `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`, and any configured provider/proxy keys so the teammate shares the same backend references. Apply both sets when composing the tmux `env` + command invocation so the teammate behaves identically to its leader.

## Key Rules
- Propagate permission mode flags only when plan mode is not required; plan mode takes precedence and should block bypass propagation.
- Always include model, settings, plugin directories, teammate mode, and chrome toggles that the leader specified.
- Forward provider-specific env vars (e.g., MITM proxy, CLAUDE_CODE_USE_BEDROCK) plus canonical teammates flags so spawned shells hit the same endpoints.
- Add `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` and `CLAUDECODE=1` to signal the child process about the teammate experiment context.

## Example Application
When a coordinator spawns a tmux teammate for `claude backup`, reuse this skill by calling the helper functions, appending the resulting `--flag` arguments and `env KEY=VAL` string to the `tmux new-session` command so the teammate shares flags, models, plugins, and upstream proxy configuration.

## Anti-Patterns (What NOT to do)
- Don’t spawn teammates with a blank env—they will default to first-party endpoints and lose plugin context.
- Don’t forget to skip bypass-permissions flags when plan mode is required; inheriting bypass would violate plan-mode guarantees.
- Avoid hardcoding env keys; derive the list from the `TEAMMATE_ENV_VARS` constant so new proxies or secrets get forwarded consistently.
