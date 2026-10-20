# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Root (CLI)
```bash
npm install          # Install root dependencies
npm test             # Run test.js smoke tests + all integration tests in test/
npm start            # Run the CLI (node ghost.js)
node test/<file>.test.js               # Run a single test
node test/gateway/<file>.test.js       # Tests are also in subdirectories
npm run test:all     # All smoke tests (help, default, safe-mode, pack-contents)
```

### Desktop App
```bash
cd desktop && npm install
npm run desktop:dev  # Electron + Vite with HMR (port 5173)
npm run build        # TypeScript compile + Vite production build
npm run lint         # ESLint on all TS/TSX files
npm run check        # TypeScript type-check only (no emit)
npm test             # Vitest unit tests
npm run test:e2e     # Playwright E2E tests
```

## Known Test Failure (Pre-existing)

`test/audit-nist-compliance.test.js` line 122 fails — the entropy validator does not detect `AKIA1234567890ABCDEF` as a secret. This predates any recent work and is in `core/validators/entropy-validator.js`.

## Architecture

**Ghost CLI** (`atlasia-ghost`) is an extensible, gateway-based Git CLI with AI-powered operations (Groq/Anthropic/Gemini). The core design principle: the CLI is a pure orchestration layer — all commands are routed through extensions via a structured JSON-RPC pipeline.

### Entry Point
`ghost.js` — `GatewayLauncher` class. Parses CLI args, initializes infrastructure, routes to extensions. Contains documented architecture violations (direct `fs` operations) awaiting refactoring.

### Pipeline (`core/pipeline/`)
Every command flows through 4 stages, **fail-closed** (any failure denies execution):
```
CLI args → GatewayLauncher (ghost.js)
         → Gateway (core/gateway.js) — extension registry & routing
         → IOPipeline (core/pipeline/) — 4-stage security enforcement
             INTERCEPT → AUTH → AUDIT → EXECUTE
         → ExtensionProcess (core/runtime.js) — subprocess over JSON-RPC stdio
```
- `intercept.js` — Parse/validate raw JSON-RPC → Intent
- `auth.js` — Capability-based authorization + rate limiting
- `audit.js` — NIST-compliant audit logging
- `execute.js` — Execution + CircuitBreaker + TimeoutManager

### Core Infrastructure (`core/`)
- `gateway.js` — Extension registry: discovers, registers, and routes to extensions
- `command-registry.js` — `CommandRegistry`: deterministic command routing built from extension manifests. Replaces ghost.js if/else dispatch. Supports namespaced invocation (`ghost policy:list`), two-word sugar (`ghost policy list`), and legacy flat aliases. Tie-breaks by `command.priority` (default 0) then lexicographic extension ID. Optional `extensions.lock.json` (or `config/extensions.lock.json`) pins command owners via `commandOwners`.
- `extension-loader.js` — Filesystem discovery + manifest validation (fail-closed); uses `DependencyResolver` to determine load order
- `runtime.js` — `ExtensionProcess`: subprocess lifecycle over JSON-RPC with state machine (`STOPPED → STARTING → RUNNING → STOPPING`), heartbeat monitoring, exponential backoff restarts
- `dependency-resolver.js` — Topological sort (Kahn's algorithm) + cycle detection (Tarjan's SCC) + semver version constraint validation for extension load ordering
- `marketplace.js` — `MarketplaceService`: fetch/search/install/uninstall extensions from registry (`GHOST_MARKETPLACE_URL`); verified via RSA public key; caches to `~/.ghost/marketplace-cache`. Full backend in `marketplace-backend/` (Express server, SQLite, health scoring, security scanning).
- `telemetry.js` — Metrics; wires OTLP/Prometheus exporters (`core/exporters/`)
- `qos/` — Rate limiting suite: `token-bucket.js` (CIR/BC), `advanced-rate-limiter.js`, `enhanced-circuit-breaker.js`, `fair-queuing.js`, `global-rate-limiter.js`
- `validators/` — Input validators: `path-validator.js`, `command-validator.js`, `network-validator.js`, `entropy-validator.js`
- `hot-reload.js` + `dev-mode.js` — File watching with debounce, graceful shutdown, state preservation (`serialize`/`deserialize` hooks), request queuing, rollback on failure
- `analytics/` — `AnalyticsPlatform` with WebSocket server on port 9877; desktop connects here for real-time metrics
- `webhooks/` — Webhook subsystem: `WebhookController`, `WebhookEventStore`, `WebhookRouter`, `WebhookTransformPipeline`, `WebhookDeliveryQueue`
- `mesh/` — Multi-agent mesh network: `AgentMeshNetwork`, `AgentDiscoveryService`, `CRDTStateSync`, `WorkflowOrchestrator`
- Security: `security-hardening.js`, `security-policy-engine.js`, `intrusion-detection.js`, `code-signing.js`, `secrets-manager.js`, `sandbox.js`

