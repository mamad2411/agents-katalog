---
name: using-moe
description: Use when starting any conversation - establishes how to find and use skills, requiring skill invocation before ANY response including clarifying questions
---

<SUBAGENT-STOP>
If you were dispatched as a subagent to execute a specific task, ignore this skill.
</SUBAGENT-STOP>

<BOOTSTRAP-CONTEXT>
{bootstrap-context}
</BOOTSTRAP-CONTEXT>

<EXTREMELY-IMPORTANT>
If you think there is even a 1% chance a skill might apply to what you are doing, you ABSOLUTELY MUST invoke the skill.

IF A SKILL APPLIES TO YOUR TASK, YOU DO NOT HAVE A CHOICE. YOU MUST USE IT.

This is not negotiable. You cannot rationalize your way out of this.
</EXTREMELY-IMPORTANT>

## The Rule

**Invoke relevant or requested skills BEFORE any response or action** — including clarifying questions, exploring the codebase, or checking files. If it turns out wrong for the situation, you don't have to use it.

**Before entering plan mode:** if you haven't already brainstormed, invoke the brainstorming skill first.

Then announce "Using [skill] to [purpose]" and follow the skill exactly. If it has a checklist, create a todo per item.

## Skill Priority

When multiple skills apply, process skills come first — they set the approach, then implementation skills (frontend-design, etc.) carry it out. Brainstorming and systematic-debugging are Moe's most common process skills, but the rule holds for any of them.

- "Let's build X" → `brainstorming` first, then implementation skills.
- "Fix this bug" → `systematic-debugging` first, then domain skills.

**Workflow depth vocabulary.** `brainstorming` classifies every
request by DEPTH — **patch** (smallest: one-line fix, config, probe),
**change** (well-scoped modification to a flow that already exists in
this repo), **feature** (new subsystem or interface). Skills that fire
only at the `feature` depth (`write-plan`,
`sdd`, `execute-plan`) say so under an "At
this depth" note at their top.

## Red Flags

These thoughts mean STOP—you're rationalizing:

| Thought | Reality |
|---------|---------|
| "This is just a simple question" | Questions are tasks. Check for skills. |
| "I need more context first" | Skill check comes BEFORE clarifying questions. |
| "Let me explore the codebase first" | Skills tell you HOW to explore. Check first. |
| "I can check git/files quickly" | Files lack conversation context. Check for skills. |
| "Let me gather information first" | Skills tell you HOW to gather information. |
| "This doesn't need a formal skill" | If a skill exists, use it. |
| "I remember this skill" | Skills evolve. Read current version. |
| "This doesn't count as a task" | Action = task. Check for skills. |
| "The skill is overkill" | Simple things become complex. Use it. |
| "I'll just do this one thing first" | Check BEFORE doing anything. |
| "This feels productive" | Undisciplined action wastes time. Skills prevent this. |
| "I know what that means" | Knowing the concept ≠ using the skill. Invoke it. |

## Skill Triggers

Match your current task against these triggers to decide which skill to load.
Skills without triggers here are general-purpose — check their description in
the skill listing.

- **`brainstorming`** — New creative work needing design exploration (features, components, behavioral changes). *Skip for:* bug fixes, refactoring, test additions, docs, or tasks with an approved spec.
- **`write-plan`** — Approved requirements or design ready for a multi-task implementation plan. *Skip for:* initial exploration (use `brainstorming`), single-file changes, bug fixes, or when a plan already exists (use `sdd`).
- **`sdd`** — Executing a multi-task plan with fresh-context isolation. *Skip for:* single tasks, debugging, initial planning, or low-level dispatch without a plan.
- **`dispatch-agents`** — Low-level mechanics for 2+ independent parallel tasks outside a plan. *Skip for:* plan execution (SDD includes dispatching), sequential tasks, single tasks.
- **`improve-architecture`** — Deliberate architectural review across modules. *Skip for:* known refactors, single-module fixes, code questions, debugging, initial design.
- **`iterate`** — Large specs (10+ files, 100+ requirements) needing audited sprints with behavior evidence. *Skip for:* well-scoped features, single tasks, bug fixes, or projects without prior planning.
- **`write-skill`** — Creating, editing, or pressure-testing SKILL.md files. *Skip for:* discussing skills conceptually, invoking skills, editing non-skill docs, building plugins.

## Platform Adaptation

If your harness appears here, read its reference file for special instructions:

- Antigravity: `references/antigravity-tools.md`
- Codex: `references/codex-tools.md`
- Gemini CLI: `references/gemini-tools.md`
- OpenCode: `references/opencode-tools.md`

## User Instructions

User instructions (CLAUDE.md, AGENTS.md, GEMINI.md, etc, direct requests) take precedence over skills, which in turn override default behavior. Only skip skill workflows or instructions when your human partner has explicitly told you to.
