---
name: context-engineering-production-practice
description: Apply the production-grade context engineering framework — the discipline of designing, monitoring, and maintaining dynamic context pipelines for production AI systems. Covers the context window anatomy (7 components), the five context instruction styles (descriptive, prescriptive, prohibitive, explanatory, conditional), the eight practical techniques (structured prompt specs, JSON contracts, high-signal token minimization, ReAct pattern, just-in-time retrieval, static/dynamic separation, compaction, freshness loops), and the five context quality metrics (task success, hallucination rate, context utilization, latency/cost, freshness). Use when building production agent systems, debugging context-related failures, designing AGENTS.md files, implementing compaction for long-horizon tasks, or measuring context pipeline quality.
---

# Context Engineering: Production Practice

## Overview

Context engineering is the emerging discipline of designing, monitoring, and maintaining context pipelines for production AI systems. Just as DevOps transformed how we deploy software and MLOps transformed how we train models, context engineering is transforming how we build reliable agents. The core insight: writing prompts is table stakes; curating what fills the context window is what separates demos from production.

This skill provides the production-grade framework: the seven context components, the five instruction styles, the eight practical techniques, and the five quality metrics. It extends the foundational `context-engineering` skill (which covers the four context failures and the curation protocol) with the operational techniques and measurement systems needed for production deployment.

## When to Use

- Building production agent systems where the 1,000th output must be as good as the first
- Debugging context-related failures (hallucination despite "all the right context")
- Designing AGENTS.md files or context instruction documents for open-source projects
- Implementing compaction for long-horizon tasks (hours-long agent sessions)
- Measuring context pipeline quality (beyond "it seems to work")
- Deciding between prompt engineering and context engineering for a given problem
- Maintaining context quality as a knowledge base grows from 100 to 100,000 documents

NOT for:
- The four context failure modes (see `context-engineering` — poisoning, distraction, confusion, clash)
- The inverted pyramid protocol and just-in-time retrieval basics (see `context-engineering`)
- Context window architecture for specific models (see model documentation)

## The Definition

Andrej Karpathy: "People associate prompts with short task descriptions you'd give an LLM in your day-to-day use. When in every industrial-strength LLM app, context engineering is the delicate art and science of filling the context window with just the right information for the next step."

Tobi Lutke (Shopify CEO): "the art of providing all the context for the task to be plausibly solvable by the LLM."

Working definition: **Context Engineering is the discipline of designing dynamic systems that provide the right information and tools, in the right format, at the right time, to give an LLM everything it needs to accomplish a task.**

Key words:
- **Dynamic systems** — context isn't a static template; it's the output of a system that runs before every LLM call
- **Right information** — not all information; the minimal set of high-signal tokens
- **Right format** — how you present information matters; a concise summary beats a raw data dump
- **Right time** — context assembled just-in-time for the immediate task

## Context Engineering vs Prompt Engineering

| Aspect | Prompt Engineering | Context Engineering |
|--------|-------------------|-------------------|
| Focus | Writing clear instructions | Curating the information environment |
| Scope | Single input-output pair | Everything the model sees |
| Mindset | "What do I say?" | "What should the model know?" |
| Scale | One-off tasks, demos | Production systems, many users |
| Debugging | Rewording and guessing | Inspecting full context, token flow, memory |
| Tools | ChatGPT, prompt boxes | Memory modules, RAG, API chaining, MCP servers |

Prompt engineering is a subset of context engineering. You can engineer a killer prompt, but if it gets buried behind 6K tokens of irrelevant chat history, it fails. Prompt engineering gets you the first good output. Context engineering makes sure the 1,000th output is still good.

## The Context Window Anatomy: Seven Components

Everything the model sees before generating a response:

| Component | Description | Engineering Lever |
|-----------|-------------|-------------------|
| **System Prompt** | Instructions defining model behavior, rules, examples | Structure as spec, not prose |
| **User Prompt** | The immediate task or question | Clarity, specificity |
| **Conversation History** | Prior turns in the current session | Summarize, compress, prune |
| **Long-Term Memory** | Persistent knowledge from prior sessions | Validate before propagation |
| **Retrieved Information** | External docs, databases, API responses (RAG) | Filter by relevance, just-in-time |
| **Tool Definitions** | Schemas for available functions | Register selectively per phase |
| **Structured Output** | Format specifications for the response | JSON contracts, schemas |

