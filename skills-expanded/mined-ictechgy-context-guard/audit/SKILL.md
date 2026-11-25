---
description: Audit local Claude Code transcript usage and summarize likely token hotspots. Use when the user asks where Claude Code tokens are going or wants evidence before optimizing.
argument-hint: [optional transcript path]
disable-model-invocation: true
---

# ContextGuard Audit

Run a best-effort transcript audit, then interpret the result conservatively.

Default command:

```bash
context-guard-audit ~/.claude/projects --top 20 --recommend
```

If the user supplies a path, audit that path instead. If no path is supplied, keep the default Claude projects path:

```bash
if [ -n "$ARGUMENTS" ]; then
  context-guard-audit "$ARGUMENTS" --top 20 --recommend
else
  context-guard-audit ~/.claude/projects --top 20 --recommend
fi
```

Report:

- observed token buckets: input, output, cache_read, cache_creation;
- new tokens per turn (cache_creation distribution) and the "by preceding tool_result" table: this is the quantity billed under prompt caching. The table covers every counted turn, so read the `cold_start` / `cache_rewrite` / `incremental` fields beside it before naming a tool. Turns that wrote the cached prefix track context size at that moment rather than what a tool just returned, so trimming one result does not change them. When those turns dominate, say so instead of naming the table's top tool;
- model distribution;
- query_source distribution: main, subagent, auxiliary;
- top transcript files and commands observed;
- generated recommendations with priority, reason, action, and evidence;
- `cache_friendliness` status, bounded prefix/tail churn signals, and any cache-layout findings;
- top likely causes and one safe next experiment;
- `token_calibration` (reconcile): observed bytes per cache_creation token vs the assumed bytes/4; `--token-proxy calibrated` re-derives the text token estimate from it (an observed corpus ratio with errors in both directions, not a tokenizer measurement); `guard_coverage`: share of large results that arrived through Read (guarded) vs Grep/Bash/MCP (unguarded);
- `context-guard doctor` adds a one-line hook-journal summary (interventions, bytes withheld, hook overhead) for the current project; quote it as observed counts, never as savings.

Privacy: default output uses basename+hash transcript labels and command category+hash labels. Do not ask for `--show-paths` or `--show-commands` unless the user explicitly wants local identifiers in the report. Cache-friendliness diagnostics use bounded redacted segment hashes and do not print raw prompt text. Recommendations are heuristics; treat them as hypotheses, especially with small `files` or `records` counts.

Caveat: Claude Code transcript schemas can change. Treat this as an operational signal, not billing authority. `cache_read`/`cache_creation` and `cache_friendliness` are provider-cache diagnostics, not proof of ContextGuard-caused token reduction. For billing authority, use Claude Console, cloud-provider billing, or configured OpenTelemetry metrics.
