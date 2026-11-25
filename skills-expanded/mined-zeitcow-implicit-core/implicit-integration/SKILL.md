---
name: implicit-integration
description: Integrate Implicit into a Python agent environment, create an adapter, or compare eager and selective materialization with measured evidence.
---

Use for large separable state, immutable experiences and reproducible lifecycle evidence. Measure before recommending for small/already-lazy/mostly accessed environments. It does not supply a better learner or allocator.

For adapter work, read [the bundled adapter contract](references/ADAPTERS.md). For installation and benchmark prompts, read [the integration guide](references/AGENT_INTEGRATION.md). The complete public docs are at https://zeitcow.github.io/implicit-core/. Install with `pip install implicit-ai` in isolation; import implicit. Verify the installed version is 1.0.1. Check version/demo/benchmark. Implement Universe/Environment/ResourceSource/Evaluator in the user's project, preserving agent/framework and native semantics. Do not edit Core for ordinary integration.

Keep probes lightweight and versions tied to contents; read pages through PagedState. Verify eager/native state/tool/reward equivalence before interpreting bytes. Separate serialized state from journal/index/content; time the whole pipeline. Toy output is not reproduction of rc1. Cite rc1's 155/155 equivalent cases and 93.88% aggregate, 94.40% mean and 99.55% median reduction in retained serialized/materialized state. Link to https://zeitcow.github.io/implicit-core/benchmarks.html for methodology and measured latency tradeoffs. Never infer RAM, learning, allocator, SOTA or universal superiority.

Enumerate MCP tools; use create_universe/address_experience/materialize/inspect_state/get_provenance. Tools use fixed synthetic state; validate_adapter covers only built-in contract. Test custom adapters via SDK, never upload code to MCP. See https://zeitcow.github.io/implicit-core/mcp.html for bounds/errors.

Preserve user journals, credentials and configuration. Exclude secrets/evaluator answers/private reasoning from public records. Reconcile interrupted effects before abandonment/replay. Ask before destructive user-data changes unless already authorized. Report measured output/provenance/errors and Core modification count. Report actual public package availability separately from unverified marketplace registration.
