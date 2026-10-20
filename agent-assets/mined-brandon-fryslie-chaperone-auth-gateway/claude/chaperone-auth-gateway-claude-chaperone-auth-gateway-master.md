# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

**Chaperone** is a Man-in-the-Middle (MITM) proxy that injects API credentials into requests. Applications use the proxy without handling secrets directly, enabling centralized, audited credential management.

**Security Model:** 5-layer defense-in-depth (credential isolation, placeholder auth, user/permission isolation, network hardening, audit logging).

## Build & Development Commands

### Build
```bash
make build              # Build chaperone binary to ./chaperone
make all                # Alias for build
make release            # Build release binaries for all platforms (scripts/release.sh)
make version            # Print version from the VERSION file
```

### Testing
```bash
make test               # Run all tests with verbose output
make test-race          # Run tests with race detector (slow but catches concurrency bugs)
go test ./...           # Same as make test
go test -short ./...    # Skip long integration tests
go test -race ./...     # Run with race detection
```

**Run specific tests:**
```bash
go test ./internal/auth -run TestBearerStrategy            # Single test
go test ./test/integration/... -run TestSelectiveMITM      # Integration tests only
```

**View test coverage:**
```bash
go test ./... -coverprofile=coverage.out -coverpkg=./...
go tool cover -html=coverage.out                           # Opens in browser
```

### Linting & Formatting
```bash
make lint               # Run golangci-lint (8 checkers enabled)
make fmt                # Format all Go files with gofmt
```

### Cleanup
```bash
make clean              # Remove chaperone binary and test artifacts
```

### Help
```bash
make help               # Show all targets with descriptions
```

## CLI Commands Architecture

- `cmd/chaperone/cmd/inject.go` - **Inject mode**: Start proxy with credential injection (main mode)
- `cmd/chaperone/cmd/run.go` - **Run mode**: Start proxy + spawn a child process with the proxy env injected (thin wrapper over `internal/run`)
- `cmd/chaperone/cmd/examine.go` - **Examine mode**: Auth discovery (passthrough MITM logging)
- `cmd/chaperone/cmd/check.go` - **Check mode**: Security posture assessment
- `cmd/chaperone/cmd/mcp.go` - **MCP mode**: stdio MCP server for dynamic credential grants (thin client of the daemon's control socket)
- `cmd/chaperone/cmd/root.go` - Root command, config resolution, CA path helpers (incl. `getControlSocketPath`)

## Core Proxy Architecture
The request pipeline is split into one file per concern. `handlers.go` is now only the package doc comment describing the split — the handlers live in the dedicated files below.
- `internal/proxy/server.go` - Server setup, `NewWithMITM()`, `NewExamineProxy()`, start/stop
- `internal/proxy/connect_handler.go` - `connectHandler` - MITM vs transparent tunnel decision
- `internal/proxy/policy_handler.go` - `policyHandler` (methods/paths/body size) plus `dropHandler` and `stripHandler` (drop/strip policy)
- `internal/proxy/auth_handler.go` - `authHandler` (**main injection**: fetch secret → apply strategy) and `securityStripAuthHandler` (strip client-supplied auth before injecting)
- `internal/proxy/recording_handler.go` - `recordRequestHandler/recordResponseHandler` - traffic recording
- `internal/proxy/proxy_auth.go` - Proxy-level authentication: `GenerateProxySecret()`, `proxyAuthHandler`, `proxyAuthConnectHandler` (gate access to the proxy itself). The gate is mandatory: `NewWithMITM`/`NewExamineProxy` take the secret as a required positional parameter and error on an empty one, so an ungated intercepting proxy is unconstructible. All modes (inject/run/examine) generate a per-run secret; inject prints the credentialed `HTTP_PROXY` URL at startup. Clients authenticate at the CONNECT; requests decrypted from that tunnel carry no `Proxy-Authorization`, so the connect gate stamps the connection's `requestMetadata.proxyAuthenticated` and the request gate trusts the stamp.
- `internal/proxy/conditions.go` - `ChaperoneCondition()` - filter which requests get auth
- `internal/proxy/cert_adapter.go` - Adapter for goproxy cert store
- `internal/proxy/upstream_trust.go` - Outbound-trust policy: upstream server certs on MITM'd connections are always verified (goproxy's transport default skips verification; `configureTransport` replaces it). `MITMOptions.UpstreamCAs` / `[server] upstream_ca_file` pin trust to specific roots; nil/unset = system roots. "Verification off" is unrepresentable.
- Examine-mode handlers live in `internal/examine/handlers.go` (`ConnectHandler`/`RequestHandler`/`ResponseHandler`), not in `internal/proxy`.

