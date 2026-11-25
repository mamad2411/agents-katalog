# RPC & Message Protocol Design

## Purpose
Design, version, and verify RPC and message protocols with interface definition languages: Protobuf proto3 service modeling, Cap'n Proto zero-copy schemas, buf-managed breaking-change gates, gRPC error and deadline semantics, streaming patterns, and wire-compatibility proof across service versions.

## Use when
- Defining or evolving a gRPC, Cap'n Proto, or JSON-RPC service surface between internal microservices.
- Choosing message field layouts, numbering, streaming modes, error codes, retry budgets, or payload size limits.
- Introducing a v2 API alongside v1 without breaking deployed clients.
- Auditing an existing protocol for wire-compatibility hazards, oversized payloads, or ambiguous error contracts.

## Do not use when
- The interface is a public REST or webhook surface governed by OpenAPI conventions rather than an IDL; use the API design workflow instead.
- Only in-process function calls are involved with no serialization boundary.
- The transport is a game-engine realtime packet layer with fixed binary layouts owned by netcode; that work belongs to engine networking, not RPC IDL design.

## Required context
- Service inventory with methods, message types, and current deployed client versions.
- IDL toolchain pins: buf 1.50.0, protoc 27.3, grpcurl 1.9.1, capnp 1.0.2 where applicable.
- Compatibility budget: which field changes are forbidden, payload ceiling such as 256 KB per response, and p99 latency target such as 120 ms.
- Error taxonomy mapping business failures to gRPC status codes with retryability labels.

## Procedure
1. **Model the service in IDL first**: author `billing/v1/invoice.proto` with package `billing.v1`, explicit `option go_package` and `java_package`, and every RPC declaring request, response, and streaming mode. Generate stubs with `buf generate` and refuse hand-written stub edits.
2. **Apply numbering and evolution rules**: never reuse or repurpose a field number, mark removed fields `reserved`, add new behavior only through new field numbers or new methods, and ship v2 as package `billing.v2` beside v1 with a documented migration window of 90 days.
3. **Fix the error contract**: map business failures to the 17 canonical gRPC status codes, for example `NOT_FOUND` for missing invoices and `FAILED_PRECONDITION` for closed periods, attach machine-readable details via `google.rpc.Status`, and label each method idempotent or not for retry policy.
4. **Bound time and bytes**: set per-method deadlines such as 800 ms for `GetInvoice` and 5 s for `ExportLedger`, cap responses at 256 KB with pagination beyond it, and require client retries to use capped exponential backoff with jitter, base 100 ms, max 3 attempts, only on idempotent methods.
5. **Gate compatibility in CI**: run `buf lint` plus `buf breaking --against '.git#branch=main'` on every change; zero breaking findings is the merge gate. Probe live surfaces with `grpcurl -plaintext billing:50051 list billing.v1.InvoiceService`.
6. **Verify end to end**: run `scripts/verify.sh`, load-test the golden method set at 500 RPS checking p99 under 120 ms, and replay v1 clients against v2 servers proving old fields still decode.

## Decision rules
- **IDL is the contract**: the checked-in schema is normative; generated code and documentation derive from it and are never edited by hand.
- **Numbers are forever**: field and method numbers are never reused, and deletions become `reserved` entries with a reason comment.
- **Additive only within a major**: minor versions add optional fields and methods; renames, type changes, and semantic changes require a new package version.
- **Errors are typed**: every failure returns a canonical status code plus structured details; free-text-only errors are forbidden.
- **Budgets are enforced**: methods exceeding the deadline or payload ceiling fail verification regardless of functional correctness.

## Evidence required
- Protocol specification following `templates/rpc-protocols-spec.md` with service inventory, numbering log, and error taxonomy.
- Clean `buf lint` and `buf breaking` reports against the main branch.
- Load-test percentiles and v1-against-v2 replay log proving wire compatibility.
- Passing execution log from `scripts/verify.sh`.

## Output contract
- Versioned IDL package with generated stubs and migration notes.
- Documented error taxonomy with retryability labels per method.
- Compatibility and performance evidence clearing the merge gate.

## Stop conditions
- Zero breaking findings with p99 under 120 ms at 500 RPS on the golden method set.
- v1 clients replay cleanly against v2 servers with old fields decoding correctly.
- Token budget exhausted.
- Blocked on external dependency.

## Escalation rules
- Escalate to the service owner if a required semantic change cannot be expressed additively and a major version with client migration must be scheduled.
- Escalate to the lead architect if payload or latency budgets conflict with product requirements, so pagination or streaming redesign can be approved.
