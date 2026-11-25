---
name: model-routing-refresh
description: Refresh a user- or project-owned point-in-time guide for model prompting, benchmark-aware routing, execution lanes, and pricing when the model landscape changes.
---

# Model Routing Refresh

Use this skill only when the owner explicitly requests or authorizes refreshing a routing guide. Ordinary orchestration must not trigger it automatically.

## Target

Use the path named by the user or project instructions. Otherwise update `~/.codex/model-prompting-and-routing.md`. If the target does not exist, use the plugin's bundled [routing snapshot](../approval-gated-orchestrator/references/model-prompting-and-routing.md) as the starting structure.

Do not edit the installed plugin's bundled snapshot. It is a versioned fallback; refreshed output belongs in a user- or project-owned path.

## Workflow

1. Read the existing target, or the bundled snapshot when creating the target. Preserve useful structure and prior decisions; update the date and increment the version.
2. Use live web research. Start with official model, prompting, and pricing documentation. Verify exact model names before adding or removing them.
3. For comparisons, use a current independent benchmark source with multiple task families and disclosed methodology. Record the benchmark version and access date.
4. Check current pricing for every included model. Label direct and routed pricing distinctly. Never silently treat a missing price as zero.
5. Keep recommendations capability-specific. Separate measured results from qualitative judgment, and mark missing or incomparable data as `—`.
6. Verify currently available execution platforms, provider routes, model IDs, reasoning levels, and usage commands rather than copying machine-specific status from the bundled snapshot.
7. Preserve the cross-platform task identity and naming contract unless the owner explicitly changes it.
8. Update source links and limitations. Do not invent scores, dates, capabilities, model IDs, prices, or quota state.

## Required Output

The guide must contain:

- date and version;
- provider-neutral prompting guidance and relevant model-specific notes;
- capability classification;
- a performance-versus-cost routing matrix;
- explicit pricing basis and evidence labels;
- execution-lane requirements;
- the canonical task reuse and naming contract;
- sources and limitations.

Retain exactly 50 model entries only when the existing guide or owner requires a best-50 shortlist.

## Boundaries

Use public, credential-free sources. Do not expose API keys or private account data, create accounts, run paid calls, install integrations, modify unrelated files, or create duplicate schedules. Model facts are time-sensitive; label the snapshot date and avoid universal rankings.
