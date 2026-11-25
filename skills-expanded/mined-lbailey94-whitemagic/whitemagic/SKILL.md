---
name: whitemagic
description: Use WhiteMagic durable memory and session continuity whenever resuming previous work, recalling prior decisions, or recording checkpoints — trigger words: recall, continuity, where we left off, remember this, checkpoint. Works with the `whitemagic` MCP server wired from this repository's .mcp.json.
---

# WhiteMagic — session continuity skill

WhiteMagic gives you durable, on-device project memory. The `whitemagic` MCP
server is wired by this repository's `.mcp.json` (stdio, `wm serve`); the
canonical store stays on this machine.

## Session rhythm

0. **Pre-Flight Ecosystem Brief (Zero Cold-Start).** When reviewing sessions,
   repos, VPS/site status, Sangha board, or planning next steps, run
   `/home/lucas/.local/bin/wm-preflight-brief` (or read
   `/home/lucas/SharedWorkspace/PREFLIGHT_BRIEF.md`; add `--live-vps` when
   live VPS funnel stats are needed). This compiles all 14 canonical repo
   states, 48h cross-IDE presence (Devin, AGY, Codex, Opencode), Sangha board
   digests, hosted/VPS health, and Gen3 continuity in `<2s` without spawning
   exploratory subagents.
1. **Recall first.** Before starting work, call the `wm` meta-tool with
   `route="session.continuity"` — it returns where the previous session left
   off (recent turns, checkpoints, open work).
2. **Open the session.** `wm(route="session.start", args={"title": "..."})`.
3. **Record selectively.** `wm(route="session.record", args={"content": "...",
   "turn_type": "decision"|"breakthrough"|"error"|"summary", "importance":
   0.0-1.0})` — only what a future session needs, not a transcript.
4. **Recall mid-task.** `wm(route="memory.search", args={"query": "..."})`
   searches all memory galaxies; every result discloses its `recall_mode`.
5. **Finish cleanly.** A short summary turn, then
   `wm(route="session.checkpoint")` so the next session resumes exactly here.

## Notes

- Prefer explicit `route=` over `thought=` for dependable behavior; the
  meta-tool takes exactly one of the two.
- Writes are governed; destructive routes need `confirm: true` and are never
  reachable by fuzzy routing.
- Memory is not encrypted by default — never record credentials or secrets.
- CLI equivalents exist for everything above: `wm session continuity`,
  `wm session record`, `wm session checkpoint`.
