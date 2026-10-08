---
name: port-daddy
description: >-
  Multi-agent coordination daemon for coding agents. Use for deterministic port
  claims, session tracking, salvage, file claims, notes, pub/sub, tuple-space
  coordination, background fleets, and debugging multi-agent failures across
  Claude Code, Codex, Gemini CLI, Cursor, or Windsurf. NOT for production
  deploy orchestration, Docker or Kubernetes networking, or cloud service
  discovery.
metadata:
  tags:
  - port
  - daddy
  provenance:
    kind: first-party
    owners: &id001
    - some-claude-skills
  authorship:
    maintainers: *id001
---

# Port Daddy v3.8.2 — Agent Coordination That Actually Works

## NOT for

- Production deployment orchestration, rollout policy, or CI release gating.
- Docker, Kubernetes, service-mesh, or cloud network discovery problems.
- Single-agent local work where no port coordination, salvage, or shared-state workflow exists.

## The Problem You Have Right Now

You're an AI agent. You're about to start a dev server. Which port? 3000? Taken. 3001? Another agent grabbed it. You pick a random port. Now nothing can find your server.

Meanwhile, another agent is editing the same file you are. Neither of you knows. You'll both commit. One of you loses work.

A third agent crashed 20 minutes ago — halfway through a migration. Its work is orphaned. Nobody knows.

**Port Daddy solves all of this in one daemon.**

## Decision Tree — Pick the Right Primitive

Read top-to-bottom. The first matching leaf is your answer. If you skip the daemon-up check, every subsequent decision is meaningless.

```mermaid
flowchart TD
  A[I want to do something coordination-shaped] --> Up{pd status<br/>== running?}
  Up -- no --> Down[examples/06-debug-daemon-down.md]
  Up -- yes --> Scope{Scope?}

  Scope -- single agent, no shared state --> Out[Out of scope: just code.<br/>NOT for this skill.]
  Scope -- this agent, this session --> Life[Lifecycle path]
  Scope -- two+ agents, same repo --> Coord[Coordination path]
  Scope -- background cadence / fleet --> Fleet[Fleet path]
  Scope -- many agents, same harbor --> Swarm[Swarm path]

  Life --> L1{What do I need?}
  L1 -- "session boundary" --> L1a[pd begin / pd done<br/>schemas/note-shape.md]
  L1 -- "deterministic port" --> L1b[pd claim {project}:{stack}:{ctx}<br/>schemas/semantic-identity.md<br/>examples/07-port-collision.md]
  L1 -- "audit trail" --> L1c[pd note --type ...<br/>assets/session-note.template.md]
  L1 -- "what happened?" --> L1d[pd sitrep / catch_me_up MCP]

  Coord --> C1{Failure mode I'm preventing?}
  C1 -- "two agents edit same file" --> C1a[pd session files claim<br/>examples/02-two-agents-same-file.md]
  C1 -- "must be exclusive" --> C1b[pd with-lock<br/>or pd lock + pd unlock]
  C1 -- "agent-to-agent signal" --> C1c[pd pub + pd watch]
  C1 -- "DM a specific agent" --> C1d[pd inbox send<br/>or talk_to_agent MCP]
  C1 -- "agent died, finish their work" --> C1e[pd salvage claim<br/>schemas/salvage-entry.md<br/>examples/03-salvage]

  Fleet --> F1{Fleet exists?}
  F1 -- "no" --> F1a[pd fleet init + edit pd-fleet.yml<br/>assets/pd-fleet.starter.yml<br/>examples/04-fleet-from-zero.md]
  F1 -- "yes, broken" --> F1b[scripts/fleet-validate.sh<br/>schemas/pd-fleet.schema.md]
  F1 -- "yes, want it daemon-managed" --> F1c[POST /fleet/register<br/>survives terminal close]
  F1 -- "yes, want to chain agents" --> F1d[on_success: publish channel<br/>+ declare in channels:]

  Swarm --> S1{Shape of the data?}
  S1 -- "typed records, multi-reader" --> S1a[pd tuple out + pd tuple rd<br/>schemas/tuple-shape.md]
  S1 -- "exactly-once work" --> S1b[pd tuple in<br/>work-stealing<br/>examples/05-tuple-swarm-handoff.md]
  S1 -- "ambient gradient / heat" --> S1c[pd pheromone spray<br/>schemas/pheromone-signal.md]
  S1 -- "broadcast, ephemeral" --> S1d[pd pub on a harbor channel]
```

