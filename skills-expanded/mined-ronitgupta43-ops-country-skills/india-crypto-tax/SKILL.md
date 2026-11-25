---
name: india-crypto-tax
description: Indian crypto (VDA) tax - flat 30% on gains, no loss set-off, 1% TDS on sales, Schedule VDA and the 2026 reporting penalties, from WazirX, CoinDCX, Binance or wallet exports. Use when an Indian asks "how much tax on my crypto", "crypto TDS", "can I set off crypto loss", "Schedule VDA", or uploads exchange exports.
---

# Crypto (VDA) tax in India, Tax Year 2026-27

## Ledger
Build the ledger as in crypto-portfolio (same columns, prices in INR). Then:
```
python crypto.py ledger.csv in
```
It prints per tax year (April to March): taxable gains, tax at 30% + 4% cess, losses that can't be used, estimated TDS, and staking income.

## Rules it applies
- Gains on transferring crypto, NFTs and other VDAs: flat 30% + 4% cess (plus surcharge at high incomes). Old section 115BBH; from 1 April 2026, section 194 of the Income-tax Act, 2025.
- Only the cost of acquisition is deductible. No deduction for fees, internet, or other expenses. The 12 lakh rebate and basic exemption don't apply to this income.
- No loss set-off at all: a loss on one coin can't reduce a gain on another coin or any other income, and can't be carried forward. The script ignores losses for this reason.
- Each sale and each crypto-to-crypto swap is a separate transfer.
- 1% TDS on sale value (old 194S, now section 393): the exchange usually deducts it. Thresholds: Rs 50,000 a year for "specified persons" (most individuals without business income), Rs 10,000 otherwise. TDS is credit against your tax; check Form 26AS/AIS. P2P buyers may have to deduct it themselves.
- Cost method: the script uses FIFO across all wallets. Say this to the user; keep it consistent every year.
- Staking/rewards: taxed as income at slab rates when received (some CAs treat the cost of those coins as zero later; flag this).

## Reporting
- Report every VDA transfer in Schedule VDA of the ITR (date bought, date sold, cost, proceeds).
- From 1 April 2026 there are penalties for crypto reporting lapses (per-day for non-filing and a fixed penalty for incorrect information), so complete records matter.
- Coins held on foreign exchanges or in foreign wallets may also need Schedule FA if the user is a resident and ordinarily resident.

End with: estimate only; confirm with a CA.

## Calculator code
If `crypto.py` isn't available (some apps keep only SKILL.md), save this code as `crypto.py` and run it as above. Don't do the arithmetic by hand.

