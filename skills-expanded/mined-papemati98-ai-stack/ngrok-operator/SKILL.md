---
name: ngrok-operator
description: Operate ngrok AI Gateway, HTTP/TCP/TLS tunnels, endpoints and webhooks. Use for sharing localhost, remote UAT connectivity, provider routing configuration, BYOK, access policies, request failures, usage and cleanup. Keeps API billing separate from Agent Fleet subscriptions and requires scoped approval for public exposure.
metadata:
  version: "0.1.0"
---

# ngrok Operator

## Start with the actual surface

1. Resolve project and host from Knowledge Hub and live state. Record account,
   environment, upstream address, objective, access scope and rollback target.
   `localhost` means the machine running the agent, not automatically the PC,
   test VM or AI Lab Server. Do not create another vault or default to local Hermes.
2. Choose only the needed reference:
   - [AI Gateway](references/ai-gateway.md): app.ngrok.ai, provider/model access,
     BYOK, budgets, fallback and inference diagnostics.
   - [Tunnels](references/tunnels.md): HTTP/TCP/TLS, policies, domains, process
     lifecycle and connectivity for DEV/UAT.
   - [Webhooks](references/webhooks.md): signatures, delivery, duplicates and replay.
3. For substantial work use the existing planning/Graph/Loop and `accept-system`
   contracts. Fleet selects the model and contractor; this skill operates the
   transport. Do not silently reroute subscription CLI work onto paid gateway API.
4. Read-only inventory may proceed. New or changed public tunnels, domains,
   production settings, credentials and real external effects need Mateusz's
   explicit approval for the exact operation. A request to install this skill
   grants none of these. Within an approved scope, execute without repeated prompts.

## Execution rules

- Prefer installed CLI or documented API over UI; use authenticated browser tools
  when no supported machine interface exists. Never invent a gateway CLI command.
- Recheck installed `--help` and current official documentation before mutation.
  If CLI is missing, report that prerequisite; do not claim the gateway is down.
- Separate agent authtoken, platform administration API key, AI Gateway management
  API key, gateway inference access key, provider key and webhook signing secret.
  Never print them, put them in task files/argv/history or copy credential stores.
  Use approved secret storage and process-scoped injection; do not change global
  provider environment variables belonging to other agents.
- Both ngrok and downstream providers are data processors to assess. Check
  retention, request logging and available opt-outs before non-synthetic payloads.
  Unknown remains UNVERIFIED; minimize data rather than claim zero retention.
  Never send production secrets, captured customer bodies or training-enabled
  Contributor model traffic as a diagnostic shortcut.
- The local traffic inspector can contain credentials and payloads. Keep it
  loopback-only, do not tunnel it, dump it or replay its history indiscriminately.
- Use small synthetic probes with deadlines and bounded retries. Distinguish
  timeout, auth, quota, upstream error, policy denial and incomplete output.
  Do not retry a potentially committed side effect without checking idempotency.

## Acceptance and closeout

Use [operation receipt](references/operation-receipt.md). A reachable URL or an
HTTP 200 is not sufficient: verify expected app behavior and denied unauthorized
access. For UI use `remote-computer-use` and role-based UAT; for webhooks confirm
exactly the expected synthetic business effect. Exclude real emails/payments.

Stop or restore only resources created/changed by this operation, identified by
endpoint/config ID and process identity. Never stop all ngrok processes. Verify
cleanup from the consumer side and preserve unrelated sessions.

Report outcome, URL/ID when safe, accepted tests, remaining prerequisites,
cost/quota if measured and rollback status. Record material integration state
with `llm-wiki record-handoff`; keep secrets and raw payloads out of the Hub.
Installed instructions, authenticated account and successful live operation are
three distinct states. Do not label file copying as native runtime discovery.
