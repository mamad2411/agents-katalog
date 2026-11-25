---
name: rust
description: "Rust engineering standards and deep references — ownership/borrowing-driven design, error handling (thiserror/anyhow), async with tokio, axum services, testing, and clippy/cargo-deny discipline. Load whenever writing, editing, or reviewing Rust: any .rs file, Cargo.toml/Cargo.lock change, cargo or clippy failure, or Rust design/test planning — with or without a role agent (/be, /rev) invoked. NOT for merely running or installing a compiled Rust tool."
---

# Rust (language skill)

This is a knowledge skill, not an agent: it loads from context whenever Rust is written or reviewed, and the role agents (`/be`, `/rev`, `/arch`) route into it for the language-level rules.
It carries the standards inline; the deep material lives in `references/` and is loaded on demand.

## Trigger

Use this skill when:
- Writing, editing, or reviewing `.rs` files
- Changing `Cargo.toml` or `Cargo.lock` — dependencies, features, lints, workspace layout
- Diagnosing a `cargo` or `clippy` failure
- Designing a Rust component — crate boundaries, error surface, async topology
- Planning tests for Rust code
- Adding a dependency to a Rust workspace

Do NOT load it for merely running or installing a compiled Rust tool — that is an operations task, not a Rust task.

## Context

This skill exists to make Rust reviews boring. Invariants live in types, so the compiler
argues about them instead of the reviewer. Failure paths are enumerated before code is
written, so error handling is a table being filled in, not an improvisation. Policy —
toolchain, lints, formatting, dependency rules, coverage — lives in checked-in files,
not in anyone's head, so "what does this repo require?" has exactly one answer. The two
goals behind every rule here: predictable consequences and cheap extension.

## Documentation Lookup (MANDATORY)

**Before implementing any feature**, check current documentation. Rust ships a new stable
release every six weeks and several load-bearing crates are pre-1.0; recall is not a source.

### Context7 MCP

Use Context7 MCP to retrieve up-to-date documentation for any crate or tool:

1. **Resolve library**: Call `mcp__context7__resolve-library-id` with the crate name
2. **Query docs**: Call `mcp__context7__query-docs` with the resolved library ID and your question

**When to use:** tokio primitives, axum extractors/routing/middleware, rusqlite API,
serde attributes, clap derive, proptest strategies.

**Example queries:**
- "tokio JoinSet and graceful shutdown"
- "axum 0.8 State extractor and middleware ordering"
- "rusqlite transactions and prepared statement caching"
- "thiserror 2 derive attributes and #[from]"
- "clap 4 derive subcommands and value parsing"
- "proptest strategies for recursive data"

### Web Research

Use `WebSearch` and `WebFetch` for anything version- or advisory-shaped:

| Question | Source to check |
|----------|-----------------|
| What changed in a stable Rust release | releases.rs / the official release notes |
| Which clippy lints are new or renamed at a version | the clippy lint list for that exact version |
| Is there an advisory against this crate | the RUSTSEC advisory database |
| What is the current version of a crate | its repository / registry page, at task time |

### Rust-specific lookup rules

- **Toolchain bumps read the notes first.** When bumping the pinned toolchain, read the
  release notes and the new clippy lints for the target version (releases.rs is the
  fastest index) *before* editing `rust-toolchain.toml`. New deny-by-default behaviour
  arrives with the compiler; meeting it in CI is not reading.
- **Pre-1.0 UI frameworks are looked up, never recalled.** Frameworks below 1.0 change
  APIs between minor versions. Look their APIs up against the framework's own repository
  at task time — current examples tree, current migration notes. This skill deliberately
  encodes none of their API surface, because anything written here would be wrong within
  two releases.

**Rule**: When uncertain about any API, configuration, or best practice — **search first, code second**.

## Versions

