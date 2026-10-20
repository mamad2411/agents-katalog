---
name: langfuse-setup
description: Set up Langfuse, including Cloud vs self-hosted deployment, API keys, environment variables, and the Langfuse Docs MCP server. Use when connecting an app to Langfuse for the first time or troubleshooting authentication.
---

# Langfuse Setup

## Cloud vs self-host

- **Langfuse Cloud**: managed, EU region at `https://cloud.langfuse.com`, US
  region at `https://us.cloud.langfuse.com`. Fastest start; free tier
  available.
- **Self-hosted**: the platform is open source (MIT core). Local or small
  deployments via Docker Compose from the `langfuse/langfuse` repo; production
  via Helm chart on Kubernetes. Self-hosting requires keeping the platform
  version current: newer SDK majors have minimum platform version
  requirements.

Pick the region or host once and keep it consistent: keys are scoped to a
project on one host.

## Keys and environment variables

Create a project in the Langfuse UI, then Settings > API Keys. You get a key
pair: public key `pk-lf-...` and secret key `sk-lf-...`.

```bash
export LANGFUSE_PUBLIC_KEY="pk-lf-..."
export LANGFUSE_SECRET_KEY="sk-lf-..."
export LANGFUSE_BASE_URL="https://cloud.langfuse.com"  # or US / self-host URL
```

- The secret key is server-side only: never ship it to browsers or commit it.
  Store in your secret manager or a local `.env` excluded from git.
- SDK auth uses both keys; direct REST calls use Basic auth with the public
  key as username and secret key as password.
- Older SDK versions used `LANGFUSE_HOST`; current SDKs read
  `LANGFUSE_BASE_URL`.

## Install

```bash
pip install langfuse                       # Python
npm install @langfuse/tracing @langfuse/otel   # JS/TS tracing
npm install @langfuse/client               # JS/TS prompts, scores, datasets
```

Verify connectivity with a minimal trace (see `langfuse-tracing`), then check
the project's Traces page. If nothing appears: wrong region URL and missing
`flush()` are the two most common causes.

## Docs MCP server

This plugin ships Langfuse's public Docs MCP server
(`https://langfuse.com/api/mcp`, streamable HTTP, no auth). It exposes search
over the Langfuse docs, GitHub issues, and discussions, so integration work
can pull current parameter shapes instead of guessing. Use it whenever exact
SDK signatures matter.

Langfuse also offers authenticated MCP servers for the data platform and for
prompt management (built into the platform at `/api/public/mcp`). Those
require project API keys; connect them separately if you want agents to read
traces or manage prompts directly.

## Troubleshooting

- 401: key pair mismatched with host or project; regenerate and re-export.
- Traces missing: confirm `LANGFUSE_BASE_URL` region, then flush before exit.
- Self-host SDK errors after upgrade: check the SDK's minimum platform
  version and upgrade the deployment first.
