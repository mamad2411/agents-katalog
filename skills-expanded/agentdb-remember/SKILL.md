---
name: agentdb-remember
description: Store a memory in AgentDB — an episode (task + outcome + critique), a pattern, or a skill. Use when the user says "remember this", "save this for later", "add to memory", or when the agent has just succeeded/failed at a task and the lesson is worth keeping.
---

# Remember

Persist a memory into AgentDB so a future session can recall it. Three flavors — pick the right one for what's being remembered:

## When to use which

| User phrasing | Use |
|---|---|
| "remember that X works for Y" | **Pattern** — `agentdb_pattern_store` |
| "save what happened when I tried X" | **Episode (Reflexion)** — `agentdb_reflexion_store` |
| "this is a reusable approach for problem X" | **Skill** — `agentdb_skill_create` |

## Pattern (most common)

```
agentdb_pattern_store(
  content: "JWT refresh token rotation pattern: ...",
  metadata: { topic, project, success: true }
)
```

Use for facts, conventions, anti-patterns, or anything that should resurface as a hint when a similar query comes up later.

## Episode

```
agentdb_reflexion_store(
  sessionId: <session>,
  task: <what we were trying to do>,
  input: <what we tried>,
  output: <what happened>,
  critique: <what we'd do differently>,
  reward: 0..1,
  success: true|false
)
```

Use right after a task completes — success OR failure. Failed episodes feed `getCritiqueSummary`; successful ones feed `getSuccessStrategies`.

## Skill

```
agentdb_skill_create(
  name: <short verb-noun>,
  description: <what it does>,
  precondition: <when to use>,
  action: <how to do it>,
  outcome: <what success looks like>
)
```

Use when a pattern has been validated 3+ times and you want it elevated to a first-class reusable skill (queryable by intent embedding).

## Don't

- Don't store secrets, API keys, or PII. AgentDB has no built-in redaction. The agentdb-aidefence plugin (separate) handles that — without it, treat the .rvf as containing whatever you put in it.
- Don't store huge blobs. The pattern store is for retrieval signals, not file storage. Use a real blob store + put the URL in metadata.
- Don't store low-quality patterns to "be safe" — recall quality degrades fast under noise. If reward < 0.3, prune it on the next consolidation pass.
