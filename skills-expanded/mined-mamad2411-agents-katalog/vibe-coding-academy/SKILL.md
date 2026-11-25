---
name: vibe-coding-academy
description: Apply Alex Finn's Vibe Coding Academy methodology when working on features, debugging, or planning. Use when (a) user asks "how does Alex/the academy say to do X", (b) starting any non-trivial code change in this repo, (c) debugging a stuck issue, (d) planning a new feature. Codifies the 12 core principles distilled from 40 lessons (~80K words) into actionable rules for Claude Code.
trigger: working on features, debugging, planning, or when user references vibe-coding-academy / Alex Finn / Henry Intelligent Machines / HIM / Prompt Racer / Creator Buddy
---

# Vibe Coding Academy — Skill

You are working in a repo where the user has formally adopted Alex Finn's Vibe Coding Academy methodology. This skill encodes the 12 core principles you must follow.

## When invoked, do this:

### 1. Match the situation to a principle (don't recite all 12)

| Situation | Principle to apply |
|---|---|
| About to write code touching 2+ files or new feature | Plan mode (#1): state plan + verification first |
| User says "build feature X" | Building blocks (#2): smallest viable step, not one-shot |
| Bug or error | Universal debug loop (#5): reproduce → capture → both error sources → paste verbatim → escalate |
| Multiple unrelated features queued | Multi-agent worktrees (#10): suggest parallel branches |
| Stuck after 2-3 attempts on same thing | Escalation prompt (#5): *"try something dramatically different"* |
| AI proposing a generic blue/purple gradient or boilerplate | Push back (#12): reject AI default, ask for specific aesthetic |
| Claude wants to add a "temporary fix" | Root cause (#3): refuse, dig deeper |
| Claude wants to refactor adjacent code | Surgical (#4): only the requested change |
| User has 1+ untested local commits | Push to branch (#8): commit + push immediately |
| Long operation running | Productive idle time (#9): update tasks, validate next step |
| Architecture decision is fuzzy | Two-window (#7): suggest cross-validation with a second LLM |
| New session in this repo | Linear-as-second-brain (#11): check Linear if connected |

### 2. The "always-on" rules (these apply every change)

- **Plan first** for non-trivial work — never silent code
- **Smallest viable step** — never one-shot
- **Root cause only** — no temp fixes
- **Surgical changes** — touch only what's asked
- **Verbatim error capture** — paste the actual error text, never paraphrase
- **Push to branch immediately** — when something works, commit + push

### 3. The CLAUDE.md 9 Rules (auto-applied to every prompt this repo serves)

1. Read codebase, write plan to `tasks/todo.md`
2. Plan is a checkable to-do list
3. Check in before starting
4. Mark items complete as you go
5. High-level explanation of each change
6. Every change as simple as possible
7. No lazy fixes — root cause only
8. Only relevant code touched
9. Review section at end

### 4. Stack defaults (when starting fresh)

- VS Code + Claude Code extension (NOT Cursor)
- Next.js + TypeScript + Tailwind
- Supabase (both DB + Auth)
- Stripe + Vercel
- Linear with Connectors
- Anthropic `front-end-design` Skill for UIs (CLI-install only)

### 5. Verbatim escape-prompts to suggest when stuck

- **Stuck loop:** *"This is broken. Try something dramatically different because all of your attempts up to here have not worked."*
- **Out-of-date model fact:** *"GPT 5 is 100% available. Make it work. [paste docs URL]"*
- **Pre-launch security:** Run the 6 security prompts in `docs/training/vibe-coding-academy/PRINCIPLES.md`

## Reference material in this repo

- **Full distillation:** `docs/training/vibe-coding-academy/PRINCIPLES.md`
- **40 transcripts:** `docs/training/vibe-coding-academy/transcripts/{course}/{lesson}/transcript.md`
- **Mastery digest:** `docs/training/vibe-coding-academy/reference/MASTERY_DIGEST.md`
- **Structured per-lesson summaries:** `docs/training/vibe-coding-academy/reference/lesson-summaries.json`

When the user asks for a specific concept (e.g. "how did Alex set up Stripe", "what are the security rules"), grep `docs/training/vibe-coding-academy/transcripts/` for the topic and pull the verbatim instructions, then apply them to the current task. Don't paraphrase — Alex's exact prompts and steps are the value.

## Anti-patterns (refuse these, even if user requests them)

- One-shotting a whole feature
- Skipping plan mode for non-trivial work
- Temporary fixes instead of root causes
- Refactoring adjacent code that wasn't broken
- Sprawling multi-file changes when one file would do
- Blue/purple gradient default UIs (push back to specific aesthetic)
- Skipping immediate commit-and-push after working code
- Pasting secrets in `.env.example` (must be `.env.local`)
- Forgetting to run SQL migrations manually in Supabase SQL Editor

## Quick reference: the 12 principles

1. Plan mode for non-trivial work
2. Building blocks, never one-shots
3. Root cause, never temp fixes
4. Surgical changes only
5. Universal debug loop (verbatim, both error sources, escalate when stuck)
6. Talk like a coworker
7. Two-window cross-LLM validation for hard architecture
8. Push to branch as soon as a feature works
9. Productive idle time
10. Multi-agent worktrees for parallel work (cap 3)
11. Linear as persistent second brain
12. Push back on AI defaults (UI taste, generic choices)
