---
name: airdrop-agent
description: Autonomous airdrop operator. Use when the task involves airdrops, testnets, quests, point farming, NFT whitelists, mass wallet/identity generation, Telegram/X/Discord growth, faucet claiming, contract deploy on testnets, or monitoring channels for new drops. Runs on Hermes, Muse, OpenClaw, Claude, or plain cron via one CLI.
version: 4.0.0
license: MIT
requires: python>=3.10
entrypoint: aa
---

# airdrop-agent skill

One agent covers the whole airdrop cycle. You drive it through `aa`; every command returns a JSON
envelope. Never invent wallet addresses, transaction hashes, or "done" states — read them from `data`.

## Boot

```bash
aa doctor                 # if this fails, fix it before anything on-chain
aa status                 # mode, KILL, identities, pending gates
```

`doctor` fails → report the failing key, do not proceed to funding/signing. `guard.kill` true → `aa unkill`
only if the operator says so.

## Envelope contract

```json
{"ok": true, "data": {...}, "next": ["..."]}
{"ok": false, "error": "approval #4 required — ..."}   exit 10
{"ok": false, "error": "value ... > per-tx cap ..."}   exit 2
{"ok": false, "error": "KILL switch is set"}           exit 99
```

Rules:
- exit `0` → continue with `next`, or answer from `data`.
- exit `10` → the payload is frozen by hash. Show the summary, wait for the human code, then
  `aa gate approve <id> <CODE>` and re-run the exact same command. Do not alter amount/recipient before approval.
- exit `2` → policy said no. Explain the number, offer the smallest fix (reduce amount, allowlist domain,
  `aa mode turbo` for testnet only), then retry.
- exit `99` → stop everything until `aa unkill`.
- exit `3` → bug or network. Read `error`, retry once, then report.

## Identity & wallet

```bash
aa identity new <label> --wallets 3        # persona + HD EVM/Solana vault
aa identity list
aa wallet new --identity <id> --chain evm --count 20
aa wallet balance --identity <id>
aa wallet send --chain <chain> --identity <id> --to <addr> --amount <n> [--broadcast]
aa sign message --identity <id> --message "..." --origin <domain>
```

Private keys and mnemonics are never printed. Need one? `aa vault export ~/aa-backup.json` (encrypted).

## Socials

```bash
aa tg login --identity <id> --phone +62...
aa tg verify --identity <id> --code 12345          # 2FA password via --password
aa tg join @channel --identity <id>
aa tg follow @a @b --identity <id>                 # daily-ish, rate limited

aa x login --identity <id> --user <u> --password <p> [--totp <secret>]
aa x follow handle1 handle2 --identity <id>
aa x post "gm" --identity <id>

aa dc login --identity <id> --email <e> --password <p>
aa dc servers --identity <id>
aa dc grind --identity <id> --server <name> --minutes 30
aa dc progress --identity <id>
```

Discord grinding uses a humanizer (typing delay, bursts, typos, persona, dedupe). It is user-token
automation: dedicated account only, and it parks when a captcha appears.

## Quests

```bash
aa quest probe https://site/tasks --identity <id>   # fields, buttons, challenge
aa quest new "Name" https://site --platform galxe --chain sepolia
aa quest validate <id>
aa quest run <id> --dry
aa quest run <id> --identity <id>
```

Use `probe` before writing any quest; never guess selectors. `dry` lists steps only, a real run
writes proofs to `~/.airdrop-agent/proofs/`. `manual`, captcha, wallet gates and a logged-out
platform park the run with a screenshot and a `next` command — park ≠ fail.

Nineteen tested quests live in `config/quests/`; `docs/TARGETS.md` says where each stops.

## Sessions and Cloudflare

One browser profile per identity; cookies survive between modules. If a quest returns
`needs_login`, log in and warm, do not force it:

```bash
aa social login x --identity <id> --user … --password …
aa session check --identity <id> --platforms x
aa session warm --identity <id>
```

Challenge: check the clearance cache first, then assist once.

```bash
aa cf status
aa cf assist --identity <id> --url https://site/tasks
aa cf clear --identity <id> --host site
```

Never rotate a proxy that already holds clearance. The cookie is bound to IP + UA.

## Testnet / on-chain

```bash
aa testnet faucets --chain sepolia
aa testnet claim --chain sepolia --identity <id>
aa testnet deploy --chain sepolia --identity <id> --kind counter
aa testnet campaign --chain sepolia --identity <id> --name daily --rounds 2
```

Every tx goes simulate → caps → gate → sign → broadcast → proof. Testnets are inside caps in balanced
and turbo. Mainnet always gates unless `allow_mainnet` is explicitly opened.

## Radar

```bash
aa radar scan --identity <id>
aa radar latest --min-score 60
aa radar add tg @channel --trust 2
```

Scan dedupes, runs scam heuristics, scores 0-100 with reasons, queues a draft quest above threshold.
Read the reasons before farming; the score is a filter, not a verdict.

## Daily / autopilot

```bash
aa daily plan --identity <id>
aa daily run --identity <id>
aa autopilot plan
aa autopilot tick
```

Autopilot modules are switches in `~/.airdrop-agent/autopilot.yaml`. Keep `chat: false` unless the
operator opted into Discord ToS risk.

## Email

```bash
aa email add --identity <id> --address me@x.com --password <app-password>
aa email otp --identity <id> --sender galxe
aa email link --identity <id> --sender project
```

Codes arrive from the agent's own inbox, not from chat text.

## Modes

`balanced` default. `turbo` widens caps and auto-approves connect/sign inside limits; hard blocks stay
(KILL, unlimited approval, eth_sign, blocklist, drainer verdict). `safe` gates everything.

```bash
aa mode turbo   # only when the operator accepts the wider caps
aa mode balanced
```

## Decision order for "cari airdrop"

1. `aa radar scan` (real sources) → 2. filter `min_score` + scam verdict → 3. open the URL once headful if
unsure → 4. draft/validate quest → 5. `--dry` → 6. run on one identity → 7. scale identities only after it works.

Do not scale before one identity succeeds. Do not fund a fresh wallet before the quest flow is proven.

## Failure playbook

| symptom | action |
|---|---|
| captcha | set `CAPTCHA_API_KEY`, or run headful and hand off; never loop blindly |
| login wall | `aa dc/x/tg login ...` once, then retry the quest |
| selector miss | `aa browser --identity <id> --url <u> --login` to inspect; report selector + screenshot |
| flood wait | wait `e.seconds`, the agent already respects `TG_MAX_FLOOD_WAIT` |
| simulation reverted | wallet unfunded or slippage; check `aa wallet balance`, faucet first |
| daily cap | smaller amount or `aa mode turbo` for testnet |

## Output style

Answer with the concrete result first: address, tx hash, gate id, score, or the exact blocking reason.
Then one next step. No preamble, no "sebagai AI", no disclaimer block.

## Portability

The skill is model-agnostic. If the host has no shell, use the MCP server (`aa mcp serve`, tools prefixed
`aa_`) and call the same operations. If the host has no persistent process, cron `aa autopilot tick`.
Config lives in `~/.airdrop-agent`; nothing is hardcoded to one machine.
