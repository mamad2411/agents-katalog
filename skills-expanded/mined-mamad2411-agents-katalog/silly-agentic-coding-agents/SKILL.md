# Rules of Engagement: AI Agents Directory

Welcome to the agentic workspace. This document serves as the directory and coordinate registry for all specialized AI agents. Every agent must consult this file before performing actions to prevent boundary conflicts, preserve architectural hygiene, and maintain clean separation of concerns.

---

## 📋 Core Rules of Engagement

1. **Strict Scope Separation**: Respect each agent's domain. Never edit files or configurations owned by another agent without explicit hand-off or approval. General source code files (e.g., TS, JS, Java, Python, Go) are shared; refactoring (Steward) and code cleanup (Gardener) may edit them to improve health, provided they preserve behavior and respect the negative constraints in their respective boundaries (e.g., not modifying styles, tests, or build files).
2. **Atomic Contributions**: Keep pull requests and edits small (ideally under 50 lines). Solve one targeted improvement at a time.
3. **Mandatory Local Verification (FullThrottle)**: Every agent must pass the Pre-PR Verification Gate (test → rebase → retry loop) before submitting any PR. See the common block `pr_gate.md` for the full protocol.
4. **Zero-Trust Security**: Never hardcode credentials, private tokens, or secrets. Utilize designated vault, Secret, or credential bindings.
5. **Continuous Learning**: Document only *critical*, non-trivial environment and syntax learnings in your individual journal located at `.jules/<agent-name>.md`. Always append new entries to the journal; never overwrite or delete entries. If a previous learning becomes obsolete due to recent changes, mark it as `[OBSOLETE]` or `[DEPRECATED]` with an explanatory note rather than deleting it.
6. **Prompt Maintenance**: Never edit compiled agent files inside [agents/](./agents) or [agents_bulk/](./agents_bulk) directly. Modify their templates and common blocks under `agent_sources/` and run `python3 build.py`. Ensure that `python3 build.py --check` passes before submitting edits.


---

## 🗂️ Agent Directory

Each agent is available in two execution formats:
- **Standard (Daily)**: Autonomous routine scan & small improvement ([agents/](./agents))
- **Bulk Refactoring**: Parameterized multi-file deep refactoring task ([agents_bulk/](./agents_bulk))

### 1. Architecture & Code Quality
* **Architect** 🧭 ([standard](./agents/architect.md) | [bulk](./agents_bulk/architect.md))  
  Responsible for architectural consistency, module boundaries, and high-level project structure.
* **Steward** 🧹 ([standard](./agents/steward.md) | [bulk](./agents_bulk/steward.md))  
  Focuses on code quality, maintainability, readability, and refactoring away technical debt.
* **Gardener** 🌱 ([standard](./agents/gardener.md) | [bulk](./agents_bulk/gardener.md))  
  Handles general hygiene, pruning dead code, cleaning imports, and removing technical clutter.
* **Curator** 📦 ([standard](./agents/curator.md) | [bulk](./agents_bulk/curator.md))  
  Manages packages and third-party dependencies, version updates, and lockfile hygiene.
* **Prompter** ✍️ ([standard](./agents/prompter.md) | [bulk](./agents_bulk/prompter.md))  
  Refines agent persona templates, optimizes system prompt token payloads, and ensures safety boundaries.


### 2. User Experience & Design
* **Navigator** 🧭 ([standard](./agents/navigator.md) | [bulk](./agents_bulk/navigator.md))  
  Focused on user flows, page routing/transitions, and navigation correctness.
* **Palette** 🎨 ([standard](./agents/palette.md) | [bulk](./agents_bulk/palette.md))  
  Owns styling (CSS), UI animations, accessible layouts, and visual delight.
* **Quill** ✒️ ([standard](./agents/quill.md) | [bulk](./agents_bulk/quill.md))  
  Responsible for copywriting, user-facing text, notifications, and copy consistency.

### 3. Testing, Security & Resilience
* **Inspector** 🧪 ([standard](./agents/inspector.md) | [bulk](./agents_bulk/inspector.md))  
  Improves code confidence by adding unit, integration, and end-to-end tests.
* **Sentinel** 🛡️ ([standard](./agents/sentinel.md) | [bulk](./agents_bulk/sentinel.md))  
  Audits configurations, manages security scanning, and secures potential vulnerabilities.
* **Sledge** 🔨 ([standard](./agents/sledge.md) | [bulk](./agents_bulk/sledge.md))  
  Executes load tests, resilience validation, and highlights system failure boundaries.
* **Bolt** ⚡ ([standard](./agents/bolt.md) | [bulk](./agents_bulk/bolt.md))  
  Implements execution micro-optimizations, caching, and performance tuning.

### 4. Kubernetes & Infrastructure Configs
* **Operator** ⚙️ ([standard](./agents/operator.md) | [bulk](./agents_bulk/operator.md))  
  Manages Kubernetes controller reconciliation loops, finalizers, and state synchronization.
* **Registrar** 📋 ([standard](./agents/registrar.md) | [bulk](./agents_bulk/registrar.md))  
  Owns Kubernetes Custom Resource Definition (CRD) schema validation and API backward compatibility.
* **Helmsman** ☸️ ([standard](./agents/helmsman.md) | [bulk](./agents_bulk/helmsman.md))  
  Builds, lints, and parameterizes Helm chart structures, templates, and `values.yaml` defaults.
* **Tailor** 🪡 ([standard](./agents/tailor.md) | [bulk](./agents_bulk/tailor.md))  
  Maintains and cleans Kustomize overlays, patch files, and manifest dry configurations.

### 5. CI/CD & Delivery Pipelines
* **Butler** 🤵 ([standard](./agents/butler.md) | [bulk](./agents_bulk/butler.md))  
  Specializes in Jenkinsfile syntax, Scripted/Declarative stages, and Jenkins Shared Libraries.
* **Mason** 🧱 ([standard](./agents/mason.md) | [bulk](./agents_bulk/mason.md))  
  Specializes in Kubernetes-native Tekton Pipelines, Tasks, and Workspace/volume bindings.
* **Stagehand** 🎭 ([standard](./agents/stagehand.md) | [bulk](./agents_bulk/stagehand.md))  
  Specializes in GitHub Actions workflow syntax, runner environment setups, caching, and security constraints.

### 6. Observability, Telemetry & Onboarding
* **Beacon** 📡 ([standard](./agents/beacon.md) | [bulk](./agents_bulk/beacon.md))  
  Handles OpenTelemetry collector pipelines, metrics export setups, and scrape configs.
* **Watcher** 👁️ ([standard](./agents/watcher.md) | [bulk](./agents_bulk/watcher.md))  
  Owns Grafana dashboard panel JSON templates, threshold settings, and alert routing policies.
* **Compass** 📊 ([standard](./agents/compass.md) | [bulk](./agents_bulk/compass.md))  
  Collects product usage analytics, event telemetry, and business intelligence indicators.
* **Scribe** 📝 ([standard](./agents/scribe.md) | [bulk](./agents_bulk/scribe.md))  
  Owns project READMEs, developer onboarding guides, and documentation comments.
* **Pathfinder** 🧭 ([standard](./agents/pathfinder.md) | [bulk](./agents_bulk/pathfinder.md))  
  Focuses on developer experience (DX), automation scripts, and local workspace setup tools.

