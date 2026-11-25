---
name: rein
description: Add spend control to an AI agent that pays for things — budgets, per-transaction caps, kill switches, human approval for large payments, and an audit log of every payment decision. Use when working with x402, HTTP 402 paywalls, agent payments, pay-per-call APIs, agent wallets, or any code where an autonomous agent can spend money; when asked to cap, budget, govern, approve, or audit what an agent spends; or when integrating @reinconsole/* packages.
---

# Rein — spend control for agents that pay

Rein governs an agent's authority to spend. It is **non-custodial**: funds never pass through it.
An agent's payment is checked against a declarative policy *before the payment is constructed*, so a
denial means nothing was signed, sent, or refunded.

MIT, Node >= 22, published on npm under `@reinconsole`.

## Choose the integration

**The agent runs in an MCP-capable harness** (Claude Code, Codex-class agents) → use the MCP
server. No code changes; the agent gets a governed `fetch` as a tool.

**The agent is a program you control** → use the SDK. One wrapper around its `fetch`.

**You are building the API that charges** → that is the Gate side, `@reinconsole/gate`. Different
package, same engine.

Either way, a **policy engine** must be running. It is the referee holding agents, policies, and a
hash-chained signed decision log:

```
npx -p @reinconsole/policy-engine rein-policy-engine   # http://127.0.0.1:8787
```

Unkeyed it binds loopback only; a public bind without an API key is a startup error by design. For
anything non-local, issue a scoped key and pass `apiKey` / `REIN_ENGINE_API_KEY`.

Or use the hosted engine at `https://engine.reinconsole.com` (invited beta). An invitee's key is
scoped to one org and narrowed to one agent: it can submit that agent's payments and nothing else.
`vendor.reinconsole.com/testnet/v1/ping` is a real $0.001 paywall to try it against.

## MCP integration

```json
{
  "mcpServers": {
    "rein": {
      "command": "npx",
      "args": ["-y", "@reinconsole/mcp"],
      "env": {
        "REIN_ENGINE_URL": "http://127.0.0.1:8787",
        "REIN_AGENT_ID": "agt_01J...",
        "REIN_NETWORK_PROFILE": "testnet"
      }
    }
  }
}
```

Omit `REIN_PAYER_PRIVATE_KEY` and the server runs in **advisory mode**: policy is checked and
reported, nothing is paid. That is the right default when demonstrating or testing — a wallet key
should be handed over deliberately, never acquired by installing a server.

`REIN_NETWORK_PROFILE` is `testnet` or `mainnet` (default `testnet`); an unknown value refuses to
boot rather than falling back. The server prints one line to stderr when it is up, and a harness
that shows nothing else will show this:

```
[rein-mcp] 0.2.0 ready on stdio for agt_01J... via https://engine.reinconsole.com (advisory -- no payer configured)
```

Tools: `rein_fetch` (the only one that can move money), `rein_status`, `rein_receipts`,
`rein_escalations`, `rein_heartbeat`.

## SDK integration

```js
import { createGuard, PaymentBlockedError } from '@reinconsole/sdk';

const guard = createGuard({
  engineUrl: 'http://127.0.0.1:8787',
  agentId,                   // from client.registerAgent(...)
  payer,                     // omit for advisory mode: evaluate, never pay
});

const fetch = guard.wrap();  // this is the whole integration
```

`guard.wrap()` returns a fetch-compatible function. Every x402 paywall behind it is evaluated
first. A block throws `PaymentBlockedError` carrying `intent`, `decision`, `receipt`, and (for an
escalation) `approval`. Pass `onBlocked: 'respond'` to get a synthetic 402 response instead, for
agent loops that prefer inspecting responses to catching.

Register the agent and its rules through `EngineClient`:

```js
import { newId } from '@reinconsole/core';
import { EngineClient } from '@reinconsole/sdk';

const client = new EngineClient({ baseUrl: 'http://127.0.0.1:8787' });
const agent = await client.registerAgent({
  orgId: newId('org'),
  name: 'research-agent',
  labels: ['research'],
  wallets: [{ chain: 'base', address: '0x...', mode: 'sdk' }],
});
await client.addPolicy({ /* see below */ });
```

## Writing a policy

```js
{
  policyId: 'research-policy',
  appliesTo: { agents: ['agt_01J...'] },   // or { labels: ['research'] }, or { chains: ['base'] }
  rules: [
    { id: 'tx-cap',       deny:     { amountGt: '0.50' } },
    { id: 'hour-budget',  deny:     { rollingSum: { window: '1h', gt: '2.00' } } },
    { id: 'new-vendor',   escalate: { vendorFirstSeen: true } },
    { id: 'trusted',      allow:    { vendorHostIn: ['*.trusted-data.io'] } },
  ],
  breakers: [{ id: 'velocity', window: '24h', txCount: 50, valueCap: '20.00' }],
  default: 'deny',
}
```

Each rule carries **exactly one** of `allow` / `deny` / `escalate`. Precedence is
**deny > escalate > allow > default**, and policies are first-applicable by `appliesTo`.

Conditions: `amountGt`, `rollingSum: { window, gt }`, `txCount: { window, gt }`, `vendorHostIn`,
`resourceIn`, `vendorFirstSeen`, `vendorReputationLt`, `amountVsResourceMedian: { gt }`,
`taskBudget: { gt }`, `taskIdMissing`.

Amounts are decimal **strings** (`'0.50'`), not numbers. Windows are duration strings (`'1h'`,
`'24h'`, `'7d'`).

## Rules for getting this right

**Default to `deny` in production.** `default: 'allow'` is a demo convenience. A policy whose
default allows is a policy that governs only what you remembered to forbid.

**`resourceIn` matches PATHS, not full URLs.** Write `'/v1/reports/*'`, not
`'https://api.x.com/v1/reports/*'`. Scope it to a vendor by pairing it with `vendorHostIn`.

**A breaker escalates; it never denies.** Breakers are a rolling envelope (`txCount` and/or
`valueCap` over a window) that trips on the payment which *would* carry the agent past it —
prospective, never retrospective. `txCount: 10` permits ten and escalates the eleventh. An explicit
deny still wins over a tripped breaker, and no allow rule can wave one past. Use a `deny` rule when
you mean a hard cap.

**An escalation is not a denial, and the agent cannot resolve its own.** `escalate` parks the
payment for a human, who releases it with an ed25519 signature over `decisionId + intentHash` by a
registered approver key. A parked request has a TTL and expires into a deny. Never build a
click-to-approve path, an "approve" tool, or an endpoint that releases a payment on anything less
than that signature — the delivery channel is transport, never authority.

**Attribute spend to a task, or per-task budgets cannot fire.** Use `guard.withTask({ taskId }, fn)`
(or `rein_fetch`'s `taskId`) for every payment belonging to one job. An intent with no `taskId`
never triggers a `taskBudget` — that is deliberate, since unattributed spend cannot be charged to a
task. To *require* attribution, add the separate `taskIdMissing` predicate.

**Do not catch `PaymentBlockedError` and retry the same request.** A deny is final and will be
denied identically. Retrying is how a runaway loop turns one refusal into a thousand.

**Do not treat a settlement report as authorization.** Reporting that a payment settled is
telemetry; it can never allow anything, and a failed report must never break a payment that already
succeeded.

**Never persist a private key through Rein, and never log one.** The guard's payer takes either a
raw key (local custody) or an injected account — `createX402Payer({ account })` accepts anything
with `address` + `signTypedData`, so a viem `toAccount` bridges CDP, Privy, or Turnkey and the key
stays with the provider.

**A testnet-profile key never pays mainnet, and no policy can make that promise.** The engine maps
Base and Base Sepolia onto one chain, so `vendorHostIn`, `amountGt` and the rest see no difference
between a $0.001 testnet quote and a $0.001 mainnet one. The boundary lives in the guard and the
payer: `REIN_NETWORK_PROFILE` for MCP, `networks: ['base-sepolia']` for `createGuard`, and the
`profile` passed to `createX402Payer`. Set it explicitly in anything that could touch real money,
never widen it to both networks in one process, and give a mainnet payer its own key and treasury.

## Testing an integration offline

`@reinconsole/mock-rails` is a full simulated x402 world — ledger, facilitator, paywalled vendor —
so the entire stack runs with no accounts, chain, or funds:

```js
import { MockLedger, MockFacilitator, createMockVendor } from '@reinconsole/mock-rails';

