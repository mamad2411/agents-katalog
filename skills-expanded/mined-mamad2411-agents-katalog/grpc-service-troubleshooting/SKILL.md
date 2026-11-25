---
name: grpc-service-troubleshooting
description: >
  Diagnoses gRPC-specific failure modes — DEADLINE_EXCEEDED, connection
  and keepalive/GOAWAY issues, HTTP/2 multiplexing problems behind
  L4/L7 load balancers, and protobuf/proto-compatibility breakage
  across client/server versions — distinct from generic HTTP ingress
  troubleshooting. Use when a user asks to "why is my gRPC call
  hanging or returning DEADLINE_EXCEEDED," "gRPC keepalive pings
  disconnecting my clients," "gRPC load balancing isn't spreading
  traffic across pods," "a proto field changed and now some clients
  fail," or "gRPC streaming call drops after N minutes."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: service-mesh-and-api-gateway
  maturity: stable
---

# gRPC Service Troubleshooting

## Purpose

gRPC's failure modes look superficially like ordinary HTTP problems but
have gRPC-specific causes that generic HTTP ingress troubleshooting
doesn't surface: a `DEADLINE_EXCEEDED` that's actually a client-set
deadline too short for a legitimately slow call, not a timeout at the
proxy layer; a long-lived streaming call that dies precisely every N
minutes because of a keepalive/`GOAWAY` mismatch between client and
server, not a network blip; and a single long-lived HTTP/2 connection
that concentrates all of a client's traffic onto one backend pod
because a plain L4 load balancer has no visibility into the
multiplexed streams inside it. This skill covers diagnosing these
gRPC-specific issues directly — distinct from
[ingress-nginx-configuration](../../../kubernetes-platform/skills/ingress-nginx-configuration/SKILL.md)-style
HTTP/1.1 ingress troubleshooting, and complementary to the
mesh-level traffic policies covered in
[service-mesh-istio](../../../kubernetes-platform/skills/service-mesh-istio/SKILL.md)
and
[linkerd-service-mesh-configuration](../linkerd-service-mesh-configuration/SKILL.md),
both of which have first-class gRPC support worth reaching for instead
of hand-rolling client-side retry/load-balancing logic.

## When to use

- A gRPC call returns `DEADLINE_EXCEEDED` and it's unclear whether the
  cause is a genuinely slow backend, a too-short client deadline, or a
  proxy-layer timeout unrelated to the application's own logic.
- A long-lived gRPC stream (server-streaming or bidi) disconnects
  reliably after a fixed interval, suggesting a keepalive or connection
  lifetime setting rather than an application bug.
- Traffic to a gRPC service isn't load-balancing evenly across backend
  pods/instances even though the client is configured to call a
  Service with multiple healthy endpoints.
- A client fails to deserialize responses (or the server fails to
  deserialize requests) after one side updates its `.proto` file or
  generated stub, despite "just adding a field."
- A gRPC call works from one environment (local, one cluster) but fails
  or times out from another, hinting at an intermediary (load balancer,
  proxy, firewall) that isn't fully HTTP/2-aware.
- Deciding whether a gRPC traffic-management need (retries, load
  balancing, timeouts) should be solved at the client library level or
  pushed into a service mesh sidecar/proxy instead.

## Prerequisites & environment

- `grpcurl` for ad hoc call testing against a service that supports
  reflection (or with a `.proto`/descriptor file supplied explicitly if
  reflection is disabled) — the fastest way to isolate whether a
  problem is client-side, network-side, or server-side.
- Access to both client and server logs with gRPC status codes and,
  ideally, deadline/latency detail — the bare error `DEADLINE_EXCEEDED`
  on the client side alone is not enough to diagnose root cause.
- Knowledge of what sits between client and server: a plain L4 load
  balancer (TCP-level, no HTTP/2 stream awareness), an L7/gRPC-aware
  load balancer or Ingress, or a service mesh sidecar — this
  fundamentally changes where a connection-level problem is likely to
  live.
- The client and server's gRPC library versions and configured
  keepalive parameters (`grpc.keepalive_time_ms`,
  `grpc.keepalive_timeout_ms`, `grpc.max_connection_age_ms`, or
  language-equivalent options) — these differ in default values across
  gRPC language implementations, so "default keepalive behavior" isn't
  a single universal number to assume.
- Both sides' `.proto` definitions (or at least their field numbers and
  types) when investigating a serialization/compatibility issue — proto
  wire-format compatibility rules operate on field numbers and wire
  types, not field names, so the actual `.proto` diff matters more than
  a description of "what changed."

## Step-by-step guidance

