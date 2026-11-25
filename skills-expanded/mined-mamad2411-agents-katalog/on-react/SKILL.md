---
name: on-react
description: Use when implementing, reviewing, or refactoring React frontend work for Onflou projects; loads the Onflou React Guide and Policy from the knowledge vault before changing UI, state, API integration, routing, styling, or frontend tests.
---

# Purpose

Reusable workflow for Onflou React frontend implementation and review.

# Required Knowledge

Read these knowledge resources before generating architecture, implementation, review comments, reports, or automation for Onflou React work:

- [React standard overview](../../../70-knowledge/company/onflou/internal/REACT_FRONT_STANDARD_v1.0/REACT%20FRONT%20STANDARD%20%28v1.0%29.md)
- [React Guide](../../../70-knowledge/company/onflou/internal/REACT_FRONT_STANDARD_v1.0/REACT%20FRONT%20STANDARD%20%28v1.0%29/Guide.md)
- [React Policy](../../../70-knowledge/company/onflou/internal/REACT_FRONT_STANDARD_v1.0/REACT%20FRONT%20STANDARD%20%28v1.0%29/Policy.md)
- [Reference assets](../../../70-knowledge/company/onflou/internal/reference-assets/README.md)
- [React component reference assets](../../../70-knowledge/company/onflou/internal/reference-assets/react-components/README.md) when working on reusable component, page, hook, or UI pattern implementation.

# Inputs

- target feature, component, page, hook, or module
- relevant user flow or UI behavior
- related API contract or data model
- auth, permission, or routing requirements
- test or verification expectation

# Workflow

1. Load the required Onflou React knowledge files.
2. Treat `Policy.md` as mandatory rules and `Guide.md` as recommended conventions.
3. If the task matches a stored component or UI pattern, inspect the matching reference asset before designing the change.
4. Identify affected frontend surface: UI, state, API integration, routing, styling, tests, or build behavior.
5. Validate naming, structure, data flow, and error/loading states against Onflou conventions.
6. Implement or review the smallest sufficient change.
7. Verify behavior with the project's existing frontend checks.
8. Record unresolved risks, missing knowledge, or convention conflicts in shared state when necessary.

# Output

- frontend implementation, review, plan, or report
- verification summary
- related task, artifact, or log references

# Safety Rules

- Never ignore `Policy.md`.
- Treat reference assets as examples, not mandatory standards.
- Do not invent frontend conventions when Onflou knowledge already defines one.
- Preserve existing component boundaries and naming consistency.
- Do not introduce broad state management, routing, styling, or build changes unless required.
- Surface missing business rules, API ambiguity, and UI edge cases before guessing.

# Incident References

Related incidents:

- Check `ai-workspace/70-knowledge/incidents/` and Onflou domain knowledge before work that may affect retries, duplicated execution, reconnects, or partial failures.

# Verification

- Confirm required Onflou React knowledge was read or explicitly unavailable.
- Confirm implementation or review aligns with React `Policy.md`.
- Confirm relevant UI states and edge cases were considered.
- Confirm tests, build checks, or manual verification steps are documented.
