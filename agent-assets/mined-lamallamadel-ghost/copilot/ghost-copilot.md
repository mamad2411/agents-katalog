# Ghost CLI – Copilot Instructions

## Commands

### Root (CLI — `atlasia-ghost`)
```bash
npm install           # Install root dependencies
npm start             # Run the CLI: node ghost.js
npm test              # Run test.js, which auto-discovers and runs all test/*.test.js
node test/<file>.test.js   # Run a single integration test
node scripts/test/smoke-help.mjs   # Smoke test: help output
npm run test:all      # All smoke tests combined
```

### Desktop Electron App (`desktop/`)
> Dev tooling only — not published to NPM.
```bash
cd desktop && npm install
npm run desktop:dev   # Electron + Vite HMR on port 5173
npm run build         # TypeScript compile + Vite production build
npm run lint          # ESLint on all TS/TSX files
npm run check         # TypeScript type-check only (no emit)
npm test              # Vitest unit tests
npm run test:e2e      # Playwright E2E tests
```

## Architecture

Ghost CLI is a **pure gateway/orchestration layer** — all domain logic lives in extensions. The CLI itself (`ghost.js`) only parses args, initializes infrastructure, and routes commands. Direct `fs` operations in `ghost.js` are documented violations awaiting refactoring.

### Command flow
```
CLI args → GatewayLauncher (ghost.js)
         → Gateway (core/gateway.js) — extension registry & routing
         → IOPipeline (core/pipeline/) — 4-stage security enforcement
             INTERCEPT → AUTH → AUDIT → EXECUTE
         → ExtensionProcess (core/runtime.js) — subprocess over JSON-RPC stdio
```

The pipeline is **fail-closed**: any stage failure denies execution.

- **`intercept.js`** — Parses raw JSON-RPC into a validated Intent object
- **`auth.js`** — Capability-based authorization + rate limiting (token bucket)
- **`audit.js`** — NIST SI-10 compliant audit logging of every event
- **`execute.js`** — Runs extension subprocess; wraps with CircuitBreaker + TimeoutManager

### Core systems
- **`core/gateway.js`** — Extension discovery, registration, and routing
- **`core/extension-loader.js`** — Filesystem discovery + manifest validation (fail-closed); calls `DependencyResolver` to determine load order
- **`core/runtime.js`** — `ExtensionProcess` subprocess lifecycle: state machine `STOPPED → STARTING → RUNNING → STOPPING`, heartbeat monitoring, exponential backoff restarts
- **`core/dependency-resolver.js`** — Kahn's algorithm (topological sort) + Tarjan's SCC (cycle detection) + semver constraint validation for extension ordering
- **`core/qos/`** — Rate limiting: `token-bucket.js` (CIR/BC/BE), `advanced-rate-limiter.js`, `enhanced-circuit-breaker.js`, `fair-queuing.js`
- **`core/validators/`** — Input sanitization: path, command, network, and entropy validators
- **`core/mesh/`** — Multi-agent mesh network: `AgentMeshNetwork`, `AgentDiscoveryService`, `CRDTStateSync`, `WorkflowOrchestrator`
- **`core/analytics/`** — `AnalyticsPlatform` with WebSocket server on port 9877 (desktop connects here)
- **`core/hot-reload.js`** — File watching, graceful shutdown, state `serialize`/`deserialize` hooks, request queuing, rollback on failure

### Extension system
Extensions are Node.js subprocesses; communication is **JSON-RPC over stdio**.

Discovery order (first match on ID collision wins):
1. `~/.ghost/extensions/` — user-installed extensions
2. `extensions/` — bundled extensions (e.g. `ghost-git-extension`)

Each extension requires a `manifest.json` validated against `core/manifest-schema.json`:
```json
{
  "id": "my-extension",
  "name": "My Extension",
  "version": "1.0.0",
  "main": "index.js",
  "commands": ["cmd1", "cmd2"],
  "capabilities": {
    "filesystem": { "read": ["**/*"], "write": ["**/.git/**"] },
    "network": {
      "allowlist": ["https://api.example.com"],
      "rateLimit": { "cir": 100000, "bc": 500000, "be": 1000000 }
    },
    "git": { "read": true, "write": true },
    "hooks": ["pre-commit", "commit-msg"]
  },
  "permissions": ["filesystem:read", "network:https", "git:read"]
}
```
`extensionDependencies` can declare version-constrained deps resolved at load time.

### Desktop app
React 18 SPA (Zustand, React Router, TailwindCSS) in Electron. Connects to the analytics WebSocket on port 9877 for real-time metrics. References the local CLI as `"atlasia-ghost": "file:.."`.

## Key Conventions

### Module system
- **Root + `core/`**: CommonJS (`require`/`module.exports`), no transpilation
- **Desktop**: TypeScript strict mode, ESM-style imports compiled by Vite
- **`packages/extension-sdk/`**: CommonJS JS files with alongside `.d.ts` TypeScript definitions

### Security / NIST SI-10
All input entering the pipeline must be sanitized by a validator in `core/validators/`. Every security-relevant event must be logged via `AuditLogger`. The pipeline is fail-closed — when in doubt, deny and log.

### Extension SDK (`@ghost/extension-sdk`)
For third-party extensions. Key classes: `ExtensionSDK` (high-level API: `requestFileRead`, `requestNetworkCall`, `requestGitExec`), `IntentBuilder`, `RPCClient`. See `docs/extension-api.md` for the full I/O intent schema.

### Testing
- Root tests use Node's built-in `assert` module, no test framework
- `test.js` is a custom runner that auto-discovers all `test/**/*.test.js` files
- Desktop uses Vitest (unit) and Playwright (E2E in `desktop/e2e/`)
- **Known pre-existing failure**: `test/audit-nist-compliance.test.js` line 122 — entropy validator does not detect `AKIA1234567890ABCDEF` as a secret (`core/validators/entropy-validator.js`)

### CLI output
Use ANSI escape codes for color output in the root/core layer (no logging library). Keep `ghost.js` as pure orchestration — domain logic belongs in extensions.

### Extension scaffolding
```bash
ghost extension init <name>      # Interactive template wizard
ghost extension validate [path]  # Validate manifest + permissions
ghost gateway reload <id>        # Hot-reload a running extension
```