const ledger = new MockLedger();
const facilitator = new MockFacilitator({ ledger, name: 'mock-facilitator' });
const vendor = createMockVendor({ facilitator, atomicPrice: '10000', payTo: '0xVendorTreasury' });

const guard = createGuard({
  engineUrl, agentId,
  fetch: vendor.fetch,                  // swap for globalThis.fetch against real vendors
  payer: facilitator.payerFor(wallet),
});
```

Assert on the *decision*, not just the HTTP outcome: `guard.receipts()` carries every decision this
guard made, allowed or not.

## Packages

| Package | Use it for |
|---|---|
| `@reinconsole/mcp` | The guard as an MCP server — a governed fetch for any MCP harness. |
| `@reinconsole/sdk` | The guard: wrap an agent's fetch. `createGuard`, `EngineClient`. |
| `@reinconsole/policy-engine` | The engine. Embeddable (`PolicyEngine`) or standalone (`rein-policy-engine`). |
| `@reinconsole/core` | Schemas for every shape. Validate at boundaries; never redefine them. |
| `@reinconsole/gate` | The vendor side: price an API per call over x402. |
| `@reinconsole/graph` | Reputation from an append-only evidence ledger. |
| `@reinconsole/mock-rails` | Offline x402 world for tests and demos. |
| `@reinconsole/x402-rails` | Real rails on Base Sepolia: EIP-3009 payer, facilitator, indexer. |
| `@reinconsole/erc8004` | On-chain agent identity per ERC-8004. |

## More

- Machine-readable index: <https://reinconsole.com/llms.txt>
- Executable quickstart: <https://reinconsole.com/agent-quickstart.md>
- Live console: <https://app.reinconsole.com>