<!-- embed: ../../../crypto/skills/crypto-portfolio/scripts/crypto.py -->
```python
"""Crypto ledger: holdings and tax reports for Canada (ca), India (in) and the US (us).
Usage: python crypto.py ledger.csv summary [--prices prices.csv]
       python crypto.py ledger.csv ca|in|us

ledger.csv columns: date,type,asset,qty,price,fee,exchange,to
  date      YYYY-MM-DD
  type      buy | sell | income (staking, airdrop, mining, rewards) | transfer (between your own wallets)
  price     value of ONE unit in your tax currency (CAD / INR / USD) at that moment
  fee       fee in your tax currency (can be blank)
  exchange  where it happened (Coinbase, Binance, Ledger...); for transfer, the wallet it left
  to        transfer only: the wallet it arrived in
Crypto-to-crypto swap = two rows on the same date: sell the coin you gave up, buy the coin you got, both at fiat value.
prices.csv (optional): asset,price  current price per unit, for unrealized profit/loss.
"""
import csv
import sys
from collections import defaultdict, deque
from datetime import date


def load(rows):
    out = []
    for r in rows:
        out.append(dict(d=date.fromisoformat(r["date"].strip()[:10]), t=r["type"].strip().lower(), a=r["asset"].strip().upper(),
                        q=float(r["qty"]), p=float(r.get("price") or 0), f=float(r.get("fee") or 0),
                        w=(r.get("exchange") or "").strip(), to=(r.get("to") or "").strip()))
    return sorted(out, key=lambda x: (x["d"], x["t"] != "buy"))


def summary(tx):
    """Pooled average cost per asset across all wallets."""
    q, cost = defaultdict(float), defaultdict(float)
    for x in tx:
        if x["t"] in ("buy", "income"):
            q[x["a"]] += x["q"]; cost[x["a"]] += x["q"] * x["p"] + (x["f"] if x["t"] == "buy" else 0)
        elif x["t"] == "sell":
            avg = cost[x["a"]] / q[x["a"]] if q[x["a"]] else 0
            q[x["a"]] -= x["q"]; cost[x["a"]] -= avg * x["q"]
    return {a: (q[a], cost[a]) for a in q if q[a] > 1e-12}


def canada(tx):
    """Average cost (ACB) pooled across all wallets; superficial loss flag; staking etc. as income."""
    q, cost = defaultdict(float), defaultdict(float)
    gains, income, flags = defaultdict(float), defaultdict(float), []
    for x in tx:
        a, y = x["a"], x["d"].year
        if x["t"] in ("buy", "income"):
            q[a] += x["q"]; cost[a] += x["q"] * x["p"] + (x["f"] if x["t"] == "buy" else 0)
            if x["t"] == "income":
                income[y] += x["q"] * x["p"]
        elif x["t"] == "sell":
            if x["q"] > q[a] + 1e-9:
                raise ValueError(f"{x['d']}: selling {x['q']} {a}, only {q[a]} recorded; add the missing buys")
            acb = cost[a] / q[a] * x["q"]
            g = x["q"] * x["p"] - x["f"] - acb
            q[a] -= x["q"]; cost[a] -= acb; gains[y] += g
            # ponytail: flags a rebuy within 30 days either side; doesn't compute the exact denied amount
            if g < 0 and any(o["a"] == a and o["t"] in ("buy", "income") and abs((o["d"] - x["d"]).days) <= 30 and o is not x for o in tx):
                flags.append(f"{x['d']} {a}: loss {-g:,.2f} may be a superficial loss (rebought within 30 days)")
    return gains, income, flags


def fifo(tx, per_wallet):
    """FIFO lots. per_wallet=True for the US (basis tracked per wallet since 2025)."""
    lots = defaultdict(deque)  # key -> [qty, unit_cost, acquired]
    sales, income, tds = [], defaultdict(float), defaultdict(float)
    for x in tx:
        key = (x["a"], x["w"]) if per_wallet else (x["a"],)
        if x["t"] in ("buy", "income"):
            lots[key].append([x["q"], x["p"] + x["f"] / x["q"] * (x["t"] == "buy" and per_wallet), x["d"]])
            if x["t"] == "income":
                income[x["d"]] += x["q"] * x["p"]
        elif x["t"] == "sell" or (x["t"] == "transfer" and per_wallet):  # transfers don't matter without per-wallet basis
            left, dest = x["q"], (x["a"], x["to"]) if per_wallet else None
            while left > 1e-12:
                if not lots[key]:
                    raise ValueError(f"{x['d']}: moving {x['q']} {x['a']} from '{x['w']}' but not enough recorded there; add the missing buys or transfers")
                lot = lots[key][0]; used = min(left, lot[0])
                if x["t"] == "sell":
                    unit = x["p"] - (x["f"] / x["q"] if per_wallet else 0)  # India: no deduction except cost
                    sales.append((x["d"], x["a"], used, used * unit, used * lot[1], lot[2]))
                else:
                    lots[dest].append([used, lot[1], lot[2]])
                    lots[dest] = deque(sorted(lots[dest], key=lambda l: l[2]))  # first in = earliest acquired
                lot[0] -= used; left -= used
                if lot[0] <= 1e-12:
                    lots[key].popleft()
            if x["t"] == "sell":
                tds[x["d"]] += x["q"] * x["p"] * 0.01
    return sales, income, tds


def fy_india(d):
    return d.year if d.month >= 4 else d.year - 1


def india(tx):
    sales, income, tds = fifo(tx, per_wallet=False)
    out = defaultdict(lambda: {"gains": 0.0, "losses_ignored": 0.0, "tds": 0.0, "income": 0.0})
    for d, a, q, proceeds, cost, _ in sales:
        g = proceeds - cost
        out[fy_india(d)]["gains" if g > 0 else "losses_ignored"] += g
    for d, v in tds.items():
        out[fy_india(d)]["tds"] += v
    for d, v in income.items():
        out[fy_india(d)]["income"] += v
    return out


def us(tx):
    sales, income, _ = fifo(tx, per_wallet=True)
    out = defaultdict(lambda: {"short": 0.0, "long": 0.0, "income": 0.0})
    for d, a, q, proceeds, cost, acquired in sales:
        long_term = (d.year, d.month, d.day) > (acquired.year + 1, acquired.month, acquired.day)
        out[d.year]["long" if long_term else "short"] += proceeds - cost
    for d, v in income.items():
        out[d.year]["income"] += v
    return out


def _selftest():
    rows = [dict(date="2025-01-10", type="buy", asset="BTC", qty="1", price="40000", fee="0", exchange="Coinbase", to=""),
            dict(date="2025-03-01", type="income", asset="ETH", qty="1", price="3000", fee="", exchange="Coinbase", to=""),
            dict(date="2025-06-01", type="buy", asset="BTC", qty="1", price="60000", fee="0", exchange="Binance", to=""),
            dict(date="2025-07-01", type="transfer", asset="BTC", qty="1", price="0", fee="", exchange="Coinbase", to="Binance"),
            dict(date="2026-02-01", type="sell", asset="BTC", qty="1", price="70000", fee="0", exchange="Binance", to="")]
    tx = load(rows)
    g, inc, _ = canada(tx)
    assert g[2026] == 20000 and inc[2025] == 3000          # sold at 70k vs average cost 50k
    i = india(tx)
    assert i[2025]["gains"] == 30000 and i[2025]["tds"] == 700  # FIFO: the 40k coin; FY 2025-26
    u = us(tx)
    assert u[2026]["long"] == 30000 and u[2026]["short"] == 0  # Binance holds the Jan coin (moved in) and the Jun coin; FIFO sells Jan first
    assert summary(tx)["ETH"] == (1, 3000)


if __name__ == "__main__":
    _selftest()
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    with open(sys.argv[1], newline="") as f:
        tx = load(list(csv.DictReader(f)))
    mode = sys.argv[2]
    if mode == "summary":
        prices = {}
        if "--prices" in sys.argv:
            with open(sys.argv[sys.argv.index("--prices") + 1], newline="") as f:
                prices = {r["asset"].strip().upper(): float(r["price"]) for r in csv.DictReader(f)}
        tot_cost = tot_val = 0
        for a, (q, c) in sorted(summary(tx).items()):
            line = f"{a}: {q:g} units, cost {c:,.2f} (avg {c / q:,.4f})"
            if a in prices:
                v = q * prices[a]; tot_val += v
                line += f", value {v:,.2f}, unrealized {v - c:+,.2f} ({(v - c) / c:+.1%})" if c else f", value {v:,.2f}"
            tot_cost += c
            print(line)
        print(f"Total cost {tot_cost:,.2f}" + (f", total value {tot_val:,.2f}, unrealized {tot_val - tot_cost:+,.2f}" if prices else ""))
    elif mode == "ca":
        g, inc, flags = canada(tx)
        for y in sorted(set(g) | set(inc)):
            print(f"{y}: capital gain/loss {g[y]:,.2f} CAD (taxable half {max(g[y], 0) / 2:,.2f}); staking/rewards income {inc[y]:,.2f} CAD")
        for line in flags:
            print("WARNING:", line)
        print("If you trade often, CRA may treat gains as business income (100% taxable). Foreign-exchange holdings costing over $100,000 need form T1135.")
    elif mode == "in":
        for fy, v in sorted(india(tx).items()):
            print(f"FY {fy}-{str(fy + 1)[2:]}: taxable VDA gains Rs {v['gains']:,.0f}, tax @30% + 4% cess Rs {v['gains'] * 0.312:,.0f}; "
                  f"losses that can't be set off Rs {-v['losses_ignored']:,.0f}; TDS est. Rs {v['tds']:,.0f} (check 26AS); "
                  f"staking/rewards income Rs {v['income']:,.0f} (taxed at slab rates)")
    elif mode == "us":
        for y, v in sorted(us(tx).items()):
            print(f"{y}: short-term {v['short']:,.2f} USD, long-term {v['long']:,.2f} USD, staking/rewards income {v['income']:,.2f} USD")
        print("Long-term is taxed at 0/15/20%, short-term and income at your bracket (see us-income-tax).")
    else:
        sys.exit("mode must be summary, ca, in or us")
```
