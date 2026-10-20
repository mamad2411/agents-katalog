# 👻 Ghost CLI v1.0.0 - Context & Instructions

Ghost CLI is an extensible Git assistant powered by a JSON-RPC gateway architecture. It acts as a **pure gateway launcher**, orchestrating extensions that provide AI-powered Git operations, security scanning, and more. This v1.0.0 release marks the transition from a simple Git utility to a robust, secure gateway-based platform.

## 🏗️ Architecture & Core Components

- **Gateway Launcher (`ghost.js`):** The entry point that initializes infrastructure (Gateway, Runtime, Pipeline, Audit) and routes CLI commands.
- **Core Engine (`core/`):**
    - `gateway.js`: Extension discovery and metadata management.
    - `runtime.js`: Manages extension lifecycles (isolation, heartbeat, auto-restart).
    - `pipeline/`: The security enforcement layer (Intercept → Auth → Audit → Execute).
    - `sandbox.js`: Security isolation for extension execution.
    - `mesh/`: Advanced agent-to-agent networking and distributed telemetry.
- **Extensions:**
    - `extensions/ghost-git-extension/`: The primary bundled extension for AI commits, audits, and versioning.
    - `packages/extension-sdk/`: SDK for building third-party extensions.
- **Desktop Console (`desktop/`):** An Electron + React application for real-time monitoring and telemetry visualization.

## 🚀 Key Commands

### Development & Maintenance
- `npm start`: Launch the Ghost CLI gateway.
- `npm test`: Run the full test suite (executes `test.js` which discovers all `*.test.js` files).
- `node scripts/benchmark-hotspots.js`: Run performance benchmarks.
- `node scripts/profile-load-test.js both`: Perform CPU and heap profiling.

### Extension Management
- `ghost extension list`: List installed extensions.
- `ghost extension init <name>`: Scaffold a new extension.
- `ghost extension validate [path]`: Validate manifest and permissions.
- `ghost extension install <path>`: Install an extension locally.

### Gateway & Telemetry
- `ghost gateway status`: Show gateway health and rate limit states.
- `ghost console start`: Start the telemetry web server (default port 9876).
- `ghost audit-log view`: View the immutable audit trail.

## 🛠️ Development Conventions

1.  **Zero Business Logic in Gateway:** The `GatewayLauncher` should only handle orchestration. Domain-specific logic (Git, AI, Filesystem) belongs in **extensions**.
2.  **JSON-RPC Communication:** All interactions between the gateway and extensions must use the JSON-RPC protocol over stdin/stdout or IPC.
3.  **Capability-Based Security:** Extensions must declare required permissions (filesystem, network, git) in their `manifest.json`. The `IOPipeline` enforces these strictly.
4.  **NIST SI-10 Compliance:** All input and output through the gateway must be sanitized and audited.
5.  **Performance First:** Avoid O(n) scans; use hash-based lookups and memoization for validation results.
6.  **Immutable Audit Trail:** All security-relevant events must be logged to the audit log via the `AuditLogger`.

## 🧪 Testing Strategy

- **Unit/Integration Tests:** Located in `test/`, following the `*.test.js` naming convention.
- **Custom Runner:** `test.js` is the master runner that executes all discovered tests.
- **E2E Tests:** Located in `desktop/e2e/` (using Playwright) for the console UI.
- **Load Tests:** Located in `test/gateway/pipeline-load.test.js` to verify performance under pressure.

## 📂 Project Structure Highlights

- `core/`: Infrastructure, security pipeline, and gateway logic.
- `extensions/`: Bundled extensions provided with the CLI.
- `packages/`: Workspace packages, including the Extension SDK.
- `desktop/`: Electron/React source code for the Ghost Console.
- `docs/`: Comprehensive guides for developers and users.
- `scripts/`: Operational scripts for profiling, benchmarking, and installation.
