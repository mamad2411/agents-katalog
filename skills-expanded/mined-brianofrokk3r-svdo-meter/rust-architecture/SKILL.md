---
name: "rust-architecture"
description: "Use when creating, changing, or reviewing architecture, crate boundaries, harness adapters, CLI/model configuration, event schemas, persistence, reporting, or third-party connector support."
---

# Rust Architecture

## Purpose

SVDO Meter is a thin measurement and reporting layer around agentic CLI work. It associates an external work identifier with an agent CLI session, observes execution, normalizes measurable facts, durably records them, and produces reports. It is not an orchestration framework, ticketing system, model router, or agent SDK.

The architecture must stay thin while allowing:

- multiple agent CLIs/harnesses such as Codex, Claude, Gemini, or future CLIs;
- CLI-specific model configuration;
- session resumption when a CLI supports it;
- workspace association when a CLI needs it;
- stable, append-only telemetry suitable for ingestion by arbitrary systems;
- replayable reporting and future third-party exporters/connectors;
- safe evolution of provider-specific event formats without breaking the canonical schema.

## Product boundary

Inputs to a measured run are conceptually:

- `ticket_identifier`: required external work identifier;
- `label`: human-readable work label;
- `harness`: selected CLI/harness;
- `session`: optional provider session/thread identifier for resumption;
- `workspace`: optional working directory;
- `harness_config`: CLI-specific configuration, including model selection.

Outputs are append-only canonical events plus derived reports.

Do not make story points, human estimates, Jira state, PR state, or other ticket-system fields mandatory runtime inputs. They belong to enrichment/reporting and should join through the ticket identifier.

## Models are CLI configuration

Treat models as configuration for a harness, never as a separate adapter type.

Prefer:

```rust
HarnessConfig::Codex(CodexConfig {
    model: Some("gpt-5.x-codex".into()),
    profile: None,
    extra_args: vec![],
})
```

Instead of:

```rust
CodexGpt5Adapter
CodexOtherModelAdapter
ClaudeSonnetAdapter
ClaudeOpusAdapter
```

A harness adapter owns how its CLI selects, validates, or reports models. The canonical event schema should record both the requested model and, when the provider reports it, the resolved/actual model.

## Recommended Cargo workspace

Start with five crates. Add crates only when dependency isolation, build isolation, ownership, or independent reuse clearly justifies it.

```text
svdo-meter/
├── Cargo.toml
├── Cargo.lock
├── rust-toolchain.toml
├── deny.toml
├── clippy.toml                 # only when project-specific Clippy config is needed
├── README.md
├── SECURITY.md
├── .github/
│   └── workflows/
│       └── ci.yml
├── crates/
│   ├── meter-core/
│   │   └── src/
│   │       ├── lib.rs
│   │       ├── ids.rs
│   │       ├── event.rs
│   │       ├── metrics.rs
│   │       ├── model.rs
│   │       └── time.rs
│   ├── meter-engine/
│   │   └── src/
│   │       ├── lib.rs
│   │       ├── ports.rs
│   │       ├── run.rs
│   │       ├── session.rs
│   │       └── export.rs
│   ├── meter-adapters/
│   │   └── src/
│   │       ├── lib.rs
│   │       ├── harnesses/
│   │       │   ├── mod.rs
│   │       │   ├── codex.rs
│   │       │   ├── claude.rs
│   │       │   └── gemini.rs
│   │       ├── storage/
│   │       │   ├── mod.rs
│   │       │   └── jsonl.rs
│   │       └── connectors/
│   │           ├── mod.rs
│   │           └── README.md
│   ├── meter-report/
│   │   └── src/
│   │       ├── lib.rs
│   │       ├── reducer.rs
│   │       ├── ticket.rs
│   │       ├── run.rs
│   │       └── format.rs
│   └── svdo-meter/
│       └── src/
│           ├── main.rs
│           ├── cli.rs
│           ├── config.rs
│           └── wiring.rs
└── tests/
    └── fixtures/
        ├── codex/
        ├── claude/
        └── gemini/
```

### Dependency direction

Keep dependency direction one-way:

```text
meter-core
    ↑
meter-engine
    ↑
meter-adapters      meter-report
       \              /
        \            /
          svdo-meter
```

Rules:

