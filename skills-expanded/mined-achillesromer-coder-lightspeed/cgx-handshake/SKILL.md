---
name: cgx-handshake
description: Resolve a Cognigrex/LightSpeed selector request into the current CGX context, authority, capabilities, minimum sufficient work plan, execution route, and receipt path without creating a parallel runtime or duplicating prior work.
---

# CGX Handshake

Use this skill whenever an Achilles, Neo, Athene, Raphael, Cognigrex, Römer-Grex, Eco-Grex, EMASSC, or LightSpeed selector is explicitly invoked, or when a Cognigrex-aware execution request must cross .cgx, LS, LS GO, Drive, Git, local models, tests, simulations, or CAD.

## Invariants

- Treat the selector as a routing default, not a new agent instance or truth store.
- Resolve the current accepted Recovery state and verifier result from live CGX state. Never hard-code an old recovery state.
- Preserve existing authority. Neo may coordinate bounded execution; Achilles remains the canonical/release gate where the current contracts say so.
- Treat LS/runtime receipts as evidence inputs, not automatic semantic truth.
- Do not create a second application, backend, filespace, ontology, or co-running Cognigrex.
- Prefer the existing LightSpeed supervisor, floor runner, LS GO bridge, project pipeline, receipt browser, Drive connector, Git connector, and local tool adapters.

## Workflow

1. Resolve selector:
   - actor requested?
   - domain requested?
   - system requested?
   - project/object/artifact requested?
2. Resolve current accepted Recovery authority, hash, topology, DBR root, and verifier state.
3. Hydrate only the required context. Stop and surface the exact gate if current verification fails.
4. Decompose user intent into:
   - operation,
   - subject/object,
   - hard constraints,
   - requested output,
   - proof/assurance requirement.
5. Resolve applicable domain/module/object and authority. When a named current object/twin is present, use the shared `cgx.object_context` / `cgx_resolve_object` path so child-domain identity, Operations binding, source owner and representation boundary come from the same current lineage.
6. Resolve live capabilities and skills.
7. Run the minimum-sufficient-work decision before dispatch.
8. Route to the smallest execution surface that can produce a valid answer or receipt.
9. If data and execution resolve to different surfaces/nodes, apply the node-exchange handshake:
   - resolve source/target node identity and registered capability independently,
   - transfer only missing inputs by content hash,
   - require exact receiver hash/size readback before dependent compute,
   - never treat a storage carrier as proof of an independent compute node,
   - never transfer semantic/governance/release authority with the bytes,
   - require a current scoped COMPUTE_ONLY/DIGITAL_WRITE-or-stronger lease as applicable.
10. Execute only through a registered capability in the existing runtime and within the resolved lease/gates. Arbitrary shell text is not a node capability.
11. Return compact transfer/compute receipts and evidence refs. Keep raw logs, raw payloads and long local-model traces local unless requested.
12. Send promotion-capable results through required review/LS GO gates.

## Query normalisation rule

Translate user language into the operation the system can actually perform. Example pattern:

- "Find a plant-based dairy-free snack" -> subject=snack, constraints=[plant-based,dairy-free], then search/filter.
- "Run/check this test" -> identify the intended test, resolve whether a valid result already exists, then retrieve/reconcile/execute only what is missing.
- "Compare these sweeps" -> inspect compatibility and mathematical overlap before scheduling a new sweep.

Do not substitute keyword search for the requested operation when a deterministic tool, test, formula, filter, simulator, or existing receipt can answer it more directly.

## Minimum-sufficient-work gate

Use the sibling skill `cgx-minimum-sufficient-work` before any expensive or repetitive execution.

## Output

Return or construct a `CGXContextEnvelope` and a compact receipt-oriented result with:
- resolved selector/domain/agent,
- current recovery state,
- selected strategy,
- capabilities/skills used,
- evidence/result refs,
- blockers/defeaters,
- next gate.
