---
name: dashboard-snapshot
description: Capture a Grafana dashboard snapshot for incident timelines + postmortem evidence — public-snapshot URL, time-range pinned, variables resolved.
---

# dashboard-snapshot

> Take a permalinked snapshot of a Grafana dashboard at a specific time window so an incident timeline or postmortem can reference exactly what the on-call saw. Output is the snapshot URL + the variables/time captured.

> **MCP binding (read before any tool call):** resolve which server backs `grafana` from `${POLYMATH_PLUGIN_DATA:-$HOME/.polymath/data}/polymath-core/project-context.json` `mcpResolution.grafana` — when `source` is `host`, the CURRENT host agent's own `grafana` MCP server is ALREADY registered: use its tools (`toolPrefix` gives the naming) and do NOT register or start a polymath copy. A server registered in a DIFFERENT agent is never a substitute. When `source` is `plugin`, the plugin-shipped `.mcp.json` server backs this skill. When `none`, credentials are unconfigured: ask the user to configure them or degrade gracefully. See the `polymath-core:mcp-bridge` skill.

## When to use

- An incident timeline needs a permalinked dashboard, not a live URL that keeps changing.
- A postmortem references "the spike at 14:08" and needs an artifact.
- A code review asks "show me the latency before/after this change" and the dashboard's live time range is wrong.

## Inputs

- Dashboard UID or URL (required) — resolve to dashboard UID via the grafana MCP.
- Time range (required) — explicit `from` + `to` ISO-8601, or a relative spec like `from=now-2h&to=now-30m` (snapshot resolves it to absolute timestamps at capture).
- Variables (optional) — template variables (e.g. `service=refund-api`, `env=prod`). Required when the dashboard uses them; otherwise the snapshot is ambiguous.

## Procedure

1. **Resolve the dashboard.** `dashboards.uid` or `search?query=...` to get the UID. Refuse if multiple match — pick the most specific or surface the candidates.
2. **Validate variables.** Fetch dashboard JSON; identify required template variables. Refuse if any required variable is unspecified (a snapshot with the wrong default variable is worse than no snapshot — it looks authoritative but isn't).
3. **Resolve relative time.** Convert `now-X` to absolute UTC timestamps at capture time. Embed the absolute range in the snapshot URL.
4. **Create the snapshot** via `POST /api/snapshots`:
   - `dashboard` — the dashboard JSON with the chosen time + variables pinned.
   - `expires` — pick a long-but-finite TTL (default 90 days for incident, never permanent; permanent snapshots leak).
   - `external` — `false` (host on the same Grafana). `true` only when sharing with non-authenticated viewers AND the dashboard contains no sensitive labels.
5. **Capture the snapshot URL + deleteKey.** The deleteKey lets you revoke later; store it in the artifact file alongside the URL.
6. **Save an artifact** at `docs/incidents/<id>/grafana-snapshots/<dashboard-slug>-<timestamp>.json` with `{ url, deleteKey, dashboardUid, time, variables, expiresAt }`.

## Output

```text
dashboard-snapshot

Dashboard:    refund-api-overview (uid abc123)
Time:         2026-05-23T14:00:00Z → 2026-05-23T14:30:00Z (absolute)
Variables:
  service = refund-api
  env     = prod

Snapshot URL:  https://grafana.example.com/dashboard/snapshot/8z9y…
Expires:       2026-08-21T14:00:00Z (90d)
Delete key:    saved (artifact only — not echoed here)

Saved artifact:
  docs/incidents/2026-09-refund-async/grafana-snapshots/refund-api-overview-20260523T1400Z.json
```

## Quality bar

- Absolute timestamps in the snapshot, never `now-X` left unresolved.
- Required template variables specified.
- `expires` is finite (not permanent).
- `deleteKey` saved in the artifact, not echoed in chat.
- `external=true` only with explicit sensitive-label check.

## Anti-patterns to avoid

- Capturing a snapshot with the dashboard's default variables and assuming it shows what you mean. Different defaults across users → different snapshots.
- Permanent snapshots ("`expires=0`"). Postmortem snapshots should age out; if you need it forever, screenshot it into the doc.
- External snapshots of dashboards with PII labels (user IDs, IPs). The external snapshot service is a separate cache.
- Skipping the artifact write. The deleteKey + URL pair is the rollback path.