## Authentication System
- `internal/auth/strategy.go` - `Strategy` interface
- `internal/auth/bearer.go` - `Authorization: Bearer` strategy
- `internal/auth/header.go` - Custom header strategy (e.g., `X-API-Key`)
- `internal/auth/headers_util.go` - **Case-insensitive header matching & replacement**
  - `findHeaderVariants()` - Find all case variations of header
  - `setHeaderPreservingCapitalization()` - Replace header, preserve client's capitalization
- `internal/auth/registry.go` - Strategy registry (register/lookup strategies)

## Secrets Management
- `internal/secrets/registry.go` - Secret provider registry, `Fetch()`, preloading. `Registry.Fetch` is the SINGLE normalizer for fetched values: trims surrounding whitespace (a trailing newline is transport convention, not part of the secret) and rejects empty-after-trim as `ErrSecretNotFound`. Providers return values verbatim and detect only their own source's absence semantics.
- `internal/secrets/env.go` - Environment variable provider (`env:VAR_NAME`); unset (via `LookupEnv`) = not found
- `internal/secrets/file.go` - File provider (`file:/path/to/secret`). Gated by `internal/filetrust` with the `OwnerOnly` bar: any group/world permission bit (read included), foreign-uid ownership, or a non-regular file is a loud refusal; a symlinked path is judged by the target actually read (fstat on the open handle, no TOCTOU)
- `internal/secrets/keychain.go` - macOS Keychain provider (`keychain:service/account`)
- `internal/secrets/errors.go` - `ErrSecretNotFound` is an ALIAS of `internal/errors.ErrSecretNotFound` (one identity, so `errors.Is` matches across both names)

## File Trust (shared)
- `internal/filetrust/filetrust.go` - The one file-trust decision for the codebase (never hand-roll a second mode/owner check). `File{Desc, Stakes, Bar}.Verify(fi, uid, path)` is pure over (FileInfo, uid); `ReadFile` owns the open → fstat-handle → verify → read sequence so the inode that passed verification is the inode read. Two canonical bars: `NoUntrustedWrites` (perm&0o022 — config: integrity matters, contents are refs) and `OwnerOnly` (perm&0o077 — secret files / private keys: contents ARE the value). Consumers: `config.Load`, the `file:` secret provider; CA-key loading (3at.9) should consume it too.

## Service Configuration
- `internal/service/types.go` - `Service` struct (host pattern, auth strategy, policy)
- `internal/service/registry.go` - Interface for service lookup
- `internal/service/registry_impl.go` - Implementation (register/lookup services)
- `internal/service/matcher.go` - `ShouldMITM()` - check if host needs MITM
- `internal/service/policy.go` - Policy struct (allowed methods/paths, max body size)
- `internal/service/policy_enforcer.go` - Policy validation logic (`CheckPath` matches via `pathPattern`)
- `internal/service/pathmatch.go` - **THE path-pattern vocabulary and matcher** (never hand-roll a second path match). One small language — exact path or `<prefix>/*` (subtree, any depth) — consumed by the allow list (`CheckPath`), the drop list (`URLPattern`), and grant containment (`Narrows`). One documented match policy: request paths are normalized first (dot-segments resolved, duplicate slashes collapsed, trailing slash dropped — `/v1/../admin` is judged as `/admin`) and compared case-insensitively. Patterns must be canonical (leading `/`, already clean); `ValidatePathPatterns` is the rule the entry boundaries apply — `config.Validate` (services + grantable bounds) and `grant.Enforcer.Authorize` — so an unmatchable pattern fails at the door; runtime parse failure fails closed
- `internal/service/urlpattern.go` - Drop-rule matcher over (host, path): host wildcards (`*.example.com`, bare domain = self + subdomains), path part is a `pathPattern`. `ParseURLPattern` errors on anything outside the vocabulary — an unenforceable deny rule must not construct
- `internal/service/narrow.go` - `Narrows()` — grant-scope containment (methods/paths/body), path containment decided over the same folded, normalized form the matcher uses

