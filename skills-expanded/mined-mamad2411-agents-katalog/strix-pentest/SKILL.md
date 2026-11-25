---
name: strix-pentest
description: Autonomous AI penetration testing methodology — multi-agent orchestration, skill injection, scan modes, and tool integration patterns for security testing
---

# Strix — Autonomous AI Pentesting Skill

## Overview

Pattern for running AI-driven penetration tests. Multi-agent hierarchy: root orchestrator delegates to specialist agents, each with 1-5 domain skills. Agents run in sandboxed Docker with shared filesystem, proxy, and notes.

Source: [usestrix/strix](https://github.com/usestrix/strix) · Apache 2.0

---

## 1. Agent Orchestration

### Hierarchy

```
Root Agent (orchestrator, not tester)
├── Discovery Agent (surface mapping)
├── Validation Agent (PoC per finding)
├── Reporting Agent (vuln report + remediation)
└── [Whitebox only] Fixing Agent (patch generation)
```

- **Root**: coordinates, delegates, tracks todos/notes, monitors graph, writes final report. Never tests directly.
- **Children**: one job per agent. Spawn reactively as surfaces discovered, not upfront.
- **Blackbox chain**: Discovery → Validation → Reporting (3 agents/vuln)
- **Whitebox chain**: + Fixing (4 agents/vuln)

### Agent Creation

- Single factory function handles root and child. Differ only in `is_root` flag.
- **Root gets**: base tools + `finish_scan` lifecycle tool
- **Child gets**: base tools + `agent_finish` lifecycle tool
- **Base tools** (~30): think, load_skill, todos CRUD, notes CRUD, web_search, vuln reporting, proxy tools, agent graph tools (create_agent, send_message, wait_for_message, stop_agent)
- **Sandbox tools**: shell + filesystem (emitted by SDK capabilities, bound to Docker session)

### Lifecycle Control

- Agent loop only terminates when lifecycle tool returns `{"success": true}`
- All other tool results keep agent in loop
- Interactive mode: message without tool call HALTS execution
- Autonomous mode: text-only turn invalid, must use lifecycle tools to terminate
- Budget stop: broadcast wakes all parked agents for clean exit
- Crash: parent notified via `[Agent crash]` message

### Coordinator State

```
statuses:    running | waiting | completed | stopped | crashed | failed
parent_of:   child_id → parent_id
metadata:    task + skills per agent
runtimes:    SDK Session + asyncio Task + stream + wake Event
```

- All mutations behind async lock
- Atomic JSON snapshot on every state change → enables resume
- Message passing: append to target's SDK Session, increment pending, set wake Event

---

## 2. Skill System

### Format

```yaml
---
name: skill-name
description: One-line description
---

# Skill Title

## Attack Surface
...
## Key Vulnerabilities
...
## Testing Methodology
...
## Validation
...
```

- YAML frontmatter: `name` + `description` only
- Body: markdown, free structure but follows consistent section pattern
- File location: `skills/<category>/<name>.md`

### Categories

| Category | Purpose |
|----------|---------|
| `vulnerabilities` | Auth bypass, business logic, race conditions, SQLi, SSRF, etc. |
| `frameworks` | Django, Express, FastAPI, Next.js specific testing |
| `technologies` | Supabase, Firebase, Auth0, payment gateways |
| `protocols` | GraphQL, WebSocket, OAuth |
| `tooling` | CLI playbooks: nmap, nuclei, httpx, ffuf, sqlmap, etc. |
| `cloud` | AWS, Azure, GCP, Kubernetes |
| `reconnaissance` | Attack surface mapping, enumeration |
| `custom` | Community-contributed, source-aware SAST |

Internal (not user-selectable): `scan_modes`, `coordination`

### Skill Resolution Order

1. Caller-requested skills
2. `scan_modes/<mode>` — always injected
3. `tooling/agent_browser` — always (shell + browser CLI)
4. `tooling/python` — always (Python via exec_command)
5. `coordination/root_agent` — root only
6. Whitebox: `coordination/source_aware_whitebox` + `custom/source_aware_sast`

All deduped. Max 5 skills per agent.

### Injection

- Skills loaded → frontmatter stripped → body passed as template vars
- Rendered into `<skill_name>body</skill_name>` XML blocks in system prompt
- On-demand: `load_skill` tool returns body inline as tool result
- Permanent: pass `skills=[...]` to `create_agent`

---

## 3. Scan Modes

### Quick — "Bug bounty hunter going for quick wins"

- Time-boxed, breadth over depth
- Phase 1: rapid orientation (whitebox: git diffs + fast semgrep; blackbox: map auth/critical flows)
- Phase 2: high-impact priority — auth bypass → access control → RCE → SQLi → SSRF → secrets
- Phase 3: minimal PoC validation
- Skips: exhaustive enumeration, full bruteforcing, low-severity, theoretical issues
- Chaining: one high-impact pivot max

### Standard — "Balanced, systematic"

- 5 phases: Recon → Business Logic → Systematic Testing → Exploitation → Reporting
- Whitebox: semgrep + AST + trivy/gitleaks/trufflehog
- Blackbox: full crawl + tech fingerprint + proxy capture
- Tests: input validation, auth/session, access control (horizontal+vertical), business logic
- Every finding → working PoC
- Chaining: "if X works, what enables next?" — complete end-to-end paths

### Deep — "Relentless. Creative. Patient."

- 6 phases: Exhaustive Recon → Business Logic Deep Dive → Comprehensive Attack Surface → Vulnerability Chaining → Persistent Testing → Comprehensive Reporting
- Business logic: storyboard, state machines, invariants
- Attack surface: every input × every technique
- Chaining: cross-component (user→admin, external→internal, read→write)
- Persistent: alternative techniques, edge cases, revisit with new info
- Agent strategy: decompose hierarchically, massive parallel swarm, one vuln type per agent

---

## 4. Tool Integration

### Host-Side Tools (function tools)

| Tool | Purpose |
|------|---------|
| `think` | Private CoT, no side effects |
| `load_skill` | Load skill markdown on-demand |
| `web_search` | Perplexity sonar-reasoning-pro, security-focused |
| `create_vulnerability_report` | CVSS calc, dedup, fix_before/fix_after PR suggestions |
| `create_todo` / `list_todos` / `update_todo` / `mark_todo_done` / `delete_todo` | Per-agent, persisted to todos.json |
| `create_note` / `list_notes` / `get_note` / `update_note` / `delete_note` | Scan-wide, persisted to notes.json |
| `create_agent` | Spawn child with task + skills |
| `send_message_to_agent` | Inter-agent communication |
| `wait_for_message` | Block until response or timeout |
| `stop_agent` | Cancel agent |
| `view_agent_graph` | See current agent tree |
| `finish_scan` | Root-only lifecycle terminator |
| `agent_finish` | Child-only lifecycle terminator |

### Proxy Tools (Caido integration)

| Tool | Purpose |
|------|---------|
| `list_requests` | Browse captured HTTP traffic |
| `view_request` | Inspect full request/response |
| `repeat_request` | Replay with modifications |
| `list_sitemap` | View discovered endpoints |
| `view_sitemap_entry` | Inspect sitemap detail |
| `scope_rules` | View/manage scan scope |

### Sandbox Tools (Docker-bound)

- `shell` — command execution in container
- `filesystem` — read/write files in `/workspace`
- `agent_browser` — headless browser CLI
- `apply_patch` — structured code patches
- `view_image` — screenshot inspection

### Integration Pattern

- All tools: `@function_tool` decorated, explicit timeout (10s-601s)
- All return `json.dumps(dict, ensure_ascii=False, default=str)`
- Context accessed via `ctx.context` dict: `agent_id`, `parent_id`, `coordinator`, `sandbox_session`, `caido_client`, `interactive`, `spawn_child_agent`
- **Errors caught and returned as model-visible string results, never raised** — keeps agent in loop
- Custom tools wrapped to `FunctionTool` with single-string input schema for chat-completions backends

---

## 5. Config System

### Precedence

```
env vars > JSON file (~/.strix/cli-config.json) > defaults
```

### Settings

- **LLM**: model, api_key, api_base, reasoning_effort (none/minimal/low/medium/high/xhigh), timeout (300s)
- **Runtime**: Docker image, backend, max_local_copy_mb (1024)
- **Integrations**: perplexity_api_key
- **Telemetry**: enabled (default true)

### Model Routing

- Non-OpenAI prefixes → LiteLLM (strips `litellm/`/`any-llm/` prefix, `ollama` → `ollama_chat/`)
- `api_base` set → chat_completions API; else responses API
- Retry: 5 max, exponential 2s→90s, on 429/500/502/503/504 + network + provider-suggested

### Scan Config

```python
scan_config = {
    "targets": [{"type": "local_code|url|domain", "value": "...", "workspace_path": "..."}],
    "scan_mode": "quick|standard|deep",  # default deep
    "skills": ["authentication_jwt", "business_logic"],
    "resume_instruction": "..."
}
```

- `local_code` target type → triggers whitebox mode
- Scope context built from targets → injected into system prompt as authorized scope

---

## 6. Adapter Patterns for Other Harnesses

### Hermes Agent
- `delegate_task` → maps to `create_agent` (spawn child)
- `memory` → maps to `notes` (scan-wide persistence)
- `todo` → maps to per-agent todos
- `terminal` → maps to sandbox `shell`
- Skills loaded via `skill_view(name)` → same frontmatter format
- Background processes via `terminal(background=true)` → maps to Docker sandbox

### Claude Code
- `Task` tool → maps to `create_agent`
- `Read`/`Write`/`Edit` → maps to sandbox filesystem
- `Bash` → maps to sandbox shell
- CLAUDE.md → maps to coordination skill injection

### Codex CLI
- `shell` commands → sandbox shell
- Code generation → patch tools
- Multi-step → agent loop until lifecycle

### Universal Mapping

| Strix Concept | Generic Equivalent |
|---------------|-------------------|
| `create_agent` | Spawn child agent/subagent |
| `send_message` | Inter-agent message bus |
| `agent_finish` | Lifecycle terminator (child) |
| `finish_scan` | Lifecycle terminator (root) |
| `load_skill` | Load domain knowledge module |
| `think` | Step-back reasoning step |
| `create_note` | Shared persistent state |
| `create_todo` | Per-agent task tracking |
| `view_agent_graph` | Agent tree introspection |

---

## 7. Skill Writing Guide

### Good skill contains:
- **Attack surface** — where to look
- **Reconnaissance** — how to enumerate
- **Key vulnerabilities** — what to test, with payloads
- **Advanced techniques** — non-obvious methods
- **Validation** — confirm findings, avoid false positives
- **False positives** — what NOT to report
- **Impact** — severity assessment
- **Pro tips** — domain-specific insights

### YAML frontmatter:
```yaml
---
name: lowercase-hyphen-name
description: One-line summary
---
```

### Body: markdown, no limit but concise. Working payloads > theory.

---

## 8. Key Design Principles

1. **Root never tests** — orchestrator only
2. **One job per agent** — reactive spawning, not upfront
3. **Errors as results, not exceptions** — keeps agent in loop
4. **Shared state across agents** — same container, same notes
5. **Skills capped at 5/agent** — focus over breadth
6. **Lifecycle tools gate termination** — no premature exit
7. **Atomic JSON snapshots** — resumable scans
8. **Budget stop broadcast** — clean shutdown for all agents
9. **Scope injection** — authorization hardcoded, not agent-controlled
10. **PoC or it didn't happen** — every finding needs working proof
