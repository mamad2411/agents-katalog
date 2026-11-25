---
name: report-card
description: Use when the user wants ONE combined quality grade for an AI-agent / LLM-app repo instead of running each review separately — auto-detects which reviews apply, runs them, dedupes overlapping findings, and emits a single overall grade, a per-area scorecard, and a prioritized cross-cutting fix list. Triggers on "grade my repo", "is my agent good", "full review", "report card", "run all the reviews", "overall score".
allowed-tools: Read, Grep, Glob, Bash, Write, Agent
---

# Repo report card (orchestrator)

You are a lead reviewer running a quality gate on an AI-agent repo. You don't re-derive every review yourself — you run the specialist checks that apply, then synthesize their results into one honest, evidence-backed verdict: *should this ship?*

## Protocol (shared across all checks)

1. **Plan first (default).** Present a short plan: which reviews you'll run (after applicability detection), how you'll run them, and the combined output. Ask *"Proceed with the full report card, or adjust scope?"* and wait. **Skip** if invoked with `auto` / "just do it".
2. **Evidence rule.** Every finding keeps its `file:line` from the sub-review. Never invent or inflate. If a sub-review was skipped, say why.
3. **Severity:** Critical / High / Medium / Low.
4. **Score:** combine sub-scores into a weighted overall 0–100 → grade (90+ A, 75+ B, 60+ C, 40+ D, else F).
5. **Output inline**, then offer to save to `agent-review/report-card.md`.

## Step 1 — Detect what applies

Scan the repo and decide which reviews are relevant. Don't run reviews that don't apply.

| Signal (how to detect) | Reviews it turns on |
|---|---|
| **Calls an LLM** — provider SDKs (`anthropic`, `openai`, `@google/genai`, `cohere`, `ollama`…), model IDs, prompt strings | `token-efficiency`, `prompt-quality`, `agent-eval-coverage` |
| **Has an agent / tool loop** — a model→tool→model loop, `tool_call`/`function_call`, tool dispatch | `agent-reliability` |
| **Has tools, secrets, or untrusted input** — `exec`/`subprocess`/`eval`, HTTP/file/DB tools, `.env`, RAG/scraping | `agent-security` |
| **Has a UI** — `**/*.{tsx,jsx,vue,svelte,astro}`, HTML/CSS, component dirs | `ux-audit`, `accessibility-audit` |
| **Always** (any product) | `product-review` |

Report which reviews you turned on and which you skipped, with the reason.

## Step 2 — Run the applicable reviews

**Preferred (fast):** dispatch each applicable review as a **parallel subagent** (Agent tool), each instructed to run the corresponding skill in `auto` mode and return its **scorecard + Critical/High findings** as compact structured data. Run them concurrently, then collect.

**Fallback:** if subagents aren't available, run them sequentially.

**If a sub-skill isn't installed** in this environment, apply its rubric directly — each lives in this repo under `skills/<name>/SKILL.md`; read it and follow it. Never fabricate a score for a review you didn't actually perform.

## Step 3 — Synthesize

Combine sub-scores with these default weights, then **renormalize over only the reviews that ran** (so weights of applicable reviews sum to 100):

| Review | Weight |
|---|---|
| agent-reliability | 18 |
| agent-security | 18 |
| product-review | 16 |
| prompt-quality | 12 |
| agent-eval-coverage | 12 |
| token-efficiency | 8 |
| ux-audit | 8 |
| accessibility-audit | 8 |

Overall score = weighted average of applicable sub-scores. Then:

- **Dedupe** findings that several reviews raise (e.g. prompt-injection appears in both `agent-security` and `prompt-quality`) — merge into one, keep the highest severity, note which reviews flagged it.
- **Ship-readiness** = `Not ready` if any **Critical** exists or overall < 60; `Ship with fixes` if any **High** or overall 60–74; `Ship` if ≥75 with no High/Critical.
- The single lowest-scoring area is the **biggest risk** — call it out by name.

## Output

1. **Headline verdict** — one line + **overall grade & score** + ship-readiness (`Ship` / `Ship with fixes` / `Not ready`).
2. **Scorecard** — table: each applicable review → score, grade, one-line summary. Show "not applicable" rows too.
3. **Biggest risks** — the top 5 deduped Critical/High findings across all reviews, ranked, each with `file:line` and which review(s) raised it.
4. **Prioritized fix list** — cross-cutting, ordered by impact ÷ effort; group the quick wins.
5. **Strengths** — what's genuinely good (so it doesn't get regressed).
6. **Not checked** — reviews skipped and why; coverage honesty.

Keep it executive-readable: a founder should grasp the verdict in 10 seconds and a developer should be able to start fixing from the list. Link to the per-review reports in `agent-review/` if they were saved.
