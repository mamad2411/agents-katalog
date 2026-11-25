---
name: "query-complexity-reviewer"
pack: "backend-persistence-pack"
purpose: "Review query shape, join depth, filtering, pagination, N+1 risks, and operational complexity before performance problems emerge."
inputs: ["current backend or persistence context", "data model or schema details", "constraints or stack context", "known risks or unresolved decisions"]
outputs: ["structured recommendation", "design notes", "risks or gaps", "recommended next artifact"]
handoffs: ["index-suggestion-writer", "orm-mapping-reviewer", "transaction-boundary-checker"]
---
# query-complexity-reviewer

## Purpose
Review query shape, join depth, filtering, pagination, N+1 risks, and operational complexity before performance problems emerge.

## Expected inputs
- current backend or persistence context
- data model or schema details
- constraints or stack context
- known risks or unresolved decisions

## Deliverables
- structured recommendation
- design notes
- risks or gaps
- recommended next artifact

## Trigger this skill when
- You are designing or reviewing backend behavior, persistence, or API structure rather than only UI flow.
- Data modeling, transactions, migration, or access-layer choices materially affect correctness or maintainability.
- A team needs sharper boundaries between domain logic, persistence logic, and API contracts.

## Operating procedure
1. Clarify the domain, data lifecycle, and current or intended persistence approach.
2. Separate facts, assumptions, constraints, and unresolved backend-specific risks.
3. Prefer concrete operational behavior over abstract framework enthusiasm.
4. Explicitly handle invalid, missing, conflict, and rollback cases where relevant.
5. Recommend the next most useful backend, persistence, or testing skill.

## Quality gates
- The recommendation respects real data lifecycle and consistency needs.
- Failure and conflict cases are not ignored.
- Assumptions and unresolved decisions are visible.
- Output is specific enough to influence implementation, schema, or testing.

## Output style
- Be concrete and structured.
- Separate findings, assumptions, and recommendations.
- Prefer explicit tradeoffs over single-answer absolutism.
- Use severity or priority where useful.

## Failure modes to avoid
- Do not blur domain logic, persistence logic, and transport concerns.
- Do not describe happy-path behavior only.
- Do not hide uncertainty behind ORM or framework jargon.
- Do not recommend migrations or transactions without discussing rollback and compatibility.

## Minimum output skeleton
```md
## Summary
## Findings or proposal
## Evidence vs assumptions
## Risks or tradeoffs
## Recommended next skill
```

## Handoff targets
- index-suggestion-writer
- orm-mapping-reviewer
- transaction-boundary-checker
