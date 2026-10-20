---
name: new-feature
description: Plan and implement a new feature end-to-end using the orchestrator workflow
agent: orchestrator
model: Claude Sonnet 4.5
tools:
  - codebase
  - search
  - changes
  - problems
  - fetch
---

# New Feature Request

## Feature: ${input:featureName:Describe the feature}

Analyze this feature request and coordinate the full development lifecycle:

1. **Analyze** the current codebase to understand where this feature fits
2. **Identify** all files that need to be created or modified (backend + frontend)
3. **Assess** security implications and data model changes
4. **Create a phased plan** with clear steps for implementation, testing, and documentation
5. **Recommend** which specialist agent should handle each phase

Consider:
- Does this require new database tables or migrations?
- Does this require new API endpoints?
- Does this require new frontend components, pages, or stores?
- Are there security considerations (auth, input validation, data exposure)?
- What tests are needed (unit, integration, e2e)?

After analysis, use the handoff buttons to route to the appropriate specialist.
