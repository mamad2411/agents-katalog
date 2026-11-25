---
name: mcp-servers
description: "Configure, install, and maintain Google-managed and self-hosted MCP servers for GCP. Covers setup, auth (ADC and service-account impersonation), capability map, troubleshooting, and version tracking. Every MCP entry includes a gcloud CLI fallback. Use when the user mentions: MCP setup, google MCP, model context protocol GCP, MCP install, MCP auth, genai toolbox, MCP tools GCP, configure MCP, developer knowledge."
license: MIT
metadata:
  "googlecloud-plugin/version": "0.1"
  "googlecloud-plugin/triggers": "MCP server, MCP setup, google MCP, model context protocol GCP, MCP install, MCP auth, genai toolbox, MCP tools GCP, configure MCP, developer knowledge"
  "googlecloud-plugin/required-scopes": ""
  "googlecloud-plugin/mcp-servers": "developer-knowledge, google-cloud-run, google-bigquery, google-gke, google-storage, google-vertex-ai, google-iam, google-logging, google-monitoring"
---

# MCP Servers — Google Cloud

Configure and maintain Model Context Protocol (MCP) servers for Google Cloud. All auth flows through ADC, optionally impersonating a service account — no downloaded keys, no credential values stored anywhere.

## Auth Architecture

All GCP MCP servers authenticate via Application Default Credentials (ADC):

```bash
# Authenticate locally (developer machine)
gcloud auth application-default login

# Act as a service account (agent or automation) — no key file
gcloud auth application-default login --impersonate-service-account=SA@PROJECT.iam.gserviceaccount.com
```

CI outside Google Cloud uses Workload Identity Federation instead. See `shared/auth/README.md` for both patterns and the key-file exception.

## What the plugin ships vs what you opt into

The harness manifests (`.mcp.json`, `mcp_config.json`, `gemini-extension.json`)
ship `gcloud` and `developer-knowledge`. Neither passes a project in its
environment: the `gcloud` server inherits `CLOUDSDK_CORE_PROJECT` if you export
it, else your active gcloud configuration — exactly as `gcloud` does. Which
project a task targets is settled per session by `gcp-project-context`, and
passed as `--project` on every project-scoped command.

