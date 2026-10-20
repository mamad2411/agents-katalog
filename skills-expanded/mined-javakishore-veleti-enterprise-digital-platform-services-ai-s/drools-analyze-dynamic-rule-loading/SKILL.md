---
name: drools-analyze-dynamic-rule-loading
description: Analyze Drools dynamic rule loading, runtime refresh, KieScanner or equivalent update mechanisms, version transitions, consistency across service instances, and rollback behavior. Use when rules change without full application redeployment or instances run different rule versions.
---

# Analyze Dynamic Rule Loading

1. Identify the rule source, update mechanism, polling/refresh behavior, and artifact version strategy.
2. Determine how each application instance discovers and activates a new ruleset.
3. Check consistency across pods/JVMs during transitions.
4. Inspect failure and rollback behavior for invalid or partially deployed rules.
5. Correlate runtime decisions with the exact ruleset version.
6. Never trigger production rule refresh unless explicitly authorized.

## Output
- Update Mechanism
- Version Transition
- Instance Consistency
- Failure/Rollback Findings
- Recommended Action
