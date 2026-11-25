---
name: context-management
description: Design and optimize context windows for agentic workflows. Use when the user asks to "manage context", "optimize context", "compact context", "context budget", "CLAUDE.md", "memory hierarchy", "context degradation", "agent is forgetting", "agent hallucinating after many turns", "long conversation", "hit token limit", "prune context", "memory tiers", or when a multi-turn workflow shows quality decay. Covers CLAUDE.md authoring, tiered memory, scratchpads, /compact strategies, read-depth rules, and subagent delegation for context relief.
---

# Context Management

Agentic workflows fail from context pressure before they fail from capability. Treat context as the scarcest resource.

## Four tiers (from GSD convention)

| Tier       | Usage   | Behavior                                                                |
|------------|---------|-------------------------------------------------------------------------|
| PEAK       | 0–30%   | Full ops. Read bodies, spawn agents, inline results.                    |
| GOOD       | 30–50%  | Prefer frontmatter reads. Delegate aggressively.                        |
| DEGRADING  | 50–70%  | Economize. Frontmatter-only reads. Warn user about budget.              |
| POOR       | 70%+    | Emergency. Checkpoint to disk. No new reads unless critical. /compact.  |

## Memory hierarchy

1. **System** — model + tool definitions (fixed, ~10-30k).
2. **Project memory — CLAUDE.md** (loaded every session). Keep under 500 lines. Conventions, glossary, project-specific rules.
3. **Skills** — loaded when triggered. Progressive disclosure via `@reference.md` imports.
4. **Session scratchpads** — `.planning/STATE.md`, `.arch/state.json`. Survive across turns.
5. **Subagent isolates** — heavy work offloaded; only 5-line exit summaries return.

## CLAUDE.md authoring rules

- Top: one-paragraph project purpose + stack.
- Glossary: project-specific terms, nicknames, acronyms.
- Conventions: file layout, naming, commit style.
- Red-lines: things Claude must never do.
- End: pointers to deeper docs via `@` (don't inline them).
- Max ~500 lines. If longer, split and `@`-import.

## Read-depth rules for orchestrators

- **< 500k context window (200k default)**: read only frontmatter, status fields, or summaries of specialist output. Never read full SUMMARY.md, VERIFICATION.md, or RESEARCH.md bodies.
- **≥ 500k (1M models)**: MAY read full specialist bodies when needed for decisions.
- **Always**: never read agent definition files — `subagent_type` auto-loads them.
- **Always**: tell specialists to Read files from disk rather than inlining file contents in the spawn prompt.

## Compaction strategies

1. **Checkpoint**: write `STATE.md` with decisions/progress, then `/compact`. Resume by Reading STATE.md.
2. **Delegate**: spawn a specialist to absorb heavy input (e.g., "read these 10 files and produce a 500-word synthesis"), return only the synthesis.
3. **Scratchpad + prune**: keep working notes on disk; reference them rather than carrying in context.

## Warning signs of degradation (catch before tier POOR)

- Agent uses vague phrases ("appropriate handling", "standard patterns") instead of specifics.
- Agent silently skips protocol steps it would normally follow.
- Tool-call count per turn drops below historical baseline.
- User has to re-state facts already in context.

## Anti-patterns

- Reading full agent definition files in the orchestrator.
- Inlining >500 lines from any one file.
- Running >5 tool calls deep without checkpointing.
- Writing CLAUDE.md with "helpful tips" — keep it to rules and pointers.

## References

- @../../agents-architect/references/context-budget.md — full read-depth tables
- @../../agents-architect/references/memory-tiers.md — hierarchy details
- See `../../agents-architect/templates/CLAUDE.md.template` — plugin-ready CLAUDE.md scaffold

## Output

When asked to design context management for a new plugin:

1. Produce a `CLAUDE.md.template` sized for the domain (< 500 lines).
2. Produce a `context-budget.md` ref doc listing tier actions.
3. Identify which workflows need checkpoint files and specify their schemas.
4. Recommend which work is done inline vs. delegated to specialists.
