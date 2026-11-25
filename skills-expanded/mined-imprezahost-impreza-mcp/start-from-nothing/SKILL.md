---
name: start-from-nothing
description: Go from no Impreza account at all to a running app — anonymous sign-up with no e-mail, a server the customer already has (the first one is free), or funding in Bitcoin or Monero for an Impreza VPS. Use when someone has no account, no server, or asks what buying hosting here involves.
---

# From nothing to a running app

Most hosting integrations assume an account and an API key already exist. This
one does not have to. The whole arc can start from zero.

## The account

An Impreza account can be created **without an e-mail address and without KYC**.
When you reach the hosted server with no credentials at all, it offers
`impreza_bootstrap_account` and a few reads of public information — docs
search, the VPS offer and quote, products, apps, manifest check, domain
availability and prices. That is the lobby: an anonymous caller can look
around, and the only thing it can create is the account. The domain tools are
limited per visitor and per day.

Two consequences worth stating plainly:

- Once you are authenticated, that tool is **not in your list any more**. If
  you are looking for it on a connected account, it is gone by design, not
  missing.
- The account comes back with a **recovery code**, and there is no e-mail to
  fall back on. If the customer loses it, we cannot restore the account for
  them — that is what "no e-mail" actually costs. Say this at the moment the
  code appears, not later.

## A server they already have costs nothing

Ask first whether the customer already has a server — any Linux machine with
root access and outbound HTTPS, at any provider. If they do, nothing has to be
bought: **the first external server is free on every account**, with no plan
and no balance.

`impreza_add_server` returns a one-line install command and its one-time token,
valid for 10 minutes. The customer runs it as root on that server (or you do,
over access they gave you for that server). Then `impreza_list_servers` shows it
online and the `deploy-an-app` skill takes over.

- The token is shown once. If it is lost or expires, call the tool again; an
  unused token holds the free slot until it expires.
- More servers: any active Impreza VPS moves the account to Bundled (5
  external servers). Say so only when the customer asks for a second one.
- Without a paid service, a hostname on the platform domain is not available:
  deploy with a domain the customer owns, or onion-only. Apps keep the Shield on.

## The money, and what you can and cannot do with it

**You cannot spend the customer's money from this conversation.** Tools that
would buy something — ordering a VPS, upgrading or resizing one, paying an
invoice, registering or transferring a domain, buying WHOIS privacy — hand back
a **checkout link** instead of charging. The customer completes the purchase on
our page.

This is deliberate, and it is not a limitation to apologise for or try to route
around. Do not look for another tool that "really" buys. There isn't one, and
the connector attests to Anthropic that it does not execute financial
transactions on a user's behalf.

What still works in chat is **funding**, because it moves no money by itself:

- `impreza_topup` raises a funding invoice for an amount.
- `impreza_topup_payment` shows the crypto address the customer sends from, by
  hand, out of their own wallet.
- `impreza_topup_status` says whether it arrived.

Bitcoin and Monero. Nothing is debited from anyone by a tool call; the customer
pushes the payment themselves.

## Then the server

`impreza_list_products` is the catalogue. It is large, so narrow it: pass
`group` for a product group or `type` for a kind, rather than reading all of it
back to the customer.

`impreza_order_vps` produces the checkout link. After the customer pays, the
VPS provisions on its own — `impreza_list_servers` will show it. Provisioning
takes minutes, not seconds; do not report a server that is not there yet.

## Then the app

The `deploy-an-app` skill takes it from there.

## Being honest about the trade

People choose this host for privacy, and the honest version of that includes
the parts that are not flattering. If a customer is deciding, these are true and
they should hear them:

- The clearnet API and MCP hosts sit behind Cloudflare, which terminates TLS.
  Both also provide onion endpoints: the [hosted MCP connector](http://mcp.imprezareshna326gqgmbdzwmnad2wnjmeowh45bs2buxarh5qummjad.onion/mcp)
  and the [API](http://api.imprezareshna326gqgmbdzwmnad2wnjmeowh45bs2buxarh5qummjad.onion).
  Hosted OAuth needs a client that can reach the endpoint through Tor and
  validate its issuer. The local MCP uses API-key credentials and an explicit
  SOCKS5 proxy with the onion API. Follow the [connection guide](https://docs.imprezahost.com/connect-mcp.html).
- The caller's IP is recorded on every API call.
- Prepared deployment configurations encrypt environment values at rest;
  their review summaries return variable names only. This protects the saved
  configuration, not the running application's own environment.
- `impreza_privacy_report` is not marketing: it **measures** what the account
  actually holds, table by table, and reports whether our own retention windows
  are being honoured. If someone asks what is kept about them, call it rather
  than summarising from memory.
