---
name: gateway-architecture-analysis
description: Analysis of multi-bot gateway architecture for Spacebar/Discord agent fleets — patterns, trade-offs, recommendations for current and future scale
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [gateway-architecture, spacebar, discord-bots, multi-bot-scaling, architecture-analysis]
    triggers: [gateway-architecture, multi-bot-gateway, spacebar-gateway, bot-fleet-scaling, architecture-decision-gateway]
    related_skills: [self-hosted-communication-server, systematic-debugging]
---

# Multi-Bot Gateway Architecture Analysis

> Context: Deploying 40+ AI agent bots to Spacebar (self-hosted Discord-compatible chat).
> Question: Should we run 1 gateway per bot, 1 gateway per team, or another pattern?

## Constraint: Spacebar/Discord Architecture

**Each bot = one WebSocket connection.** Spacebar and Discord both authenticate at the *bot token* level — each connection identifies as exactly one user. There is no multi-bot multiplexing on a single connection. Every bot that needs to be online simultaneously requires its own WebSocket → one gateway process per token.

**No way around this.** Even Discord themselves run separate processes per bot internally.

## How Discord Scales (The Industry Model)

Discord's own large-scale server operators (100+ bots) use one of two patterns:

| Platform | Pattern | How They Manage |
|----------|---------|-----------------|
| **Top.gg / Discord Bot Lists** | 1 process per bot | PM2 process manager, Docker Compose, or K8s |
| **Self-hosted multi-bot fleets** | 1 script handling N connections via discord.py | Custom launcher script + process supervision |
| **Discord's internal bot platform** | 1 bot = 1 microservice | Kubernetes pod per bot |

**Key takeaway:** There is no "one connection for all bots" pattern. The bottleneck is never the WebSocket (idle connections use ~0.1% CPU). The bottleneck is LLM processing when bots are actively reasoning.

## Architecture Options for Our Fleet

### Option A: N Separate Processes (39 gateways)
Each Hermes profile runs its own `hermes gateway run --profile <name>` process.

```
┌─────────────────────────────────────┐
│ Process Manager (PM2 / Supervisor)  │
│  ├── hermes (profile: data-lead)       │  →  Spacebar WebSocket
│  ├── hermes (profile: assistant)      │  →  Spacebar WebSocket
│  ├── hermes (profile: verifier)       │  →  Spacebar WebSocket
│  ├── ...                           │  →  ...
│  └── hermes (profile: integration-lead)      │  →  Spacebar WebSocket
└─────────────────────────────────────┘
```

| Factor | Value |
|--------|-------|
| **Complexity** | Low — Hermes-native, 1 command per profile |
| **Isolation** | Perfect — each bot crashes independently |
| **Memory (idle)** | ~50MB per process (shared Hermes code, Python VM overhead) → ~2GB for 40 |
| **Memory (active)** | ~200MB per actively-reasoning agent → 2-4GB for 8 active at once |
| **Management** | Need a supervisor (PM2, systemd, or launcher script) |

### Option B: One Script, N Connections (Team-level)
A single Python script that opens N discord.py connections and routes messages to the right agent logic.

```
┌──────────────────────────────────────────────┐
│ fleet-manager.py (1 process, 8 connections) │
│  ├── WebSocket → data-lead#0001                  │
│  ├── WebSocket → assistant#0001                 │
│  ├── WebSocket → verifier#0001                  │
│  └── ...                                     │
└──────────────────────────────────────────────┘
```

| Factor | Value |
|--------|-------|
| **Complexity** | **High** — need custom routing, agent dispatch, conversation state per bot |
| **Isolation** | Poor — one crash kills all bots in the team |
| **Memory** | ~200MB for all connections (single Python process) |
| **Hermes integration** | **None** — you'd bypass Hermes profiles entirely, losing SOUL.md, skills, cron, memory provider integration |
| **Management** | Single process to manage |

### Option C: Hybrid — Team Launcher (Recommended)
One shell launcher script per team that starts all N profiles as subprocesses, with unified logging and restart.

