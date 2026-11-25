---
name: codex-trim
description: Use when a user wants to trim Codex CLI's startup context, injected instructions, tools, apps, or skill listings by interactively choosing unused configuration and measuring before/after. Not for Claude Code, conversation compaction, or historical cost analysis.
---
# Codex trim

## 1. Establish scope and dependencies

Require the operator to specify global, project, or local before choosing a write target.
Global is `$CODEX_HOME/config.toml` (normally `~/.codex/config.toml`); project is trusted
`.codex/config.toml`. Inspect effective layers, trust, managed requirements, launch
overrides, and profile before proposing changes. Inventory can proceed while scope is pending.
Explain who shares the target: global reaches sessions using that config directory
across projects; project settings also affect other sessions in that tree on reload
or relaunch, including Niles workers.

For local scope, discover whether the CLI supports private project configuration.
Otherwise explain supported invocation overrides and agree how the operator will launch
them; do not silently write project/global config or invent an ignored config filename.
If persistence is wanted, agree a supported mechanism and its actual scope first.

Discover supported controls, profiles, and feature inspection commands from `codex --help`
and the official [configuration reference](https://developers.openai.com/codex/config-reference/).
Confirm that documented controls are supported by the installed CLI; reject unsupported
settings rather than assuming that a parsed TOML key is effective.

Ask which workflows must survive; preserve their execution/file tools, required
instructions, skills, and integrations. Under Niles or another orchestrator, preserve
shell access and injected `developer_instructions` carrying the worker briefing.
Native multi-agent delegation is a separate dependency to discuss. Keep mandatory
repository and managed instructions.

## 2. Inventory and measure

Use fresh processes with the same cwd, model, profile, launch overrides, trust, and
opening prompt. Discover supported local prompt inspection commands from the CLI help
and confirm they make no generation call. Carry the intended profile and overrides into
the probe; do not compare a bare probe against a customized launch. Store evidence privately.

Compare serialized bytes, input items, instruction blocks, and tool exposure where the
inspection output supports them. Bytes are not tokens or a guaranteed complete HTTP
payload. Inspection setup can differ from a live launch; disclose that limit. If local
inspection is unavailable, report the limit rather than silently making a paid call.

Inspect loaded AGENTS files and overrides, skill listings, enabled features, MCP/app
tools, and plugin contributions. Discover current names instead of copying a fixed
tool deny list. For actual tokens, offer a separately authorized pair of identical
fresh turns using supported usage reporting. Inspect the counter definitions and show
input/cache/write/output categories without double-counting overlapping totals.
This incurs generation cost and is optional.

## 3. Offer an à la carte patch

For each candidate show current source/value, proposed change, lost capability, and
measured or hypothesized effect. Suggest a small first batch with reasons; let the
operator select individual items or keep them. A request to trim does not approve
every candidate. Find supported controls for these categories from the installed CLI's
help and documentation:

- Instruction blocks: permissions, apps, collaboration, and environment guidance.
  Distinguish omitting guidance from changing enforcement; both affect behavior.
- Skills: bundled or selected skills, catalogue size, and automatic instructions.
  Preserve manual and automatic discovery needed by retained workflows.
- Memory: distinguish stopping injection from stopping generation.
- MCP/apps: server/app enablement, individual tools, and exposure surfaces.
  Hiding from one surface does not establish complete removal.
- Tools: unused search, planning, user interaction, and delegation capabilities.
  Verify which tools a feature switch removes instead of assuming a general deny list.
- Instructions on disk: review selected AGENTS content separately. Discover precedence,
  accumulation, and size-limit scope before editing. Replacing base model instructions
  risks behavior and is not a routine trimming preset.

Output/thinking budgets and conversation compaction do not measure startup payload savings.

## 4. Apply and verify

Show the exact selected diff or invocation, target paths, and rollback; apply after
the operator approves those choices. Arrange an exclusive edit window with other
settings writers, including CLI trust persistence; an agent-only lock or atomic rename
does not coordinate them. If writers cannot be paused, hand off the patch instead.
Within that window, reread and compare with the reviewed snapshot; if changed, merge
selected edits into the latest content and obtain approval of the revised diff.
Back up those bytes privately, record before/after values and new files, and check TOML
syntax plus CLI acceptance. For rollback, use the same guarded process to reverse only
our edits whose current values still match our result; stop on conflicts and preserve
unrelated changes. Restore whole bytes or delete a new file only if it still exactly
matches our post-write snapshot. Invocation-only changes need no file write.

Inspect the actual sandbox, approval policy, protected paths, and outer filesystem
restrictions to determine whether self-editing is permitted. Do not infer write access
from the working directory or assume an approval policy grants filesystem access.
If blocked, report the actual denial and provide the selected patch for operator
application. Do not escalate permissions or change sandbox mode to complete trimming.

Launch fresh for the after measurement. Report byte and inventory deltas as such,
and tokens only if actually measured. Check that selected removals took effect and
retained workflows still work using a bounded smoke test without unapproved paid turns.
Investigate overrides or ignored keys when nothing changes; offer rollback on
regression. Finish with scope, applied/kept choices, launch command if local,
measurement limitations, evidence paths, and precise restoration steps.
