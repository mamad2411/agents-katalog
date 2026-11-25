---
name: drools-analyze-rule-tests
description: Analyze Drools rule tests for scenario coverage, expected facts/outcomes, boundary conditions, conflicting rules, regression protection, and deterministic execution. Use when reviewing or improving automated tests for DRL, decision tables, Rule Units, or CEP rules.
---

# Analyze Rule Tests

1. Map business scenarios to rules and expected outcomes.
2. Inspect positive, negative, boundary, overlap, and conflict cases.
3. Verify tests assert outcomes and relevant fact changes, not only that rules fired.
4. Include regression scenarios for previously observed failures.
5. Keep tests deterministic and explicit about session/time behavior.
6. Identify untested rule interactions.

## Output
- Scenario Coverage
- Missing Cases
- Interaction/Boundary Risks
- Test Quality Findings
- Recommended Tests
