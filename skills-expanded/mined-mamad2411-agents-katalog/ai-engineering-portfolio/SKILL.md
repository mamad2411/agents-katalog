---
name: ai-engineering-portfolio
description: Five structured AI engineering project briefs for a 2026 portfolio — RAG Knowledge Assistant, AI Agent Workflow, AI Evaluation Dashboard, Multimodal Document AI, and Secure AI System — each with a build checklist, a "best for" skill tag, and a copy-paste kickoff prompt. Use when the user wants project ideas that demonstrate real AI engineering skill beyond a basic chatbot, is building a portfolio for AI/ML engineering job applications, or asks what to build next to prove they can do retrieval, tool-use, evaluation, multimodal input, and security — not just call an LLM API. Source: @ksk_data "5 AI Engineering Projects to Build in 2026."
---

# 5 AI Engineering Projects to Build in 2026

Five project briefs, meant to be built roughly in this order — each adds one
capability a plain chatbot doesn't have. Pick one, use its kickoff prompt to
scope it with Claude, then build it before moving to the next.

## 1. RAG Knowledge Assistant

Build an AI system that answers from trusted documents instead of guessing.

**Build with:** document ingestion, embeddings + vector search, retrieve +
rerank, source citations, answer evaluation.

**Best for:** RAG, retrieval, grounding, and LLM application skills.

**Kickoff prompt:**
```
I want to build a RAG Knowledge Assistant: an AI system that answers questions
from a specific set of documents instead of guessing from general knowledge.

My documents are: [describe — PDFs, internal wiki, docs folder, etc.]
My stack preference: [language/framework, or "recommend one"]

Design the two pipelines:
1. Indexing — how to chunk these documents, which embedding model, which
   vector store, and why.
2. Query — retrieval + reranking approach, how many chunks to pass to the
   LLM, and how to force every answer to cite its source chunk.

Then give me a build order (what to build and test first) and a way to
evaluate whether an answer is actually grounded in the retrieved documents,
not the model's own training knowledge.
```

See this repo's `rag-pipeline-architecture` skill for the reference
architecture and failure modes to check first before starting this build.

## 2. AI Agent Workflow

Build an agent that can reason, use tools, and complete a real workflow.

**Add:** tool calling, external APIs, memory/state, human approval,
execution logs.

**Best for:** agentic AI, APIs, orchestration, and automation.

**Kickoff prompt:**
```
I want to build an AI agent that completes this real workflow end to end:
[describe the workflow — e.g. "triage a support ticket and draft a reply,"
"research a lead and log it to a CRM"]

Design:
1. Which tools/external APIs it needs to call, and what each tool's input/
   output contract should look like.
2. How it should hold memory or state across steps in the workflow.
3. Where a human approval step is required before an action executes (which
   actions are reversible vs. irreversible).
4. What gets logged for every execution, so I can debug a bad run after the
   fact.

Then scope a minimal first version I can build and test this week.
```

See `web-task-scoping` for the Target/Limit/Run/Review governance pattern to
apply once tool calls can touch real external systems, not just talk about
them.

## 3. AI Evaluation Dashboard

A working demo is not enough — learn how to measure whether it actually
works.

**Track:** task success, answer quality, tool-call traces, latency + cost,
regression tests.

**Best for:** evaluation, observability, and production AI.

**Kickoff prompt:**
```
I have an AI system ([describe it — a chatbot, a RAG assistant, an agent])
and I want to build an evaluation dashboard for it, not just eyeball whether
outputs look right.

Design an eval set (a fixed list of test inputs with expected outcomes or
grading criteria) and a scoring approach for:
1. Task success rate
2. Answer/output quality (define what "good" means for this specific system)
3. Tool-call traces (did it call the right tool with the right arguments)
4. Latency and cost per run
5. Regression tests (how I catch a change that quietly makes things worse)

Then give me a minimal dashboard structure (even a spreadsheet or simple
script is fine to start) I can run after every change to the system.
```

## 4. Multimodal Document AI

Build an AI app that understands text, images, and real documents together.

**Try:** PDF/image upload, vision understanding, data extraction, structured
output, validation checks.

**Best for:** multimodal AI, documents, vision, and automation.

**Kickoff prompt:**
```
I want to build a multimodal document AI: upload a PDF or image (e.g.
[invoice / receipt / scanned form / ID document]) and get back structured
data I can trust.

Design:
1. How to handle the upload and route it to a vision-capable model.
2. What structured output schema to extract into (give me a concrete JSON
   shape for this document type).
3. Validation checks to run on the extracted data before I trust it (e.g.
   required fields present, totals that should add up, dates in range).
4. What to do when extraction confidence is low — flag for human review
   rather than silently guessing.

Then scope a minimal version I can test against 5-10 real sample documents.
```

This repo already has `invoice-receipt-processor` covering one concrete
version of this brief — check there first if the document type is an
invoice or receipt rather than building the extraction pipeline from
scratch.

## 5. Secure AI System

Show that you can build AI that is useful without ignoring safety and
control.

**Include:** prompt-injection tests, tool permissions, access controls,
guardrails, audit logs.

**Best for:** AI security, governance, and production readiness.

**Kickoff prompt:**
```
I have an AI system ([describe it]) that [reads external content / calls
tools / has access to sensitive data — describe what makes it risky] and I
want to harden it before calling it production-ready.

Walk through:
1. Prompt-injection test cases specific to this system — what untrusted
   input could try to redirect it, and how to test for that.
2. Tool permissions — which tools/actions should require explicit scoping
   or approval, and which are safe to run freely.
3. Access controls — who/what can trigger this system and with what data.
4. Guardrails — what it should refuse to do even if instructed to.
5. Audit logs — what gets recorded so a bad outcome can be traced back to
   its cause.

Give me a checklist I can run this system against before calling it
production-ready.
```

Claude Code's built-in `security-review` and `add-agent-guardrails` skills
(not files in this repo — invoke them directly by name) cover parts of this
brief already; run them rather than building the guardrail/audit-log
scaffolding from scratch.

## Related skills in this repo

- `rag-pipeline-architecture` — reference architecture for project 1.
- `web-task-scoping` — governance procedure for project 2 once tools touch real systems.
- `security-review`, `add-agent-guardrails` — existing tooling for project 5.
- `invoice-receipt-processor` — a concrete instance of project 4 for invoices/receipts specifically.
- `saas-mvp-24h` — if the goal is a shippable product rather than a portfolio demo, that skill's 24-hour build phases apply once one of these five is scoped.

## Notes

Source: @ksk_data TikTok "AI Series" carousel, "5 AI Engineering Projects to
Build in 2026" (7 slides — intro, 5 numbered project briefs, outro). The
kickoff prompts above are written from the carousel's own build checklists
(they weren't given as literal copy-paste prompts in the source) — review
and adjust the bracketed placeholders before using.
