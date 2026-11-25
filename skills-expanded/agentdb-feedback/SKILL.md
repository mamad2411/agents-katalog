---
name: agentdb-feedback
description: Close the learning loop — record reward signal for an action AgentDB suggested. Use after using anything from agentdb_pattern_search / reflexion_recall / skill_search / learning_route. The bandit needs the signal to improve.
---

# Feedback

Close the loop on a memory or routing decision so AgentDB's bandit learns.

## When to use

- **Always** after using a recall result, a routed action, or a skill suggestion. The most-undervalued part of the loop.
- After a task ends — record episode-level reward.
- When intentionally ignoring a suggestion — record *negative* reward so the bandit notices.

## API

```
agentdb_record_feedback(
  id:        <pattern/skill/episode/decision id>
  reward:    -1..1
  context?:  { task, outcome, latency, ... }
)

agentdb_bandit_update(
  arm:       <bandit arm name>
  reward:    -1..1
)
```

## Reward conventions

| Outcome | Reward |
|---|---|
| Used the suggestion, task succeeded | **+1.0** |
| Used the suggestion, task partial success | **+0.5** |
| Used the suggestion, didn't help | **0.0** |
| Used the suggestion, made things worse | **-0.5** |
| Ignored the suggestion (other reason) | **-0.1** (mild downweight) |
| Rejected as wrong / harmful | **-1.0** |

## Pattern: bracket every recall with feedback

```
const hits = await agentdb_pattern_search(query)
for (const h of useful(hits)) {
  use(h)
  await agentdb_record_feedback(h.id, +1)
}
for (const h of skipped(hits)) {
  await agentdb_record_feedback(h.id, -0.1)
}
```

Without negative feedback, the bandit only sees "winners" and exploration starves.

## Don't

- Don't aggregate. Per-id feedback is what the bandit consumes; a single "task succeeded" reward attached to the task itself doesn't update individual memory weights.
- Don't fabricate reward. Honest 0.0 ("retrieved but didn't help") teaches more than dishonest +1.
- Don't only reward — *especially* record negative reward. It's the higher-information signal.
