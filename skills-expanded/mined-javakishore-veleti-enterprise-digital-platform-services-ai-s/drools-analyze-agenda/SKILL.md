---
name: drools-analyze-agenda
description: Analyze Drools agenda behavior including salience, agenda groups, activation groups, ruleflow groups, no-loop, lock-on-active, focus, and firing order. Use for ordering problems, competing rules, loops, or unexpected activation behavior.
---

# Analyze Agenda

1. Identify all rules participating in the affected decision.
2. Inspect salience, agenda groups, activation groups, ruleflow groups, no-loop, and lock-on-active.
3. Trace focus and activation order when runtime evidence is available.
4. Identify hidden ordering dependencies or mutually exclusive activations.
5. Prefer explicit business sequencing over accidental ordering.
6. Do not use salience as a blanket fix for unclear rule design.

## Output
- Agenda Structure
- Activation Ordering
- Conflicts/Loops
- Ordering Dependencies
- Recommended Design
