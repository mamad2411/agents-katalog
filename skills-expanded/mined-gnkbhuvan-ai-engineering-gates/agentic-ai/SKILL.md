---
name: agentic-ai
description: |
  Agentic AI architecture — deciding whether to build an agent at all, then designing it.
  Branches: design a single- or multi-agent system, decide agent vs. workflow, design
  tools/MCP integration, design agent memory, design planning/orchestration, debug a
  looping or failing agent, or add human-in-the-loop safety gating. This is an
  architecture/design skill — use `fastapi-genai` for implementation and
  `prompt-engineering` for the actual prompt templates.
---

# Agentic AI Architecture

Architecture methodology for agentic systems. Audience includes non-engineers (PMs,
architects) as well as AI engineers—stay at the architecture/decision level here. Prompt
templates (ReAct, tool-call syntax) live in `prompt-engineering`; service implementation
lives in `fastapi-genai`.

## First-Principles Foundation

1. **Agent vs. workflow vs. plain prompt — the core distinction**: in a plain prompt, you
   get one response. In a **workflow**, code paths decide which tools/steps run — the
   sequence is deterministic. In an **agent**, the model itself decides which tools to use
   and what to do next, looping (perceive → plan → act → observe) until it judges the task
   done. Only call something an agent if the model is genuinely making that loop's
   decisions — a single tool call wrapped in a retry loop is a workflow, not an agent.
2. **More steps is not free reliability — it's a cost**: if per-step accuracy is 95%, that
   compounds to roughly 60% over 10 sequential steps and 0.6% over 100. Every additional
   step in an agent's loop is a reliability tax you pay deliberately, not an upgrade you get
   for free. Design for the fewest steps that solve the task.
3. **More tools is not free capability — it's a tax on tool selection**: performance drops
   as tool count grows, mainly from ambiguity/overlap between tool descriptions making
   correct selection harder. Keep the tool set small and the descriptions disjoint; don't
   reach for "give it more tools" as a default fix.
4. **Never let a model verify its own work as the sole check**: self-grading and
   self-stated confidence are unreliable signals. Use a separate validator, a heuristic
   check, or a human — not the same model re-asserting it's right.
5. **KISS applies to agents more than almost anything else**: don't complicate the
   architecture (more agents, more tools, more planning steps) without a specific, named
   reason. The simplest architecture that solves the task is the right one until it
   demonstrably isn't.

## Trigger Decision Tree

1. **Does this need to be an agent at all?** If the task is a single well-defined
   transformation with no need for the model to choose its own steps, it's a plain prompt.
   If the steps are known and fixed, it's a workflow (code decides). Only build an agent
   when the model genuinely needs to decide what to do next based on what it just observed.
2. **Confirm missing details**—gate below; do not architect past this point until it passes.
3. **Design the agent loop**: tools, planning strategy, memory → `references/agent-fundamentals.md`,
   `references/tools-and-mcp.md`, `references/planning-and-reasoning.md`,
   `references/memory-architecture.md`.
4. **Single agent or multiple?** Default to single. Escalate only with a specific reason →
   `references/multi-agent-orchestration.md`.
5. **Decide build vs. buy** (native SDK vs. framework, prototype vs. production) →
   `references/multi-agent-orchestration.md`.
6. **Plan failure modes, evaluation, and human-in-the-loop gating before shipping** →
   `references/failure-modes-and-safety.md`.

### When Information Is Missing—Ask Before Architecting

| Missing? | Ask |
|---|---|
| Why an agent at all | "What does the model need to decide dynamically that a fixed sequence of steps couldn't?" |
| Action consequences | "Are any of the agent's actions irreversible or costly (payments, deletions, sending messages)? Those need human sign-off, not just a tool description." |
| Tool inventory | "What specific tools/systems does it need access to—and is each one truly necessary?" |
| Latency/cost tolerance | "How many seconds and how much per task is acceptable? More planning steps cost both." |
| Failure tolerance | "What should happen when the agent gets stuck or is uncertain—fail loudly, ask the user, or retry?" |
| Success criteria | "How will you know the agent actually completed the task correctly?" |

**Gate**: this step is done only when every row above that's actually unclear from context has either been answered by the user or stated out loud as an explicit assumption with no objection. Silently assuming and continuing does not satisfy this — stop and ask instead.

## Build vs. Buy — Quick Reference

| Question | Default | Escalate only if |
|---|---|---|
| Native SDK or framework? | Provider-native (Claude Agent SDK / OpenAI Agents SDK) | You need multi-provider portability or a graph-style orchestration topology a simple loop can't express |
| Prototype or production framework? | LangGraph/CrewAI/AutoGen-class framework for prototyping | Moving to production — many teams build a thin internal framework on top, or extend the OSS one, once requirements stabilize |
| Single agent or multi-agent? | Single agent | Genuine task specialization, parallelism, or fault-isolation need — add the *minimum* number of agents that solves it |

→ Full criteria, orchestration topologies, and framework comparison:
`references/multi-agent-orchestration.md`

## Deliverables

When delivering an agent architecture, provide:

1. **Agent vs. workflow justification** — why this needs dynamic decision-making, not a
   fixed pipeline
2. **Tool inventory** with each tool's purpose and a note on why it's necessary (not just
   available)
3. **Planning/reasoning strategy** chosen, and why
4. **Memory design** (what persists, what doesn't, for how long)
5. **Single- vs. multi-agent decision** and justification if multi-agent
6. **Failure modes considered** and how each is handled (retry, escalate, fail loudly)
7. **Human-in-the-loop gates** on any irreversible or costly action

## References

| File | Topic | Load When |
|------|-------|-----------|
| `references/agent-fundamentals.md` | Agent vs. workflow, agent loop, when agents are/aren't warranted | Deciding whether to build an agent at all |
| `references/tools-and-mcp.md` | Tool design/categories, tool-count trade-offs, MCP host/client/server/transport architecture | Designing what the agent can act on |
| `references/planning-and-reasoning.md` | Planning strategies, decoupling planning from execution, control flow, reasoning patterns and their failure modes | Designing how the agent decides what to do next |
| `references/memory-architecture.md` | Short/long-term memory, vector/semantic memory, working memory, memory management strategies | Designing what the agent remembers across steps/sessions |
| `references/multi-agent-orchestration.md` | Single vs. multi-agent decision, coordination strategies, orchestration frameworks, build-vs-buy | Scaling beyond one agent, or choosing tooling |
| `references/failure-modes-and-safety.md` | Failure taxonomy, evaluation metrics, human-in-the-loop gating, automation-bias prevention | Hardening before launch or debugging a misbehaving agent |
