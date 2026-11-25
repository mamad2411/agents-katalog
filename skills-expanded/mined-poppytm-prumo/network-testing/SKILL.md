# Network Resilience Testing

## Purpose
Prove networked systems survive packet loss, latency spikes, jitter, partitions, and reconnect storms using tc/netem and Toxiproxy fault injection, exponential-backoff retries with jitter, idempotent operations, and measured recovery-time objectives.

## Use when
- Testing multiplayer, API client, sync engine, or webhook delivery behavior under loss, delay, duplication, or corruption.
- Validating reconnect, resync, backoff, circuit-breaking, and offline-queue draining logic.
- Setting retry budgets, timeout hierarchies, and recovery-time objectives for networked features.
- Reproducing field incidents (hotel Wi-Fi disconnects, 4G handoffs, region partitions) in CI.

## Do not use when
- Implementing tick logic, prediction, or interpolation itself (use `realtime-synchronization`).
- Defining packet encodings or schema evolution (use `serialization`).
- Measuring page-load performance on healthy networks (use `performance-web`).

## Required context
- Fault profiles: loss percent, delay mean plus jitter, duplication, corruption, partition duration, disconnect frequency.
- Retry and timeout inventory per dependency: attempts, backoff base and cap, jitter strategy, idempotency coverage.
- Recovery objectives: detection time, reconnect time, catch-up time, acceptable data loss in operations.
- Test harness: Toxiproxy 2.9 or tc/netem scripts, seeded chaos scenarios, staging topology matching production hops.

## Procedure
1. **Model the hostile network explicitly**: define profiles such as clean LAN (0.1 ms, 0 percent loss), hotel Wi-Fi (60 ms plus 40 ms jitter, 2 percent loss, drops every 90 s), 4G handoff (300 ms spike 5 s, then partition 10 s), and region partition (full split 60 s with asymmetric return).
2. **Inject faults reproducibly**: implement each profile as a Toxiproxy toxic (latency, bandwidth, slow_close, timeout) or a tc netem qdisc command (loss 2 percent, delay 60 ms 40 ms distribution normal), seeded and committed so CI replays the exact storm.
3. **Enforce retry discipline**: retries use exponential backoff with full jitter (sleep = random(0, min(cap, base × 2^attempt)), base 200 ms, cap 10 s, max 5 attempts), GET/PUT/DELETE retry only on safe errors, POST retries only with Idempotency-Key, and every retry path logs attempt, backoff, and outcome.
4. **Test partitions and reconnect storms**: split brain for 60 s asserting both sides queue instead of corrupting, then heal and verify convergence within the 30 s RTO; drop 500 clients at once and confirm the reconnect storm stays under 2x provisioned accept rate with staged backoff.
5. **Measure recovery, not just survival**: record detection time (heartbeat miss after 3 × 2 s interval), reconnect p95, backlog drain rate (5,000 ops/min), duplicate rate after dedup (under 0.01 percent), and user-visible frozen time.
6. **Record evidence and run scripts/verify.sh** from the repo root with fault scripts, retry matrices, and recovery dashboards attached.

## Decision rules
- **Idempotency before retries**: no operation gains a retry until its replay is proven safe via keys or dedup IDs.
- **Backoff always has jitter**: synchronized retries without jitter are a self-inflicted DDoS and fail review.
- **Timeouts form a hierarchy**: client timeout exceeds server timeout exceeds downstream timeout, each with margin; inverted hierarchies are defects.
- **Queues are bounded and visible**: offline queues cap at 10,000 operations with drop-oldest-plus-warning policy and a drain gauge.
- **Recovery has a number**: every networked feature declares an RTO (reconnect plus catch-up) and proves it under the hotel Wi-Fi profile.

## Evidence required
- Fault-injection scripts (Toxiproxy/toxics JSON or tc netem commands) committed and seeded.
- Retry matrix per dependency: attempts, base, cap, jitter, idempotency coverage.
- Recovery measurements: detection, reconnect p95, drain rate, duplicate rate against RTO.
- Passing execution log from scripts/verify.sh.

## Output contract
- Chaos scenario suite runnable in CI with deterministic seeds and pass/fail thresholds.
- Retry, timeout, and queue configuration with documented budgets.
- Recovery report proving RTO compliance or honest gap analysis.

## Stop conditions
- All profiles pass with RTO met, duplicate rate under 0.01 percent, reconnect storm within accept budget.
- Fault exposes a design flaw (non-idempotent mutation, unbounded queue) requiring implementation rework.
- Token budget exhausted.
- Blocked on external dependency.

## Escalation rules
- Escalate to Lead Architect if recovery requires protocol redesign (idempotency keys, dedup stores, CRDTs) beyond test scope.
- Escalate to Infrastructure if staging cannot reproduce production hop count, TLS termination, or NAT behavior faithfully.
