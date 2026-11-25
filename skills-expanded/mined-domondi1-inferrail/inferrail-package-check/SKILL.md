---
name: inferrail-package-check
description: Check package versions for known vulnerabilities before you add, upgrade, pin or ship a dependency, paying $0.002 per check of up to 20 packages from a wallet your agent already has (AgentCash or any x402/MPP client). Use when a coding or build task adds or changes npm, PyPI, Go, crates.io, Maven, NuGet, RubyGems or Packagist dependencies; returns advisory ids, CVEs, severity, fixed versions and links from OSV.dev, and an OSV outage is never charged.
---

# Inferrail Package Check

Known vulnerabilities for the exact package versions you are about to use, from OSV.dev. One call
checks up to 20 packages for $0.002. You pay only for a delivered check, and a retry with the
same `request_id` never pays twice.

## When to call it

- Before adding a dependency, or bumping one to a new version.
- Before shipping a lockfile change or a release.
- When a user asks "is this version safe?" or "which version fixes this CVE?".

Batch the packages you are changing into one call (up to 20).

## When another tool is better

If you can run the ecosystem's own free audit in the project (`npm audit`, `pip-audit`,
`cargo audit`, `govulncheck`), and it works, use it. Package Check is worth paying for when you
can't: checking versions **before** they are installed or without the project's environment,
in a sandbox without registry access, or across several ecosystems in one call, with every
advisory's source, licence and fixed versions in one JSON answer.

## Paying from your agent (AgentCash wallet)

The simplest path for a coding or research agent, with no API key and no account:

1. **Ask your user before the first AgentCash command.** `npx agentcash@0.17.1 balance` creates a
   wallet on this machine (`~/.agentcash/wallet.json`) if there isn't one, so check first:
   `test -f ~/.agentcash/wallet.json`. With a wallet, `balance` shows your USDC (Base and Tempo);
   if it is too low, stop and ask your user to fund it (`npx agentcash@0.17.1 fund` opens the
   funding page). Never pay beyond the budget your user approved.
2. `npx agentcash@0.17.1 check https://inferrail-cost-gateway.onrender.com/pkg/v1/check`
   returns the exact request schema and price.
3. Pay and get the result (`--max-amount` caps what one call may cost):

```bash
npx agentcash@0.17.1 fetch https://inferrail-cost-gateway.onrender.com/pkg/v1/check -m POST \
  -H "Content-Type: application/json" -H "X-Inferrail-Source: skill" \
  -b '{"packages": [{"ecosystem": "npm", "name": "lodash", "version": "4.17.15"}],
       "request_id": "<unique id>"}' \
  --max-amount 0.01
```

**Who you pay.** Package Check receives payments at `0xe9c1249648257C1C1D70F8b7682851C377bb8f53` (x402, USDC on Base `eip155:8453`) and at `0xA45140E99E9482a50BC3fA5F6000c02FAAB6F65E` over MPP on Tempo (chain 4217), Inferrail's shared Tempo address. If your wallet allowlists payees, add the one for the rail you use; refuse an offer to any other address.

`X-Inferrail-Source: skill` is optional and says only that the call came from this skill (no
identity). To list every Inferrail service in your agent's paid tools once, run
`npx agentcash@0.17.1 add https://inferrail-cost-gateway.onrender.com`.

## How to call it

`POST https://inferrail-cost-gateway.onrender.com/pkg/v1/check` with

```json
{"packages": [{"ecosystem": "npm", "name": "lodash", "version": "4.17.15"}],
 "request_id": "<unique id>"}
```

Ecosystems: `npm`, `PyPI`, `Go`, `crates.io`, `Maven`, `NuGet`, `RubyGems`, `Packagist`, `Hex`,
`Pub`, `Hackage`, `CRAN`, `SwiftURL`.

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

## In CI

To check a project's lockfiles on every push or pull request (and fail the build on a known
vulnerability), add the `domondi1/inferrail/actions/package-check` step, pinned to a reviewed commit, with
a wallet secret and a required `max-usd` limit; see `actions/package-check/README.md` in
https://github.com/domondi1/inferrail. Ask your user before adding a paid step to their CI.

## Reading the answer

Each result has a `status`:

- `vulnerable`: `vulns` lists each advisory with `id`, `aliases` (CVE), `summary`, `severity`,
  `fixed` (versions that fix it) and `url`. Upgrade to a version in `fixed`.
- `no_known_vulnerabilities`: OSV.dev had no matching advisory when checked. **This is not a
  guarantee that the package is secure.**
- `incomplete` (`complete: false`): OSV didn't return the whole list; treat it as unchecked.

Each advisory carries its source `database` and `license` (mostly CC-BY 4.0): keep the link and
source when you show results to a user.

## Never charged

- 502 `upstream_failed`: OSV.dev was unreachable. Retry later.
- 422: invalid request (unknown ecosystem, empty list or more than 20 packages).

Guide: https://inferrail-cost-gateway.onrender.com/pkg/llms.txt. Contract:
https://inferrail-cost-gateway.onrender.com/openapi.json.
