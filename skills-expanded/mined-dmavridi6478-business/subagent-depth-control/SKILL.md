---
name: subagent-depth-control
description: Explains and configures Claude Code's subagent nesting-depth limit — how many layers deep a subagent can spawn its own subagents, why each layer multiplies context windows and token cost rather than adding to it, how the default has changed across versions, and the CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH setting to control it directly. Use whenever the user asks about subagent/multi-agent nesting, token costs from nested agents, "why is this costing so much," or is following a guide about subagent depth and should verify it against their actual Claude Code version first. Also trigger when advising on any Claude Code setting whose default has changed across versions — the general lesson here is check the version before trusting a guide's claimed default.
---

# Subagent Depth Control

Source: "Your subagents stopped nesting 5 levels deep. The guides didn't notice." (AI Unlocked, Tool Drop 19, @iunlockedai). Verified against the official docs (code.claude.com/docs/en/agent-sdk/subagents) rather than taken at face value from the carousel alone.

## The core mechanic: nesting multiplies, it doesn't add

A subagent that can spawn subagents doesn't add agents — it multiplies them. Each nesting layer runs its own context window and burns its own tokens. Copying a nesting-depth config from an old guide without understanding this can produce a bill, not a preference.

## What actually happens at the depth limit

At the configured limit, Claude Code doesn't error or break — it simply withholds the `Agent` tool from the subagent at that depth, so that subagent does the remaining work itself and returns one summary instead of spawning further. Nothing breaks; the fan-out just stops.

## The default has changed twice since June — verify before trusting a guide

| Claude Code version | Default nesting depth | Configurable? |
|---|---|---|
| v2.1.172 – v2.1.216 | 5 layers, nesting on by default | No — the limit could not be changed at all |
| v2.1.217 – v2.1.218 | 1 (effectively off unless raised) | Yes — `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` introduced |
| v2.1.219 and later | 3 | Yes |

Several widely-shared guides still describe depth 5 as a hard cap with no way to change it — that was true in June 2026 and stopped being true at v2.1.217. **Run `claude --version` before trusting any guide's claimed default**, and decide the depth deliberately rather than inheriting whatever a cached guide or a June-era config implies.

## The actual setting

In `settings.json`:

```json
{
  "env": {
    "CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH": "2"
  }
}
```

- Sets how many subagent layers below the main conversation are allowed to spawn further subagents.
- Set to `"1"` to turn nesting off entirely — a subagent still runs, but cannot spawn its own subagents.
- **This variable has only existed since v2.1.217** — on an older build it silently does nothing, which is itself a reason to check the version first rather than assume the setting takes effect.

## Output conventions when using this skill

- When asked about subagent nesting cost/behavior, check the current Claude Code version before stating a default — don't assume the version this skill's table describes as current is still current by the time it's read.
- If advising a user whose guide/config predates v2.1.217, flag explicitly that the setting they're relying on may not exist in their version, or that the default they're assuming is outdated.
- Frame nesting-depth as a cost/scope decision, not just a technical toggle — more depth means more parallel context windows and more token spend for the same task, similar in spirit to `web-task-scoping`'s discipline of not granting more autonomy/scope than a task actually needs.

## Related skills in this repo

- **web-task-scoping**: Same underlying discipline — don't grant more autonomy/depth/scope than the task actually needs, applied to browser tasks instead of agent-spawn depth.
- **night-shift-workflow**: If a scheduled/unattended workflow spawns nested subagents, the depth setting here is one more lever in that skill's Claude-may/human-approval boundary — deeper nesting means more unattended work happening per run.
- **claude-code-tooling**: The broader directory of external Claude Code tools/config knowledge this skill's specific setting belongs alongside.

## Notes

Source: "Your subagents stopped nesting 5 levels deep. The guides didn't notice." carousel (AI Unlocked, Tool Drop 19, @iunlockedai), cross-checked against the official docs (code.claude.com/docs/en/agent-sdk/subagents) as shown in the carousel's own cited screenshot — not taken at face value from the carousel text alone, consistent with this skill's own stated discipline of verifying version-dependent claims.
