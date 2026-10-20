---
name: grafana-setup
description: Set up Grafana access, including service accounts and tokens, and install the official mcp-grafana MCP server via Docker or binary. Use when connecting Caeros or scripts to a Grafana instance.
---

# Grafana Setup

Works for self-hosted Grafana (9.0+) and Grafana Cloud
(`https://<stack>.grafana.net`).

## Service account token

Grafana API auth uses service accounts (legacy API keys are deprecated):

1. Administration > Users and access > Service accounts.
2. Create a service account; assign the least role that covers your use
   (Viewer for read-only queries and dashboard search; Editor covers most
   mcp-grafana operations, including dashboard writes).
3. Add a token to the account; copy it once and store it in a secret manager
   or untracked `.env`. It will not be shown again.

Fine-grained RBAC (where available) lets you scope tighter, e.g.
`datasources:query` plus `dashboards:read` only.

```bash
export GRAFANA_URL="https://myinstance.grafana.net"   # or http://localhost:3000
export GRAFANA_SERVICE_ACCOUNT_TOKEN="<token>"
```

Sanity check: `curl -H "Authorization: Bearer $GRAFANA_SERVICE_ACCOUNT_TOKEN" $GRAFANA_URL/api/org` should return your org.

## mcp-grafana (official MCP server)

Source: https://github.com/grafana/mcp-grafana. This plugin's MCP config runs
it over stdio via Docker, passing `GRAFANA_URL` and
`GRAFANA_SERVICE_ACCOUNT_TOKEN` through from your environment (never inlined):

```bash
docker pull grafana/mcp-grafana
docker run --rm -i -e GRAFANA_URL -e GRAFANA_SERVICE_ACCOUNT_TOKEN \
  grafana/mcp-grafana -t stdio
```

No Docker? Install the binary instead and point the MCP config's `command` at
it with empty args (stdio is the default transport):

```bash
GOBIN="$HOME/go/bin" go install github.com/grafana/mcp-grafana/cmd/mcp-grafana@latest
# or download a prebuilt release from the repo's releases page
```

Optional env: `GRAFANA_ORG_ID` for multi-org instances.

## Tool categories

Enabled by default: search, dashboard, datasources, Prometheus, Loki,
alerting, incidents, annotations, snapshots, navigation, provisioning,
OnCall, Sift, Pyroscope. Disabled by default (enable with
`--enabled-tools "...,clickhouse"`): admin, CloudWatch, ClickHouse,
Elasticsearch/OpenSearch, Graphite, InfluxDB, Snowflake, and others. Each
category also has a `--disable-<category>` flag to trim the surface.

Flags: `-t/--transport` (stdio, sse, streamable-http; stdio default),
`--debug` for verbose HTTP logging.

## Troubleshooting

- 401/403: token expired or role too low; regenerate, or raise to Editor.
- Datasource tools failing on old Grafana: the by-UID API needs Grafana 9.0+.
- Docker on localhost Grafana: inside the container `localhost` is the
  container; use `http://host.docker.internal:3000` as `GRAFANA_URL`.
- Wrong org data: set `GRAFANA_ORG_ID`.
