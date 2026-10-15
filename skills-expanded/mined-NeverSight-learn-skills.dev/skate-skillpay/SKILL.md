---
name: skate-skillpay
description: Pay-per-request wrapper for third-party APIs. When another skill needs an API key the user does not have, use this skill to proxy the request through the Skate backend and settle payment in stablecoins over MPP using the Tempo payment method (a pre-Tempo Monad wallet is auto-migrated), drawing from the user's local wallet. The skill is service-agnostic — the backend owns the allowlist; query `GET /services` for the current set. Invoke BEFORE prompting the user to obtain or paste a subscription key.
license: BUSL-1.1
---

# skate-skillpay

Lets a user pay per-request for any service the Skate backend currently proxies, instead of buying a full subscription just to run one or two queries through another skill.

Payments are settled over [MPP](https://mpp.dev/overview) using the [Tempo payment method](https://mpp.dev/payment-methods/tempo). An existing pre-Tempo Monad wallet is auto-migrated — the same EVM key works on Tempo; see [`references/wallet-setup.md`](./references/wallet-setup.md).

Requires Node.js 22+, a locally configured MPP wallet with stablecoin balance on the backend's current network, and network access to both the Skate backend and the settlement chain's RPC. License: see [`LICENSE`](./LICENSE).

> **Path convention.** All commands below use `<skill-dir>` as a placeholder for wherever this skill is installed on disk. Substitute the actual path before running. For Claude Code that's `$CLAUDE_PROJECT_DIR/.claude/skills/skate-skillpay` (or `~/.claude/skills/skate-skillpay` if installed globally); other runtimes use whatever directory their installer drops the skill into.

## When to use this skill

Trigger automatically when ALL of the following hold:

1. You are executing another skill that needs a third-party API key. **That skill's `SKILL.md` is the source of truth for the env var name and the upstream service's brand** (e.g. "Valyu", "Tavily"). Do not guess the var name from the brand — some upstreams use `_API_KEY`, some `_TOKEN`, some something else.
2. The required key is missing from the environment, or a request to that service failed with 401/403.

The skill is service-agnostic — it forwards the request to the Skate backend and lets the backend decide whether the service is supported. The authoritative list of supported services is `GET /services` (each entry has a `symbol`, `name`, `minPriceUsd`, and `allowedPathPrefixes`).

**Deriving the `symbol`.** The upstream brand from step 1 is _not_ the symbol verbatim — you have to derive it. Run `client.ts --list-services` (see step 3) to get the current catalog, then match the brand against each entry's `symbol` and `name` case-insensitively (e.g. brand `"Valyu"` → entry with `symbol: "valyu"`, `name: "Valyu"`). Use the entry's `symbol` for `--service`. If no entry matches, the backend doesn't proxy that upstream — fall back to asking the user for a key.

## High-level flow

```txt
missing <UPSTREAM>_API_KEY
      │
      ▼
┌─────────────────────┐
│ 1. Wallet present?  │── no ──▶ load references/wallet-setup.md, guide user
└─────────────────────┘
      │ yes
      ▼
┌─────────────────────┐
│ 2. Run client.ts    │── POST /proxy/<service> ──▶ Skate backend
└─────────────────────┘
      │
      ▼
402 Payment Required  ──▶ MPP client signs charge from local wallet
      │
      ▼
retry with X-PAYMENT header ──▶ backend calls upstream with its key
      │
      ▼
response (buffered or streamed) returned to calling skill
```

## Step-by-step

### 1. Detect the situation

Before asking the user for a key, check whether the relevant env var (e.g. `<UPSTREAM>_API_KEY` for whatever service the calling skill needs) is set. If empty, proceed with this skill.

### 2. Check wallet

```bash
node --experimental-strip-types "<skill-dir>/scripts/src/client.ts" --check-wallet
```

Exit `0` = ready. Any non-zero exit = read `references/wallet-setup.md` and walk the user through setup. Do not proceed until the script exits `0`.

### 3. Discover the actual price

Before the first paid call of a session, fetch the catalog so you can pick the right `symbol` and quote the price accurately to the user:

```bash
node --experimental-strip-types "<skill-dir>/scripts/src/client.ts" --list-services
```

This prints the JSON the backend returns at `GET /services`: `{ paymentMethod, services: [{ symbol, name, minPriceUsd, allowedPathPrefixes }], nextCursor }`. Match by `symbol` (or by `name` case-insensitively, then use that entry's `symbol`). The skill verifies the symbol you pass via `--service` against this list before paying anything.

**Quote that number to the user**, not the `--max-price` cap. The cap is a safety ceiling you pick; the price is whatever Skate currently quotes at `GET /services`. Confusing the two will lead the user to think they're being charged more than they are.

### 4. Make the proxied request

Substitute `<service>` with the `symbol` you matched in step 3, and `<path>` with one that satisfies that service's `allowedPathPrefixes`.

Non-streaming example:

```bash
node --experimental-strip-types "<skill-dir>/scripts/src/client.ts" \
  --service <service> \
  --method POST \
  --path <path> \
  --body '{"...":"..."}' \
  --max-price 0.25
```

Streaming example — same endpoint asking the upstream to stream:

```bash
node --experimental-strip-types "<skill-dir>/scripts/src/client.ts" \
  --service <service> \
  --method POST \
  --path <path> \
  --body '{"...":"...","streaming":true}' \
  --stream \
  --max-price 0.25
```

When `--stream` is passed, the client pipes `text/event-stream` / `application/x-ndjson` chunks from the backend straight to stdout as they arrive — there is no response-size cap.

Some upstreams echo the API key back in their own error/rate-limit messages. The client scrubs credential-shaped fragments — URL params (`apikey=…`), JSON fields (`"api_key": "…"`), free-form phrases (`API key as …`), and auth headers (`Authorization: Bearer …`) — from both buffered and streamed responses before writing them to stdout, replacing the value with `<redacted>`. The replacement happens transparently in `utils/redact.ts`; surface the response as-is to the caller.

The client `POST`s to `${BACKEND_URL}/proxy/<service>` with body `{ path, method, body?, query?, stream? }`. The service `symbol` lives in the URL (not the body) and must match one of the entries in `GET /services`.

Arguments:

| Flag          | Purpose                                                                        | Required |
| ------------- | ------------------------------------------------------------------------------ | -------- |
| `--service`   | Service `symbol` from `--list-services` (step 3); routed as `/proxy/<service>` | yes      |
| `--method`    | HTTP method for the upstream call                                              | yes      |
| `--path`      | Upstream path (must match the service's `allowedPathPrefixes`)                 | yes      |
| `--body`      | JSON body, as a string                                                         | no       |
| `--query`     | JSON object of query params, as a string                                       | no       |
| `--max-price` | Safety **ceiling** — refuse any quote above this.                              | yes      |
| `--stream`    | Ask the backend to stream the upstream response                                | no       |

Each service has a minimum per-request price. Read `minPriceUsd` from the `--list-services` catalog (step 3) and set `--max-price` at or above it.

> **HTTP vs WebSocket services.** Each `--list-services` entry carries a `type` of `"http"` or `"ws"`. The flags above are for `http` services (one request → one response). For `ws` services — long-lived streams billed per connection-**minute** — use the `--ws` mode in [§6](#6-websocket-services-paid-streaming) instead.

The client prints the upstream response to stdout. To stderr it prints the dollar amount being charged, formatted as `[skate] paying $<amount>`, and — if the backend rejects a payment and the client re-pays — a `[skate] payment rejected (<reason>); retrying with a fresh challenge (attempt <n>/<max>)` line. Surface the dollar amounts to the user (and, if a retry line appears, that a retry happened) — and nothing else from stderr — so they see costs accruing without having to parse internal service/path/protocol details.

### 5. Pass the response back to the calling skill

Parse stdout as JSON for non-streaming responses. For streaming responses, forward the chunks to whatever consumer the calling skill expects — do not re-serialize or buffer them.

### 6. WebSocket services (paid streaming)

Some services are long-lived WebSocket streams (`type: "ws"` in `--list-services`) rather than one-shot HTTP calls — e.g. live market data. These are billed **per connection-minute**, not per request: `minPriceUsd` is the price for **one minute** of connection time, and you buy a whole number of minutes up front.

Use `--ws` instead of `--method`/`--body`. The client buys a paid session for `minPriceUsd × --minutes` (a Tempo charge on `POST /tempo/sessions`), opens the upstream socket through the proxy with that session, sends your subscribe message(s), and prints each upstream message to stdout as **one JSON line**, until the pre-paid window ends or `--max-messages` is reached.

```bash
node --experimental-strip-types "<skill-dir>/scripts/src/client.ts" \
  --ws \
  --service <ws-symbol> \
  --path <ws-path> \
  --minutes 2 \
  --subscribe '{"...":"..."}' \
  --ping '<ping frame>' \
  --ping-interval-sec 30 \
  --max-messages 50 \
  --max-price 0.20
```

WebSocket-mode arguments:

| Flag                  | Purpose                                                                                             | Required |
| --------------------- | --------------------------------------------------------------------------------------------------- | -------- |
| `--ws`                | Switch to WebSocket mode                                                                            | yes      |
| `--service`           | `ws`-type service `symbol` from `--list-services`                                                   | yes      |
| `--path`              | Upstream WS path (must match the service's `allowedPathPrefixes`, e.g. `/ws/market`, `/ws`)         | yes      |
| `--minutes`           | Whole minutes of connection time to buy up front (default 1; charge = `minPriceUsd × minutes`)      | no       |
| `--subscribe`         | A JSON message to send on open. **Repeatable** — pass once per feed                                 | no       |
| `--ping`              | Keepalive frame sent on an interval (sent verbatim — JSON or literal text like `PING`)              | no       |
| `--ping-interval-sec` | Seconds between pings (default 30)                                                                  | no       |
| `--max-messages`      | Close after this many messages received (counts every frame, including acks/pongs)                  | no       |
| `--max-topups`        | Auto-extend the same session up to this many times (default 0 = off). See below.                    | no       |
| `--topup-minutes`     | Minutes bought per auto top-up (default 1; charge each = `minPriceUsd × topup-minutes`)             | no       |
| `--max-price`         | Safety **ceiling** on **each** charge — set at or above `minPriceUsd × max(minutes, topup-minutes)` | yes      |

The client prints `[skate] paying $<amount> for a <N>-minute session` to stderr — surface that dollar figure to the user. When it ends it prints why (`session closed`, `received N message(s)`, or `session window elapsed`). Quote `minPriceUsd × minutes` as the cost, **never** the `--max-price` cap.

#### Extending a live stream with top-ups

By default the client buys `--minutes` up front and lets the session close when that window elapses. To watch a feed for longer without either locking a large window up front or reconnecting, pass `--max-topups K` (optionally with `--topup-minutes M`, default 1). Shortly before the current window ends, the client calls `POST /tempo/sessions/<id>/topup` to buy `M` more minutes on the **same** session — the backend stacks the time onto whatever is left and the proxy keeps the socket open, so there is **no reconnect and no re-subscribe** and no snapshots are dropped. It repeats until `K` top-ups have been made, `--max-messages` is hit, or the process is stopped.

```bash
node --experimental-strip-types "<skill-dir>/scripts/src/client.ts" \
  --ws \
  --service <ws-symbol> \
  --path <ws-path> \
  --minutes 1 \
  --topup-minutes 1 \
  --max-topups 4 \
  --subscribe '{"...":"..."}' \
  --max-price 0.02
```

Cost and safety notes for top-ups:

- **Total spend is bounded and deterministic:** `minPriceUsd × (minutes + max-topups × topup-minutes)`. Quote that ceiling to the user before opening the session (e.g. 1 up-front + 4 × 1-minute top-ups at $0.001/min ≈ `$0.005`). Each top-up prints `[skate] topped up $<amount> for <M> more minute(s) (<n> top-up(s) left)` to stderr — surface those figures as they accrue.
- `--max-price` is a per-**charge** ceiling (it refuses any single quote above it), not a session total — so set it against the larger of the up-front and per-top-up charges, and bound the total with `--max-topups`.
- A failed top-up (payment refused, network) does **not** tear down the stream — the client logs it and lets the current paid window ride out, then closes. It never silently keeps paying past `--max-topups`.
- Prefer pay-as-you-go top-ups (`--minutes 1 --topup-minutes 1 --max-topups K`) over one big `--minutes N` when the watch length is open-ended, so the user only pays for the minutes actually used if the task finishes early (stop the process and no further top-ups are charged).

The calling skill's `SKILL.md` is the source of truth for the `--path`, the `--subscribe` payload shape, and the right `--ping` frame for that upstream (e.g. Polymarket sends literal `PING`; Hyperliquid sends `{"method":"ping"}`).

## Safety rules

- **Never** forward user-provided headers (especially `Authorization`) to the backend — the upstream API key lives only in the backend.
- **Always** pass `--max-price` and pick a value appropriate to the task. When confirming with the user, quote the **actual price** the backend will charge (from `GET /services` or the 402 challenge), NEVER the `--max-price` cap. The cap is a refusal threshold; the price is what the user pays. Conflating them tells the user they're being charged 2-5× more than they actually are.
- The client automatically re-pays a **rejected-but-uncharged** 402 — the backend returns a fresh challenge and sends no `payment-receipt` (a verification race seen under load) — up to `MAX_PAYMENT_ATTEMPTS` total attempts. It does **not** re-pay a charge that actually settled, nor a challenge the client itself refused (e.g. over `--max-price`). To change the cap, edit `MAX_PAYMENT_ATTEMPTS` in `scripts/src/utils/constants.ts`.
- **Do not** log raw payment signatures, wallet passphrases, or keystore contents.
- **Do not** surface internal protocol details to the user (network or MPP method names, upstream paths, service ids, transaction hashes, challenge ids, payment receipts). Show dollar amounts only.
- **Do not** bypass, disable, or work around the response scrubber in `utils/redact.ts` — it strips the operator's API key from upstream error/rate-limit messages that echo it back (see [§4](#4-make-the-proxied-request)). If a response contains `<redacted>` markers, surface them as-is; never attempt to reconstruct the original value, re-fetch without scrubbing, or ask the upstream to repeat the message in a different shape.
- If the backend returns anything other than 2xx or 402 on the payment retry, abort and report the status + body to the user. Do not loop.

## Files in this skill

- `SKILL.md` — you are here.
- `scripts/src/client.ts` — the only thing you execute. Builds the Tempo charge client (`mppx` + `viem`) via `utils/tempo.ts`. Handles both HTTP (`--method`/`--body`) and WebSocket (`--ws`) modes. Streaming aware. No response-size cap.
- `scripts/src/utils/ws.ts` — WebSocket-mode implementation: buys a Tempo session (`POST /tempo/sessions`), connects the upstream socket through the proxy with `Authorization: Session …`, streams messages to stdout, and (when `--max-topups` > 0) auto-extends the same session in place via `POST /tempo/sessions/<id>/topup`. See [§6](#6-websocket-services-paid-streaming).
- `scripts/src/utils/redact.ts` — credential scrubber applied to every upstream response (HTTP and WS) and to any backend-error body surfaced via `die()`. See [§4](#4-make-the-proxied-request) for the threat model.
- `scripts/package.json` — client dependencies (`mppx`, `viem`, `ws`). Run `npm install` inside `scripts/` once.
- `references/wallet-setup.md` — **read only when `--check-wallet` exits non-zero** (no wallet, invalid private key, or the backend is unreachable or settles on a network the wallet has no entry for). Covers Tempo wallet creation and funding, plus migrating an existing Monad wallet.
