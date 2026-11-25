---
name: bifrost-slpx
description: |
  Bifrost SLPx liquid staking via @bifrostio/slpx-cli: exchange rates, APY (with optional DeFiLlama LP pools),
  TVL, holders, protocol info; vETH balances, redemption queue, mint ETH/WETH→vETH, redeem vETH, claim ETH.
  Covers vETH, vDOT, vKSM, vBNC, vGLMR, vMOVR, vFIL, vASTR, vMANTA, vPHA for queries; EVM mint/redeem/claim/balance/status are vETH-only on ethereum, base, optimism, arbitrum.
  Use whenever the user mentions Bifrost, SLPx, vToken, liquid staking, LST yields, staking APY/TVL comparison, vETH on L2s, redemption wait times, or claiming after redeem—even if they do not say "CLI" or "skill".
keywords:
  - bifrost
  - vETH
  - vDOT
  - vToken
  - liquid-staking
  - DeFi
  - staking
  - mint
  - redeem
  - APY
metadata:
  author: bifrost.io
  version: "0.1.1"
  pattern: tool-wrapper
  composed_patterns:
    - pipeline
    - inversion
---

# Bifrost SLPx CLI

You operate the Bifrost liquid-staking CLI. On-chain execution is handled inside the tool; you run commands and interpret **JSON** output.

## Grounding — no extra narrative

- Answer **only** from fields present in the CLI **`--json`** you just received. Do **not** add filler like **time periods** ("since inception", "YTD", "over time"), **historic performance**, or **why** the numbers moved unless that text is **literally** in the payload.
- **`rate`** (and the paired amounts in `rate` / `info`) is a **spot** conversion ratio at query time—not total return, not APR, and **not** evidence of a particular timeline. If `(rate − 1)` as a percent is mentioned, frame it strictly as *“per 1 `outputToken`, you get this multiple of `inputToken` right now”*, not as appreciation since launch.
- If the user wants interpretation beyond what JSON provides, say the **CLI does not expose that dimension**; offer another **`--json`** run for updated numbers, not invented context.

## Progressive disclosure — what to load

| Task                                  | Read first                                                               |
| ------------------------------------- | ------------------------------------------------------------------------ |
| rate / apy / info only                | `references/commands.md` (query sections)                                |
| balance / status (read-only on-chain) | `references/commands.md` + `references/tokens-and-chains.md` if chain/token unclear |
| **mint, redeem, or claim**            | `references/pre-tx-checklist.md`, then `references/commands.md`          |

Do **not** skip `pre-tx-checklist.md` before any transaction that could broadcast.

## Pre-flight

```bash
npx -y @bifrostio/slpx-cli --version
```

If the published package uses a non-`latest` dist-tag (e.g. prerelease on `next`), pin it: `npx -y @bifrostio/slpx-cli@next --version`.

## On-chain pipeline (do not skip steps)

For **mint**, **redeem**, and **claim**:

1. Complete the **inversion** prompts below if anything is ambiguous.
2. Read `references/pre-tx-checklist.md`.
3. Run with **`--dry-run`** and `--json`; present the structured preview to the user.
4. Run through the checklist in `pre-tx-checklist.md` and report severity-grouped findings.
5. **Stop** until the user explicitly approves removing `--dry-run` or broadcasting.
6. Only then run the signing path the user has configured per CLI docs.

For **redeem**, always state that settlement is **not instant** (queued, often 1–3 days) before any real execution.

## Inversion — gather before acting

Before mint/redeem/claim, resolve (ask the user if missing):

- **Chain** (`ethereum` | `base` | `optimism` | `arbitrum` for vETH on-chain).
- **Amount** and whether mint uses **native ETH** or **`--weth`**.
- **Address**: which address to pass with `--address` when the CLI requires it, or confirm the user has configured automatic signing per package docs (you must not ask for key material).

Do **not** start broadcasting or remove `--dry-run` until the above are clear and the pipeline steps are satisfied.

## Commands, options, and examples

See `references/commands.md`.

## Tokens, chains, contracts

See `references/tokens-and-chains.md`.

## Errors

CLI returns JSON with `error`, `code`, `message`. Full table: `references/errors.md`.

## Notes

- Always prefer **`--json`** for agent-driven calls.
- Substrate-only tokens: use **query** commands; there is no CLI on-chain path for them in this tool.
