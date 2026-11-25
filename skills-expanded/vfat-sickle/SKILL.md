---
name: vfat-sickle
description: "Use when reviewing a VFAT farm or Sickle-held position, comparing harvest, compound and exit costs, or checking automation and strategy permissions."
license: MIT
compatibility: "Read-only protocol APIs or RPC through existing configured tools. No signer included."
metadata:
  author: "Galleon Labs"
  version: "0.7.1"
---

# VFAT Sickle

Produce a farm decision or Sickle inventory with explicit custody, fee bases and exit steps. VFAT yield browsing does not require a wallet connection; a Sickle is a distinct onchain account, not the user's EOA.

## Read farm and ownership evidence

Collect chain, farm/pool, public owner and intended research or maintenance action. Start from VFAT's public farm/portfolio pages and the current deployed contracts linked by official documentation. Resolve the owner's Sickle for that chain, its factory and strategy registry; verify actual ownership and supported targets through deployed verified ABIs. A position in the Sickle can exist while the EOA shows no LP tokens.

Separate LP principal, farm receipt/gauge balance, unclaimed rewards and any automation permissions. Identify the strategy and external pool/gauge actually holding assets. No supported public VFAT quote API or execution MCP was established by this review; do not invent `vfat_*` tool calls or treat an unverified npm wrapper as a supported integration.

## Compare the real economics

Keep fee APR and reward APR separate. VFAT's documented fee APR uses trailing seven-day fees; it is a historical estimate, not the next week's return. Emissions depend on the current gauge/epoch and can be zero even when an old page shows rewards. Re-read relevant protocol announcements and chain rates.

For harvest, compound, rebalance or exit, list the exact route and each charge's base: rewards, withdrawn principal or entire position. Include swap slippage, pool fees, automation charges and gas. Do not subtract a principal-based rebalance fee as though it applied only to rewards. Fixed rates in the documentation are review evidence; inspect the current route before preparing a user action.

## Plan without adding authority

A deposit can deploy a Sickle and transfer assets; automation enrollment can authorize future actions. Display these effects as distinct decisions. Use the chosen official UI or verified contract builder for unsigned preparation. Inspect every batched target, spender, recipient and native value, including strategy-registry support. Never enroll automation merely because the user asked for a yield comparison.

For an existing exit, track any unstake, withdraw, swap and reward stages. Completion needs receipts and Sickle/EOA balances agreeing with the requested output; successful harvest does not prove principal exited. On unsupported strategy, missing owner evidence, stale farm data or ambiguous send, return the unresolved state and reconcile existing hashes before another action.

## Worked result

Synthetic farm: $10,000 principal and $100 rewards. A route charges 0.9% of rewards to compound, while a selected rebalance charges 0.03% of the position. Those bases yield $0.90 and $3 respectively before swap/gas costs. A displayed 24% historical fee APR does not establish $2,400 future earnings. Return separate costs and leave automation disabled for a research-only request.

## Sources and limits

Primary documentation and source reviewed 2026-10-25; no account authorization, signing or financial action was tested. [Read recipes and current primary sources](references/reads.md) ship with this skill. Recheck supported deployments and schemas before a consequential handoff. Research adds no permission to trade, transfer, vote or change account authority.
