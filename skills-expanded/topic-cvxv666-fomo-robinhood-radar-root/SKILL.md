---
name: fomo-agent
description: FOMO Robinhood Radar — a research watchlist of Robinhood Chain memecoin traders discovered through fomo.family. Use when the user asks who the good traders are, who moved between active/watch/dropped, what the cohort is buying or holding right now, to analyse a token or a trader, to score or rescore wallets in chat, or to check what is quietly broken in the pipeline.
---

# FOMO Robinhood Radar

Reads the SQLite database the pipeline builds and runs its CLI. Everything below is research
output about public on-chain activity: what other wallets have already done, and how well they have
done it.

## When to trigger

- "покажи топ-трейдеров" / "who are the good traders"
- "кого добавили в active" / "who dropped and why"
- "что покупают прямо сейчас" / "what is the cohort buying"
- "разбери токен X" / "analyze this token" / "who holds this"
- "разбери трейдера X" / "what is this trader doing"
- "проскорь кошельки" / "пересчитай баллы" / "score the pending wallets"
- "что сломалось" / "is the pipeline healthy"

## Where the data lives

Two databases, and picking the wrong one is the most common mistake:

| | path | what is in it |
|---|---|---|
| **live** | `root@<server>:/opt/fomoradar/fomo_agent.db` | everything: collection runs every 30 min, the tape, the scores |
| local | `./fomo_agent.db` | whatever this machine last collected — usually stale |

Anything that answers a question about *current* traders or tokens must run on the server:

```bash
ssh -i ~/.ssh/fomoradar root@<server> 'cd /opt/fomoradar/app && /opt/fomoradar/venv/bin/python -m fomo_agent.cli <command>'
```

The same data is already published, so prefer reading it over re-deriving it: the site at
https://fomoradar.app (`/`, `/fresh`, `/leaderboard`, `/search`, `/trader/<who>`, `/token/<mint>`), the API at
`/api/*` (`leaderboard`, `signals`, `fresh`, `tape`, `activity`, `stats`, `distribution`, `search`,
`token/{mint}`, `token/{mint}/chart`, `trader/{who}`, `health`), and the bot **@fomoradarRH_bot**
(`/status`, `/health`, `/signals`, `/fresh`, `/token`, `/trader`, `/subscribe`).

## Commands

Run from the repo root with the venv python (`.venv/Scripts/python` on Windows).

| Intent | Command |
|---|---|
| Overview: verdict counts, top active, 24h buys | `cli report --hours 24` |
| Whose money is in a token | `cli token <address> --hours 48` |
| One trader in full | `cli trader <handle-or-address> --hours 168` |
| What is quietly broken | `cli health` |
| Score / rescore wallets | `cli score` — see below |
| Pull fresh fills (free, no key) | `cli track` |
| Read what wallets actually hold | `cli holdings` |
| Fill the tape from before tracking | `cli backfill --days 30` |
| Name and price unknown tokens | `cli enrich-tokens` |
| Turn collected fomo users into wallets | `cli resolve` |
| Read fomo: board, verified wallets, notes | `cli fomo-api` |
| Tokens several trusted wallets entered at once | `cli hot` (`--backtest` to pick the bar) |
| Read the chain live and push bursts | `cli watch` |
| Refresh everything once | `cli run --once` |

Direct SQL is fine (tables: `traders`, `tokens`, `trades`, `holdings`, `fomo_users`, `fomo_swaps`,
`fomo_positions`, `score_history`, `bot_subscribers`, `bot_sent`, `runs`). Schema version lives in
`PRAGMA user_version`.

There is no `cli fresh` — the fresh-launch feed is a site route and a bot command, and its data comes
from `/api/fresh`.

## Scoring in chat

The pipeline's most-used job, because `ANTHROPIC_API_KEY` is deliberately not on the server. The
export carries the same context and the same instructions the API path would send.

