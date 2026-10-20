# GEMINI.md - Project Context: Shipper

`shipper` is a **publishing reliability layer** for Rust workspaces. It is designed to make the process of publishing multiple crates safer, deterministic, and resumable, addressing common real-world failures like partial publishes, CI cancellations, and registry backpressure.

## Orientation

- `MISSION.md` — north star: mission, vision, audience, beliefs.
- `ROADMAP.md` — five pillars + nine-competency thesis and sequencing.
- `docs/README.md` — documentation index (Diátaxis: tutorials/how-to/reference/explanation).
- `docs/explanation/why-shipper.md` — the *why*, distilled.
- `docs/product.md`, `docs/structure.md`, `docs/tech.md` — product overview, code structure, tech stack.
- `docs/INVARIANTS.md` — events-as-truth contract.

## Project Overview

- **Core Purpose:** Enhances `cargo publish` by adding a reliability layer that handles planning, preflight checks, retries, and state persistence.
- **Main Technologies:** Rust (Edition 2024), `clap` (CLI), `anyhow` (Error Handling), `serde` (Serialization), `tokio` (Async - though much of the current logic is sync with thread sleeps), `chrono` (Time).
- **Architecture (three-crate product shape, #95):**
    - **`crates/shipper-core` (Engine):** Library only, no CLI deps. Owns planning, preflight, engine execution, registry interaction, state/receipts/events, remediation primitives. Stable embedding surface.
    - **`crates/shipper-cli` (CLI adapter):** Owns `clap` parsing, subcommand dispatch, help text, progress rendering. Exposes `pub fn run()`.
    - **`crates/shipper` (Install face):** 3-line binary forwarding to `shipper_cli::run()`; library re-exports a curated subset of `shipper-core`. This is what users `cargo install`.

## Building and Running

- **Build:** `cargo build`
- **Install CLI:** `cargo install --path crates/shipper --locked`
- **Test:** `cargo test` (Note: some tests use `serial_test` as they modify environment variables or global state).
- **Fuzzing:** Located in `fuzz/` directory; can be run with `cargo-fuzz`.

## Key Commands (via `shipper-cli`)

- `shipper plan`: Builds and displays the deterministic publish order.
- `shipper preflight`: Runs all safety checks (git cleanliness, ownership, version existence) without publishing.
- `shipper publish`: Executes the plan, writing state to `.shipper/state.json` and a receipt to `.shipper/receipt.json`.
- `shipper resume`: Continues an interrupted publish run using the existing state file.
- `shipper status`: Compares local workspace versions against the registry.
- `shipper doctor`: Diagnostics for the environment, authentication (CARGO_REGISTRY_TOKEN), and tool versions.

## Development Conventions

- **Safety:** The project enforces `#[forbid(unsafe_code)]` in the workspace.
- **Error Handling:** Uses `anyhow::Result` for flexible error reporting across the library and CLI.
- **Reporting:** Uses a `Reporter` trait to abstract logging/output, allowing the CLI to provide formatted eprints while keeping the library agnostic.
- **State Management:** Execution state is persisted atomically as JSON. The `plan_id` is used to ensure that resumes match the intended plan.
- **Events-as-Truth Invariant:** `events.jsonl` is the authoritative source of truth; `state.json` is a projection over events for fast resume; `receipt.json` is a summary at end-of-run. See `docs/INVARIANTS.md`.
- **Product Thesis:** Shipper's value is organized as nine competencies (Prove, Survive, Reconcile, Narrate, Remediate, Harden, Profile, Integrate, Ergonomics). See `ROADMAP.md` and master tracking issue #109. The biggest open gap is Reconcile (#102 / #99).
- **North Star:** `MISSION.md` is the canonical mission/vision/beliefs document. Read it before scoping non-trivial work.
- **Testing Pattern:** 
    - Extensive use of `tempfile` for filesystem isolation.
    - Registry interactions are mocked in tests using a local `tiny_http` server.
    - `insta` is used for snapshot testing in some modules.
- **Registry Integration:** Uses `CARGO_REGISTRY_TOKEN` and `CARGO_HOME/credentials.toml` for authentication, mimicking Cargo's own behavior.

## Project Structure

- `crates/shipper-core/src/`:
    - `lib.rs`: Library surface.
    - `engine/`: Preflight + publish + resume + rehearsal orchestration.
    - `plan/`: Workspace analysis, topological ordering, plan ID.
    - `state/`: `state.json`, `events.jsonl`, `receipt.json` persistence.
    - `ops/`: I/O primitives (auth, cargo subprocess, git, lock, process, storage).
    - `runtime/`: Error classification, policy, environment fingerprinting.
    - `types.rs`: Shared data structures (re-exports `shipper-types`).
- `crates/shipper-cli/src/`:
    - `lib.rs`: `pub fn run()` — argparse + subcommand dispatch.
    - `main.rs`: 3-line wrapper over `shipper_cli::run()`.
    - `output/`: Progress bars, formatting.
- `crates/shipper/src/`:
    - `lib.rs`: Curated re-export of `shipper-core`.
    - `bin/shipper.rs`: 3-line wrapper over `shipper_cli::run()`.
- `templates/`: Example CI/CD configurations (GitHub/GitLab).
- `fuzz/`: Fuzzing targets for robust state loading and token resolution.
