---
name: givebutter-integration
description: Use when a nonprofit-toolkit skill could be grounded in live Givebutter data (donations, donors, campaigns, funds), or when deploying, configuring, or debugging the Givebutter integration. Explains when to invoke the Givebutter MCP tools and why the server is a remote Cloudflare Worker rather than a local stdio process.
---

# Givebutter integration

The `nonprofit-toolkit` plugin can connect to [Givebutter](https://givebutter.com) — the organization's fundraising platform — through an MCP server that exposes campaigns, contacts, transactions, households, funds, and financial data as tools. This skill explains **when to use those tools** and **why the integration is built the way it is**, so you make good calls about invoking it and don't "fix" the architecture by reverting it to something simpler that won't work.

## When to invoke the Givebutter tools

The other skills in this plugin produce far stronger output when grounded in real data instead of placeholders. Reach for the Givebutter MCP when the task benefits from live numbers, names, or campaign state:

| Skill | Givebutter tools that ground it | What you gain |
| ----- | ------------------------------- | ------------- |
| `donor-thank-you` | `list_transactions`, `get_contact`, `list_contact_activities` | Real donation amount, date, and donor history instead of `[AMOUNT]` placeholders |
| `organization-profile-builder` | `list_campaigns`, `list_funds` | Actual programs and designations, not invented ones |
| `grant-writing-basics` | `list_transactions`, `list_campaigns`, `list_funds` | True fundraising totals and outcomes for needs statements and budgets |
| `budget-creation` | `list_transactions`, `list_payouts`, `list_funds` | Actuals to build forward-looking budgets from |
| `social-media-content` | `list_campaigns` | Current campaign goals and progress for accurate promotion |

**Prefer the read tools** (`list_*`, `get_*`) when generating content. The server also exposes write tools (`create_*`, `update_*`, `delete_*`) that mutate a live donor database — only call those when the user has explicitly asked to change Givebutter data, and confirm the specifics first. There are 65 tools total spanning campaigns, campaign members/teams/tickets/discount codes, contacts (+ activities and tags), households, transactions, plans (recurring donations), pledges, payouts, funds, messages, and webhooks.

### When NOT to invoke it

- The user is drafting generic or templated content where real data adds nothing.
- The integration isn't connected (no URL configured — see below). The plugin's other skills all work without it; don't block on Givebutter.
- You only need one figure the user already gave you. Don't round-trip to the API for data you already have.

## Why it is configured the way it is

This is the part that's easy to get wrong if you only read `.mcp.json`. The upstream [givebutter-mcp](https://github.com/johnnylinsf/givebutter-mcp) is a **stdio** server — it runs as a local child process and talks over stdin/stdout. That works in desktop Claude Code but **fails in Claude Cowork, which runs each session in a sandboxed VM with no access to local processes**. Since the primary consumer here is a non-technical user in Cowork, a local stdio server was a non-starter.

So the integration is deliberately a **remote HTTP MCP server**:

```
plugin .mcp.json (type: http)  ─────►  Cloudflare Worker  ─────►  Givebutter REST API
   url + bearer token                  givebutter-mcp-worker        api.givebutter.com
   from userConfig                     (sibling repo)               (key held server-side)
```

- **The server runs remotely and is already deployed.** You do not need its source, the `givebutter-mcp-worker` repo, or any local files to call the tools — don't go looking for them. That repo is a separate project that only matters when someone deploys or extends the server, which is out of scope for using it.
- **`type: "http"` is required, not a preference.** Cowork's plugin MCP schema only supports remote transports (`http`/`sse`). Do not "simplify" the `.mcp.json` back to a `command`/`args` stdio block to "fix" a connection problem — stdio cannot run in Cowork's sandbox and this will break it.

### Credentials and security model

- The **Givebutter API key lives only on the Worker** as a secret (`wrangler secret put GIVEBUTTER_API_KEY`). It is never in this repo, the plugin, or the client config.
- The Worker is gated by an optional shared **bearer token** (`MCP_AUTH_TOKEN`). The Worker holds a full-access key behind an obscure-but-public URL, so the token is the only thing stopping anyone who learns the URL from driving the account. Treat it like a password; rotate it if it leaks.
- Neither the endpoint URL nor the token is committed. Both are supplied at **plugin-enable time** via the `userConfig` prompts declared in `plugin.json` (`givebutter_mcp_url`, `givebutter_mcp_token`), and substituted into `.mcp.json` as `${user_config.*}`.

### Caveat: userConfig substitution in Cowork

`${user_config.*}` substitution is documented for desktop Claude Code. Cowork's plugin `.mcp.json` schema (`type`/`url`/`headers`/`oauth`) does not explicitly confirm it honors the same substitution. If a Cowork user's integration fails to connect despite a correct URL/token, the fallback is to place the literal URL and token directly in their installed copy's `.mcp.json` — still never committed to this repo.

## Using it at runtime

If the integration is connected — the user supplied a URL when enabling the plugin — the Givebutter tools are simply available; call them as needed per the table above. If no URL is configured, the integration is off; it is optional, so proceed without it rather than trying to set it up yourself.

### Troubleshooting

| Symptom | What it means / what to do |
| ------- | -------------------------- |
| Givebutter tools aren't available at all | No URL was configured at enable time, or (in Cowork) `${user_config}` wasn't substituted. The integration is optional — continue without it, or ask the user to set the URL/token (and try the literal-value fallback noted above). |
| `401 Unauthorized` from the server | Bearer token mismatch between the plugin config and the server. A trailing newline or space when the token was pasted is the usual culprit — ask the user to re-enter it. |
| `API request failed: 401/403` inside a tool result | The Givebutter API key held by the server is wrong or revoked. This is a maintainer fix on the server, not something to resolve from here. |
| Connection works but a list is empty | Correct behavior — the account simply has no records for that resource yet. |

Deploying, extending (adding tools), or rotating the server's secrets is a maintainer task performed in the separate `givebutter-mcp-worker` project, documented in that repo's README. It is out of scope for using the tools and not something you need access to here.
