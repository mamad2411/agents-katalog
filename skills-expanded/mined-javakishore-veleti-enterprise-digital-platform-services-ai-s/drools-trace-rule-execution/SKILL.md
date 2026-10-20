---
name: drools-trace-rule-execution
description: Trace Drools rule execution from inserted facts through matches, agenda activations, firing order, fact mutations, and final outcomes. Use when determining which rules fired, why they fired, or how a decision was produced.
---

# Trace Rule Execution

1. Resolve the ruleset, session type, input facts, and execution entry point.
2. Follow insert/update/modify/delete operations and derived facts.
3. Trace matching rules, agenda activation, firing order, and consequences.
4. Track fact changes that cause additional activations.
5. Identify the first rule or fact transition that explains an unexpected outcome.
6. Distinguish observed execution evidence from inferred behavior.

## Output
- Input Facts
- Activation/Firing Sequence
- Fact State Changes
- Decision Path
- First Unexpected Transition
