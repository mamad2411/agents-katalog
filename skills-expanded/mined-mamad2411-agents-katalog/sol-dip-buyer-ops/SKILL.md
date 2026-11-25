---
name: sol-dip-buyer-ops
description: Operate Cooper's Solana dip-buyer at ~/git/darkmatter/sol-dip-buyer — multi-buyer same-mint (mrv/mrv2/dip), buy≠sell, botctl, freq paint + jitter, timed ref ramps, padre liq-proportional sells, Alchemy direction cron. Status tables include last-4 of wallet addrs. Never multi-wallet buy split farms.
---

# sol-dip-buyer ops

Repo: `~/git/darkmatter/sol-dip-buyer` (Prelude/`nix develop`, venv `.venv`).

## Hard rules

1. **Detached live only via `scripts/botctl`** — never long-lived live in the agent foreground.
2. **Refuse multi-wallet buy split/wash farms.** Same *buy* strategy on multiple **named** hot wallets (separate run_ids + keypairs) is OK for size/verify — that is not a wash farm. Dual-strategy = isolated risk + buy≠sell accounts.
3. **Buy and sell must never share an account.** Live sell requires `--buy-wallet <BUY_PUBKEY>` and dies if it equals the sell key. Sibling opposite-side heartbeats with the same wallet also fail closed.
4. **Tokens do not auto-route buy→sell.** Transfer buy wallet → sell wallet yourself (or a separate transfer tool). Sell bot only dumps what's on the sell account.
5. **Restart budgets net of `state.json` spent** — bump `--budget` or use wallet mode; don't assume a fresh ceiling unless `--reset-state`.
6. **Never paste key material.** Keypaths only. Prefer `himitsu exec` for `sol-1` → `~/wallets/padre-sol-1.json`.
7. **Restart ≠ idle.** Boot had `last_trade_ts=0` unless seeded; if spot is still under buy-ref the first loop market-buys. Pair every live restart/ref bump with default honor-last-fill + `--start-cooldown 90`. See `references/ref-ramp.md`.

## Layout (multi-strategy)

```text
runs/<mint8>/<run_id>/     # default run_id = <side>-<style>
runs/<mint8>/              # legacy single-bot still supported
```

Per-run files: `bot.pid`, `bot.lock` (flock **per run_id**), `heartbeat.json`, `bot.log`, `state.json`, `trades.csv`.

Same mint + two strategies = two run dirs = two locks. Lock is **not** global per mint.

## Public address / hex for key files

```bash
solana-keygen pubkey ~/wallets/padre-sol-1.json
# example: GKzKZWPbCBZsSC22Neabbowiz5LdbBgs98uwticafXjy

# pubkey hex only (last 32 of 64-byte JSON) — safe to display
python3 -c 'import json,sys; print(bytes(json.load(open(sys.argv[1])))[32:].hex())' ~/wallets/padre-sol-1.json
# full secret hex — NEVER paste into chat/screenshots; local terminal only if needed
```

JSON keypair = 64 bytes (32 seed + 32 pubkey). Mode `600` on `~/wallets/*.json`.

### Terminal exposure (what peers can see)

- `ps` / botctl cmdline: **path** to keyfile + **public** addresses in flags — not private key bytes.
- heartbeats/logs: wallet pubkey, spent, status (public by design).
- `cat`/`xxd` of key JSON or secret hex → treats as leaked; avoid in shared TUI/screenshare.
- On-chain activity for any pubkey is world-readable regardless of terminal hygiene.

### Import base58 secret → `~/wallets/*.json`

Triggers: “import /tmp/key into ~/wallets”, MetaMask Solana export, any base58 secret landing on disk.

1. **Never cat/print the secret into chat.** Inspect length/type only (`wc -c`, `file`, first-bytes via `xxd` of a *copy* only if needed). Existing style: 64-int JSON arrays, mode `600`, dir `700`.
2. **Detect shape:**
   - Base58 text, ~87–88 chars, decodes to **64 bytes** → full secret key (seed‖pubkey). Common MM / Phantom export.
   - Base58 → **32 bytes** → seed only; expand with ed25519 before writing (or ask user for full secret).
   - Already a JSON array of 64 ints → copy with `cp -f` + `chmod 600`; skip convert.
3. **Convert without npm deps** (no `@solana/web3.js` / `bs58` required on path):

```bash
# Hermes terminal: avoid bare `&` in scripts (bitwise AND in python -c / heredoc
# is parsed as shell backgrounding by this tool). Prefer python -c without `&`,
# or write a .py file then run it.
python3 -c '
import json, os
from pathlib import Path
ALPHABET = b"123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
def b58decode(s):
    n = 0
    for c in s.encode():
        n = n * 58 + ALPHABET.index(c)
    pad = 0
    for c in s.encode():
        if c == ALPHABET[0]:
            pad += 1
        else:
            break
    full = n.to_bytes((n.bit_length() + 7) // 8, "big") if n else b""
    return b"\x00" * pad + full
src = Path("/tmp/key")  # or path user gave
raw = src.read_text().strip()
data = b58decode(raw)
assert len(data) == 64, len(data)
wallets = Path.home() / "wallets"
wallets.mkdir(mode=0o700, exist_ok=True)
name = "imported.json"  # or user-provided name
out = wallets / name
n = 1
while out.exists():
    n += 1
    out = wallets / ("imported-%d.json" % n)
fd = os.open(str(out), os.O_WRONLY + os.O_CREAT + os.O_EXCL, 0o600)
with os.fdopen(fd, "w") as f:
    json.dump(list(data), f)
    f.write("\n")
print(out)
'
solana-keygen pubkey ~/wallets/imported.json   # confirm; match export UI if MM
rm -f /tmp/key   # source was often world-readable (e.g. /tmp 644) — wipe after success
```

