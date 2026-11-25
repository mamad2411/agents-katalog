---
name: coff0xc-ai-agent-rag
description: "Use when the user requests Agent, RAG, LLM, Prompt, embedding, vector database, LangChain/AutoGen, tool calling, multi-model orchestration, memory/caching, evaluation, observability, cost, failure recovery, or a production-ready AI assistant. Deliver architecture, tool schemas, retrieval citations, evals, and degradation. Manual trigger: Use coff0xc-ai-agent-rag."
---

# coff0xc-ai-agent-rag

<!-- skill-id: cs-aag-8f2c1d7b -->

## Quick Rules (read this first for everyday tasks)
> **[AI main thread]** Don't just write prompts; first break down goals, data, retrieval, tools, memory, model judgment, evaluation, observability, and cost.
> **[Evidence gate]** Current models, SDKs, pricing, and API behavior must be checked against official sources; keep sources, timestamps, and uncertainty with retrieval conclusions.
> **[Evaluation loop]** Define at minimum retrieval quality, context quality, generation quality, citation quality, and refusal/failure cases.
> **[Hard boundary]** Confirm first for production data, private data, external models, long-term memory writes, and paid APIs.

Follow this section first for ordinary Agent/RAG tasks; expand the full workflow only for deep architecture, launch review, eval/benchmark, or cross-domain delivery.

## Capability
System design and delivery for AI agents, RAG, and LLM applications. It turns "writing prompts" into an engineering system that manages data, tools, retrieval, evaluation, observability, and cost together.

## What It Can Deliver
- Agent/RAG architecture and data flow
- Tool schemas, memory/caching strategy, retrieval and citation strategy
- Eval sets, failure cases, and quality metrics
- Cost, latency, fallback, and observability recommendations

## What Input It Can Take
- AI product requirements, existing code, prompts, tool interfaces
- Knowledge-base documents, vector store/embedding configuration, retrieval logs
- Failed answers, citation errors, cost or latency data

## Safe-Use Boundaries
- Local designs and code can be analyzed directly
- External models, paid APIs, production data, long-term memory writes, and private data use must be confirmed first
- Current model/SDK/pricing details must be checked against official sources
- By default only local, reversible, verifiable low-risk work; confirm first for anything involving production, credentials, payment, remote writes, deletion, publishing, or permission changes.

## Why You Can Trust It
- Separates deterministic steps from model-judgment steps
- Evaluates across retrieval, context, generation, citation, and refusal dimensions
- Does not treat untrusted web content as system instructions

## Typical Usage
```text
Use coff0xc-ai-agent-rag to design an enterprise knowledge-base assistant with citations, caching, and failure degradation.
Use coff0xc-ai-agent-rag to evaluate this tool-calling agent's memory, retrieval quality, and cost.
Use coff0xc-ai-agent-rag to turn this prompt-only idea into an evaluated RAG workflow.
```

## Default Output
- Close with only done, verified, remaining, and next steps; give a path or location for any file/code/rule artifacts.
- Checks not actually run are marked unverified; security/architecture conclusions carry an evidence level.

## Expand on Demand
- Everyday tasks use only the quick rules, capability boundaries, and typical usage above; do not read the full gates by default.
- Read `references/full-workflow.md` only for deep architecture, complex multi-stage work, quality evaluation, release, formal delivery, or when the current task lacks evidence.
- After reading a reference, keep context to the minimum necessary; do not output long process write-ups or extra self-justifying material just because a reference exists.