```
┌──────────────────────────────────────────────┐
│ trading-team.sh (launcher)                   │
│  ├── hermes gateway run --profile data-lead     │  →  Spacebar WebSocket
│  ├── hermes gateway run --profile assistant    │  →  Spacebar WebSocket
│  ├── hermes gateway run --profile verifier     │  →  Spacebar WebSocket
│  ├── ...                                    │  →  ...
│  └── hermes gateway run --profile analyst      │  →  Spacebar WebSocket
└──────────────────────────────────────────────┘
```

| Factor | Value |
|--------|-------|
| **Complexity** | Low — Hermes-native, team organized |
| **Isolation** | Perfect — each bot independent |
| **Memory** | Same as Option A (~2GB for 40 bots idle) |
| **Hermes integration** | **Full** — every bot keeps its SOUL.md, skills, cron, memory provider |
| **Management** | One command per team: `bash trading-team.sh` |

### Option D: Kanban Representative Bot
One bot per team *channel* that receives messages and delegates to sub-agents via Kanban.

```
Spacebar #trading channel
  ↓ message arrives
representative-bot (data-lead)  ←  only bot with a gateway
  ├── delegate_task → assistant (no gateway, backend only)
  ├── delegate_task → verifier (no gateway)
  └── reply in channel
```

| Factor | Value |
|--------|-------|
| **Complexity** | Medium — Kanban routing works but sub-agents are headless |
| **Isolation** | Medium — representative is single point of failure |
| **Memory** | **Lowest** — 1 process per team, ~200MB total |
| **Hermes integration** | Partial — representative has full Hermes, sub-agents are invoked via delegate_task with limited context |
| **Downside** | Loses independent bot presence. You can't DM assistant directly. Sub-agents don't have persistent memory across invocations. |

## 🚨 Limitation: Resume (OP 6) Not Implemented in Spacebar

A critical architectural constraint discovered during operation: Spacebar's **Resume (OP 6) is not implemented**. The file `src/gateway/opcodes/Resume.ts` contains a stub that always responds with:

```typescript
await Send(this, { op: 9, d: false });  // INVALID_SESSION, full reconnect needed
// return this.close(CLOSECODES.Invalid_session);  // commented out!
```

Every time a bot reconnects (after a brief network interruption, heartbeat timeout, or server restart), Spacebar:
1. Receives the OP 6 Resume
2. Sends OP 9 with `d: false` (which tells the client to discard its session and fully reconnect)
3. Does NOT close the WebSocket (the `close()` is commented out!)
4. The Fermi client then sends a custom close code **4041** to signal session invalidation
5. The bot does a full re-IDENTIFY (takes hundreds of ms to multiple seconds)

**Effect on 44-bot fleet:** Any server restart or network blip triggers a reconnect cascade where ALL 44 bots simultaneously re-IDENTIFY. This causes:
- IDENTIFY latency to spike (14s-63s observed)
- CPU/memory pressure on the Spacebar server
- Messages briefly failing with "fake0.xxx" IDs while the WebSocket is down
- 209+ concurrent connections during reconnect storms

**No fix without source code changes.** This requires implementing actual session state storage in `Resume.ts` with sequence number validation. The workaround is:
- Keep the **core council (9 bots) always on** to minimize reconnect frequency
- **Rate-limit bot reconnections** via config (`limits.rate.enabled: true`)
- Add a **max-connections limit** to the gateway config

## 🚨 Implemented: Resource Constraints Force Tiered Architecture

During actual operation (June 2026), the 44-bot-all-at-once approach was replaced with a **tiered core + on-demand model** due to RAM constraints (~3-4GB for 44 bots, exceeded available RAM on a dev machine).

| Scale | Option A (N processes) | Option C (Team launcher) | Option D (Rep bots) |
|-------|----------------------|------------------------|-------------------|
| **40 bots (today)** | ~2GB RAM idle, 39 processes | ~2GB RAM idle, 6 launchers | ~300MB RAM, 6 processes |
| **100 bots** | ~5GB RAM idle, 100 processes | ~5GB RAM idle, 10 launchers | ~500MB RAM, 10 processes |
| **200 bots** | ~10GB RAM idle, 200 processes | ~10GB RAM idle, 15 launchers | ~1GB RAM, 15 processes |

