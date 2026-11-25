---
name: eval-fetch
description: Use when a user asks to fetch Galileo evidence, provides Galileo URLs or IDs, says "fetch this Galileo link", or needs traces, sessions, experiments, or log streams saved locally.
---

# Eval Fetch

Use this skill to turn messy Galileo console links and IDs into local evidence.
The goal is a grounded debug packet, not a diagnosis.

Do not print secret values. Report only credential variable names, whether
expected variables are present, and the exact fetch blocker.

## First Parse The Input

Use `skills/eval-engineer/scripts/parse_galileo_url.py` when the user provides a
Galileo URL. Follow `skills/eval-engineer/references/galileo-url-intake.md` for
artifact-specific behavior.

Preserve source metadata in the packet:

- `source.console_url`
- `source.console_host`
- `source.workspace_slug`
- `source.project_id`
- artifact IDs such as `log_stream_id`, `experiment_id`, `session_id`, or
  `trace_id`

## Ask Only For Missing Information

- project URL: ask for log stream, experiment, session, trace, time window, or
  failure metric.
- Experiments list URL: ask for latest experiment, specific experiment, failing
  experiment, or comparison pair.
- Log stream URL: ask for latest N traces, failed traces, time window, or
  aggregate metrics if the user did not specify.
- Log stream aggregate metrics: use
  `skills/eval-engineer/scripts/fetch_log_stream_packet.py` with `--url` or
  `--project-id` plus `--log-stream-id`. This fetches traces, spans, sessions,
  aggregates numeric scorer metrics into `.galileo/current/debug-packet.json`,
  and reports `metric_fetch_status`.
- Trace/session URL: fetch that artifact and ask whether to compare against a
  baseline only if needed.
- If the URL parser returns `fetch_ready: true`, say the Galileo artifact is
  resolved. If a slice is still needed, ask which slice to fetch; do not label
  the URL as not fetch-ready.
- If the current repo has no fetch helper, SDK method, API route, or saved
  packet capable of fetching the requested aggregate, say `fetch implementation gap`.
  Do not imply that scorer aggregates, trace lists, or
  metric distributions were fetched when the command only parsed the URL.
- If `fetch_log_stream_packet.py` writes a packet with
  `metric_fetch_status: missing_metric_results`, say the fetch worked but
  Galileo did not return scored metrics for the requested slice.

## Gotchas

- Parsing a URL is not fetching evidence. Do not imply scorer aggregates, trace
  lists, or metric distributions were fetched unless a fetch helper or saved
  packet actually produced them.
- Function experiments may produce system token and latency metrics while
  requested scorer aggregates are absent. Treat that as missing quality evidence,
  not as a passing quality result.
- If a project URL resolves but no slice is specified, ask for the smallest
  useful slice instead of marking the URL unusable.

## Validation Loop

After fetching or writing a packet:

1. Confirm `.galileo/current/debug-packet.json` exists or name the output path.
2. Check that `source` metadata and stable artifact IDs are present.
3. Run `python3 skills/eval-engineer/scripts/summarize_debug_packet.py <packet>`
   when a packet was written.
4. If validation fails, revise the fetch command, packet, or blocker statement
   before routing to `/eval-diagnose`, `/eval-measure`, or `/eval-cost`.

## Output

Write or guide writing `.galileo/current/debug-packet.json`. If fetching cannot
complete, state the blocker exactly: missing credentials, permission denied,
ambiguous URL, incomplete scorer jobs, or missing metric results.
