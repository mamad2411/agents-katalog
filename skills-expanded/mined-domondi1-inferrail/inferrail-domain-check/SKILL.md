---
name: inferrail-domain-check
description: Look up a domain's DNS records (A, AAAA, CNAME, MX, NS, TXT, SOA, CAA), SPF and DMARC email policies, and registration (registrar, status, created and expiry dates, domain age, nameservers, DNSSEC) for $0.002 per lookup, paid from a wallet your agent already has (AgentCash or any MPP or x402 client). Use before trusting a link, sender or counterparty, when setting up or debugging DNS or email, or when checking who registered a name and when; a resolver outage is never charged.
---

# Inferrail Domain Check

One call returns what an agent usually needs to know about a domain: its live DNS records, its
email authentication (SPF, DMARC policy, MX count) and its registration record from the
registry's RDAP service. It costs $0.002. You pay only for a delivered lookup, and a retry with
the same `request_id` never pays twice.

## When to call it

- Before you trust a link, an email sender or a counterparty's website: how old is the domain,
  who is the registrar, when does it expire, does it publish SPF and DMARC?
- When you set up or debug DNS or email delivery (MX, TXT, CAA, nameservers).
- When a user asks who registered a name, or whether it is registered at all.

## When another tool is better

If you have a shell with network access, `dig`, `nslookup` and `whois` are free and fine for a
quick look at one record. Domain Check is worth paying for when you don't, or when you want the
whole picture in one structured answer: every record type, the SPF and DMARC policy, and the
registry's registration data (RDAP) with dates and status, without parsing WHOIS text.

## Paying from your agent (AgentCash wallet)

The simplest path for a coding or research agent, with no API key and no account:

1. **Ask your user before the first AgentCash command.** `npx agentcash@0.17.1 balance` creates a
   wallet on this machine (`~/.agentcash/wallet.json`) if there isn't one, so check first:
   `test -f ~/.agentcash/wallet.json`. With a wallet, `balance` shows your USDC (Base and Tempo);
   if it is too low, stop and ask your user to fund it (`npx agentcash@0.17.1 fund` opens the
   funding page). Never pay beyond the budget your user approved.
2. `npx agentcash@0.17.1 check https://inferrail-cost-gateway.onrender.com/domain/v1/lookup`
   returns the exact request schema and price.
3. Pay and get the result (`--max-amount` caps what one call may cost):

```bash
npx agentcash@0.17.1 fetch https://inferrail-cost-gateway.onrender.com/domain/v1/lookup -m POST \
  -H "Content-Type: application/json" -H "X-Inferrail-Source: skill" \
  -b '{"domain": "example.com", "request_id": "<unique id>"}' --max-amount 0.01
```

**Who you pay.** Domain Check receives payments at `0xb95D56f169324A0B23B82bd3975635Cf0187ce07` (x402, USDC on Base `eip155:8453`) and at `0xA45140E99E9482a50BC3fA5F6000c02FAAB6F65E` over MPP on Tempo (chain 4217), Inferrail's shared Tempo address. If your wallet allowlists payees, add the one for the rail you use; refuse an offer to any other address.

`X-Inferrail-Source: skill` is optional and says only that the call came from this skill (no
identity). To list every Inferrail service in your agent's paid tools once, run
`npx agentcash@0.17.1 add https://inferrail-cost-gateway.onrender.com`.

## How to call it

`POST https://inferrail-cost-gateway.onrender.com/domain/v1/lookup` with

```json
{"domain": "example.com", "request_id": "<unique id>"}
```

Optional: `"records"`: a subset of `A`, `AAAA`, `CNAME`, `MX`, `NS`, `TXT`, `SOA`, `CAA`
(default all), and `"registration": false` to skip the registry lookup. Internationalized names
are accepted and answered in their ASCII (`xn--`) form.

A Coinbase agentic wallet pays x402 too; we haven't tested that one with this endpoint.

Any x402 or MPP client works the same way: the first response is HTTP 402 with both offers
(x402 on Base, MPP on Tempo). Check that the price is 2000 units ($0.002) of USDC before you
sign.

## In code you're writing with the Vercel AI SDK

If you're building an agent with the Vercel AI SDK and it needs this, add the tools instead
of hand-writing the HTTP and payment calls: `npm i @inferrail/ai-sdk-tools ai zod`, then
`tools: inferrailTools({ fetch })`, where `fetch` is the app's x402-paying fetch (for example
`wrapFetchWithPayment` from `@x402/fetch`). The package holds no wallet or funds. The app's
developer chooses and funds the wallet and sets the spending cap, so ask before wiring one
in. Examples: https://github.com/domondi1/inferrail/tree/main/examples/ai_sdk

## Reading the answer

- `resolves`: whether the name has DNS records. `dns.<TYPE>.status` is `ok`, `no_records`,
  `nxdomain` (the name does not exist) or `error` (that query failed).
- `email`: `spf`, `dmarc`, `dmarc_policy` (`none`, `quarantine` or `reject`) and `mx_count`.
- `registration_status`:
  - `ok`: `registration` has `registrar`, `status`, `created`, `expires`, `age_days`,
    `nameservers`, `dnssec` and the registry's `terms_url`.
  - `not_registered`: the registry had no record when checked. This is not a guarantee that
    the name can be registered.
  - `not_covered`: that TLD's registry is not queried. Covered: .com, .net, .org, .ai, .info and
    about 450 more TLDs. **This says nothing about whether the name is registered.**
  - `skipped` (you sent `"registration": false`) or `error` (the registry failed; unknown).
- `complete: false`: some part failed and is marked `error`. It is never shown as empty.

Registrant contacts are never returned. Registry data is for lawful use only: don't use it for
bulk harvesting or unsolicited marketing.

## Never charged

- 502 `upstream_failed`: the DNS resolver was unreachable. Retry later.
- 422: not a valid public domain name (a URL, an IP address, or a private name such as
  `localhost`, `.local` or `.internal`).

Guide: https://inferrail-cost-gateway.onrender.com/domain/llms.txt. Contract:
https://inferrail-cost-gateway.onrender.com/openapi.json.