### Extensions
Extensions are Node.js subprocesses communicating via JSON-RPC over stdio. Extension discovery order:
1. `~/.ghost/extensions/` (user extensions, take precedence on ID collision)
2. `extensions/` (24 bundled extensions; key ones: `ghost-git-extension`, `ghost-agent-extension`, `ghost-ai-extension`, `ghost-bridge-extension`, `ghost-policy-extension`, `ghost-security-extension`, `ghost-marketplace-extension`)

Each extension has a `manifest.json` validated against `core/manifest-schema.json`:
```json
{
  "id": "my-extension",
  "name": "My Extension",
  "version": "1.0.0",
  "main": "index.js",
  "commands": ["cmd1", "cmd2"],
  "capabilities": {
    "filesystem": { "read": ["**/*"], "write": ["**/.git/**"] },
    "network": { "allowlist": ["https://api.example.com"] },
    "git": { "read": true, "write": true },
    "hooks": ["pre-commit", "commit-msg"]
  },
  "permissions": ["filesystem:read", "network:https", "git:read"]
}
```
`extensionDependencies` can declare version-constrained deps resolved at load time.

Scaffold: `ghost extension init <name>` | Validate: `ghost extension validate [path]` | Hot-reload: `ghost gateway reload <id>` | Dev mode: `ghost dev enable|disable|status`

### Extension SDK (`packages/extension-sdk/` → `@ghost/extension-sdk`)
For third-party extension authors. Key classes: `ExtensionSDK` (high-level API: `requestFileRead`, `requestNetworkCall`, `requestGitExec`), `IntentBuilder`, `RPCClient`. Full TypeScript definitions included. Documentation in `docs/`.

### Desktop App (`desktop/`)
Electron monitoring console — **not published to NPM, dev tooling only**. React 18 SPA, Zustand state, React Router, Vite build. Connects to the analytics WebSocket (port 9877) for real-time metrics. References the local CLI via `"atlasia-ghost": "file:.."`.

## Code Style
- **Root/Core:** CommonJS modules (`require`/`module.exports`), ANSI escape codes for color output (no logging library), minimal comments
- **Desktop:** ESLint flat config, strict TypeScript, functional React components with hooks
- **SDK:** CommonJS with TypeScript `.d.ts` definitions alongside JS files

## Testing Conventions
- Root tests use Node's built-in `assert` module — no test framework
- `test.js` is a custom runner that auto-discovers all `test/**/*.test.js` files (including subdirectories: `test/gateway/`, `test/extensions/`, `test/e2e/`)
- Desktop uses Vitest (unit) and Playwright (E2E in `desktop/e2e/`)

## Critical Pitfalls
- **Manifest write patterns** must use `**/` prefix (e.g. `**/package.json`, `**/.git/**`) — relative patterns like `package.json` won't match absolute paths via `GlobMatcher.match()`
- **Test credential patterns** must be scanner-safe fakes to avoid GitHub push protection blocks: use `rk_test_FAKEKEYFORTESTING...` (not `rk_live_`), `SKxxxxxxxx...` (not hex-looking SIDs)
- **`git rev-parse` output** has trailing `\n` — always `.trim()` the result
- **Pipeline is fail-closed** — all input must be sanitized by a validator in `core/validators/`; every security-relevant event must be logged via `AuditLogger`; when in doubt, deny and log
