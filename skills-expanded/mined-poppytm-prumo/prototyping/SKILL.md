# Prototyping

## 1. Purpose
To map, sketch, decide, and prototype interactive concepts to validate assumptions using progressive fidelity levels, ultimately culminating in engineering handoff.

## 2. Use When
- Designing new features with high uncertainty.
- Conducting a 5-day Design Sprint.
- Incrementally increasing fidelity from sketch to interactive UI.

## 3. Do Not Use When
- The feature is fully defined and validated.
- Building purely backend architecture.

## 4. Required Context
- The user problem to be solved.
- Current fidelity level (e.g., lo-fi, mid-fi, hi-fi).

## 5. Procedure
1. **Sketch**: Generate low-fidelity concepts (paper/whiteboard).
2. **Wireframe (Lo-fi)**: Establish flow, structure, and gray box layouts.
3. **Mid-fi**: Integrate real content and basic interactions.
4. **Hi-fi**: Apply design tokens, refined typography, and final visual details.
5. **Interactive**: Wire states and transitions for user testing.
6. **Handoff**: Document component mapping, interaction specs, and constraints.

## 6. Decision Rules
- Do not increase fidelity until the lower fidelity's assumptions are validated.
- Real content must be used in mid-fi; avoid lorem ipsum to test layout realities.

## 7. Evidence Required
- A prototype asset corresponding to the targeted fidelity level.
- Annotated handoff documentation for engineering.

## 8. Output Contract
- Specifications, user flows, and structured prototyping documents.

## 9. Stop Conditions
- The prototype successfully answers the core validation questions of the current stage.

## 10. Escalation Rules
- Escalate if user testing fundamentally invalidates the problem statement, requiring a pivot.
