---
name: agentdb-recall
description: Retrieve relevant memories for the current task from AgentDB. Use at the start of a task to load prior knowledge, when stuck to surface what worked before, or when the user asks "what do we know about X" / "have we done this before?"
---

# Recall

Pull relevant past memories into the current context.

## When to use

- **Task start** — auto-load any prior episodes / patterns / skills that look relevant
- **When stuck** — search for past failures + critiques on similar tasks
- **User asks** — "have we done this?", "what do we know about X?"
- **Decision point** — surface successful strategies before committing to one

## Pick the right tool

| Need | Tool | Returns |
|---|---|---|
| Similar past tasks | `agentdb_reflexion_recall` | Episodes, top-k by similarity |
| Lessons from past failures | `agentdb_critique_summary` | Combined critique text |
| What worked last time | `agentdb_success_strategies` | Approach summaries from high-reward episodes |
| Generic patterns / facts | `agentdb_pattern_search` | Patterns ranked by similarity |
| Reusable skills by intent | `agentdb_skill_search` | Skills ranked by precondition match |

## Standard recall flow at task start

1. Embed the current task description.
2. Call `agentdb_reflexion_recall` with `k=5`, `minReward=0.5`.
3. Call `agentdb_pattern_search` with the same query, `k=5`.
4. Dedupe + rank — present the top 3-5 to the user as "things I found that look relevant."
5. If user-confirmed useful: call `agentdb_record_feedback` (or `recordFeedback` via the library) so the bandit learns.

## Filters worth knowing

- `minReward` — drop low-quality matches (default 0.3).
- `onlyFailures` — explicitly query the postmortem set when debugging.
- `onlySuccesses` — only winning approaches when copying a strategy.
- `timeWindowDays` — recent context only when the codebase has shifted.

## Don't

- Don't dump all 50 hits — pick 3-5. Cognitive overload tanks quality.
- Don't recall and ignore. If you used a memory, record feedback. If you didn't, record negative feedback. The bandit needs the signal.
- Don't recall episode content verbatim into prompts when the task changes. Summarize the *lesson*, not the artifact.
