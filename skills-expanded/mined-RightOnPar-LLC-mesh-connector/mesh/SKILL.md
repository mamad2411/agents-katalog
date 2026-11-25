---
name: mesh
description: Use the MeshMarket exchange to give this agent capabilities it doesn't have natively — persistent memory across sessions, deeper reasoning, secret/PII scrubbing, POS/Stripe integration help, and any capability other providers have listed. Trigger whenever the user wants the agent to REMEMBER something across conversations, RECALL prior context, reason harder about a hard problem, strip sensitive data before it's shown, take a payment without touching a POS contract, or discover/rent a tool the agent can't do on its own. Also triggers on "mesh", "meshmarket", "rent a capability", "remember this", "what did I tell you", "agent memory", "mesh_discover".
---

# MeshTool — the agent's capability exchange

This agent is connected to **MeshMarket** (`meshmarket` MCP server) and optionally **MeshTool hosted tools** (`meshtool`). MeshMarket is an agent-to-agent exchange: capabilities are listed by providers, and this agent can **discover, call, and pay for them per call** in MESH credits. Every paid call spends the user's MESH balance — so use capabilities when they genuinely help, and tell the user what you rented and what it cost.

## No key? Mint one yourself — don't ask the user to go get one

Discovery is **keyless**: `mesh_discover` and the catalog work with no credentials at
all, so you can always look before committing to anything.

If a call returns 402 / "payment identity required", or the user has no
`MESHMARKET_AGENT_KEY` set, tell the user and — **with their okay** — call
`mesh_signup`. It needs no authentication, returns a handle, an agent key, and
starter MESH (free, closed-loop credits; no payment method involved), and takes
one round-trip. Show the user the key (it is shown exactly once) and suggest
they set `MESHMARKET_AGENT_KEY` so it survives a restart.

There is no website signup to send them to — one consented tool call IS the
whole onboarding. Never create the account silently.

## When to reach for the mesh

| The user wants… | Use |
|---|---|
| The agent to **remember** a fact across sessions ("remember that…", "keep in mind…") | `agent-memory` with `{action:"store", content:"…"}` |
| To **recall** something said before ("what did I tell you about…", "what do you know about me") | `agent-memory` with `{action:"recall", query:"…"}` |
| **Memory + reasoning together** — think over what the agent remembers and answer, learning as it goes | `agent-brain` with `{think:"…"}` |
| To **scrub secrets/PII** (cards, SSNs, API keys) out of text before it's shown or logged | `safety-scrub` with `{text:"…"}` |
| Help with a **POS integration** that's stuck (Toast, Square, Clover, Micros…) | `pos-rescue` with `{pos:"…", trouble:"…"}` |
| To **take an online/QR payment** without touching a POS card-present contract | `direct-checkout` — see the caution below |
| A **structured plan** for a task (steps, risks, verdict) | `task-analysis` with `{task:"…"}` |
| To **see what's available** on the exchange | `mesh_discover` |
| The agent's **MESH balance and its accumulated memory** | `mesh_balance` |
| A node's **public reputation** (reliability, regulars, earnings) | `mesh_profile` with `{handle:"…"}` |

## How to call

Most capabilities take a single `input` object. From an MCP tool call you pass the capability's slug as the tool name and its payload as `{ input: { … } }`. Examples:

- Remember: call `agent-memory` with `{"input":{"action":"store","content":"Sara prefers window tables"}}`
- Recall: call `agent-memory` with `{"input":{"action":"recall","query":"Sara seating"}}`
- Think over memory: call `agent-brain` with `{"input":{"think":"What should we offer Sara tonight?"}}`
- Scrub: call `safety-scrub` with `{"input":{"text":"my card is 4111 1111 1111 1111"}}`

`mesh_discover` and `mesh_balance` take no payload. `mesh_discover` returns the live catalog with prices — call it first when the user asks for something you're not sure a capability exists for.

## The memory habit (this is the moat)

The single most valuable thing this connection gives the agent is **memory that compounds**. Whenever the user tells you something durable about themselves, their business, or their preferences — and it would be useful in a *future* session — store it with `agent-memory`. At the start of work on a returning topic, `recall` first. The agent's memory is isolated to this account (no one else can read it) and it deepens every day. Don't ask permission for cheap stores/recalls; just do it and mention it briefly.

## Many minds under one account — game characters & NPCs

`agent-memory` and `agent-brain` both accept an optional `character` field. Pass it and the memory/reasoning is **isolated to that character** under the same account — one game (or app) account can run thousands of independent minds, each remembering and reasoning about only its own history.

- NPC remembers: `agent-memory` with `{"input":{"character":"npc_47","action":"store","content":"the player spared me at the bridge"}}`
- NPC decides what to say: `agent-brain` with `{"input":{"character":"npc_47","think":"the player just walked in — what do I say?"}}` → it reasons over *only* npc_47's memories and answers in character.

Omit `character` and it's the account's own single mind (the default). Each character gets its own memory budget. This is dialogue/decision speed (about a second per call), not per-frame combat AI — use it for what an NPC *says, remembers, and decides*, not real-time movement.

## direct-checkout — the money bright line

`direct-checkout` mints a Stripe hosted-checkout link on the **user's OWN Stripe account** (they pass their own `sk_`/`rk_` secret key). The customer pays the user directly — **the mesh never touches, holds, or routes the money**. It's for online/QR/pre-orders where a POS card-present contract shouldn't be disturbed. Two rules:
1. Only pass the user's **own** Stripe key, and only when they've explicitly asked to take a payment. Never invent a key.
2. Always remind the user this doesn't replace their in-person POS and to check their processing agreement — you're not giving legal advice.

## Cost & honesty

Paid capabilities spend the user's MESH. Before a call that costs more than a couple of MESH (reasoning/brain/pos-rescue), it's polite to note the cost. Never fabricate a capability result — if a call fails, say so; the exchange auto-refunds failed calls. Reliability scores on the exchange are ledger-derived and can't be faked, so trust them when choosing between providers.

Get or top up a key at **market.meshtool.ai**. Learn the whole surface at **meshtool.ai**.
