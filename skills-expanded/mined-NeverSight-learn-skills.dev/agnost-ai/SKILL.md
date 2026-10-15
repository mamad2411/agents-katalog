---
name: agnost-ai
description: USE to guide an AI agent or CLI tool through adding Agnost AI analytics to a customer Python or TypeScript app from this installed skill directory. Prefer Agnost SDK/MCP packages, use OTel only when the user explicitly asks for OTel or refuses Agnost packages, then verify with one real local or production interaction.
---

# Agnost AI integration

Work from the target app root. This is the skill route: do not tell the user to
install an npm package, use a global binary, or run a package runner. Agents may
call bundled `scripts/` helpers from this installed skill directory, but the
skill contract is the integration workflow.

## Ask first

Before editing, ask only for missing facts:

- Agnost org id from the dashboard.
- Target app/package path if the repo is a monorepo.
- Whether verification should happen in a local app or deployed production app.
- Whether installing Agnost packages is allowed.
- The real AI entrypoint: chat route, agent call, MCP server startup, or tool call.
- How the app is restarted or deployed after env/code changes.

If the org id is absent, stop and ask for it. Do not invent one.

## Choose the route

Prefer SDK/MCP integration:

- TypeScript conversation app: install `agnostai`, initialize once, wrap the real
  model/agent call with `begin()` and `end()`.
- Python conversation app: install `agnost`, initialize once, wrap the real
  model/agent call with `begin()`/`end()` or `track_ai()`.
- TypeScript MCP server: install `agnost`, call `configureFromEnv()` and
  `trackMCP(server, orgId, config)` after server construction and before
  transport connection.
- Python MCP/FastMCP server: install `agnost-mcp`, call `track(server, org_id,
  config(...))` after tool registration and before `run()`.

Use OTel only when the user explicitly requests OTel or refuses Agnost SDK/MCP
packages. Supported recipe targets include Vercel AI SDK, Mastra, Spectrum TS,
LangChain, OpenAI, and other already-instrumented OTel apps.

Do not make a synthetic fetcher or custom OTLP payload path when an official SDK,
MCP wrapper, or framework OTel option exists.

## Read the right reference

Open only the matching section from `references/frameworks.md`:

- `#conversation-ts-agnostai`
- `#conversation-py-agnost`
- `#mcp-ts-agnost`
- `#mcp-py-agnost-mcp`
- `#vercel-ai-otlp`
- `#openai-openinference-otlp`
- `#mastra-otlp`
- `#spectrum-ts-app-level-otel-spans`
- `#langchain-langsmith-otel-mode`

For `vercel-ai`, read `references/frameworks.md#vercel-ai-otlp` before editing.
Use the official Agnost recipe only: OTel exporter setup plus
`experimental_telemetry` on modern `generateText`/`streamText`/`generateObject`
calls. If the app uses legacy `OpenAIStream(...)` without a modern call shape,
configure env/deps only if the user chose OTel, then report that app telemetry
requires migrating to a supported Vercel AI SDK call shape or using SDK
instrumentation. Do not generate custom OTLP fetches, synthetic spans, or
wrapper functions.

## Script helpers

Scripts are helpers for agents and CLI tools, not the product surface.

Use them only after choosing the route above:

```bash
node "$SKILL_DIR/scripts/detect.mjs" --dir . --strategy <auto|sdk|otel> --json
node "$SKILL_DIR/scripts/instrument.mjs" --dir . --framework <framework> --org-id <org-id> --mode <local|prod> --env-mode <file|shell|manual> --json
node "$SKILL_DIR/scripts/send-demo.mjs" --org-id <org-id> --transport <ingest|otel> --mode <local|prod> --json
```

`detect.mjs` can suggest a route. `instrument.mjs` can apply the narrowest known
edit. `send-demo.mjs` can check whether Agnost accepts traffic, but it does not
prove the customer app is integrated.

## Definition of done

Integration is done only when the user's own application runs locally with the
production Agnost endpoint and emits telemetry from its real code path.

- Set local app env to the real org id and prod endpoints:
  `AGNOST_ORG_ID=<org-id>`, `AGNOST_ENDPOINT=https://api.agnost.ai`, and when
  using OTel, `AGNOST_OTEL_URL=https://otel.agnost.ai`.
- Tell the agent harness/user to run the local application with its normal start
  command after env and code changes are applied.
- Trigger one real chat, agent action, or MCP tool call through that running
  local app.
- Confirm that event in the Agnost dashboard before saying the integration is
  complete.

Do not call integration done from `send-demo.mjs`, a standalone SDK snippet, or
any event that bypasses the user's running application.

## Verify

After dependencies, env vars, and code edits:

1. Ask the user to restart the local app or deploy/restart the production app.
2. Ask the user to perform one real chat, agent action, or MCP tool call.
3. Ask the user to check Agnost dashboard raw logs, conversations, tools, or
   traces for that real interaction.

Report the route used, files changed, env vars required, restart/deploy step,
and the exact real interaction needed for verification. If no event appears,
inspect app logs and env propagation before adding more code.

## Verification loop

Repeat until the real interaction appears in Agnost or a concrete blocker is
found:

1. Ask for the smallest missing evidence: restart/deploy confirmation, env var
   source, app logs, real interaction timestamp, dashboard screenshot/log, or
   the exact AI entrypoint.
2. Fix only the proven gap.
3. Ask the user to restart/deploy again and repeat the same real interaction.
4. Re-check the Agnost dashboard result before claiming success.