**The five questions, in order:**

1. **Daemon up?** — `pd status`. If not, you have no coordination at all. Fix this first.
2. **Scope?** — single-session, two-agent, fleet (cadence), or swarm (many-in-harbor)? They use different primitives; mixing them is theatre.
3. **What failure mode am I preventing?** — silent overwrite, port conflict, dead-agent loss, missed signal? The failure mode chooses the primitive.
4. **Durable or ephemeral?** — notes (forever) and tuples-with-no-TTL (until-removed) are durable. Pheromones and pub/sub are ephemeral. Picking the wrong one either pollutes the audit trail or loses signal.
5. **Read-many or take-once?** — `tuple rd` and `pub` are fan-out; `tuple in` and `lock` are exactly-one-winner. Get this wrong and you either drop work or duplicate it.

## Failure-Mode Triage

When something is already broken, jump straight here.

| Symptom | Likely cause | First diagnostic | Fix / runbook |
|---|---|---|---|
| `pd <anything>` → `Connection refused` | Daemon not running | `pd status` | `examples/06-debug-daemon-down.md` |
| `pd status` hangs forever | Daemon wedged on event loop | `lsof ~/.port-daddy/daemon.sock`; check `daemon.log` | `kill -9 $(cat ~/.port-daddy/daemon.pid)` then `pd start` |
| `pd claim` returns the "wrong" port | Identity-deterministic by design — it's correct | `pd find <identity>` to confirm | Use a different identity context, not a different port |
| `pd begin` says session already active | Stale session for this PID | `pd whoami` | `pd done` then re-`begin`, or continue in the existing one |
| `pd session files claim` says conflict | Another agent already claimed it | `pd swarm_awareness` or read the warning | `examples/02-two-agents-same-file.md` |
| Fleet agent never fires on commit | `fleet.name != basename(projectDir)` (most common) | `scripts/fleet-validate.sh` | Fix `fleet.name`; re-`pd fleet up` |
| Fleet agent fires but does nothing | `prompt` is too vague, or `allowedTools` blocks needed action | `pd spawned` shows it ran briefly; check its log | Tighten the prompt; widen the allowlist |
| `pd salvage` shows huge backlog | Stale entries from agents that crashed long ago | `pd salvage --project <p>` | Triage with `scripts/salvage-triage.sh`; dismiss obviously-dead entries |
| `pd tuple rd` returns nothing | Wrong harbor or pattern shape | `pd tuple scan --harbor <h>` | `schemas/tuple-shape.md` for grammar |
| `pd note` writes succeed but `pd notes` returns empty | Notes encrypted but key changed | `ls -la ~/.port-daddy/master.key` perms must be `0600` | Restore key from backup; otherwise the notes are unreadable |
| Pheromone always reads near-zero | Decay outpacing spray cadence | `pd pheromone show --table <t> --id <i>` | Either spray more often or raise `--strength`; pheromones are not a database |
| Two agents both `tuple in` succeed on same tuple | Bug — file feedback | `.spark/feedback/$(date +%F)-tuple-double-take.md` | The daemon should atomic-take; this is a regression |

## L3 Index — Where the Deep Knowledge Lives

This file is the L1/L2 entry. Don't paste deep references inline — load on demand:

| Need | Read |
|---|---|
| Worked end-to-end scenario | `examples/INDEX.md` (8 scenarios: bootstrap, conflict, salvage, fleet, swarm, daemon-down, port-collision) |
| Authoritative contract / data shape | `schemas/INDEX.md` (semantic-identity, pd-fleet schema, tuple, note, pheromone, salvage, MCP tools) |
| One-shot helper to run | `scripts/` (preflight, session-resume, salvage-triage, fleet-validate, agent-handshake) |
| Template to copy and edit | `assets/` (pd-fleet.starter.yml, .portdaddyrc.starter, session-note.template.md) |
| Full HTTP API (93+ endpoints) | `references/api-reference.md` |
| JavaScript SDK | `references/sdk-reference.md` |
| Advanced multi-agent patterns | `references/multi-agent-patterns.md` |
| `.portdaddyrc` per-project config | `references/portdaddyrc-spec.md` |