| Technology | Version | Notes |
|------------|---------|-------|
| Rust (stable) | 1.97.0 (2026-07-09) | Pin exactly in `rust-toolchain.toml` — see `references/toolchain-and-lints.md` |
| Edition | 2024 | The baseline; available since Rust 1.85 |
| Cargo `[lints]` | stable since Cargo 1.74 | Workspace-level lint severities in the manifest |
| clippy.toml | test allowances | `allow-unwrap-in-tests`, `allow-expect-in-tests`, `allow-panic-in-tests` |
| tokio | 1.x | Async runtime; the lockfile pins the minor |
| thiserror | 2 | Error derives for library crates |
| anyhow | 1 | Error type for binary boundaries only |
| axum | 0.8 | HTTP services; pre-1.0 — re-check APIs at task time |
| rusqlite | 0.40 | Embedded SQLite; `bundled` implications in `references/dependencies-supply-chain.md` |
| clap | 4 | CLI argument parsing (derive) |
| rand | 0.9 | OS entropy via `TryRngCore` (`OsRng.try_fill_bytes`); 0.8's infallible `OsRng.fill_bytes` is gone |
| proptest | 1 | Property-based testing |
| cargo-deny, cargo-audit, cargo-llvm-cov, cargo-machete | current | Supply chain, advisories, coverage, unused deps |

> **Volatility note.** Versions above are current as of **Aug 2026 — re-verify before
> pinning**. Rust itself moves every six weeks; the pre-1.0 crates move faster.

## The Doctrine — ten standards (BLOCKING at review)

Each standard is one sentence of rule, enforced at review, with the mechanism and depth
in its reference. A violation is a review finding, not a style comment.

### 1. Illegal states are unrepresentable

**Rule:** Model state so the compiler rejects the impossible — no `bool` + `Option` pairs
that co-vary, enums with data-carrying variants for mutually exclusive states, a newtype
at every meaning-bearing boundary.

A `(bool, Option<T>)` pair has four representable states where the domain has two, and
every reader must re-derive which two are legal. An enum makes the illegal states
unwritable and every `match` exhaustive, so adding a state breaks the build at every
site that must care. Newtypes turn ID-swapping bugs into type errors, paid once at
design time.

```rust
// BAD — four representable states, two legal; the invariant lives in reviewers' heads
struct Job {
    finished: bool,
    result: Option<Output>,
}

// GOOD — exactly the legal states; forgetting a case fails to compile
enum Job {
    Running { started: Instant },
    Finished { result: Output },
}
```

→ `references/architecture.md`

### 2. Failure paths are enumerated before code

**Rule:** Every new fallible function gets a failure table in the dev doc before
implementation — failure | detected by | mapped to | caller action | test name — and
tests are named from its rows.

Error handling written during implementation is improvisation; error handling written
before it is a contract. The table forces the questions that get skipped under time
pressure — who detects this, what does the caller do — and its last column *is* the
test list, so coverage of failure paths is planned rather than accidental.

| Failure | Detected by | Mapped to | Caller action | Test name |
|---------|-------------|-----------|---------------|-----------|
| Config file missing | `fs::read` `NotFound` | `ConfigError::Missing { path }` | fall back to defaults, warn once | `missing_config_falls_back_to_defaults` |
| Config not valid TOML | `toml::from_str` | `ConfigError::Malformed { source }` | exit nonzero with parse location | `malformed_config_exits_with_location` |
| Port already bound | `TcpListener::bind` | `StartupError::PortInUse { port }` | exit nonzero naming the port | `bound_port_exits_naming_port` |

→ `references/errors.md`

### 3. Zero unwrap/expect/panic in production paths

**Rule:** `unwrap()`, `expect()`, and `panic!()` are banned from production code by
`[workspace.lints]` — enforced by the build, not by convention — with tests exempted
via clippy.toml.

Conventions do not survive deadlines; lints do. `clippy::unwrap_used`,
`clippy::expect_used`, and `clippy::panic` at `deny` make the ban a compile failure,
and the clippy.toml test allowances (`allow-unwrap-in-tests` and friends) keep it
practical — in a test, unwrap *is* the assertion.