4. **Report only:** destination path, mode, pubkey. Do not echo secret bytes/hex/base58 back.
5. Prefer a **named** hot wallet (`mrv.json`, etc.) over leaving `imported.json` long-term — rename if user wants. Fresh bot hot wallet > dumping a large cold/MM bag into dip-buyer.
6. After import, wire with `solana-keygen pubkey` before `--keypair` / buy≠sell flags.
7. **Dedup before celebrating a “new” wallet.** Compare decoded 64 bytes (or pubkey) against every `~/wallets/*.json`. Same base58 twice (e.g. `/tmp/key` then `/tmp/mrv`) → same pubkey; keep one named file, delete/rename the duplicate, tell Cooper.

## Botctl

```bash
cd ~/git/darkmatter/sol-dip-buyer
export DIP_BUYER_KEYPAIR=~/wallets/padre-sol-1.json   # or BUY_/SELL_ side envs
export SOLANA_RPC_URL='…'   # preferred

./scripts/botctl list
./scripts/botctl status --mint $MINT          # all runs under mint
./scripts/botctl status --run-dir runs/<m8>/<run_id>
./scripts/botctl logs --run-id buy-paint --mint $MINT -f
./scripts/botctl stop --run-dir runs/<m8>/<run_id>
./scripts/botctl stop --mint $MINT --all
./scripts/monitor_check.py --mint $MINT --all
```

### Dual buy styles (same mint, one wallet)

```bash
./scripts/botctl start --mint $MINT --side buy --style paint --run-id buy-paint \
  --live --confirm-live YES --keypair "$DIP_BUYER_KEYPAIR" \
  --ref-mcap 100000 --prefer-dex pumpswap
./scripts/botctl start --mint $MINT --side buy --style absorb --run-id buy-absorb \
  --live --confirm-live YES --keypair "$DIP_BUYER_KEYPAIR" \
  --ref-mcap 100000 --prefer-dex pumpswap --budget 20
```

### Same strategy on two wallets (verify / size — not wash farm)

Stop legacy flat `runs/<mint8>/` first so one wallet isn't double-fired. Cross-wire each bot's `--sell-wallet` to the **other** hot pubkey so buy≠sell enforcement stays green even though both sides are buys.

**`--sell-wallet` on a buy run is annotation/guard only — it does NOT sell.** `side=buy` never dumps tokens. `tokens_sold` stays 0 until a separate `--side sell` process exists. If Cooper asks “is X selling?” check `side`, `tokens_sold`, and cmdline — not the sell-wallet flag alone.

```bash
PADRE=~/wallets/padre-sol-1.json          # GKzKZW…
MRV=~/wallets/mrv.json                    # AZYsGo… (replaced marv-dip-buyer/PWbrhU…)
PADRE_PUB=$(solana-keygen pubkey "$PADRE")
MRV_PUB=$(solana-keygen pubkey "$MRV")

./scripts/botctl stop --mint $MINT --all
./scripts/botctl start --mint $MINT --side buy --style paint --run-id buy-paint-padre \
  --live --confirm-live YES --keypair "$PADRE" --sell-wallet "$MRV_PUB" \
  --ref-mcap 150000 --budget 99 --prefer-dex pumpswap --budget-mode wallet
./scripts/botctl start --mint $MINT --side buy --style paint --run-id buy-paint-marv \
  --live --confirm-live YES --keypair "$MRV" --sell-wallet "$PADRE_PUB" \
  --ref-mcap 150000 --budget 99 --prefer-dex pumpswap --budget-mode wallet
```

Expect `wallet_low` on any dry wallet until funded; process stays up. Spent ceilings are **per run_id** — switching the marv run's keypair does **not** reset `state.spent_sol` (budget still counts prior fills on that run).

### Swap buy keypair mid-run (keep run_id + spent)

