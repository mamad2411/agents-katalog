# CLAUDE.md — Operating Constitution for the l2arb build

> This file is loaded into **every** Claude Code iteration. It is the highest
> authority on *how* to work in this repo. `plan/backlog.md` says *what* to
> build next; this file says *how* to build anything at all. Read it fully at
> the start of every loop. Keep it current — if you learn a durable rule, add
> it here (concise) and note the change in `ralph/memory/decisions.md`.

---

## 1. Mission & Scope (do not drift)

Build a **Python, off-chain, near-zero-latency arbitrage _detection_ engine for
Layer 2 blockchains.** It watches live L2 state and emits arbitrage
opportunities. It is a **detector and analytics system, not a trader.**

**In scope**
- On a **single chain**: detect **2-hop (spatial)**, **triangular**, and
  **multi-hop** (bounded-length cyclic) arbitrage.
- **Cross-chain**: detect **simple 2-hop only** (same asset, two chains). No
  cross-chain triangular/multi-hop.
- Real-time streaming detection + a historical backtesting/analytics path.

**Explicitly OUT of scope (never build these, even if a task seems to ask)**
- ❌ Signing or submitting transactions; any private key; any "execute the trade"
  path. This system never holds keys and never sends value.
- ❌ MEV *extraction* tactics (sandwiching, front-running, generalized
  back-running bots). We *detect price discrepancies*; we do not attack anyone.
- ❌ Any data source that is not verifiable on-chain (see §3).

If a backlog task appears to cross these lines, **stop, do not implement it**,
write the concern to `ralph/memory/blocked.md`, and pick the next safe task.

---

## 2. The Ralph Loop — how each iteration works

You are started **fresh** each iteration with no memory except these files. The
filesystem is your memory. Follow this exact procedure every time:

1. **Orient (read, in order):**
   - This file (`CLAUDE.md`).
   - `ralph/memory/progress.md` — what is already done.
   - `ralph/memory/learnings.md` — accumulated gotchas; do not relearn them.
   - `ralph/memory/blocked.md` — known blockers; do not bang on them.
   - `plan/backlog.md` — the ordered task list.
2. **Confirm the tree is green** before changing anything:
   `make check`. If it is red, your #1 job this iteration is to make it green
   again — a red tree blocks all progress. Fix it, commit, stop.
3. **Select exactly ONE task**: the highest-priority unchecked `[ ]` item in
   `plan/backlog.md` whose dependencies are satisfied. Do not batch tasks.
4. **Do the task TDD-first** (see §4). Write the test(s), watch them fail,
   implement the minimum elegant code to pass, refactor.
5. **Run the gates**: `make check` must pass (and `make integration` /
   `make verify` when the task touches those tiers). 100% of tests green — no
   skips-to-pass, no `xfail` to dodge a real failure.
6. **Update the written record** (§6): tick the backlog item, append to
   `progress.md`, add any `learnings.md` entry, update docs and this file if a
   rule changed.
7. **Commit** one atomic change with a clear message (§7). Then **stop.** The
   loop will restart you for the next task.

**One task per iteration. Leave the tree green. Write down what you learned.**
That discipline is the whole point — it keeps context small and progress durable.

If you finish and the backlog has no remaining actionable `[ ]` items and all
milestone acceptance criteria in `plan/milestones.md` pass, create the sentinel
`ralph/DONE` with a one-line summary and stop.

---

## 3. Data integrity — the non-negotiable rule

**Only real, live, on-chain-verifiable data may flow through production paths.**

- Every price/reserve/liquidity number originates from **on-chain state read via
  RPC** (`eth_call`, `eth_getLogs`, `eth_subscribe`) or is **derived
  deterministically** from such state by AMM math with a unit test proving the
  derivation.
- **No synthetic, random, hard-coded, or "example" market data in any runtime
  path.** Mock/synthetic data is allowed **only** inside clearly-marked unit
  tests, and must never be importable by `src/l2arb` runtime modules.
- Every DEX pool the engine trusts must be **verified**: correct contract, at a
  known address, with reserves cross-checked against an **independent oracle**
  (Blockscout MCP `read_contract` at a pinned block, or a second RPC). Agreement
  between two independent sources is the bar for "verifiable." See
  `docs/DATA_INTEGRITY.md`.
- Data must be **fresh**: attach block number + timestamp to every quote; reject
  or flag stale state; invalidate on reorg.
- The `verify` test tier (`make verify`) exists to enforce this and must stay
  green. A detection the engine cannot tie back to a specific block is a bug.

---

## 4. Test-based development — the definition of "done"

No file is "done" until it is **tested and the whole suite is green.** Tests are
written *with or before* the code, never bolted on later.

**Every task must, as applicable, add/extend tests across the relevant tiers:**

| Tier | What it proves | Tooling |
|------|----------------|---------|
| syntax/style | it parses, formats, lints clean | `ruff format`, `ruff check` |
| types/logic | interfaces are sound | `mypy --strict` |
| unit | AMM math & graph search are correct | `pytest -m unit`, `hypothesis` |
| integration | boundaries work (RPC/redis/db) | `pytest -m integration` |
| chain | matches real forked/live chain state | `pytest -m chain` (Anvil fork) |
| db | schema + queries round-trip | `pytest -m db` |
| verify | data is on-chain-verifiable | `pytest -m verify` |
| benchmark | latency SLOs hold | `pytest -m benchmark` |

