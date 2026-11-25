---
name: dev-learner
description: Meta-skill — extract reusable skills from the current conversation. Identifies patterns that appeared 3+ times and proposes them as new skills. Pairs with skill-creator builtin.
---

# Dev Learner

Derived from oh-my-claudecode (MIT, Yeachan Heo). Adapted for the EvoNexus Engineering Layer.

Meta-skill: scan the current conversation for patterns that appeared 3+ times and propose extracting them as reusable skills. The "self-improving workspace" feedback loop.

## Use When
- A long session involved repeated workflows that aren't yet skills
- You want to formalize a pattern you keep manually invoking
- Post-EPIC retrospective: what should have been a skill but wasn't?

## Do Not Use When
- Single-pattern conversation → no extraction value
- The pattern is too specific to one project → keep as agent memory
- The pattern is already a skill → just document it better

## Workflow

### Phase 1 — Pattern Detection
Scan the conversation for:
- **Repeated workflows** — same sequence of agents called 3+ times
- **Repeated prompts** — similar instructions issued repeatedly
- **Repeated outputs** — same artifact format produced multiple times
- **Repeated handoffs** — same agent pair invoked together repeatedly

### Phase 2 — Extraction
For each detected pattern:
1. Name it (e.g., "PR review pipeline", "Debug investigation flow")
2. Describe the trigger
3. Document the steps
4. Identify the agents involved
5. Identify the inputs and outputs

### Phase 3 — Proposal
Propose the new skill:
- **Name:** suggested skill name (`dev-{action}` if engineering, `{prefix}-{action}` otherwise)
- **Trigger:** when to invoke
- **Workflow:** the steps
- **Pairs with:** which agents/skills

### Phase 4 — Creation (optional)
If user accepts, hand off to `skill-creator` (builtin) to actually generate the skill file.

## Output

```markdown
## Learner Report — {session topic}

### Patterns Detected
1. **{Pattern name}**
   - Occurrences: 4 times
   - Steps: ...
   - Suggested skill: `dev-{action}`

2. **{Pattern name}**
   - ...

### Skill Proposals
[Detailed proposal for each detected pattern]

### Recommendation
[Which to extract first, which to skip]
```

## Pairs With
- `skill-creator` (builtin) — to generate the actual skill file
- `create-agent` (builtin) — if the pattern warrants a new agent instead
- All 19 engineering agents (which patterns might be extracted from)

## Anti-patterns
- Over-extraction (every 2-occurrence sequence becomes a skill)
- Under-extraction (missing genuine repeated patterns)
- Naming conflicts (proposing names that collide with existing skills)
