---
name: claude-code-reference
description: Reference tables for Claude Code configuration -- the memory hierarchy and what each layer costs, model selection and pricing, effort levels, and context engineering rules. Use when auditing CLAUDE.md, deciding where a piece of knowledge belongs, choosing a model or effort level, or debugging why an instruction was not followed.
---

# Claude Code Reference

Verified against Claude Code v2.1.234, August 2026. These are lookup tables, not
behavioural rules -- the always-on rules live in `~/.claude/CLAUDE.md`.

## Memory Hierarchy

Claude Code loads memory in layers. Understanding the cost of each layer prevents
context waste.

| Layer | Location | Loaded | Cost |
|-------|----------|--------|------|
| Managed policy | `/Library/Application Support/ClaudeCode/CLAUDE.md` | Every session | Always on, cannot be excluded by user settings |
| User | `~/.claude/CLAUDE.md` | Every session | Always in context |
| User rules | `~/.claude/rules/*.md` | Every session unless `paths:` scoped | Always in context |
| Project | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Every project session | Always in context |
| Project rules | `.claude/rules/*.md` | Every project session | Always in context |
| Path-scoped rules | `.claude/rules/*.md` with `paths:` frontmatter | When Claude reads a matching file | On demand |
| Project local | `./CLAUDE.local.md` | Every project session | Always in context (gitignored) |
| Child directory | `./packages/foo/CLAUDE.md` | On demand | Only when Claude reads files in that dir |
| Auto memory | `~/.claude/projects/<id>/memory/MEMORY.md` | First 200 lines **or** 25KB, whichever comes first | Partial, per session |
| Skills | `.claude/skills/<name>/SKILL.md` | Description at start; full body on invoke | ~1 line per skill at start |

**Principle:** CLAUDE.md is always-on and expensive. Skills are on-demand and cheap.
Put always-needed behavioural rules in CLAUDE.md; put reference material in skills.

**Size target:** under 200 lines per CLAUDE.md file. Longer files consume more
context and measurably reduce adherence. `/doctor` proposes trims for checked-in
CLAUDE.md files. `/context` shows which memory files actually loaded.

### Rules gotchas

Path scoping works -- the original global-loading bug
(<https://github.com/anthropics/claude-code/issues/16299>) is no longer
reproducible. No changelog entry pins the fix to a version; a reporter confirmed it
working in v2.1.63. Verify in your own setup with `/context`. Two narrower traps
remain open:

- Every `.md` under `.claude/rules/` loads at launch unless it carries its own
  `paths:` frontmatter, and discovery is **recursive**. Reference files parked in
  a `refs/` subdirectory load globally unless individually scoped.
- `@`-imports inside a path-scoped rule load **unconditionally**, even when the
  rule never matches. Avoid imports in rules; duplicate the few lines instead.

### What survives compaction

Project-root CLAUDE.md is re-read from disk and re-injected. Nested CLAUDE.md
files and path-scoped rules are **not** -- they reload only when Claude next
touches a matching file. Instructions given only in conversation are lost.

## Model Selection

| Model | Alias | Context | $/Mtok (in/out) | Use for |
|-------|-------|---------|-----------------|---------|
| Fable 5 | `fable` | 1M | $10 / $50 | Long autonomous sessions, ambiguous root-cause work, tasks larger than one sitting |
| Opus 5 | `opus` | 1M | $5 / $25 | What `opus` resolves to. Team lead, complex architecture, security-critical code |
| Sonnet 5 | `sonnet` | 1M | $2 / $10 | Standard teammates, daily coding |
| Haiku 4.5 | `haiku` | 200K | $1 / $5 | Read-only subagents, file search, codebase exploration |

| Role | Model | When |
|------|-------|------|
| Team lead | Opus 5 | Coordination, synthesis, complex decomposition |
| Teammate (default) | Sonnet 5 | Standard implementation tasks |
| Teammate (escalated) | Opus 5 | Complex architecture, security-critical, performance-sensitive, intricate animation, deep cross-codebase reasoning |
| Teammate (long-running) | Fable 5 | Work that would otherwise be split across sittings; needs self-verification |
| Subagent (read-only) | Haiku 4.5 | File search, codebase exploration |
| Subagent (code changes) | Sonnet 5, or Opus 5 when complex | Implementation or refactoring |

Teammate models are named in the spawn prompt. `teammateDefaultModel` was removed
in v2.1.234; `CLAUDE_CODE_SUBAGENT_MODEL` still works. Unspecified teammates
inherit the lead's model.

With Fable 5: describe the outcome rather than the steps, hand it ambiguous
problems, and skip the "remember to test this" reminders -- it verifies its own
work without prompting.

## Effort Levels

`low`, `medium`, `high`, `xhigh`, `max`. Default is `high` on every model that
supports effort. Set with `/effort` or `--effort`.

| Level | Use for |
|-------|---------|
| `low` | Mechanical edits, renames, formatting |
| `medium` | Routine implementation with a clear spec |
| `high` | Default. Most coding work |
| `xhigh` | Architecture decisions, subtle debugging |
| `max` | Deepest reasoning; current session only unless set via env var |

`ultracode` is not an effort level -- it sends `xhigh` and additionally has Claude
orchestrate dynamic workflows for substantive tasks. Session-scoped.

## Context Engineering Rules

Context is a finite resource. Every token competes for attention.

1. **CLAUDE.md is always-on and expensive.** Only what applies to every interaction. Target under 200 lines.
2. **Skills are on-demand and cheap.** Reference material, procedures, specialised knowledge. ~1 line each at startup.
3. **Prefer forks over fresh subagents when context matters.** `/subtask` inherits the conversation and reuses the prompt cache, so it costs *less* than a clean subagent. Spawn a fresh `Explore` subagent only when a clean window is the point.
4. **Agent Teams are parallel isolated contexts.** Each teammate has its own window; the lead coordinates via structured messages.
5. **Tell Claude what to keep during compaction.** Specified in the Compaction section of CLAUDE.md.
6. **`/clear` between unrelated tasks.** A clean session with a good prompt beats a long one with accumulated corrections.
7. **Course-correct early.** After 2 failed corrections, `/clear` and restart with a better prompt.
8. **Match effort to the task.** Drop to `low` for mechanical work; reserve `xhigh` for architecture and debugging.
9. **Pick the model per job.** See Model Selection above.

## When CLAUDE.md Is the Wrong Tool

CLAUDE.md is delivered as context, not enforced configuration -- compliance is
likely but never guaranteed. If something must happen at a fixed point every
time, use a **hook** instead. Exit code 2 blocks on `PreToolUse`,
`UserPromptSubmit`, `Stop` and `SubagentStop`; it has no effect on post-action
events like `PostToolUse`.

Hooks are configured in `settings.json`, a plugin's `hooks/hooks.json`, or skill
and subagent frontmatter.

## Parallelism Primitives

| | Subagents | Agent Teams | Workflows |
|---|---|---|---|
| Who decides what runs next | Claude, turn by turn | The lead, turn by turn | The script |
| Where results live | Claude's context window | A shared task list | Script variables |
| What's repeatable | The worker definition | The team definition | The orchestration itself |
| Scale | A few per turn | A handful of peers | Dozens to hundreds per run |
| Reach for it when | You need a focused answer | Agents must challenge each other | The same step repeats across many items |

Subagent caps: 3 levels of nesting, 20 concurrent. The 200-per-session spawn cap was removed in v2.1.224.
Workflow caps: 16 concurrent agents, 1,000 agents per run.