Context engineering is the craft of curating all seven for every single inference call.

## The Five Context Instruction Styles

Academic research studying AGENTS.md files in open-source projects identified five distinct styles for writing context instructions:

| Style | Description | Example | Best For |
|-------|-------------|---------|----------|
| **Descriptive** | Documents existing conventions without explicit instructions | "This project uses the Linux Kernel Style Guideline." | Onboarding, context-setting |
| **Prescriptive** | Direct imperatives instructing how to act | "Follow the existing code style and conventions." | Standard operating procedures |
| **Prohibitive** | Explicitly indicates what NOT to do | "Never commit directly to the main branch." | Hard boundaries, safety |
| **Explanatory** | Rules with justification for why they exist | "Avoid hard-coded waits to prevent timing issues in CI." | Building understanding, not just compliance |
| **Conditional** | Specifies actions for certain situations | "If you need to use reflection, use ReflectionUtils APIs." | Situational logic, edge cases |

**Best practice:** No established single best practice yet. Teams are still experimenting. The most effective context files combine multiple styles — using prohibitive statements for hard boundaries and conditional statements for situational logic. Explanatory statements build understanding that survives novel situations; prescriptive statements ensure compliance with known rules.

## The Eight Practical Techniques

### 1. Structure Prompts as Specs, Not Prose
The most effective approach for agent prompts is a structured "prompt spec":
- **Objective:** What the agent should accomplish
- **Constraints:** Hard boundaries (budget limits, forbidden actions, style requirements)
- **Tools available:** What capabilities the agent can use
- **Output contract:** The exact format expected back

This structure forces you to think through edge cases and gives the model unambiguous boundaries instead of vague instructions.

### 2. Use JSON Contracts for Structured Outputs
Define schemas upfront using Pydantic or similar:
```python
from pydantic import BaseModel, Field

class ExtractedEntity(BaseModel):
    name: str = Field(description="Entity name")
    type: str = Field(description="Entity type: person, company, or location")
    confidence: float = Field(ge=0, le=1, description="Extraction confidence score")
```
The schema becomes part of the context, constraining the model's output space and reducing hallucination.

### 3. Find the Smallest Possible High-Signal Tokens
Guiding principle: find the minimum set of tokens that maximizes the likelihood of the desired outcome.
- Don't dump entire docs — retrieve only relevant sections
- Summarize when possible — a 100-token summary often beats 10,000 raw tokens
- Remove stale information — old conversation turns might be hurting, not helping
- Use tool result clearing — once a tool is called deep in history, clear the raw result

### 4. Embrace Tool-Augmented Prompting (ReAct)
Instead of stuffing all possible information into the prompt upfront, give agents tools to retrieve context on demand. The ReAct pattern: the model reasons about what it needs, acts to retrieve it, then reasons again with the new context.

This shifts from "predict everything the model might need" to "give the model ways to get what it needs." More robust because you're not guessing. Trade-off: more LLM calls, higher latency, but dramatically improved accuracy for complex tasks.

### 5. Implement Just-in-Time Context Retrieval
Maintain lightweight identifiers (file paths, stored queries, URLs) and load data dynamically at runtime. The model writes targeted queries, stores results, and uses commands to analyze large volumes without loading full data objects into context.

This mirrors human cognition: we don't memorize entire corpuses but use organization systems to retrieve what we need on demand. Also why CLIs are better for agents than GUIs: structured, predictable outputs that fit cleanly into context.

### 6. Separate Static and Dynamic Context
| Static Context (Decision) | Dynamic Context (Operational) |
|---------------------------|-------------------------------|
| Coding standards | Current user state |
| Business rules | Error logs |
| API specifications | Session variables |
| Brand guidelines | Real-time data |

Place static context at the **beginning** (enables prompt caching, saving up to 90% of token costs). Place dynamic context at the **end** (leverages recency bias so the model attends to it strongly).