- `meter-core` depends on no adapter, process, network, or CLI crate.
- `meter-engine` depends on `meter-core`, defines application ports/use cases, and owns lifecycle decisions.
- `meter-adapters` implements ports using processes, files, or network clients.
- `meter-report` consumes canonical events and contains deterministic aggregation/reporting logic.
- `svdo-meter` is the composition root: argument parsing, configuration loading, dependency wiring, exit codes.
- No crate may depend on the binary crate.
- Provider-specific types must not leak into `meter-core` public APIs.

## Core domain

Use explicit newtypes rather than passing raw strings everywhere.

```rust
pub struct TicketId(String);
pub struct RunId(uuid::Uuid);
pub struct EventId(uuid::Uuid);
pub struct SessionId(String);
pub struct HarnessName(String);
pub struct ModelName(String);
```

Use UUIDv7 or another sortable globally unique ID for `run_id` and `event_id`. IDs created by external harnesses remain opaque strings.

Keep canonical metrics factual and additive where possible. Do not persist business interpretations as source facts.

Good canonical facts:

- started/completed timestamps;
- wall duration;
- provider session ID;
- requested/resolved model;
- input tokens;
- cached input tokens;
- output tokens;
- reasoning tokens when available;
- command/tool start and completion;
- exit status;
- file-change events;
- provider errors;
- retries/resumptions;
- harness/provider event type;
- run success/failure/cancellation.

Derived metrics belong in reporting:

- tokens per story point;
- minutes per story point;
- estimated-human-hours / agent-hours;
- effort classification;
- rework classification;
- productivity ratios;
- cost estimates that depend on changing model prices.

## Canonical event envelope

The local append-only event log is the durable source of truth. Every event should have a stable envelope and a versioned payload.

```rust
pub struct MeterEvent {
    pub schema_version: u16,
    pub event_id: EventId,
    pub occurred_at: DateTime<Utc>,
    pub observed_at: DateTime<Utc>,
    pub run_id: RunId,
    pub ticket_id: TicketId,
    pub label: Option<String>,
    pub harness: HarnessName,
    pub requested_model: Option<ModelName>,
    pub resolved_model: Option<ModelName>,
    pub session_id: Option<SessionId>,
    pub workspace: Option<PathBuf>,
    pub kind: EventKind,
    pub payload: EventPayload,
}
```

Prefer a tagged typed payload for canonical fields:

```rust
#[serde(tag = "type", content = "data", rename_all = "snake_case")]
pub enum EventPayload {
    RunStarted(RunStarted),
    SessionObserved(SessionObserved),
    TokenUsage(TokenUsage),
    CommandStarted(CommandStarted),
    CommandCompleted(CommandCompleted),
    FileChanged(FileChanged),
    HarnessEvent(HarnessEventMetadata),
    RunCompleted(RunCompleted),
    RunFailed(RunFailed),
}
```

Provider-specific raw data may be stored as `serde_json::Value`, but only inside an explicitly provider/raw field or separate raw stream. Do not let untyped provider JSON become the canonical domain model.

### Schema evolution

- Version the event schema independently from the binary version.
- Add optional fields compatibly when possible.
- Never change the meaning or units of an existing field silently.
- Use explicit units in names such as `_ms`, `_bytes`, or `_tokens`.
- Never reuse an old enum variant for a different meaning.
- Reports must tolerate unknown future event kinds.
- Preserve enough source metadata to replay/recompute metrics later.

## Harness port

A harness is a CLI integration boundary. It should not know about reports or third-party connectors.

Conceptual port:

```rust
#[async_trait::async_trait]
pub trait HarnessAdapter: Send + Sync {
    fn name(&self) -> &'static str;
    fn capabilities(&self) -> HarnessCapabilities;

    async fn execute(
        &self,
        request: HarnessRequest,
        events: EventPublisher,
    ) -> Result<HarnessResult, HarnessError>;
}
```

`HarnessRequest` includes common fields plus a typed harness configuration enum.

```rust
pub enum HarnessConfig {
    Codex(CodexConfig),
    Claude(ClaudeConfig),
    Gemini(GeminiConfig),
}
```

Do not branch throughout the engine with code such as `if harness == "codex"`. Resolve the adapter once in the composition root or registry and then call the port.

### Capabilities

Model differences between CLIs with capability metadata rather than special-case branches.

```rust
pub struct HarnessCapabilities {
    pub supports_resume: bool,
    pub supports_workspace: bool,
    pub supports_event_stream: bool,
    pub reports_token_usage: bool,
    pub reports_model: bool,
}
```

