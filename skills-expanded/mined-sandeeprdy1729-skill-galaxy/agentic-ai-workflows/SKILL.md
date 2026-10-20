---
name: agentic-ai-workflows
description: "Design and implement agentic AI systems that autonomously chain multiple tools to complete complex tasks. Covers tool composability, multi-step reasoning, approval flows, error recovery, and production deployment patterns."
license: Apache 2.0
tags: ["agentic-ai", "tool-use", "composability", "multi-step", "claude", "mcp", "automation"]
difficulty: advanced
time_to_master: "10-20 weeks"
version: "1.0.0"
---

# Agentic AI Workflows

## Overview

Agentic AI refers to systems where a language model autonomously plans, executes, and iterates on multi-step tasks using external tools. Unlike single-turn Q&A, agentic workflows involve tool chaining — where the output of one tool feeds the input of the next — enabling complex real-world automation.

## When to Use This Skill

- Building AI agents that chain 3+ tool calls to complete a task
- Designing approval workflows for high-stakes AI actions
- Implementing error recovery and retry logic in tool chains
- Optimizing tool selection and routing for token efficiency
- Creating human-in-the-loop checkpoints for compliance
- Orchestrating multi-agent systems with specialized roles

## Core Concepts

### Tool Composability Architecture

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Tool A      │────►│  Tool B      │────►│  Tool C      │
│  (Fetch Data)│     │  (Transform) │     │  (Take Action)│
└──────────────┘     └──────────────┘     └──────────────┘
       │                    │                     │
       ▼                    ▼                     ▼
  Context grows      Model reasons          Final result
  with results       about next step         delivered
```

### Composability Patterns

| Pattern | Description | Example |
|---------|-------------|---------|
| **Sequential Chain** | A → B → C in order | Fetch data → analyze → send report |
| **Conditional Branch** | If/else based on tool output | Check status → approve or escalate |
| **Fan-out/Fan-in** | Parallel tools, merge results | Query 3 APIs → combine insights |
| **Iterative Loop** | Repeat until condition met | Search → refine query → search again |
| **Human Checkpoint** | Pause for approval | Draft email → user approves → send |

### Claude's Composability Advantage

Claude naturally chains 4-5+ tools per turn when given "Always Allow" permissions. This is a decisive advantage over systems like ChatGPT that require per-action approval, creating "Permission Fatigue" that breaks complex workflows.

## Implementation Guide

### Designing Tool Chains

**Rule 1: Each tool should return enough context for the model to decide the next step.**

```python
# Bad: returns only an ID
def get_account():
    return {"account_id": "acc_123"}

# Good: returns context the model needs for next decision
def get_account():
    return {
        "account_id": "acc_123",
        "balance": 15420.50,
        "status": "active",
        "last_transaction": "2026-03-28",
        "pending_invoices": 3
    }
```

**Rule 2: Design tools as composable units, not monolithic endpoints.**

```python
# Composable tools for financial analysis
tools = [
    "get_account_summary",    # Returns balances, status
    "list_transactions",       # Returns recent transactions
    "run_forecast",           # Takes balance + transactions, returns projection
    "generate_report",        # Takes forecast, outputs formatted report
    "send_notification",      # Sends result to stakeholder
]
```

### Human-in-the-Loop (HITL) Patterns

For high-stakes actions (payments, deletions, external communications):

```typescript
server.tool(
  "request_approval",
  "Pause workflow and request human approval for a proposed action",
  {
    action: z.string().describe("Description of the action to approve"),
    details: z.object({
      type: z.enum(["payment", "deletion", "communication", "deployment"]),
      impact: z.string(),
      reversible: z.boolean(),
    }),
  },
  async ({ action, details }) => {
    const approval = await approvalQueue.submit({
      action,
      details,
      timestamp: new Date().toISOString(),
      status: "pending",
    });

    // Block until human responds
    const decision = await approvalQueue.waitForDecision(approval.id);

    return {
      content: [{
        type: "text",
        text: decision.approved
          ? `Approved by ${decision.approver}. Proceeding.`
          : `Rejected: ${decision.reason}. Workflow halted.`,
      }],
    };
  }
);
```

### Error Recovery Strategies

```
┌─────────┐     ┌──────────┐     ┌───────────┐
│ Execute │────►│  Error?  │──No─►│  Continue  │
│  Tool   │     │          │      │  Chain     │
└─────────┘     └────┬─────┘      └───────────┘
                     │Yes
                     ▼
              ┌──────────────┐
              │  Retry with  │──Success──►  Continue
              │  backoff     │
              └──────┬───────┘
                     │Fail
                     ▼
              ┌──────────────┐
              │  Graceful    │
              │  degradation │
              └──────────────┘
```

**Patterns:**
1. **Retry with exponential backoff** for transient failures (network, rate limits)
2. **Fallback tools** — if primary API fails, try alternative data source
3. **Partial results** — return what you have with a note about missing data
4. **Escalation** — trigger human-in-the-loop when automated recovery fails

### Context Window Management

As tools are chained, each result accumulates in the context window. Strategies:

- **Summarize intermediate results** — Don't pass raw API responses between steps; extract only what's needed
- **Use tool-level pagination** — Return 10 results with "more available" rather than 1000
- **Implement "Code Mode"** — Let the model write code that runs locally, keeping raw data out of context
- **Clear completed context** — Mark earlier tool results as disposable after they've been consumed

### Multi-Agent Orchestration

```
┌─────────────┐
│ Coordinator  │ ◄─── User request
│   Agent      │
└──────┬───────┘
       │ Delegates
       ├──────────────────┬──────────────────┐
       ▼                  ▼                  ▼
┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│  Research   │   │  Analysis   │   │  Execution  │
│   Agent     │   │   Agent     │   │   Agent     │
│  (read-only)│   │  (compute)  │   │  (actions)  │
└─────────────┘   └─────────────┘   └─────────────┘
```

## Security Considerations

- **Principle of least privilege** — Each tool gets only the permissions it needs
- **Input validation** — Model-generated inputs can be adversarial; sanitize at every boundary
- **Audit logging** — Record every tool call, input, and output for compliance
- **Rate limiting** — Prevent runaway loops from consuming excessive API quotas
- **Scope separation** — Read-only tools should never have write access

## Best Practices

1. **Start simple** — Build 2-tool chains before attempting 5-tool orchestrations
2. **Test each tool independently** before testing the chain
3. **Design for idempotency** — Tools may be called multiple times
4. **Prefer structured outputs** — Give the model clear data to reason about
5. **Monitor token usage** — Complex chains can consume 50K+ tokens per turn
6. **Build kill switches** — Every agent workflow must be interruptible

## Resources

- [Anthropic Tool Use Documentation](https://docs.anthropic.com/en/docs/tool-use)
- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [Building Effective Agents (Anthropic)](https://docs.anthropic.com/en/docs/agents)

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-03-31 | Initial documentation |

---

*Part of SkillGalaxy - 10,000+ comprehensive skills for AI-assisted development.*
