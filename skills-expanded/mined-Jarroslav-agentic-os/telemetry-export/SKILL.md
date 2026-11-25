---
name: telemetry-export
description: >-
  Project a pipeline run's governance ledgers (events.jsonl, decisions.jsonl)
  into redacted NDJSON and hand them to a host-declared observability backend.
  Invoke when an operator wants run/gate telemetry visible outside the
  workspace — "export run telemetry", "send this run's events to Axiom",
  "wire up observability for the pipeline", "ship gate decisions to our
  dashboard". Requires a declared profile in
  `.agentic/guides/integration/telemetry-flow.md`; absent that, this skill is
  a no-op by design. Not for: token/cost telemetry (unimplemented, see
  tokenomics.md's usage.sampled), querying a backend from an agent (use the
  backend's own MCP server or skill set), or any automatic/default export —
  this skill only runs when explicitly invoked or wired into a host-owned hook.
version: 0.1.0
license: Apache-2.0
allowed-tools: Read, Bash, Glob, Grep
---

# telemetry-export

Turns one run directory's append-only ledgers into a redacted NDJSON stream
and pipes it to whatever backend the host project has declared. Read
`references/observability-adapters.md` before touching this skill or its
projector — it is the contract that keeps this a thin, replaceable adapter
rather than a vendor client.

> **Deny-by-default.** The projector script never forwards `summary`,
> `verdict.rationale`, `prior_context`, or an `artifacts[]` path. If a question
> can't be answered from structural/enum fields, this skill does not answer it.
> Widening the allowlist is a decision for `observability-adapters.md`, not an
> ad-hoc addition here.

## Invocation

```
telemetry-export [run-dir]
```

`run-dir` defaults to the newest run under `docs/superpowers/runs/` (same
discovery `ticket-sync` uses). Typically invoked by an operator after a run
completes, or wired into a host's own Stop hook — this skill never registers
itself as a hook in `plugin.json`, so nothing exports by default.

## Steps

1. **Read the flow file.** Look for
   `.agentic/guides/integration/telemetry-flow.md`. If it is absent, or
   `**Status**` is not `configured`, stop — print nothing, append nothing.
   This is the same `warn-and-continue` posture as `work-item-adapters.md`.
2. **Resolve the run directory.** Use the given path, or the newest
   `meta.json` under `docs/superpowers/runs/` (maxdepth 2), matching
   `ticket-sync`'s discovery exactly so the two adapters never disagree about
   "the current run."
   If the run is managed by `.agentic/state/runtime.sqlite3`, invoke
   `legacy.export` before reading the compatibility files. If that operation is
   unavailable, block rather than exporting a stale view.
3. **Run the projector:**
   ```
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/export-run-telemetry.py" \
     --run <run-dir> --extra-fields "<Extra fields, if declared>"
   ```
   Capture stdout (the NDJSON batch) and the `CURSOR {...}` line the script
   writes to stderr.
4. **Nothing new?** If stdout is empty, stop without writing any event — a
   receipt for zero new lines would itself become the next `telemetry.*` line
   to exclude, for no benefit.
5. **Invoke the declared exporter**, piping the NDJSON batch to its stdin,
   under a timeout (120s, matching `ticket-sync`). Never let a nonzero exit or
   a hang block turn-end.
6. **Record the outcome** through the runtime event/evidence operation for a
   managed run, then refresh compatibility files with `legacy.export`. For an
   unmanaged legacy run, append the outcome to `events.jsonl`:
   - success → `telemetry.export_receipt`, `data` = the `CURSOR` object plus
     `{"line_count": <lines sent>}`.
   - failure/timeout → `telemetry.export_warning`, `data` =
     `{"reason": "<short reason>"}`. The `CURSOR` offsets are **not** advanced
     on failure, so the same batch is retried next invocation.

## What ships vs. what a host adds

This skill and its projector ship with zero egress: no endpoint, no token, no
vendor name. A host project opts in by writing
`.agentic/guides/integration/telemetry-flow.md` and picking a profile —
`references/profiles/axiom.md` or `references/profiles/otlp-logs.md` document
the two shipped ones; a `custom` profile can point at anything that reads
NDJSON on stdin.

## Related

- `references/observability-adapters.md` — the full contract (allowlist
  tables, `run_id` injection, failure handling).
- `scripts/export-run-telemetry.py` — the projector this skill invokes.
- `references/profiles/axiom.md`, `references/profiles/otlp-logs.md` — shipped
  backend profiles.
- `hooks/ticket-sync` — the sibling adapter this skill's run-discovery and
  failure posture deliberately match.