The engine validates requested behavior against capabilities before spawning the process.

## Process execution

Harness adapters should spawn the actual executable directly and consume structured output incrementally.

Prefer:

```rust
tokio::process::Command::new(binary)
    .arg("exec")
    .arg("--json")
    .arg(prompt);
```

Never prefer:

```rust
Command::new("sh")
    .arg("-c")
    .arg(format!("codex exec --json {prompt}"));
```

Reasons:

- no shell injection surface;
- correct handling of spaces/non-UTF-8 paths;
- no quoting rules to maintain;
- explicit argument boundaries.

Use `PathBuf`/`&Path` for paths and `OsString`/`OsStr` for process arguments where appropriate. Do not force filesystem paths through UTF-8 strings.

Consume stdout/stderr as streams. Do not `read_to_end` unbounded provider output. Use bounded channels and explicit maximum event/line sizes.

## Event normalization

Provider event parsing happens in the provider adapter.

A provider adapter should:

1. receive provider output;
2. parse enough structure to identify the event;
3. preserve the provider event name and safe metadata;
4. normalize known measurable facts into canonical events;
5. ignore unknown fields for metrics without failing the run;
6. optionally preserve raw provider payloads under an explicit retention policy.

Unknown provider events must not crash the meter.

Prefer tolerant parsing:

```rust
let raw: serde_json::Value = serde_json::from_str(&line)?;
let normalized = normalizer.normalize(&raw);
```

Do not require every provider event to match one enormous Rust enum that must be updated before newer CLI versions can run.

## Durable local log first

The local append-only JSONL/NDJSON event store is the primary durable write path.

The runtime sequence is:

```text
provider event
    ↓
normalize
    ↓
append canonical event locally
    ↓
acknowledge internally / continue
```

A remote destination must not sit between the harness and durable local recording.

Do not design:

```text
Codex → Datadog API → local state
```

Design:

```text
Codex → local event log → exporter/checkpoint → Datadog
```

This is an outbox/replay model. It gives:

- no agent-run failure because a SaaS destination is down;
- deterministic replay;
- connector retry without re-running work;
- multiple outputs from the same canonical source;
- easier debugging and auditing.

## Event store port

```rust
#[async_trait::async_trait]
pub trait EventStore: Send + Sync {
    async fn append(&self, event: &MeterEvent) -> Result<(), StoreError>;
    async fn stream(&self, query: EventQuery)
        -> Result<EventStream, StoreError>;
}
```

The initial implementation is `JsonlEventStore`.

Requirements:

- one complete JSON object per line;
- newline terminated records;
- append-only semantics;
- stable UTF-8 serialization;
- bounded event size;
- explicit flush policy;
- no partial record accepted as valid on read;
- corruption handling that can skip/report a final truncated line after crash;
- restrictive file permissions when created;
- no secrets or prompts by default.

The event store is the source of truth. Any session index is a rebuildable projection/cache.

## Session association

Session mappings should be derivable from events.

Emit a canonical event when a provider session is learned or changed:

```text
session_observed(ticket_id, harness, session_id, workspace?)
```

A small local index may accelerate resumption:

```text
(ticket_id, harness, workspace?) -> latest session_id
```

But the index is not canonical. If deleted, rebuild it from the log.

Do not assume a ticket can only ever have one provider session. A ticket may have multiple sessions, harnesses, workspaces, or runs over time.

## Reporting architecture

Reports are pure projections over canonical events.

Use reducers:

```rust
pub trait Reducer<E> {
    type Output;
    fn apply(&mut self, event: &E);
    fn finish(self) -> Self::Output;
}
```

Example hierarchy:

```text
MeterEvent
  ↓
RunReducer
  ↓
RunSummary
  ↓
TicketReducer
  ↓
TicketSummary
  ↓
Period/Team Report
```

Reducers should be deterministic and side-effect free. Given the same ordered event stream, they must return the same report.

Keep report rendering separate from aggregation:

```text
aggregation → ReportModel → terminal/json/html/etc.
```

Do not put ANSI formatting, JSON formatting, or HTML in the reducers.

## Connector architecture

Call third-party outputs `connectors` or `exporters`, not primary runtime sinks.

Conceptual port:

```rust
#[async_trait::async_trait]
pub trait Connector: Send + Sync {
    fn name(&self) -> &'static str;

    async fn export(
        &self,
        batch: &[MeterEvent],
    ) -> Result<ExportReceipt, ConnectorError>;
}
```

