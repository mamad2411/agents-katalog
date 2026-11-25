---
name: senior-skill-authoring
description: Use when creating a new agent skill, or changing an existing skill's trigger, process, boundaries or evals.
---

# Skill Authoring

**Core rule:** a skill earns its place only when agents demonstrably behave worse without it.

## 1. Prove a skill is the right abstraction

Answer before writing:

- What recognizable situation should trigger it?
- What goes wrong today without it? Write down one concrete failure you observed or can reproduce.
- Could an existing skill own this behavior?
- Is this a reusable workflow (skill), a project-only rule (repository instructions), reference material, or a deterministic mechanic (script/CLI)?

## 2. Write the trigger first

The `description` says **when** to use the skill and, where useful, when not to. Start with "Use when…". Do not summarize the procedure there: an agent that reads a summary may follow the summary instead of the skill.

Keep the name prefixed (`senior-…`) and specific enough not to collide with host or third-party skills.

## 3. Keep the hot path small

`SKILL.md` holds the minimum procedure needed every time the skill triggers. Put material needed only sometimes in one-level-deep files the skill points to at the step that needs them:

```text
senior-example/
├── SKILL.md
├── references/
│   └── topic.md
└── scripts/
    └── deterministic-check.mjs
```

`npm run validate:skills` rejects a `SKILL.md` over 500 lines of body or 20,000 bytes: hosts may truncate longer skills after context compaction.

## 4. Separate judgment from mechanics

Keep interpretation, prioritization, trade-offs and explanations in the skill. Move behavior to scripts or the `senior` CLI when it is repeated, deterministic, fragile to reconstruct by hand, or easier to test as code.

## 5. Write for current models

Current models follow instructions literally. Use normal volume and explicit conditions ("at medium risk and above…") instead of capital letters and absolute threats, which make them apply heavy process to trivial work. Put one short core rule at the top, and a table of the excuses the agent is likely to make, each paired with what to do instead.

## 6. Define the exit and the boundaries

Every skill needs an exit condition. Destructive or external actions need an explicit approval boundary. Do not impose heavyweight process on low-risk work.

## 7. Write evals before declaring success

At least three cases per skill:

1. a request that should trigger it;
2. a nearby request that should not trigger it, or should take the light path;
3. an edge or pressure case that tests its most important boundary.

Each case lists observable required and forbidden behaviors. Then run `npm run validate:skills` and `npm run validate:evals`. Structural validation is not evidence that the skill improves behavior: when a runner is available, compare runs with and without the skill and judge the outcome, not only whether the steps were followed.

| If you notice yourself thinking… | Do this instead |
|---|---|
| "This is useful advice, it deserves a skill" | Show the failure it prevents first |
| "I'll make it MANDATORY so it always fires" | State when it applies; loud rules over-trigger |
| "The validator passes, so the skill works" | Validation checks shape, not behavior |
