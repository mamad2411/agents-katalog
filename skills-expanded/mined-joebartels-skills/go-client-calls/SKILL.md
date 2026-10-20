---
name: go-client-calls
description: Use when Go work creates or changes outbound HTTP or unary gRPC calls, client configuration, idempotency or replay policy, retries, circuit breakers, or remote-failure interpretation. Skip pure calculations, server-only handlers, and mechanical edits without a client-policy decision.
---

# Go client calls

Fit the call policy to the remote operation and its callers. Inspect the API,
supplied client, effective configuration, existing middleware and supported
Go/library versions before adding mechanisms. A reusable client and one bounded
request can be sufficient. Keep supported APIs and caller-visible results with
API contracts, construction/lifecycle with composition, scope mechanics with
context, and synchronization with concurrency guidance.

Read [HTTP clients](references/http-clients.md) for HTTP work or
[unary gRPC clients](references/grpc-clients.md) for gRPC work. Streaming
recovery, hedging and workflow orchestration require their own contracts.

## Establish the operation before the attempts

Identify one logical operation, its side effects, the promised result and what
a failed acknowledgement leaves known or uncertain. Determine which layer can
repeat it: caller workflow, application loop, interceptor, native client or
transport. Inspect existing retries before choosing an owner. Define whether
a limit counts application invocations, configured attempts or actual wire/server
executions; transparent retries and redirects can make those counts differ.

Establish repeat safety independently of transient-failure classification:

| Operation contract | Replay decision |
| --- | --- |
| Repetition has the same permitted effect | Repeat only eligible failures within the budget. |
| Server deduplicates one operation identity and payload | Keep that identity and semantically identical payload across attempts and outer caller retries. |
| Mutation may have completed and no replay guarantee exists | Preserve uncertainty; reconcile or expose the failed acknowledgement according to the caller contract. |

A new key per invocation can duplicate an operation when its caller retries.
A header alone establishes no server guarantee. Inspect deduplication scope,
retention and conflicting-payload behavior. Recreate replayable request data
from the operation's stable inputs; do not replay a consumed or truncated body.
Timeout/cancellation does not prove the server performed no effect.

## Choose bounded failure behavior

Use the operation and protocol contract to distinguish permanent rejection,
credentials/configuration failures, caller stopping and plausible dependency
transients. A status code or a generic client error alone does not establish
safe repetition. Some failures require restarting the enclosing transaction,
refreshing authorized credentials or reconciliation rather than replaying this
call. Preserve promised status/error classifications, independent causes and
accepted effects; add no universal public error hierarchy.

Use an existing suitable native policy before adding another retry layer.
Layered retry limits multiply work. Bound permitted attempts and cancellable
waiting under one total operation budget; attempt scopes only narrow what
remains. Apply backoff and jitter when synchronized callers would amplify load.
Honor valid server retry guidance within the remaining budget; unrepresentable
positive delays must not become zero or an early retry. Retain the appropriate
rejection/uncertain outcome when the budget prevents another attempt.

Reuse supplied clients, transports and connections. Preserve instance-specific
endpoints, credentials and host policy without process-global mutation. Use
secure transport in production and workload-appropriate response/message and
connection limits. Bound diagnostic presentation where promised while retaining
inspectable causes; a bounded response reader does not bound every error message.
Client ownership and release stay with their existing owner.

## Add a breaker only for a demonstrated need

If persistent failures require isolation, define dependency scope, health-eligible
outcomes, counting unit, trip/recovery policy and caller-visible rejection. Use
the project's existing mechanism when suitable. Timeouts, bounded retries or
admission control may already contain the problem.

Keep the caller result and dependency-health signal separate. Evaluate health
eligibility for every completion, including a successful result accompanied by
caller stopping. If the contract excludes that completion, retain the caller's
result policy while recording a neutral health event. Treating excluded errors
as successes resets failure history and can falsely close a half-open breaker;
a binary success/failure classifier cannot express neutrality. Excluded recovery
completions release admission without proving recovery. Specify what establishes
health, bound recovery admissions, and prevent old in-flight completions from
changing a newer generation. Do not introduce per-request breaker state or
share failures across unrelated dependencies.

Verify applicable behavior through the configured client boundary: actual
requests/RPC executions and effects, identity/payload/metadata stability, native
policy/commitment, permanent rejection, budgets, body ownership, health exclusion
and recovery. Include successful work during stopping when those policies
interact. Preserve minimal disabled/simple paths. Report actual checks and
unverified boundaries; passing a generic retry helper does not establish the
effective client policy.