## Quick Start (Do This First)

```bash
# 1. Start your session — ALWAYS do this first
pd begin "Building auth module"

# 2. Claim a port — deterministic, never conflicts
PORT=$(pd claim myapp:api:main -q)

# 3. Leave breadcrumbs for other agents
pd note "JWT validation working, moving to refresh tokens"

# 4. Check who else is working here
pd salvage --project myapp    # Any dead agents to rescue?

# 5. End cleanly
pd done
```

## Why This Matters

Without Port Daddy:
- Port conflicts every time two agents run dev servers
- No record of what agents did or decided
- Crashed agents leave orphaned work nobody finds
- No way for agents to signal each other
- File edit collisions destroy work silently

With Port Daddy:
- Deterministic ports — same identity always gets the same port
- Immutable notes — full audit trail of every decision
- Salvage queue — dead agent work is preserved and claimable
- Pub/sub + file claims — agents coordinate without stepping on each other
- Background fleet — QA, docs, testing run automatically on every commit
- Binary IPC — sub-microsecond heartbeats and pheromone sprays over Unix socket
- Pheromone trails — ambient numeric signals that decay over time for contention detection
- Tuple space — shared typed memory for swarm coordination
- Semantic trie — O(k) identity lookups replacing SQL LIKE scans

## Shibboleths

- If the task only needs one temporary port and no shared session state, launching fleets and pheromone trails is theater, not coordination.
- If you need hard exclusion for a critical section, use a lock; advisory file claims are for negotiation, not safety.
- If the failure is in container ingress, DNS, or production service discovery, Port Daddy is the wrong layer.

## MCP Tools Available

**Start here (high-level, one call does many things):**

| Tool | What It Does |
|------|-------------|
| `begin_session` | Register as an agent + start a session atomically |
| `end_session_full` | End session + unregister atomically |
| `whoami` | What agent am I? What session? What files do I own? |
| `catch_me_up` | What happened while I was away? Recent activity, notes, dead agents |
| `swarm_awareness` | Who else is working here? All agents, sessions, file claims |
| `file_heat` | Which files are agents fighting over? Pheromone-based contention map |
| `talk_to_agent` | Send a direct message to a specific fleet agent by name |
| `claim_port` | Get a deterministic port for a service identity |
| `add_note` | Leave an immutable breadcrumb (notes can never be deleted) |
| `acquire_lock` | Distributed lock for critical sections |
| `spawn_agent` | Launch a background AI agent with a task |
| `fleet_init` | Set up a background agent fleet with git hooks and pd-fleet.yml |
| `pd_discover` | Find additional tools by category |

**Tuple space tools (shared swarm memory):**

| Tool | What It Does |
|------|-------------|
| `tuple_out` | Write a typed tuple to the shared space (harbor-scoped) |
| `tuple_read` | Read tuples matching a pattern (non-destructive) |
| `tuple_take` | Atomically read + remove tuples matching a pattern |
| `tuple_scan` | List all tuples in a harbor or global space |
| `tuple_count` | Count tuples matching a pattern |

**Discover more tools by category:**
Call `pd_discover` with a category name: `magic`, `session-lifecycle`, `ports`, `sessions`, `notes`, `locks`, `messaging`, `agents`, `inbox`, `webhooks`, `integration`, `dns`, `briefing`, `tunnels`, `projects`, `changelog`, `activity`, `system`, `tuples`, `pheromone`

**Integration signals:** Use `integration ready` and `integration needs` to coordinate service dependencies. When your service is ready, signal it so other agents can proceed.

## Core Concepts

### Semantic Identities: `project:stack:context`

Every service gets a semantic name. The name IS the port — deterministic hashing means the same identity always maps to the same port. Identities are indexed in an in-memory **Adaptive Radix Tree** for O(k) lookups (where k is key length), replacing SQL LIKE scans.

```bash
pd claim myapp:api:main           # Always gets port 3142 (or whatever hash gives)
pd claim myapp:api:feature-auth   # Different port, same project
pd find 'myapp:*'                 # Prefix search — resolves through the trie, not SQL
pd find 'myapp:*:main'            # Wildcard — all stacks with context "main"
```

### Sessions & Notes