```toml
# Root Cargo.toml (excerpt — full template in the reference)
[workspace.lints.clippy]
unwrap_used = "deny"
expect_used = "deny"
panic = "deny"
```

```toml
# clippy.toml — the exemption that makes the ban livable
allow-unwrap-in-tests = true
allow-expect-in-tests = true
allow-panic-in-tests = true
```

→ `references/toolchain-and-lints.md`

### 4. Every spawned task has an owner

**Rule:** Every `tokio::spawn` yields a `JoinHandle` that is awaited, tracked in a
`JoinSet` (or equivalent), or explicitly documented as detached — a silently dropped
handle is a defect.

A dropped handle detaches the task: its panic is never observed, its completion is never
awaited, and shutdown cannot drain it. That is occasionally the right design — a
fire-and-forget metrics flush — but then it is a documented decision at the spawn site,
not an accident of an ignored return value.

```rust
async fn run(state: AppState) -> anyhow::Result<()> {
    let mut tasks = tokio::task::JoinSet::new();
    tasks.spawn(sync_loop(state.clone()));
    tasks.spawn(flush_loop(state));
    while let Some(joined) = tasks.join_next().await {
        joined?;
    }
    Ok(())
}
```

→ `references/async-tokio.md`

### 5. Policy is checked-in files

**Rule:** `rust-toolchain.toml` (exact pin + CI assertion), `[workspace.lints]`,
`rustfmt.toml`, `deny.toml`, and a coverage threshold all exist in the repository —
absence of any of these in an application repo is a review finding.

Policy that lives in heads is renegotiated on every PR; policy that lives in files is
diffed, reviewed, and enforced by machines. These five files are the whole surface:
which compiler, which lints at which severity, which formatting, which dependencies,
how much test coverage. Their absence is not neutral — it means the policy is whatever
happened most recently.

| File | What it pins |
|------|--------------|
| `rust-toolchain.toml` | The exact compiler — asserted in CI, bumped deliberately |
| `[workspace.lints]` in root `Cargo.toml` | Lint severities, identical locally and in CI |
| `rustfmt.toml` | Formatting — one answer per workspace, and per product |
| `deny.toml` | Advisories, licenses, bans, sources |
| Coverage threshold in CI | The floor under test coverage — ratchet-only |

→ `references/toolchain-and-lints.md`, `references/dependencies-supply-chain.md`

### 6. Tests are behaviour sentences, listed before implementation

**Rule:** The test list is written before the code, each name a sentence about observable
behaviour; timing logic runs under paused tokio time; fixtures refuse to start when a
real credential is present in the environment.

A test named `test_process_2` verifies nothing to a reader; `expired_token_is_rejected`
is a requirement that happens to be executable. Paused time (`tokio::time::pause`) makes
timeout logic deterministic and instant instead of flaky and slow. The credential guard
turns "the test suite accidentally hit production" from an incident into a refused start.

```rust
#[tokio::test(start_paused = true)]
async fn idle_connection_is_closed_after_timeout() {
    let pool = Pool::with_idle_timeout(Duration::from_secs(300));
    let conn = pool.checkout().await;
    pool.release(conn);

    tokio::time::advance(Duration::from_secs(301)).await;

    assert_eq!(pool.open_connections(), 0);
}
```

→ `references/testing.md`

### 7. Errors are API contracts

**Rule:** Library crates expose `thiserror` enums; `anyhow` appears only at binary
boundaries; wire error codes are named constants in one module with an exhaustive
round-trip test.

An error type is the half of the API that gets designed by accident. A `thiserror` enum
makes the failure surface enumerable and matchable by callers; `anyhow` in a library
erases exactly that. Wire codes scattered as string literals drift — one module, named
constants, and a round-trip test that fails when a variant is added but not mapped.

```rust
// Library crate: enumerable, matchable failure surface
#[derive(Debug, thiserror::Error)]
pub enum StoreError {
    #[error("record {id} not found")]
    NotFound { id: RecordId },
    #[error("storage unavailable")]
    Unavailable(#[from] rusqlite::Error),
}
```

