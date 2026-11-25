---
name: agentdom
version: 0.1.0
description: Universal execution backend — 1,300+ intents across 13 providers (GitHub, Stripe, Linear, HubSpot, Slack, Notion, Vercel, Supabase, Resend, Cal, OpenAI, Anthropic, OpenRouter) plus any app exposing .well-known/agentdom.json.
homepage: https://getagentdom.com
license: MIT
runtime:
  type: mcp
  transport: stdio
  command: agentdom
  args: ["serve"]
permissions:
  network: prompt
  filesystem: deny
  process: allow
tools:
  - name: dispatch_intent
    description: Route an intent to the cheapest available transport (api > cli > browser > desktop) across all registered providers.
    schema:
      intent:   { type: string, required: true, description: "Dotted intent id, e.g. contacts.create, issues.create, messaging.send" }
      args:     { type: object, required: false, description: "Arguments matching the intent's schema" }
      provider: { type: string, required: false, description: "Optional provider host to pin (e.g. linear.app, github.com)" }
  - name: wallet_auth
    description: Authenticate to a provider via OAuth2 / API key / device flow. One-time setup per provider; persisted in ~/.agentdom/wallet.json.
    schema:
      provider: { type: string, required: true }
      intents:  { type: array,  required: false, description: "Intents the agent will need — used to compute OAuth scopes" }
  - name: wallet_list
    description: List authenticated providers (secrets are not returned).
  - name: discover_surfaces
    description: Enumerate every surface this machine can drive — running desktop apps, installed CLIs, live browser sessions — with an inverted intent index.
    schema:
      intent: { type: string, required: false }
  - name: scan_app
    description: Auto-generate typed tools for a running desktop app via the accessibility tree.
    schema:
      app: { type: string, required: true }
  - name: policy_list
    description: Show the current permission policy and any pending approval requests.
notes:
  - First-run auth is browser-mediated. Subsequent runs are fully headless.
  - For CI/Docker, export the wallet with `agentdom wallet export --base64` and pass via AGENTDOM_WALLET_B64.
  - Side-effecting intents (send, delete, write) honor the AgentDOM policy engine. Set policy via `agentdom policy set`.
---

# AgentDOM skill for OpenClaw

This skill turns AgentDOM into OpenClaw's universal execution backend. Where OpenClaw's
built-in tools (browser, canvas, nodes, cron, Discord/Slack actions) cover the inbound
and presentation layers, AgentDOM covers the outbound execution layer for any SaaS API,
desktop app, CLI tool, or web UI.

## What you get out of the box

| Provider       | Auth        | Intents |
| -------------- | ----------- | ------- |
| github.com     | Device Flow | 811     |
| stripe.com     | API Key     | 442     |
| linear.app     | OAuth 2.0   | 8       |
| hubspot.com    | OAuth 2.0   | 8       |
| vercel.com     | API Key     | 8       |
| slack.com      | OAuth 2.0   | 6       |
| notion.so      | OAuth 2.0   | 6       |
| supabase.com   | API Key     | 7       |
| resend.com     | API Key     | 5       |
| cal.com        | OAuth 2.0   | 6       |
| openai.com     | API Key     | 5       |
| anthropic.com  | API Key     | 2       |
| openrouter.ai  | API Key     | 3       |

Plus any host that publishes `.well-known/agentdom.json` — discovered at call time.

## How an OpenClaw agent uses it

```js
// Lobster workflow step
await dispatch_intent("issues.create", {
  title: "Login crash on iOS 17.5",
  description: "Stack trace attached",
  assignee: "alice",
}, "linear.app");
```

The runtime resolves Linear's manifest, fetches the cached OAuth token, calls the
REST API, and returns the result. If Linear's API is down, it falls back to the
CLI transport; if no CLI exists, it falls back to the browser UI.

## Auth (one-time per provider)

```
wallet_auth({ provider: "linear.app" })
wallet_auth({ provider: "github.com" })
wallet_auth({ provider: "resend.com",  key: "re_..." })
```

After this, every subsequent agent run on this machine is headless.

## Approval integration

Side-effecting intents trigger AgentDOM's policy engine. The skill emits a
`policy.prompt` event when an action needs approval; route it into Lobster's
approval-gate queue and call `policy_approve(id)` to release it.

## See also

- [AgentDOM spec](https://github.com/RagavRida/agentdom/blob/main/WELL-KNOWN-SPEC.md)
- [Manifest format](https://github.com/RagavRida/agentdom/blob/main/MANIFEST-SPEC.md)
- [Publisher SDK](https://getagentdom.com/docs/publisher)