Sessions track what each agent is doing. Notes are **immutable** — once written, they can never be edited or deleted. This creates an audit trail that agents and humans can trust. Notes are **encrypted at rest** with AES-256-GCM (master key at `~/.port-daddy/master.key`, auto-generated on first boot).

```bash
pd begin --identity myapp:api --purpose "Building auth"
pd note "Found SQL injection in token validation"
pd note "Patched. Tests green."
pd done
```

### Salvage (Dead Agent Recovery)

When an agent crashes, its session enters the salvage queue. Another agent can claim and continue the work:

```bash
pd salvage --project myapp        # See dead agents' context
pd salvage claim dead-agent-42    # Pick up their work
```

**IMPORTANT:** Always check `pd salvage` at the start of a session. You might be able to continue where a crashed agent left off instead of starting from scratch.

### File Claims (Advisory)

```bash
pd session files claim src/auth/*.ts
# Another agent tries the same file:
pd session files claim src/auth/login.ts
# → CONFLICT: claimed by agent 'myapp:api'
```

Claims are advisory — they warn, don't lock. Hard locks cause deadlocks. Advisory claims cause conversations.

### Pub/Sub Messaging

Agents signal each other through channels:

```bash
# Agent A finishes database setup
pd pub myapp:events "database-ready"

# Agent B was watching
pd watch myapp:events --exec "npm run migrate"
```

### Distributed Locks

For operations that truly must be exclusive:

```bash
pd with-lock deployment -- npm run deploy
# Or manually:
pd lock db-migration --ttl 300
pd unlock db-migration
```

## Binary IPC Protocol (v3.8.2)

High-frequency agent communication over a Unix domain socket with MessagePack encoding. The IPC channel sits alongside the HTTP API — agents that need low-latency communication (heartbeats, pheromone sprays, pub/sub publish) use IPC automatically when the daemon is running.

**Key properties:**
- **7-byte header**: `[type:1][conv_id:4][payload_len:2]` + MessagePack payload
- **70-80% bandwidth reduction** vs HTTP JSON
- **~3us latency** for fire-and-forget operations (vs ~200us HTTP)
- **13 FIPA performatives**: INFORM, REQUEST, QUERY_REF, REFUSE, FAILURE, NOT_UNDERSTOOD, SUBSCRIBE, UNSUBSCRIBE, etc.
- **Fire-and-forget**: heartbeats, pheromone sprays, pub/sub publish (conv_id=0)
- **Request-response**: claims, locks, sessions (conv_id for correlation)
- **Pub/sub subscriptions**: with dead-man cleanup on disconnect
- **Auto-reconnect**: client reconnects with subscription replay on socket drop
- **SDK fast paths**: `heartbeat()`, `pheromoneSpray()`, `publish()` auto-use IPC when available

**Socket location:** `~/.port-daddy/daemon.ipc`

**Security hardening:**
- Rate limiting: 500 frames/sec per connection
- Connection limit: 256 max (REFUSE for excess)
- 3-strike protocol violation budget (malformed frames disconnect)
- Backpressure via write queue + drain events
- Lock release on IPC disconnect

You don't need to use IPC directly. The SDK and CLI use it transparently for hot-path operations.

## Fleet: Background Agents (v3.8.0)

Declare agents in YAML. They fire on git commits, cron schedules, or pub/sub messages. Auto-respawn on crash with circuit breaker.

```bash
pd fleet init     # Creates pd-fleet.yml + git hook
pd fleet up       # Starts the fleet
git commit -m "fix auth"  # QA, docs, cartographer fire automatically
pd fleet status   # What is the fleet doing?
pd fleet down     # Stop the fleet
```

The starter fleet includes: **QA** (bug hunting), **Documentarian** (docs sync), **Cartographer** (roadmap tracking), **Spark** (idea generation), **Spider** (cross-feature connections).

```yaml
# pd-fleet.yml
fleet:
  name: myapp
  harbor: "{project}:fleet"
  agents:
    qa:
      trigger: git:committed        # React to pub/sub events
      respawn: true                  # Auto-restart on crash
      max_respawns: 3               # Circuit breaker
      backend: claude-cli
      allowedTools: "Read,Grep,Glob,Bash(npm test*)"
      prompt: "Review the last commit for bugs..."

    gardener:
      schedule: "*/10 * * * *"      # Or run on a cron schedule
      backend: custom
      prompt: "git status --porcelain"
      on_success: publish git:status  # Chain agents via channels

  channels:
    git:committed:
      description: "Fired after a successful commit"
      consumers: [qa]
```

