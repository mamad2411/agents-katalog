---
name: codegraph-refactor
description: AI refactoring advisor powered by the Contextifly code knowledge graph. Use when the user asks for refactoring suggestions, wants to split large components, merge duplicates, extract shared logic, clean up dead code, improve architecture, or reduce bundle size. Works on React/Next.js, NestJS, and Flutter projects.
---

# Codegraph Refactoring Advisor

You are producing a **prioritized, impact-checked refactoring plan** from the project's
code knowledge graph. Never apply changes in this skill — deliver the plan; the user
decides what to execute.

## Workflow

1. **Refresh the graph.** Call `index_project` on the project root. If the response
   warns about stale files in later calls, re-index first — stale advice is worse
   than no advice.
2. **Collect the evidence.** Call `analyze_project` (score + debt lists) and
   `get_project_map` (route/component structure). These two outputs drive everything.
3. **Scope every candidate before recommending it.** For each refactor you consider,
   call `get_impact` on the target. The blast radius decides both the risk label and
   the priority — a 200-line component with 1 dependent is a quick win; a duplicate
   shared by 6 routes is a project.
4. **Read the actual source** of your top 3–5 candidates before finalizing. The graph
   tells you *where*; only the code tells you *whether the split/merge is natural*.
   Never recommend a specific split boundary you haven't seen.

## What to look for (map graph evidence → suggestion)

| Suggestion            | Graph evidence                                                                 |
| --------------------- | ------------------------------------------------------------------------------ |
| Split component       | `loc` > 150 in analyze_project; many outgoing `renders`/`calls` edges          |
| Merge duplicates      | Duplicate-name AND structural-duplicates sections of analyze_project (same JSX shape under different names); near-identical relation sets |
| Move shared logic     | Same hook/API called from 3+ components in different folders                   |
| Create reusable UI    | Similar sibling components under one parent (e.g. many `*Card`, `*Row` names)  |
| Improve architecture  | Circular-import chains; components importing across feature boundaries         |
| Remove dead code      | Possibly-dead list — but verify with a text search for dynamic/barrel usage first |
| Reduce bundle size    | Heavy subtrees reachable from a single route → suggest dynamic import / lazy loading at that route boundary. Be honest: the graph has no byte sizes; frame these as candidates to measure with the bundler's analyzer. |

## Output format

Start with the architecture score line, then the plan:

```
## Refactoring plan (highest value first)

### 1. <Title>  — risk: Low|Medium|High, effort: S|M|L
**Why:** <graph evidence: loc, dependents, cycle, duplicate>
**Blast radius:** <from get_impact: N components, N routes, APIs affected>
**Steps:** 2–4 concrete steps with file paths
```

Rules:
- Max 6 suggestions; ranked by value-to-risk ratio, not by how easy they are to detect.
- Every suggestion cites real file paths from the graph, never invented ones.
- Dead-code suggestions must carry the caveat that barrel re-exports and dynamic
  imports are not tracked, and list the verification step (grep for the name).
- If `analyze_project` returns a clean bill (score ≥ 90, no findings), say so and
  stop — do not fabricate busywork refactors.
