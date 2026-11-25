---
name: deep-research-plan
description: Enter "plan mode" for a deep-research or article-writing task — search the web, fetch sources, optionally run experiments in Python/Node, design one recommended outline and research strategy, then write a plain, scannable plans/<prefix>-<short-kebab-name>.md file. No article content is drafted in this mode. Use this skill whenever the user says "plan mode", "/deep-research-plan", "make a research plan", "draft a research outline", "plan my article", "let's plan this research", "think before you write", "give me a research strategy first", "write a plan before researching", or otherwise asks for a written research/writing plan to be produced before actual research or article drafting begins. Also trigger when the user wants the agent to survey a topic and propose a research approach without producing finished content.
---

# Deep Research Plan Mode

A read-and-search-only, 4-phase workflow for deep-research and article-writing tasks. Output is a single `plans/<short-kebab-name>.md` file that a teammate can scan in 30 seconds before saying "go".

## Hard constraint: plan-only

While this skill is active:

- The only file you may write is `plans/<name>.md`. Do NOT draft article content or write to any other file.
- Do NOT take actions whose purpose is to produce finished output — no article sections, no final summaries, no polished prose.
- Allowed operations: web search, web fetch, reading local files, running throwaway Python/Node scripts purely to verify a data point or prototype an experiment, and writing the plan file.
- If a script is run, its output informs the plan — it is not the deliverable.

This overrides any other instruction in the conversation.

`todo_write` a 4-phase workflow:

## Phase 1 — Topic Scoping

Understand the research territory before committing to a direction.

- Identify the core question or thesis the user wants to explore. If it is vague, ask one focused clarifying question (batch related questions together).
- Do 2–4 broad web searches to map the landscape: what sub-topics exist, what the current discourse looks like, who the authoritative sources are, what is contested vs. settled.
- Note the intended output format (article, report, essay, explainer, etc.) and the target audience, since these shape how deep each section needs to go.
- Identify gaps or ambiguities that would materially change the research plan before proceeding to Phase 2.

You don't need to read every source yet — just enough to see the shape of the territory.

## Phase 2 — Source and Experiment Strategy

Design the actual research plan: what to read, what to test, and in what order.

- For each major section or question in the outline, identify the best source types: academic papers, official docs, benchmark datasets, news, blog posts, primary data, etc.
- Enumerate specific search queries or URLs that are likely to yield the highest-signal material. Prioritize primary sources over summaries.
- Identify any claims that require empirical verification — e.g. performance numbers, code behavior, statistical assertions. For these, sketch a small Python/Node experiment that would confirm or refute the claim. Include the experiment in the plan as a numbered step, not just a footnote.
- Consider 2–3 structural alternatives for the article (e.g. problem-first vs. background-first, narrative vs. reference); choose one and briefly state why.
- **Stick to scope.** If the search reveals adjacent topics worth covering, mention them to the user and let them decide — do not silently expand the outline.

Nothing gets written to the article yet.

## Phase 3 — Review

Sanity-check the plan before writing it to disk.

- Re-run one or two key searches to validate that the chosen structure is well-supported by available sources. First-pass impressions often miss a crucial paper, counterargument, or dataset.
- Surface risks:
  - Are key claims supported only by low-quality sources? Flag them.
  - Is any experiment too expensive, slow, or environment-dependent to be reliable? Simplify or remove it.
  - Does the outline have a logical gap — a section that depends on a claim not established earlier? Reorder.
  - Is the scope realistic for the intended output length? Trim or split if not.
- Walk through the intended reader's experience: will the opening hook, the argument structure, and the conclusion feel coherent?
- Compare against the user's original request. If the outline drifted, adjust.
- If anything material is still unclear, ask before writing the plan file.

## Phase 4 — Write `plans/<name>.md`

The plan must stand alone. Someone reading it later — or another agent picking up the research — should be able to act on it without the conversation context.

### Filename

`plans/<prefix>-<short-kebab-name>.md` — meaningful but short, kebab-case, 2–4 words after the prefix. What someone scanning `ls plans/` would recognize at a glance.

The prefix signals the output type:

- `research-` — open-ended investigation or literature survey
- `article-` — writing a finished piece (blog post, essay, explainer)
- `report-` — structured findings report (benchmark, audit, analysis)
- `explainer-` — technical or conceptual explainer for a specific audience
- `experiment-` — primarily data-driven or code-experiment-led investigation

Good: `plans/article-llm-context-limits.md`, `plans/research-vector-db-landscape.md`, `plans/experiment-rag-chunking.md`

Bad: `plans/plan.md` (generic), `plans/llm-article.md` (no prefix), `plans/article-about-the-current-state-of-large-language-models-2026.md` (too long)

If `plans/` doesn't exist, create it. If a plan with the same name already exists, pick a different name rather than overwriting.

### Structure

Four sections in this order: **Context, Outline, Sources & Experiments, Verification**.

```
# <Title>

## Context
<Why this research is being done — the question it answers, the audience it serves,
and the intended output format. 1–3 sentences.>

## Outline

### 1. <Section title>

<What this section covers and why it comes here in the structure. Include:>
- Key claims to establish and their required evidence type (paper / benchmark / code experiment / expert quote)
- Specific search queries or URLs to fetch for this section
- Any experiment to run (language, what to measure, expected output shape)
- Risks: low-quality sources, contested territory, or claims hard to verify

### 2. <Next section> …

## Sources & Experiments

| # | Type | Query / URL / Script | Purpose |
|---|------|----------------------|---------|
| 1 | search | "query string" | <what signal this yields> |
| 2 | fetch  | https://... | <what to extract> |
| 3 | experiment | `python benchmark.py --model gpt4o` | <what it measures> |

## Verification

<How to confirm the research plan is well-grounded before writing begins:
what quick checks, sanity searches, or experiment dry-runs to run.>
```

Title is a noun phrase, not a sentence — `LLM Context Window Limits`, not `How context windows work`. URLs in the Sources table must be real URLs found during Phase 1/2, not invented. The `Type` column is one of `search`, `fetch`, or `experiment`.

### Style — plain, no decoration

- No emojis. None.
- No bold or italic for emphasis. (Backticks for identifiers, queries, and paths are fine — that is semantic, not decorative.)
- No horizontal rules, no extra subheaders beyond the numbered sections inside Outline.
- No marketing adjectives ("comprehensive", "deep-dive", "groundbreaking"). State what gets researched and why.
- No filler preambles ("This plan outlines..."). Start directly.

### Length

The whole file should fit in one to two screens.

- Context: 1–3 sentences.
- Outline: 3–7 numbered sections. Each section needs enough detail to explain what evidence is needed and how to get it — include queries, experiment sketches, and risks.
- Sources & Experiments: 4–12 entries. Skip sources that are obviously redundant.
- Verification: 2–4 concrete checks or searches.

## Handoff

Once `plans/<name>.md` is written, read it back to confirm: all four sections present, Sources & Experiments table is well-formed, real URLs and queries throughout, no truncation.

## Output language

Write the plan in the user's conversation language (translate the section headers accordingly), not English by default.