**Key features:**
- Works with any LLM backend: `claude-cli`, `ollama`, `gemini`, `aider`, `custom`
- Template variables (`{project}`) resolve from the YAML context
- `on_success: publish <channel>` chains agents via pub/sub (DAG topology validated at startup)
- Fleet harbor auto-created on `pd fleet up` — all agents share a semantic namespace
- Each agent gets full PD coordination: registration, sessions, heartbeats, salvage on crash
- Auto-respawn with `respawn: true` and `max_respawns` circuit breaker

## Tuple Space: Shared Swarm Memory (v3.8.0)

Agents write typed tuples to a shared space. Other agents query by pattern. Based on Linda (Gelernter, 1985). Harbor-scoped for fleet isolation. TTL for auto-expiry.

```bash
# Spider writes a connection it discovered
pd tuple out '["connection", "trie+pubsub=routing", "spider", 0.9]' --harbor myapp:fleet

# Spark reads all connections with confidence > 0.7
pd tuple rd '["connection", "*", "*", ">0.7"]' --harbor myapp:fleet

# Take (remove) a processed task from the space
pd tuple in '["task", "build-auth", "pending"]'

# Scan all tuples in a harbor
pd tuple scan --harbor myapp:fleet

# Count tuples
pd tuple count --harbor myapp:fleet
```

Pattern matching: exact values, `*` wildcard, `>N`/`<N` numeric comparisons, `myapp:*` semantic identity prefixes.

**HTTP API:**
- `POST /tuples` — write a tuple (body: `{ tuple, harbor?, writtenBy?, ttl? }`)
- `GET /tuples` — read by pattern (query: `pattern`, `harbor`, `limit`)
- `DELETE /tuples` — take (destructive read) by pattern
- `GET /tuples/scan` — list all tuples in a harbor
- `GET /tuples/count` — count tuples

## Pheromone Trails: Ambient Signals (v3.8.0)

Agents spray numeric signals (0-1) onto entities. Signals decay exponentially over time at read, creating ambient awareness without polling.

```bash
# Spray a signal onto a service
pd pheromone spray --table services --id myapp:api --key urgency --strength 0.8

# Sniff pheromone values (applies read-time decay)
pd pheromone sniff --table services --id myapp:api

# View file heat map (which files are most contested)
pd pheromone files

# List all non-zero pheromone trails
pd pheromone list
```

Use cases: file contention detection, agent reputation scoring, hot-path identification, adaptive thresholds.

**HTTP API:**
- `POST /pheromone/spray` — set a pheromone value (body: `{ table, id, key, strength }`)
- `GET /pheromone/:table/:id` — read pheromone values (applies read-time decay)
- `GET /pheromone` — list all non-zero pheromones
- `GET /pheromone/files` — file heat map from session file claims (query: `path`, `depth`)

## The Arbiter: Runtime Invariant Enforcement (v3.8.0)

The Arbiter monitors every state transition against 6 formally-derived invariants from the TLA+ specification:

- **PID squatting** — no process can claim another's port
- **Capability escalation** — agents can't exceed declared capabilities
- **Note monotonicity** — notes are append-only, never deleted
- **Escrow positivity** — encrypted note escrow balances stay positive
- **Lock owner validity** — only the owner can release a lock
- **Heartbeat freshness** — stale agents get reaped

In strict mode, critical violations trigger man-overboard salvage.

```bash
pd arbiter status         # Check rules and violation count
pd arbiter violations     # List recorded violations
```

## Runtime File Locations (v3.8.2)

All runtime files live in `~/.port-daddy/` (not `/tmp/`). This eliminates symlink attacks, survives `/tmp/` cleanup, and keeps permissions user-private (0700 directory).

| File | Purpose |
|------|---------|
| `~/.port-daddy/daemon.sock` | HTTP Unix socket (CLI, SDK, MCP) |
| `~/.port-daddy/daemon.ipc` | Binary IPC socket (agent hot path) |
| `~/.port-daddy/daemon.pid` | PID file |
| `~/.port-daddy/daemon.port` | TCP port file (dashboard discovery) |
| `~/.port-daddy/master.key` | AES-256-GCM master key for note encryption |

