---
name: prototype-question
description: Define the decision, evidence target, scope, fidelity, and stopping rule for a product prototype. Use before building when the prototype risks becoming a polished demo without a testable question. Do not use when the user has already supplied an equally precise prototype brief.
---

# Prototype Question

Design the smallest artifact that can make one important unknown observable.

## Frame the probe

1. Name the decision the prototype should inform and the highest-risk assumption behind it.
2. Choose one primary question. Move secondary questions to a later list.
3. Identify who must experience or inspect the prototype and in what context.
4. Select the minimum fidelity required for credible evidence:
   - representation for structure or comprehension;
   - clickable flow for navigation or interaction;
   - coded behavior for state, timing, AI behavior, feasibility, or instrumentation;
   - concierge or Wizard-of-Oz behavior when the system can be simulated honestly.
5. Specify which states and branches must be real, which may be simulated, and what must be disclosed.
6. Define evidence collection and support / reject / reframe criteria.
7. Set a stopping rule for both building and testing.

## Output

```markdown
## Decision this prototype informs
## Primary unknown
## Audience and context
## Minimum prototype
- Fidelity:
- Must be real:
- May be simulated:
- Out of scope:
## Evidence plan
## Support / reject / reframe criteria
## Stop rule
## Result handoff
```

## Boundaries

- Do not prototype the entire product to answer a local question.
- Do not confuse stakeholder approval, visual polish, or successful generation with user evidence.
- Never conceal simulated AI, data, payments, permissions, or destructive actions from test participants.
- If no plausible observation could change the decision, recommend a different evidence method.
