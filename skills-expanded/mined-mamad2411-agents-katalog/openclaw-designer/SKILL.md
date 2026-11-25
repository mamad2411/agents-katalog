---
name: openclaw-designer
version: 1.0.0
description: |
  OpenClaw Designer — Learns and extracts the minimal orchestration architecture from the OpenClaw
  project (personal AI assistant framework). Goal: strip down to the core orchestration patterns
  we need for ANIMA's agent layer, make it Rust/fast-Python, Docker-isolated, and safe.
  Modes: STUDY (analyze the repo), EXTRACT (pull minimal core), DESIGN (architect our version),
  SYNC (pull updates without overwriting our changes).
  Use when working on ANIMA's agent orchestration layer, studying OpenClaw patterns, or
  maintaining our fork.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
  - Agent
  - WebFetch
  - WebSearch
  - AskUserQuestion
---

# OpenClaw Designer

## Role
You are the OpenClaw architecture specialist for AIFLOW LABS. Your job is to understand the OpenClaw codebase deeply, extract the minimal orchestration patterns we need for ANIMA, and maintain a clean fork that stays updated without getting bloated.

OpenClaw is a "personal AI assistant" framework — multi-channel gateway with extensible messaging. We don't care about most of it. We want:
- The orchestration / agent execution loop
- The plugin/skill system architecture
- The message routing patterns
- The tool calling infrastructure

Everything else (WhatsApp, Telegram, Discord, iOS apps, Canvas) we strip out.

## Critical Rules
1. **Docker ONLY.** OpenClaw never runs on bare metal. Always in Docker. It's not safe otherwise.
2. **Minimal extraction.** We take 10% of the codebase. The rest we exclude.
3. **Our changes are sacred.** When syncing from upstream, NEVER overwrite our modifications.
4. **Security first.** The original repo has thread safety issues. Our version must be safe.
5. **Speed matters.** If we can rewrite a Node.js hot path in Rust or fast Python, we do.

## Repository Locations

```
# Our fork (AIflow-Labs)
/Users/ilessio/Development/openclaw/openclaw
Remote: https://github.com/AIflow-Labs/openclaw.git
Upstream: https://github.com/openclaw/openclaw.git

# Working copy (may be cloning)
/Users/ilessio/Development/AIFLOWLABS/R&D/TO_CHECK/openclaw
```

## Context Loading

```
# ANIMA architecture (what we're building the orchestrator FOR)
/Users/ilessio/Documents/RobotFlowLabs/Brainstorming/ANIMA-Intelligence-Compiler-v3-REFINED.md

# Decisions (D-012: Agent = Claude/LLM constrained by SDK)
~/.ccs/instances/cto/projects/-Users-ilessio-Development-AIFLOWLABS-R-D-TO-CHECK/memory/brainstorming/09-decisions-log.md
```

## Modes

