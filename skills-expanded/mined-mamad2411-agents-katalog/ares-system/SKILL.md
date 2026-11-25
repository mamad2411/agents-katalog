---
name: ares-system
description: >
  Complete reference for working with the ARES (Advanced Rust & Ethereum Security) platform — an AI-powered security testing platform with 8 integrated tools: Trident (Solana fuzzing), Semgrep (static analysis), Checked Math (Rust overflow detection), FuzzyAI (LLM fuzzing), Whistleblower (prompt extraction), MCP Injection (MCP security testing), Multi-Agent System (AI orchestration), and HexStrike AI (pentest automation).

  Use this skill whenever the user wants to: run security scans on smart contracts, perform AI-powered vulnerability analysis, execute pentest automation, analyze Rust/Solana code, fuzz Solana programs, test LLM security, extract system prompts, audit MCP tools, or orchestrate multiple security tools via the multi-agent system. Also trigger when the user mentions ARES, aressystem.dev, security audit workflow, or any of the 8 security tools.
---

# ARES Security Platform

ARES is an **AI-powered security testing platform** built on Express + TypeScript with 8 integrated security tools orchestrated by a hierarchical multi-agent system.

**Base URL (Production):** `https://api.aressystem.dev`
**Base URL (Local):** `http://localhost:8889`

---

## Quick Orientation

| What you need | Where to look |
|---|---|
| Run a security scan | `references/api-endpoints.md` |
| Understand the 8 tools | `references/tools-integration.md` |
| Configure multi-agent AI | `references/multi-agent-system.md` |
| Deploy or restart the API | Quick commands below |

---

## Architecture Overview

```
┌─────────────────────────────────────────────┐
│  React Frontend (Port 5173)                 │
│  - Cyberpunk UI with real-time monitoring   │
└─────────────────────┬───────────────────────┘
                      │ HTTP/SSE
┌─────────────────────▼───────────────────────┐
│  Express API Server (Port 8889)              │
│  - 8 Security Tools                          │
│  - Hierarchical Multi-Agent System            │
│  - SSE Streaming                              │
└─────────────────────┬───────────────────────┘
                      │
┌─────────────────────▼───────────────────────┐
│  Security Tools                               │
│  - Trident (Rust/Cargo)                      │
│  - Semgrep (Python)                           │
│  - Checked Math (Rust analysis)               │
│  - FuzzyAI (Python/OpenRouter)                │
│  - Whistleblower (Python)                     │
│  - MCP Injection (Python)                    │
│  - HexStrike (Bash/Kali tools)               │
└─────────────────────────────────────────────┘
```

---

## Security Tools Summary

| Tool | Purpose | Key Capability |
|---|---|---|
| **Trident** | Solana program fuzzing | 12,000 tx/s fuzzing |
| **Semgrep** | Static analysis | 30+ languages |
| **Checked Math** | Rust overflow detection | Static analysis |
| **FuzzyAI** | LLM fuzzing | 18+ attack types |
| **Whistleblower** | Prompt extraction | System prompt leaks |
| **MCP Injection** | MCP security testing | MCP vulnerability detection |
| **HexStrike AI** | Pentest automation | 150+ Kali tools |
| **Multi-Agent** | AI orchestration | Hierarchical agentic loop |

---

## AI Models

| Role | Model | Context Window |
|---|---|---|
| Orchestrator | `stepfun/step-3.5-flash:free` | 256K |
| Specialist | `nvidia/nemotron-3-super-120b-a12b:free` | 128K |
| Worker | `nvidia/nemotron-3-nano-30b-a3b:free` | 131K |

---

## Quick Commands

### Docker Management

```bash
# Restart running containers
docker-compose restart

# Deploy fresh build
docker-compose build --no-cache && docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Start services
docker-compose up -d
```

### API Health Check

```bash
curl https://api.aressystem.dev/health
```

---

## Streaming Response Format

Multi-agent endpoints emit Server-Sent Events (SSE):

| Event | Description |
|---|---|
| `status` | Phase change / progress `{ phase, message, agent, model, step?, totalSteps? }` |
| `token` | Single LLM token chunk `{ text, agent, model, phase }` |
| `result` | Final output `{ response, findings, toolsUsed, duration, timestamp }` |
| `error` | Failure `{ message }` |

---

## Common Request Patterns

### Non-Streaming Request

```bash
curl -X POST https://api.aressystem.dev/api/multi-agent/autonomous \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Audit this Solana program for reentrancy vulnerabilities"}'
```

### Streaming Request

```bash
curl -N -X POST https://api.aressystem.dev/api/multi-agent/autonomous/stream \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Run a comprehensive security audit on 0x123..."}'
```

### Security Audit Across All Domains

```bash
curl -X POST https://api.aressystem.dev/api/multi-agent/tasks/security-audit \
  -H "Content-Type: application/json" \
  -d '{"target": "0x123...", "scope": ["blockchain"]}'
```

---

## Environment Variables

Key environment variables for deployment:

| Variable | Description | Default |
|---|---|---|
| `OPENROUTER_API_KEY` | OpenRouter API key | Required |
| `ARES_PORT` | API server port | 8888 |
| `ARES_TOOLS_TIMEOUT` | Tool execution timeout | 300000ms |
| `ARES_TOOLS_CACHE_ENABLED` | Enable tool caching | true |
| `TRIDENT_PATH` | Path to Trident binary | /app/trident |
| `SEMGREP_PATH` | Path to Semgrep | semgrep |

---

## Response Format

**Success:**
```json
{ "status": "ok", "data": { ... } }
```

**Error:**
```json
{ "error": "Human-readable message" }
```

---

## Additional Resources

### Reference Files

For detailed API endpoints, tool configurations, and multi-agent system internals:

- **`references/api-endpoints.md`** — Complete API endpoint reference
- **`references/tools-integration.md`** — All 8 security tools details
- **`references/multi-agent-system.md`** — Hierarchical AI agent system

### Documentation

- **Quick Start:** `QUICK_START.md`
- **Security Tools Reference:** `SECURITY_TOOLS_QUICK_REFERENCE.md`
- **Multi-Agent System:** `docs/MULTI_AGENT_SYSTEM.md`
- **Trident:** `docs/TRIDENT_INTEGRATION.md`
- **Semgrep:** `docs/SEMGREP_INTEGRATION.md`
- **Checked Math:** `docs/CHECKED_MATH_INTEGRATION.md`
