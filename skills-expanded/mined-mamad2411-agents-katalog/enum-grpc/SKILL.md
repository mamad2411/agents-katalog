---
name: enum-grpc
description: gRPC service enumeration through reflection, proto descriptor extraction, method signature mapping, authentication-requirement classification, and plaintext-exposure detection. Passive-first service discovery with active probing gated by authorization and scope validation.
disable-model-invocation: true
risk: safe-active
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft, service-inventory, method-signature-map, auth-classification]
---

# Enum gRPC

Use this skill to enumerate gRPC services, map their method signatures, and classify authentication requirements. gRPC uses Protocol Buffers (protobuf) over HTTP/2, which hides methods behind binary serialization. Enumeration relies on server reflection, proto file discovery, and safe probing. This skill does not include exploitation or injection testing.

## Required inputs

- Validated target host and port for each gRPC endpoint.
- Scope file defining allowed testing methods and rate limits.
- Authorization cache valid for all in-scope hosts.
- Optional: .proto files, service definitions, or API documentation provided by the target owner.
- Optional: gRPC metadata or tokens if available for authenticated probing.

## Required gates

1. Use `pentest_agent_load_config` and `pentest_agent_validate_policy` before planning.
2. Use `pentest_agent_parse_scope` and `pentest_agent_validate_target` for every gRPC host and port before contact.
3. Use `pentest_agent_check_authorization` before any active request that includes credentials or performs authenticated probing.
4. Use `pentest_agent_build_command` for dry-run preview of gRPC reflection and method-calling tools.
5. Use `pentest_agent_execute_tool` for all active probing with rate-limit and output policy enforcement.
6. Use `pentest_agent_append_evidence` for service inventories, method maps, and auth classifications.

## Workflow

### Phase 1 — Service endpoint discovery

Locate gRPC endpoints before probing individual services.

- Identify gRPC ports. Common gRPC ports: 50051 (plaintext default), 443 (TLS with HTTP/2), 8443, 9090. gRPC-web often runs on 443 or standard web ports.
- If the target is a web application, inspect JavaScript for gRPC-web client configuration: `grpc-web`, `@grpc/grpc-js`, `protobufjs`, or `google-protobuf` imports that reveal service endpoints.
- Test whether standard web ports respond to HTTP/2 with gRPC content types. Send a request with `Content-Type: application/grpc` and observe the response.
- For internal or backend targets, scan common gRPC port ranges using catalog network tools. Only scan ports explicitly in scope.
- Document every discovered gRPC endpoint: host, port, TLS status, and whether HTTP/2 is confirmed.

### Phase 2 — Server reflection enumeration

Server reflection is the primary discovery mechanism for gRPC services.

- Use a gRPC reflection client (like `grpcurl` from the catalog) to list all registered services on each endpoint.
- If TLS is enabled, use the `-insecure` flag only if the certificate is self-signed and the target is explicitly in a lab or internal scope. For production targets, respect TLS.
- For each discovered service, list all RPC methods. Record the method type: unary (single request, single response), server-streaming, client-streaming, or bidirectional-streaming. Streaming methods have different timeout and rate-limit characteristics.
- For each method, describe the request and response message types using the reflection descriptor. This reveals the full parameter surface.
- If server reflection is disabled, record it and move to Phase 3. Do not attempt to brute-force service or method names.

### Phase 3 — Proto file and descriptor discovery

When reflection is unavailable, look for proto definitions through other channels.

- Check for exposed `.proto` files on the target web server: common paths include `/proto/`, `/protos/`, `/api/proto/`, `/grpc/`.
- Check for compiled protobuf descriptors (`.desc`, `.pb`, `.protoset` files) that applications sometimes expose.
- Search JavaScript bundles for protobuf message definitions. gRPC-web clients often embed the proto definitions as JSON descriptors or in serialized form.
- Check public protobuf registries (like Buf Schema Registry) for the target organization. Many teams publish proto files publicly.
- If no proto information is recoverable, document the limitation and request documentation from the target owner.

### Phase 4 — Method signature and parameter mapping

Build a complete signature map for every discovered method.