```bash
cli score --export pending.json              # every wallet due for a verdict
cli score --export pending.json --unscored   # only wallets that have never been scored
cli score --export pending.json --force      # the whole roster, schedule ignored
cli score --import scored.json --model-label 'claude-opus-5 (in-chat)'
```

`--export` selects by the rescore schedule, not by "everything": `active` after 24h, `watch` after
72h, `dropped` after 14 days, anything untracked immediately. So an empty export means the roster is
current, not that something failed.

### The loop that works at scale

A context is about 2 KB, so a 300-wallet export runs to two thirds of a megabyte — too much to
read whole. Do this instead:

1. **Digest it.** Write a throwaway script that prints one line per wallet: address, handle, fomo
   PnL at 24h/7d/30d, trade count, volume, the 30-day on-chain aggregates (trades, unique tokens,
   bought, sold, median hold, early buys) and the open book as `SYM:pnl/cost×multiple`. One line per
   wallet is enough to judge; the full contexts stay in the file for the ones that need a closer look.
2. **Score in batches of ~60**, writing each to its own `batchN.json`.
3. **Validate before sending.** Merge the batches and check: every exported address covered exactly
   once, no extras, score inside its status band, `style` and `red_flags` from the allowed vocabulary,
   `confidence` in [0,1]. A silent mismatch here is worse than a wrong score — it looks like a
   successful import.
4. **Import**, then confirm the queue drained with another `--export`.

### Output format

A JSON array, or `{"results": [...]}`. One object per wallet — `docs/example_scores.json` is the
reference:

```json
{
  "address": "0x0a6ebed0155edb4b21d92ad02897a626cd90119e",
  "score": 96,
  "status": "active",
  "style": ["swing", "holder", "sniper"],
  "red_flags": [],
  "summary": "19.5M 30d PnL is the largest on the board and it is not one lucky ticket: PONS at 115x on a 68k basis, USELESS at 5x on 830k, MarsCoin at 3x on 965k. 3239 fills across 290 tokens with 88 early entries means the entries are systematic.",
  "confidence": 0.95
}
```

- `status` must agree with `score`: **≥70 active**, **40–69 watch**, **<40 dropped**.
- `style` ⊆ `sniper, swing, scalper, holder, copy-follower`.
- `red_flags` ⊆ `bot, bundler, insider-like, wash, one-hit`.
- `summary` is 2–3 sentences that cite the specific numbers behind the verdict. "Strong trader with
  good PnL" is useless; it appears verbatim on the public trader page and in `/api/leaderboard`.
- Unknown addresses and invalid objects are counted and skipped, never guessed at.

### How to weigh the evidence

**fomo's PnL is the primary signal, and it includes open positions.** A wallet showing millions on a
few thousand of on-chain outlay is not a glitch — the position ran and was never sold. Negative
on-chain cash flow is what accumulating looks like, not what losing looks like.

**The cost basis is what separates skill from a ticket.** A 780x on a 2k entry and a 2.1x on a 3.7M
entry can show the same PnL; only the second is evidence that someone can deploy size. Prefer several
independent winners over one, and a real basis over a large multiple on dust.

**Read the losses too.** The open book shows them, and they are the half that used to be invisible:
48 early entries mean nothing if the same book has one position written off entirely and another down
two thirds. Score the net, not the highlight.

Flags are for unambiguous shapes only — a 6-minute median hold across 282 tokens in dust size is a
`bot`; 46M of volume against a 54k book is `wash`; one unresolvable bag explaining the whole number
is `one-hit`. Few trades means low `confidence`, not a low score.

## Reading the numbers

- **Conviction** on a token is Σ(score/100)² over the wallets in it — *whose* money is there, not how
  many wallets. One trader at 85 outweighs a crowd at 40, because anyone can open a wallet.
- **Heat** (the `/fresh` feed) is conviction × earliness, where earliness decays by half every hour
  after the pool opens. On a token that launched this morning, *when* someone bought is most of what
  their buy means; conviction alone cannot tell those apart.
