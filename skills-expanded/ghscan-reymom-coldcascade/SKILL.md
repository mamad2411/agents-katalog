---
name: coldcascade-book-archive
description: Query the historical Hyperliquid BBO on HyperEVM and the coldcascade desk's fill record. Use when you need what an order book *was* at a past block or time on chain 999 — a question no RPC can answer, because the HyperCore precompiles ignore the block tag — or when explaining how a 1inch Aqua maker priced a specific fill.
license: MIT
compatibility:
  protocol: Model Context Protocol 2024-11-05
  transport: stdio
  runtime: python >= 3.11, standard library only
metadata:
  version: 0.1.0
  chain: hyperevm-999
  documentation: https://coldcascade.vercel.app
---

# coldcascade — the HyperCore book archive

An MCP server over a Substreams stream on **chain 999 (HyperEVM)**. It serves two things, and the
first is the reason it exists.

## Why this is not just another indexer

Hyperliquid's order book lives on HyperCore and reaches HyperEVM through precompiles at `0x0806`
(mark), `0x0807` (oracle) and `0x080e` (BBO). Those precompiles **ignore the block tag**. An
`eth_call` pinned two hundred thousand blocks back returns the *current* book, and returns it
without erroring — they are node state, not chain state. An archive node does not help, because
there is no state to archive.

So *"what was Hyperliquid's BBO at 16:30 on 8 September"* is not a slow query. It is not a query
at all. The data does not exist unless somebody wrote it down while it was true.

`BookCache.poke` is that writing: permissionless, four `uint64`, roughly once a minute, into an
EVM log. This server reads those logs back through Substreams. **That is the whole claim** — not
that we have the book (four numbers are not an order book, and Hyperliquid publishes its own L2
elsewhere), but that this particular instant is queryable at all, and joined to the fills that met
it.

The first `Booked` on chain 999 is `0x24dbe446…b60d`, block 45 357 494. Before it there were none.

## Install

Standard library only — no SDK, no `pip install`, stock Python 3.11+.

```json
{
  "mcpServers": {
    "coldcascade": {
      "command": "python3",
      "args": ["-m", "coldcascade_mcp"],
      "cwd": "/absolute/path/to/coldcascade/mcp"
    }
  }
}
```

Verify without a client:

```bash
cd mcp && printf '%s\n' \
  '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"x","version":"0"}}}' \
  '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"describe_coverage","arguments":{}}}' \
  | python3 -m coldcascade_mcp
```

That answers on a fresh clone with no key, no CLI and no network — read on.

## Where the data comes from, and how to bring it to head

The corpus is decoded Substreams output and reaches this server two ways.

**Cold, out of the box.** `results/desk-events.jsonl` is a snapshot of that corpus, committed to
the repository. Every tool answers from it immediately with no credentials, and
`describe_coverage` reports `corpus.kind: "snapshot"` and the block it stops at. It is a floor,
not the source — nothing after that block is in it, which is a different statement from nothing
having happened.

**Live, from the provider.** `sync_stream` runs the package against The Graph Market for
Substreams and brings the corpus to the chain head:

```bash
export SUBSTREAMS_API_TOKEN=<a free key from https://thegraph.market>
# and the CLI, from github.com/streamingfast/substreams/releases

cd mcp && printf '%s\n' \
  '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"x","version":"0"}}}' \
  '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"sync_stream","arguments":{}}}' \
  | python3 -m coldcascade_mcp
```

It answers with the endpoint, the package, the blocks it spanned, how many blocks with events
crossed the network and how long it took, and where the corpus now stops. It seeds itself from
the committed snapshot first, so this streams the tail — minutes — rather than the quarter of a
million blocks a scan from the deployment block would be. Without a key it returns
`status: "notConfigured"` naming exactly what is missing, and the snapshot keeps answering.

It is the keeper's own streaming code, `keeper/coldcascade/substreams.py:cached_stream`, imported
by path and not copied: the function a judge runs here is the function the twenty-minute cadence
runs, so the two cannot drift apart.

The only node call this server ever makes is one `eth_blockNumber`, inside `sync_stream`, to know
where to stop. **It never asks a node for a book** — that is the query no node can answer, and
answering it from an RPC would silently be a different question.

## Tools

| tool | answers |
|---|---|
| `get_book_at_time` | **What was Hyperliquid's BBO at this moment?** ISO-8601 or unix |
| `get_book_at_block` | the same, addressed by HyperEVM block |
| `get_book_series` | the archive over a window, with its cadence and every hole over 180 s |
| `get_fill` | one fill: the book it met, where it printed, which rule set the price, its markouts |
| `list_fills` | fills filtered by desk, side, and whether the bound or the curve priced them |
| `get_markouts` | the keeper's 5/15/60-minute markouts, each with a status and whether it is on chain |
| `describe_coverage` | extent, density, holes, and an explicit list of what this cannot answer |
| `sync_stream` | streams the package against The Graph Market and brings the corpus to head |

