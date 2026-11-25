---
name: free-design-intake
description: >-
  Converts a human photonic-device objective and constraints into a validated,
  solver-independent SimulationContract. Use for free-design mode before
  selecting Meep, Lumerical, or another solver adapter.
disable-model-invocation: true
---

# Free-design requirement intake

Produce `simulation-contract.json` conforming to:

```text
../../schemas/v1/contracts.schema.json#/$defs/SimulationContract
```

## Workflow

1. Establish device objective, observables, geometry, materials, fabrication
   constraints, method-appropriate excitation or eigenproblem, boundaries or
   periodicity, outputs, accuracy, and resources.
2. Ask only for omissions that materially change physics, cost, or
   interpretation.
3. Query the Example Library using device, material, band, observable,
   dimensionality, mode, and minimum quality.
4. Record every reused example ID/version, quality, reusable field, and
   transformation in `example_references`.
5. Mark example-derived values as suggestions; they never override an explicit
   user constraint.
6. Include method-appropriate convergence or sensitivity cases.
7. Keep all assumptions visible with reason, consequence, and acceptance.
8. Validate the completed contract. Correct the document rather than weakening
   the schema.

Select the numerical method before the solver. Route periodic 2D PWE, slab GME
bands/radiative Q/symmetry, and supported Hopfield polaritons to
`legume-gme-workflow` when its scalar nondispersive approximation is adequate.
Route driven broadband scattering, transient fields, and general lossy or
dispersive structures to a full-wave solver instead. Never add fake
source/monitor/PML fields to an eigenproblem contract.

## Gate

Do not select a solver or generate a model until:

- requested observables also appear in raw or derived outputs;
- material models and valid spectral ranges are identified;
- interpretation-changing assumptions are accepted;
- G1 contract review is recorded.
