---
name: claude-code-reference
description: Reference tables for Claude Code configuration -- the memory hierarchy and what each layer costs, model selection and pricing, effort levels, and context engineering rules. Use when auditing CLAUDE.md, deciding where a piece of knowledge belongs, choosing a model or effort level, or debugging why an instruction was not followed.
---

# Claude Code Reference

Verified against Claude Code v2.1.311, October 2026. These are lookup tables, not
behavioural rules -- the always-on rules live in `~/.claude/CLAUDE.md`.

## Memory Hierarchy

Claude Code loads memory in layers. Understanding the cost of each layer prevents
context waste.

| Layer | Location | Loaded | Cost |
|-------|----------|--------|------|
| Managed policy | macOS `/Library/Application Support/ClaudeCode/CLAUDE.md`; Linux/WSL `/etc/claude-code/CLAUDE.md`; Windows `C:\Program Files\ClaudeCode\CLAUDE.md` | Every session | Always on, cannot be excluded by user settings |
| User | `~/.claude/CLAUDE.md` | Every session | Always in context |
| User rules | `~/.claude/rules/*.md` | Every session unless `paths:` scoped | Always in context |
| Project | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Every project session | Always in context |
| Project rules | `.claude/rules/*.md` | Every project session | Always in context |
| Path-scoped rules | `.claude/rules/*.md` with `paths:` frontmatter | When Claude reads, writes or edits a matching file, or views it via Bash | On demand |
| Project local | `./CLAUDE.local.md` | Every project session | Always in context (gitignored) |
| Child directory | `./packages/foo/CLAUDE.md` | On demand | Only when Claude reads, writes or edits files in that dir |
| Auto memory | `~/.claude/projects/<id>/memory/MEMORY.md` | First 200 lines **or** 25KB, whichever comes first | Partial, per session |
| Skills | `.claude/skills/<name>/SKILL.md` | Description at start; full body on invoke | One description per skill at start (keep it short) |

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
| Fable 5.1 | `fable` | 1M | $10 / $50 | Long autonomous sessions, ambiguous root-cause work, tasks larger than one sitting |
| Opus 5.5 | `opus` | 1M | $4 / $20 | What `opus` resolves to. Team lead, complex architecture, security-critical code |
| Sonnet 5.5 | `sonnet` | 1M | $2 / $10 | Standard teammates, daily coding |
| Haiku 5.5 | `haiku` | 1M | $0.10 / $0.50 (rises to $0.50 / $2.50 over 100K tokens) | Read-only subagents, file search, codebase exploration |

| Role | Model | When |
|------|-------|------|
| Team lead | Opus 5.5 | Coordination, synthesis, complex decomposition |
| Teammate (default) | Sonnet 5.5 | Standard implementation tasks |
| Teammate (escalated) | Opus 5.5 | Complex architecture, security-critical, performance-sensitive, intricate animation, deep cross-codebase reasoning |
| Teammate (long-running) | Fable 5.1 | Work that would otherwise be split across sittings |
| Subagent (read-only) | Haiku 5.5 | File search, codebase exploration |
| Subagent (code changes) | Sonnet 5.5, or Opus 5.5 when complex | Implementation or refactoring |

Teammate models are named in the spawn prompt. `teammateDefaultModel` was removed
in v2.1.234. A teammate's model resolves in this order: the spawn prompt, the agent
definition's `model`, `CLAUDE_CODE_SUBAGENT_MODEL` (a default, not an override, since
v2.1.251; `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1` forces it), then the lead's model.
`CLAUDE_CODE_WORKFLOW_SUBAGENT_MODEL` (v2.1.296) pins every workflow agent to one model.

Fable 5, Opus 5, Sonnet 5 and Haiku 4.5 are now legacy (still available). The `best`
alias is Fable 5.1 where available, otherwise Opus 5.5.

## Effort Levels

`low`, `medium`, `high`, `xhigh`, `max`. Default is `high` on models that
support effort, except Opus 5.5, Sonnet 5.5 and Haiku 5.5, which default to `medium`
(Opus 4.7 defaults to `xhigh`). Set with `/effort` or `--effort`.

| Level | Use for |
|-------|---------|
| `low` | Mechanical edits, renames, formatting |
| `medium` | Routine implementation with a clear spec |
| `high` | Default. Most coding work |
| `xhigh` | Architecture decisions, subtle debugging |
| `max` | Deepest reasoning; current session only unless set via env var |

`ultracode` is not an effort level. Since v2.1.284 it is a separate toggle (Tab in the
`/effort` slider, or `/effort ultracode on|off`) that has Claude orchestrate dynamic
workflows at whichever effort level the session runs at. Only the `--effort ultracode`
launch flag also sets `xhigh`.

## Context Engineering Rules

Context is a finite resource. Every token competes for attention.

1. **CLAUDE.md is always-on and expensive.** Only what applies to every interaction. Target under 200 lines.
2. **Skills are on-demand and cheap.** Reference material, procedures, specialised knowledge. One short description each at startup.
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
`UserPromptSubmit`, `Stop` and `SubagentStop`; it cannot block post-action
events like `PostToolUse` (stderr is still shown to Claude).

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