The portable `mcp.json` (Agent Plugins 1.0.0) declares **one** server — `gcloud`
— because that is the only one that starts with no user-supplied configuration:

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
  "mcpServers": {
    "gcloud": { "type": "stdio", "command": "npx", "args": ["-y", "@google-cloud/gcloud-mcp"] }
  }
}
```

Two consequences worth knowing:

- **No `env` block.** Agent Plugins expands only `${PLUGIN_ROOT}` and
  `${PLUGIN_DATA}`. A `${GCP_PROJECT_ID}` placeholder would be passed through
  *literally* and mis-set your project. Export it in your own shell instead —
  the client passes the ambient environment through:
  ```bash
  export CLOUDSDK_CORE_PROJECT=your-project-id
  gcloud auth application-default login
  ```
- **The capability table below lists logical GCP capabilities**, not entries in
  `mcp.json`. Most are reachable through the `gcloud` server; anything needing
  its own config file is an opt-in you add to your client's own MCP settings.

## Developer Knowledge — shipped in the harness manifests

`developer-knowledge` is Google's remote MCP server for official documentation
(Google Cloud, Firebase, Android, Web, Gemini), at
`developerknowledge.googleapis.com/mcp` over streamable HTTP. Use it for
platform facts — GA status, quotas, which role or service — before relying on
memory. For `gcloud` flag syntax, `gcloud help` stays the authority
(see `gcloud-guardrails`).

| Harness | Manifest | Auth |
|---------|----------|------|
| Claude Code | `.mcp.json` | ADC through `headersHelper` (`scripts/dk_adc_headers.py`); API key in `DEVELOPERKNOWLEDGE_API_KEY` as a fallback |
| Antigravity | `mcp_config.json` | ADC (`authProviderType: google_credentials`) |
| Gemini CLI | `gemini-extension.json` | ADC (`authProviderType: google_credentials`) |

No API key is needed if you are logged in to gcloud:

```bash
gcloud auth application-default login
gcloud config set project PROJECT_ID   # quota project for the docs API
```

User credentials are refused (`403`) without a **quota project**. Claude Code's
helper sends one as `X-Goog-User-Project`, taken from the ADC file's
`quota_project_id` or else the gcloud project; set it explicitly with
`gcloud auth application-default set-quota-project PROJECT_ID`. The helper runs
on each connection, prints `{}` if gcloud is missing or logged out, and the
static key header then applies:

```bash
export DEVELOPERKNOWLEDGE_API_KEY=...   # optional; in your shell profile, never in a repo
```

It is **not** in the portable `mcp.json`: it needs client-managed credentials,
and Agent Plugins 1.0.0 expands no placeholders beyond the plugin's own paths.

The helper needs `python3` on `PATH`. With neither a working gcloud login nor
a key, the server fails to connect; nothing else in the plugin depends on it.

**Already have a Developer Knowledge server of your own?** Claude Code drops a
plugin server whose URL matches one you configured yourself, so your entry
always wins. If yours depends on a key variable that is not set, every call
fails with `API key not valid`. Either:

- **use the plugin's server** — remove your entry by its configured name
  (`claude mcp list` shows it): `claude mcp remove YOUR_SERVER_NAME`; or
- **keep your own** — set the key variable it references.

## Google-Managed MCP Servers (v0.1)

| Server | Capability | Required Role |
|--------|-----------|---------------|
| `google-cloud-run` | Deploy/manage Cloud Run services | `roles/run.admin` |
| `google-bigquery` | Query/manage BigQuery datasets | `roles/bigquery.user` |
| `google-gke` | GKE cluster management | `roles/container.developer` |
| `google-storage` | Cloud Storage bucket ops | `roles/storage.objectAdmin` |
| `google-vertex-ai` | Vertex AI model/endpoint management | `roles/aiplatform.user` |
| `google-iam` | IAM policy management | `roles/iam.securityAdmin` |
| `google-logging` | Cloud Logging query/ingest | `roles/logging.viewer` |
| `google-monitoring` | Metrics, alerting | `roles/monitoring.viewer` |

## Remote Cloud CLI MCP — opt-in

Google also runs `gcloud` as a remote MCP server: `cloudcli.googleapis.com/mcp`, one tool (`run_gcloud_command`), executing each command in a Google-managed environment under your identity. Nothing starts on your machine. The shipped `gcloud` server (local `npx @google-cloud/gcloud-mcp`) stays the default; choose the remote one when you cannot run Node locally or want execution off the workstation.

`gcloud-guardrails` applies unchanged: the remote tool runs whatever command string it is given, including deletes.

**Prerequisites** — each is an action a named human authorises:

1. Enable the Cloud CLI Execution API (`cloudcli.googleapis.com`) on a host project. That project carries the API's quota and billing; it need not be the project you operate on.
2. Grant the caller `roles/mcp.toolUser` (permission `mcp.tools.call`) on the host project.
3. The caller still needs ordinary roles on the target resources (for example `roles/run.viewer`); the MCP role grants no resource access.

Missing either of the first two returns `403` on both tool discovery and calls.

**Configuration** — both clients below attach ADC themselves through `authProviderType: google_credentials`. The Antigravity form is the one Google's `gcloud` skill documents for this server; the Gemini CLI form follows Google's own `google-cloud-developer` extension manifest, which configures its remote server the same way.

Antigravity (`mcp_config.json`):

```json
"gcloud-remote": {
  "serverUrl": "https://cloudcli.googleapis.com/mcp",
  "authProviderType": "google_credentials"
}
```

Gemini CLI (`gemini-extension.json`):

```json
"gcloud-remote": {
  "httpUrl": "https://cloudcli.googleapis.com/mcp",
  "authProviderType": "google_credentials"
}
```

Claude Code has no equivalent of `authProviderType`, so it cannot attach ADC to a remote server from configuration alone; keep the local `gcloud` server there.

**Calling it** — `run_gcloud_command` takes `command` (the full `gcloud` line) and `project` (`projects/HOST_PROJECT`, used only for the API's quota and billing). Put `--project=TARGET_PROJECT` inside `command`; the `project` parameter does not set it. Treat `exit_code == 0` as the only success signal.

Not shipped in any manifest: it needs an enabled API and an IAM grant before it works, and the plugin enables neither on your behalf.

## GenAI Toolbox (Google's MCP for Databases) — opt-in

Google's MCP Toolbox for Databases enables LLM agents to query Cloud SQL, AlloyDB, Spanner, BigQuery, and more safely.

> **Why this is not shipped in any manifest.** Toolbox needs `--config <your tools.yaml>`,
> a path only you can supply. No Agent Plugins placeholder can express it, so
> shipping it in the portable manifest would mean a server that fails to start
> on every fresh install. Add it to your own client config once you have a
> `tools.yaml`. (A failing server is isolated by spec — it would not take the
> skills down — but a broken default is still a broken default.)

```bash
# Run the toolbox MCP server (requires a tools.yaml pointing at your database)
# Tested 2026-07-23: this is the correct package. Full docs: https://mcp-toolbox.dev
npx -y @toolbox-sdk/server --stdio --config tools.yaml