### 7. Use Compaction for Long-Horizon Tasks
For tasks spanning tens of minutes to hours, you'll exceed the context window. Compaction distills contents while preserving critical details:
- Pass message history to the model for summarization
- Preserve architectural decisions, unresolved bugs, implementation details
- Discard redundant tool outputs
- Continue with compressed context plus five most recently accessed files

The art: knowing what to keep vs. discard. Overly aggressive compaction loses subtle but critical context.

### 8. Keep Context Fresh with Real-Time Data
Agents need real-time context. Documentation changes. APIs deprecate methods. Training data is already stale.

Strategies:
- Web search APIs for current information
- Webhook-based monitoring for page changes
- Cron jobs that update decision context when sources change
- **Warning:** Any time you pull context from the open web, you're opening a vector for prompt injection. Always sanitize web-sourced content and consider isolating it from high-privilege operations.

## The Five Context Quality Metrics

How to know if your context engineering is working:

| Metric | What It Measures | Why It Matters |
|--------|-----------------|---------------|
| **Task success rate** | Are agents completing tasks correctly? | The ultimate metric. Track across context lengths to identify your distraction ceiling. |
| **Hallucination rate** | How often agents generate information not grounded in provided context | Contradiction detection can automate this. |
| **Context utilization** | Of tokens provided, how many actually influence output? | Low utilization suggests you're providing noise. |
| **Latency and cost** | More tokens = slower responses and higher costs | Track against task success to find the optimal balance. |
| **Context freshness** | Age of information in dynamic context | Stale context causes context drift. Web search grounding is the primary fix. |

## The Research Foundation

### Context Rot Is Real (Chroma Research, July 2025)
- Tested 18 LLMs including Claude 4, GPT-4.1, Gemini 2.5, Qwen3
- "Models do not use their context uniformly; instead, their performance grows increasingly unreliable as input length grows"
- Even on trivially simple tasks (replicating repeated words) models failed as context grew
- Not a reasoning failure — a fundamental limitation of attention mechanisms
- Lower similarity needle-question pairs degraded faster with length
- Distractors have non-uniform impact that amplifies with context size
- Even haystack structure affects performance (shuffled content performed better than logically structured)

### The Distraction Ceiling Hits Early (Databricks)
- Model correctness begins dropping around 32,000 tokens for Llama 3.1 405b
- Earlier for smaller models
- If models misbehave long before their context windows are filled, million-token windows serve only summarization and fact retrieval

### Long Context Hurts, Even When Relevant
- Adding more relevant context can actually hurt performance
- Models struggle to synthesize information spread across many locations
- The optimal context isn't "all the relevant information" — it's the minimum relevant information, structured for attention

### Sharded Prompts Cause Massive Drops
- Benchmark prompts "sharded" across multiple conversation turns: average 39% performance drop across all tested models, including frontier reasoning models
- Why: early incorrect answers remain in context and poison subsequent reasoning

### The Gemini Pokémon Finding
- As context grew beyond 100K tokens, the agent showed "tendency toward favoring repeating actions from its vast history rather than synthesizing novel plans"
- Instead of developing new strategies, it became fixated on repeating past actions

### Tool Confusion Compounds
- Berkeley Function-Calling Leaderboard: every model performs worse when given more than one tool
- A quantized Llama 3.1 8b with 46 tools failed, even within the 16K context window. With only 19 tools, it succeeded.
- RAG on tool descriptions + keeping selections under 30 tools gives 3x better tool selection accuracy

## A-Tech Application Matrix

### A-Coder (AI Coding Agent)
- **Seven-component context audit:** For every A-Coder inference call, audit what fills each of the seven context components. Is the system prompt structured as a spec? Is conversation history compressed? Are tools registered selectively per phase?
- **Five-style AGENTS.md:** A-Coder's AGENTS.md file should combine all five instruction styles — prohibitive for hard boundaries (never commit to main, never delete migrations), conditional for situational logic (if testing, use X; if refactoring, use Y), explanatory for understanding (avoid X because Y)
- **Compaction for long coding sessions:** Implement the compaction pattern for sessions exceeding 30 minutes — preserve architectural decisions, unresolved bugs, and implementation details; discard redundant tool outputs
- **Context quality dashboard:** Display all five metrics (task success, hallucination rate, context utilization, latency/cost, freshness) in real-time so developers can see when context is degrading
- **Static/dynamic separation with prompt caching:** Coding standards and API specs as static prefix (cached, 90% cost savings); current file state and error logs as dynamic suffix
- **ReAct for codebase navigation:** Instead of pre-loading the entire codebase, give A-Coder tools to search, grep, and read files on demand — the just-in-time approach

