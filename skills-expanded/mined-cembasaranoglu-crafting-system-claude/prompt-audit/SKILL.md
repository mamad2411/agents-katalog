---
name: prompt-audit
description: Audits agent prompts for clarity, source-first behavior, risk boundaries, tool policy, output schemas, examples, validation honesty, and tuning readiness. Use when reviewing or improving a prompt.
---
# Prompt Audit

Audit the provided prompt or prompt target: `$ARGUMENTS`

## Instructions

1. Identify the prompt's intended surface: Claude chat, Claude API, Claude Code, skill, plugin, subagent, or MCP workflow.
2. Separate facts, assumptions, recommendations, unknowns, and blockers.
3. Check for:
 - clear objective
 - role and responsibility boundaries
 - source-first behavior
 - risk gate and ask-vs-act boundary
 - tool-use trigger rules
 - context layout
 - XML or schema structure
 - examples and edge cases
 - output contract
 - validation/evaluation plan
 - contradictory instructions
 - over-prompting or under-specification
4. Do not rewrite the whole prompt unless the user asks. First produce findings.

## Output

```yaml
prompt_audit:
 overall_grade: "excellent | good | needs_work | unsafe | blocked"
 target_surface: ""
 critical_findings: []
 high_findings: []
 medium_findings: []
 low_findings: []
 contradictions: []
 missing_sections: []
 tuning_recommendations: []
 minimum_next_fix: ""
```