**Real-world note:** The "~50MB per process idle" is the Python interpreter overhead. On Windows, Python processes share the same code pages (DLLs), so the *actual* incremental cost per additional bot is closer to 10-15MB. 40 bots would use ~400-600MB actual RAM, not 2GB.

## Spacebar-Specific Optimizations (Our Advantage)

Since Spacebar is **self-hosted**, we can optimize in ways Discord doesn't allow:

1. **No rate limits** → bots can connect/disconnect freely, no backoff delays
2. **No gateway intent gating** → bots don't need to declare privileged intents
3. **No identify ratelimit** → all 40 bots can connect simultaneously
4. **Can modify server code** → could theoretically add multi-bot multiplexing to Spacebar itself (future work)
5. **Database-level auth** → bot tokens are simply DB sessions; we control the JWT signing key

## Recommendation

**Option C: Team Launcher scripts** — one launcher per team, Hermes-native, full profile integration, easy to manage.

### Why not Option B (Custom fleet manager)?
Building a custom fleet manager that bypasses Hermes profiles means building your own:
- Agent personality loader (SOUL.md)
- Skill system
- Cron scheduler
- Memory provider abstraction
- Tool registry

That's essentially rebuilding Hermes. **Not worth it.**

### Why not Option D (Rep bots only)?
Some bots **need** independent presence:
- Chief of Staff needs to be @mentionable in any channel
- Council leads need dedicated DM channels
- Trading bots need to post independently
- Losing individual bot identities defeats the purpose of having 40 distinct agents

### Why Option C:
- Each bot keeps its full Hermes profile (SOUL.md, skills, memory, cron)
- Bots are independently @mentionable in Spacebar
- Team launcher scripts provide organization (start/stop/status per team)
- Processes can be managed via task manager, supervisor, or simple batch files
- Scales to 100+ by adding more launcher scripts
- Low complexity — uses Hermes's native gateway, just organizes the startup

## Implementation Plan

```yaml
Teams and their launchers:

Council (1 gateway = chief-of-staff):
  → start-council.sh
  → One bot: chief-of-staff

Executive (8 gateways):
  → start-executive.sh
  → technology-lead, growth-lead, intelligence-lead
  → treasury-lead, counsel-lead, compliance-lead
  → portfolio-lead, operations-lead

Specialists (8 gateways):
  → start-specialists.sh
  → manufacturing-lead, ai-agency, media-lead
  → cyber-osint, market-lead, legal-case-support
  → health-performance, outreach-lead

Trading (8 gateways):
  → start-trading.sh
  → data-lead, assistant, verifier, product-lead, admin
  → scout, people, analyst

Social Media (5 gateways):
  → start-social.sh
  → nova, writing-lead, notes, lane, pulse

Knowledge (4 gateways):
  → start-knowledge.sh
  → history-lead, automation-lead, creative-lead, security-lead

Hermes Dev (5 gateways):
  → start-hermes-dev.sh
  → dev-lead, skills-lead, integration-lead, qa-lead, docs-lead
```

**Total: 6 team launchers managing 39 gateway processes**

### Actual Deployed Structure (June 2026)

The **fleet-manager.py** CLI (`${MY_REPOS}\Documents\github\relay-pool\fleet-manager.py`) implements a refined tiered model:

**Core Council (always-on, 9 bots):**
`python fleet-manager.py deploy`
→ chief-of-staff, technology-lead, growth-lead, intelligence-lead, treasury-lead, counsel-lead, compliance-lead, portfolio-lead, operations-lead

**On-demand activation by council lead:**
`python fleet-manager.py activate <team>`