1. **Separate a deadline problem from a connectivity problem first.**
   `DEADLINE_EXCEEDED` on the client means the client's own deadline
   expired before a response arrived — it does not by itself tell you
   whether the server was slow, unreachable, or the deadline was simply
   too short:
   ```bash
   grpcurl -max-time 30 -d '{"id": "123"}' payments-api.internal:443 \
     payments.v1.PaymentsService/GetPayment
   ```
   If a generous `-max-time` succeeds where the application's normal
   (shorter) deadline fails, the real issue is a deadline set too
   aggressively for the call's actual latency distribution — not a
   backend outage. Check the server's own processing time (application
   logs, tracing) to confirm what a realistic deadline should be.

2. **Check for deadline propagation issues in a multi-hop call chain.**
   A common cause of `DEADLINE_EXCEEDED` in a service-to-service chain
   is the *caller's* deadline propagating unchanged into a downstream
   call that itself has other work to do first — the downstream service
   inherits an already-shrinking budget it didn't set:
   ```
   Client sets deadline: now + 2s
     → Service A (does 1.5s of its own work)
       → Service B receives ~0.5s of remaining deadline, not a fresh 2s
   ```
   Confirm whether the deadline seen at the failing hop is the
   originally-set value or a much smaller propagated remainder — if the
   latter, the fix is usually giving upstream callers a more realistic
   end-to-end deadline budget, not increasing any single service's
   internal timeout.

3. **For a stream that dies at a fixed interval, check keepalive and
   max-connection-age settings on both sides**, since a mismatch here
   produces a very regular, almost clock-like disconnect pattern:
   ```
   # Server-side (example, gRPC-Go)
   grpc.KeepaliveParams(keepalive.ServerParameters{
     MaxConnectionAge:      30 * time.Minute,
     MaxConnectionAgeGrace: 5 * time.Second,
   })
   # Client-side
   grpc.WithKeepaliveParams(keepalive.ClientParameters{
     Time:    20 * time.Second,
     Timeout: 5 * time.Second,
   })
   ```
   If the server enforces `MaxConnectionAge` (common for forcing
   periodic reconnects to rebalance load) but the client doesn't
   transparently reconnect and resume its stream, the client sees a
   hard disconnect at exactly that interval. Confirm the client library
   is configured to retry/reconnect on `GOAWAY`, not just log an error.

4. **If keepalive pings themselves are the cause of disconnects**
   (server closing connections it considers abusive), check for a
   mismatch between the client's ping interval and the server's
   enforcement policy:
   ```
   # Server-side minimum ping enforcement (gRPC-Go)
   grpc.KeepaliveEnforcementPolicy(keepalive.EnforcementPolicy{
     MinTime:             15 * time.Second,
     PermitWithoutStream: false,
   })
   ```
   A client pinging more frequently than the server's `MinTime`
   tolerates gets disconnected with a `too_many_pings` `GOAWAY` —
   visible in server-side logs, not obviously in client-side error
   messages, which is why this is easy to misdiagnose as "random"
   network instability instead of a policy mismatch.

5. **Diagnose uneven load distribution as an HTTP/2 connection-reuse
   problem, not a load-balancer misconfiguration first.** gRPC
   multiplexes many RPCs over one long-lived HTTP/2 connection; an L4
   load balancer only balances at connection-establishment time, so a
   client that opens one connection and reuses it for its lifetime
   sends every RPC to whichever single backend that connection landed
   on:
   ```bash
   kubectl top pods -n payments -l app=payments-api
   # one pod consistently far hotter than its siblings under equal client load
   ```
   Fix by moving to client-side (per-RPC) load balancing — a gRPC
   client configured with a resolver that returns multiple backend
   addresses and a `round_robin` (or similar) load-balancing policy —
   or by fronting the service with an L7/gRPC-aware proxy (a service
   mesh sidecar, or an Ingress/load balancer with explicit gRPC/HTTP2
   support) that can distribute individual streams, not just TCP
   connections.

6. **Confirm intermediaries are actually gRPC/HTTP2-aware** when a call
   fails only through a specific network path (works pod-to-pod inside
   the cluster, fails through an external load balancer or Ingress):
   ```bash
   grpcurl -plaintext payments-api.payments.svc.cluster.local:8080 \
     payments.v1.PaymentsService/GetPayment
   grpcurl payments-api.example.com:443 \
     payments.v1.PaymentsService/GetPayment
   ```
   A plain TCP/L4 load balancer, an old HTTP/1.1-only proxy, or an
   Ingress controller without gRPC support configured (some require an
   explicit annotation/backend-protocol setting to speak HTTP/2 to the
   upstream) will break gRPC even though a basic TCP health check
   against the same port succeeds.