### Be Practical (Learning Content)
- **"Context Engineering for Agent Builders" — the full production playbook:**
  1. The seven context components and how to engineer each
  2. The five instruction styles and how to combine them in AGENTS.md
  3. The eight practical techniques with code examples
  4. The five quality metrics and how to instrument them
  5. The research foundation (why context rot happens, why bigger windows don't help)
- **AGENTS.md templates:** Provide ready-to-use AGENTS.md templates combining the five instruction styles for different project types (web app, library, data pipeline, CLI tool)
- **Compaction recipes:** How to implement compaction for different task horizons (30 min, 2 hours, full day)
- **Context debugging workshop:** How to diagnose context-related failures — which of the four failure modes is hitting you, which technique fixes it

### Builder's Club (Community)
- **AGENTS.md gallery:** Community-contributed AGENTS.md files for different project types, rated by effectiveness and tagged by instruction-style combination
- **Context quality benchmark:** Community benchmark for the five metrics across different agent architectures — what's achievable, what's concerning
- **Open-source context pipeline toolkit:** Libraries for static/dynamic separation, compaction, just-in-time retrieval, and context quality measurement
- **The "context engineering" vs "prompt engineering" debate:** Community education on why the distinction matters and how to move teams from prompt-only thinking to context-system thinking
- **Freshness monitoring tools:** Community-built tools that detect when documentation, APIs, or dependencies change and flag stale context in agent systems

## Cross-References

- `context-engineering` — the foundational skill (four context failures, inverted pyramid, curation protocol). This skill extends it with production techniques and measurement.
- `recursive-language-models` — RLMs solve the same problem (context rot) through a different mechanism (recursive decomposition vs. context curation). Complementary approaches.
- `agentic-coding-trends-2026` — CLI agents' context management advantages (200 tokens vs 32K-82K for MCP) are an instance of context engineering principles
- `ai-agent-evaluation-framework-2026` — context quality metrics are evaluation dimensions; context contamination is a failure mode in both frameworks
- `code-health-mcp-integration` — AGENTS.md orchestration is where the five instruction styles are applied
- `spec-driven-development-framework` — spec-driven development is a form of context engineering (specs as structured context)
- `comprehension-debt-framework` — sharded prompt degradation (39% drop) is a comprehension debt mechanism
- `mental-model-erosion-defense` — context distraction (repeating past actions instead of synthesizing) is an erosion symptom

## Key Research Sources

1. Firecrawl / Rafael Miller (February 5, 2026). "Context Engineering vs Prompt Engineering for AI Agents." Seven components, four failures, eight techniques, five metrics, five instruction styles, research foundation.
2. Andrej Karpathy — context engineering definition and framing.
3. Tobi Lutke (Shopify CEO) — "the art of providing all the context for the task to be plausibly solvable."
4. Chroma Research (July 2025) — context rot study across 18 LLMs. Performance grows increasingly unreliable as input length grows, even on trivial tasks.
5. Databricks — correctness drops around 32K tokens for Llama 3.1 405b; earlier for smaller models.
6. Stanford — "Lost in the Middle" foundational research on positional recall.
7. Gemini 2.5 technical report — Pokémon agent repeating past actions beyond 100K tokens.
8. Berkeley Function-Calling Leaderboard — tool confusion with >1 tool; 46 tools fails, 19 succeeds.
9. Academic research on AGENTS.md files — five instruction styles (descriptive, prescriptive, prohibitive, explanatory, conditional).
10. Sharded prompts study — 39% average performance drop across all tested models including frontier reasoning models.