Connector requirements:

- consume canonical events, never provider-specific events directly;
- idempotency based on `event_id` when destination semantics allow it;
- checkpoint only after successful remote acceptance;
- exponential backoff with jitter;
- bounded retry policy;
- structured failure reporting;
- batch where the destination supports it;
- configurable field redaction;
- no connector failure may corrupt the local event store;
- connector-specific dependencies remain in the adapter crate or a connector-specific crate if they become heavy.

Split a connector into its own crate only when it has heavy dependencies, independent release/ownership, feature isolation, or materially increases compile time.

## Configuration

Use a typed top-level configuration with harness-specific sections.

Example TOML:

```toml
[storage]
path = "~/.local/state/svdo-meter/events.jsonl"

[harnesses.codex]
binary = "codex"
model = "gpt-5.x-codex"

[harnesses.claude]
binary = "claude"
model = "sonnet"

[connectors.example]
enabled = false
endpoint = "https://example.invalid/v1/events"
```

Rules:

- parse into typed structs;
- validate once at startup;
- keep credentials out of the config file when environment/OS credential stores are available;
- do not use a global `HashMap<String, serde_json::Value>` as application configuration;
- unknown configuration keys should normally be rejected or warned on deliberately, not silently ignored.

## Operational logging vs telemetry

Use `tracing` for SVDO Meter's own diagnostic/operational logs.

Do not mix operational logs with the canonical telemetry stream.

```text
stderr / tracing            → "failed to parse optional provider field"
events.jsonl                → canonical measured work facts
```

This separation prevents debugging text from polluting ingestion.

## This instead of that

### Adapter structure

Use one adapter per CLI/harness with model as config.

Instead of one adapter per CLI/model combination.

### Persistence

Use append-only canonical events plus replayable projections.

Instead of updating one mutable `ticket_metrics.json` record in place.

### Connectors

Use local durable append followed by asynchronous/replayable export.

Instead of performing remote API calls inline before telemetry is durable.

### Metrics

Store raw token counters and timestamps.

Instead of storing only derived fields such as `effective_tokens` or `productivity_score`.

### Provider parsing

Normalize known facts and tolerate unknown events.

Instead of failing when a CLI adds a new JSON field/event.

### Types

Use `TicketId`, `RunId`, `EventId`, `PathBuf`, and typed configs.

Instead of passing `String` and untyped JSON through every layer.

### Process execution

Use `Command::new(binary).args(...)`.

Instead of `sh -c`, `bash -c`, or concatenated command strings.

### Abstraction

Introduce traits at actual replaceable boundaries: harness, event store, connector, clock/test seam.

Instead of creating a trait for every struct simply to appear abstract.

### Errors

Use typed domain/adapter errors in libraries and attach context at boundaries.

Instead of converting everything immediately to strings.

### Metrics aggregation

Use deterministic event reducers.

Instead of incrementing global counters from scattered adapter callbacks.

## When to add a new harness

A new CLI belongs under `meter-adapters/src/harnesses/` initially.

It must implement:

- typed configuration;
- capability declaration;
- process invocation without a shell;
- start behavior;
- resume behavior if supported;
- structured event parsing where available;
- canonical token/session/run events where observable;
- provider-version compatibility tests using fixtures;
- graceful behavior for unknown events;
- no report-specific logic.

Before merging, add fixture-based tests that replay representative output without requiring the real CLI or network credentials.

## When to split a crate

Do not split because a module reached an arbitrary line count.

Split when at least one is true:

- a component has heavy optional dependencies;
- compile-time isolation matters;
- it has an independent public API/use case;
- security isolation is beneficial;
- different teams own/release it;
- feature flags have become hard to reason about;
- dependency direction is otherwise being violated.

## Architecture review checklist

Before approving a structural change, verify:

- Does the core remain provider agnostic?
- Are models still harness config rather than adapter types?
- Is provider-specific JSON contained in the adapter boundary?
- Is telemetry durable locally before optional export?
- Can a report be rebuilt from the event log?
- Can session state be rebuilt from events?
- Does a new dependency belong in the crate receiving it?
- Does the change introduce a shell invocation or unbounded buffer?
- Does it preserve schema compatibility or explicitly version a break?
- Does it avoid recording prompt/model content or credentials by default?
- Can the behavior be tested with deterministic fixtures rather than a live provider?
