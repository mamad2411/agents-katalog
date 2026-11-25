# MCP Tooling & Integrations

## Purpose
Develop and integrate Model Context Protocol servers and client toolkits: scaffold spec-compliant servers, implement stdio and Streamable HTTP transports, build client session handling with version negotiation, and prove conformance with the protocol test battery.

## Use when
- Scaffolding a new MCP server (TypeScript, Python, or Rust SDK) with tools, resources, and prompts.
- Implementing or switching transports: local stdio vs remote Streamable HTTP with session management.
- Building client-side integration: session lifecycle, capability negotiation, sampling, and elicitation flows.
- Running protocol conformance, backwards-compatibility, or cross-client interop tests for an MCP release.

## Do not use when
- Defining the domain tool surface and scopes of one product integration (use `mcp-integration`).
- Designing a non-MCP plugin sandbox or extension marketplace (use `plugin-architecture`).
- Debugging a single flaky Playwright flow unrelated to MCP transport (use `playwright-ui`).

## Required context
- MCP protocol version target (e.g., `2025-06-18`) and SDK versions (e.g., TypeScript SDK 1.12.0, Python SDK 1.9.0).
- Transport choice and constraints: stdio subprocess budget, or HTTP endpoint with session store (e.g., Redis) and TLS termination.
- Client matrix under test (e.g., Harbor Desktop 3.1, VS Code extension 0.24, CI runner 0.8) with capability sets.
- Conformance baseline: protocol test battery version and currently known failures.

## Procedure
1. **Scaffold from the SDK**: Generate the server with the official SDK (`npx @modelcontextprotocol/create-server harbor-notes`), pin dependency versions in the lockfile, and assert `npm run conformance:local` passes before adding domain tools.
2. **Implement transports deliberately**: Ship stdio for local use (newline-delimited JSON-RPC, 10 MB message cap, clean SIGTERM shutdown within 2 s); add Streamable HTTP for remote use with resumable session IDs stored server-side and a 60 s heartbeat, verifying reconnect resumes the same session.
3. **Negotiate versions and capabilities**: On `initialize`, advertise protocol version and capability flags; reject mismatched majors with error `-32099` and a human-readable upgrade hint; log negotiated versions per session for interop forensics.
4. **Build client session handling**: Implement reconnect with exponential backoff (200 ms base, 5 s cap, 8 attempts), request timeouts at 30 s with typed `Timeout` errors, and progress-token support for long tools (progress every 5 s or the client may cancel).
5. **Run conformance and interop**: Execute the protocol battery (214 cases in v3.2: framing, batching, cancellation, error shapes) against both transports; then run the 3-client interop matrix and record per-client pass rates with failure transcripts.
6. **Publish and verify**: Version the server package (`harbor-notes-mcp 2.1.0`), publish the changelog with protocol/SDK pins, complete `templates/mcp-tooling-spec.md`, and run `scripts/verify.sh` to confirm artifact completeness.

## Decision rules
- **SDK-first, no hand-rolled framing**: Custom JSON-RPC parsers are forbidden; all wire code goes through the official SDK.
- **Both transports tested**: A server advertising stdio and HTTP proves conformance on both; untested transports are removed from the capability advertisement.
- **Timeouts and heartbeats are mandatory**: Any request without a 30 s timeout or any HTTP session without a 60 s heartbeat fails review.
- **Breaking protocol changes bump major**: SDK or protocol upgrades that alter the wire format require a major server release with migration notes.
- **Interop failures block release**: A conformance-green server that fails against a declared client still blocks until fixed or the client is de-listed.

## Evidence required
- Conformance battery report: 214 cases, per-transport results, zero unexplained failures.
- 3-client interop matrix with pass rates and failure transcripts.
- Session-resume drill log: kill and reconnect mid-tool-call, asserting exactly-once visible semantics.
- Published package version with protocol/SDK pins and changelog.
- Completed `templates/mcp-tooling-spec.md` with transports and verdicts.
- Passing execution log from `scripts/verify.sh`.

## Output contract
- MCP server/client toolkit implementation with pinned SDK and dual-transport support.
- Tooling specification with transport contracts, negotiation policy, and interop verdicts.
- Conformance and interop evidence archived with the release under test.

## Stop conditions
- Conformance battery green on all advertised transports and interop matrix green on declared clients.
- Session resume, timeout, and heartbeat behaviors proven with logs.
- Token budget exhausted.
- Blocked on external dependency.

## Escalation rules
- Escalate to SDK maintainers (upstream issue with minimal repro) when conformance failures trace to SDK framing bugs rather than server code.
- Escalate to client owners when interop fails on a declared client due to client-side capability gaps; de-list only with product sign-off.
- Escalate immediately on authentication bypass, session fixation, or cross-tenant session leakage in the transport layer.
