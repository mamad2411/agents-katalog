---
name: agentdb-route
description: Ask the AgentDB bandit which RL algorithm / skill / pattern fits the current task best. Use at task start when there are multiple plausible approaches and you want the data-driven pick.
---

# Route

Ask the Thompson Sampling bandit which approach to use for the current task.

## When to use

- Task start with multiple plausible skills / algorithms
- Branching decision — A/B between approaches
- Cold start on a new task type — let the bandit explore

## API

```
agentdb_learning_route(
  task:        <description>
  candidates?: [<skill_id> | <algo>, ...]   // omit to consider everything
  context?:    { stack, project, ... }
)

Returns: { picked, expectedReward, confidence, alternatives: [...] }
```

## How it picks

Thompson Sampling: each candidate has a Beta(α, β) posterior over reward. The bandit samples once from each, picks the highest sample. Exploration emerges naturally — uncertain candidates get tried until their posterior tightens.

Four bandit decision points across AgentDB:

1. **Pattern ranking** — which historical pattern matches this query best?
2. **Algorithm selection** — which RL algo trains best on this task?
3. **Compression tier** — full / PQ8 / PQ4 / binary?
4. **Skill composition** — chain A→B→C or A→D→E?

The router unifies them: it returns the picked candidate AND a `decisionTrace` showing which decision points fired.

## Use the result, then close the loop

```
const { picked } = await agentdb_learning_route(...)
const result = await runWith(picked)
agentdb_bandit_update(arm: picked, reward: result.reward)
```

The `agentdb-feedback` skill (this plugin) wraps the close-loop step.

## Don't

- Don't second-guess the bandit on early calls — exploration is by design.
- Don't refuse the bandit's pick without recording negative reward. If you ignored a suggestion and used a different one, log that — otherwise the bandit thinks its pick "worked" because no negative signal arrived.
