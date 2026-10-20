---
name: jb-well-known-projects
description: |
  Canonical Juicebox V6 project IDs and names. Use when: (1) user asks about NANA,
  Croptop, REV, Banny, Defifa, Artizen, Markee, or other well-known projects,
  (2) need to look up a popular project, (3) user mentions a token symbol like
  $REV, $NANA, $BAN. CRITICAL: these are THE canonical ecosystem projects with
  fixed, deploy-time project IDs — same ID on every chain. Look up by ID; never
  search by name first.
author: Claude Code
version: 6.0.0
date: 2026-07-09
---

# Juicebox V6 Well-Known Projects

The canonical projects are created by the V6 deployment itself, so their project IDs
are constants (source: `deploy-all-v6/script/Deploy.s.sol`), identical on every
supported chain (Ethereum, Optimism, Base, Arbitrum + their Sepolia testnets).

## CRITICAL — Memorize these

| Project ID | Name | Token | Notes |
|-----------:|------|-------|-------|
| **1** | NANA / Bananapus | $NANA | The fee project — all protocol fees route here. |
| **2** | Croptop | $CPN | Croptop publisher network. |
| **3** | Revnet Network | $REV | THE canonical revnet. |
| **4** | Banny Retail | $BAN | Banny NFT project (721 hook). |
| **5** | Defifa | $DEFIFA | Defifa revnet. |
| **6** | Artizen | $ART | |
| **7** | Markee | $MARKEE | |
| TODO | Juicy Vision | $JUICY | This app's project. TODO(v6): fill in project ID once $JUICY is redeployed on V6. |

Per-project ERC-20 token addresses: `deploy-all-v6/deployments/<chain>/JBERC20__Project<NAME>.json`.

## Query strategy

1. User mentions a well-known name or token symbol → query the fixed project ID directly.
2. Same ID works on ALL chains — never ask "which chain?".
3. Bendystraw queries must filter `version: 6`.
4. Don't search by name first — use the known ID.

## Anti-pattern: what NOT to do

❌ "Let me search for the Revnet Network project..."
❌ "Which chain is REV on?"
❌ Guessing project IDs.

## Correct pattern

✅ "REV is project 3. Fetching its current state from [chain]..."
✅ "NANA is project 1 on all chains. Here's the treasury balance..."
