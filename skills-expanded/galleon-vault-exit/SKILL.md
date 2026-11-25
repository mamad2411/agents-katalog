---
name: galleon-vault-exit
description: "Use when checking how much can leave an ERC4626 vault, reconciling pending and claimable ERC7540 redemptions, or choosing withdraw versus redeem under liquidity and fee constraints."
license: MIT
compatibility: "Read-only EVM RPC or official provider tools; Node.js 20+ for the optional offline assessment. No signer required."
metadata:
  version: "0.4.1"
  author: "Andrew Wilkinson and Galleon Labs"
  source: "https://github.com/galleonlabs/crypto-defi-skills"
---

# Vault exit assessment

Answer how much of the requested exit fits the observed limit, what remains, and which read would resolve an uncertainty. Produce an exit feasibility record with amounts and units. A snapshot is historical evidence; refresh it before calling any amount available now.

## Resolve the exit interface and identities

Resolve chain, vault entry point, implementation, underlying asset, share token, owner, controller, receiver and caller. Keep token addresses and decimals separate. For ordinary ERC4626 the vault is the share token; for ERC7575 and ERC7540 read `share()` and query the returned token for balance and decimals. A zero balance at the vault address is not proof that external shares are missing.

Identify the **redemption** interface from verified implementation documentation and interface reads. An instant deposit can still have an asynchronous redemption. ERC7540 redemption support uses `supportsInterface(0x620ee8e4)`; inspect ERC165 and ERC7575 support too. A false or reverted interface call does not prove synchronous ERC4626 behavior. If unresolved, return the missing implementation/interface evidence before choosing a method.

Read [protocol recipes](references/recipe.md) for the selected interface. Use one block number and hash for all observations, including previews and request state. Collect previews with the intended vault caller; caller-dependent fees can change their result, and a router may be that caller. Identify whose account each limit describes: the owner for synchronous exits, the controller for asynchronous claims.

## Synchronous redemption

Collect `asset()`, share and asset decimals, `balanceOf(owner)`, `maxWithdraw(owner)` and `maxRedeem(owner)`. Read total assets/supply, pause state, fees and strategy liquidity when needed to explain the limit. Total assets or a token balance alone cannot replace the owner-specific limit.

- For exact assets, compare the request with `maxWithdraw`, then call `previewWithdraw` for the candidate amount and compare required shares with ownership.
- For exact shares, compare the request with `maxRedeem` and ownership, then call `previewRedeem` for the candidate amount.
- If a partial amount is the only supported portion, obtain a preview for that exact partial amount. Never scale a full-exit preview: fees and rounding can be nonlinear.

Previews include exit fees but ignore withdrawal limits. `convertToAssets` is an idealized conversion, not an executable quote. Keep a missing or reverted preview unknown; preserve the observed limit and explain the exact next read.

## Asynchronous redemption and reconciliation

Resolve the request controller separately from the original share owner. Read controller-wide `maxWithdraw(controller)` and `maxRedeem(controller)`. Obtain request IDs from verified receipts/events or the official implementation's request inventory, then read `pendingRedeemRequest(requestId, controller)` and `claimableRedeemRequest(requestId, controller)`.

Keep three observations separate: **wallet shares**, **pending shares**, and **claimable shares**. Requested shares may already be escrowed or burned, so wallet balance does not cap a controller's claim. Do not convert pending shares to guaranteed assets or assume an ETA or yield accrual. Asynchronous redemption previews are specified to revert; do not call them to price a claim or label the shares worthless.

Request identity includes chain, vault, controller and request ID. ID zero is an aggregate: read it once, not once per historical request transaction. Distinct nonzero IDs may fulfill at different rates and times. State whether the inventory is complete, partial or unknown. Controller-wide exit limits cannot be attributed to one selected request. Partial inventory does not erase a supplied controller limit, but it cannot establish all outstanding requests.

Choose the next step from the evidence:

| Observation | Useful result and next step |
| --- | --- |
| Positive controller limit | Report the supported claim portion in the requested unit; prepare a simulation of `withdraw` or `redeem` using the actual controller/caller/receiver. Asset proceeds for an exact-share claim need implementation-specific evidence or simulation. |
| Pending shares, zero claim limit | Report the pending share amount; re-read fulfillment state according to the vault's documented process. A successful request is not delivery. |
| Zero pending and claimable | Reconcile request inventory, controller, receipts and receiver balance before inferring anything was claimed. Zero state alone does not prove settlement. |
| Request exceeds current claim limit | Report the remainder in the original unit. Reconcile existing requests before proposing another `requestRedeem`; do not duplicate a pending request. |
| Unrequested wallet shares remain | A new `requestRedeem(shares, controller, owner)` is a separate operation requiring its own bounds, authority and simulation. No generic `requestWithdraw(assets)` or universal `claim()` exists. |

## Optional reproducible assessment

Use the dependency-free [offline helper](scripts/assess-exit.mjs) when exact arithmetic, incomplete request coverage or repeated observations make the decision harder to inspect. Read the [observation contract and examples](references/assessment.md), then run from this skill directory:

```sh
node scripts/assess-exit.mjs examples/async-partial.json
node scripts/assess-exit.mjs examples/sync-partial.json
```

Replace the synthetic inputs with actual same-block reads to assess a real snapshot. The helper only compares supplied values, uses raw integer strings, and has no provider, credential or signing access. It returns an observed limit, partial remainder, indicative method, request coverage and next reads. It does not prove current liquidity, authorize a partial exit or simulate a call. Conflicting block evidence produces no candidate.

## Preparation and completion

For an authorized write, prepare the complete unsigned sequence using maintained official tools and simulate with actual sender, receiver, account roles, allowances and amount. Direct owner ERC4626 redemption generally needs no underlying-token approval; delegated share spending and ERC7540 operator permissions are different contracts. Verify the deployed rules. Never add a broad approval to repair an unexplained revert.

Standard exit calls have no `maxShares` or `minAssets` arguments. Use a documented router or supported guard when a user requires slippage protection. Do not invent signature arguments, cancellation support or request-ID claim selection. Preserve existing authorization; a read-only assessment grants no signing or spending authority, and a partial amount is not approval to execute it.

Return an answer-first record: requested amount, supported portion and remainder with units; chain/vault/asset/share identities; owner/controller/receiver; block number/hash; request inventory coverage; gaps and next read. Separate observations, estimates, simulation and confirmed receipt evidence.

After authorized execution, reconcile the transaction identity, receipt/events, share or request-state change, and the receiver's actual underlying balance change. A request-to-claim transition alone is not a received balance. On an ambiguous timeout, reconcile hash/nonce and request state before retrying. Preserve fees, losses and remaining exposure.

Sources checked 2026-10-10. This directory, including references, examples and helper, is independently installable.
