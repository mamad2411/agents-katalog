# 🚀 Squad Quick-Start Guide

**Blaze.LlmGateway Development Squad** — A 9-agent, 8-skill agentic development framework for rapid, high-quality feature delivery.

This guide shows you how to launch and orchestrate the squad for your Blaze.LlmGateway tasks.

---

## Quick Launch (TL;DR)

### **Claude Code**
```
/agent squad "Add circuit breaker pattern to LlmRoutingChatClient"
```

### **Copilot CLI**
```powershell
copilot -p "Start a squad run for: Add resilient failover to routing"
```

---

## The Two Paths

### 🎯 **Path 1: Human-Gated Phased Development** (Recommended)

**Command:**
```bash
/agent squad "Your task description"
```

**When to use:**
- ✅ Complex features that need architectural review
- ✅ High-risk changes (e.g., routing logic, resilience patterns)
- ✅ Production-critical systems
- ✅ When you want to review each phase

**Workflow:**
```
[CONDUCTOR] → Create run dir + reasoning log
    ↓
[PLANNER] → Research + spec + plan (you review)
    ↓
[ARCHITECT] → ADR design document (you review)
    ↓
[CODER] → Implementation in isolated Git worktree
    ↓
[TESTER] → Unit tests + integration tests (95% coverage target)
    ↓
[REVIEWER] → Clean-context diff review + quality gate
    ↓
[INFRA] → AppHost / Aspire updates
    ↓
[SECURITY-REVIEW] → ADR-0008 cloud-egress check
    ↓
[DONE] → Results merged to main
```

**Artifacts Created:**
- `Docs/squad/runs/<timestamp>-<task-slug>/reasoning.log.md` — decision trail
- `Docs/squad/runs/<timestamp>-<task-slug>/handoff/` — inter-agent envelopes
- `Docs/squad/runs/<timestamp>-<task-slug>/spec.md` — feature specification
- `Docs/squad/runs/<timestamp>-<task-slug>/plan.md` — implementation plan
- `Docs/design/adr/<N>-<title>.md` — architecture decision record

---

### ⚡ **Path 2: Autonomous Parallel Development** (Hands-Off)

**Command:**
```bash
/orchestrate "Your task description"
```

Or with a pre-written PRD:
```bash
/orchestrate --prd Docs/PRD/my-feature.md
```

**When to use:**
- ✅ Clear, well-scoped tasks
- ✅ Work that decomposes into parallel streams (Coder + Tester + Infra)
- ✅ Rapid prototyping / proof-of-concept
- ✅ No human gates needed between phases

**Workflow:**
```
[ORCHESTRATOR] → Generate PRD (if needed) + decompose tasks
    ↓
    ├─→ [CODER] (isolated Git worktree #1)
    ├─→ [TESTER] (isolated Git worktree #2)
    └─→ [INFRA] (isolated Git worktree #3)
    ↓
[ORCHESTRATOR] → Monitor all 3 in parallel
    ↓
[ORCHESTRATOR] → Merge all worktrees back to main
    ↓
[DONE] → Full implementation + tests + infra
```

**Artifacts Created:**
- `Docs/squad/runs/<timestamp>-<task-slug>/reasoning.log.md` — decision trail
- `Docs/squad/runs/<timestamp>-<task-slug>/prd.md` — generated PRD
- `.worktrees/<task-slug>-coder/` — isolated Coder worktree
- `.worktrees/<task-slug>-tester/` — isolated Tester worktree
- `.worktrees/<task-slug>-infra/` — isolated Infra worktree

---

## Examples by Task Type

### Add a New LLM Provider

```bash
# Human-gated (recommended for production changes)
/agent squad "Add Anthropic Claude as an LLM provider with routing hints"
```

**Expected output:**
- ADR explaining provider architecture
- New `AddAnthropicProvider()` extension in Infrastructure
- Test coverage for routing to Anthropic
- AppHost configuration

---

### Implement Circuit Breaker Pattern

```bash
# Autonomous (clear, well-scoped)
/orchestrate "Add circuit breaker to LlmRoutingChatClient with exponential backoff"
```

**Expected output:**
- Parallel development of:
  - ✅ Circuit breaker middleware (Coder)
  - ✅ 95% test coverage (Tester)
  - ✅ Monitoring + resilience config (Infra)
- All merged and ready

---

### Fix a Bug

```bash
# Quick fix with tests
/agent squad "Fix: MCP tool caching not clearing on provider failure"
```

---

## Understand the Agents

| Agent | Role | Phase |
|-------|------|-------|
| **Conductor** | Orchestrates the squad, creates run directories, gates phases | Early (research) |
| **Planner** | Research, specification, implementation planning | Planning |
| **Architect** | Writes ADR, validates MEAI pipeline, resilience design | Architecture |
| **Coder** | Implements C# code, follows squad guardrails | Implementation |
| **Tester** | xUnit tests, Moq mocks, 95% coverage enforcement | Testing |
| **Reviewer** | Clean-context diff review, `-warnaserror` + coverage gate | Quality |
| **Infra** | AppHost, Aspire, secrets, service discovery | Infrastructure |
| **Security-Review** | ADR-0008 cloud-egress audit, default-deny checks | Security |
| **Orchestrator** | Autonomous loop, parallel worktrees, no human gates | All (parallel) |