Override via environment variables: `PORT_DADDY_SOCK`, `PORT_DADDY_IPC`, `PORT_DADDY_PORT_FILE`.

## CLI Quick Reference

| Command | Purpose |
|---------|---------|
| **Session Lifecycle** | |
| `pd begin` / `pd done` | Start/end session (agent registration included) |
| `pd whoami` | Current agent and session context |
| `pd note` / `pd notes` | Write/read immutable notes |
| **Port Management** | |
| `pd claim` / `pd release` | Claim/release deterministic ports |
| `pd find` | Wildcard service search (trie-accelerated) |
| **Coordination** | |
| `pd lock` / `pd unlock` | Distributed locks |
| `pd with-lock` | Run command under lock with auto-release |
| `pd pub` / `pd watch` | Pub/sub messaging |
| `pd session files claim` | Advisory file claims |
| **Fleet & Agents** | |
| `pd fleet init` | Create pd-fleet.yml + git hook |
| `pd fleet up/down/status` | Start/stop/inspect the fleet |
| `pd spawn` / `pd spawned` | Launch/list background agents |
| `pd spawn kill` | Kill a spawned agent |
| `pd salvage` | Dead agent recovery |
| **Swarm Memory** | |
| `pd tuple out/rd/in` | Write/read/take tuples |
| `pd tuple scan/count` | List/count tuples |
| `pd pheromone spray` | Set ambient signal on an entity |
| `pd pheromone sniff` | Read pheromone values (with decay) |
| `pd pheromone list` | List all non-zero pheromones |
| `pd pheromone files` | File heat map |
| **System** | |
| `pd status` | Daemon health |
| `pd version` | Version and code hash |
| `pd arbiter status` | Invariant enforcement status |
| `pd arbiter violations` | List recorded violations |
| `pd dev start/stop/status` | Isolated dev daemon (port 9877) |

## Decision Matrix: Which Tool When

| Problem | Solution |
|---------|----------|
| Dev server port conflict | `pd claim myapp:api -q` |
| Need to coordinate with other agents | `pd begin` + `pd session files claim` |
| Agent-to-agent signaling | `pd pub` + `pd watch` |
| Direct message to a specific agent | `talk_to_agent` MCP tool or `pd inbox send` |
| Background automation | `pd fleet init` + `pd fleet up` |
| Share knowledge across agents | `pd tuple out` / `pd tuple rd` |
| Track "hotness" of resources | `pd pheromone spray` / `sniff` |
| See file contention at a glance | `file_heat` MCP tool or `pd pheromone files` |
| Crashed agent left work behind | `pd salvage` |
| Exclusive operations (deploys, migrations) | `pd with-lock` |
| What happened while I was away? | `catch_me_up` MCP tool |
| Who else is working right now? | `swarm_awareness` MCP tool |
| Check for invariant violations | `pd arbiter status` |

## Common Issues

### Port Daddy daemon not running
**Symptom:** `Connection refused` on any pd command
**Fix:** `pd start` or `pd install` (installs as launchd service, auto-starts on login)

### Port already claimed
**Symptom:** You get a port but it's the "wrong" one
**This is correct behavior.** Same identity = same port, always. If you need a different port, use a different identity context: `myapp:api:feature-x` instead of `myapp:api:main`.

### Session already active
**Symptom:** `pd begin` says a session exists
**Fix:** Call `pd whoami` to see the current session. Either `pd done` the old one or continue working in it.

### File claim conflicts
**Symptom:** Another agent claimed files you need
**Fix:** This is the system working. Check `pd swarm_awareness` to see who owns what. Coordinate via `pd pub` or work on different files.

### IPC connection failures
**Symptom:** IPC-related errors in logs
**Fix:** The SDK falls back to HTTP automatically. IPC is an optimization, not a requirement. Check that `~/.port-daddy/daemon.ipc` exists and has correct permissions (should be user-only, created by the daemon).

## Quality Gates

Before declaring "done" on any PD-mediated work:

- The agent registered an identity (`pd whoami` returns one).
- File claims match the files actually edited.
- At least one `progress` note per primitive milestone.
- A `handoff` note exists if the work is ending mid-stream (salvage-friendly).
- `pd done` was called — leaving sessions open is the most common dogfooding violation.