```rust
// Binary boundary: anyhow adds context on the way out, and only here
fn main() -> anyhow::Result<()> {
    let config = load_config().context("loading configuration")?;
    run(config).context("running service")
}
```

→ `references/errors.md`

### 8. unsafe is forbidden outside audited FFI islands

**Rule:** `unsafe_code = "deny"` at workspace level; per-crate opt-out only for dedicated
FFI crates; every `unsafe` block carries a `// SAFETY:` comment stating the invariant it
relies on.

Rust's guarantee is only as good as the discipline around its escape hatch. Confining
`unsafe` to named island crates makes the audit surface small and findable, and
`clippy::undocumented_unsafe_blocks` at `deny` makes the SAFETY comment a build
requirement rather than a habit.

→ `references/security.md`

### 9. Validate at process boundaries; secrets stay out of argv and logs

**Rule:** Input crossing a process boundary is validated on entry into domain types;
secrets arrive via environment or file, never argv; secret comparison is constant-time.

Inside the process, types carry the proof of validation (standard one); the boundary is
where the proof is created. Argv is world-readable on shared hosts and lands in shell
history and process listings; logs outlive incidents. `==` on secret material leaks
timing — comparison goes through a constant-time primitive, always.

```rust
// The boundary parses raw input into a domain type; everything inside takes the type.
impl TryFrom<&str> for TenantId {
    type Error = ValidationError;

    fn try_from(raw: &str) -> Result<Self, Self::Error> {
        let trimmed = raw.trim();
        if trimmed.is_empty() || trimmed.len() > 64 {
            return Err(ValidationError::TenantIdLength { len: trimmed.len() });
        }
        Ok(TenantId(trimmed.to_owned()))
    }
}
```

→ `references/security.md`

### 10. One framework-agnostic core crate; shells are thin adapters

**Rule:** Domain logic lives in a core crate with no framework dependency; CLI, HTTP,
and UI shells adapt it — a UI-framework major bump must not touch the core crate.

The test is mechanical: if bumping the UI framework's major version produces a diff in
the core crate, the boundary has leaked. Pre-1.0 frameworks churn; a thin shell absorbs
the churn in one place. The core crate is also where the real tests live — fast, no
framework harness, no I/O.

```text
workspace/
├── core/          # domain types, logic, errors — no framework dependency
├── cli/           # clap shell: parse args, call core, print
├── server/        # axum shell: extract, call core, respond
└── ui/            # UI-framework shell — the only crate a framework bump may touch
```

→ `references/architecture.md`

## Deep-dive references (load on demand)

Nine references live in `references/` — read the relevant one when the task calls for
it, not all of them up front:

- `references/toolchain-and-lints.md` — toolchain pinning + CI assertion, MSRV, edition
  2024 idioms, the full `[workspace.lints]` template, clippy.toml, rustfmt.toml,
  coverage, CI gate order. Load when setting up or reviewing repo policy, or on any
  clippy/fmt dispute.
- `references/dependencies-supply-chain.md` — lockfile law, pin policy, the deny.toml
  template, advisory-ignore reasoning, unmaintained and bundled-C dependencies. Load
  when adding, bumping, or auditing dependencies.
- `references/architecture.md` — type-driven design, newtypes, crate layout, the
  core-vs-shell split. Load when shaping a new crate, module, or public API.
- `references/errors.md` — failure tables, the thiserror/anyhow split, wire-code
  registry and round-trip tests. Load when defining or mapping any fallible surface.
- `references/async-tokio.md` — task ownership, cancellation, channels and backpressure,
  locks across `.await`. Load for any async code.
- `references/sqlite-rusqlite.md` — embedding SQLite from Rust: connection ownership,
  migrations, the `bundled` feature. SQL semantics live in the sql language skill
  `../sql/SKILL.md` — cross both ways.
- `references/testing.md` — behaviour-sentence tests, paused tokio time, fixture
  guards, proptest. Load when planning or writing tests.