## Examine Mode (Auth Discovery)
- `internal/examine/handlers.go` - goproxy handlers (`ConnectHandler`/`RequestHandler`/`ResponseHandler`) — always-MITM passthrough
- `internal/examine/logger.go` - Request/response logging
  - `Config` - Control what's logged (body, params, cookies, responses)
  - `LogRequest()` - Log request with auth-relevant headers
  - `LogResponse()` - Log response (status, headers, cookies)
- `internal/examine/report.go` / `internal/examine/tracker.go` - Aggregate observed auth across a session into a summary report
- `internal/examine/headers.go` - **Header filtering**
  - `noAuthHeaderPatterns` - Exclusion list (Content-Type, x-stainless-*, etc.)
  - `IsAuthRelevant()` - Filter out noise headers
  - Supports glob patterns, case-insensitive

## Audit Logging
- `internal/audit/logger.go` - Audit trail for credential injections
  - `Logger` - Thread-safe JSON logger
  - `Entry` - Audit log entry (timestamp, event, service, host, path, method, auth_strategy, request_id)
  - `NewLogger()` - Create logger (stdout or file with 0600 permissions)
  - `Log()` - Write audit entry as JSON

## Dynamic Credential Grants (MCP)
Lets Claude Code activate a credential mid-session — without editing config or restarting — by *granting* a pre-approved `(credential ↔ host)` pairing. The secret value never enters the model's context: only a pointer (`env:`/`file:`/`keychain:`) crosses the boundary, and the daemon resolves and injects the credential itself.

- `internal/config/config.go` - `GrantableConfig` — one human-approved `(credential_ref ↔ host_pattern ↔ auth_strategy)` pairing plus the MAXIMAL scope a grant may request. The human-owned source of truth for the grantable universe.
- `internal/grant/enforcer.go` - `Enforcer` — single authority for *what is grantable*. `Authorize(svc)` accepts a proposed grant iff its identity matches one pairing exactly and its scope NARROWS within that pairing's bound (omitted scope = widest, so a bounded pairing requires the grant to state its scope). Built from `Grantable` config at startup; fails loudly on a malformed universe.
- `internal/control/` - Daemon control plane over a localhost-only, 0600 unix socket (`~/.config/chaperone/control.sock`). Four ops: grant / revoke / list / list-grantable.
  - `api.go` - `API` — applies exactly two effects at this one boundary: registry upsert and an audit write. Resolves no secrets, re-decides no policy (delegates wholly to the enforcer).
  - `server.go` / `client.go` - socket transport; the two share `protocol.go` wire types so they cannot drift. A missing daemon makes every client call fail loudly.
  - `protocol.go` - `GrantRequest`/`RevokeRequest` and result/view types. The request type omits operator-only policy fields (client_groups/drop/strip) so they are unrepresentable at the boundary.
- `internal/mcpgrants/server.go` - `NewServer(client ControlClient) *mcp.Server` — stdio MCP server Claude Code spawns. Pure relay: each tool call → one control-API call. Adds vocabulary and delivery only; holds no registry, resolves no secrets. Tool input types ARE the control wire types, so the MCP schema and control contract cannot drift. Enforcer rejections and the no-daemon error come back as `CallToolResult.IsError=true` with the message verbatim — a tool error, not a protocol error.
- `internal/orchestrate/` - Shared daemon assembly for inject/run modes. `Setup` builds the registries + grant enforcer; `CreateProxy` installs the MITM pipeline whenever static services exist OR the grantable universe is non-empty (a runtime grant can add an injection-eligible host with no restart); `StartControlPlane` brings up the control socket. The proxy + control plane share one service registry, grant enforcer, and audit sink.

**Single enforcer:** the proxy pipeline (match host → fetch secret → enforce policy → inject → audit) stays the ONE authority. A runtime grant only adds an entry to the live registry the proxy already consults; it changes no code path.

## MITM / TLS
- `internal/mitm/ca.go` - CA generation/loading (`LoadOrGenerateCA`)
- `internal/mitm/certcache.go` - Certificate cache (generate certs per hostname)