# Example tools.yaml (BigQuery source)
# sources:
#   my-bq:
#     kind: bigquery
#     project: PROJECT_ID
# tools:
#   run_query:
#     source: my-bq
#     description: Run a read-only BigQuery query
#     statement: SELECT ...
```

> **Package note (tested 2026-07-23):** use `@toolbox-sdk/server` via npx — **not** `pip install toolbox-core` / `uvx toolbox-core`. `toolbox-core` is the Python SDK *library* for building apps; it has no server CLI entry point.

- [MCP Toolbox for Databases (announcement)](https://cloud.google.com/blog/products/ai-machine-learning/mcp-toolbox-for-databases-now-supports-model-context-protocol)
- [GitHub: googleapis/genai-toolbox](https://github.com/googleapis/genai-toolbox)

## Self-Hosted / Community MCPs

| Server | Install | Use |
|--------|---------|-----|
| `gcloud-mcp` | `npx @modelcontextprotocol/server-gcloud` | Broad gcloud CLI coverage |
| `k8s-mcp` | Standard k8s MCP server | Kubernetes API for GKE |

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| `401 Unauthorized` | ADC not set or expired | `gcloud auth application-default login` |
| `403 Permission Denied` | SA missing required role | Add role per table above |
| `MCP server not found` | Server not installed | Check install step in references/ |
| Connection timeout | VPC firewall blocking | Verify Private Google Access + firewall |
| `gcloud-remote` returns `403` on `tools/list` | Cloud CLI Execution API not enabled on the host project, or caller lacks `roles/mcp.toolUser` | Ask an admin to enable the API and grant the role on the host project |
| `gcloud` server `failed` straight after installing or updating the plugin (Claude Code) | First connection after install/update failed (cause unknown; a separate cold `npx` start measured 2.8 s, inside the 30 s limit); Claude Code caches the failure for 15 minutes | Wait 15 minutes or reconnect from `/mcp`; use `gcloud` in the shell meanwhile |
| `developer-knowledge` returns `API key not valid` | A user-configured server with an unset key variable is shadowing the plugin's | Remove that server (`claude mcp remove YOUR_SERVER_NAME`) to use the plugin's, or set its variable |
| `developer-knowledge` returns `403` with ADC | No quota project, or the Developer Knowledge API is not enabled on it | `gcloud auth application-default set-quota-project PROJECT_ID`; ask an admin to enable the API |

## References

- [GenAI Toolbox Docs](https://github.com/googleapis/genai-toolbox/blob/main/README.md)
- [Model Context Protocol Spec](https://modelcontextprotocol.io/introduction)
- [MCP Servers Registry](https://github.com/modelcontextprotocol/servers)
