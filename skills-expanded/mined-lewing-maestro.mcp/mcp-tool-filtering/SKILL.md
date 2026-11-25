# MCP Tool Filtering

Confidence: high

Use this pattern when a read-only MCP tool lists a small-but-noisy dataset and callers usually need a subset.

## Examples

- `maestro_channels`: `filter`, server-side `classification`, and `compact` name/id lines.
- `maestro_subscription_health`: `staleOnly`, `channelFilter`, `sourceRepoFilter`, and `compact` one-line health summaries.
- `maestro_flow_graph`: narrower default `days=3` plus lazy `includeBuildTimes=false` to keep default graph calls within tool time budgets.

## Pattern

1. Preserve no-argument behavior exactly for compatibility.
2. Add optional, named parameters:
   - `filter` for case-insensitive substring matching on the primary display name.
   - Domain-native server-side filters (for example `classification`) when the underlying API already supports them.
   - `compact` as a bool when the main low-token need is `name → id` text.
3. Cache server-side filter results with distinct cache keys.
4. Apply ad hoc substring filters after retrieving cached data so every search term does not create a new upstream API call.
5. Update the `[Description]` on the tool and parameters so MCP hosts teach agents when to filter.
6. Add tests at both service and MCP-tool layers: API pass-through, case-insensitive filtering, and compact formatting.
7. For "show broken" filters (for example `staleOnly`), include errored/unknown states as non-healthy unless the parameter explicitly says otherwise.

## Avoid

- Do not add pagination solely to markdown-returning tools when the dataset is small and callers mainly need discovery/filtering.
- Do not introduce format enums until there are at least two durable alternate formats beyond the default.