- **Position state** (`analyze.position_state`, the single definition all three surfaces read) is
  `open`, `trimmed`, `closed`, `held`, `pre-tape` or `unknown` — the tape's buys and sells settled
  against the balance actually on chain. The last three are admissions, not results: `held` means the
  wallet holds more than the tape ever saw it buy, `pre-tape` means it sold more than it bought, and
  both mean the entry price is unrecoverable. Show size and cost for those, never a PnL — "revenue
  minus what we watched go in" would be profit computed from half a record.
- **Mult** is the position's worth against its cost. A dash means fomo reports profit already
  withdrawn, so the entry price cannot be recovered.
- **Book value** is the only portfolio figure that does not need an entry price.
- **USDG and WETH are quote assets**, never positions. Some sources book a swap from the pool's side,
  filing "sold X for USDG" as a USDG purchase. Never present them as something the cohort bought.
- A fomo profile address is not a wallet. Never track one on-chain; `resolve` infers the real one.

## Examples

**"Разбери трейдера unipcs"** → `cli trader unipcs`

```
# unipcs  (active, score 96)
0x0a6ebed0155edb4b21d92ad02897a626cd90119e

fomo 30d $19.5M · open bags 217 worth $13.3M unrealised
fills 184 · volume $1.0M · win 67% of 6 round trips

## The book — 217 names open
  PONS               $7.8M open   cost $67.7k    held
  USELESS            $3.4M open   cost $829.8k   held
  MEME                   - open   cost $287.0k   held
  (71 more sold down from an entry older than our tape, so neither size nor profit can be stated)

## What came back out
realised $24.0k over 6 positions, 4 of 6 sold out entirely for a profit
```

Lead with the verdict and the two or three positions that justify it, then say plainly what could not
be priced. The parenthetical is not a footnote — it is the difference between a book and a guess.

**"Кто держит этот токен?"** → `cli token 0x80ba…9136`

```
# CRUMBS  0x80baa4b3bfac6f4978700df824b1b3d98e889136
liquidity $56.7k · mcap $388.6k

## Who holds it
4 holders, 3 of them scoring 60+ · avg score 64 · conviction 1.68

## Flow, last 48h
bought $275.2k · sold $185.2k · 144 fills by 26 wallets
```

Holders and buyers are two different populations and two different conviction numbers. A token
launched hours ago has buyers and almost no holders — quote the one that answers the question asked.

**"Что сломалось?"** → `cli health`

```
ok   router               3827 fills in the last day
ok   fomo collection      last collection 0.4h ago
ok   scoring queue        0 tracked wallets waiting for a verdict
ok   wallet resolution    264 fomo users still without an on-chain address
```

Every failure in this system looks identical from outside — the site renders, the numbers just stop
moving. A flat tape reads as a quiet market until someone checks the dates, so check `health` before
concluding the cohort went quiet.

## Limits

- Robinhood Chain (id 4663) by default. Solana and Base still work but need a Codex or Helius key,
  and several Codex queries are plan-gated (`filterWallets`, `detailedWalletStats`, `balances`).
- **fomo's own API is not server-reachable** — Cloudflare refuses every non-browser client. fomo
  data comes from fomoapi.io over HTTP (`cli fomo-api`, `FOMOAPI_KEY`), on a free key of 1,000
  credits a month that the schedule spends about 30 a day of. When a collection goes stale, the two
  explanations are a rejected key and an exhausted month, and `cli health` names both. The older
  route — a signed-in Chrome on the server posting through `extension/` — is still in the tree and
  switched off; it ended when fomo restricted the account it depended on.
- The RPC will answer about any block range but refuses expensive ones, and how expensive depends on
  how hot the blocks are. `backfill` treats the width as a negotiation: halve on "timed out", pause
  and retry on 429, newest window first so an interrupted run has already filled what matters most.
- Never invent fomo endpoints. `sources/fomo.py` is filled only from `docs/fomo-endpoints.md`.
