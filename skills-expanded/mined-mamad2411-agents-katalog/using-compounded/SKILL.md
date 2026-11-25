---
name: using-compounded
description: Use this skill at the start of any session where compounded is installed, or whenever the user mentions earning trust, verifying skills, the trust ladder, compounded, the trust gradient, autonomous skills, or asks how compounded works. Explains the four trust states (.proposed, .verified, .trusted, .autonomous) and when each applies.
---

# Using compounded

compounded is installed. This means three things are true:

1. **A user-global memory file** lives at `~/.claude/compounded/USER.md`. It is loaded into your context at session start. It is bounded — usually under 1500 characters. Use it for preferences and facts that apply across all the user's projects, not for project-specific notes (those belong in CLAUDE.md or AutoMemory's MEMORY.md).

2. **Skills you create earn trust over time.** Skills do not start trusted. They start as proposals, get verified by replay, and graduate through a four-state trust ladder.

3. **There is a portable archive.** The user can run `/compounded:export` to bundle their USER.md and verified skills into a single archive that moves between machines.

## The Trust Ladder

When you (the agent) discover a useful procedure during a session — something non-trivial, repeatable, that took you more than a couple of tool calls to figure out — you may propose it as a skill. Skills then graduate through four states:

| State | What it means | When it loads |
|-------|---------------|---------------|
| `.proposed` | Just authored. Untested. | Never auto-loaded. Listed by `/compounded:status`. |
| `.verified` | Replayed successfully on at least one matching task. | Loads only when explicitly invoked by name. |
| `.trusted` | Used 3+ times without correction. | Auto-loads when relevant, asks for confirmation before applying. |
| `.autonomous` | Used 10+ times, zero corrections in last 5. | Auto-loads and applies without asking. |

Promotions happen automatically based on usage. Demotions also happen automatically:

- A user correction during a skill's use → demote one step
- 3 corrections in 30 days → demote to `.proposed`
- A failed verification on a `.proposed` skill → move to `.rejected/` (recoverable, not deleted)

## When to propose a skill

Use the `compounded-author` skill (which has the full procedure) when **all** of these are true:

- The task involved more than 3 tool calls
- The procedure is repeatable on a similar future task
- You actually solved it (not just gave up halfway)
- It is not redundant with an existing skill
- It does not duplicate something native (Claude Code's bundled skills, AutoMemory, AutoDream)

When in doubt, do not propose. The trust ladder works only if rejection is rare and meaningful. Proposing too aggressively pollutes `.proposed/` and dilutes verification signal.

## When NOT to propose

- Trivial procedures already obvious to a competent agent
- One-off tasks unique to this session
- Things the user explicitly asked you not to remember
- Procedures that depend on session-specific paths or variables you cannot abstract

## How memory composes with compounded

You may see all of these in context at session start. They serve different purposes; do not conflate them.

- `CLAUDE.md` — instructions the user wrote. Authoritative. Follow them.
- `MEMORY.md` (AutoMemory, per-project) — notes Claude Code wrote about *this project*. Trust but verify.
- `USER.md` (compounded, user-global) — preferences and facts that apply across all the user's projects. Cross-project, machine-independent.
- A list of available skills — names and one-line descriptions. Load full skill content only when relevant.

## What you should NOT do

- Do not edit the trust state of a skill manually. The state is managed by compounded's verifier subagent and hooks.
- Do not write to `~/.claude/compounded/skills/` directly with file tools. Use the `skill_propose` mechanism described in the `compounded-author` skill.
- Do not assume a skill is verified just because it exists. Check its directory: `.proposed/`, `.verified/`, `.trusted/`, `.autonomous/`.
- Do not propose skills that are really "notes." Notes go in MEMORY.md (AutoMemory handles them) or USER.md (the user owns it).

## Available commands

- `/compounded:status` — shows USER.md size, skill counts by state, recent transitions, recent rejections
- `/compounded:trust-status` — visualizes the trust ladder, shows promotion-worthy and demotion-worthy skills
- `/compounded:export <path>` — produces a portable archive
- `/compounded:import <path>` — merges an archive on a new machine
- `/compounded:verify <skill>` — manually run the verifier on a `.proposed/` skill
- `/compounded:trust <skill>` — manually promote a skill (skip the gradient)
- `/compounded:demote <skill>` — manually drop a skill back one trust state
- `/compounded:pin <skill>` — lock a skill at its current trust state

## Pitfalls

- Skills in `.proposed/` are NOT in your skill index. You cannot invoke them. They are draft hypotheses, not capabilities.
- The verifier subagent runs only when a `.proposed/` skill matches the current session's task. Most sessions trigger zero verifier calls. If a proposal sits unverified for 30 days, it is auto-rejected (with an entry in the rejection log).
- The trust state is per-skill, not per-user. If you reset trust on a skill, you reset it for everyone using that skill on this machine.
