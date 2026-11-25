---
name: drools-analyze-rule
description: Analyze Drools DRL rule semantics, conditions, consequences, attributes, bindings, constraints, and interactions. Use when reviewing a rule, explaining why it matched or did not match, or identifying correctness risks in declarative business logic.
---

# Analyze Rule

1. Read the relevant DRL, domain facts, service instructions, and tests.
2. Identify rule conditions, bindings, consequences, attributes, and referenced facts.
3. Evaluate constraint semantics and interactions with other rules.
4. Check salience, no-loop, lock-on-active, agenda/activation groups, and enabled/date constraints when present.
5. Separate business-rule intent from observed implementation.
6. Do not change business semantics without explicit requirements.

## Output
- Rule Intent
- Match Conditions
- Consequences
- Interaction Risks
- Evidence and Recommended Change
