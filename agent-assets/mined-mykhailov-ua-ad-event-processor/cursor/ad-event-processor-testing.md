---
description: Test taxonomy, holdout proofs, edge-case matrix, race/alloc/compiler gates
globs:
  - **/*_test.go
  - **/*_fault_test.go
  - **/*_bench_test.go
  - scripts/ci/*test*
  - scripts/fault/**
alwaysApply: false
---

# Testing Policy

## Purpose

Apply when adding or changing tests, fuzz targets, fault proofs, or CI test gates.

Cross-refs: `boundaries.mdc` (**Test dishonesty catalog**), `anti-slop.mdc`, `fault-tests.mdc`, `hot-path.mdc`, `parser.mdc`, `cold-path.mdc`, `development.mdc`.

## Test taxonomy

| Suffix / prefix | Role |
| :--- | :--- |
| `*_test.go` | Unit and behavioral tests beside code |
| `*_fault_test.go` | Failure modes, invariant proofs, duplicate delivery |
| `*_integration_test.go` | Real PG/Redis/CH via testcontainers (`integration:` skip reason) |
| `*_bench_test.go` | Microbench; hot path must be 0 allocs/op when cited |
| `TestChaos_*` | Parser/wire security and sustained load (`internal/ingestion/`) |
| `Fuzz*` | `go test -fuzz`; must not panic on arbitrary input |
| `TestProof_*` / `*_holdout*` | Negative assertion: fails if wrong branch ships |

Placement: beside code under test. Shared corpora: `fault_*` packages, `model/testdata/`, `scripts/fault/`.

## Holdout tests (required for non-obvious behavior)

A holdout test proves the **intended branch**, not just "no error":

| Rule | Example |
| :--- | :--- |
| Naming | `*_holdout`, `*_holdoutPositive`, or `TestFoo_withoutBar` when Bar is the fix |
| Positive + negative | Assert positive case **and** at least one negative that would pass if logic inverted |
| Farm heuristic | `TestResidentialIntelResult_holdoutWithoutFarmHeuristic` - `Proxy: true` alone must **not** trip farm heuristic; `ResidentialProxy: true` must |
| Policy parity | `model/testdata/policy_parity.json` plus hand-picked threshold row (`TestResidentialProxySignal_holdoutPositive`) |

Banned: scaffold that only logs "integration scaffold must exercise Postgres" with no assertion (`integration_test_slop_gate.sh`).

## Agent-resistant proofs (vs meta-slop)

Full matrix and lie modes: `anti-slop.mdc` (**Agent-resistant verification**).

| External pattern | Repo substitute (honest) |
| :--- | :--- |
| Black-box holdouts | In-repo `*_holdout*` + `merge-integration` / `test-fault` tiers agents often skip |
| Mutation testing | **Not in CI**; holdout negative must fail when fix reverted |
| Compiler `-m` gate | `escape_heap_gate.sh` + `hot_path_static_gate.sh` on hot files |
| eBPF / perf per test | Load-test BPF tier only (`malformed.sh`, `bpf/resource.sh`) |
| Property / quick | `Fuzz*`, `TestChaos_*`, `AssertBudgetInvariant`, wire corpora |

PR touching parsers: extend fuzz corpus or chaos row. PR touching spend/sink: holdout + invariant helper.

## Financial and ordering invariants

Any spend/debit/outbox/recon path change must prove:

| Invariant | Helper / proof |
| :--- | :--- |
| `current_spend <= budget_limit` (PG, +/-1 micro-unit) | `domain.AssertBudgetInvariant` / `ingestion.AssertBudgetInvariant` |
| No accept without debit alignment | Fault test + 503 fail-closed, not silent accept |
| Stream admission before debit | `TestStreamProducerAdmissionRaceWithoutReserve` pattern |
| Post-debit enqueue fail -> rollback | `TestUnifiedFilter_RollbackDebit_LocalQuanta`; metric `ad_stream_producer_post_debit_rejected_total` ~0 |
| Outbox duplicate -> no double-apply | Idempotency key, version check, `ON CONFLICT` |
| Slot migration fence | Budget unchanged under concurrent workers (`migration_fence_test`) |

Run invariant assertions **after** fault injection (kill worker, corrupt feed, queue overflow), not only on happy path.

## Concurrency, races, and RCU

| Scenario | What to prove | Pattern in tree |
| :--- | :--- | :--- |
| RCU snapshot swap | No torn reads during `Publish`; readers see gen A or B only | `TestCIDR_RCUSwap_ConcurrentReaders` |
| Concurrent map/store apply | No panic; final state consistent | `TestStore_concurrentApplyDiff` |
| Stream admission race | Without reserve: queue full after debit; with reserve: 503 before debit | stream producer fault tests |
| Shard 0 optional | `nil` shard 0 in `[]redis.UniversalClient` - no panic | `state_shard_nil_spof_test.go` |
| Settings/registry watchers | `pickHealthyShard` / `StartWatchShards` skip nil entries | `TestProof_Shard0Nil_*` |

CI: `bash scripts/ci/race_short.sh` (`go test -race -short` on `./internal/... ./pkg/...`).

Race-sensitive microbenches: tag `//go:build !race` when bench hammers atomics (`local_quanta_*_bench_test.go`).

Do not use `t.Parallel()` on tests that mutate shared global metrics, env, or package-level `atomic.Value` snapshots without isolation.

## Compiler, build tags, and alloc gates

| Gate | When | Command |
| :--- | :--- | :--- |
| Heap escape baseline | Touch hot handler/filter/rtb files | `bash scripts/ci/static/escape_heap.sh` |
| Zero-alloc microbench | Hot parse/filter/auction change | `make test-alloc-gate` |
| Race detector | Shared mutable state or new goroutine in request path | `bash scripts/ci/race_short.sh` |

`-gcflags=-m` escape lines must not grow above baseline - new `escapes to heap` in hot files fails CI even when tests pass.

`unsafe.String` / frame lifetime: cross-hop tests catch edge vs gnet drift.

## Payload, JSON, and extreme characters

Track JSON corpus (`fraudTrackJSONCases2026`, `requests_parse_fault_test.go`) - extend when adding parse rules:

| ID / theme | Edge | Expected |
| :--- | :--- | :--- |
| G-J01 | Truncated object | Reject |
| G-J03 | Oversized UUID string (128+ chars) | Reject |
| G-J04 | Duplicate key `user_id` | Last wins |
| G-J06 | Unicode-escaped **key** `\u005f` | Reject (ASCII keys only) |
| G-J07 | Numeric `campaign_id` | Reject (strict string UUID) |
| G-J09 | Unicode escapes **inside** UUID value | Reject |
| G-J10 | `null` campaign_id | Reject |
| G-J12 | UTF-8 BOM prefix | Reject |
| G-J13 | Embedded NUL `0x00` in string | Reject |

Parser security gaps (`TestChaos_ParserSecurity_PS_*`):

| Gap | Attack | Budget constant |
| :--- | :--- | :--- |
| json_pool_cap_poisoning | `sync.Pool` cap poisoning | `maxPoolObjectSize` |
| json_key_pair_flood | Key-pair flood | `MaxJSONKeyPairs` |
| json_key_escape_walk | Backslash escape walk in key | `MaxJSONStringScanBytes` |
| json_overlong_utf8 | Overlong UTF-8 (`\xc0\xaf`) | `JSON_STRICT_UTF8` |
| json_non_ascii_key | Non-ASCII key bytes | Reject |
| json_lone_surrogate | Lone surrogate `\uD800` | Reject |
| json_whitespace_bomb | Distributed whitespace bomb | `MaxJSONTotalWSkip` |
| json_quote_escape_bomb | Quote-dense escape bomb | `MaxJSONStringEscapes` |
| openrtb_duplicate_keys | Duplicate OpenRTB keys | Last wins on `id`, `imp` |

Wire / framing: TE.TE obfuscation, HPACK continuation bomb, protobuf field budget (`PROTO_MAX_FIELDS`), HTTP/2 oversized frame, chunk extension `;`, slow-body spin (`HTTP1_INCOMPLETE_MAX`). See `parser.mdc`.

## Feed refresh fail-open vs fail-closed

| State | Corrupt/missing feed behavior | Test |
| :--- | :--- | :--- |
| First boot, no feeds | Fail-open (no match on empty table) | `TestCIDR_FeedRefreshFailClosed_FirstBootFailOpen` |
| After good snapshot | Corrupt refresh retains previous snapshot | `TestCIDR_FeedRefreshFailClosed_RetainsSnapshot` |
| Feed line formats | `#` comments, inline comments, junk lines, IPv6 | `TestCIDR_FeedLoader_LineFormats` |

Same pattern for TLS fingerprint feeds, residential intel, DC ASN tables: corrupt refresh must not wipe last good snapshot.

## XDP edge_filter token bucket (math holdouts)

Full XDP/BPF policy: `xdp-bpf.mdc`. BPF `token_bucket_consume_existing` in `deploy/edge/xdp/bpf/edge_filter.c` is verified by Go simulation in `internal/edge/token_bucket_sim_test.go` (no CAP_BPF required). Do not claim bucket correctness from `prog.Test` alone.

| Test | Proves |
| :--- | :--- |
| `TestTokenBucket_subintervalCredit_holdout` | Fixed refill admits strictly more than legacy (`last_ns = now` on every pass) under sub-interval flood |
| `TestTokenBucket_refillInterval_matchesRate` | After `tokens=0`, next pass near `NS_PER_SEC/rate` |
| `TestTokenBucket_sustainedAboveRate_converges` | Offered load above rate: fixed admission bounded; legacy never exceeds fixed |
| `TestTokenBucket_lastNSInvariant` | `last_ns` monotonic and `last_ns <= now` |
| `TestTokenBucket_averageOfferedBelowRate_neverStarves` | Offered below rate: zero drops |

Source shape holdout: `TestEdgeFilterRateLimitPerCPUHash_holdout` (reads `edge_filter.c` for PERCPU_HASH, `token_bucket_consume_existing`, `TCPOPT_NOP`, `ICMP_FRAG_NEEDED`, `syn_cookie_tail_call`).

```bash
go test ./internal/edge/ -short -run TestTokenBucket_ -count=1
go test ./internal/edge/ -short -run TestEdgeFilterRateLimitPerCPUHash_holdout -count=1
```

BPF prog integration (CAP_BPF): `TestXDP_dropNonTCPOnTrackerPort`, `TestFault_XDPSynCookieWithTCPOptions`.

## Cross-hop and parity

Edge nginx Lua and tracker gnet must agree on the same wire:

- `TestChaos_CrossHop_NginxGnet` - `differential_count=0`.
- `http1IngressCanonical` corpus for regression diffs.
- Shard CRC32C: Go asm, Go fallback, and `edge-slot-map.lua` - parity tests in `sharding_test.go`.
- Policy parity files (`model/testdata/*.json`) for ML/heuristic alignment.

## Fuzz targets

Existing: `FuzzJA3Parse`, `FuzzLinkSignerVerify`, `FuzzSafePageVerifyParse` (`landing_protection_fuzz_test.go`).

Rules:

- Fuzz func must not panic; return early on invalid input.
- Prefer testing parse + match + evaluate on fuzz input, not only parse.
- Nightly parser fuzz: `.github/workflows/parser-fuzz-nightly.yaml`.
- License/JWT: `license-fuzz-nightly-gate`, `scripts/test/telegram/fuzz_smoke.sh`.

## Fault proof logging

Use `pkg/faultproof.Log` or `t.Logf("fault_proof fault=%s ...")` so `scripts/fault/resilience_fault_gates.sh` and operators can grep proof lines.

Parser holdouts: `faultproof.Log` with `case_id`, `proof=closed`. `proof=open` requires follow-up test or PR waiver (`anti-slop.mdc`).

## Integration tests (`*_integration_test.go`)

Mandatory (`integration_test_slop_gate.sh`):

1. `testing.Short()` skip with reason containing `integration:`.
2. Real infra helper (`testutil.SetupPostgres`, `SetupRedis`, etc.).
3. Behavioral `require.*` / `assert.*` - not scaffold-only.
4. No `testify/mock`, `gomock`, or bare `t.Skip()`.

Never `httptest.NewServer` in a package that also uses testcontainers for the same dependency class (`anti_slop_gate.sh`).

## Banned / low-value tests (delete, do not add)

- Stdlib-only roundtrips with no app logic.
- Nil receiver smoke with no contract.
- Field echo without behavior.
- Duplicate route-meta smoke.
- Chaos tests with `chaos_pct=0` that always pass.
- Weakening assertions to green CI without fixing behavior.
- Mock Redis bench named `BenchmarkUnifiedFilter_Check` (must be `_mock`).

## Verification matrix (by touch surface)

| Touched surface | Minimum commands |
| :--- | :--- |
| Hot parse/filter/handler | `make test-alloc-gate`; `bash scripts/ci/static/escape_heap.sh` |
| Parser/security wire | `go test ./internal/ingestion/ -run=TestChaos_ParserSecurity -count=1`; `TestChaos_CrossHop_NginxGnet` |
| Spend/debit/quanta/stream | `AssertBudgetInvariant` in executed test; stream admission fault tests |
| Outbox/payment/webhook | `*_fault_test.go` idempotency; `cold_path_json_gate.sh` if handlers |
| New `*_integration_test.go` | `bash scripts/ci/static/integration_test_slop.sh` |
| Shared mutable / goroutines | `bash scripts/ci/race_short.sh` |
| Default PR scope | `bash scripts/ci/pr_fast.sh` |

## Related rules

`anti-slop.mdc`, `cold-path.mdc`, `code-style.mdc`, `fault-tests.mdc`, `hot-path.mdc`.
