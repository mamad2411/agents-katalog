# claude-skills — project instructions

This repo is a toolkit for scalping USDT perpetuals. Five skills cooperate in
two layers:

- **Planning layer** — uses Bybit public REST for data (scan, structure,
  sizing). No keys, no orders.
- **Execution layer** — routes actual orders through the **StrategyFactory
  webhook** (`https://fastcloud.daviddtech.com`) against the connected
  exchange (currently **Toobit**, UID 294780483, affiliated).

`risk-guard` sits between them as the stateful kill-switch.

## Repo layout

```
claude-skills/
├── CLAUDE.md                        # this file (auto-loaded)
├── PROMPT.md                        # paste-ready briefing for a fresh Claude
├── README.md
├── .env                             # encrypted credentials (v2) — DO NOT EDIT by hand
├── .gitignore
├── strategyfactory-webhook.md       # webhook API reference (read this for execution)
├── skills/
│   └── strategyfactory-webhook.md   # (duplicate / legacy copy)
├── bybit-scan/
│   ├── SKILL.md
│   └── scan.py                      # 15m vol-spike screener
├── bybit-structure/
│   ├── SKILL.md
│   └── structure.py                 # trend / ATR / VWAP / swings on one symbol
├── scalp-plan/
│   ├── SKILL.md
│   └── plan.py                      # qty, stop, TP, notional, margin
├── risk-guard/
│   ├── SKILL.md
│   └── guard.py                     # per-trade cap + daily drawdown veto
└── bybit-trade/                     # direct-Bybit execution (NOT primary path)
    ├── SKILL.md
    └── trade.py                     # testnet by default; separate from webhook flow
```

State file (not checked in): `~/.claude/skills/risk-guard/state.json`

## Primary trading flow

For any real trade, follow this order. Do not skip steps.

1. **Scan** — `python bybit-scan/scan.py --top 5`
   Rank Bybit USDT perps by 15m vol spike, tight spread, real liquidity.

2. **Structure** — `python bybit-structure/structure.py SYMBOL`
   Confirm trend/range, ATR, VWAP, swing levels on a candidate.

3. **Plan** — `python scalp-plan/plan.py --equity <E> --risk <R> --side <long|short> --entry <P> --symbol SYMBOL --tick <T> --lot <L>`
   Get qty / stop / TP / R:R. Pull `tick` and `lot` from Bybit
   `instruments-info` (or Toobit's equivalent) — don't guess.

4. **Risk check** — `python risk-guard/guard.py check --risk-usd <R>`
   Must exit 0. Exit 2 = vetoed, stop.

5. **Pre-trade checks (StrategyFactory)** — in this order:
   a. (optional) `POST /checker/affiliate` with `{"exchange":"toobit","uid":"294780483"}`
      — affiliate check is optional, not a gate
   b. `POST /webhooks/` with `mode: "check_api_active"` + encrypted creds
   c. `POST /webhooks/` with `mode: "accountbalance"` + encrypted creds

6. **Place trade** — `POST /webhooks/toobit` (or `/webhooks/<exchange>`)
   with the full trade payload (see `strategyfactory-webhook.md`, §3).
   Always include `"encryptor": "2"`.
   For TP/SL, use `force_tp: "1"` + `multi_tp: "0"` + `tp_3_size: "100"` +
   `tp_3_price: "<price>"` + `stop_loss_price: "<price>"`. **Do not** use
   `take_profit` / `stop_loss` — those fields are silently ignored.

7. **Record** — `python risk-guard/guard.py open ...` with the returned
   order info so the session ledger stays accurate. On close,
   `python risk-guard/guard.py close ...`.

## Exchange mapping (planning vs execution)

| Purpose          | Source                                            |
| ---------------- | ------------------------------------------------- |
| Market data      | Bybit public REST (`api.bybit.com`)               |
| Trade execution  | StrategyFactory webhook → Toobit                  |
| P&L / risk state | `risk-guard/state.json` (local)                   |

Bybit symbols and Toobit symbols may differ. Always verify the Toobit symbol
(usually `BTCUSDT.P` / `SOLUSDT.P`) before sending a trade payload.

## Credentials

Encrypted v2 credentials live in `.env`. Map them into webhook payloads:

- `AGENT_TOOBIT_API_KEY_ENC_V2` → `api_key`
- `AGENT_TOOBIT_API_SECRET_ENC_V2` → `api_secret`
- `AGENT_TOOBIT_PASSPHRASE_ENC_V2` → `passphrase` (if present)
- Always send `"encryptor": "2"` in the payload

Never print, log, or display plain-text credentials. Never accept API keys
on the command line. The `bybit-trade/` path reads `BYBIT_API_KEY` /
`BYBIT_API_SECRET` from env only and defaults to testnet — it is not the
primary execution path and should only be used for direct Bybit testing.

## Hard rules (non-negotiable)

1. **Affiliate check is optional.** If run and it fails, surface the
   signup link from `strategyfactory-webhook.md` §7, but do not block
   the trade.
2. **Risk cap enforced in code.** $50/trade, -$200/day defaults. Never
   overridden at call time. `risk-guard check` is the only gate.
3. **Idempotent identifiers.** Every order tracked with a deterministic
   `orderLinkId` (or webhook-side equivalent) so retries don't double-fire.
4. **Testnet by default** for `bybit-trade`. Requires BOTH `--live` AND
   `BYBIT_ENV=live` to hit mainnet — belt and suspenders.
5. **Verbatim errors.** Surface whatever the exchange / webhook returned.
   No invented fallbacks.
6. **Log `event_id`** from every StrategyFactory response for traceability.
7. **No plain-text keys** in files, logs, stdout, or command-line args.

## Quick reference

- Webhook base: `https://fastcloud.daviddtech.com`
- Webhook docs: [`strategyfactory-webhook.md`](strategyfactory-webhook.md)
- Connected UID (Toobit): `294780483`
- Affiliate endpoint: `POST /checker/affiliate`
- Account endpoint: `POST /checker/account` or `POST /webhooks/` with `mode`
- Trade endpoint: `POST /webhooks/toobit`
