# AGENTS.md — standing rules for the Ralph loop

These rules are **invariant across every iteration**. They exist to keep the
build green, the data honest, and the bug count near zero. Read them every loop.
Breaking one is worse than making no progress.

## The prime directives

1. **Only real, on-chain-verifiable data.** Never invent, hardcode, mock, stub,
   or "temporarily" fake pool reserves, prices, block hashes, gas values, or
   addresses in any code path that can reach a shipped artifact. Test fixtures
   must be **recorded real** on-chain data at a **pinned block**, captured by a
   documented script — not hand-typed plausible numbers.

2. **Never fake `verified:true`.** The `verified` flag means "reproducible from
   the canonical chain at the stamped block hash." If you can't prove it, it's
   `false`. No test may set it true without the real reproduction.

3. **Never reward-hack the tests.** Do not delete, `#[ignore]`, `--skip`,
   loosen an assertion, or narrow a fixture to turn a suite green. If a test
   legitimately can't run (endpoint down, engine not installed), mark it
   **BLOCKED** in `PROGRESS.md` with the concrete reason and move on — do not
   pretend it passed. Making a test pass by weakening what it proves is the one
   unforgivable action.

4. **Leave the build green.** Never commit with the Tier-A suite red
   (`cargo build` + `clippy -D warnings` + `fmt --check` + `cargo test`). If you
   can't get green this iteration, commit nothing to the milestone, record the
   blocker in `PROGRESS.md`, and stop.

5. **One task per iteration.** Do the single most important unmet thing for the
   current milestone. Small diffs. Don't rush ahead; don't refactor unrelated
   code; don't start milestone N+1 while N has unmet exit criteria.

## How to work each iteration

6. **Orient before editing.** Read `PROGRESS.md`, the current milestone in
   `docs/BUILD_PLAN.md`, and the relevant parts of `docs/ARCHITECTURE.md` /
   `docs/ENGINE_CONTRACT.md`. Look at the actual code state — don't trust memory
   (there is none; each loop is a fresh context).

7. **Conform to the contract, don't change it.** `docs/reference/INTEGRATION.md`
   is the engine team's spec — immutable here. Map onto it per
   `docs/ENGINE_CONTRACT.md`. If reality seems to contradict the contract, record
   the discrepancy in `PROGRESS.md` and pick the contract; do not silently
   diverge.

8. **Test-first where it's cheap; test-always where it matters.** Every new
   behavior gets a test named in the milestone's exit criteria. The on-chain
   equality tests (event-derived state == `eth_call` at block N) are the backbone
   — prioritize them.

9. **Respect the dependency order.** `core → amm → rpc/chains → ingest/v4 →
   aggregator → engine-client → output → app`. Don't build a layer on an untested
   one.

10. **Keep it plug-and-play.** No hidden global state, no hardcoded endpoints or
    addresses in code (they live in `config/`), stable output envelope, `/health`
    + `/metrics` intact. Anything an integrator would need is config.

11. **Prefer boring, proven crates** (`alloy`, `tokio`, `serde`, `reqwest`,
    `proptest`, `criterion`). Don't add a dependency without a reason recorded in
    the commit.

## Definition of done (and how the loop ends)

12. A milestone is done only when **all its exit-criteria tests pass**. The whole
    component is done only when every milestone is done **and** the Tier-B
    live/nightly gates pass (benches within budget, soak clean, e2e green).

13. When — and only when — everything in `docs/BUILD_PLAN.md` is satisfied,
    append a line beginning `RALPH-COMPLETE` to `PROGRESS.md` with a one-line
    evidence summary (commit SHAs, bench p99s, soak duration). The loop runner
    watches for that sentinel and stops. Do not write it early. Do not write it on
    a hunch.

## Commit & progress discipline

14. **Commit each finished, green task** with a clear message referencing the
    milestone (e.g. `M4: V2 Sync-decode ingestor + pinned-block equality test`).
    Do not commit secrets, endpoint URLs with keys, or large fixtures without a
    capture script.

15. **Update `PROGRESS.md` every iteration** — tick what you finished, note what's
    next, log any BLOCKED item with its reason. `PROGRESS.md` is the loop's only
    memory; if it's not written down, it didn't happen.

16. **Never push to a branch other than the designated feature branch.** Never
    force-push over others' work.
