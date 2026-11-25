---
name: ai-agent-founding-team
description: How to design an AI-powered founding team using a multi-agent architecture — covering the org chart layout, the first six agent hires (content, research, outreach, ops, finance, customer), and installing a Chief of Staff orchestrator agent that directs all others from a single goal. Original content from @theromanknox. Use when setting up an autonomous agent team for a solo founder or small business.
---

# AI Agent Founding Team

Original content by @theromanknox. Three-page framework for wiring up an autonomous AI workforce for a one-person or small business.

---

## Page 2 — The Org Chart (One-Click Setup)

Design the AI team like a real company org chart before writing a single prompt.

**Core principle**: Give each agent one role, one lane, and one output format. Agents that do everything do nothing reliably.

**The top layer**:
- **Chief of Staff** (orchestrator) — receives the goal, breaks it into tasks, delegates to specialists, assembles the output
- Reports: all specialist agents route their outputs back to the Chief of Staff for assembly

**Why one-click setup matters**: The org chart should be wired once as a configuration (Claude Code project, CLAUDE.md, or a tool like n8n), so that a single trigger (one message, one webhook, one cron job) starts the whole team — not a manual prompt to each agent every time.

---

## Page 3 — First Six Hires

Six agents every solo founder or small-business operator needs before any specialist hires:

| # | Agent | One job |
|---|---|---|
| 1 | **Content agent** | Drafts posts, emails, scripts, and carousels from a brief |
| 2 | **Research agent** | Scans competitors, trends, sources, and summarises findings |
| 3 | **Outreach agent** | Writes cold DMs/emails and manages follow-up sequences |
| 4 | **Ops agent** | Tracks tasks, updates project boards, surfaces blockers |
| 5 | **Finance agent** | Monitors invoices, expenses, and flags anomalies |
| 6 | **Customer agent** | Responds to FAQs, handles tier-1 support, escalates edge cases |

**Hiring order**: hire in priority order for the business model. A content-led business hires Content + Research first. A service business hires Customer + Ops first.

**Tool tip**: Each agent needs exactly three things — a system prompt (its role), access to tools (search, file read/write, send message), and a reporting format (how it hands off output to the Chief of Staff).

---

## Page 4 — Your Chief of Staff

> "The One Nobody Installs."

**Role**: The Chief of Staff is an **agents orchestrator** — it receives a single high-level goal and:
1. Breaks the goal into tasks
2. Assigns each task to the right specialist agent
3. Collects outputs
4. Assembles the final deliverable
5. Returns it to the human — without the human touching any intermediate step

**How to use it**:

```
Give it a single goal.
It directs your agents and assembles everything without you.
```

**Implementation patterns**:

- **Claude Code subagents** — use `claude --subagent` to spawn specialist agents from a coordinating Claude Code session. The parent session acts as Chief of Staff.
- **n8n workflow** — an "orchestrator" node receives the trigger, calls specialist sub-workflows for each task, then a "merge" node assembles the outputs.
- **LangGraph / CrewAI** — define a supervisor node connected to a set of worker nodes; the supervisor dispatches and collects.

**The one rule**: The Chief of Staff must never do the work itself — only direct, collect, and assemble. The moment an orchestrator starts writing content, it loses the ability to coordinate everything else.

---

## Common failure modes

| Failure | Fix |
|---|---|
| Agents overlap — two agents do the same thing | Each agent's system prompt must name what it does NOT do |
| Chief of Staff bottleneck — everything waits for it | Parallelize tasks that don't depend on each other; the CoS dispatches simultaneously |
| No handoff format — agents return unstructured text | Define a JSON or structured Markdown output template for each specialist |
| Human re-prompts individual agents — defeats the point | Route everything through the Chief of Staff; the human only gives the top-level goal |

---

## Minimal Claude Code CLAUDE.md template for a 6-agent founding team

```markdown
## Agent roles

### Chief of Staff
You are an orchestrator. Receive the user's goal, break it into tasks,
delegate to the appropriate specialist agents below, collect their outputs,
and assemble a final deliverable. Never do the specialist work yourself.

### Content Agent
You write posts, emails, and carousels. Input: a brief. Output: draft.

### Research Agent  
You search, summarise, and cite. Input: a topic/question. Output: bullet list with sources.

### Outreach Agent
You write cold messages and follow-ups. Input: target + context. Output: message sequence.

### Ops Agent
You track tasks and blockers. Input: status update or goal. Output: updated task list.

### Finance Agent
You monitor invoices and expenses. Input: data snapshot. Output: anomaly flags + summary.

### Customer Agent
You handle tier-1 support. Input: customer message. Output: response draft or escalation flag.
```

Source: @theromanknox carousel (pages 2–4), Sep 2026. Build skills: skool.com/knox.
