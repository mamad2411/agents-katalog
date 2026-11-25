---
name: ai-systems-review
description: >-
  Hostile self-review of recently written AI workflow code that then applies
  fixes (agents, tools, chat context, summarization, tokens, attachments). Use
  after generating AI systems code, or when asked to self-review and harden it.
  Not for PR peer review (code-review) or no-edit devil's-advocate attacks
  (adversarial-challenge). Prefer: adversarial-challenge → decide → this skill.
---

# ai-systems-review

Hostile self-review of **your own** recent AI-powered workflow code, then harden it.
Examples in the process are chat/context-heavy — map each section onto whatever
subsystem actually changed (agents, tools, RAG, streaming, attachments, etc.).

## Not this skill

| This skill | `adversarial-challenge` | `code-review` |
| --- | --- | --- |
| Hostile pass → **edit** top ≤5 | Attack design; **no edits** | Peer PR/diff → **verdict** |

## Operating rules

- Setup: `git status` and `git diff` (staged + unstaged). If the tree is clean, ask which paths to review — do not wander the repo.
- Adapt failure-mode prompts to the changed subsystem; do not force a summarization lens onto unrelated code.
- Model/cost choices on OpenRouter: use the `openrouter` skill for live pricing and capability checks — do not invent slugs or prices.
- After the prioritized list: **edit the working tree** for those ≤5 items. If an item is architectural or large multi-file, propose it and wait. Do not substitute pasteable blocks for real edits.
- Preserve intended behavior; no drive-by refactors outside the list.

## Process

### 0. Setup

- Run `git status` and `git diff` (include staged). Confirm the change set before reviewing.

### 1. High-level review

- Briefly restate what this code is supposed to do.
- Identify the **core design choices** (data models, background processes, token handling, error handling, where logic lives, etc.).
- Call out anything that feels **overly clever, brittle, or tightly coupled**.

### 2. Correctness and robustness

- Look for **bugs, race conditions, and edge cases**:
  - What can go wrong if:
    - The LLM call fails, times out, or returns malformed output?
    - Token estimates are wrong or the conversation grows faster than expected?
    - The server restarts mid–background-task (no queue), or multiple requests hit at once?
    - Tools/agents race, attachments fail validation, or streams abort mid-response?
- For each risk, propose a **specific mitigation** (guard clauses, retries, fallbacks, logging, schema tweaks, etc.).

### 3. Performance and cost

- Evaluate **token usage, model choice, and background work**:
  - Right model(s) for the job (e.g. cheap/mini for summarization)? Verify via `openrouter` when applicable.
  - Unnecessary work (duplicate summarization, re-counting tokens, reloading data, oversized prompts)?
- Suggest **concrete changes** that cut latency/cost **without** sacrificing behavior.

### 4. Architecture and maintainability

- Is logic **modularized** (context/prompt/model services, DB models), or piled into one route file?
- Identify extracts/reuse opportunities.
- Highlight **naming or structure** that will confuse a future engineer (including “future me”).

### 5. API & data flow clarity

- Trace: **request → DB → background work → LLM → response** (adapt stages to the feature).
- Confirm it is easy to reason about and extend (new agents, tools, context strategies).
- Call out spooky/implicit assumptions (messages, attachments, tool results) and propose a clearer pattern.

### 6. Logging, observability, and failure modes

- Logs/metrics for: summarization (or equivalent jobs), token/truncation decisions, background failures, tool/LLM errors.
- Propose **specific log lines** and fields.
- Define **degraded mode**: what if the background job never runs or fails repeatedly?

### 7. Security and data handling

- File handling, blobs, URLs, base64: validate types/sizes; no accidental public URLs.
- Suggest **minimal, practical** hardening only.

### 8. Concrete refactors + apply

- Prioritized list (**max 5**): one-line summary, file(s)/function(s), why it matters.
- **Apply** those improvements in the working tree (see Operating rules).
- End with a short **sanity checklist** for manual app verification.
