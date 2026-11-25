---
name: tool-discover
description: "Search the offline generative-game catalog and available live metadata to recommend licensed, compatible tools for a concrete workflow."
---

# Tool Discover

## Outcome

Turn a production need into a small, evidence-backed tool shortlist.

## Required inputs

- desired artifact or workflow
- engine and operating system
- hardware, budget, privacy, and license constraints

Ask for missing information only when it changes the route materially. Otherwise
state conservative assumptions and proceed with read-only analysis.

## Workflow

1. Translate the request into required capabilities and quality gates.
2. Search the checked-in catalog first; enrich volatile metadata through GitHub only when available.
3. Filter by operating system, architecture, runtime, GPU backend, VRAM, application requirements, maturity, and license status.
4. Compare at most three candidates by capability, quality, cost, performance, permissions, and limitations.
5. Recommend one route and state why rejected candidates do not fit.

## Expected artifacts

- search criteria
- ranked shortlist
- license and risk notes
- recommended recipe

## Workflow-specific gates

- Do not refresh or rewrite the catalog implicitly.
- Unknown or custom code, weight, dataset, output, or commercial terms block commercial recommendations.
- A catalog entry is metadata, not permission to download or launch its repository.

## Production completion gate

Before recommending production use, complete and report all seven gates:

1. Rights, consent, code/model/dataset/output license, and generation-provenance checks.
2. Technical format, naming, scale, color, metadata, and target-import validation.
3. Visual and temporal consistency review across representative views and states.
4. Runtime memory, frame-time, draw-call, streaming, and asset-budget checks.
5. Playability and interaction smoke tests in the target runtime.
6. Screenshot, capture, diff, or artifact-regression evidence with reproducible settings.
7. Human approval before replacing source assets or promoting generated output.

Unknown rights, missing consent, unsupported hardware, conflicting host adapters,
or failed quality gates block production promotion. Preserve originals and make
fallbacks explicit.
