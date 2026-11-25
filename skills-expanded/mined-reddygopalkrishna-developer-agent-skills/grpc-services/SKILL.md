---
name: grpc-services
description: Builds and reviews gRPC services and .proto contracts - versioned packages, field numbering and reserved fields, buf lint and buf breaking in CI, status codes and rich error details, deadlines and propagation, retries via service config, streaming choices, load balancing over HTTP/2, health checks, reflection, interceptors, TLS/mTLS, and browser access via gRPC-Web, Connect or JSON transcoding. Use when writing or changing .proto files, implementing gRPC servers or clients, calls hang or all traffic hits one pod, or exposing gRPC to browsers. Not for choosing between REST, GraphQL and gRPC (see api-design).
license: MIT
---

# gRPC Services

The `.proto` file is a binary wire contract: field numbers and types can never change meaning once a client has shipped. Protect the contract with tooling, put a deadline on every call, and remember that HTTP/2 connections are long-lived, which changes how load balancing works.

## When to use

- Writing or changing `.proto` files, or adding a new gRPC service.
- Implementing a gRPC server or client in any language.
- Calls hang, time out in chains, or retries cause duplicates.
- All traffic goes to one backend pod, or connections drop behind a proxy.
- Browsers or third parties need to call a gRPC service.

Not for: choosing a protocol (the api-design skill has the comparison table and a status-code table in `references/graphql-and-grpc.md`), or message streaming between services through a broker (see event-driven-architecture).

## Workflow

1. **Design the proto** with the rules below, in a dedicated `proto/` directory with one package per API version.
2. **Lint and check compatibility:** `buf lint` and `buf breaking` locally and in CI.
3. **Generate code** with `buf generate` (or `protoc`) from a checked-in config. Don't hand-edit generated files.
4. **Implement the server** with interceptors for recovery, tracing, logging, metrics and auth, and a single place that maps domain errors to status codes.
5. **Implement clients** with deadlines on every call, retries in service config, and an explicit load-balancing choice.
6. **Add the standard health service** and wire it to readiness probes.
7. **Test** with an in-process server, then manually with `grpcurl`.
8. **Instrument** per-method latency, status codes and in-flight streams (see the observability skill).

## Proto design

```proto
syntax = "proto3";

package acme.orders.v1;

import "google/protobuf/field_mask.proto";
import "google/protobuf/timestamp.proto";

service OrderService {
  rpc GetOrder(GetOrderRequest) returns (GetOrderResponse);
  rpc ListOrders(ListOrdersRequest) returns (ListOrdersResponse);
  rpc UpdateOrder(UpdateOrderRequest) returns (UpdateOrderResponse);
}

message Order {
  reserved 5;                    // removed field: number never reused
  reserved "legacy_status";      // and neither is its name
  string id = 1;
  string customer_id = 2;
  OrderStatus status = 3;
  google.protobuf.Timestamp created_at = 4;
  optional string coupon_code = 6;   // presence matters: unset vs ""
}

enum OrderStatus {
  ORDER_STATUS_UNSPECIFIED = 0;  // zero value has no business meaning
  ORDER_STATUS_PENDING = 1;
  ORDER_STATUS_SHIPPED = 2;
}

message GetOrderRequest { string id = 1; }
message GetOrderResponse { Order order = 1; }

message ListOrdersRequest {
  int32 page_size = 1;
  string page_token = 2;
}
message ListOrdersResponse {
  repeated Order orders = 1;
  string next_page_token = 2;
}

message UpdateOrderRequest {
  Order order = 1;
  google.protobuf.FieldMask update_mask = 2;
}
message UpdateOrderResponse { Order order = 1; }
```

Rules:

| Rule | Why |
| --- | --- |
| Package includes a major version (`acme.orders.v1`) | Breaking changes go into `v2`, served side by side until clients migrate |
| Each RPC has its own request and response message | You can add fields to one RPC without affecting others |
| Never change a field's number or type | The wire format identifies fields by number; old clients would misread data |
| `reserved` every removed field number **and** name | Prevents accidental reuse that corrupts old clients' data |
| Enum zero value is `<ENUM>_UNSPECIFIED` | Proto3 defaults to 0; it must mean "not set" |
| Enum values prefixed with the enum name | Enum values share the package scope in C++ and some other languages |
| `optional` (or wrapper types) where unset differs from zero/empty | Proto3 scalars otherwise can't express "not provided" |
| `page_size` / `page_token` / `next_page_token` for lists | Standard pagination; cap `page_size` on the server |
| `FieldMask` for partial updates | Distinguishes "set to empty" from "don't touch" |
| Well-known types for time (`Timestamp`, `Duration`) | Consistent across languages |