**Standing testing rules**
- **Test pairing**: every `src/l2arb/<module>.py` has a matching
  `tests/.../test_<module>.py`. Enforced by `scripts/check_test_pairing.py`.
- **Coverage ratchets, never drops.** The `COV_FAIL_UNDER` floor only goes up.
  Core math (`amm/`) and detection (`detect/`) target 100% line+branch.
- **Property-based tests** for all AMM math (invariants: constant-product holds,
  monotonicity, no-free-lunch without a real edge).
- **Determinism**: tests must not depend on wall-clock or live network unless
  marked `chain`/`integration`; pin blocks; freeze time where needed.
- Prefer **failing the test first** and confirming the failure message is the
  one you expect. A test that has never been red proves nothing.
- **After roughly every couple of new source files**, run the *integration*
  tier for the subsystem you touched, not just unit — wiring bugs hide between
  green units.

---

## 5. Engineering principles — elegant, robust, secure, maintainable, evolvable

- **Ports & adapters (hexagonal).** The core (AMM math, graph detection) knows
  nothing about web3, redis, or FastAPI. Chains and DEXes plug in behind typed
  `Protocol` interfaces so a new L2 or a new DEX family is an adapter, not a
  rewrite. See `docs/ARCHITECTURE.md`.
- **Typed everywhere.** `mypy --strict`. Public functions have full signatures
  and docstrings stating units (wei? bps? token decimals?) — unit confusion is
  the #1 source of on-chain math bugs.
- **Async, non-blocking hot path.** Never block the event loop; no sync I/O in
  streaming code (ruff `ASYNC` guards this). Hot loops are `numba`/`numpy`.
- **Fail loud on bad data, degrade gracefully on infra.** A malformed price is a
  bug (raise). A dropped RPC connection is expected (reconnect, failover).
- **Security by construction.** No secrets in code or logs; read-only endpoints;
  validate every external input (`pydantic`); `bandit` + `pip-audit` clean.
- **Small, composable modules.** If a file exceeds ~300 lines or a function
  exceeds ~40, ask whether it should be split. Elegance is a review criterion,
  not a nicety.
- **Evolvable.** Every architectural decision is recorded in
  `ralph/memory/decisions.md` (ADR-style) so the next iteration can reverse it
  deliberately, not accidentally.

---

## 6. Documentation discipline (do this every iteration)

- Update `ralph/memory/progress.md` with what you did (append-only log).
- Add any durable gotcha to `ralph/memory/learnings.md`.
- Record any architectural choice in `ralph/memory/decisions.md`.
- Keep `docs/` accurate: if behaviour changed, the doc changes in the **same
  commit.** Stale docs are treated as bugs.
- Keep this `CLAUDE.md` and `README.md` truthful. If setup steps changed, fix
  them now, not "later."
- Public APIs, modules, and non-obvious math carry docstrings with **units and a
  reference** (e.g. link to the Uniswap V3 whitepaper section).

---

## 7. Git & commit hygiene

- Work only on the branch `claude/l2-arbitrage-engine-j4olzf`.
- One task → one atomic commit. Message: imperative subject, then *why*.
  Reference the backlog id, e.g. `feat(amm): add V2 out-given-in [T-0301]`.
- Never commit a red tree. Never commit secrets, `.env`, or large binaries.
- Push with `git push -u origin claude/l2-arbitrage-engine-j4olzf`.

---

## 8. Enhancement audits (run on cadence, not just when convenient)

Every **5th iteration** (and whenever `progress.md` says one is due), spend that
iteration on an **audit task** instead of a feature — pick the next audit dimension
in rotation and file findings as new backlog items (do not fix opportunistically
and sprawl the diff):

1. **Correctness/data-integrity audit** — re-verify a sample of live pools
   against the independent oracle; hunt for any non-on-chain data leak.
2. **Latency audit** — profile the hot path (`py-spy`, benchmarks); confirm SLOs;
   find allocations/blocking calls on the event path.
3. **Security audit** — `pip-audit`, `bandit`, secret scan, input-validation
   review, dependency diff.
4. **Simplicity/maintainability audit** — dead code, over-long modules,
   duplicated logic, missing docstrings/units, coverage gaps.
5. **Evolvability audit** — are new chains/DEXes still add-an-adapter? Any leak
   of infra concerns into the core?

Record audit results in `ralph/memory/progress.md` and open backlog items for
anything found. An audit that finds nothing is logged as such.

---

## 9. When you are blocked

If a task cannot be completed safely (missing credential, ambiguous spec,
out-of-scope, needs a human decision):
- Append a precise entry to `ralph/memory/blocked.md` (what, why, what's needed).
- Do **not** fake it with mock data or a stub that pretends to pass.
- Pick the next actionable backlog task. If none exist, write `ralph/DONE` and stop.

---

## 10. Quick command reference

```
make setup         # install core deps + dev toolchain (uv sync)
make setup-all     # also install the analytics extra (Phase 9)
make check         # fast gate: lint + types + pairing + tests+coverage
make ci            # full gate incl. security audit
make integration   # RPC-fork / redis / db tier (needs services-up)
make verify        # on-chain data-integrity tier
make bench         # latency regression gates
make services-up   # local Postgres/Timescale + Redis
```
