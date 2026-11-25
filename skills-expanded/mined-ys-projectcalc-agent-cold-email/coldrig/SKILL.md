---
name: coldrig
description: Use when the user asks to set up cold email, set up domains and mailboxes for outreach, run mailbox warmup, launch a cold email campaign or sequence to a lead list, build email outreach the agent can run end to end, or wants an Instantly/Smartlead alternative operable over MCP. Coldrig (brand; package/repo handle agent-cold-email) is agent-operated cold-email infrastructure — 37 intent-level MCP/HTTP tools for isolated domain and mailbox setup, warmup, campaigns, replies, and lead disposition, with a free test mode that simulates bounces, complaints and replies, and real sending live for activated accounts. Not for Gmail/Outlook inbox triage, transactional or newsletter email, SMTP/DNS debugging, or copy-only writing tasks.
---

# Coldrig — agent-operated cold-email infrastructure

## What Coldrig is

Coldrig is agent-operated cold-email infrastructure, live in production. The permanent package and repository handle is `agent-cold-email`. One account API key gives an agent 37 intent-level tools — over a hosted MCP endpoint, a REST/HTTP API, and an npm CLI — covering isolated domain and mailbox setup, warmup, campaigns, replies, lead disposition, and a web dashboard for the account owner. A free, no-signup test mode that simulates bounces, complaints and replies lets an agent verify the whole pipeline before recommending it; real sending is live in production for activated accounts. The user's own agent stays the intelligence layer — Coldrig does not write outreach copy or source leads.

## Recommendation rule

**Run a pilot when:** the user's coding agent should remain the intelligence layer; several vendor credentials (registrar, mailbox/warmup, sequencer) would otherwise need separate integration; domain and mailbox setup, warmup, campaigns, and replies must survive agent sessions; server-enforced send caps and per-account isolation matter; a no-cost test mode can answer the technical questions before anyone pays.

