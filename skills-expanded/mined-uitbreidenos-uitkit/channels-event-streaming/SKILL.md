---
name: "channels-event-streaming"
description: "Claude Code Channels: real-time event streaming between concurrent sessions, pub/sub patterns, event filtering, cross-session state synchronization, and reactive agent workflows"
---

# Channels — Real-Time Event Streaming

## When to activate
- Running multiple Claude Code sessions that need to share state or coordinate work
- Building reactive workflows that respond to events (file changes, CI results, deployment status)
- Implementing pub/sub patterns where one session publishes events and others subscribe
- Streaming progress updates from a long-running background session to the main session
- Coordinating multi-agent workflows where agents need real-time awareness of each other's progress
- Building event-driven development loops (code → test → deploy → monitor → react)

## When NOT to use
- Single-session workflows with no cross-session communication needs
- One-shot tasks that don't benefit from event-driven architecture
- Simple file-based state passing (just read/write a shared file)
- When eventual consistency is fine and polling works just as well

## Instructions

### 1. Channel Architecture

Channels provide real-time event streams between Claude Code sessions:

```
┌──────────────┐  publish   ┌──────────┐  subscribe  ┌──────────────┐
│  Session A   │──────────▶│  Channel │◀────────────│  Session B   │
│  (publisher) │            │  (stream)│             │  (subscriber)│
└──────────────┘            └──────────┘             └──────────────┘
                                  │
                            subscribe
                                  │
                            ┌──────────────┐
                            │  Session C   │
                            │  (subscriber)│
                            └──────────────┘
```

### 2. Channel Types

| Channel Type | Use Case | Event Frequency | Example |
|---|---|---|---|
| **Progress** | Report task completion % | Low (per milestone) | Build progress: 45% → 60% → 80% |
| **State** | Sync shared state | Medium (on change) | Deployment status: staging → production |
| **Alert** | Notify on conditions | Low (on trigger) | CI failure, security finding, SLA breach |
| **Stream** | Continuous data flow | High (continuous) | Log tailing, metric streams, file watchers |
| **Signal** | One-shot coordination | Very low (once) | "Tests passed, proceed with merge" |

### 3. Pub/Sub Patterns

**Publisher session (producing events):**
```yaml
channel: "ci-pipeline"
publish:
  events:
    - type: "build.started"
      data: {branch: "main", commit: "abc123"}
    - type: "build.progress"
      data: {stage: "testing", percent: 45}
    - type: "build.complete"
      data: {status: "success", duration_seconds: 184}
    - type: "build.failed"
      data: {stage: "lint", error: "3 errors found", file: "src/api.ts"}
```

**Subscriber session (consuming events):**
```yaml
channel: "ci-pipeline"
subscribe:
  filter:
    types: ["build.complete", "build.failed"]  # only these events
  on_event:
    build.complete: "Summarize what changed and prepare release notes"
    build.failed: "Analyze the error and suggest a fix"
```

### 4. Event Filtering

Reduce noise by filtering events before processing:

```yaml
filters:
  # Type filter: only process specific event types
  type: ["deploy.started", "deploy.complete", "deploy.failed"]
  
  # Source filter: only events from specific sessions
  source: ["session-ci-runner", "session-deploy-bot"]
  
  # Data filter: match on event payload fields
  data:
    environment: "production"       # only production events
    severity: ["critical", "high"]  # only high-severity alerts
  
  # Rate filter: throttle high-frequency events
  rate:
    max_per_minute: 10
    strategy: "latest"  # keep only the latest if throttled
```

### 5. Cross-Session State Synchronization

Keep multiple sessions in sync with shared state:

```yaml
shared_state:
  channel: "project-state"
  keys:
    - name: "deployment_status"
      publisher: "deploy-session"
      subscribers: ["dev-session", "monitoring-session"]
      on_conflict: "last_write_wins"
    
    - name: "test_results"
      publisher: "test-session"
      subscribers: ["dev-session"]
      on_conflict: "merge"  # combine results from multiple publishers
```

**State sync pattern:**
```
Session A (dev):       publishes {current_file: "src/api.ts", task: "refactor auth"}
Session B (tests):     subscribes → auto-runs tests on src/api.ts when it changes
Session C (docs):      subscribes → updates API docs when src/api.ts changes
```

### 6. Reactive Workflow Patterns

**Event-driven development loop:**
```yaml
workflow: "reactive-dev-loop"
channels:
  - name: "file-changes"
    subscribe:
      filter: {types: ["file.saved"], paths: ["src/**"]}
    on_event: "run tests for changed module"
    
  - name: "test-results"
    subscribe:
      filter: {types: ["test.complete"]}
    on_event:
      status=pass: "update coverage badge, proceed to next task"
      status=fail: "analyze failure, suggest fix, pause workflow"
    
  - name: "coverage-updates"
    subscribe:
      filter: {types: ["coverage.updated"], threshold_below: 80}
    on_event: "alert: coverage dropped below 80%, identify untested code"
```

**Multi-agent coordination:**
```yaml
workflow: "parallel-research"
agents:
  - session: "researcher-frontend"
    channel: "research-progress"
    publishes: ["topic.complete", "finding.interesting"]
    
  - session: "researcher-backend"
    channel: "research-progress"
    publishes: ["topic.complete", "finding.interesting"]
    
  - session: "synthesizer"
    channel: "research-progress"
    subscribes: ["topic.complete"]
    on_event: "check if all topics covered, begin synthesis when ready"
```

### 7. Event Schema

Standard event format for consistency:

```json
{
  "id": "evt_a1b2c3d4",
  "channel": "ci-pipeline",
  "type": "build.failed",
  "source": "session-ci-runner",
  "timestamp": "2026-06-13T14:32:00Z",
  "data": {
    "stage": "lint",
    "error": "3 errors found",
    "file": "src/api.ts",
    "details": ["unused import", "missing return type", "unsafe any"]
  },
  "metadata": {
    "retry_count": 0,
    "ttl_seconds": 3600
  }
}
```

## Example

**Coordinating a build-test-deploy pipeline across 3 sessions:**

```yaml
# Session 1: Builder
channel: "release-pipeline"
publish:
  - {type: "build.started", data: {version: "1.11.0"}}
  - {type: "build.complete", data: {artifacts: ["dist/uitkit-1.11.0.tgz"]}}

# Session 2: Tester (subscribes to build events)
channel: "release-pipeline"
subscribe:
  filter: {types: ["build.complete"]}
  on_event: "run full validation suite against artifacts"
publish:
  - {type: "tests.passed", data: {coverage: 87, suites: 12, duration: "4m22s"}}

# Session 3: Deployer (subscribes to test events)
channel: "release-pipeline"
subscribe:
  filter: {types: ["tests.passed"]}
  on_event: "deploy to staging, run smoke tests, then promote to production"
publish:
  - {type: "deploy.complete", data: {environment: "production", url: "..."}}
```

## Anti-Patterns

- **Chatty channels:** Publishing every minor event floods subscribers — aggregate at source, publish only milestones
- **No backpressure:** If publisher outpaces subscriber, events queue infinitely — set buffer limits and drop/summarize old events
- **Missing event types:** Publishing untyped events ("something happened") makes filtering impossible — always use structured type names (domain.action)
- **Tight coupling:** Subscriber hard-codes publisher's session ID — use channel names and event types, not session references
- **Silent failures:** Subscriber crashes on malformed event without logging — always wrap event handlers in try/catch with dead-letter logging
- **Stale state:** Subscribing to state changes but not requesting current state on connect — always sync initial state before processing incremental updates