Google's API Improvement Proposals (aip.dev) are the most complete style guide; `buf lint` enforces a common subset.

## Contract checks with buf

A minimal `buf.yaml` at the repo root (buf v2 config format; check the buf docs for your version):

```yaml
version: v2
modules:
  - path: proto
lint:
  use:
    - STANDARD
breaking:
  use:
    - FILE
```

```bash
buf lint
buf breaking --against '.git#branch=main'
buf generate
```

Run `buf lint` and `buf breaking` as required CI checks on every change under `proto/`. A failing `buf breaking` means "make a new version", not "add an exception", unless the API owner explicitly accepts the break.

For request validation, declare rules in the proto with a validation library (for example protovalidate) instead of hand-written checks in every handler.

## Deadlines

Every client call sets a deadline. A call without one can wait forever and pile up resources across a call chain.

| Language | Setting a deadline |
| --- | --- |
| Go | `ctx, cancel := context.WithTimeout(ctx, 2*time.Second); defer cancel(); client.GetOrder(ctx, req)` |
| Java | `stub.withDeadlineAfter(2, TimeUnit.SECONDS).getOrder(req)` |
| Python | `stub.GetOrder(req, timeout=2.0)` |
| C# | `client.GetOrderAsync(req, deadline: DateTime.UtcNow.AddSeconds(2))` |
| Node (`@grpc/grpc-js`) | `client.getOrder(req, { deadline: Date.now() + 2000 }, callback)` |

- **Propagate** the incoming deadline: on the server, pass the request's context (Go `ctx`, C# `context.CancellationToken`, Java's current `Context`) to downstream calls so they inherit the remaining time.
- Check for cancellation in long handlers and stop work when the client has gone.
- Pick deadlines from the dependency's latency SLO, not a round number. See the resilience-patterns skill.

## Retries

- Configure retries in the **service config**, not in hand-written loops, and only for idempotent methods:

```json
{
  "methodConfig": [{
    "name": [{ "service": "acme.orders.v1.OrderService", "method": "GetOrder" }],
    "timeout": "2s",
    "retryPolicy": {
      "maxAttempts": 3,
      "initialBackoff": "0.1s",
      "maxBackoff": "1s",
      "backoffMultiplier": 2,
      "retryableStatusCodes": ["UNAVAILABLE"]
    }
  }]
}
```

- Retry `UNAVAILABLE` by default. Retry `DEADLINE_EXCEEDED` or `RESOURCE_EXHAUSTED` only for idempotent methods and with backoff.
- For non-idempotent methods (create, charge), add an idempotency key field to the request and dedupe on the server before enabling any retry.
- Retry at one layer only. If a service mesh also retries, turn one of them off.

## Errors

- Map domain errors to status codes in **one place** (an error-mapping function or server interceptor). Never let handlers return `UNKNOWN` or leak internal error strings.
- Use the right code: `INVALID_ARGUMENT` for bad input, `NOT_FOUND`, `ALREADY_EXISTS`, `FAILED_PRECONDITION` for wrong state, `ABORTED` for concurrency conflicts, `PERMISSION_DENIED` vs `UNAUTHENTICATED`, `UNAVAILABLE` for transient failures. The full table with retry guidance is in the api-design skill's `references/graphql-and-grpc.md`.
- Attach structured details with `google.rpc.Status` details: `BadRequest` (field violations), `ErrorInfo` (stable `reason` and `domain`), `RetryInfo` (retry delay). Clients branch on these, not on message text.

## Choosing a call type

| Call type | Use when | Watch out for |
| --- | --- | --- |
| Unary | Request/response; most RPCs | — |
| Server streaming | Server sends many results or live updates (tailing, progress) | Long-lived streams need keepalive, reconnect and resume logic |
| Client streaming | Client uploads many items or chunks | Server must bound total size and time |
| Bidirectional streaming | Interactive sessions (chat, collaborative editing) | Hardest to load-balance, test and observe; use only when needed |

- Message size limits apply per message, and defaults differ by implementation (many default to a few MB on receive). Check your library's defaults. For large data, stream chunks or upload to object storage and pass a reference (see the file-storage-uploads skill).
- Streams pin a client to one backend for their whole life. Prefer unary calls unless streaming is truly needed.

## Load balancing and connections

gRPC multiplexes many calls over one long-lived HTTP/2 connection. Connection-level (L4) load balancing therefore sends **all** of a client's calls to one backend. A plain Kubernetes ClusterIP Service behaves this way.

