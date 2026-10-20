# CLAUDE.md

Engineering guide for the **L2 Data Ingestion Layer** — the read-path data-feed
component of a Cross-Chain Flash-Loan Arbitrage app, built and hardened by a
**Ralph loop**. This file orients any agent (or human) working in the repo. It is
checked-in project guidance: **treat the invariants below as binding.**

---

## 1. Start here (read in this order)

1. **`ralph/AGENTS.md`** — the standing, invariant rules. Read them **every**
   time. Breaking one is worse than making no progress.
2. **`ralph/PROMPT.md`** — the per-iteration build prompt.
3. **`docs/ARCHITECTURE.md`** — the design (one-process decision, data flow,
   crate layout, latency budget, reorg/verify, testing strategy).
4. **`docs/ENGINE_CONTRACT.md`** — how on-chain state maps onto the engine's JSON
   (V2/V3/V4, gas model, `native_price_in`, the `verified` honesty flag).
5. **`docs/reference/INTEGRATION.md`** — the engine team's contract, **verbatim
   and immutable**. Conform to it; never edit it.
6. **`ralph/PROGRESS.md`** — the loop's only memory: checklist, next task,
   BLOCKED items, per-iteration log. Update it every iteration.
7. **`docs/BUILD_PLAN.md`** — phased milestones M0–M10 with test-based exit
   criteria.

New to the repo? `README.md` → `docs/ARCHITECTURE.md`.

---

## 2. The prime directives (invariant — never violate)

These come from `ralph/AGENTS.md` and **override any impulse to move faster**:

1. **Only real, on-chain-verifiable data.** Never invent, hardcode, mock, or
   "temporarily" fake reserves, prices, block hashes, gas, or addresses in any
   path that can reach a shipped artifact. Test fixtures are **recorded real**
   on-chain data at a **pinned block**, captured by a documented script.
2. **Never fake `verified:true`.** It means "reproducible from the canonical
   chain at the stamped `block_hash`, and the latest reconcile matched." If you
   can't prove it, it's `false`.
3. **Never reward-hack the tests.** Do not delete, `#[ignore]`, `--skip`, loosen
   an assertion, or narrow a fixture to go green. A test that legitimately can't
   run is marked **BLOCKED** in `PROGRESS.md` with a concrete reason — never
   faked green.
4. **Leave the build green.** Every commit must pass the Tier-A gate:
   `cargo fmt --check` + `cargo clippy --all-targets --all-features -D warnings` +
   `cargo test --workspace`.
5. **One task per iteration.** Smallest safe step. Don't refactor unrelated code;
   don't start milestone N+1 while N has unmet exit criteria.
6. **Conform to the contract, don't change it.** `docs/reference/INTEGRATION.md`
   is immutable here. If reality seems to contradict it, record the discrepancy in
   `PROGRESS.md` and pick the contract.
7. **Respect the dependency order** (below). Don't build a layer on an untested one.
8. **Stay plug-and-play.** No hardcoded endpoints/addresses in code — they live in
   `config/`. Keep the output envelope stable and `/health` + `/metrics` intact.

---

## 3. What this component is (and is not)

A **single Rust process** that runs one supervised async **ingestor task per
chain** across five L2s, feeding one shared **aggregator** that assembles a
synchronized cross-chain snapshot and POSTs it to the `l2arb` Python detection
engine, then fans ranked opportunities out to a configurable output sink.

- **Chains:** Arbitrum One `42161`, Base `8453`, Optimism `10`, Unichain `130`,
  Ink `57073`.
- **It is a pure read path.** It **holds no keys, signs nothing, submits no
  transactions.** Signing, slippage protection, flash-loan callbacks, and MEV
  execution belong to the **separate** execution component — they are explicit
  **non-goals** here (`docs/ARCHITECTURE.md §11`). Do not add them.
- **The two headline decisions:** (1) one process, many chains — coherent
  simultaneous cross-chain view, isolated per-chain failure domains, one artifact;
  (2) Rust + `alloy` + `tokio` — no GC tail-latency, and the key trick: **read new
  pool state out of the event the node already pushed** (`Sync`/`Swap` logs carry
  post-trade reserves / `sqrtPrice`), so the hot path has **no extra RPC
  round-trip**.

---

## 4. Workspace & crate map

15 crates. Dependencies flow **downward**; this is also the milestone/build order,
so each layer leaves a green, self-contained base:

```
core → amm → rpc/chains → registry → ingest/v4 → gas → aggregator
     → engine-client → output → observability → config → app
```

| Crate | Package | Responsibility |
|-------|---------|----------------|
| `crates/core` | `l2i-core` | Domain types + the engine JSON contract (`DetectRequest`/`Response`, `Pool`, `Token`, `Blockstamp`); `DecU256`/`DecI256` decimal-string serde; golden tests. |
| `crates/amm` | `l2i-amm` | Pure math (no I/O): V2 constant-product, V3/V4 TickMath (faithful `v3-core` port), `sqrtPriceX96→price`, `native_price_in`. |
| `crates/rpc` | `l2i-rpc` | `alloy` providers (WS subscribe / HTTP archive), Multicall3 `aggregate3`, batched `code_at_batch`, `PrefetchProvider` (batch-once-then-replay), rate-limit **failover** across comma-separated endpoints, reconnect+backoff, single-flight coalesce, `ChainProvider` trait, `MockProvider` (feature `testing`, Multicall3-aware + round-trip counter). |
| `crates/chains` | `l2i-chains` | Per-chain `ChainSpec`, gas model, canonical predeploy addresses (Multicall3, OP `GasPriceOracle`/`L1Block`, Arb `ArbGasInfo`). |
| `crates/registry` | `l2i-registry` | The **on-chain validation gate** (§7 of ARCHITECTURE) + pool-registry TOML loader + `sol!` ABI bindings + V4 `compute_pool_id`. |
| `crates/ingest` | `l2i-ingest` | Per-chain event decode (`Sync`/`Swap`/`Mint`/`Burn`), in-memory `Mirror` (DashMap), reorg tracker, reconcile, warm-start persist. |
| `crates/v4` | `l2i-v4` | Uniswap V4 adapter: `PoolManager` logs by `poolId`, `StateView` seed/reconcile, hook-safety gate, dynamic-fee read → emit as `v3` shape. |
| `crates/gas` | `l2i-gas` | Live gas + L1-data-fee reads (OP `getL1Fee`, Arbitrum `ArbGasInfo`), `assemble_chain_context`. **Lives above `rpc`** (it does RPC reads) to avoid a `chains↔rpc` cycle. |
| `crates/aggregator` | `l2i-aggregator` | Atomic per-chain snapshots (`re_stamp`), sync policy, `build_detect_request`, incremental tracker, cadence (debounce+heartbeat), `filter_cross_chain`. |
| `crates/engine-client` | `l2i-engine-client` | `EngineClient` trait; keep-alive HTTP impl + subprocess impl; `validate_response` (contract §10). |
| `crates/output` | `l2i-output` | Versioned `Envelope { schema_version, kind, chain_blocks, payload }`; `OutputSink` trait; stdout + WS-server sinks (redis/grpc are config surface, loudly `Unavailable`). |
| `crates/observability` | `l2i-observability` | Prometheus `/metrics`, `/health`, latency timers, tracing setup. |
| `crates/config` | `l2i-config` | Typed `Config` mirroring `config.example.toml`; `parse`/`load`/`validate`/`enabled_chains`. |
| `crates/app` | `l2-ingest` (bin) | The binary: load→validate→supervise→wire. `pipeline` (supervisor + aggregator loop), `ingestor` (live actor), `context` (cached per-chain gas/price on a `watch`), `crosschain`. |
| `crates/benches` | `l2i-benches` | Criterion hot-path benches (decode/apply/snapshot). |

---

## 5. The hot path (latency-critical — keep RPC off it)

```
node WS push (newHeads, logs)
  → decode event  (< 100 µs, alloy typed decode, no alloc)
  → update Mirror (< 50 µs, sharded DashMap)
  → aggregator: atomic per-chain snapshot + build DetectRequest (< 1 ms, incremental=deltas)
  → EngineClient keep-alive POST /detect
  → validate response → publish Envelope to sink
Intra-process budget (decode→emit): < 5 ms p99, CI-benched.
```

**Rules for anything on this path:**
- **No RPC round-trip per block.** `eth_call`/multicall is for **seeding** and
  **background reconciliation only**, run on off-loop workers (see
  `app/context.rs`, `ingest/reconcile.rs`). Never add a blocking RPC to the log/head
  handling loop.
- **No blocking calls in async tasks** (`std::thread::sleep`, blocking fs/IO). Use
  `tokio` equivalents. Blocking stalls log-draining and blows the latency budget.
