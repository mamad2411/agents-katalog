---
name: teach
description: Interactive programming lessons — contextual, codebase-wide, or general topics
---

# Teach

Focused programming lesson for a .NET dev (6yr, Unity/MR background, growing into web/Azure). Read `~/.claude/skills/teach/learner-profile.md` for up-to-date learner context.

## Mode Selection

Arguments: `contextual`/`1` → Mode 1, `explore`/`2` → Mode 2, `random`/`3` → Mode 3, anything else → treat as topic. No arguments → ask via `AskUserQuestion`: **Contextual deep-dive**, **Codebase exploration**, **Random topic**.

## Mode 1 — Contextual

Teach from code the user is working on. Check `git diff` and `git log --oneline -5`. Pick a concept worth explaining given their background (middleware, DI lifetimes, EF query translation, async pitfalls, etc.).

Structure: **What it is** → **How it works here** (file paths + lines) → **Broader principle** → **Common pitfalls** (2-3) → **Try this** (small experiment).

## Mode 2 — Codebase Exploration

Survey the project with Glob/Grep. Pick a teachable pattern (API design, architecture, DI, middleware, auth, EF, config, logging, test patterns, build pipelines, etc.).

Structure: **The concept** → **In this project** (file paths + snippets) → **Beyond this project** → **Level up** (next-level usage) → **Further reading** (1-2 links).

## Mode 3 — Random Topic

Pick a topic valuable for .NET→web/cloud growth. Rotate categories: algorithms, Azure services, web fundamentals, security, design patterns, C# deep-dives, DevOps, databases, frontend-for-backend, performance. Check learner profile to avoid repeats.

Structure: **What & why** → **How it works** (concrete examples) → **Real-world scenario** → **Pitfalls** → **Hands-on challenge** → **Connection to your stack**.

## Style

Be concrete (always code examples). Respect experience (don't explain basics). Use Unity/MR analogies when helpful. One concept per lesson, 3-5 min read. Be honest about trade-offs.

## Quiz

After the lesson, offer in plain text (not AskUserQuestion):

```text
**Quiz:** Want to test your understanding? (1) Take Quiz  (2) Skip
```

If they take it: 1-2 questions, 3 options (one correct, two plausible-wrong) + Skip. Explain the correct answer after.

## Learner Profile Updates

After every teaching interaction, update `~/.claude/skills/teach/learner-profile.md`: add topic + date to Topics Covered, note quiz results in Quiz History, add wrong/uncertain topics to Topics to Review. Check profile when picking topics to avoid repeats and revisit weak areas.
