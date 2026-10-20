---
name: connect-rpc-basics
description: >
  Build APIs with Connect (Connect-RPC): Protobuf services over HTTP, multi-protocol
  (Connect, gRPC, gRPC-Web), handlers/interceptors, errors/codes, and browser-friendly
  clients. Use for owned services migrating from or alongside gRPC — not raw gRPC-only
  deep mesh policy (use gRPC skills) or generic REST OpenAPI design alone.
---

# Connect-RPC Basics

## Scope And Authorization

- **In scope:** services and protos you own.
- **Out of scope:** attacking third-party Connect/gRPC endpoints without authorization.
- Prefer TLS everywhere; do not disable auth interceptors for convenience in prod.
- Pair with `code-quality-standards`, `protobuf-grpc-reverse-engineering` for unknown protos (authorized), and auth skills for JWT/mTLS.

## When To Use

- Defining `.proto` services consumed via **Connect** Go/TS/etc. generators.
- Supporting browsers (gRPC-Web / Connect protocol) without heavy Envoy-only setups.
- Tokens: Connect-RPC, connectrpc, protobuf HTTP, gRPC-Web, interceptors, idempotency.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Classic gRPC deadlines/retry only | `grpc-deadline-and-retry` |
| Protobuf schema recovery | `protobuf-grpc-reverse-engineering` |
| REST/OpenAPI-first | `api-recon-and-docs` / OpenAPI skills |
| Client-side LB | `client-side-load-balancing` |

## Protocol Options

| Protocol | Content-Type (typical) | Clients |
| --- | --- | --- |
| Connect | `application/connect+proto` / json | Simple HTTP/1.1 friendly |
| gRPC | `application/grpc` | Standard gRPC stacks |
| gRPC-Web | `application/grpc-web*` | Browsers |

One handler can often serve multiple protocols.

## Workflow

### 1. Confirm scope and success

1. Service name, languages, browser need, auth model, compatibility with existing gRPC.
2. Success: codegen builds; unary + streaming as required; errors map cleanly; auth interceptor works.
3. Version protos (`package`, `buf` breaking checks).

### 2. Define API

```protobuf
syntax = "proto3";
package example.v1;
option go_package = "example/gen/example/v1;examplev1";

service Greeter {
  rpc Greet(GreetRequest) returns (GreetResponse);
}

message GreetRequest { string name = 1; }
message GreetResponse { string message = 1; }
```

1. Use `buf generate` or protoc plugins for Connect.
2. Keep breaking-change policy (field numbers reserved).

### 3. Implement server (conceptual Go)

```go
// Handler implements GreeterHandler
func (s *Server) Greet(ctx context.Context, req *connect.Request[examplev1.GreetRequest]) (*connect.Response[examplev1.GreetResponse], error) {
    if req.Msg.Name == "" {
        return nil, connect.NewError(connect.CodeInvalidArgument, errors.New("name required"))
    }
    return connect.NewResponse(&examplev1.GreetResponse{Message: "hello " + req.Msg.Name}), nil
}

// Mount on HTTP mux with path from generated code
// mux.Handle(examplev1connect.NewGreeterHandler(svc, connect.WithInterceptors(auth)))
```

### 4. Interceptors and cross-cutting

| Concern | Practice |
| --- | --- |
| Authn | Validate bearer/mTLS in interceptor |
| Authz | Per-procedure checks |
| Logging | Procedure, peer, code; redact |
| Timeouts | Context deadlines from client |
| Validation | protovalidate / manual |

### 5. Clients

```bash
# curl-ish mental model: Connect often works with ordinary HTTP tools for unary JSON mode
curl -s -X POST "https://api.example.com/example.v1.Greeter/Greet" \
  -H "Content-Type: application/json" \
  -d '{"name":"ada"}'
```

1. Generated clients for type safety.
2. Browser: prefer Connect protocol or gRPC-Web as configured CORS.

### 6. Verify

1. Unit test handlers with in-memory client.
2. Integration: all three protocols if enabled.
3. Negative: unauthenticated → `CodeUnauthenticated`.
4. Load: streaming backpressure behavior acceptable.

### 7. Operate

1. Metrics by procedure and code.
2. Reflect carefully — disable server reflection in prod if not needed.
3. Gateway/CORS for browser origins allowlist.

## Error Codes (selected)

| Code | When |
| --- | --- |
| InvalidArgument | Validation |
| Unauthenticated | No/invalid credentials |
| PermissionDenied | Authz fail |
| NotFound | Missing entity |
| ResourceExhausted | Quota |
| Internal | Unexpected |

Do not leak stack traces to clients.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| API | Versioned protos + buf | Ad-hoc JSON drift per client |
| Auth | Interceptor on all procedures | Trust network only |
| Browser | Explicit CORS + Connect | `Access-Control-Allow-Origin: *` + cookies |
| Errors | Typed codes | 200 with error string only |
| Compat | Multi-protocol intentional | Accidental gRPC-only break for web |

## Output Checklist

- [ ] Proto service defined and versioned
- [ ] Codegen + handler implemented
- [ ] Protocols required for clients enabled
- [ ] Interceptors for auth/log/timeout
- [ ] Tests for success and error codes
- [ ] CORS/TLS/auth verified for browser if any
- [ ] Metrics/dashboards for procedures
- [ ] Residual compatibility risks noted

## Rules

- Owned APIs only for exposure changes.
- Prefer protobuf contracts over undocumented JSON.
- Evidence via tests and curl/client calls.
- Focus on **Connect-RPC basics**; deep gRPC mesh and RE are other skills.
