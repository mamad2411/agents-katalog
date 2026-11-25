---
name: cgx-minimum-sufficient-work
description: Decide whether a Cognigrex request should reuse existing results, reconcile compatible prior evidence, execute only missing discriminating work, or run a bounded new test/simulation.
---

# CGX Minimum Sufficient Work

Apply this before tests, simulations, sweeps, searches over large corpora, CAD jobs, long local-LLM runs, or broad GPT analysis.

## Decision order

1. **Exact reusable result**
   - Does a current, valid receipt/result already cover the requested subject, variables, constraints, method, and proof standard?
   - If a target node/root already has an exact verified content hash and size, reuse that payload; do not retransmit bytes.
   - If a compatible compute receipt already binds the same capability, input-manifest hash, assumptions and proof standard, reuse it; do not recompute.
   - If yes: retrieve it. Do not rerun.

2. **Reconciliation**
   - Do two or more compatible prior results bracket or otherwise determine the requested state?
   - Is mathematical reconciliation/interpolation valid under the governing model and uncertainty bounds?
   - If yes: compute the smallest proof needed to align them and issue a reconciliation receipt. Do not launch a mass sweep.

3. **Missing discriminant only**
   - Identify the smallest unresolved variable, boundary, coefficient, geometry, condition, or evidence item that prevents a valid answer.
   - Execute only that missing discriminating work.

4. **Bounded new execution**
   - Run a new test/simulation/sweep only when existing evidence cannot answer the request and the missing state cannot be validly derived.
   - Constrain ranges, samples, fidelity and tools to the decision need.

5. **Block**
   - Stop if current Recovery/hydration/authority is invalid, required inputs are missing, or execution would exceed the resolved lease.

## Compatibility checks before reconciliation

Require compatible:
- object identity/version or an explicit transformation,
- units and coordinate/reference frames,
- governing equations/assumptions,
- boundary and initial conditions,
- measurement/test method,
- uncertainty treatment,
- evidence provenance.

Never interpolate across discontinuities, phase changes, topology changes, invalid domains, or materially different methods merely to avoid execution.

## Resource arbitration

Prefer:
- deterministic lookup over reasoning,
- formula/proof over sweep when valid,
- local Python over GPT arithmetic for repeated numerical work,
- existing test runner over re-implementing a test in chat,
- local simulation/CAD for heavy deterministic work,
- local LLM for first-pass classification/decomposition when configured,
- GPT for ambiguity resolution, cross-domain synthesis, critique, and user-facing explanation.

## Required output

Record:
- chosen strategy,
- reused receipt/result IDs,
- compatibility checks,
- any derived calculation/proof,
- unresolved discriminant,
- bounded execution requested (if any),
- why broader work was not required.
