---
name: diagnose
description: Read-only claude-anyteam substrate inspector for leads. Use when the lead invokes /claude-anyteam:diagnose or asks to inspect team roster, manifest cache, visibility_degraded events, #51 SendMessage flap repair evidence, wrapper MCP tool-discovery diagnostics, or substrate health.
when_to_use: User asks to diagnose claude-anyteam substrate state, wrapper MCP tool discovery, manifest cache freshness, visibility-degraded noise, or Agent Teams health.
---

# claude-anyteam diagnose

Use this skill to inspect claude-anyteam substrate state without hand-reading team files. The normal path is read-only: run the CLI and summarize the report.

```bash
claude-anyteam diagnose --team <team-name>
```

If the current session has `CLAUDE_ANYTEAM_TEAM` (or legacy `CODEX_TEAMMATE_TEAM`) set, `--team` may be omitted.

## Options

- `--team <name>`: team to inspect; defaults to the current session team env var.
- `--agent <name>`: scope roster, manifests, events, and wrapper diagnostics to one teammate.
- `--since <iso-time>`: filter event and wrapper-diagnostic rows by ISO timestamp, e.g. `2026-04-28T15:00:00Z`.
- `--json`: emit a structured report for copy/paste or follow-up analysis.
- `--instrument-spawn`: **MUTATING.** Writes `env.CLAUDE_ANYTEAM_WRAPPER_MCP_DIAGNOSTICS=1` to `~/.claude/settings.json` so the next teammate spawn captures wrapper MCP tool-discovery diagnostics. Do not use this flag unless the user explicitly wants to enable instrumentation.

## What the report covers

1. Roster snapshot: also run or quote `claude-anyteam team-roster --team <team> --json` when the lead wants raw rows. The JSON includes members, adapter PID hints, and `capability_version` per member.
2. Manifest cache state: reads `~/.claude/teams/<team>/manifests/*.json`, showing each peer's `capability_version`, on-disk timestamp, and stale/orphaned entries.
3. Recent `visibility_degraded` events: scans the most recent `events/*.jsonl` files and summarizes the last 50 by payload category/surface.
4. #51 SendMessage flap repair evidence: filters recent events for repair-path emissions such as `send_message_repair`, `repaired_via_send_message_tool`, and suppressed missing-tool claims.
5. Wrapper MCP diagnostics: if #44 instrumentation has produced `diagnostics/wrapper-mcp-tools.jsonl`, shows recent tool-discovery snapshots and missing-tool signals.
6. Substrate health checklist: green/yellow/red status for adapter MCP responsiveness, manifest cache population, capability hook registration, and stress sandbox marker state.

## Example human output

```text
claude-anyteam diagnose team=build-team scope=all mode=read-only
team_dir=/home/me/.claude/teams/build-team

[roster]
- codex-impl type=claude-anyteam backend=in-process model=gpt-5.5 pid=31415 capability_version=2 capabilities=turn_steer,structured_output

[manifest-cache]
- codex-impl capability_version=2 mtime=2026-04-28T15:19:36Z status=current

[visibility-degraded:last-50]
total=2
- peer_steer_rejected: count=2 latest=2026-04-28T15:20:11Z agent=codex-impl

[flap-repair:#51]
total=1
- 2026-04-28T15:21:03Z codex-impl prose.repaired_via_send_message_tool

[wrapper-mcp-diagnostics]
path=/home/me/.claude/teams/build-team/diagnostics/wrapper-mcp-tools.jsonl
- 2026-04-28T15:19:36Z agent=codex-impl event=server_registered_snapshot pid=31415 send_message_registered=True missing=[]

[health]
🟢 adapter_mcp_responsive: latest wrapper snapshots registered all expected tools
🟢 manifest_cache_populated: manifests present for all scoped routed members
🟢 capability_hooks_registered: advertised capabilities have runtime hooks
🟡 sandbox_markers_expected: no stress sandbox marker found for scoped cwd
```

## Response guidance

- State clearly whether you used read-only mode or the mutating instrumentation flag.
- Include exact commands run, especially `claude-anyteam diagnose ...` and `claude-anyteam team-roster --team <team> --json` when raw roster evidence matters.
- Preserve red/yellow findings verbatim enough that a follow-up teammate can route repair work without re-running the command.