7. **Diagnose proto compatibility failures from the actual wire-format
   rule, not from field names.** Protobuf compatibility is governed by
   field **numbers** and wire types, not names — a client and server
   using different `.proto` versions can still interoperate correctly
   if changes were additive (new optional/repeated field with a new
   number) but will break if a field number was reused for a different
   type or a required semantic changed:
   ```protobuf
   // Breaking: reusing field number 3 for an incompatible type
   message Payment {
     string id = 1;
     int64 amount_cents = 2;
     // was: string currency = 3;
     bool  is_refund = 3;   // BREAKING — field 3's wire type changed
   }
   ```
   Diff both sides' actual `.proto` files (or decode a captured
   payload with `protoc --decode_raw`) rather than relying on a
   changelog description — "just added a field" is only safe if the
   number truly is new and unused by any still-deployed client/server
   version.

8. **Use `grpcurl` with reflection to isolate client vs. server vs.
   network** whenever the failure mode is ambiguous:
   ```bash
   grpcurl -plaintext payments-api.internal:8080 list
   grpcurl -plaintext payments-api.internal:8080 describe payments.v1.PaymentsService
   grpcurl -plaintext -d '{"id":"123"}' payments-api.internal:8080 \
     payments.v1.PaymentsService/GetPayment
   ```
   A `grpcurl` call that succeeds directly against the server but fails
   through the application client points at a client-side
   configuration issue (deadline, keepalive, load balancing); a
   `grpcurl` call that fails the same way the application does points
   at the server or an intermediary.

## Best practices

- Set gRPC deadlines based on the real end-to-end latency budget of a
  call chain, and propagate a *shrinking* deadline deliberately rather
  than treating deadline propagation as automatic and correct by
  default — a deep call chain needs either a generous top-level
  deadline or per-hop deadlines that account for downstream work.
- Configure both client and server keepalive parameters together and
  verify they're compatible (client ping interval ≥ server's minimum
  enforced interval; client configured to reconnect on `GOAWAY`) rather
  than tuning one side in isolation.
- For any gRPC service with more than one backend instance, use
  client-side (per-RPC) load balancing or route through an L7/gRPC-aware
  proxy — never assume an L4 load balancer distributes gRPC traffic
  evenly, since it only balances at connection time, not per RPC.
- Treat proto compatibility as governed by field numbers/wire types,
  not field names or "looks like an additive change" — reusing a field
  number, changing a field's type, or changing `repeated`/`optional`
  semantics in an incompatible way breaks wire compatibility regardless
  of how the change reads in a diff.
- Prefer a service mesh's built-in gRPC-aware retry/load-balancing/
  timeout policy (Istio's `VirtualService` timeout/retry, Linkerd's
  `ServiceProfile`) over hand-rolled client-side retry logic where a
  mesh is already in place — see
  [service-mesh-istio](../../../kubernetes-platform/skills/service-mesh-istio/SKILL.md)
  and
  [linkerd-service-mesh-configuration](../linkerd-service-mesh-configuration/SKILL.md)
  for the mesh-level configuration.
- When fronting gRPC through a gateway (Kong, an Ingress controller),
  confirm gRPC/HTTP2 upstream support is explicitly enabled — it is
  often not the default backend protocol, and a gateway speaking
  HTTP/1.1 to the upstream breaks gRPC silently or with a confusing
  error unrelated to the real cause.

## Common pitfalls

- **Symptom:** A gRPC call fails with `DEADLINE_EXCEEDED` intermittently,
  and the backend's own processing-time logs show it completed well
  within the caller's configured deadline.
  **Fix:** The deadline seen at the server is very likely a shrunk
  remainder propagated from an upstream caller that already consumed
  part of the original budget, not the deadline the failing service's
  own code set. Trace the deadline value across the actual call chain
  (not just the failing hop) before concluding the failing service
  itself needs a longer timeout.

- **Symptom:** A long-lived streaming RPC disconnects reliably every
  ~30 minutes, and reconnecting immediately succeeds and runs fine for
  another ~30 minutes.
  **Fix:** This regular interval is the signature of a server-enforced
  `MaxConnectionAge` (or an intermediary's idle/max connection
  lifetime) rather than a network fault. Confirm the client is actually
  configured to transparently reconnect and resume on `GOAWAY` — many
  gRPC client libraries require this to be explicitly enabled, and
  without it, a routine server-side connection-age enforcement looks
  like a recurring outage.

