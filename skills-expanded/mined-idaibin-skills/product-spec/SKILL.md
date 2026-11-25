---
name: product-spec
description: "Define product behavior and acceptance, or reconstruct source-grounded product evidence as an explicitly unaccepted candidate."
---

# Product Specification

## Entry Gate

Own current product facts and acceptance, not implementation architecture or visual
semantics. Require a named product authority or authorized artifact target; resolve
only decisions needed for the requested slice.

## Route Map

| Request condition | Read | Result |
| --- | --- | --- |
| Explicitly reconstruct current product evidence from an existing implementation | [source reconstruction](references/source-reconstruction.md) | Observed candidate and owner decisions; never automatic Ready |
| One feature needs behavior, states, and acceptance | [workflow](references/workflow.md) and [template](references/template.md) | Progressive Feature Spec |
| Submission failure or uncertain completion affects recovery | [workflow](references/workflow.md#ready-for-an-implementation-slice) | Accepted input, outcome and safe-retry rules, or a scoped Open decision |
| New product line/boundary reset is explicit | [workflow](references/workflow.md) | Foundation Spec |
| Confirmed changes update a named fact source | [documentation boundaries](references/documentation-boundaries.md) | Bounded artifact update |
| A material product decision needs challenge | [decision pressure test](references/decision-pressure-test.md) | Decision disposition |
| Prototype evidence is decisive | [prototype evidence](references/prototype-evidence.md) | Qualified product facts |

## Invariants

- Do not promote UI appearance, source, or tests into product authority. The reconstruction profile may label observations and inferences separately; accepted product decisions still require the product owner.
- Keep product behavior separate from shared visual semantics, technical design, implementation, and runtime proof.
- Stop each slice at its Ready gate; unknowns remain named, not silently decided.
  Missing outcome/retry criteria are Open Product decisions, not implementation
  details. Do not infer success or safe retry from an unqualified lookup result;
  return confirmed behavior separately from the unresolved recovery slice.

## Output Map

Return the one applicable current product artifact, source basis, decisions/states,
acceptance, current scope, unresolved questions, and next owner. Keep removed scope
and conversation history out of the terminal artifact. Reconstruction returns the separately labelled observed candidate, fixed evidence refs, contradictions/unknowns and next owner; it is not an accepted Product contract.

## Reference Map

- Read [workflow](references/workflow.md) for Feature/Foundation/update procedure and gates.
- Read [template](references/template.md) when creating an artifact.
- Read [documentation boundaries](references/documentation-boundaries.md) for authority and placement.
- Read [prototype evidence](references/prototype-evidence.md) only when prototype evidence applies.
- Read [decision pressure test](references/decision-pressure-test.md) only for a material decision challenge.
- Read [source reconstruction](references/source-reconstruction.md) only for an explicitly requested existing-product evidence rebuild.
- Read [usage](references/usage.md) for public modes and nearest owners.
- Maintainers only: read [eval cases](references/eval-cases.md); do not load it during ordinary runtime.
