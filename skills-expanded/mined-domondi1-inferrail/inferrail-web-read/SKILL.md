---
name: inferrail-web-read
description: Read public web pages as clean markdown with each page's own metadata (description, canonical URL, authors, published and modified dates, language), one URL for $0.002 or up to 10 URLs in one call at $0.002 per page, paid in USDC from a wallet your agent already has (AgentCash or any x402/MPP client). Use when a task needs the text of an article, docs page, changelog or product page, or evidence from several sources; a page that can't be read (blocked, missing, bot check, JavaScript-only) is never charged, and a retry never pays twice.
---

# Inferrail Web Read

One public web page as clean markdown, $0.002 per delivered page, or up to 10 in one call. No
account, no API key: your agent pays per page from its own wallet.

## When to call it

- A task needs the text of an article, docs page, changelog, release notes or product page.
- You are gathering evidence from several sources you already have the URLs for (one call).
- You need the page's own date, author or canonical URL to cite it.

## When another tool is better

If your environment already has a free web fetch tool that returns what you need, use it.
Web Read is worth paying for when you have none (many agent runtimes don't), when you need
clean markdown plus the page's declared metadata in one predictable JSON shape, or when you
want several pages in one call. It reads pages without running JavaScript and honours
robots.txt, so it can't read pages that need a browser or that block crawlers; those are
refused and never charged.

## Paying from your agent (AgentCash wallet)

The simplest path for a coding or research agent, with no API key and no account:

1. **Ask your user before the first AgentCash command.** `npx agentcash@0.17.1 balance` creates a
   wallet on this machine (`~/.agentcash/wallet.json`) if there isn't one, so check first:
   `test -f ~/.agentcash/wallet.json`. With a wallet, `balance` shows your USDC (Base and Tempo);
   if it is too low, stop and ask your user to fund it (`npx agentcash@0.17.1 fund` opens the
   funding page). Never pay beyond the budget your user approved.
2. `npx agentcash@0.17.1 check https://inferrail-cost-gateway.onrender.com/read/v1/page`
   returns the exact request schema and price.
3. Pay and get the result (`--max-amount` caps what one call may cost):

```bash
npx agentcash@0.17.1 fetch https://inferrail-cost-gateway.onrender.com/read/v1/page -m POST \
  -H "Content-Type: application/json" -H "X-Inferrail-Source: skill" \
  -b '{"url": "https://example.com/", "request_id": "<unique id>"}' --max-amount 0.01
```

**Who you pay.** Web Read receives payments at `0xA45140E99E9482a50BC3fA5F6000c02FAAB6F65E` (x402, USDC on Base `eip155:8453`) and at the same address over MPP on Tempo (chain 4217). If your wallet allowlists payees, add the one for the rail you use; refuse an offer to any other address.

`X-Inferrail-Source: skill` is optional and says only that the call came from this skill (no
identity). To list every Inferrail service in your agent's paid tools once, run
`npx agentcash@0.17.1 add https://inferrail-cost-gateway.onrender.com`.

## In code you're writing with the Vercel AI SDK

If you're building an agent with the Vercel AI SDK and it needs this, add the tools instead
of hand-writing the HTTP and payment calls: `npm i @inferrail/ai-sdk-tools ai zod`, then
`tools: inferrailTools({ fetch })`, where `fetch` is the app's x402-paying fetch (for example
`wrapFetchWithPayment` from `@x402/fetch`). The package holds no wallet or funds. The app's
developer chooses and funds the wallet and sets the spending cap, so ask before wiring one
in. Examples: https://github.com/domondi1/inferrail/tree/main/examples/ai_sdk

## As an MCP tool

- Server: `https://inferrail-cost-gateway.onrender.com/read/mcp/` (MCP streamable HTTP).
  Official MCP Registry name: `io.github.domondi1/inferrail-web-read`.
- Tool: `read_page(url, request_id?)`.
- Call it without payment: the result is an x402 PaymentRequired. Pay with an x402 MCP client
  (for example the x402 SDK's `x402MCPSession`), which repeats the call with the payment in
  `_meta["x402/payment"]`. The page comes back with the payment response.

## Over HTTP

1. `POST https://inferrail-cost-gateway.onrender.com/read/v1/page` with
   `{"url": "https://...", "request_id": "<unique id>"}`.
2. The answer is HTTP 402. Check the offer before you sign: x402 exact, 2000 units
   ($0.002) of USDC on Base (`eip155:8453`). The same 402 also offers MPP on Tempo.
3. Sign and repeat the request (x402: `PAYMENT-SIGNATURE` header; MPP:
   `Authorization: Payment`). HTTP 200 is the page and its receipt.

A ready, tested buyer: `examples/web_read/buy_page.py` in
https://github.com/domondi1/inferrail. It pays from `EVM_PRIVATE_KEY`, refuses any offer
above `--max-usd` before signing, and retries a lost response safely.

From Node with an x402 client you already use (`@x402/fetch`):
`examples/web_read/typescript/web-read.ts` in the same repository. Pass it your
`wrapFetchWithPayment(fetch, client)`; it never sees a key. `guardWebReadPrice(client)` makes
your client refuse a Web Read offer above $0.002 or to another address before signing, and
`readPage(paidFetch, url)` sends a request_id and retries a lost response with it.

A Coinbase agentic wallet pays x402 too; we haven't tested that one with this endpoint.

## Several pages in one call

`POST https://inferrail-cost-gateway.onrender.com/read/v1/pages` reads 1 to 10 pages in one paid
request: `{"urls": ["https://...", "https://..."], "request_id": "<unique id>"}` (with AgentCash:
the same `fetch` command with this URL and body, and `--max-amount 0.03`).

- Use it when a task already has its list of sources (research, citation checks, comparing
  docs); use `/read/v1/page` for one page, or when you decide the next URL from the last one.
- Price: $0.002 per page, one payment for the batch (3 URLs: $0.006; 10 URLs: $0.02). Check that
  the 402's amount is 2000 units (USDC) times the number of URLs before you sign.
- All or nothing: if any page can't be read, nothing is charged and no page is returned. The
  answer (`error: pages_failed`) has `results`, one per URL, with `delivered` and, for each
  failure, `error`. Send the batch again with only the delivered URLs and a new `request_id`.
- A lost response: send the same `urls` in the same order with the same `request_id` from the
  same wallet within 10 minutes; you get the paid batch and are not charged again.
- No duplicate URLs and no more than 10: such a request gets 422 before any payment offer.

## What a delivered page contains

`title`, `content_markdown`, `word_count`, `content_sha256`, `final_url`, and `metadata`:
`description`, `canonical_url`, `authors`, `published_at`, `modified_at` (ISO 8601, as the page
wrote it), `language`, `site_name`, `image` and `type`. Each is exactly what the page declares
(meta tags, Open Graph, JSON-LD); a field the page doesn't declare is `null` (`authors: []`),
never guessed. Cite `canonical_url` and `published_at` when you quote a source.

## Rules that keep you from paying twice

- Always send a `request_id`. If a response is lost, send the same url and request_id
  again from the same wallet within 10 minutes: you get the paid page and the new
  signature isn't settled.
- Refused or failing pages cost nothing: 422 (unsupported or private address,
  robots.txt, non-text, over 2 MB, the site answered 4xx, the site served a bot check
  (`bot_check`), or the page has no text without JavaScript (`no_readable_content`);
  retrying won't help);
  502 or 504 (the site failed or timed out; may work later).
- Guide: https://inferrail-cost-gateway.onrender.com/read/llms.txt. Contract:
  https://inferrail-cost-gateway.onrender.com/openapi.json.
