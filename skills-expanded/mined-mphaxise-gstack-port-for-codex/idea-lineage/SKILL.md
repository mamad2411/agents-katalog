---
name: idea-lineage
description: Trace one idea's evolution through the local brain corpus with cited evidence, reversals, and current live version.
---

# Idea Lineage

Use this skill when the user asks where an idea came from, how their thinking changed, what the current version is, or what branches were abandoned.

This port is adapted from `garrytan/gbrain` at commit `814258dda67945ffec9457a1e73980e947b7e462`.

## Workflow

1. Resolve the target idea:
   - restate the idea in one sentence
   - search exact phrases and close variants with `python3 scripts/brain_search.py`
   - inspect likely concept, source, and idea pages directly
2. Gather evidence:
   - dates
   - source page slugs
   - direct snippets or quotes
   - related concepts and backlinks when present
3. Classify the lineage:
   - first mention
   - best articulation
   - current live version
   - reversals
   - contradictions
   - abandoned branches
   - related concepts
4. Synthesize only what the evidence supports.
5. Offer to save a lineage page only after the read-only answer is complete.

## Output

Use this shape unless the user asked for a different format:

```markdown
## Current Live Version
[1-3 sentences with confidence.]

## Lineage
- First mention: [date] - [claim] ([source])
- Best articulation: [date] - [claim] ([source])
- Turning point: [date] - [what changed] ([source])

## Reversals and Contradictions
- [evidence-backed changes or "No clear evidence found"]

## Abandoned Branches
- [branch and why it appears abandoned]

## Evidence Gaps
- [what was checked and what is missing]
```

## Guardrails

- Keep the scope to one idea. Use `concept-synthesis` for broad concept maps.
- Do not invent a smooth story from sparse evidence.
- Do not mutate brain pages without explicit user instruction.
- Treat the user's own direct statements as the highest authority for their current view.
