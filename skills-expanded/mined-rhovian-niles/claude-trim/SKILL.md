---
name: claude-trim
description: Use when a user wants to trim Claude Code's startup context, system prompt, tool definitions, or skill listings by interactively choosing unused settings and measuring before/after. Not for Codex CLI, conversation compaction, or historical cost analysis.
---
# Claude trim

## 1. Establish scope and dependencies

Require the operator to specify global, project, or local before choosing a write target;
never default to global. Global is `~/.claude/settings.json`, project is shared
`.claude/settings.json`, and local is `.claude/settings.local.json`. Resolve the actual
config directory and project root; inspect other layers, managed policy, launch flags,
and environment that could override the target. Inventory can proceed while scope is pending.
Explain who shares the target: global reaches sessions using that config directory
across projects; project/local files also affect other sessions in that tree on reload
or relaunch, including Niles workers.

Discover supported controls and their meaning from `claude --help` and the official
[settings reference](https://code.claude.com/docs/en/settings-reference) and
[environment reference](https://code.claude.com/docs/en/env-vars). Confirm that documented
controls are supported by the installed CLI before proposing them.

Ask which workflows must survive. Preserve their command execution, file access,
instructions, skills, and integrations. If running under an orchestrator such as Niles,
preserve its shell commands and appended launch briefing; native delegation tools are
a separate dependency to discuss. Keep mandatory repository and managed instructions.

## 2. Inventory and measure

Reconstruct the intended launch: cwd, model, settings sources, tool/permission flags,
appended instructions, and environment. Discover the CLI's context inspection commands;
prefer interactive inspection in fresh sessions using that launch for both measurements.
Store evidence privately outside the repository.
Wait for discovery to settle and compare at the same opening state.
If a local headless inspection command is supported, confirm it makes no generation call
and carry over the relevant launch flags and environment. Treat it as an auxiliary probe,
not a reproduction of an interactive launch. Do not substitute a paid prompt if unavailable.
Record category estimates and available inventories; inspect tool exposure separately
when inspection omits names. Separate deferred definitions from loaded context.
Compare before/after within the same launch and interaction mode; headless and interactive
tools/prompts can differ. Label unavailable interactive evidence as unverified, not zero
savings. These estimates are not billed tokens or a complete wire capture.

Inspect enabled plugins, MCP servers, hooks that inject text, memory/imports/rules, output
style, and discovered skills. Read the current inventory rather than pasting a tool list.
Do not install a logging proxy or redirect API traffic for the default measurement.

## 3. Offer an à la carte patch

Show a small menu derived from that inventory: item, current source/value, proposed
change, capability lost, and whether savings are measured or still a hypothesis.
Recommend candidates with reasons, then let the operator select individual items or keep
them. A general request to trim is not selection of every candidate. Find the supported
control for each selected item from the installed CLI's help and documentation:

- Whole features: unused bundled workflows, connectors, remote control, and artifacts.
- Individual tools: distinguish removing definitions from restricting or pre-approving
  calls; check the documented permission-rule and tool-selection semantics.
- Individual skills: distinguish hiding descriptions, keeping manual invocation, and
  disabling invocation. Check whether plugin skills use separate controls.
- MCP/plugins: distinguish disabling a source and its instructions from deferring schemas
  or hiding tools on one exposure surface.
- Instructions: memory, imports, rules, git guidance, and output style. Review instruction
  edits as separate explicit selections, with their behavioral costs.
- Other features: background tasks, browser guidance, scheduling, and simpler prompts.
  Check scope restrictions and effects on discovery/authentication before recommending.

Turning off telemetry or reducing output/thinking limits does not establish startup
payload savings. Moving prompt sections to a user message is not removing them.

## 4. Apply and verify

Present the exact selected diff, affected paths, and rollback before writing; apply once
the operator has approved those choices. Arrange an exclusive edit window with other
settings writers, including CLI permission persistence; an agent-only lock or atomic
rename does not coordinate them. If writers cannot be paused, hand off the patch instead.
Within that window, reread and compare with the reviewed snapshot; if changed, merge
selected edits into the latest content and obtain approval of the revised diff.
Back up those bytes privately, record before/after values and new files, and validate JSON.
For rollback, use the same guarded process to reverse only our edits whose current values
still match our result; stop on conflicts and preserve unrelated changes. Restore whole
bytes or delete a new file only if it still exactly matches our post-write snapshot.

Inspect the actual permission mode, protected-path rules, and outer filesystem policy
to determine whether self-editing needs approval or is blocked. Do not infer the mode
from an interactive or headless launch, or promise universal access or prohibition.
If blocked, report the denial and provide a patch for operator application; do not change
permission mode or bypass protection to finish.

Remeasure in a fresh process, since some switches read only at startup. Report before,
after, absolute/percentage delta by loaded category, deferred inventory separately, and
which capabilities disappeared. Check retained workflows with a bounded smoke test;
ask before any test requiring a paid generation turn. Check the intended interactive
launch before calling a headless zero delta ineffective. Investigate regressions and
offer guarded rollback. Finish with scope, applied selections,
kept dependencies, evidence paths, and precise restoration steps.