- `references/security.md` — the unsafe policy, secret handling, boundary validation.
  Load for security-relevant code or any `unsafe`.
- `references/rust-review.md` — the reviewer's pass over a Rust diff. Loaded by `/rev`,
  and for self-review before requesting one.

## Workflow note

This skill owns no gates. The `workflow-engine` contract and the role agents' own gate
checks apply unchanged; this skill only supplies the language knowledge inside them.
Rust-specific gate triggers to know (they mirror `workflow.yaml` — that file decides):

- New dependencies, new crates, and new crate boundaries are **ARCH triggers**
  (`new_dependency`, `new_service`, `cross_boundary`).
- Security-sensitive surfaces — auth, secrets, external input, **network exposure such
  as a new listening socket**, crypto — are **SECOPS triggers**.
- New `unsafe` is not a named workflow trigger; it is BLOCKING-severity review
  territory (`references/rust-review.md`), and `/rev` escalates to `/secops` when the
  block touches a security surface.

Whether those gates fire is the workflow-engine's decision, not this skill's. What this
skill does supply is the evidence the gates consume: the failure table, the test list,
and the checked-in policy files are what `/rev` and `/verify` check against.

## Checklist

### Before Implementing
- [ ] Failure table written for every new fallible function (standard two)
- [ ] Test list written — behaviour sentences, before any implementation (standard six)
- [ ] Stack versions confirmed against `## Versions` — and re-verified if that table is stale
- [ ] The deep-dive reference for the touched area loaded

### Before Commit
- [ ] `cargo fmt --check` clean
- [ ] `cargo clippy --all-targets --locked -- -D warnings` clean
- [ ] `cargo test --locked` green
- [ ] `cargo deny check` clean
- [ ] No TODO/FIXME committed (`clippy::todo` at deny makes this mechanical)
- [ ] Change verified as landed — behaviour observed, not assumed (the `verify-landed` process skill)

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| `unwrap()` in a production path | Turns a recoverable failure into a process abort at a distance | `Result` + failure table; ban enforced by `[workspace.lints]` (standard three) |
| Lock held across `.await` | Deadlocks and stalled tasks when the future parks while holding the guard | Scope the guard before awaiting; `clippy::await_holding_lock` at deny |
| Dropped `JoinHandle` | Task panics vanish; shutdown cannot drain the task | Await it, track it in a `JoinSet`, or document the detachment (standard four) |
| `bool` + `Option` co-varying state | Illegal state combinations are representable and eventually occur | One enum with data-carrying variants (standard one) |
| Stringly-typed IDs | Any `String` fits any parameter; swapped IDs compile and corrupt | Newtypes at meaning-bearing boundaries |
| Real `sleep` in tests | Slow suite, then flaky suite as timings tighten | Paused tokio time; assert on the clock, not the wall |
| Env mutation in tests | `set_var` is `unsafe` in edition 2024 for a reason — process-global races | Inject config; tests build their own config values |
| Advisory ignore without a reason | Permanent by default; the scanner goes quiet one entry at a time | Three-part reason: path, why unreachable, exit trigger — `references/dependencies-supply-chain.md` |
| `CREATE TABLE IF NOT EXISTS` as the migration story | Schema drift is invisible; existing tables never evolve | Versioned migrations — `references/sqlite-rusqlite.md` |
| `==` on secret material | Comparison time leaks how much of the secret matched | Constant-time comparison primitive (standard nine) |
| Unbounded channels | Hidden queue grows until memory pressure becomes the backpressure | Bounded channels; choose the full-queue behaviour explicitly |
| TODO in committed code | A promise with no owner and no trigger | Finish it, or file a ticket and remove the marker; `clippy::todo` at deny |
| Ad-hoc wire error codes | String literals drift between producer and consumer | One constants module + exhaustive round-trip test (standard seven) |
| Divergent rustfmt widths across sibling repos of one product | Every cross-repo diff is noise; reviews slow down | One width, in `rustfmt.toml`, everywhere — `references/toolchain-and-lints.md` |
