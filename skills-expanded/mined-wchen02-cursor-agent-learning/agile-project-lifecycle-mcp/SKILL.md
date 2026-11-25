---
name: agile-project-lifecycle-mcp
description: Full agile lifecycle with MCP: use MCP to fetch current docs/API schema during discovery and development. Use when building a project from a rough idea that depends on external APIs or libraries and you want up-to-date references via MCP.
---

# Agile Project Lifecycle + MCP (Replit-Style, Full Loop + HITL)

Same phases and gates as the base [agile-project-lifecycle](../agile-project-lifecycle/SKILL.md), with **MCP (Model Context Protocol)** used for live docs and API schemas during discovery, planning, and development. Invoke this skill when the user wants the agile lifecycle **and** MCP for docs/APIs.

## When to use (MCP variant)

- The user has a rough idea that involves **external APIs or libraries** (e.g. Stripe, React, Prisma) and wants **current docs/schemas via MCP** instead of pasting docs.
- You want the full agile flow (requirements → develop → unit → integration → e2e → feedback loop + HITL) **with MCP** at discovery and develop.
- **MCP server setup:** Use a configured MCP server (e.g. project-docs, Context7, Stripe). In this repo: [examples/mcp-servers/README.md](../../../examples/mcp-servers/README.md) and [.cursor/mcp.json.example](../../../.cursor/mcp.json.example). Run `npm install` in `examples/mcp-servers/project-docs/`, copy the example to `.cursor/mcp.json`, restart Cursor.

## MCP best practice: check tool schema first

Before calling any MCP tool, read the tool’s descriptor (e.g. `mcps/<server>/tools/<tool>.json`) so you use correct parameters and required fields.

## Phase 0: Discovery and requirements

- **Research:** Use **explore** (or main agent) to understand the codebase. **Use MCP** to fetch current docs or API schema for the idea (e.g. Context7 for library docs, project-docs for repo docs, Stripe MCP for payments). Use this to clarify scope and write accurate requirements. Check each MCP tool’s schema before calling.
- **Clarify:** Summarize what "done" looks like in 2–5 sentences. If the idea is vague, ask 1–2 short clarifying questions and incorporate answers.
- **Requirements:** Produce a short **requirements** section the human can approve (user-facing outcomes, acceptance criteria, out of scope, technical constraints).

Then output **Gate 1: Requirements** (same as base skill). **Stop.** Do not start development until the user has approved.

---

## Phase 1: Iteration planning

- Invoke the **planner** subagent with the approved requirements. **Optionally use MCP** to refine scope (e.g. "what endpoints exist?" from an API schema). Get slices and current slice scope/steps. Present the iteration plan.

---

## Phase 2: Development cycle (loop)

Same structure as base skill (2.1 Develop → 2.2 Unit → 2.3 Integration → 2.4 E2E → 2.5 Verify → 2.6 Gate 2). MCP-specific:

### 2.1 Develop (with MCP)

- Implement the current slice. **Call MCP** whenever you need up-to-date API or library details (signatures, options, examples). Check tool schema before each MCP call. Follow project rules. Keep the project runnable.

### 2.5 Verify (optional MCP)

- Verifier can use MCP to check implementation against current docs (e.g. "does this match the official API?").

### 2.6 Feedback gate (Gate 2)

Same as base skill. **Optional:** Use **beforeMCPExecution** / **afterMCPExecution** hooks to audit or gate MCP usage; see [.cursor/hooks/examples/mcp-hooks.example.json](../../hooks/examples/mcp-hooks.example.json) and [.cursor/rules/mcp-patterns.mdc](../../rules/mcp-patterns.mdc).

---

## Phase 3: Completion

Same as base skill. Run only when the user said "Complete" or approved the final iteration.

---

## Loop summary

Same as base skill. Never assume approval. For test levels, see [reference.md](reference.md). For MCP server setup and hooks, see [examples/agent-frameworks/agile-project-lifecycle-mcp.md](../../../examples/agent-frameworks/agile-project-lifecycle-mcp.md) and [.cursor/rules/mcp-patterns.mdc](../../rules/mcp-patterns.mdc).