- **Panic-safety is a system property.** The release profile is
  `panic = "abort"` (`Cargo.toml`), so a panic in **any** task aborts the **whole
  process** (all 5 chains) — the supervisor cannot catch it. Therefore the live
  path must **not panic**: prefer `Result` propagation over `.unwrap()`/`.expect()`/
  slice-indexing/unchecked-arithmetic on any input derived from chain data. Decoders
  already return `Result` and length-check — keep it that way.

---

## 6. Build, test, run

```bash
# Tier-A gate (must be green on every commit):
cargo fmt --all --check
cargo clippy --all-targets --all-features -- -D warnings
cargo test --workspace

# Build the binary + validate a config (no network needed):
cargo build --release
./target/release/l2-ingest --check-config --config config/config.example.toml

# Run against real endpoints (fill config.toml first; start l2arb once):
cp config/config.example.toml config.toml    # then fill RPC endpoints + pools
uvicorn l2arb.api.http:app --port 8080        # the engine, long-running
./target/release/l2-ingest --config config.toml

# Tier-B (live, not per-commit): benches + soak
cargo bench -p l2i-benches
L2I_LIVE=1 ./scripts/soak.sh
```

Toolchain is **pinned to Rust 1.94.1** (`rust-toolchain.toml`). `unsafe_code` is
`forbid` workspace-wide — this is a pure read path; no `unsafe` is warranted.

---

## 7. Engine-contract cheat-sheet (`docs/ENGINE_CONTRACT.md` is normative)

- **Only two pool kinds** the engine can price: `v2` (constant product) and `v3`
  (concentrated liquidity). **V4 pools map onto the `v3` shape**, identified by
  `poolId`. Anything the engine can't price (Curve/Balancer/Solidly-stable,
  fee-on-transfer/rebasing tokens, unsafe-hook V4) **must be excluded** and logged
  loudly at startup — feeding it in produces phantom opportunities, the worst
  failure mode.
- **Big integers are decimal strings, always** (`reserve*`, `sqrt_price_x96`,
  `liquidity`) — never JSON numbers (precision loss). Use `DecU256`/`DecI256`.
- **`fee_pips` is fee in millionths** (0.30% → 3000, 0.05% → 500).
- **`token0.address < token1.address`** byte-wise; `reserve0` pairs with `token0`.
  Do not re-sort.
- **`blockstamp` = `{ chain_id, number, block_hash, timestamp }`** — the
  `block_hash` is what makes state verifiable and reorg-aware.
- **"In sync"** = intra-chain single-block (never mix block N and N−1 for one
  chain in a request) + freshest-verified-per-chain.
- **`native_price_in[T]`** is a float ratio derived from the ingested WETH/T pool
  (numeraire-base-units per 1 wei of native). `f64` here is **contract-conformant**
  — the only place floats are acceptable. A numeraire with no derivable path is
  omitted.
- **Cadence:** build+send on meaningful change with a `min_interval_ms` debounce
  floor and a `max_interval_ms` heartbeat ceiling. **First request of a session is
  `incremental: false`; then `true`.** After a reconnect/reseed, the incremental
  tracker/policy must reset so the next request is full again.
- **Response handling (§10):** confirm every leg was `verified:true`, `net_profit >
  0`, and blockstamps round-trip. A bad/non-200/schema-invalid response is a failed
  tick — log, count the error metric, keep the last good snapshot; **never crash the
  ingestor.**

---

## 8. Invariants to preserve when editing

Breaking any of these is a correctness/safety regression:

- **`verified` honesty** — a pool that is reorg-in-flight, reconnecting/reseeding,
  reconcile-mismatched, or has an unpinnable dynamic fee/hook **must** emit
  `verified:false`. Never emit stale or unproven state as `verified:true`.
- **The validation gate is the security boundary** (`registry/gate.rs`). Every
  configured pool must pass code-exists → token0/1 → fee → deny-list →
  decimals/symbol → factory (V4: hook-safety → poolId) or it does not enter the
  live set. A logged-but-not-enforced check is a bypass.
- **No RPC on the hot path;** off-loop workers only (see §5).
- **Atomic per-chain snapshots;** never mix two blocks of one chain in a request.
- **The output envelope is stable** and versioned (`schema_version`). Downstream
  consumers depend on it.
- **Decimal-string big-ints** everywhere in the contract; the golden serde tests
  guard this.

---

## 9. Testing strategy & fixtures

Two tiers (`docs/ARCHITECTURE.md §9`). **Only Tier A gates the loop** (deterministic).

