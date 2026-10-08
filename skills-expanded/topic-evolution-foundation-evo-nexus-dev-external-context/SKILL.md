---
name: dev-external-context
description: Parallel external documentation lookup. Spawn multiple @scroll-docs agents simultaneously to fetch SDK refs, API docs, and framework guides for different topics in one pass.
---

# Dev External Context

Derived from oh-my-claudecode (MIT, Yeachan Heo). Adapted for the EvoNexus Engineering Layer.

Parallel external research. When a task needs multiple unrelated external lookups (SDK A + Framework B + Standard C), spawn `@scroll-docs` instances in parallel instead of serial.

## Use When
- Task requires 3+ external doc lookups on different topics
- Time-sensitive research where serial lookups would be slow
- Cross-referencing multiple SDKs / frameworks for the same problem

## Do Not Use When
- Single lookup → use `@scroll-docs` directly
- Internal codebase questions → use `@scout-explorer` instead
- The lookups are dependent (B needs A's result first) → run serial

## Workflow

1. **Decompose** the research need into 2+ independent topics
2. **Spawn** `@scroll-docs` agents in parallel — one per topic
3. **Collect** the briefs as they return
4. **Synthesize** into a single research summary
5. Save to `workspace/development/research/[C]external-context-{topic}-{date}.md`

## Output Format

```markdown
## External Context — {topic}

### Lookup 1: {topic A}
[from @scroll-docs]

### Lookup 2: {topic B}
[from @scroll-docs]

### Lookup 3: {topic C}
[from @scroll-docs]

## Synthesis
[Combined understanding]

## Conflicts
[Where sources disagree]

## Recommendation
[Next step based on combined research]
```

## Pairs With
- `@scroll-docs` (parallel workers)
- `@compass-planner` (consumer of synthesized research)
- `@apex-architect` (consumer for architecture decisions)
