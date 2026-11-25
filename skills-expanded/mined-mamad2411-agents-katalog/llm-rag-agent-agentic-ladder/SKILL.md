---
name: llm-rag-agent-agentic-ladder
description: The four-rung ladder from an animated @hackproduct9 explainer - LLM (the model on its own), RAG (adds retrieval), AI agent (adds tools in a loop) and agentic AI (adds coordination across agents) - with the rule "each one is the last one plus one capability", when each rung is enough, and what each rung adds in cost and risk. Use when someone asks the difference between an LLM, RAG, an agent and agentic AI, or when deciding how much machinery a task actually needs.
---

# LLM vs RAG vs Agent vs Agentic

Source: an 18-second animated diagram by @hackproduct9, "LLM vs RAG vs Agent vs Agentic: each one is the last one plus one capability". Four stages, one capability added per stage. The explanatory text below is mine; the stage labels and captions are the diagram's.

| Rung | Diagram label | Caption | Adds | Enough when |
|---|---|---|---|---|
| 1 LLM | the model | knows only its training data | nothing: prompt in, answer out | The task needs general knowledge or writing and no fresh or private facts |
| 2 RAG | + retrieval | answers from your docs | a document store the model reads before answering | Answers must come from your own documents |
| 3 AI Agent | + tools in a loop (search, code, API) | acts until the task is done | tools and a loop that repeats until a goal is met | The task needs actions or several dependent steps |
| 4 Agentic AI | + coordination (research, build, review) | many agents, one goal | an orchestrator that divides work among agents | The goal is too big or varied for one agent's loop |

Final frame: model + retrieval + tools + coordination.

## What each rung costs

- **Rung 2:** retrieval quality becomes your accuracy ceiling; bad chunks give confident wrong answers.
- **Rung 3:** every tool is a way to do damage, and loops can run away. Add limits on steps, spend and permissions. [Certain]
- **Rung 4:** coordination multiplies cost and failure points, and errors can compound across agents. Use it only when one agent measurably cannot do the job. [Likely]

## Rule

Climb one rung at a time and stop at the lowest rung that passes your test cases. Related: `agent-repos-week-5` for runtimes, `hallucination-guardrails-6` for checks, `/agent-ladder` to apply it.