1. Import/name new key under `~/wallets/` (`600`); `solana-keygen pubkey`; detect duplicate of existing files before treating as new capital.
2. Stop only that `--run-id`.
3. Restart identical flags except `--keypair` (+ update its peer's `--sell-wallet` to the new pubkey if dual-wired).
4. Old hot still holds leftover SOL/tokens until swept — not auto-migrated.
5. Prove via heartbeat `wallet` + cmdline path, not filename alone.

### Retarget reference mid-run (raise/lower `--ref-mcap`, keep spent)

`state.json` already holds `ref_price_usd` / `ref_mcap_usd`. Passing `--ref-mcap` / `--ref-price` on restart **overrides** them and logs `ref overridden -> price=… mcap=…`. Spent / fills stay — do **not** `--reset-state`.

```bash
for RID in buy-paint-mrv2 buy-paint-marv buy-paint-dip; do
  ./scripts/botctl stop --mint "$MINT" --run-id "$RID"
done
# same keypair/sell-wallet/budget/style; only ref (+ optional ramp) changed
./scripts/botctl start … --run-id buy-paint-mrv2 \
  --ref-mcap 175000 --ref-mcap-end 200000 --ref-ramp-end 12h \
  --start-cooldown 90 …
# prove: heartbeat ref_mcap_usd / ref_ramping / ref_mcap_end; log "ref RAMP armed";
# NO instant SIGNAL unless dd+CD allow (seeded cooldown / start-cooldown lines)
```

**Raising ref while spot is below it** jumps drawdown and used to auto-fill on boot. Always pair with honor-last-fill (default) + `--start-cooldown`. Budget ceiling still from `state.spent` + `--budget` / wallet mode.

### Timed ref ramp (start → end by a future time)

Cooper: set a time with the ref so it increases until then.

| Flag | Role |
|------|------|
| `--ref-mcap START` | Now (ramp start) |
| `--ref-mcap-end END` | Finish mcap |
| `--ref-ramp-end SPEC` | `12h` / `2d` / ISO end |
| `--ref-price-end` | Absolute USD ramp (mcap preferred) |
| `--start-cooldown S` | Boot grace against instant clip |
| `--honor-last-fill` | Default on — seed CD from `last_fill_at` |

Linear each poll via `current_ref()`; after end, holds END. Heartbeat: `ref_ramping`, `ref_ramp_progress`, `ref_mcap_start/end`, `ref_ramp_end_ts`. Details: `references/ref-ramp.md`.

### Buy ref vs sell ref geometry

Independent per side (buy = dip anchor, sell = TP anchor).

| Setup | Behavior |
|-------|----------|
| **sell < buy** | Overlap band: both can fire same region (two-sided churn). Sells arm earlier. |
| **sell = buy** | Clean hinge. |
| **sell > buy** | Hold gap in the middle. |

Live MARV often: **buy 200k or ramp 175→200** · **sell 175k** → sells wait ~189k for +8% TP; buys paint under 200k. Explain before Cooper sets asymmetric refs.

### Restart auto-buy (why “it always buys a clip”)

`last_trade_ts=0` + armed dd → first loop skips cooldown → Jupiter buy. Not ladder math failure. Mitigations: honor-last-fill + `--start-cooldown 90`. Log: `seeded cooldown from last_fill_at` / `start-cooldown active` and no immediate SIGNAL.

### Buy + sell on separate wallets

```bash
# wallet A = buys
export DIP_BUYER_BUY_KEYPAIR=~/wallets/padre-sol-1.json
BUY_PUB=$(solana-keygen pubkey "$DIP_BUYER_BUY_KEYPAIR")

# wallet B = sells (different keyfile)
export DIP_BUYER_SELL_KEYPAIR=~/wallets/sell-hot.json
SELL_PUB=$(solana-keygen pubkey "$DIP_BUYER_SELL_KEYPAIR")

./scripts/botctl start --mint $MINT --side buy --style paint --run-id buy-paint \
  --live --confirm-live YES --keypair "$DIP_BUYER_BUY_KEYPAIR" \
  --sell-wallet "$SELL_PUB" --ref-mcap 100000 --prefer-dex pumpswap

./scripts/botctl start --mint $MINT --side sell --style normal --run-id sell-tp \
  --live --confirm-live YES --keypair "$DIP_BUYER_SELL_KEYPAIR" \
  --buy-wallet "$BUY_PUB" \
  --tp-ladder '0.25:0.30,0.50:0.40,1.0:0.30' --stop-loss 0.40 \
  --ref-mcap 100000 --prefer-dex pumpswap
```

Side-specific env aliases also honored by the bot: `DIP_BUYER_BUY_KEYPAIR`, `DIP_BUYER_SELL_KEYPAIR`, `DIP_BUYER_BUY_WALLET`, `DIP_BUYER_SELL_WALLET`.

## Sides

| Side | What | Wallet |
|------|------|--------|
| `buy` (default) | SOL→token dip ladder | buy keypair; sizes from wallet SOL (`budget-mode wallet` live default) or fixed `--budget` |
| `sell` | token→SOL TP ladder + optional `--stop-loss` | **different** sell keypair; sizes from token bag on that wallet |

Sell TP: `--tp-ladder 'gain:frac,...'` of **current bag**. Default = each rung **once** per run via `tp_hits`. With **`--tp-repeat`**, the same rung can fire again after cooldown (required for continuous slow drip / eventual exit without a dump rung).

**Drip-sell knobs (added to `dip_buyer.py` — prefer liq mode over bag-% TP):**

| Flag | Role |
|------|------|
| **`--sell-response liq`** | **Preferred.** Clip SOL ≈ `pool_sol × --sell-liq-frac`. Price only gates via `--sell-min-gain` (default 0 = at/above ref). Deeper book → larger clips; thin book → smaller. |
| `--sell-liq-frac F` | With liq: fraction of pool SOL per clip (default `0.005` = 0.5%; live often 0.005 + `--max-sell-sol 2`). |
| `--sell-min-gain G` | Min gain vs sell-ref before liq sells (0 = ≥ref; raise to wait for strength). |
| `--sell-response tp` | Legacy: bag % from TP ladder vs price (default if flag omitted). |
| `--tp-repeat` | TP mode: re-arm rungs after each fill. Not required for liq. |
| `--max-sell-sol N` | Cap each clip to ~N SOL **out** (scales token raw after quote). |
| `--max-sell-impact F` | If quote impact (0–1) still too high after shrink → cut further or `impact_skip`. |
| `--sell-frac-cap` | Hard max fraction of bag per clip (liq uses as probe upper bound before SOL shrink). |
| `--max-pool-frac` | Soft-caps sell SOL-out to `pool_sol * frac`. |
| `--max-per-hour` | Sell tracks SOL-out in `recent[]`. |
| `--cooldown` | Floor between clips (gentle: 180s+). |

Prove liq: boot `SELL MODE=liq: clip SOL ~= pool_sol * 0.0050`; signal `liq pool=196.68*0.0050=0.98SOL` + optional `+solcap`; heartbeat `sell_response=liq`, `sell_liq_frac`.

Impact from Jupiter may arrive as fraction (`0.20`) **or** percent (`20.3`); bot normalizes `>1.0 → /100` before caps.

**Full exit is NOT default without drip.** Once-per-rung residual stays forever unless a later rung has `frac≈1.0`, stop-loss, restart+dump, or **`--tp-repeat` + small SOL caps** grinding the bag down over time. Gentle ladders without repeat exit *less*. Say this before arming if Cooper says “sell all eventually.”

**% of bag ≠ gentle if bag is huge.** Real incident: 4% of ~600M MARV → ~24M tok → **~35 SOL / ~20% impact** on a ~170 SOL pool. Always pair tiny frac with **`--max-sell-sol 1`** (or lower) + **`--max-sell-impact 0.02`**. Fat inventory without SOL cap **will** chalk the chart.

### Slow paint-up + padre drip (preferred live profile)

Goal: buyers quietly paint green on dips; padre sells **only on strength** without re-nuking.

```bash
# Preferred: FREQ ladder — dd:cooldown_seconds, fixed clip (deeper → faster, not bigger)
FREQ='0.15:150,0.25:90,0.40:60,0.55:40,0.70:25'
# Legacy size ladder (only if explicitly wanted): SOFT='0.20:1.0,0.30:1.5,0.45:2.0,0.60:2.5,0.75:3.0'

# buyers — budget 500 ≈ whole-wallet (chain is real limit); buy-response freq + timing RNG
./scripts/botctl start --mint $MINT --side buy --style paint --run-id buy-paint-marv \
  --live --confirm-live YES --keypair ~/wallets/mrv.json \
  --sell-wallet "$(solana-keygen pubkey ~/wallets/padre-sol-1.json)" \
  --ref-mcap 175000 --budget 500 --prefer-dex pumpswap --budget-mode wallet \
  --buy-response freq --base-clip 1.0 --min-cooldown 20 --ladder "$FREQ" \
  --cooldown 180 --cooldown-jitter 0.30 --poll-jitter 0.5 \
  --max-clip 1.2 --max-pool-frac 0.025 --target-impact 0.02 \
  --max-per-hour 12 --slippage-bps 400

# third buy hot when sisters drain (import → mrv2.json first)
./scripts/botctl start --mint $MINT --side buy --style paint --run-id buy-paint-mrv2 \
  --live --confirm-live YES --keypair ~/wallets/mrv2.json \
  --sell-wallet "$(solana-keygen pubkey ~/wallets/padre-sol-1.json)" \
  --ref-mcap 175000 --budget 500 --prefer-dex pumpswap --budget-mode wallet \
  --buy-response freq --base-clip 1.0 --min-cooldown 20 --ladder "$FREQ" \
  --cooldown 180 --cooldown-jitter 0.30 --poll-jitter 0.5 \
  --max-clip 1.2 --max-pool-frac 0.025 --target-impact 0.02 \
  --max-per-hour 12 --slippage-bps 400

./scripts/botctl start --mint $MINT --side buy --style paint --run-id buy-paint-dip \
  --live --confirm-live YES --keypair ~/wallets/marv-dip-buyer.json \
  --sell-wallet "$(solana-keygen pubkey ~/wallets/padre-sol-1.json)" \
  --ref-mcap 175000 --budget 500 --prefer-dex pumpswap --budget-mode wallet \
  --buy-response freq --base-clip 0.5 --min-cooldown 20 --ladder "$FREQ" \
  --cooldown 180 --cooldown-jitter 0.30 --poll-jitter 0.5 \
  --max-clip 0.6 --max-pool-frac 0.02 --target-impact 0.018 \
  --max-per-hour 8 --slippage-bps 400

# padre SELL — stop any padre BUY first + null old buy heartbeat wallet
# null wallet claim (keep spent history):
# python3 -c 'import json;from pathlib import Path
# p=Path("runs/<m8>/buy-paint-padre/heartbeat.json"); d=json.loads(p.read_text())
# d["wallet"]=None; d["status"]="stopped"; p.write_text(json.dumps(d,indent=2)+"\n")'

# PREFERRED: liquidity-proportional drip (size ∝ pool, not bag% / not price ladder)
./scripts/botctl start --mint $MINT --side sell --style absorb --run-id sell-absorb-padre \
  --live --confirm-live YES --keypair ~/wallets/padre-sol-1.json \
  --buy-wallet "$(solana-keygen pubkey ~/wallets/mrv.json)" \
  --ref-mcap 175000 --prefer-dex pumpswap \
  --sell-response liq --sell-liq-frac 0.005 --sell-min-gain 0 \
  --sell-frac-cap 0.05 \
  --max-sell-sol 2.0 --max-sell-impact 0.02 --max-pool-frac 0.01 \
  --max-per-hour 6 --cooldown 180 --cooldown-jitter 0.30 --poll-jitter 0.5 \
  --start-cooldown 60 --slippage-bps 300 --min-sell-tokens 1000

# LEGACY TP bag% drip (only if Cooper wants price-rung sells):
#   --sell-response tp --tp-ladder '0.08:0.02,…' --tp-repeat --max-sell-sol 1.0 …
```

- **Default sell path = liq**, not TP. Cooper asked for size proportional to liquidity instead of price.
- Sell ref often **lower** than buy ref (e.g. buy ramp 200→250, sell 175k) so buys paint dips while sells only gate at/above sell-ref.
- No `--stop-loss` on the gentle path.
- Prove liq sell: boot `SELL MODE=liq` + `sell_response=liq sell_liq_frac=0.005`; signals `liq pool=…`; not stuck on `below first TP rung`.
- Prove jitter: `sell cooldown roll`; cmdline `--cooldown-jitter`.
- If impact still high: **stop sell**, lower `--sell-liq-frac` / `--max-sell-sol` / impact — do not push through.
- **All live restarts failing** with `ValueError: badly formed help string` → unescaped `%` in argparse help → escape `%%`.

**“Sell soon” while under buy-ref:** sell-ref is independent. With **liq** + `--sell-min-gain 0`, sells arm once spot ≥ sell-ref (no need for +8% TP). Still pair with liq-frac + SOL/impact caps or fat bags chalk the chart.

**Flip buy→sell same pubkey:** stop the buy run_id first. Sibling scan reads **every** mint heartbeat `wallet` including **stopped** hearts — clear/null `wallet` on the old buy heartbeat (keep spent history) or sell start dies with `WALLET SEPARATION: … sibling buy run at …/buy-paint-padre`. Buy bots' `--sell-wallet` annotations alone do not block; heartbeat `wallet` does.

## Styles (buy risk levers)

| Style | Intent |
|-------|--------|
| `absorb` | Quiet fill, low impact (~2% pool) |
| `normal` | Balanced |
| `paint` | Visible green wicks (~10% pool + `--target-impact`) |

Overrides: `--max-clip`, `--max-pool-frac`, `--max-per-hour`, `--cooldown`, `--target-impact`, `--ladder`, **`--buy-response {size,freq}`**, **`--base-clip`**, **`--min-cooldown`**.

**`--buy-response freq` (preferred when Cooper says dips should affect frequency not size):**

- Ladder is `dd:cooldown_seconds` (example `0.15:150,0.40:60,0.70:25`).
- Clip = `--base-clip` every fire (pool/impact/hour still soft-cap).
- Heartbeat fields: `buy_response`, `base_clip_sol`, `effective_cooldown_s`.
- Log boot: `BUY RESPONSE=freq: fixed clip=…`; signal: `freq cd=60s`.
- Floors: `max(min_cooldown, ladder_cd)`; non-positive ladder value falls back to `--cooldown`.

## Live arming gate

Requires all of: `--live`, `--confirm-live YES`, keypair (`--keypair` or env).
Live sell also requires `--buy-wallet`.

## Heartbeat statuses (not crashes)

- `wallet_low` — idle until SOL top-up (buy + wallet mode)
- `budget_exhausted` — fixed budget done
- `bag_empty` — sell wallet has no tokens
- `filled` / `running` / `stopped` — normal

## Common failure → fix

| Symptom | Cause | Fix |
|---------|-------|-----|
| `already running pid=… run_dir=…` | Same run_id still up | `botctl stop --run-dir …` then start; or new `--run-id` |
| `another instance holds …/bot.lock` | Flock held | stop holder; don't start second clone same run dir |
| stale pid / dead process, list says stopped | interrupted start left pid file | `botctl stop` cleans; if lock zombies, stop again before start |
| `buy and sell wallet must differ` / `WALLET SEPARATION: sibling buy run` | Same pubkey live **or** stopped buy heartbeat still has `wallet` set | stop buy; null `wallet` on old buy heartbeat; pass distinct `--buy-wallet` on sell |
| live sell missing buy-wallet | botctl/start gate or fill-time check | pass `--buy-wallet $BUY_PUB` |
| `WALLET LOW` with big `spent` and SOL still on-chain | ceiling ≤ spent in state (wallet mode min of chain and budget-spent) | raise `--budget` way above wallet (Cooper default **500**) so chain SOL is the limit; top-up then auto-extends. Top-up alone does **not** extend if hard ceiling still binds |
| freq mode `clip rounded to 0` with dust wallet | `--base-clip` > available SOL − fee | lower `--base-clip` (e.g. 0.5) or fund wallet |
| seller farming buys / sticky dump | buy ref far above spot + dual buyers + short CD / fixed period | use `--buy-response freq` + small base-clip + hour/min-cd + **`--cooldown-jitter` / `--poll-jitter`**; or stop buys; see exploitability section |
| every bot exits instantly, help traceback `%` | argparse help has bare `%` (e.g. `+/-25%`) on Py 3.14 | escape as `%%` in help= strings; `py_compile` is not enough — `--help` must run clean |
| bots fire on exact metronome after each fill | no jitter / jitter=0 | restart with `--cooldown-jitter 0.25+` — sample once per wait, clear after fill |
| **every ref bump / restart instantly market-buys** | `last_trade_ts=0` + spot still under buy-ref | `--start-cooldown 90` + default honor-last-fill; log must show seed lines |
| sell TP never fires after raising sell-ref | gain vs **new** sell ref = 0 (tp mode) | first TP needs spot ≥ sell_ref×(1+first_rung); **or switch `--sell-response liq --sell-min-gain 0`** to sell at/above ref |
| liq sell still logs `below first TP rung` | old binary / flag not passed | prove cmdline has `--sell-response liq`; boot must say `SELL MODE=liq` |
| buy and sell both active mid-band | sell_ref < buy_ref and spot in between | intentional overlap; raise sell-ref / lower buy-ref / accept two-sided |
| sell free bag shrinks after Streamflow lock | lock leaves free ATA | expected; drip only unlocked sleeve; see `references/streamflow-padre-lock.md` |
| sell TP never fires | gain vs **sell** ref = 0 (spot under ref) | lower sell `--ref-mcap` / raise spot; or liq mode with min-gain 0 |
| first “gentle” sell nukes chart | frac×huge bag ≫ pool, no SOL/liq cap | **stop sell**; restart `--sell-response liq --sell-liq-frac 0.005 --max-sell-sol 1 --max-sell-impact 0.02`; check `liq pool=` / `+solcap` |
| sell only one TP then idle with bag left | default once-per-rung `tp_hits` | `--sell-response liq` (continuous) or `--tp-repeat` / final rung `frac=1` |
| status update missing wallet tails | Cooper wants last-4 of each addr | always suffix `…fXjy` / `…Es19` etc. in fleet tables |
| `impact_skip` spam | pool thin / cap still hot | lower max-sell-sol; wait for deeper book; don't raise frac |
| monitor cron reject absolute script path | Hermes requires `~/.hermes/scripts/` relative | wrapper `runpy` → repo script; cron `script=name.py` |
| Can't run two bots same market | Expected **same run_id**; dual needs different `--run-id`/`--side`/`--style` | use nested multi-strategy layout |

## Paper smoke

```bash
./scripts/botctl start --mint $MINT --side buy --style paint --run-id buy-paint-paper \
  --paper --ref-mcap 100000 --budget 5 --prefer-dex pumpswap
# or once:
.venv/bin/python dip_buyer.py --mint $MINT --side buy --style paint --run-id smoke \
  --paper --ref-mcap 100000 --budget 3 --once --prefer-dex pumpswap
```

## Key paths (current roster)

| File | Pubkey | Role (current ops) |
|------|--------|------|
| `~/wallets/mrv2.json` | `A3KwFS…` | Soft-paint **buy** — `buy-paint-mrv2` (main dry-powder when sisters drain) |
| `~/wallets/mrv.json` | `AZYsGo…` | Soft-paint **buy** — `buy-paint-marv` |
| `~/wallets/marv-dip-buyer.json` | `PWbrhU…` | Soft-paint **buy** — `buy-paint-dip` |
| `~/wallets/padre-sol-1.json` | `GKzKZW…` | **Sell** bag — `sell-absorb-padre` (himitsu `sol-1` / Padre). Stop any padre **buy** run before arming sell. |

Always `solana-keygen pubkey` before wiring. Never leave secrets in `/tmp`. Live fleet often: **buy ref 200k or ramp 175→200** · **sell ref 175k** (overlap only if spot sits between). Padre free ATA after Streamflow lock is what sell sees — not escrowed locked bag.

### Cooper preference: paint up slowly, sell slowly on strength

Wants **chart-paint upward** without dual full-paint spray, and padre inventory **dripped** so sells don't own the dip. Prefer freq buys + **`--sell-response liq`** (see Sides + `references/sell-response-liq.md`). Status updates should include **last-4 chars** of each wallet address.

**Default buy response = freq, not size.** Deeper dips should **fire more often**, not buy bigger clips. In `dip_buyer.py`:

| Flag | Meaning |
|------|---------|
| `--buy-response freq` | Ladder second field = **cooldown seconds** (deeper → smaller numbers). Clip size stays fixed. |
| `--base-clip N` | Fixed SOL per buy in freq mode (mrv ~1.0, thin sister ~0.5). |
| `--min-cooldown S` | Floor CD (default 15; live often 20). |
| `--cooldown-jitter J` | Multiplicative RNG on each CD interval (default **0.25** = ±25%; live often **0.30**). Sampled **once per wait**, held until fill — countdown stable, period unpredictable. `0` disables. |
| `--poll-jitter S` | Extra RNG seconds on wait sleeps (default **0.35**; live often **0.5**). Caps at poll. Breaks fixed wake grids. |
| `--buy-response size` | Legacy: ladder second field = SOL clip (grows with depth). Default if flag omitted. |

**Timing unpredictability (when Cooper says “so it can’t be predicted”):** always pass non-zero `--cooldown-jitter` on live buy *and* sell. Log: `cooldown roll base=60.0s -> 70.5s` then next `-> 44.9s`; sell `sell cooldown roll base=180.0s -> …`. Heartbeat exposes `cooldown_jitter` + `effective_cooldown_s` (the *scheduled* jittered value). Coarse band still follows depth (deeper→faster); only exact fire-second is blurred. argparse help must escape `%` as `%%` or Python 3.14 raises `badly formed help string` and **all bots fail to start**.

```bash
# freq ladder: dd:cooldown_seconds (NOT sol size) — deeper → faster + RNG timing
FREQ='0.15:150,0.25:90,0.40:60,0.55:40,0.70:25'

./scripts/botctl start --mint $MINT --side buy --style paint --run-id buy-paint-marv \
  --live --confirm-live YES --keypair ~/wallets/mrv.json \
  --sell-wallet "$(solana-keygen pubkey ~/wallets/padre-sol-1.json)" \
  --ref-mcap 150000 --budget 500 --prefer-dex pumpswap --budget-mode wallet \
  --buy-response freq --base-clip 1.0 --min-cooldown 20 --ladder "$FREQ" \
  --cooldown 180 --cooldown-jitter 0.30 --poll-jitter 0.5 \
  --max-clip 1.2 --max-pool-frac 0.025 --target-impact 0.02 \
  --max-per-hour 12 --slippage-bps 400

# thin sister: same FREQ ladder, smaller fixed clip, same jitter
./scripts/botctl start … --run-id buy-paint-dip --keypair ~/wallets/marv-dip-buyer.json \
  --buy-response freq --base-clip 0.5 --min-cooldown 20 --ladder "$FREQ" \
  --cooldown 180 --cooldown-jitter 0.30 --poll-jitter 0.5 \
  --max-clip 0.6 --max-per-hour 8 --budget 500 --ref-mcap 175000 …

# when mrv/dip dry, add mrv2 as lead buyer (same FREQ/175k/jitter)
./scripts/botctl start … --run-id buy-paint-mrv2 --keypair ~/wallets/mrv2.json \
  --buy-response freq --base-clip 1.0 --ref-mcap 175000 --budget 500 …
```

Prove: boot log `BUY RESPONSE=freq` + `cooldown_jitter=+/-30% poll_jitter=0.50s`; signals `freq cd=70s` (jittered, not bare ladder); regen rolls after each fill; heartbeat `buy_response=freq`, `base_clip_sol`, `effective_cooldown_s`, `cooldown_jitter`.

### Market direction cron (holders / liq / external liq)

Cooper wants a recurring human read without babysitting:

- Script: `scripts/market_direction_report.py`
- Wrapper: `~/.hermes/scripts/marv_direction_report.sh` → `himitsu exec alchemy-api-key -- …`
- Cron: `0 */4 * * *`, deliver Slack DM, **self-expires ~10d** via `runs/.market_direction_state.json` `expires_at`
- Scores whether pool/holders/mcap move **beyond** our bot deploy (Alchemy top bags + fleet spent/recv)

Details: `references/market-direction-report.md`. Pump homepage vs post-grad discovery: `references/pumpfun-homepage-visibility.md`.

**Size-mode soft ladder** (only if Cooper explicitly wants bigger clips deeper — not default now):

```bash
--style paint --buy-response size --ladder '0.20:1.0,0.30:1.5,0.45:2.0,0.60:2.5,0.75:3.0' \
  --max-clip 2.5 --max-pool-frac 0.03 --target-impact 0.025 \
  --max-per-hour 8 --cooldown 120 --slippage-bps 400
```

### Wallet = ceiling: set `--budget` biiiig (e.g. 500)

Cooper often wants “use the whole wallet.” In `budget-mode wallet`, avail = `min(wallet_sol − fee_reserve, budget − spent)`. If `spent` hits an old low budget (99/130/16) while SOL still sits on-chain, status is `wallet_low` / rem=0 **even with 20+ SOL left** — not an empty wallet.

- Restart with **`--budget 500`** (or any number ≫ wallet) so the hard ceiling is de facto chain balance + fee reserve.
- Top-ups then auto-extend buys without another budget bump.
- `spent` still accumulates in state (history); that is fine. Don't confuse spent counter with remaining deployable SOL.
- Thin wallets (dip ~0.5–3 SOL): set `--base-clip` ≤ available or clip rounds to 0 /$ idle.

Diagnosing “too aggressive” / limited buys:

1. **Budget bind first** — spent ≥ budget while wallet_sol > fee_reserve → raise budget, not style.
2. Else sum dual `max_per_hour`, shallow `level_hits`, fills_last_1h, avg impact, freq `effective_cooldown_s`.
3. Dual full-paint size-mode ≈ **70 SOL/hr** theoretical; soft dual size ≈ **14–18**; freq dual ≈ `hour caps` with fixed ~0.5–1 SOL clips.
4. Raising buy ref while spot is below it re-arms deep dd and can dump remainder immediately — stop first if undesirable.

When pausing aggression: **`botctl stop` the process** (buys *and/or* sell) so top-ups / TPs cannot auto-resume. Budget ceiling alone is not a pause.

### Reactive-buy exploitability (seller-made dips)

Yes — robots are **predictable market-buy liquidity**, not resting bids. Seller (including your own padre drip to a degree) can:

1. Hold price under a ladder rung vs fixed buy ref → bots keep Jupiter-buying on poll + CD.
2. **Sticky deep dd** (e.g. ref 150k, spot 65k) = nearly continuous arming; attack is time + CD, not pin-point spoofing.
3. Dual buyers ≈ 2× that flow on the same mint/ref.
4. Sell bounce / sandwich on public Jupiter routes.

Mitigations already preferred: **freq not size** (clip stays small, only CD shortens), **cooldown/poll jitter** (destroys exact fire-second prediction; does not hide the depth→band map), deeper first rung, hour caps, long min CD, soft impact/pool frac. Optional not yet coded: recover-or-pause, velocity filter, single-buyer while selling, trailing buy ref. If Cooper asks “are they susceptible?” — answer yes, explain sticky-dd drain, point at freq+small clip+hour cap+jitter as the live defense, offer stop if worried.

**Same-mint buy + sell interaction:** buy≠sell keys stop wash *on one account*, not “you buying your own sell pressure on the pool.” Padre drip that prints dd vs **buy** ref will re-arm kids.

### Monitor (cron)

```bash
# local check (quiet on health; prints + exit 1 on alert)
.venv/bin/python scripts/monitor_slow_paint.py
.venv/bin/python scripts/monitor_slow_paint.py --json

# Hermes forever cron (script must live under ~/.hermes/scripts/ — absolute repo
# paths are rejected). Wrapper:
#   ~/.hermes/scripts/sol_dip_slow_paint_monitor.py → runpy repo monitor
# schedule: */5 * * * * · no_agent=true · deliver slack:D0AK02MKFRP ·
# workdir=~/git/darkmatter/sol-dip-buyer · repeat forever (repeat=0 / cron form)
```

Alerts: dead/stale run heartbeats, sell `last_impact` / `last_sol_out` over caps, drip hour SOL-out over cap (ignores the one-shot pre-drip 35 SOL fill), spot dump coincident with rising sell `received_sol`. For `no_agent` watchdogs: empty stdout = healthy silence.

## Token-2022 MARV transfers (spl-token)

MARV mint `6xycyGrZ…pump` is **Token-2022** (`TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb`), not classic Tokenkeg. Bare `spl-token transfer $MINT …` fails or hits the wrong program — always pass program id + Alchemy RPC when public RPC 429s:

```bash
PROG=TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb
MINT=6xycyGrZRxXcsAoX722kZwvy9evQEJ69d36puN15pump
RPC=$(himitsu exec alchemy-api-key -- sh -c 'k="$ALCHEMY_API_KEY"; case "$k" in http*) echo "$k";; *) echo "https://solana-mainnet.g.alchemy.com/v2/$k";; esac')

# aprove gift of 1 MARV from top bag (padre) → known creator (on-chain proof, no TG doxx)
spl-token transfer --program-id "$PROG" \
  --owner ~/wallets/padre-sol-1.json --fee-payer ~/wallets/padre-sol-1.json \
  --url "$RPC" --fund-recipient --allow-unfunded-recipient \
  "$MINT" 1 T5kYFsDUowtUunXsQYRxF9vNVApryD2wcFQZuRPuq5c
```

Creator/dev (pump + gecko): `T5kYFsDUowtUunXsQYRxF9vNVApryD2wcFQZuRPuq5c`. Public socials: TG `@pepedevsolana`, X `@puffbear_`. See `references/community-gift-dev.md` for throwaway contact + gift framing.

## Holders / airdrops / contact (not bot features)

- **Dip/sell bots do not raise holder count.** Few named hots deepen bags; Gecko “holders” only moves on new owner addresses. Answer: bot can paint/drip; holders need external buys or deliberate distribution.
- **Refuse multi-wallet holder farms / dust to burners** (wash optics + already-concentrated supply). Same-name multi-hot **buy** for size/verify stays OK.
- **Gift unlocked inventory to aligned locked-dev for *them* to airdrop (you don't run drop / don't dictate drop terms)** is an allowed *human* path when Cooper decides. Identity: personal TG/X = doxx. Use **MySudo number + new TG account on phone** (MySudo is phone-only; Desktop Telegram here is **@ Coop** personal — never DM project devs from it). Optional prior on-chain proof: 1 MARV from top holder → creator as above, then throwaway TG cites that sig.
- Detail + draft message: `references/community-gift-dev.md`.

## Pitfalls

- **Don't** start a second process to “add size” on the same run — stop/retune or top up wallet.
- **Don't** assume sister strategies share spent/budget — each run has its own `state.json`.
- **Don't** use the buy hot wallet for TP sells — separation is policy + enforced code path.
- Legacy flat `runs/<mint8>/` without nested children still works for one bot; once any nested run exists, prefer nested paths for new starts.
- `botctl status` with no args / `--all` → `list`. `--mint` alone lists all strategies under that mint.
- **Hermes terminal + Python `&`:** bare `&` in `python3 -c '… a & b …'` or heredoc is rejected/misparsed as shell backgrounding. Use `+`/`//` instead of bitwise `&`/`|`, or write a temp `.py` file. Same trap hit when doing base58 import converts.
- **Wipe world-readable import sources** (`/tmp/key`) only after `solana-keygen pubkey` succeeds on the new `~/wallets/*.json`.
- **Raising `--ref-mcap` on a running live bot needs stop+restart with the flag** — editing `state.json` alone is racey while the process holds it; use override-on-start. Confirm both runs via heartbeat `ref_mcap_usd` before walking away.
- Dual same-strategy runs must keep **distinct** `--run-id`s and matching `--keypair`/`--sell-wallet` pairs on every restart or botctl will either refuse lock or flip wallets.
- **`--sell-wallet` ≠ selling.** Buy runs hang that flag for the opposite-pubkey guard only. Cooper regularly reads it as “padre is selling” — answer with side + tokens_sold + no sell PID.
- **Run spent survives wallet swap.** Replacing marv's key with `mrv` kept ~90+ SOL spent on `buy-paint-marv`; remaining budget = ceiling − state spent, not new-wallet balance alone. Balance questions need on-chain SOL **and** bot spent counters.
- On-chain inventory can lag bot identity: long-run tokens often sit on whichever buy wallet filled earlier (e.g. padre ~600M MARV vs brand-new mrv bag).

## References

- `references/dual-strategy.md` — design notes + verify checklist from the multi-run cutover
- `references/ref-retarget.md` — live 100k→150k dual paint restart notes (MARV mint example)
- `references/ref-ramp.md` — timed linear ref ramp, restart cooldown seed, buy/sell ref geometry
- `references/wallet-roster.md` — current hot keys/roles + sell-wallet semantics + buy→sell flip
- `references/sell-tp-gentle.md` — TP once-per-rung residual, sell-soon lower ref, fat-bag impact
- `references/sell-response-liq.md` — preferred sell mode: clip SOL ∝ pool; price only gates
- `references/slow-paint-drip.md` — slow paint-up buyers + padre drip sell + monitor cron
- `references/buy-response-freq.md` — dips→frequency not size: flags, ladder shape, budget 500, exploit notes
- `references/cooldown-jitter.md` — once-per-wait RNG on buy/sell CDs + poll jitter; argparse `%%` pitfall; prove via log rolls
- `references/market-direction-report.md` — 4h/10d Slack direction cron + Alchemy holders/liq (himitsu `alchemy-api-key`)
- `references/pumpfun-homepage-visibility.md` — what moves Pump.fun homepage / KoTH / post-grad discovery (not a bot flag)
- `references/community-gift-dev.md` — throwaway TG (MySudo), gift framing to locked MARV dev, Token-2022 1-unit proof send, no drop-term dictation
- `references/streamflow-padre-lock.md` — lock top bag on Streamflow; free ATA vs sell bot; optics vs drip sleeve