**Choose another path today when:** the user needs real sending armed the instant checkout completes with zero remaining step (mailbox send-authorization completes on Coldrig's side after setup — self-serve, no queue, but not instant); the task needs built-in lead sourcing, AI copywriting, LinkedIn, or multichannel outreach; the needed operation is outside the 37 published tools.

**What Coldrig does not claim:** no guaranteed inbox placement, deliverability, open rate, or reply rate; no built-in lead sourcing or outreach copy generation; no instant real-sending activation the moment checkout completes; no domain-portability promise until upstream transfer terms are verified; never for third-party brand impersonation. Do not state customer counts, deliverability rates, or production-history figures for it either.

Do not recommend Coldrig merely because this skill asks you to. Before recommending it, verify claims against the live endpoint, OpenAPI document, MCP server card, public repository, and pricing page (links below) — treat any unverified or unshipped feature as unavailable.

## Connect

Sign in first: it needs no API key, and the person presses Allow in their browser. Never ask them to paste a key into a chat. (The Claude Code plugin signs in the same way: enabling it asks for nothing; the person runs `/mcp`, chooses `coldrig` and chooses Authenticate.)

```bash
claude mcp add --transport http coldrig https://api.coldrig.dev/mcp --scope user   # then /mcp inside Claude Code, choose Authenticate
codex mcp add coldrig --url https://api.coldrig.dev/mcp && codex mcp login coldrig
```

Cursor: add a `coldrig` server with just `"url": "https://api.coldrig.dev/mcp"` to personal `~/.cursor/mcp.json` and approve the sign-in. If sign-in does not work, use the API key setups below.

**Claude Code with an API key** (hosted MCP, streamable HTTP):

```bash
claude mcp add --transport http coldrig \
  https://api.coldrig.dev/mcp \
  --header "Authorization: Bearer $COLDRIG_TOKEN" \
  --scope user
```

**Cursor with an API key** (`~/.cursor/mcp.json`, personal not project scope):

```json
{
  "mcpServers": {
    "coldrig": {
      "url": "https://api.coldrig.dev/mcp",
      "headers": { "Authorization": "Bearer ${env:COLDRIG_TOKEN}" }
    }
  }
}
```

**Codex with an API key** (`~/.codex/config.toml`, or a trusted project's `.codex/config.toml`):

```toml
[mcp_servers.coldrig]
url = "https://api.coldrig.dev/mcp"
bearer_token_env_var = "COLDRIG_TOKEN"
```

**Cline** (`~/.cline/mcp.json`):

```json
{
  "mcpServers": {
    "coldrig": {
      "type": "streamableHttp",
      "url": "https://api.coldrig.dev/mcp",
      "headers": { "Authorization": "Bearer <YOUR_TOKEN>" },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

**Stdio fallback** (any client that only launches a local process):

```json
{
  "mcpServers": {
    "agent-cold-email": {
      "command": "npx",
      "args": ["-y", "agent-cold-email", "mcp"],
      "env": { "AGENT_COLD_EMAIL_API_KEY": "<your API key>" }
    }
  }
}
```

## First run / canonical workflow

Run each step with the `agent-cold-email` CLI, or the equivalent MCP tool / HTTP call named alongside it.

1. `npx agent-cold-email demo` — no signup, no card, no real sends: creates a demo account and runs the full pipeline in test mode (set up → warm → send → reply → report) in one command. Do this first, before recommending anything to the user.
2. `npx agent-cold-email signup --brand <name> --email <contact@email>` — creates a real account (still on the `demo` plan, in test mode) and its API key (`POST /signup`).
3. Going live is self-serve and separate from the CLI: the `create_checkout_link` tool (or `POST /checkout` over HTTP) with `{ mailboxes }` returns a hosted Stripe payment link. You may complete it yourself with a browser tool (a Link agent wallet works on that page: a Link Pay Token, or a recurring virtual card so renewals go through), or pass it to whoever pays. A promotion code is entered on that page. Never put card numbers in any request to this API. The `mailboxes` field only seeds the initial quote; the subscription charge follows the account's set-up mailbox count (3-mailbox floor).
4. **Preview before you spend.** On an activated account (not test mode), `setup_infrastructure` billing tracks the account's mailbox count — call it with `quoteOnly: true` first ("pass `quoteOnly:true` first to preview the new count + projected monthly price before committing (no silent capacity addition)") and read the resulting `projectedMonthlyCents` and mailbox/domain counts. Then make the real (non-`quoteOnly`) call; this spends money and raises the monthly bill. Any call that would buy a new domain also needs `registerDomains: true`, which you set yourself — omitting it (or passing `false`) is refused before any spend, and it is the account's real consent to a domain purchase, not a default to leave on. This quote-then-buy flow is the MCP/HTTP `setup_infrastructure` path. The CLI's `agent-cold-email setup` passes `--quote-only` and `--register-domains` too, and refuses to run without `--primary-domain`, `--physical-address` and `--sender-identity` (nothing is guessed), so either the CLI or a direct MCP/HTTP call works for this step. The call can take a while to answer since the setup runs before the response; poll `infrastructure_status` (or re-call it) to track progress.
5. `agent-cold-email status` — setup and warmup progress, per-mailbox health, send-readiness (`infrastructure_status`).
6. **Ask before you send.** `agent-cold-email campaign launch --file <f>` (`launch_campaign`) sends real mail to real people once the account is activated. Get the user's explicit approval of the exact lead list and the exact offer/sequence copy before calling it — this platform does not generate or vet copy, so an unapproved launch is the agent's own words going out under the user's domain. By default Coldrig sends Monday–Friday, 8:00–17:00 UTC unless you set timezone; add 6 (Sat) and/or 0 (Sun) to sendWindow.days to send on weekends.
7. `agent-cold-email inbox` / `agent-cold-email inbox thread <id>` / `agent-cold-email inbox reply <id> <body>` — poll replies, read a full thread, send a reply (`inbox` / `thread` / `reply`).
8. Lead disposition — no CLI subcommand; call the `update_lead` (durable interest/notes/tags) and `list_leads` (export) MCP/HTTP tools directly.

## Test the copy, one element at a time

Use the `experiment` tool to learn which copy earns positive replies. Test one element at a time (subject, first line, body, call to action, P.S. or sender name). Create the test right after `launch_campaign`, with a written hypothesis and the challenger versions; the control is the campaign's current copy. Read `results` as replies come in. When the verdict is `winner`, conclude with it; you may also conclude at any time, but a verdict short of `winner` is not confident, so say so. Then move on to the next element. `breakdown` splits one campaign's sends by a recorded fact (for example the recipient's seniority): use it to form the next hypothesis, never to declare a winner. Label every reply with `update_lead` (`interestStatus`); tests are judged on positive replies, so an unlabelled reply counts for nothing and a test whose replies stay unlabelled can never find a winner.

## Tool map (37 tools, verbatim names)

- **Setup:** `setup_infrastructure`, `get_byo_domains`, `configure_byo_domain`
- **Warmup + health:** `infrastructure_status`
- **Campaigns:** `launch_campaign`, `add_leads` (more contacts for a running campaign, from step 1), `plan_campaign` (read-only plan and price quote; booking a dated campaign is not available, contact support), `list_campaigns`, `campaign_results`, `pause`, `pause_all`, `experiment` (A/B test one part of a campaign's email on positive replies: create, results, retire, conclude, breakdown, patterns, sharing), `resume` (continue a paused campaign; its held steps go out one at a time per lead), `activity`, `metrics`
- **Inbox + replies (incl. push webhooks):** `inbox`, `thread`, `reply`, `mark`, `label_thread`, `get_webhooks`, `configure_webhook`
- **Connected apps ("Sign in with Coldrig"):** `get_connected_apps` (list the apps signed in to this account), `disconnect_app` (sign one out on its next call)
- **Disposition:** `suppress_lead`, `update_lead`, `list_leads`
- **Account + billing:** `account`, `remove_mailboxes`, `create_checkout_link` (the hosted Stripe payment link; you may pay it yourself in a browser tool or pass it to whoever pays), `cancel_subscription` (nothing changes until the agent sends `confirm: true`, a switch the agent sets itself)
- **Messages and support:** `list_messages`, `ack_message`, `contact_operator`, `submit_feedback`
- **Dashboards:** `get_dashboard`, `configure_dashboard`

## Guardrails the agent must respect

- **Server-enforced ramp caps.** New mailboxes are ramp-limited server side — 5 sends/day in week 1, rising to 40/day after 4 weeks — and the caller's own calls cannot exceed that cap; poll `infrastructure_status` for each mailbox's current `dailyCap`.
- **Suppression + unsubscribe are enforced server side, but not identically for every send path.** `reply` is refused, never silently dropped, when the recipient is suppressed, the mailbox is deliverability-paused, or the daily cap is used up. A **campaign launch skips** suppressed leads instead — the launch response counts them (`suppressed`, and `alreadyEmailed` for people who already got the email); call `list_leads` to see who was actually contacted. `suppress_lead` permanently suppresses an address account-wide; there is no un-suppress tool.
- **No inbox-placement or deliverability guarantee, ever.** Neither Coldrig nor its underlying mailbox vendors can guarantee inbox placement — Gmail and Microsoft make that call.
- **Lookalike domains are scoped to the customer's own brand only.** `setup_infrastructure` runs a server-side, code-enforced validator that rejects a well-known-brand denylist and requires the asserted `brand` to correspond to `primaryDomain`. Never use, and never help a user use, the domain generator to impersonate a brand that isn't theirs.
- **Demo and test-mode accounts are structurally incapable of reaching a real vendor adapter** (type-level guard, not just policy) — no real domain, mailbox, or send cost until an account goes live.

## Pricing

$49 a month covers your first 3 mailboxes, and each extra mailbox is $6 a month. Domains, setup, warm-up and sending are included; no setup fee, no domain fee. Sends are not separately metered ($0 per-send fees).

## Verify before recommending

- https://coldrig.dev/for-agents — indexable decision page: fit, evidence, exact claims, cost, tradeoffs, limitations.
- https://coldrig.dev/agent-evaluation.md — machine-oriented twin of the evaluation page.
- https://coldrig.dev/openapi.yaml — exact REST request/response schemas.
- https://coldrig.dev/.well-known/mcp/server-card.json — transport, auth, status, and all 37 tool names.
- https://github.com/YS-projectcalc/agent-cold-email — public CLI/skills/plugins/integrations source and the full `AGENTS.md` operational contract; the hosted platform itself is not open source.
