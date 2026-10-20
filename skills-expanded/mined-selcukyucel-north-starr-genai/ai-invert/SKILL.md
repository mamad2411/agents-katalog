---
name: ai-invert
description: Run AI-specific inversion analysis on a requirement before implementation. Dispatches the `ai-invert-analyst` agent on a separate thread. Use before complex or high-stakes AI tasks that touch prompts, models, RAG, or AI-powered outputs.
---

# /ai-invert — Dispatch the AI Inversion Analyst

## Purpose

Entry point for AI-specific inversion analysis. Delegates the heavy lifting to the `ai-invert-analyst` agent on a separate thread so the main conversation stays lean.

Use this **before** implementation for any AI work that touches prompts, models, RAG pipelines, or AI-powered outputs. For non-AI code changes within an AI project, use `/genai-invert` instead.

## Pre-flight: Auto-sync Check

Read the root `CLAUDE.md` (if it exists). If `## How to Approach Tasks` appears AFTER `## Tech Stack` or `## Architecture`, the file has an outdated section order. Silently run `/genai-sync` to fix it before continuing.

## Input

The user provides a requirement, feature description, or task involving AI components.

## Workflow

### Step 1 — Confirm Scope with the User

Briefly restate the requirement and confirm the AI components touched (prompts, RAG, guardrails, outputs). If the requirement is a single sentence with no detail, ask the user whether they want `/discover` to elicit structure first — an inversion on a vague requirement produces vague risks.

### Step 2 — Dispatch the Agent

Spawn `ai-invert-analyst` via the Agent tool (`subagent_type: "north-starr-genai:ai-invert-analyst"`) on a separate thread. Pass the full requirement text plus any known constraints (cost envelope, latency target, deadline).

The agent will:
1. Read relevant code, prior decisions (`.plans/DECISIONS.md`), and learnings (`.plans/LEARNINGS.md`)
2. Work through 10 risk dimensions (user impact, prompt fragility, hallucination, data pipeline, cost, reasoning, model dependency, guardrails, architecture, virtue trade-offs)
3. Generate adversarial input examples tailored to this pipeline
4. Classify every risk NEW / PRE-EXISTING / AMPLIFIED
5. Cross-consult `cost-estimator`, `rag-advisor`, and `guardrails-designer` where the risk profile requires it
6. Write `.plans/INVERT-<name>.md` and return a summary

### Step 3 — Read the Result and Present

When the agent returns, read `.plans/INVERT-<name>.md` and present a concise summary to the user:

```
AI inversion analysis complete: .plans/INVERT-<name>.md

Overall risk: <LOW/MEDIUM/HIGH>
Top 3 risks:
  - <risk 1>
  - <risk 2>
  - <risk 3>

Cross-consult log: <count> peer agents cited

Next step:
  - MEDIUM or HIGH → "Risk is <level>. I'll spawn `genai-layoutplan` to build an implementation plan. It runs on a separate thread so your main context stays clean. Proceed?"
  - LOW → "Risk is LOW. `genai-layoutplan` is optional. Want structured planning, or proceed directly to implementation?"
```

### Step 4 — Dispatch `genai-layoutplan` (on user approval)

If the user approves and risk is MEDIUM or HIGH, spawn `genai-layoutplan` with the INVERT file path. It runs on a separate thread.

## Notes

- This skill is a thin dispatcher — the real analysis lives in the `ai-invert-analyst` agent
- The agent produces `.plans/INVERT-<name>.md` which feeds `genai-layoutplan`
- For non-AI code changes within an AI project, use `/genai-invert` (standard inversion)
- The agent runs on a separate thread to keep main conversation context clean
- If `.plans/INVERT-<name>.md` already exists for this requirement, tell the user and ask whether to refine (add a revision section) or regenerate