- **Tier A (every commit, 100% green):** unit + property (`proptest`) + the
  backbone **on-chain equality tests** — *event-derived mirror state == independent
  `eth_call` at a pinned block, exactly* — plus reorg/reconcile/contract-serde
  tests. Fixtures are **recorded real** on-chain data at pinned blocks
  (`crates/*/tests/fixtures/*.json`), captured on-chain — never hand-typed.
- **Tier B (nightly / pre-release, not per-commit):** criterion latency benches
  vs the §8 budget, a live soak (continuous reconcile stays 100%, no memory growth,
  reconnect exercised), and an e2e plug-and-play run against live endpoints + a real
  `l2arb`.

When adding a behavior, add the test named in the milestone's exit criteria. For
anything touching chain data, the proof is the pinned-block equality test.

---

## 10. Current status

**M0–M10 complete + a post-M10 production-audit hardening pass.** Tier-A is green
on HEAD (build + `clippy -D warnings` + `fmt --check` + 145+ tests; benches far
under the §8 budget; live HTTP smoke green on all 5 chains). See `ralph/PROGRESS.md`
for the authoritative checklist and per-iteration log.

**NOT `RALPH-COMPLETE`** — the sentinel additionally requires the two Tier-B gates,
both **BLOCKED** in *some* dev sandboxes and recorded honestly (never faked green):
1. the real `l2arb` engine (not on PyPI here) → blocks the M8 real-engine contract
   test + M10 e2e;
2. a WebSocket L2 endpoint → blocks the M1 `newHeads`/`logs`-over-WS smoke + the
   sustained soak. **Refined 2026-08-10** (`claude/ingestion-engine-endpoints-rx9h18`,
   `docs/notes-ingestion-engine-endpoints.md`): the blocker is not necessarily "no WS
   endpoint exists" — a real, working `wss://` credential from a normal provider
   (Alchemy/QuikNode/dRPC/...) is exactly as configurable as the HTTP side via
   `l2arb setup --all-chains` (§5 below) or a hand-filled `config.toml`. What's
   specifically blocked in a sandboxed agent session with a TLS-terminating egress
   proxy is the **WS upgrade handshake itself** — confirmed live: three unrelated
   providers all failed identically with a TLS `UnknownIssuer` error, while the same
   session's plain HTTPS to the same three providers worked and seeded real pool
   state successfully. The sandbox's own proxy documentation lists WebSocket
   upgrades as explicitly unsupported ("report, do not work around"). On a normal
   deployment with direct internet access this is not a factor at all.

To close them in an environment where WS genuinely works end-to-end, provide the
engine (`[engine].http_url`/`subprocess_cmd`) and a real chain's `ws_url`, run the
e2e + `scripts/soak.sh`, and only then append the `RALPH-COMPLETE` line with an
evidence summary.

---

## 11. Non-obvious decisions & gotchas

- **`gas` is above `rpc`, not in `chains`.** The build plan sketches gas adapters
  in `chains`, but `chains` is depended-on by `rpc`; adapters that do RPC reads must
  live above `rpc`. Predeploy **address constants** stay in `chains`.
- **V4 emits `kind:"v3"`.** V4's concentrated-liquidity math is identical to V3;
  only the *identity* (`poolId`) and *read path* (`StateView`/`PoolManager`) differ.
- **`f64` appears only in `native_price_in` derivation** — that ratio is a JSON
  float in the contract. All swap-relevant amounts stay `U256` decimal strings.
- **`panic = "abort"` + supervisor** — see §5. Panic-safety on the live path is
  mandatory, not stylistic.
- **redis/grpc sinks are config surface, not built** — they return a loud
  `Unavailable`. ws + stdout are the shipped sinks.
- **Off-loop reads are batched, not per-item.** Seeding, the validation gate
  (via `rpc::PrefetchProvider` — batch every read once, then replay the existing
  per-pool `validate_pool` offline), and reconcile (grouped by block) all go
  through Multicall3 `aggregate3` + a batched `eth_getCode`. When adding a new
  off-loop read path, batch it too — don't reintroduce one request per pool.
- **Endpoint failover ≠ retry-everything.** `rpc::failover` hands off to the next
  comma-separated endpoint only on rate-limit/transport errors; a revert/decode
  error must **propagate** (every endpoint returns it identically). Don't widen
  `is_failover_error` to swallow real results.
- **Do not edit `docs/reference/INTEGRATION.md`.**
