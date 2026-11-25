---
description: "Generate a new feature specification following the SDD template"
mode: "agent"
---

# Create Spec

Generate a new feature specification following the Spec-Driven Development template.

Feature name: {{input}}

## Instructions

1. **Gather requirements** from the user:
   - Ask clarifying questions about the feature
   - Understand the problem being solved
   - Identify constraints and dependencies

2. **Read existing specs** for context:
   - `specs/01_product_manager.md` — Product vision
   - `specs/02_backend_lead.md` — Backend patterns
   - `specs/03_frontend_lead.md` — Frontend patterns
   - `specs/04_db_architect.md` — Database conventions

3. **Determine spec number**: Check existing specs in `specs/` folder, use next available number (feature specs start at 10+)

4. **Generate spec document** with these sections:

   - **Vision**: Problem Statement, Success State, Who Benefits
   - **Requirements**: Functional (Must/Should/Nice to Have) + Non-Functional
   - **Database Schema** (if applicable): Tables, indexes, constraints
   - **API Endpoints** (if applicable): Method, path, description, auth, request/response examples
   - **Frontend Components** (if applicable): Components, state changes, routes
   - **Integration Points**: With existing systems
   - **Security Considerations**: Auth, validation, rate limiting
   - **Success Metrics**: What to measure
   - **Out of Scope**: What this spec does NOT include
   - **Open Questions**: To resolve before implementation

5. **Save the spec**: Write to `specs/XX_feature_name.md`

6. **Generate initial tickets**: Break the spec into 2-4 hour tickets, present as a draft sprint

## Output Format

```
## Created Spec: XX_feature_name.md

### Summary
[One-line description]

### Sections Completed
[List of sections]

### Suggested Sprint Tickets
| # | Ticket | Owner | Model |
|---|--------|-------|-------|

**Estimated: X tickets, ~Y hours**

Would you like me to add these as a new sprint in the backlog?
```

## Important Rules

- Always ask clarifying questions before writing
- Follow existing naming conventions in the project
- Include concrete examples, not placeholders
- Reference existing patterns from other specs
- Break down into implementable, testable pieces
- Mark spec as "Draft" until validated