---

## The 11 Coordination Skills

The squad has access to powerful coordination skills:

| Skill | Purpose |
|-------|---------|
| **reasoning** | Append-only decision log maintenance |
| **quality-gate** | Enforce `-warnaserror` + 95% coverage |
| **prove-it-bugfix** | TDD bug-fix flow (reproduce → test → fix → verify) |
| **claude-devfleet** | Multi-agent parallelization via Git worktrees |
| **team-builder** | Compose and dispatch parallel agent teams |
| **dispatching-parallel-agents** | Auto-assign tasks to subagents |
| **autonomous-agent-harness** | Task queue + scheduler + memory for loops |
| **dmux-workflows** | TMux orchestration (WSL/Unix) |
| **subagent-driven-development** | Hierarchical task delegation |
| **loop-operator** | Loop supervision + recovery |
| **write-a-prd** | PRD generation from raw task description |

---

## Monitoring a Squad Run

### Check the reasoning log:
```bash
cat Docs/squad/runs/<timestamp>-<task-slug>/reasoning.log.md
```

### View handoff envelopes (inter-agent communication):
```bash
ls Docs/squad/runs/<timestamp>-<task-slug>/handoff/
```

### Inspect isolated worktrees (parallel mode):
```bash
ls -la .worktrees/
```

### Check the spec and plan:
```bash
cat Docs/squad/runs/<timestamp>-<task-slug>/spec.md
cat Docs/squad/runs/<timestamp>-<task-slug>/plan.md
```

---

## Guardrails (Automatic)

Every squad run enforces:

✅ **MEAI Law** — All LLM interactions use `IChatClient`, `ChatMessage`, `ChatOptions`  
✅ **Streaming by Default** — Endpoint uses SSE, never polling  
✅ **Keyed DI** — Provider resolution via `GetKeyedService<IChatClient>(key)`  
✅ **Quality Gate** — Build: `-warnaserror`; Tests: 95% coverage minimum  
✅ **File-Lock Disjointness** — No two agents own the same file per phase  
✅ **Clean-Context Review** — Reviewer sees only changed code, not entire repo  
✅ **Cloud-Egress Audit** — All external calls logged and reviewed (ADR-0008)  
✅ **Append-Only Reasoning** — Decision trail preserved forever  

---

## Common Patterns

### I need a quick proof-of-concept
```bash
/orchestrate "POC: Redis caching for provider responses"
```

### I'm uncertain about the approach
```bash
/agent squad "Research: Should we use circuit breaker or bulkhead pattern?"
```
The Planner will explore both, then you decide before architecture.

### I have a complete PRD ready
```bash
/orchestrate --prd Docs/PRD/feature-name.md
```

### I need to fix something in a running squad
Reach out mid-phase to the Conductor (in the squad's own conversation). It will pause the current phase and let you redirect.

---

## Expected Output Timeline

### `/agent squad` (Human-Gated)
- **Planner phase:** 5–10 min (spec + plan)
- **You review:** (your time)
- **Architect phase:** 3–5 min (ADR)
- **You review:** (your time)
- **Coder phase:** 5–15 min (implementation)
- **Tester phase:** 3–10 min (tests + coverage)
- **Reviewer phase:** 2–5 min (quality gate)
- **Infra phase:** 2–5 min (AppHost/Aspire)
- **Security review:** 1–3 min (ADR-0008 check)
- **Total:** 20–50 minutes (plus your review time)

### `/orchestrate` (Autonomous)
- **PRD generation:** 2–3 min (if needed)
- **Parallel execution:** 10–20 min (all three agents in parallel)
- **Merge + finalization:** 2–5 min
- **Total:** 15–30 minutes (fully autonomous, no waits)

---

## Troubleshooting

### "Command not found: /agent squad"
→ Ensure the squad plugin is installed:
```bash
copilot plugin list
```
You should see `squad@_direct (v2.0.0)`.

### "TypeError: a.replace is not a function"
→ Known issue in Copilot CLI v1.0.34. Try upgrading:
```bash
copilot upgrade
```

### "Git worktree already exists"
→ Clean up stale worktrees:
```bash
git worktree list
git worktree remove .worktrees/<name>
```

### Squad is stuck or not responding
→ Check the reasoning log to see where it paused:
```bash
tail -50 Docs/squad/runs/<timestamp>-<task-slug>/reasoning.log.md
```

---

## Next Steps

**Ready to go?** Pick a task and run:

```bash
# Human-gated (recommended first time)
/agent squad "Add resilient failover for provider timeouts"

# Or autonomous (once familiar)
/orchestrate "Implement provider health checks in AppHost"
```

**Questions?** Check:
- `.github/copilot-instructions.md` — Squad architecture & conventions
- `CLAUDE.md` — Architecture decisions & guardrails
- `prompts/squad/conductor.prompt.md` — Conductor's thinking process
- `Docs/design/adr/0010-parallel-orchestration-path.md` — Why two paths?

---

**Happy squading! 🚀**
