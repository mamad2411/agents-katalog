---
name: architect-before-code
description: Use when a founder says "let's start building", "what's the architecture", "should I just prototype this", "the codebase is a mess", "the AI keeps building a different thing each time", "it worked at ten files and broke at four hundred", "no one holds the system in their head", or an agent-generated prototype is collapsing under growth and nobody named the parts. Triggers on Brain/Memory/Planning/Tools, closed loop, data flywheel, wrapper-or-moat, "is this just a wrapper", and CLAUDE.md/AGENTS.md master-file questions. Produces a filled System Inventory and the committed master file before any code. Skill turns a blank-page prototype into a named system; without it, the agent invents a fresh shape every session.
stage: architect
function: engineering
license: CC-BY-4.0
attribution: AI-Native OS by Adam M. Adamek (Impact Brussels ASBL)
---

# Architect Before Code

AI made prototyping nearly free, which is precisely how it hides the bill. You describe a feature, a
working version appears, and the ease of appearing stops you deciding anything. Hand an agent no
shape and it invents one freshly each session, until six weeks in you run a system no human holds in
their head and no model holds across two conversations. Cheap code did not abolish the cost of bad
architecture. It moved it downstream, where it is dearer. You are the lead systems engineer now. Fix
the shape, write it down, let the agents fill it in after.

## The method

Architect first, then generate. Full framework: Handbook
[Chapter 05](../../handbook/05-architecting-before-code.md). Artefact:
[`SYSTEM-INVENTORY-TEMPLATE.md`](../../masterfiles/SYSTEM-INVENTORY-TEMPLATE.md). The four pillars
expanded, the naming walkthrough, a worked architecture, anti-patterns and a copyable template:
[`references/system-inventory-method.md`](references/system-inventory-method.md).

1. **Write the System Inventory.** Name every moving part before you generate one of them: each model,
   each prompt layer, each tool, each data store, each outside dependency, in one document. An agent
   that can see the whole system stops hallucinating a parallel one. Use the template.
2. **Name the four pillars.** The **Brain** reasons and you rent it at your competitor's price. The
   **Memory** is everything the system knows that the Brain does not: retrieval, vector store,
   master file. **Planning** is how it decides what to do, in order, before it acts. **Tools** are
   how it reaches the world, each call with a blast radius you can name out loud.
3. **Design the closed loop first.** Find the one line where a customer's use today makes the product
   measurably better next month. That line is your moat. Bolt it on last, as most teams do, and you
   have a wrapper. Put it in first; everything downstream either feeds it or robs it.
4. **Write the master file first.** Put `CLAUDE.md` / `AGENTS.md` in the repo before the first
   feature, holding your principles, trade-offs, and the constraints a newcomer would break by
   accident. Add a line each session. The prompt is a performance. The file is a memory.
5. **Decide the fallbacks.** List the answers that must never be wrong, then write the deterministic,
   non-AI route for each. A hallucination in a meme app is a screenshot. The same one on a label is a recall.
6. **Then generate.** Agents build against the inventory, never a blank page. The structure you wrote
   is the score. You know who the conductor is.

## Output

- A filled **System Inventory** (Brain, Memory, Planning, Tools) plus the one closed loop named in a sentence.
- A `CLAUDE.md` / `AGENTS.md` master file committed before the first feature.
- Next: run `agentic-build-loop` to generate against the inventory.

## Constraints

- Architecture before code, always. Generating before the inventory is the faster mess, not the faster company.
- If you cannot say the closed loop in one sentence, you have a wrapper. Fix that before another line ships.
- Stay theme-agnostic; the founder supplies the domain, you supply the rigour.

## Dictionary

[RAG](../../dictionary/02-context-and-sessions.md#rag-retrieval-augmented-generation) ·
[memory system](../../dictionary/02-context-and-sessions.md#memory-system) ·
[plan mode](../../dictionary/04-agentic-patterns.md#plan-mode) ·
[data flywheel](../../dictionary/07-ai-native-business.md#data-flywheel) ·
[the Remove-the-AI test](../../dictionary/07-ai-native-business.md#the-remove-the-ai-test)

## Copy-paste version

> For non-coders: paste into any chatbot or no-code builder (Claude.ai, ChatGPT, Lovable, Bolt, v0).

```
Act as my lead systems engineer. Before I generate any code, design the system on paper.
My product: [ONE_LINER]. Domain: [DOMAIN].
1. Brain: which model reasons, and what cheaper fallback covers bulk or failure?
2. Memory: what does the system know that the model does not - which documents, which retrieval,
   which persistent master file?
3. Planning: how does it decide what to do, in order, before acting? Where does a human approve?
4. Tools: which APIs or actions does it call, and what is the worst case if each one misfires?
5. The closed loop: write the ONE sentence where a customer's use today makes the product better
   next month. If I cannot, tell me I have a wrapper and help me find the loop.
6. List the answers that must never be wrong, and the boring deterministic route for each.
Do not flatter the design. End with the single next action: write my CLAUDE.md master file now.
```
