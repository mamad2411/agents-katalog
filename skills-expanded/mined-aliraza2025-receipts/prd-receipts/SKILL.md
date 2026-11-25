---
name: prd-receipts
description: Turns interview notes, call transcripts, support tickets, or stakeholder requests into a PRD that keeps observations, inferences, and assumptions separate, with quotes as receipts, explicit non-goals, and success metrics. Use when the user asks for a PRD, product requirements, a feature spec, or to synthesize user or stakeholder interviews into requirements.
---

# PRD receipts

A good PRD lets an engineer see which requirements came from what people actually said or did, and which came from someone's guess. This skill keeps those apart.

## Workflow

1. **Sort the raw input** into three buckets before writing anything:
   - **Observed:** what someone said (quote it) or did (describe it), with who and when.
   - **Inferred:** a pattern across several observations. List the observations it rests on.
   - **Assumed:** anything else, including the requester's proposed solution.
2. **Write the problem** using only observed and inferred items. If the problem rests mostly on assumptions, say so at the top and recommend discovery before build.
3. **Separate requests from needs.** A stakeholder asking for a feature is an observation about the request, not proof of the need behind it. Record both.
4. **Scope tightly.** Write non-goals as carefully as goals.
5. **Attach metrics** in the `metric-receipts` style: definition, decision it informs, and what it does not prove.
6. **List open questions** with the person who can answer each one.
7. **Strip private data.** Replace customer names, addresses, and contact details with roles ("office manager", "field tech").

## PRD template

```markdown
# [Feature name]

**Status:** draft | **Owner:** ... | **Evidence strength:** strong | mixed | mostly assumed

## Problem
[2 to 4 sentences, observed and inferred only]

## Evidence
| Type | Receipt | Source (role, date) |
|---|---|---|
| Observed | "quote" | office manager, interview 1 |
| Inferred | pattern | from observations 1, 3, 4 |
| Assumed | belief | requester |

## Users and jobs
## Requirements
| ID | Requirement | Why (evidence row) | Priority |
## Non-goals
## Success metrics
## Risks and open questions
| Question | Who can answer | By when |
```

## Example (evidence rows, illustrative)

A fictional window-cleaning business building a quoting tool:

| Type | Receipt | Source |
|---|---|---|
| Observed | "I need a price while the customer is still on the phone." | office staff, requirements session |
| Observed | Quotes were built by hand from past jobs in the field-service system. | workflow walkthrough |
| Inferred | Speed of quoting matters more than precision to the cent. | sessions with owner and staff |
| Assumed | Customers will accept an estimate range instead of a fixed price. | not yet tested |

The assumed row becomes an open question, not a requirement.

## Rules

- Never put an assumption in the Problem section.
- Every requirement points to at least one evidence row, or is marked `ASSUMPTION`.
- Quotes are verbatim; paraphrases are labeled as paraphrases.