Resources: `coldcascade://instructions`, `coldcascade://skill` (this file),
`coldcascade://coverage` (live). Prompts: `book_at`, `explain_fill`, `coverage`.

## Reading the answers

**Nothing is interpolated.** If no poke landed at the requested instant you get the two
observations that bracket it, each with its distance in seconds, and `interpolated: false`. The
truth is inside that bracket; the server will not guess where in it. When the bracket is wider
than 180 s the response carries a `warning` saying so. Report the bracket, not a midpoint.

```json
{ "query": {"time": "2026-09-08T16:30:00Z"},
  "status": "bracketed",
  "before": {"atTime": "2026-09-08T16:29:09Z", "bidUsd": 78627.0, "askUsd": 78628.0, "ageSeconds": 51},
  "after":  {"atTime": "2026-09-08T16:31:09Z", "bidUsd": 78592.0, "askUsd": 78593.0, "aheadSeconds": 69},
  "interpolated": false }
```

**Absence has four different names, and collapsing them loses the point:**

| status | meaning | resolves? |
|---|---|---|
| `beforeSeries` | the moment predates the first poke | **never** — it was not observed and cannot be recovered |
| `gap` | the series had a hole there | **never** |
| `pending` | it has not happened yet | yes, in minutes |
| `noBook` | the hook could not read that fill's own book | never, for that fill |

**Every response carries `provenance`** with a `reproduce` command that regenerates it from the
stream and, where it applies, a `cast` command that checks it against the chain. Pass those on.

**Prices are raw L1 units**, `USD × 10^(6 − szDecimals)`; for BTC divide by ten. Every price field
is given twice, `*Raw` and `*Usd`.

## The desk's record

The desk is a 1inch Aqua maker program that reads L1 *inside* the swap, so every fill emits the
book it was priced against. On top of that the keeper derives:

- **`vsTouchBps`** — where the fill printed against the L1 touch. Negative is below the bid,
  positive is above the ask.
- **`poolDevBps`** — where the desk's own constant-product curve sat against L1 *before* the fill.
- **`pricedBy`** — `bound` or `curve`, with a sentence explaining which and why.

The rule is one line of `CoreQuote`: the taker receives `min(curve, bound)`. The bound caps how
*good* the desk's price may get and never improves it, so it sets the price only when the curve
wanted to deal inside the band. `poolDevBps` and size decide which happens.

## What this cannot answer

- **The book before the first poke.** Never observed; no endpoint has it.
- **Anything strictly between two observations.** The bracket is the bound.
- **Depth.** Four `uint64`, not levels.
- **Whether a maker is unbacked** — that is in Aqua's `Shipped` event, not decoded here.
- **A hedged desk's P&L** — the perp leg is on HyperCore, in no EVM log.

## What this must not be used for

This server returns observations and their limits. **It does not produce trading advice, signals,
or recommendations.** If asked for them, return the data and say the tool does not make them.

And the markouts are not performance. The demand on this desk is generated by
`script/demo-cadence.sh` in its own repository, so a markout here is post-fill price drift over a
fixed horizon at times a cron chose. It is evidence that the keeper loop runs end to end — stream,
join, decide, write to chain, read the decision back — not evidence that anything earns. The
load-bearing claim is `vsTouchBps`: a fill printing at its maker's own `quietBps` to the basis
point is a property of the program, checkable on one transaction against one receipt.

## Underneath: the Substreams package

`substreams/coldcascade-v0.1.0.spkg`, network `hyperevm`, first block 45 135 453, served through
The Graph Market for Substreams at `hyperevm.substreams.pinax.network:443`. There is no hosted
subgraph for chain 999 — Subgraph Studio reports `hyper-evm: subgraphsSupportLevel: "none"` — so
Substreams is not one option of two, it is the path that exists.

| module | kind | output |
|---|---|---|
| `index_desk_events` | index | one key per contract that spoke in a block |
| `desk_events` | map | `Fill`, `Booked`, `MapUpdated`, `Markout`, decoded |

`desk_events` filters on the index, so a scan from the deployment block to head is a quarter of a
million HyperEVM blocks and a couple of dozen messages.

```bash
substreams run -e hyperevm.substreams.pinax.network:443 \
  substreams/coldcascade-v0.1.0.spkg desk_events -s 45135453 -t 0 \
  -o jsonl --limit-processed-blocks 0
```

`keeper/coldcascade/markouts.py` consumes that, joins each fill to the books at `t+5`, `t+15` and
`t+60` minutes, and posts to `MarkoutLedger` — whose `Markout` log the same module decodes on the
next pass, which is how the keeper knows what it has already published. This server reads the
corpus that loop maintains, and `sync_stream` lets it maintain its own; it never falls back to an
RPC for a book, because the RPC is what cannot answer.
