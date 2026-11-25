---
name: ai-assisted-sales
description: Use when a founder is stuck in pilot purgatory, when deals go quiet after a thrilled champion says yes, when they say "the pilot stalled", "they loved the demo but procurement went dark", "how do I get from pilot to paid", "we keep automating spam", "scale sales without hiring", or they are about to put a pilot logo on a fundraising slide as if it were revenue. Also when one human is drowning in routing, follow-up, and CRM entry. Produces a sales-motion map (stages plus where agents help), a pilot-design template that writes the success bar and path to paid before the pilot starts, and the pilot-to-paid gate. Run after design-the-mva; pairs with gateway-agent-ops for the routing spine.
stage: grow
function: growth
license: CC-BY-4.0
attribution: AI-Native OS by Adam M. Adamek (Impact Brussels ASBL)
---

# AI-Assisted Sales

Most of the work that loses you deals is not the selling. It is the connective tissue: reading the lead, pulling the case study, drafting the reply, logging it, setting the reminder. Hand that to a system that runs at three in the morning and your scarce humans show up only where judgement is required. But there is a deadlier trap. A demo books a pilot, the pilot earns a logo, the logo raises a round, and a signature got counted as revenue. A pilot is branded curiosity, not a contract. The core move: design every pilot with a written success bar and a path to paid before it starts.

## The method

Map where money moves, automate the middleware, and gate every pilot to paid. Full framework: [`references/sales-motion.md`](references/sales-motion.md), drawn from handbook [Chapter 11](../../handbook/11-ai-assisted-sales.md).

### Step 1: Map the path a dollar takes

Write the real sequence from first contact to signed and supported, the way it happens today. Mark each step with one word: where an agent helps, and where a human must stay.

| Stage | Agent role | Human gate |
| --- | --- | --- |
| Qualify | read, score, route the lead | none |
| Scope | gather context, pull the case study, draft | the message that goes out |
| Pilot | run the agreed test, log signals | the success-bar call |
| Prove | compose the pilot report, run checks | verify before it ships |
| Expand | draft the renewal, surface usage | the close and the money |

### Step 2: Draw the line and automate one step

Everything below the trust line runs as software; everything above it stays a person. Automate the single step that is most repetitive, most often where deals go cold, and lowest-risk to hand off. That one step is your first revenue agent, not the whole pipeline.

### Step 3: Design the pilot with the bar set first

Before the pilot starts, write the success metric, the timebox, and the path to paid. No open-ended pilots. Use the pilot-design template in the reference.

| Pilot field | Set before start |
| --- | --- |
| Success metric | the one number that converts to a yes |
| Timebox | the date the pilot ends, fixed |
| Path to paid | the contract terms a pass triggers |
| Gate map | the procurement, security, compliance owners who must sign |

### Step 4: Build the buyer's gate map

On day one, ask the champion who in procurement, security, and compliance must sign, and where each stands today. A pilot with all three mapped and moving is a deal. A thrilled champion and three blanks is a press release waiting to expire.

### Step 5: Put the human gate at the send, and the money

Route, qualify, gather, log, and schedule unattended. Keep a human on the act that touches your name: the message going out and the money going out. An agent that drafts is a force multiplier; one that issues a refund to the wrong account is a liability that bills you.

## Output

- A **sales-motion map**: the real stages, with each marked human or middleware, and the one step automated first.
- A **pilot-design template** filled for one live pilot: success metric, timebox, path to paid, gate map.
- The **pilot-to-paid gate**: pilots and contracts in separate columns, with conversion tracked as its own number.
- Next: stand up the routing spine with `gateway-agent-ops`, then `capture-learning` on the first pilot result.

## Constraints

- Name the failure mode: the open-ended pilot with no success metric. A pilot without a written bar and a path to paid is where deals go to look alive while they die. Forbid it.
- Apply human-on-the-loop: automate the middleware, never the decision to trust a vendor or release a budget, and never automate spam. The human gate sits at the send and the money.
- Stay theme-agnostic; the founder supplies the domain and the real buyer. Never invent a customer, a pilot result, or a figure.

## Dictionary

[gateway agent](../../dictionary/04-agentic-patterns.md#gateway-agent) ·
[decoupling headcount from revenue](../../dictionary/07-ai-native-business.md#decoupling-headcount-from-revenue) ·
[the six-pillar trust substrate](../../dictionary/06-evaluation-and-safety.md#the-six-pillar-trust-substrate) ·
[data flywheel](../../dictionary/07-ai-native-business.md#data-flywheel)

## Copy-paste version

> For non-coders: paste into any chatbot or no-code builder (Claude.ai, ChatGPT, Lovable, Bolt, v0). Tag: `build`.

```
Act as my AI-native revenue-operations architect. Product: [ONE_LINER]. For: [ICP]. Domain:
[DOMAIN]. My riskiest live pilot: [PILOT]. My binding limit: [CONSTRAINT].

1. Map the real path a dollar takes, first contact to signed and supported, as it happens today.
   Mark each step HUMAN (the call, the close, the trust) or MIDDLEWARE (routing, summarising,
   drafting, logging). Tell me how much of my sales day is middleware in disguise.
2. Circle the ONE middleware step to automate first: most repetitive, most often where deals go
   cold, lowest-risk to hand off. That is my first revenue agent. Do not automate the whole pipeline.
3. Design my pilot with the bar set BEFORE it starts: the one success metric that converts to a
   yes, a fixed end date, and the exact contract terms a pass triggers. No open-ended pilots.
4. Build my buyer's gate map: name who in procurement, security, and compliance must sign, and ask
   me where each stands today. Tell me which blanks make this a press release, not a deal.
5. Put the human gate at the message going out and the money going out, nowhere else. Tell me which
   steps run unattended and which need my hand.

CONSTRAINTS: a pilot is not revenue; no pilot without a success metric and a path to paid; never
automate the trust decision or spam. OUTPUT: a sales-motion map, a filled pilot-design template,
and the pilot-to-paid gate, then ONE next action.
```
