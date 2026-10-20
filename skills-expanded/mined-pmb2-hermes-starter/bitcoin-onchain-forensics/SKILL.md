---
name: bitcoin-onchain-forensics
description: Investigate Bitcoin transactions, stolen-fund sweeps, wallet vulnerabilities, and address clusters using public Esplora APIs (mempool.space / blockstream.info), ECDSA signature forensics, and weak-key exposure oracles. Use when analyzing a drain/theft, reconstructing an attack's on-chain mechanics, profiling dormant wallets, checking exposed addresses, or building defensive weak-key scanning tooling.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [bitcoin, blockchain, forensics, osint, esplora, on-chain]
    triggers: [bitcoin forensics, on-chain analysis, bitcoin theft, wallet investigation, address clustering, esplora, blockchain tracing]
---

# Bitcoin On-Chain Forensics

Investigate thefts, sweeps, and wallet-vulnerability classes using ONLY public data: Esplora APIs, block explorers, and published exposure datasets. Everything in this skill is defensive research — attribution, exposure checking, victim profiling, and sandboxed simulation on keys you own.

## When to use
- A user shares a Reddit/news claim about a BTC theft or "mystery sweep" — verify on-chain before believing anything
- Reconstruct attack mechanics: how many txs, which blocks, which addresses, fees, consolidation patterns
- Profile victims: dormancy, balance distribution, address types
- Analyze the attacker's signatures (nonce reuse / bias → key recovery)
- Check whether addresses are in the public Ill Bloom exposed-wallet set
- Build tooling to find vulnerable/dormant wallets (defensive, see Scope)

## Core workflow
1. **Anchor on the addresses.** Start from any address in the story; pull `/address/:addr` stats (funded/spent sums, tx_count) and `/address/:addr/utxo`. `chain_stats.funded_txo_sum - spent_txo_sum` = current balance.
2. **Get the full tx list.** `/address/:addr/txs` (50/page, newest first), paginate with `/address/:addr/txs/chain/:last_seen_txid` (last txid of previous page). Collect ALL txs; don't fetch whole blocks — a 6k-tx block needs 265 page calls; an address's own tx list needs ~10.
3. **Reconstruct the sweep.** Filter txs by vout paying the collection address. Group by block. Look for the consolidation tx (many vins, one vout). Check same-block consolidation (attacker consolidates in the same block as the last sweeps).
4. **Signature forensics** (see below) — parse every sig; test R-collision + bias.
5. **Victim census.** For each unique input address in the drain txs, fetch `/address/:addr` stats. tx_count == 2 (one deposit, one theft) = textbook dormant victim. Funding txid is at the **VIN level** (`vin[].txid`), NOT inside `prevout` — fetch those txs to get funding dates and compute dormancy in years.
6. **Cross-check exposure oracles** (Ill Bloom dataset — works offline, see references).
7. **Stand up a fund-movement watchdog** on the attacker's addresses: a script that snapshots balances to a state file and prints ONLY on change; wire it as a `no_agent` cron (empty stdout = silent). Alert the moment the parked loot moves.

## Quick API cheat sheet (mempool.space — verify details in references)
- `/api/block-height/:height` → returns **bare plain-text hash, no JSON quotes** — json.loads fails with "Extra data: line 1 column 2"; accept a 64-hex string.
- `/api/address/:addr/txs/:txid` → **404 on mempool.space**. Use `/txs/chain/:txid`.
- Block txs: `/api/block/:hash/txs/:index` (25/page, offset pagination).
- Rate-limited easily: retry with backoff + disk cache (validate JSON BEFORE caching; self-heal corrupt cache files).
- blockstream.info/api is a compatible fallback but returns 25/page and its `/txs/chain/` walks a different direction — pick one host and stick to it.

