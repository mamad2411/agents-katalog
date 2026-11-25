---
name: agentdb-skill-create
description: Promote a validated pattern into a reusable Skill in AgentDB's skill library. Use when the same approach has worked 3+ times across episodes, or when the user explicitly says "make this a skill" / "save this as reusable".
---

# Promote to Skill

Take an approach that's been validated multiple times and elevate it to a first-class Skill — queryable by intent, composable into chains, and tracked separately from one-off patterns.

## When to use

- **Repeated success** — a pattern has reward ≥ 0.7 across 3+ episodes
- **User explicit** — "make this reusable", "save as a skill"
- **Pre-deployment** — codifying tribal knowledge before shipping the agent

## Anatomy of a skill

```
agentdb_skill_create(
  name:         <verb-noun-noun>          // e.g. "rotate-jwt-refresh-token"
  description:  <one-liner>               // what it does
  precondition: <plain English query>     // matched by intent embedding
  action:       <step list>               // executable steps
  outcome:      <success criteria>        // what "worked" looks like
  tags:         [<topic>, <stack>, ...]
  metadata:     { sourceEpisodeIds: [...], confidence }
)
```

The `precondition` is what makes the skill discoverable — it's embedded and matched against future task intents. Write it like a search query: *"need to rotate a JWT refresh token without invalidating active sessions"*, not like a docstring.

## Composition

Skills can chain via `agentdb_skill_compose`:

```
compose(
  intent: "set up authenticated API with token rotation",
  available: [skill_a, skill_b, skill_c]
) → bandit picks the best chain ordering
```

The bandit tracks composition rewards over time; bad orderings decay automatically.

## Don't

- Don't skill-ify single successes. One data point doesn't generalize.
- Don't skill-ify project-specific code paths. Skills should be transferable; if the action only works in one repo, it's a pattern, not a skill.
- Don't put secrets or repo-specific paths in `action`. Use placeholders.
