---
name: Pull-in
description: Load a specific skill, profile section, or spec into the current conversation on demand. Use when you need deeper context for a focused task without loading everything at once. Adapts to Claude Code, claude.ai, and Cowork.
---

# /pull-in

Load a specific piece of context into the current conversation, on demand.

Use when you want a deeper lens on one thing — voice, design, the spec, a specific skill — without loading every skill every session.

---

## Which surface are you on?

**Claude Code**
You can read skill files directly from `~/.claude/skills/{skill-name}/SKILL.md`, profile from `~/.claude/CLAUDE.md`, and spec from the current project. Read the requested file and hold its content in working memory for the rest of the session.

**claude.ai chat**
You can't read files. When the user says `/pull-in voice`, respond: "Paste your voice skill or the relevant section and I'll load it." Then treat the pasted content as the loaded skill.

**Cowork**
You have workspace access. Read the requested skill, profile, or spec file from the workspace. Same behavior as Code otherwise.

---

## Why this exists

plsBuild OS ships 15 skills. Loading all of them into every session wastes context on stuff not relevant to the current task.

The pattern: keep sessions lean. Pull in only what you need, when you need it.

Default-loaded (always available):
- Profile
- Current spec
- Voice (if you're writing anything user-facing)

Pull-in on demand (loaded only when asked):
- design, pitch, growth, retro, research, audit, support, go-live, learning-log, unblock, naming, agents, learn-codebase

---

## How to invoke

### Explicit mode

```
/pull-in design
/pull-in voice pitch
/pull-in spec
```

Claude loads the named skill file(s) into the conversation. Those skills are now "in context" for the rest of the session.

Multiple skills at once is fine. Don't load all of them — that defeats the purpose.

### Auto-suggest mode

```
/pull-in
```

With no argument, Claude looks at what you're working on, suggests which skills would help, and asks before loading.

Example output:
```
Looking at this conversation, two skills would help:

1. /design — you're choosing layouts and colors
2. /voice — the copy draft in the last message is too corporate

Pull both in? (yes / just design / skip)
```

---

## What counts as a "pull"

When Claude pulls in a skill, it reads the full SKILL.md content and holds it in working memory for the rest of the session. Treat the skill as if the user had invoked it directly.

The pull happens once per session per skill. If the user asks to pull in the same skill twice, confirm once that it's already loaded rather than duplicating.

---

## Pulling in profile or spec sections

For profile and spec, support partial pulls:

```
/pull-in profile.stack          # just the stack defaults
/pull-in profile.values         # just the values section
/pull-in spec.current-focus     # just what they're working on now
/pull-in spec.decisions         # just the key decisions made
```

Small chunks. Scoped context. Faster than reloading the whole file.

---

## When NOT to use this

- **If you need all of it.** If a task genuinely needs five skills at once, just invoke them normally. Pull-in is for *focused* work, not everything-work.
- **For default-loaded content.** Profile, current spec, and voice are already loaded. Don't re-pull them.
- **As a substitute for invoking the skill directly.** If you know you want `/design`, run `/design`. Pull-in is for when you want design thinking *in the background* while you work on something else.

---

## Graduation pattern

Once you're deep in the workflow layer (Notion, Linear, etc.), pull-in evolves into "link the relevant page." Same idea — bring in focused context — just sourced from your external system instead of a local file.
