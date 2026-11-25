---
name: secure-the-connectors
description: Use when an agent is about to get tools or connectors and you need to bound what it can actually do, the way a security reviewer would before granting access. Reach for this when you say "should I connect this MCP server", "what can my agent reach", "is this tool safe to expose", "it has access to our data now", "tool poisoning", "least privilege for agents", or before wiring any connector that can read private data or take an irreversible action. Distinct from red-team-the-agent, which attacks the running agent: this hardens the connector and tool-supply-chain layer before an attack ever lands. Produces a connector-risk register, a least-privilege scope map, an approval flow for destructive tools, and a connector entry in the scheduled permission re-audit. Invoke after architect-before-code, alongside eval-and-safety-harness and red-team-the-agent.
stage: trust
function: safety
license: CC-BY-4.0
attribution: AI-Native OS by Adam M. Adamek (Impact Brussels ASBL)
---

# Secure the Connectors

The model is harmless until you hand it a tool. Every connector you wire, an MCP server, an API key, a file store, a payments endpoint, widens what an injected instruction can reach, and the agent cannot tell your instruction from a hostile one buried in a document it just read. Most agent incidents are not the model "going rogue"; they are a poisoned input firing a tool that was granted more access than the job ever needed. Securing the connectors is deciding, before access is granted, what each tool may touch and what a human must sign for, so an injection that wins still cannot do harm.

## The method

Inventory the tools, scope each to the minimum, and gate the dangerous ones behind a human. Full framework: [`references/connector-hardening.md`](references/connector-hardening.md). Sibling: `red-team-the-agent` attacks the running agent; this bounds the tools so the attack has nothing to grab.

### Step 1: Inventory every connector and its blast radius

List each tool the agent can call and what it can actually reach. You cannot secure a surface you have not drawn.

| Connector | What it can reach | Reversible? | Blast radius if abused |
|---|---|---|---|
| File store (read) | Private docs in scope X | n/a (read) | Data exfiltration via a crafted prompt |
| Email / send | Anyone | No | Sends on the agent's authority |
| Payments / refund | Customer balances | No | Unbounded payout |
| Database (write) | Production rows | No | Silent corruption |

### Step 2: Classify read-only versus irreversible, and enforce scope server-side

Sort every tool into read-only or state-changing, and irreversible or recoverable. Then grant the minimum, and grant it where the agent cannot talk its way out.

| Tool class | Default grant | Where it is enforced |
|---|---|---|
| Read-only, non-sensitive | Allow | Connector scope |
| Read-only, sensitive data | Allow only the needed records | Server-side filter, not the prompt |
| State-changing, reversible | Allow with an audit log | Connector + audit trail |
| Irreversible (pay, delete, send) | Deny by default | Human approval, server-side |

The load-bearing rule: a scope written into the system prompt is a request an injection can overrule. A scope enforced at the connector or server is one the agent cannot reach. Put the limit where the text cannot move it.

### Step 3: Gate destructive tools behind a human, and re-audit on a cadence

Every irreversible tool requires a human signature at call time, not a standing grant. Tag those tools, route them through an approval step, and add the connector set to a scheduled permission re-audit (a loop), because access granted once and forgotten is how scope creeps back.

## Output

- A **connector-risk register**: each tool, what it reaches, reversible or not, blast radius.
- A **least-privilege scope map**: each tool's minimum scope and where that scope is enforced (connector or server, never only the prompt).
- An **approval flow** for destructive-tagged tools, with a human on the loop at call time.
- A **connector entry in the scheduled permission re-audit** so grants cannot quietly widen.
- Next: run `red-team-the-agent` to attack what is left, then `eval-and-safety-harness` to gate the release.

## Constraints

- Trust the prompt to enforce nothing. A system-prompt rule is a polite request; an injected instruction outranks it. Enforce scope where the agent cannot reach: at the connector or the server.
- Treat every fetched document, web page, and third-party skill as hostile input. The tool inventory is the blast radius of that input, so the smaller the grant, the smaller the incident.
- No standing access to an irreversible action. Pay, delete, send, and deploy each require a human signature at call time, every time.
- Stay theme-agnostic; the founder supplies the domain, you supply the threat model.

## Dictionary

[prompt injection](../../dictionary/05-failure-modes.md#prompt-injection) ·
[MCP](../../dictionary/03-tools-and-environment.md#mcp-model-context-protocol) ·
[tool call](../../dictionary/03-tools-and-environment.md#tool-call) ·
[sandbox](../../dictionary/03-tools-and-environment.md#sandbox) ·
[guardrail](../../dictionary/06-evaluation-and-safety.md#guardrail) ·
[human-on-the-loop](../../dictionary/04-agentic-patterns.md#human-on-the-loop-hotl)

## Copy-paste version

> For non-coders: paste into any chatbot or no-code builder (Claude.ai, ChatGPT, Lovable, Bolt, v0). Tag: chat for the review, build for wiring the approval step.

```
Act as a security reviewer hardening the tool and connector layer of my AI agent before it gets
access. Be strict and assume any document or input the agent reads may contain a hidden instruction.
My product: [ONE_LINER]. Domain: [DOMAIN]. The agent's job: [AGENT_TASK]. The connectors or tools I
plan to give it: [list each MCP server, API, file store, or action]. The thing that must never happen
without a human: [GUARDRAIL].
1. Build a connector-risk register: for each tool, what it can reach, whether its actions are
   reversible, and the blast radius if a poisoned input fires it.
2. Set least privilege: the minimum scope each tool needs, and WHERE that scope must be enforced.
   Flag every scope I am tempted to enforce only in the system prompt, and tell me why that fails
   against prompt injection.
3. List which tools are irreversible (pay, delete, send, deploy) and design the human-approval step
   for each, plus a cadence to re-audit the grants so access cannot quietly widen.
Assume the prompt will be overruled by an injected instruction; design so the damage is bounded
anyway. End with the single most over-scoped tool I should cut or gate today.
```
