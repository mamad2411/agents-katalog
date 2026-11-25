---
name: context-lifecycle
description: "Automated context boundary orchestration. Runs at phase ends, pre/post-compact, and after git push. Chunks work across sessions via session-bridge, context-pack, and neural-memory without losing continuity."
user-invocable: true
metadata:
  author: topia
  version: "1.0.0"
  layer: L3
  model: haiku
  group: state
  tools: "Read, Glob, Grep"
  emit: context.checkpoint.written, context.compacted
  listen: context.pressure.high, checkpoint.request, phase.complete
---

# context-lifecycle

## Purpose

Orchestrate **when** to save state, **when** to recommend `/compact`, and **how** to resume after compaction or push — so the agent does not rely on manual compaction alone. Hooks write `.topia/checkpoint.md` deterministically; this skill coordinates the agent-side follow-up.

## Triggers

- **Hook message** after `pre-compact` or `git push` (checkpoint already on disk)
- **Post-compact** injection (resume from checkpoint)
- `build` / `team` at phase boundaries when context-watch is YELLOW+
- `checkpoint.request` or `phase.complete` signals
- User: `/topia context-lifecycle` or "resume after compact"

## Calls (outbound)

- `session-bridge` (L3): Save Mode, Checkpoint Mode, Load Mode
- `context-engine` (L3): health classification before compact recommendation
- `context-pack` (L3): handoff briefings before subagent spawn
- `neural-memory` (L3): Flush Mode before compaction when MCP available
- `recall` (L3): minimal unified recall at session start after compact

## Called By (inbound)

- `context-engine` (L3): delegates Boundary Save when ORANGE/RED
- `build` (L1): phase boundaries, ORANGE/RED context
- `team` (L1): before parallel dispatch, after merge, push boundaries
- `session-bridge` (L3): after hook-written checkpoint
- `rescue` (L1): between refactoring sessions

---

## Mode: Boundary Save (phase end / ORANGE)

1. Invoke `topia:context-engine` — report health level.
2. If ORANGE or RED → invoke `topia:session-bridge` (Save Mode) with current phase, files touched, decisions, remaining tasks.
3. If RED → recommend `/compact` immediately after Save.
4. If spawning a subagent next → invoke `topia:context-pack` for a &lt;1500 token handoff.
5. If neural-memory MCP configured → invoke `topia:neural-memory` (Flush Mode) before compact.
6. Emit advisory: next safe boundary for compact or new session.

## Mode: Hook Resume (pre-compact / git push)

Hooks have already written `.topia/checkpoint.md`. Agent MUST:

1. Read `.topia/checkpoint.md` and `.topia/progress.md` (do not re-explore the repo first).
2. Confirm git state matches checkpoint (warn if branch/commit diverged).
3. If post-push: recommend `/compact` or new session; do not start unrelated work in the same bloated context.
4. Continue from **Resume Command** in checkpoint.

## Mode: Post-Compact Resume

After `/compact`, PostCompact hook re-injects checkpoint preview. Agent MUST:

1. Read full `.topia/checkpoint.md`.
2. Optionally invoke `topia:recall` (minimal) for neural-memory / agora if configured.
3. Mark checkpoint consumed after successful resume:
   - Rename to `.topia/checkpoint-[date].resolved.md` (keep last 3 resolved).
4. Emit `context.compacted` (observability) when resume is confirmed.

## Chunking policy

| Stage | Context strategy |
|-------|------------------|
| Research / plan | Separate session or Task; `context-pack` briefing only |
| Implementation | One module per workstream; `team` fork for parallel |
| Review | Fresh Task; `contexts/review.md`; never same window as impl |
| Ship (push) | Hook checkpoint → compact or new session |

## Output Format

### Boundary Save
```
## Context Lifecycle — Boundary Save
- Health: [GREEN|YELLOW|ORANGE|RED]
- Saved: [.topia files updated]
- Compact: [recommended now | at next boundary | not yet]
```

### Hook / Post-Compact Resume
```
## Context Lifecycle — Resume
- Source: [.topia/checkpoint.md]
- Next step: [single explicit action]
- Compact: [done | pending]
```

## Constraints

1. MUST read `.topia/checkpoint.md` before re-exploring the repo after compact or push
2. MUST NOT skip `session-bridge` Save when context-engine reports ORANGE/RED
3. MUST recommend `/compact` at ORANGE only at a safe phase boundary (not mid-edit)
4. Hooks own deterministic checkpoint files — this skill coordinates agent behavior, not hook scripts

## Sharp Edges

| Failure Mode | Severity | Mitigation |
|---|---|---|
| Compacting without checkpoint | CRITICAL | Hooks write checkpoint on pre-compact/push; verify file exists |
| Resuming from stale checkpoint after large git drift | HIGH | Compare branch/commit in checkpoint vs current git |
| Same context for impl + review | HIGH | Use `team` fork + `context-pack`; never merge review into impl window |
| Ignoring hook stdout after push | MEDIUM | Treat push checkpoint as hard boundary — compact or new session |

## Cost Profile

~100-300 tokens per boundary check (haiku). Flush/recall add MCP latency when configured. Hooks are zero LLM cost.

## Done When

- Checkpoint on disk matches current work (or user acknowledged drift)
- User knows whether to `/compact` or start fresh
- Next action is explicit (file + step), not "what were we doing?"