- **Symptom:** One backend pod runs consistently hotter (CPU, request
  count) than its siblings despite them all being healthy and
  registered behind the same Service/load balancer.
  **Fix:** A plain L4/TCP load balancer only chooses a backend once per
  connection, and a gRPC client typically holds one long-lived HTTP/2
  connection open for a long time, sending every RPC on it to the same
  backend. Move to client-side load balancing with a multi-address
  resolver and `round_robin` policy, or front the service with an
  L7/gRPC-aware proxy that balances per-stream rather than per-connection.

- **Symptom:** After a server deploys a new `.proto` version with what
  looked like a purely additive change, a subset of older clients start
  failing to deserialize responses or silently receive wrong field
  values.
  **Fix:** A field number was very likely reused for an incompatible
  type, or a previously-`optional` field's absence/presence semantics
  changed in a way that's additive in the `.proto` source but not in
  the wire format. Diff the actual field numbers and wire types (not
  just the source diff) between the old and new `.proto`, and use
  `protoc --decode_raw` against a captured payload to see exactly what
  bytes an old client is misinterpreting.

- **Symptom:** To "fix" a `DEADLINE_EXCEEDED` error during an incident,
  someone doubles or removes the client's deadline entirely, the errors
  stop, and the change stays in place afterward.
  **Fix:** Removing or drastically extending a deadline masks whatever
  made the call slow in the first place (a genuinely degraded backend,
  a propagation bug, a missing index) and lets a slow call chain tie up
  client resources far longer than intended, risking cascading
  resource exhaustion under real load. Treat a deadline change made
  purely to silence an error as a temporary diagnostic step — confirm
  the actual latency cause first (server-side tracing, deadline
  propagation trace from step 2), then set a deadline based on the real
  latency budget, not on "whatever makes the error go away."

## Worked example

**Scenario:** `checkout-service` calls `payments-api` via gRPC and
intermittently sees `DEADLINE_EXCEEDED`; separately, `payments-api`'s
pods show uneven CPU load despite three healthy replicas behind the
same Kubernetes Service.

```bash
# 1. Isolate whether it's a real backend slowness or a deadline issue
grpcurl -max-time 30 -d '{"id":"123"}' payments-api.payments.svc.cluster.local:8080 \
  payments.v1.PaymentsService/GetPayment
# succeeds in ~1.2s — the backend itself isn't the bottleneck

# 2. Trace the deadline actually seen at payments-api
# (application-level logging of the incoming context deadline)
# reveals payments-api receives ~200ms remaining, not checkout-service's
# configured 2s — an upstream hop (order-service) is consuming 1.8s
# of the budget before calling payments-api at all

# 3. Confirm the uneven-load symptom is HTTP/2 connection reuse
kubectl top pods -n payments -l app=payments-api
# payments-api-7f9...-abcde consistently 3x the CPU of its siblings
```

Root causes and fixes:
1. `order-service`'s call to `checkout-service` propagates a 2s deadline
   unchanged, but `order-service` itself does ~1.8s of work before
   calling `payments-api`, leaving it almost no budget. Fix: give
   `order-service` its own realistic deadline budget for its
   `payments-api` call (e.g. a fresh 1.5s deadline set explicitly at
   that call site) rather than blindly propagating the inherited
   deadline downstream.
2. `checkout-service`'s gRPC client was configured with a single static
   target address and no load-balancing policy, so its one long-lived
   HTTP/2 connection to `payments-api` pinned all traffic to whichever
   pod it first connected to. Fix: configure the client with a
   Kubernetes-DNS-based resolver returning all backend pod IPs and
   `grpc.WithDefaultServiceConfig` set to `round_robin`, so each new RPC
   (not just each new connection) can land on a different backend.

Re-running the `grpcurl` deadline test and `kubectl top pods` after both
fixes confirms `payments-api` now sees a healthy ~1.5s deadline budget
and CPU load spread evenly across all three replicas.

## Cross-references

- [service-mesh-istio](../../../kubernetes-platform/skills/service-mesh-istio/SKILL.md) — mesh-level gRPC-aware timeout, retry, and load-balancing configuration (`VirtualService` timeout/retries, `DestinationRule` load-balancing policy) as an alternative to hand-rolled client-side logic.
- [linkerd-service-mesh-configuration](../linkerd-service-mesh-configuration/SKILL.md) — Linkerd's `ServiceProfile`-based per-route timeout/retry configuration, which is gRPC-aware and solves the same class of problem at the mesh layer.
- [kong-api-gateway-configuration](../kong-api-gateway-configuration/SKILL.md) — configuring a gateway's upstream to actually speak gRPC/HTTP2 rather than falling back to HTTP/1.1, relevant to the intermediary-awareness check in step 6.