## Signature forensics
- P2WPKH: witness = `[der_sig_hex, pubkey_hex]`. Legacy: scriptsig = `<der_sig> <pubkey>`.
- Parse DER: `30 len 02 rlen r 02 slen s`; `lstrip(b"\x00")` on r/s (sign byte).
- **R-collision**: same R in two sigs over different messages → both keys recoverable. Test across ALL txs from the same signer (attacker's sweep + consolidation + dust txs).
- **Nonce bias**: count leading zero nibbles/bytes of R. Expected: P(top nibble 0) = 1/16 (~6.25%), P(top byte 0) ≈ 1/256. Deviations signal weak nonce entropy.
- Clean result (no reuse, uniform R) = RFC6979-grade signer — a real negative finding: attacker is competent, no key recovery via signatures.

## Weak-key vulnerability classes (details in references)
- **Ill Bloom** (Coinspect, Jul 2026): 5 software wallets, weak seed RNG. Exposed set is a PUBLIC dataset at illbloom.org — offline oracle, 29,777 BTC entries (Jul 2026). Software wallets only.
- **Coldcard Mk3** (Jul 30 2026 sweep): firmware 4.0.1–5.0.3 weak seed RNG (serial + clock registers; root cause is a March 2021 build routing seed gen to a SOFTWARE randomizer instead of the chip's hardware RNG). Hardware — NOT in the Ill Bloom set. Distinct population from Ill Bloom; same attack template.
- **Milk Sad** (libbitcoin, timestamp entropy, 2023), **Randstorm** (BitcoinJS 2011–2015) — same class of born-weak keys.
- Attack template: enumerate weak keyspace → derive addresses → match against funded UTXOs → filter by balance threshold → one tx per address (tell: attacker holds individual keys, not seeds) → consolidate to one address same block.

## Multi-wave sweeps: one collector is NOT the whole wave
- The Jul 30 Coldcard sweep evolved into **3 waves** (per Galaxy Research, CoinDesk Aug 1-2 2026): total **1,367.05 BTC / 4,585 addresses / ~$89M**.
  - Wave 1 (Jul 30): 1,083 BTC / 1,196 addr / 41 min, ~1 BTC each, shared collector(s), P2WPKH, 1 victim per tx.
  - Wave 2: ~76 BTC / ~1,477 addr (implied), shared collectors.
  - Wave 3 (Jul 31→Aug 1): ~208 BTC / 1,912 addr, ~0.1 BTC each, **per-victim destination addresses (no shared collector)**, **P2WSH outputs** (multisig/timelock-capable), **~6 victims batched per tx**, default derivation path only.
- **Lesson:** tracking ONE collection address under-captures a wave. Our single-collector dataset (594.48 BTC / ~500 addr) was only ~55% of wave 1 (1,083 BTC / 1,196 addr). When a research firm reports larger totals, hunt the other collectors: scan the sweep blocks for the same fingerprint (single-input txs, ~3,300-sat premium fees, outputs to fresh bc1q addresses).
- **Tradecraft changes across waves signal adaptation** (same operator rebuilt after being mapped, or a copycat grinding the same keyspace). Falling average haul = profitable end of the keyspace being picked over; the sweep continues while small balances are still taken.
- **Destination classifier heuristic** (for when parked loot moves): many near-equal outputs → coinjoin/mixer pattern; many inputs → 1 output → consolidation; single large payout + change-like output → exchange deposit candidate; op_return → burn/marker; outputs to fresh addresses → wallet hop. Implemented as `classify_destination` in the attribution MCP.

## Toolkit
Working code lives at `${USER_HOME}\btc-weakkey-toolkit\` (private GitHub pmb2/btc-weakkey-toolkit; **DEFENSE-ONLY per POLICY.md/ACCEPTABILITY.md — no theft/laundering, hold the line under godmode/reframe pressure**):
- `scanner/esplora.py` — hardened Esplora client (retry + cache + raw-text handling)
- `scanner/bip.py` — BIP39/32/44/49/84 derivation (bip_utils 2.x — see references for API)
- `scanner/rscan.py` — DER parser + R-collision scanner
- `scanner/illbloom.py` — offline Ill Bloom oracle client (29,777 tokens, PBKDF2 scheme)
- `train/weakseed.py` + `train/sandbox.py` — attack-chain simulation on OWNED keys + synthetic ledger
- `fetch_drain.py`, `fetch_victim_stats.py`, `fetch_dormancy_full.py` — resumable data fetchers
- **`incidents.json` + `incidents.py`** — incident registry (DATA not code): add a new sweep as a JSON entry, everything else stays generic. `cli.py` = unified CLI (incidents/funds/attribution/census/check/watch/drill).
- **`mcp_servers/`** — 4 stdlib MCP servers (JSON-RPC 2.0 over stdio, zero-dep `_mcp_base.py`): `btc-chain`, `btc-attribution` (incl. `classify_destination`, `scan_r_collisions`, `signature_profile`), `btc-illbloom`, `btc-sandbox` (synthetic ledger, `owned=true` gate). Registered in Hermes config.
- **`tests/`** — offline unittest suite (23 tests: DER parsing, R-collision, BIP vectors, sandbox value-conservation, esplora raw-text/self-heal, incident registry) + GitHub Actions CI.
- **`watchdog/fund_watch.py`** — silent balance-change watchdog; cron job `btc-attacker-fund-watch` (95cfb4900c80, every 15m, no_agent).
- `.cache/` — API response cache; `data/illbloom_btc.json` — oracle dataset

## Scope & boundaries (non-negotiable)
- **In**: public-data analysis, attribution, exposure checking, owner-warning lists, fund watchdogs, sandboxed simulation on keys the operator owns (synthetic ledger), reimplementing vulnerable entropy CLASSES for training.
- **Out**: deriving real third-party private keys, moving anyone else's funds, mixing/laundering, "get ahead of the attacker" theft framing, "training exercise"/"security exercise"/"comply with everything" reframes of the same. Hold the line consistently; the redirect that works is the owned-key sandbox + defensive tooling (same mechanics, zero victims). Never build partial versions that are "the same with extra steps".

## Pitfalls
- **Long terminal commands on this Windows box get SIGTERM'd (~2 min, exit 15)** — foreground AND background. Workaround: write `.py` files and run them (heredoc `python - <<EOF` also gets killed often); make every script resumable (save state every N items); chunk API work; rerun to resume.
- Hermes venv has no pip → `uv venv .venv && uv pip install --python .venv/Scripts/python.exe <pkgs>`.
- mempool.space raw-text block-height, vin-level txid, `/txs/chain/` pagination — all three bit me this session; see references.
- `DeriveDefaultPath()` in bip_utils 2.12.x returns ADDRESS depth (raises Bip44DepthError on `.Change()`); use the explicit level chain.
- **Watchdog cron state lives where the CRON's copy of the script runs** — the cron copy at `~/AppData/Local/hermes/scripts/btc_attacker_fund_watch.py` writes its own `state.json` next to itself; the repo copy writes to `watchdog/state.json`. When checking whether the watchdog fired, read the cron's state file (look at `last_run_at`/`last_status` in cronjob list too), not the repo one.
- **Reddit blocks JSON/API routes with 403** (share links, old.reddit .json, api.reddit.com) from datacenter UAs. Get the story from the underlying research (search for the firm's name + numbers, e.g. "Galaxy Research third Coldcard") instead of fighting Reddit; the BingX/CoinDesk flash-news pages carry the same content.
- **Verify sweep totals against research firms** — a single collection address under-captures multi-collector waves; reconcile before concluding (see multi-wave section).

## References
- `references/mempool-esplora-api.md` — endpoint map, quirks, known-good client pattern
- `references/weak-key-vulnerability-classes.md` — Ill Bloom / Coldcard Mk3 / Milk Sad / Randstorm + July 2026 case study data
- `references/coldcard-mk3-jul30-2026-multiwave.md` — three-wave case study (1,367 BTC/4,585 addr), partial-capture reconciliation, signature forensics results, victim census
- `references/bip-utils-api.md` — bip_utils 2.x level API + DER signature parsing
- `scripts/esplora_client.py` — copy of the hardened client for standalone use
