---
name: loggly-optimizer
description: Default workflow for any loggly MCP usage. Use whenever retrieving, filtering, aggregating, or diagnosing loggly data so queries stay token-efficient, API-efficient, and evidence is summarized compactly before raw event expansion.
---

# loggly Optimizer

Use a staged workflow that narrows search space early and keeps output compact.

Load [references/query-patterns.md](references/query-patterns.md) only when building complex filters, grouping patterns, or fallback plans.

## Non-Negotiables

1. Start with a narrow time range. Default to 60 minutes if the user does not specify a range.
2. Run aggregate-first queries before event-level pulls.
3. Prefer `count_events`, `field_facets`, `volume_metrics`, and `stats_query` over event retrieval.
4. Pull raw events only after narrowing by high-signal filters.
5. Use the smallest practical page size. Default to `size: 25`; increase only when justified.
6. Fetch the next page only if the first page leaves unresolved questions.
7. Summarize evidence by pattern and count. Do not dump full event payloads.
8. Include exact timestamps for key events and absolute dates in findings.
9. If the scope is still too broad after first narrowing pass, stop and state the missing filter needed.

## Tool Selection

1. Use `count_events` to measure scope quickly.
2. Use `field_facets` to identify the most informative dimensions (`host`, `app`, `log type`, tags, class/method fields).
3. Use `volume_metrics` for spike detection and trend segmentation before pulling lines.
4. Use `create_search` + `get_events` for targeted evidence with constrained size.
5. Use `iterate_events_page` and `iterate_events_next` only for deep dives after a first-pass summary.
6. Use `search_and_get_events` only for narrow, well-defined queries.
7. Use `raw_api_call` only when a required endpoint is unavailable via standard MCP tools.

## Workflow

1. Extract anchors:
- IDs, exact class/method, error strings, environment, and timeframe.
2. Scope check:
- Run `count_events` with anchor + time window.
- If count is high, run `field_facets`/`volume_metrics` to identify high-signal constraints.
3. Narrow query:
- Add exact phrases first, then dimensions (`host`, `app`, tags), then error/state qualifiers.
- Re-run `count_events` after each narrowing step.
4. Evidence pull:
- Run `create_search` with small `size`.
- Fetch only required columns in `get_events`.
- Pull additional pages only when necessary.
5. Compress output:
- Group near-identical messages by fingerprint and show counts.
- Keep only representative lines and key timestamps.
6. Report:
- State root cause hypotheses, confidence, evidence count, and remaining unknowns.

## Output Contract

1. `Scope`: query window, anchors, and final event count.
2. `Narrowing path`: each filter added and resulting count change.
3. `Top evidence`: grouped message patterns with counts and 1-2 example timestamps.
4. `Conclusion`: most likely cause(s), confidence level, and next query if needed.