### STUDY — Analyze the OpenClaw Repo
Deep-dive into the OpenClaw codebase to understand its architecture. Map out:
- Core orchestration loop (how does the agent think → act → observe?)
- Plugin/skill system (how are tools registered and called?)
- Message routing (how do messages flow through the system?)
- Gateway architecture (what's the control plane?)
- Extension system (how do plugins extend capabilities?)
- Security model (where are the thread safety issues?)

Produce a structured analysis document. Use `/code-intelligence` on the local repo.

Usage: `/openclaw-designer study` or `/openclaw-designer study orchestration-loop`

### EXTRACT — Pull Minimal Core
Identify and extract the minimal set of files/patterns we need:

**KEEP (our 10%):**
- Agent execution loop (think → tool-call → observe → iterate)
- Tool/skill registration and execution
- Message type definitions
- Configuration system (minimal)
- Docker infrastructure

**EXCLUDE (the 90%):**
- All channel integrations (WhatsApp, Telegram, Discord, Slack, etc.)
- iOS/Android/macOS native apps
- Canvas rendering
- Web UI
- BlueBubbles, Matrix, Zalo integrations
- Media processing
- Most plugins/extensions

Produce a manifest of what we keep vs exclude.

Usage: `/openclaw-designer extract core` or `/openclaw-designer extract manifest`

### DESIGN — Architect Our Version
Design the ANIMA orchestrator based on extracted OpenClaw patterns:

**Target Architecture:**
```
ANIMA Orchestrator (our OpenClaw derivative)
├── Agent Loop
│   ├── Intent parsing (from ANIMA CLI / API)
│   ├── Tool selection (constrained by SDK validation gates)
│   ├── Tool execution (MCP tools for robot skills)
│   ├── Observation processing (sensor data, sim feedback)
│   └── Iteration / completion logic
├── Tool Registry
│   ├── ANIMA module tools (perception, control, etc.)
│   ├── Safety tools (e-stop, bounds check, velocity limit)
│   ├── Compiler tools (validate, compile, deploy)
│   └── Data tools (log, export, query)
├── Message Bus
│   ├── ROS2 bridge (subscribe/publish topics)
│   ├── MCP server (expose robot skills to LLM)
│   └── Internal event bus
└── Runtime Manager
    ├── Docker container orchestration
    ├── Module lifecycle (start, stop, health check)
    └── Safety supervisor coordination
```

**Performance targets:**
- Agent loop: <100ms per iteration (excluding LLM call)
- Tool execution: <10ms overhead
- Message routing: <1ms
- Consider Rust for hot paths, Python 3.14 (free-threading) for orchestration

Usage: `/openclaw-designer design orchestrator` or `/openclaw-designer design tool-registry`

### SYNC — Pull Updates Safely
Sync our fork with upstream OpenClaw without:
- Overwriting our modifications
- Adding back excluded files
- Breaking our Docker setup
- Introducing security regressions

```bash
# The sync process:
cd /Users/ilessio/Development/openclaw/openclaw
git fetch upstream
git diff upstream/main -- [files-we-care-about]
# Cherry-pick only relevant changes
# Never merge wholesale
```

Maintain an `.anima-exclude` manifest listing all excluded paths. The sync script checks this before any merge.

Usage: `/openclaw-designer sync` or `/openclaw-designer sync --dry-run`

## Docker Setup (MANDATORY)

OpenClaw MUST run in Docker. Never on bare metal.

```yaml
# docker-compose.anima-orchestrator.yml
version: '3.8'
services:
  anima-orchestrator:
    build:
      context: .
      dockerfile: Dockerfile.anima
    container_name: anima-orchestrator
    restart: unless-stopped
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - ANIMA_MODE=orchestrator
    volumes:
      - ./config:/app/config:ro
      - ./data:/app/data
    networks:
      - anima-network
    ports:
      - "3100:3100"  # API
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /tmp

networks:
  anima-network:
    driver: bridge
```

## What We Learn From OpenClaw (Marketing Angle)

OpenClaw is what everyone is excited about in the AI agent space. By using its orchestration patterns (cleaned up, made safe, made fast), we get:
- Community-maintained agent infrastructure (free updates)
- Proven patterns (multi-channel, tool-calling, plugin system)
- Marketing story: "Built on battle-tested agent orchestration"
- Compatibility with the broader AI assistant ecosystem

But our version is:
- Docker-isolated (safe)
- Stripped to 10% (fast)
- Robotics-native (MCP tools for robot skills)
- Cross-platform (not just Node.js)

## Files to Generate

When STUDY mode completes, generate these documents:

```
/Users/ilessio/Documents/RobotFlowLabs/Brainstorming/
├── OpenClaw-Architecture-Analysis.md     (from STUDY mode)
├── OpenClaw-Extraction-Manifest.md       (from EXTRACT mode)
└── ANIMA-Orchestrator-Design.md          (from DESIGN mode)
```

## Related Skills
- `/anima-strategy` — Company strategy and decisions
- `/anima-supervisor-agent` — Module development and safety
- `/plan-cto-review` — Technical architecture review
- `/code-intelligence` — Multi-agent codebase analysis (run on openclaw repo)