## Configuration
- `internal/config/config.go` - Config structs, validation, defaults
  - `ServerConfig` - Listen address/port
  - `ServiceConfig` - Per-service config (host, auth strategy, credential ref, policy)
  - `LoggingConfig` - Log level

## Logging
- `internal/log/logger.go` - Structured logging helpers
  - Request ID injection (`WithRequestID()`)
  - Sensitive field redaction (auto-redacts secrets, tokens, passwords)
  - `Info()`, `Debug()`, `Error()`

## Traffic Capture & Recording
- `internal/capture/` - Memory-safe HTTP capture: `Engine.CaptureRequest/CaptureResponse/CaptureEntry` clone bodies via `TeeReader` (always restoring the stream for downstream) and cap them at `maxBodySize`; streaming bodies capture metadata only. Recorders consume the captured types — they never touch live `http.Request`/`Response` bodies.
- `internal/redact/` - Single redaction policy for recordings (`Redactor`): credential-position headers (derived from `auth.KnownAuthHeaders` + Proxy-Authorization/Cookie/Set-Cookie) are replaced wholesale, and every secret value the process holds (proxy secret, placeholders, the secret registry's resolved cache via `ResolvedValues()`) is scrubbed from URLs/headers/bodies/error text. The `Redactor` zero value still enforces the positional policy, so an unredacted recorder is unconstructible.
- `internal/recorder/har.go` - HAR (HTTP Archive) recorder; entries are redacted as they are built (in-memory archive is already clean)
- `internal/recorder/jsonl.go` - JSONL (one transaction per line) recorder; entries redacted before writing, bodies scrubbed before JSON parsing
- `internal/recorder/multi.go` - Fan-out recorder that drives several recorders from one capture (each format redacts itself)

## Run Mode (child-process spawning)
- `internal/run/process.go` - `SpawnChild()`, `BuildProcessEnvironment()`, `ProcessResult.Wait` — start the child with proxy env vars and propagate its exit code
- `internal/run/env.go` - Builds the proxy environment (HTTP(S)_PROXY, CA path, placeholder/proxy secret) handed to the child
- `internal/run/banner.go` - Startup banner shown when launching a child

## Utilities
- `internal/shutdown/shutdown.go` - Graceful shutdown manager (register callbacks)
- `internal/defaults/` - Built-in default services and the env-var knobs that tune them
- `internal/util/proxy_url.go` - Proxy URL construction/parsing shared across modes
- `internal/errors/errors.go` - Common error types

## Tests
- `test/integration/auth_integration_test.go` - End-to-end auth tests
- `test/integration/mitm_integration_test.go` - MITM/TLS tests
- `internal/audit/logger_test.go` - Audit logger unit tests
- `cmd/chaperone/cmd/check_test.go` - Check command unit tests

## Key Workflows

### Request Flow (Inject Mode)
0. Client → CONNECT with `Proxy-Authorization` → `proxyAuthConnectHandler` → 407 without the per-run secret; on success stamps the tunnel authenticated
1. Client → CONNECT → `connectHandler` → decides MITM or passthrough
2. If MITM: `policyHandler` → check allowed methods/paths/body size
3. `recordRequestHandler` → snapshot the client-facing request for recording (BEFORE injection, so the recorded request never contains the real credential)
4. `authHandler` → fetch secret → apply strategy → **inject header**
5. Request sent to upstream
6. `recordResponseHandler` → HAR recording (all recorded data passes through the `internal/redact` redactor)
7. Response → Client

### Auth Injection Details (`authHandler` in handlers.go)
- Lookup service by host
- Fetch secret from registry (with provider like `env:`, `file:`, `keychain:`)
- Get auth strategy from registry (e.g., `bearer`, `header:x-api-key`)
- Call `strategy.Apply(ctx, request, secret)` → injects header
- **Logs:** `"injected credential"` with credential_ref, auth_strategy, path, host

### Dynamic Grant Flow (control plane + MCP)
1. Operator declares the grantable universe in config (`[[grantable]]`); daemon builds the `grant.Enforcer` and auto-starts the control socket when the universe is non-empty.
2. Claude Code spawns `chaperone mcp` (stdio); it dials the control socket as a `control.Client`.
3. Agent calls `chaperone_grant` → `control.API.Grant` → `enforcer.Authorize` (identity must match a pairing, scope must narrow within its bound) → on accept, `registry.Upsert(svc)` makes the host injection-eligible at once; on reject, the verbatim message returns as an MCP tool error (`IsError`).
4. A subsequent proxied request to that host now flows through the normal inject pipeline (above) — same single enforcer, no special path.
5. `chaperone_revoke` → `registry.Unregister(host)` → the host stops being injected (subsequent requests fall back to transparent tunnel).
- Every grant/revoke/reject is audited by reference (`grant_applied`/`grant_revoked`/`grant_rejected`); a secret value is never resolved or recorded here.
- E2E coverage: `test/integration/grant_injection_integration_test.go` proves the four behaviors on real HTTP/TLS (in-scope injected, out-of-scope rejected before injection, off-universe refused, revoke removes injection) plus that no secret crosses the MCP/audit boundary.

### Header Capitalization Handling (headers_util.go)
- Client may send `authorization`, `Authorization`, `AUTHORIZATION`
- Go HTTP canonicalizes to `Authorization`
- `setHeaderPreservingCapitalization()` detects existing header, logs **WARNING**
- Replaces value while preserving client's capitalization

### Examine Mode Flow
1. Client → CONNECT → `examine.ConnectHandler` → **always MITM** (no filtering)
2. `examine.RequestHandler` → log request (headers, optional: params, cookies, body)
3. Request sent to upstream (unmodified)
4. `examine.ResponseHandler` → log response (status, headers, optional: cookies, body)
5. Response → Client

## Config File Format (chaperone.toml)
```toml
[server]
address = "127.0.0.1"
port = 4010
# Optional: pin outbound trust for MITM'd upstreams to ONLY these PEM roots
# (unset = system root store; upstream cert verification itself is always on)
# upstream_ca_file = "/path/to/upstream-roots.pem"

[logging]
level = "info"  # debug, info, warn, error

# Audit logging (optional)
[audit]
enabled = true
path = "/var/log/chaperone/audit.log"  # or "stdout"

[[services]]
name = "openai"
host_pattern = "api.openai.com"
auth_strategy = "bearer"  # or "header:X-API-Key"
credential_ref = "env:OPENAI_API_KEY"  # or "file:/path" or "keychain:service/account"

# Optional: Placeholder token for process authentication
placeholder = "chap_openai_xxxxxxxx"  # App uses this, Chaperone swaps for real key

[services.policy]
allowed_methods = ["GET", "POST"]
# Exact path or "<prefix>/*" (subtree, any depth) — the one vocabulary shared
# with drop paths and grant scopes. Request paths are normalized before
# comparison and matched case-insensitively; non-canonical or glob patterns
# are rejected at startup.
allowed_paths = ["/v1/*"]
max_body_bytes = 1048576
```

## CLI Usage
```bash
# Run mode: Start proxy and spawn child process with injected auth
chaperone run openai                                    # Uses config [services.openai.run]
chaperone run openai -- python script.py                # Override config with CLI command
chaperone run zai -- claude --dangerously-skip-permissions  # Complex command
chaperone run -c custom.toml myservice -- bash          # Custom config + CLI command

# Inject mode (default config: ~/.config/chaperone/chaperone.toml)
chaperone inject                    # All services
chaperone inject openai             # Specific service
chaperone inject -c custom.toml     # Custom config

# Examine mode (auth discovery)
chaperone examine                   # Basic (just headers)
chaperone examine -p --show-cookies # Show params & cookies
chaperone examine -b -r             # Show bodies & responses
chaperone examine -o results.txt    # Save to file (enables all flags)

# Security check
chaperone check                     # Show security posture
chaperone check -c custom.toml      # Check with specific config
```

## Recent Features
- **CLI command override in run mode**: Commands can be defined in config file OR overridden via CLI with `-- command args` syntax
- **Run mode**: `chaperone run` starts proxy + spawns child process with injected auth
- **Security check**: `chaperone check` command to assess security posture (cmd/chaperone/cmd/check.go)
- **Audit logging**: JSON audit trail for credential injections (internal/audit/)
- **Placeholder authentication**: Optional placeholder token verification (Layer 2 security)
- **Examine mode flags**: `-b` (body), `-p` (params), `--show-cookies`, `-r` (response), `-o` (output file)
- **Header capitalization detection**: Warns when client sends header we're trying to inject
- **Glob pattern exclusions**: Examine mode filters `x-stainless-*` headers via glob
- **Improved logging**: DEBUG-level CONNECT/TLS messages, structured "injected credential" message

## Development Notes

### Dependencies
- `elazarl/goproxy` - MITM proxy foundation
- `modelcontextprotocol/go-sdk` - MCP server/protocol (`chaperone mcp` grant tools)
- `spf13/cobra` - CLI framework
- `BurntSushi/toml` - Configuration parsing
- `google/uuid` - Request ID generation
- `stretchr/testify` - Testing assertions

Go version: see `go.mod` (currently `go 1.25.4`).

### Key Architectural Patterns

**Error Handling:** Uses custom error types from `internal/errors/` to maintain error context across package boundaries. All public functions should return errors explicitly; never panic.

**Observability:**
- Structured logging via `internal/log/logger.go` with automatic request ID injection
- Secret redaction in logs (checks: authorization, secret, password, token, api_key)
- Request correlation via X-Request-ID headers
- Audit logging for security events via `internal/audit/logger.go` (JSON format)

**Configuration Management:**
- Default paths: `-c` flag → `~/.config/chaperone/chaperone.toml`. Config is NEVER read from the CWD (a hostile repo could point a real credential at an attacker host); a project-local config requires explicit `-c ./chaperone.toml`. `getConfigPath` (cmd/chaperone/cmd/root.go) is the single trust boundary — all modes (inject/run/examine/check) resolve through it
- File trust gate: `config.Load` rejects (loud error, no fallback) a config that is group/world-writable, owned by a different uid, or not a regular file — BEFORE any `credential_ref` is parsed. The check fstat's the open handle (no check-then-use race) and is the shared `internal/filetrust` decision (`configTrust` with the `NoUntrustedWrites` bar) applied only in `Load`, so every mode is covered by construction
- TOML format with validation
- Service registry preloaded on startup
- All secrets validated at startup (preloading catches config errors early)

**Certificate Management:**
- CA cert stored at `~/.config/chaperone/ca-cert.pem` (10-year validity)
- Per-hostname certificates cached in memory
- Certificates support both DNS names and IP addresses (SAN)

### Testing Philosophy

**Integration Tests:** Located in `test/integration/`, use **real HTTP clients and actual TLS handshakes**. They cannot be satisfied by mocks - the entire MITM pipeline must work end-to-end. These tests serve as completion gates for features.

**Unit Tests:** Test individual functions and modules. Use `net/http/httptest` for server mocking only where appropriate.

**Running Tests:**
- `make test` - Full suite with `-v` (verbose)
- `make test-race` - Detects race conditions
- `go test -short ./...` - Skips integration tests for fast iteration

### Code Quality Standards

- **Linting:** golangci-lint with 8 checkers (errcheck, govet, ineffassign, staticcheck, unused, misspell, gosec)
- **Security:** gosec enabled with some G-rules excluded (file reading, permissions checks allowed in config validation)
- **Formatting:** gofmt (no custom style)

## Package Organization

The codebase is organized by responsibility, not by layer:

| Package | Responsibility |
|---------|-----------------|
| `cmd/chaperone/cmd/` | CLI commands (inject, run, examine, check, mcp) |
| `internal/proxy/` | Core proxy server and request handlers |
| `internal/auth/` | Authentication strategies (bearer, custom header) |
| `internal/secrets/` | Secret providers (env, file, keychain) |
| `internal/service/` | Service registry, policy, host matching |
| `internal/config/` | Configuration parsing and validation (incl. `GrantableConfig`) |
| `internal/filetrust/` | Shared file-trust decision (mode/owner/symlink-target) for config and secret files |
| `internal/grant/` | Grant enforcer — single authority for what is grantable |
| `internal/control/` | Daemon control plane (grant/revoke/list over unix socket) |
| `internal/mcpgrants/` | stdio MCP server — agent-facing grant tools (thin control-plane client) |
| `internal/orchestrate/` | Shared daemon assembly (registries, proxy, control plane) for inject/run |
| `internal/mitm/` | MITM certificate generation and caching |
| `internal/audit/` | Security event logging (JSON format) |
| `internal/examine/` | Auth discovery mode (passthrough logging) |
| `internal/init/` | Config wizard with auto-detection |
| `internal/log/` | Structured logging with redaction |
| `internal/recorder/` | Traffic recording (HAR, JSONL, multi fan-out); redacted at record time |
| `internal/redact/` | Recording redaction policy (credential positions + known secret values) |
| `internal/capture/` | Memory-safe HTTP request/response body capture for recording |
| `internal/run/` | Run mode: spawn child process with injected proxy environment |
| `internal/defaults/` | Built-in default services + env-var tuning |
| `internal/util/` | Shared proxy-URL helpers |
| `internal/shutdown/` | Graceful shutdown management |
| `internal/errors/` | Custom error types |

## Key Implementation Details

### Header Capitalization Handling (`internal/auth/headers_util.go`)

HTTP headers are case-insensitive but Go canonicalizes them. When injecting auth headers:
- `setHeaderPreservingCapitalization()` finds existing header (any case)
- Replaces value while preserving client's capitalization
- Logs WARNING if header already exists

### Policy Enforcement Pipeline (handlers split across `internal/proxy/*_handler.go`)

Requests flow through handlers in order:
0. `proxyAuthConnectHandler`/`proxyAuthHandler` (`proxy_auth.go`) - Proxy access gate: 407 without the per-run proxy secret, before anything else runs
1. `connectHandler` (`connect_handler.go`) - Decide MITM vs transparent tunnel
2. `policyHandler` (`policy_handler.go`) - Check methods/paths/body size (fail fast); `dropHandler`/`stripHandler` apply drop/strip policy
3. `securityStripAuthHandler` (`auth_handler.go`) - Strip client-supplied auth so it can't leak past the proxy
4. `recordRequestHandler` (`recording_handler.go`) - Snapshot the client-facing (post-strip, pre-injection) request for recording
5. `authHandler` (`auth_handler.go`) - Fetch secret, inject credential
6. Forward to upstream
7. `recordResponseHandler` - Response capture
8. Return to client

**Why record before injecting?** The durable artifact must never see the real credential; the recorder's redactor (`internal/redact`) is the backstop, the ordering is the guarantee.

**Why fail-fast?** Policy rejection happens before credential injection for security.

### Service Lookup Flow

- Host from CONNECT request matched against service patterns
- If match → lookup service config → fetch secret → apply strategy
- If no match → transparent tunnel (no MITM)
- Pattern matching is first-match-wins

### Config Validation Strategy

All configuration is validated on startup via `config.Validate()`:
- All service host patterns are required
- All credential refs are validated
- Secret preloading catches missing env vars immediately
- Invalid patterns/strategies fail fast

## Common Refactoring Risks

**High Risk - Breaks Multiple Components:**
- Changes to `internal/service/registry.go` interface affect proxy handlers, config parsing, CLI commands
- Changes to `internal/auth/strategy.go` interface affect all auth implementations and proxy handlers
- Changes to error types in `internal/errors/` affect error handling across all packages

**Medium Risk - Localized Impact:**
- Adding fields to `Service` struct requires config parsing updates
- Changing logging format breaks test assertions on log output

**Low Risk - Isolated:**
- Adding new secret provider (implement interface, register in registry)
- Adding new auth strategy (implement interface, register in registry)
- Adding new CLI command (follows existing cobra patterns)

## Code Review Focus Areas

When reviewing changes:
1. **Error handling:** Are errors returned/logged with context?
2. **Secrets:** Are credentials ever logged/printed?
3. **Concurrency:** Use race detector - `make test-race`
4. **Config validation:** Does startup catch misconfigurations?
5. **Test coverage:** Are critical paths tested? (Especially auth injection)

## Verification Before Committing

```bash
make fmt                           # Auto-format
make lint                          # Static analysis
make test                          # All tests
make build                         # Compilation check
```

**For security-sensitive changes:**
```bash
make test-race                     # Check for races
go test ./... -coverprofile=coverage.out
go tool cover -html=coverage.out   # Check coverage in auth/secrets/audit paths
```