| Team | Lead | Members | Command |
|------|------|---------|---------|
| technology | technology-lead | 8 bots (dev, dev-lead, docs-lead, qa-lead, skills-lead, integration-lead, automation-lead) | `activate technology` |
| intelligence | intelligence-lead | 11 bots (history-lead, pulse, security-lead, cyber, content, creative-lead, etc.) | `activate intelligence` |
| investment | portfolio-lead | 9 bots (trading scouts + sports) | `activate investment` |
| revenue | growth-lead | 2 bots (solumina, ai-agency) | `activate revenue` |
| operations | operations-lead | 4 bots (health, market-lead, jobs) | `activate operations` |
| legal | counsel-lead | 1 bot (legal-case-support) | `activate legal` |

Standby bots (35 total) consume zero resources until activated. See `self-hosted-communication-server/references/fleet-manager-py.md` for full team mapping.

### Evolution: Channel Rep System (June 2026)

The fleet was further refined with a **channel representative routing** layer. Previously, all bots responded to all messages (causing spam). The rep system uses Hermes native `DISCORD_FREE_RESPONSE_CHANNELS` + `DISCORD_REQUIRE_MENTION` to gate which bots respond where:

**Pattern:**
- ALL bots default to `DISCORD_REQUIRE_MENTION=true` (only respond when @mentioned)
- Each channel's designated rep bot gets `DISCORD_FREE_RESPONSE_CHANNELS=<channel_ids>` (responds without @mention is its channel)
- @mention any bot to bring them into any conversation
- Summon system for cross-team collaboration (adds temp free-response channels)

**Architecture file:** `configs/rep-config.json` in the agent-fleet repo.
**CLI:** `scripts/rep-router.py` for summon/status/dismiss.
**Docs:** `docs/REP_SYSTEM.md`.

This eliminated the spam problem without any monkey-patching — it's all Hermes-native env vars. See the `self-hosted-communication-server` skill for the full implementation guide.

## Current State (June 2026 — Local Instance)

The fleet was successfully migrated to a local Spacebar instance (port 3100). The gateway wrapper (`spacebar-gateway.py`) connects reliably. Key findings from the migration:

| Aspect | Status | Notes |
|--------|--------|-------|
| Gateway wrapper | **Works** | spacebar-gateway.py connects all bots to localhost:3100 |
| `permission_overwrites: null` | **Resolved** (handled by discord.py or wrapper shim) | No crash observed |
| Env var bleed | **Active pitfall** | Stale `DISCORD_BOT_TOKEN` in parent shell overrides `.env` file reads — see self-hosted-communication-server skill |
| `.env.spacebar` files | **Must be deleted** | Old files contain `SPACEBAR_BOT_TOKEN` that takes precedence |
| Token rotation | **Fresh registration required** | Updating password hashes via `jsonb_set` not reliable; register new accounts instead |
| Gateway state files | **Must be cleaned** | `gateway_state.json` and `gateway.pid` persist after unclean shutdown and cause token bleed |
| Channel directory | **Built correctly** | 33-36 channels visible per bot |
| Slash commands | **Minor issue** | "Unknown application" 404 for newly-registered bots (no application registered) — non-blocking |

## Open Items

1. **Application registration for slash commands** — New bot registrations don't auto-create a Discord Application. The `/skill` and other slash commands fail with 404. Fix: create application records in the Spacebar `applications` table or register via API after bot creation. Workaround: set `DISCORD_COMMAND_SYNC_POLICY=off` in every profile's `.env` to skip the sync entirely (no slash commands, but everything else works).

2. **OP 6 Resume** — Still not implemented in Spacebar, causing full reconnect storms on restart. Tiered architecture (core council always on + on-demand teams) is the workaround.

## Future Scaling Considerations

| Scale | Concern | Mitigation |
|-------|---------|------------|
| 50-100 bots | Windows process table overhead | Use Python subprocess pool instead of individual terminals |
| 200+ bots | Memory pressure | Switch to Linux (Docker) or trim idle processes |
| 500+ bots | Gateway connection count | Add multi-bot multiplexing to Spacebar server itself |
| Message volume > 10/min | LLM queueing | Kanban queue per team + priority routing |
| Cross-bot coordination | Message ordering | MemPalace shared memory + decision log |