Pick one:

- **Client-side balancing:** resolve all backends (e.g. a headless Kubernetes Service with a `dns:///` target) and use the `round_robin` policy via service config: `{"loadBalancingConfig": [{"round_robin": {}}]}`.
- **L7 proxy or service mesh** that balances per request (Envoy, Linkerd, Istio, or a cloud load balancer with HTTP/2 and gRPC support).
- **Server `MaxConnectionAge`** (where supported) so clients reconnect periodically and spread out after scale-ups.

Also:

- Every proxy on the path must support HTTP/2 end to end, or gRPC fails in confusing ways.
- Align client keepalive pings with server keepalive enforcement. Pinging more often than the server allows gets the connection closed (`ENHANCE_YOUR_CALM` / "too many pings").

## Health, reflection and tooling

- Implement the standard `grpc.health.v1.Health` service and set the status to `SERVING` only when dependencies needed to serve are ready. Kubernetes can probe it natively with `grpc` probes (stable since Kubernetes 1.27), or use `grpc_health_probe`.
- Server reflection lets tools discover services without proto files. Enable it for internal and development environments; consider disabling it on public endpoints.
- Manual testing with `grpcurl`:

```bash
grpcurl -plaintext localhost:50051 list
grpcurl -plaintext localhost:50051 describe acme.orders.v1.OrderService
grpcurl -plaintext -d '{"id": "ord_123"}' localhost:50051 acme.orders.v1.OrderService/GetOrder
```

Drop `-plaintext` for TLS endpoints. Never point manual write calls at production without explicit confirmation from the user.

## Interceptors, auth and transport security

- Server interceptor order (outermost first): panic/exception recovery, tracing, logging, metrics, authentication, authorization, validation.
- Use OpenTelemetry's gRPC instrumentation for traces and metrics instead of hand-rolled timing.
- Send credentials as metadata (`authorization: Bearer <token>`) via per-RPC credentials. Most implementations refuse to send per-RPC credentials over insecure channels, which is intentional.
- Authorize per method (and per resource) in the server, not only at the edge. See the auth-implementation skill for service-to-service identity.
- Use TLS everywhere outside local development. Use mTLS for service-to-service traffic, either directly or through a service mesh. Insecure credentials are for local development only.

## Browsers and REST clients

| Option | How |
| --- | --- |
| gRPC-Web | Browser client library plus a proxy (e.g. Envoy) or a server with built-in gRPC-Web support |
| Connect protocol | Connect libraries serve gRPC, gRPC-Web and a simple HTTP/JSON protocol from the same handlers |
| JSON transcoding | Map RPCs to REST routes with `google.api.http` annotations, served by a gateway (e.g. grpc-gateway, Envoy's transcoder, ASP.NET Core JSON transcoding) |

Renaming a field keeps the binary format but breaks JSON transcoding and JSON clients. Treat renames as breaking when JSON is in play.

## Testing

- Unit-test handlers with an in-process server: Go `bufconn`, Java `InProcessServerBuilder`/`InProcessChannelBuilder`, .NET `WebApplicationFactory`, Python a server on a local port.
- Test deadline behavior: a slow fake dependency must produce `DEADLINE_EXCEEDED`, not a hang.
- Test error mapping: each domain error yields the expected code and details.
- `buf breaking` is your contract test for wire compatibility.

## Anti-patterns

- **No deadlines**: hung calls pile up across services.
- **Reusing a removed field number**: old clients silently misread data.
- **Shared request messages** across RPCs: one change ripples through unrelated methods.
- **Business meaning on enum value 0**: unset values look like a real state.
- **L4 load balancing**: one pod takes all traffic while others sit idle.
- **Retrying non-idempotent methods**: duplicate orders or charges.
- **Returning `UNKNOWN` / `INTERNAL` for everything**: clients can't tell bad input from outages.
- **Huge messages** instead of streaming or object storage: memory spikes and size-limit errors.
- **Skipping `buf breaking`** because "we only added a field": renumbering and type changes slip in.

## Done when

- Protos are versioned by package, linted, and `buf breaking` runs as a required CI check.
- Removed fields are reserved by number and name; enums start with `_UNSPECIFIED = 0`.
- Every client call has a deadline; servers propagate deadlines downstream.
- Retries are configured in service config for idempotent methods only.
- Domain errors map to correct status codes with structured details, in one place.
- Load balancing is per request (client-side or L7), verified by watching traffic spread across backends.
- The health service is implemented and used by readiness probes; TLS or mTLS is on outside local development.
