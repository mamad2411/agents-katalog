---
name: orchestrate-intent
description: Route intent to verified A2A capabilities using options-first operating-mode interrogation, recommended path selection, and owner-controlled reusable workflows.
---

# Orchestrate Intent

## When to use

Use for work that may execute on Machine A or Machine B.

## Procedure

1. State the goal, observable acceptance criteria, constraints, intent/workflow class, required outcomes, and authority.
2. Check for an applicable owner-selected workflow preference and newest owner-adjustment revision. Treat preference as guidance, never authority.
3. If this is first setup/first materially new workflow and no explicit operating mode applies, present the short options prompt: **A Approve once then autonomous (recommended), B Ask every execution, C Observe/recommend only, D Custom**. Record the owner's selection; do not infer it from silence.
4. Call `a2a_list`; discover configured peers when their card is not current.
5. Coarse-filter Agent Cards only. Do not treat a card as detailed proof.
6. Call plausible peers with the versioned `ADVERTISEMENT_INDEX` request from `contracts/advertisement-protocol.md`.
7. Validate peer identity, schema version, revision, digest, status, and index.
8. Request only relevant capability documents and apply `routing/AGENTS.md` gates.
9. Build only materially different paths backed by eligible verified capabilities. On first use, show a compact option set with exactly one evidence-based recommended path plus Custom when useful; persist the owner's actual selection even if it differs from the recommendation.
10. Determine authorization from the selected operating mode: A may use a confirmed active bounded grant after verified first use; B requires fresh approval every modifying run; C remains observe/recommend-only unless a fresh explicit approval authorizes the modification; D must resolve to deterministic local custom policy.
11. Send the selected peer the versioned task request from `contracts/task-contract.md`, including operating mode, owner-adjustment revision, selection, and authorization reference.
12. For multi-machine work, create a small DAG and transfer only necessary artifacts through A2A.
13. On timeout, inspect task/history before retrying with the same idempotency key.
14. Check every acceptance result, operating mode, adjustment revision, and authorization-used field; disclose partial, blocked, approval-required, refused, or failed outcomes exactly.
15. Keep only minimal routing/preference metadata and opaque local-grant references. Never request or retain raw local experience.

## Recommendation priority

Eligibility first. Then honor applicable explicit owner preference. For a new path recommendation, consider verified outcome fit, required authority, privacy boundary, reliability/evidence freshness, reversibility/recovery, current availability, local proximity to inputs, and transfer/resource cost. Recommendation never overrides owner selection.

## Stop / re-interrogate conditions

Stop and ask only the affected decision when the owner asks to change/adjust the workflow, no valid operating-mode selection exists, first-use path selection is required, no in-scope authority exists, or authority/irreversible effects/recipient/cost/credential scope/filesystem/network scope/target/environment/capability/peer identity materially changed or is unclear. Do not repeat unrelated setup questions.
