---
name: cross-repo-trace
description: >-
  Trace how a field / contract / value / request flows across the trdlabs ecosystem
  end-to-end — producer (platform) → SDK (@trdlabs/sdk) → consumers (lab, office,
  backtester). Use to understand a seam — "how does X connect?", "where does this
  value come from / go?", "trace this contract across repos". Works from any repo folder.
---

# Cross-Repo Trace

Answer **"how does `X` connect producer → SDK → consumers, end-to-end?"** — the
question you ask to *understand a boundary* before working on it. Descriptive of
the *path*, where `cross-repo-consumers` is descriptive of the *set*.

## When to use

- To understand how a platform field reaches a consumer (via which SDK subpath).
- To follow a request / value across repo boundaries.
- To map a contract's producer, wrapper, and consumers before changing it.

## The canonical ecosystem seam

```text
platform  ──(HTTP ops-read / API contract)──►  sdk (@trdlabs/sdk facade)  ──►  consumers
  produces the data + the contract              wraps the surface               lab (npm), backtester (npm kernel)
                                                                                 office (hand-mirrored DTOs, NOT npm)
```

- Producer contract: `platform` ops-read spec (see
  `docs/architecture/contracts/platform-office.md` / `platform-sdk.md`).
- SDK facade: `sdk/src/{ops-read,intake,historical,research-contract,validation}`,
  exported as `@trdlabs/sdk/<subpath>`.
- Consumers: `lab` / `backtester` import the npm subpaths; **`office` hand-mirrors
  the DTOs** in `office/apps/server/src/connector/*/` (a contract edge, not code import).

## How

1. Anchor the ends: `search_symbols` for the producer symbol and the consumer symbol.
2. Call path: `get_call_chain` / `get_callers` between them.
3. Value flow (a field / DTO through helpers, args, returns): `flow_between(source, sink)`.
4. Contract-level view: `contracts` to see the producer↔consumer contract match.
5. Pub/sub or channel hops if any: `taint_paths` with source/sink patterns.

## Output

- The end-to-end path as `producer → SDK subpath → each consumer`, with the concrete
  files at each hop.
- Explicitly mark the **transport** at the consumer end: npm import (`lab`,
  `backtester`) vs hand-mirrored DTO (`office`).
- Note where the trace **stops** (e.g. office's mirror is a copy boundary — the value
  does not flow past it via code, it is re-declared).