- For each method, document the fully qualified service name, method name, request message type, and response message type.
- Parse the request message fields: field name, field number, type, and whether the field is required, optional, or repeated. This reveals every parameter the method accepts.
- Identify sensitive parameter patterns: fields named `token`, `password`, `secret`, `key`, `auth`, `admin`, `role`, `permissions`, `user_id`, `account_id`.
- Identify dangerous method patterns: methods named `Delete`, `Destroy`, `Remove`, `Update`, `SetPermission`, `AssignRole`, `CreateUser`, `GenerateToken`.
- Build a service-to-method inventory with parameter detail for downstream testing.

### Phase 5 — Authentication-requirement classification

Classify every method by its authentication posture.

- Call a simple read method (like `Get` or `List`) without any metadata or authentication headers. Record whether the server returns data, an unauthenticated error, or a permission-denied error.
- Call the same method with a valid token or metadata if available. Record the difference in behavior.
- Test a mutation method without authentication, if one is available and the test is read-only (e.g., a `Validate` method that does not persist changes). An unauthenticated mutation that succeeds is critical.
- Test whether gRPC metadata-based authentication is enforced consistently across methods. gRPC services often implement interceptors on the server side; a misconfigured interceptor may skip auth for certain methods.
- Test whether services running on different ports have different authentication policies. A gRPC service on port 50051 (internal) may have no auth while the same service on port 443 (external) requires it.
- Produce an auth-requirement matrix: service, method, auth required, token privilege tier if tested.

### Phase 6 — Transport security and plaintext detection

gRPC supports both TLS and plaintext transport. Plaintext in production is a finding.

- For each endpoint, determine whether TLS is enforced. A gRPC endpoint accepting plaintext HTTP/2 on an internal or production network is a transport-security gap.
- Test whether the same service is available on both TLS and plaintext ports. Common pattern: TLS on 443, plaintext on 50051 or 9090.
- Check whether the gRPC service advertises `grpc-exp` (gRPC Experimental) or deprecated protocol versions. These may lack the security features of the current protocol.
- Check whether TLS implements mutual TLS (mTLS). For internal service-to-service gRPC, mTLS is expected. Absence of mTLS on internal endpoints is a finding.
- Document the transport security posture for every endpoint.

## Decision points

- Reflection disabled, no proto files: classification is limited. Document the services that could be discovered (if any) and recommend enabling reflection in a controlled manner or providing documentation.
- Mutation testing: only call mutation methods for classification if the method has a side-effect-free read path (like `Validate` or `Check`). Never call destructive mutations during enumeration.
- Port scanning: if the target uses non-standard gRPC ports, scan the documented port range from scope. Do not extend port scanning beyond the scope boundary.
- Internal vs external: if the same service is accessible on both internal and external ports, test both and document the policy difference.

## Prohibited behavior

No calling destructive or state-changing mutations during enumeration. No brute-force of service or method names. No exploitation of discovered methods. No credential guessing via gRPC metadata. No probing of out-of-scope hosts or ports. No downgrading TLS connections to plaintext without explicit authorization. Do not run raw shell commands when a `pentest_agent_*` gate exists.

## Stop conditions

Stop on an endpoint when all services are listed, all methods are signature-mapped, and auth classification is complete. Stop if a method call results in a state change or error suggesting data modification. Stop if the authorization cache expires. Stop if the target returns a rate-limit or connection-refused response.

## Evidence

Append evidence via `pentest_agent_append_evidence`:
- gRPC endpoint inventory with transport-security details.
- Service list per endpoint with method counts.
- Method signature map: service, method, request type, response type, parameter fields.
- Auth-requirement matrix per method per privilege tier.
- Transport-security posture: TLS version, cipher, mTLS status, plaintext availability.

Never store gRPC response payloads containing user data, credentials, tokens, PII, or internal identifiers. Redact proto definitions containing internal architecture details before storage.

## Report handoff

Record findings via `pentest_agent_record_finding` for: server reflection enabled on production (medium), plaintext gRPC in production (high), missing mTLS on internal service-to-service endpoints (medium), unauthenticated mutation access (critical), inconsistent auth policy across services (high), and deprecated protocol versions (low). Render the final report with `pentest_agent_render_report`.
