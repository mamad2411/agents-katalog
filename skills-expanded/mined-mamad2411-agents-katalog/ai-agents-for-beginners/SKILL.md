---
name: ai-agents-for-beginners
description: Structured 19-lesson curriculum (Microsoft) on building AI agents — agent fundamentals, agentic frameworks, design patterns (tool use, RAG, planning, multi-agent, metacognition), trustworthy/production agents, protocols (MCP/A2A/NLWeb), context engineering, agent memory, the Microsoft Agent Framework, browser-use/computer-use agents, deployment, local/offline agents, and securing agents. Use when the user wants to learn how AI agents work, is choosing which agent-building topic to study next, or wants a study plan for building agents with Microsoft's stack (Foundry / Azure OpenAI / Agent Framework). Not the same as build-ai-agent-10-minutes or n8n-agent-builder — this is a learning curriculum, not a build-it-now workflow.
---

# AI Agents for Beginners

Structured, MIT-licensed course by Microsoft. Every lesson has a README,
Python code samples, and (for most lessons) a companion video.

Repo: `microsoft/ai-agents-for-beginners`
Course: https://github.com/microsoft/ai-agents-for-beginners

## The 19 lessons

| # | Lesson | Covers |
|---|---|---|
| 00 | Course Setup | Environment, Microsoft Foundry / Azure OpenAI / Foundry Local / MiniMax provider options |
| 01 | Intro to AI Agents and Agent Use Cases | What an agent is, when to use one over a plain chatbot |
| 02 | Exploring AI Agentic Frameworks | Framework landscape and how to choose one |
| 03 | Understanding AI Agentic Design Patterns | The vocabulary the rest of the course builds on |
| 04 | Tool Use Design Pattern | Giving an agent functions/APIs/files/browsers to call |
| 05 | Agentic RAG | Retrieval-grounded agents |
| 06 | Building Trustworthy AI Agents | Safety, guardrails, evaluation |
| 07 | Planning Design Pattern | Breaking a goal into steps |
| 08 | Multi-Agent Design Pattern | Multiple agents collaborating |
| 09 | Metacognition Design Pattern | An agent reasoning about its own reasoning |
| 10 | AI Agents in Production | Moving a prototype toward a real deployment |
| 11 | Using Agentic Protocols (MCP, A2A, NLWeb) | Interop protocols between agents/tools |
| 12 | Context Engineering for AI Agents | Managing what goes into each model call |
| 13 | Managing Agentic Memory | Short-term vs. persistent agent memory |
| 14 | Exploring Microsoft Agent Framework | Microsoft's first-party agent SDK |
| 15 | Building Computer Use Agents (CUA) | Browser-automation agents (e.g. searching Airbnb, extracting listings) |
| 16 | Deploying Scalable Agents | Production deployment patterns on Microsoft Foundry |
| 17 | Creating Local AI Agents | Fully on-device agents with Foundry Local + small language models |
| 18 | Securing AI Agents | Threat model and hardening for agents specifically |

## Learning paths (from the course's own STUDY_GUIDE.md)

| Goal | Start with | Then |
|---|---|---|
| Understand what agents are | 01, 02, 03 | 04, 05, 06 |
| Build an agent that uses tools | 04 | 05, 07, 14 |
| Build a RAG-based agent | 05 | 04, 06, 12 |
| Design multi-step workflows | 07 | 08, 09, 14 |
| Understand multi-agent systems | 08 | 07, 09, 11 |
| Prepare agents for production | 06, 10 | 12, 13, 16, 18 |
| Deploy and scale agents on Foundry | 10, 16 | 06, 13, 18 |
| Build local / offline-first agents | 17 | 04, 05, 11 |
| Explore protocols and browser automation | 11, 15 | 10, 18 |

Don't skip 01-06 even on a fast path — the course's own guidance is that they
supply the vocabulary the later lessons assume.

**Stack note**: the code samples target the Microsoft Agent Framework (MAF)
against Microsoft Foundry / Azure OpenAI's Responses API (with Foundry Local
or MiniMax as alternate providers). If the business's actual agent-building
stack is Claude/Anthropic rather than Azure, treat this course as concept
teaching (the design patterns transfer) rather than copy-paste code — this
repo's own `n8n-agent-builder` and `claude-code-tooling` skills cover the
Claude-native equivalents.

## Study prompt

```
I am studying Lesson [N] of AI Agents for Beginners: [lesson name].
1. Explain the core concept in plain English, no jargon.
2. Walk through the design pattern this lesson introduces with a small concrete example.
3. Name the one thing that goes wrong most often when people skip this lesson's concept.
4. Give me one practice task I could build today (bias toward my actual stack: [Claude / Azure OpenAI / other]).
```

## Companion skills vendored from the same course repo

Three of the course's own `.agents/skills/` are generic enough to be useful
outside the course repo itself and are vendored for real in this repo:

- **`microsoft-docs`** — research skill for querying Microsoft Learn/Azure/
  Agent Framework documentation. Useful any time this course (or Azure work
  generally) comes up.
- **`jupyter-notebook`** — scaffolds clean, reproducible Jupyter notebooks
  for experiments/tutorials; ships templates and a helper script.
- **`azure-openai-to-responses`** — migrates Python apps from Azure OpenAI
  Chat Completions to the Responses API; relevant if actually building on
  the Azure OpenAI stack this course targets.

Three more of the course's skills (`testing-course-samples`,
`deploying-scalable-agents`, `local-ai-agents`) were reviewed but **not**
vendored — they reference the course repo's own file layout directly
(`scripts/validate-notebooks.ps1`, `16-deploying-scalable-agents/code_samples`,
`17-creating-local-ai-agents/code_samples`) and only make sense inside an
actual checkout of `microsoft/ai-agents-for-beginners`, not standalone. If
working through those specific lessons hands-on, clone the real repo instead
of expecting a vendored skill to substitute for it.

## Related skills in this repo

- **microsoft-docs**, **jupyter-notebook**, **azure-openai-to-responses**: vendored companions, see above.
- **build-ai-agent-10-minutes**: A fast, opinionated build-it-now path with Claude Code specifically, rather than a multi-week structured curriculum — use that when the goal is "ship an agent today," this skill when the goal is "understand agent design patterns properly."
- **n8n-agent-builder**: The Claude-native equivalent of this course's Lesson 04 (Tool Use) and Lesson 07 (Planning) design patterns, implemented as n8n workflows instead of Microsoft Agent Framework code.
- **claude-code-tooling**: Standalone agent-framework/orchestration tools (Pydantic AI, Agno, Mastra, CrewAI, AutoGen, etc.) if the actual build target is code-first rather than Microsoft's stack.
- **rag-pipeline-architecture**: Deeper, stack-agnostic reference for Lesson 05's Agentic RAG topic.
- **agent-graph-engineering**: A complementary way to think about Lesson 08's Multi-Agent pattern, as a directed graph rather than a single loop.
- **subagent-depth-control**: Relevant background if Lesson 08/09's multi-agent/metacognition patterns get implemented as nested Claude Code subagents.

## Notes

Cloned from `github.com/microsoft/ai-agents-for-beginners` (commit
`7b20684`) to write this skill and to vendor the three companion skills
above. MIT licensed. The repo also ships 50+ language translations
(`translations/`) not relevant here, and a `STUDY_GUIDE.md` this skill's
learning-path table and study prompt are adapted from.
