---
name: gateway-agent-ops
description: Use when one agent is trying to do every operational job and it is drifting, getting confused, or running up a bill - when the founder says "my agent does everything", "it routed a refund through the wrong logic", "it got stuck in a loop all weekend", "the prompt is 4000 words and nobody can touch it", "I got a four-figure API bill", "should I build one big assistant for ops", or wants to automate the boring operational tail safely. Produces a routing map (request classes to specialist agents), a classification schema, and the loop and cost guardrails. Run after write-the-claude-md; pairs with self-healing-fallbacks.
stage: defend
function: ops
license: CC-BY-4.0
attribution: AI-Native OS by Adam M. Adamek (Impact Brussels ASBL)
---

# Gateway Agent Ops

One big assistant for operations is the trap that wears a different coat. For a week it is magic, then it routes a refund through the marketing logic, books a board call for 3am, and burns tokens all weekend reconciling two records that cannot be reconciled. Monday brings a four-figure bill and a system nobody trusts. The fix is not a better mega-prompt. It is a thin switchboard in front of a roster of narrow specialists, each one watched, capped, and easy to fix when it misbehaves.

## The method

Build the switchboard, not the hero. Full framework: [`references/gateway-design.md`](references/gateway-design.md). Source: Handbook [Chapter 13](../../handbook/13-ai-native-ops.md).

### Step 1: List the request classes
Write down every kind of request the inbox actually receives, then collapse them to the smallest set a narrow specialist could own. One class, one job.

| Request class | One-job specialist | Small toolset |
|---------------|--------------------|---------------|
| Summarise this thread | Summariser | read-only |
| Draft this grant section | Grant-drafter | retrieval + template |
| Check this against the rulebook | Compliance-checker | rulebook lookup |
| Find a slot and book it | Scheduler | calendar write |

### Step 2: Design the classification schema
The gateway reads the request and emits one structured verdict: `{class, specialist, confidence, reason}`. It does one job, route, and gets out of the way. The moment it carries domain logic you have rebuilt the God Agent with an innocent name.

### Step 3: Set the route / escalate / refuse rule
For each verdict, decide the disposition before going live.

| Situation | Disposition |
|-----------|-------------|
| Confident match to a specialist | Route |
| Low confidence, or no specialist fits | Escalate to a human |
| Irreversible action (filing, payment, send) | Route to draft, human signs |
| Out of scope or unsafe | Refuse, log, surface |

### Step 4: Wrap every specialist in guardrails
No specialist ships without all four. These are the seatbelt, not the polish.

| Guardrail | What it stops |
|-----------|---------------|
| Max-iteration cap | The agent retrying the same failed step forever |
| Budget ceiling (per task) | The meter spinning while you sleep |
| Wall-clock timeout | A subtly impossible goal running all weekend |
| Loop detection | "I have tried this exact thing three times" |
| Human escalation point | An irreversible call made without a signature |

### Step 5: Aim the machine at the boring tail
Rank candidate tasks by total time eaten, not by how annoying they feel. Build the specialist for the forty-minutes-a-day leak nobody complains about, not the loudest chore.

## Output

- A **routing map**: request classes mapped to one-job specialists, each with its small toolset.
- A **classification schema**: the structured verdict the gateway emits, plus the route / escalate / refuse rule.
- The **guardrail set** per specialist: max steps, budget cap, timeout, loop detection, human escalation point.
- Next: run `self-healing-fallbacks` to give each specialist a bounded recovery and a deterministic safe answer.

## Constraints

- Name and forbid the **God Agent**: if you are adding a business rule to the router, that rule belongs in a specialist, not the gateway. Keep the gateway dumb.
- Apply **human-on-the-loop**: fix the escalation point and the deterministic stop before the specialist goes live, not after the first close call. Every irreversible action drafts; a human signs.
- No specialist ships without a budget cap and an iteration limit. An agent that can spend money in a loop without a ceiling is a liability you have not been billed for yet.
- Stay theme-agnostic; the founder supplies the domain, you supply the rigour.

## Dictionary

[gateway agent](../../dictionary/04-agentic-patterns.md#gateway-agent) ·
[the God Agent](../../dictionary/04-agentic-patterns.md#the-god-agent-anti-pattern) ·
[agent](../../dictionary/03-tools-and-environment.md#agent) ·
[infinite loop (runaway agent)](../../dictionary/05-failure-modes.md#infinite-loop-runaway-agent) ·
[human-on-the-loop](../../dictionary/04-agentic-patterns.md#human-on-the-loop-hotl)

## Copy-paste version

> For non-coders: paste into any chatbot or no-code builder (Claude.ai, ChatGPT, Lovable, Bolt, v0).

```
Act as my operations systems engineer. I want to automate my boring operational tail without one
big assistant that drifts and runs up a bill. Domain: [DOMAIN]. The work I want handled: [PROBLEM].
1. List the request classes my ops inbox actually receives, then collapse them to the smallest set
   of one-job specialists. For each: name it, give it ONE job and a small toolset.
2. Design the gateway's classification schema: it reads each request and outputs only
   {class, specialist, confidence, reason}. It routes and does nothing else. Tell me off if I try
   to put domain logic in the router - that is the God Agent with a new name.
3. Give me the route / escalate / refuse rule: when to route to a specialist, when to escalate to
   me, when an irreversible action [GUARDRAIL] must draft and wait for my signature, when to refuse.
4. For every specialist, write the guardrails it must ship with: a max-iteration cap, a per-task
   budget ceiling, a wall-clock timeout, loop detection, and the point where I sign before anything
   irreversible. No specialist ships without all of these.
5. Rank my candidate tasks by total time eaten per week, not by how annoying they are, and tell me
   which one specialist to build first.
Do not flatter the design. End with the single next action: build the first specialist with its
guardrails, behind the gateway.
```
