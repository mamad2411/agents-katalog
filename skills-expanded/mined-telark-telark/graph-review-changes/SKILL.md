---
name: graph-review-changes
description: Use for a risk-ranked review of a diff or branch (what changed, what it affects, whether it is tested) when the code-review-graph MCP server is connected and list_graph_stats shows this repository indexed. Without an indexed graph, review from the diff and normal search instead.
---

# Review changes with the graph

Goal: a review that ranks the changes by risk, shows what each one affects, says whether it is tested, and ends with a merge recommendation.

Confirm with `list_graph_stats` that the graph covers this repository and is current; otherwise review from `git diff` and ordinary search. `detail_level="minimal"` keeps answers compact where a tool accepts it.

| Need | Tools |
|---|---|
| Risk-scored summary of the diff | `detect_changes` (for a branch, set `base` to `git merge-base main HEAD`) |
| Source snippets to review | `get_review_context` |
| Impacted execution paths | `get_affected_flows` |
| Tests covering a changed function | `query_graph` with `tests_for` |
| Blast radius | `get_impact_radius` |

Tests in this repository live apart from the code (`services/<svc>/internal/tests/<area>/`, `services/analyzer/tests/`); when `tests_for` finds nothing, look there before calling a change untested. For untested changes, suggest specific test cases.

Also check the diff against `AGENTS.md`: version fields untouched, docs updated in the same change, tests in the right place, constants instead of literals.

## Output

Findings grouped by risk (high, medium, low), each with:

- what changed and why it matters
- test coverage status
- suggested improvements

End with an overall merge recommendation.
