---
name: research-ideation
description: "Use when the researcher has no specific research question yet — when they need to discover what to study, not how to study it. Triggers on keywords like 'what should I research', 'research ideas', 'what can I do with this dataset', or when a dataset/paper is provided without a formed question."
---

# Research Ideation

## Overview

Generate concrete research ideas from loose inputs — keywords, datasets, papers — and present them with actionable metadata. This skill is **divergent**: it expands possibilities. Its downstream partner `research-brainstorming` is **convergent**: it narrows one idea into a rigorous study design.

**Core principle:** You cannot refine a question you haven't asked yet. Ideation comes before design.

## When to Use

**Use this skill when:**
- The user has no formed research question — only keywords, a dataset, or vague interest
- The user says "what should I research?", "what can I do with this data?", "research ideas for [topic]"
- A dataset or paper is provided without a specific question attached
- `whats-next` diagnoses the state as Pre-ideation

**Do NOT use this skill when:**
- The user already has a research question (e.g., "Does X cause Y?") → use `research-brainstorming`
- The user has a hypothesis to test → use `hypothesis-first`
- The user is stuck mid-project → use `whats-next`

**Discriminating rule:** If the user can state their interest as "Does/Is/Can [X] [verb] [Y]?", they have a formed question → skip to `research-brainstorming`. If they cannot, they are in ideation territory.

## Checklist (Step Order Fixed)

You MUST create a task for each of these items and complete them in order:

1. **Collect inputs** — gather keywords/datasets/papers from conversation or by asking
2. **Explore sources** — analyze what's available
3. **Generate ideas** — 3-5 by default; 5-10 if scope is broad
4. **Present ideas** — each with title + description + metadata table
5. **Recommend and propose** — highlight one + suggest `research-brainstorming` handoff

## Step 1: Collect Inputs

The skill accepts three types of input. All optional, but at least one must be present:

1. **Keywords / interest area** — e.g., "attention mechanism", "neuroimaging", "time-series forecasting"
2. **Dataset** — files in the project (csv, npy, etc.) whose structure the agent explores
3. **Papers / literature** — user-provided PDFs, URLs, or web search for recent trends

**Collection rules:**
- Check what the user already provided in conversation. Skip what's already known.
- If nothing is provided, ask once: "Are there datasets or papers I should look at? Or just throw me some keywords."
- Minimum requirement: one keyword. The skill can start from a single keyword alone.
- Do NOT ask multiple questions. One prompt, then start working.

## Step 2: Explore Sources

Adapt exploration to the input types available:

| Input type | What to do |
|------------|------------|
| **Dataset** | Read the file(s). Analyze columns, shape, dtypes, descriptive stats (N, mean, std, NaN rate, label distribution). Note what variables are available and what relationships could be studied. |
| **Paper** | Read abstract + methodology + limitations. Extract the research question, key findings, and identified gaps. Note what the authors suggest for future work. |
| **Keywords** | Web-search for recent trends, open problems, and active debates in the area. Look for survey papers, workshop topics, and recent preprints. |

When multiple input types are present, look for **cross-pollination** — where dataset characteristics meet literature gaps or keyword trends.

## Step 3: Generate Ideas

**Default: 3-5 ideas.** If the agent judges the scope is broad (multiple fields, large dataset with many variables, or diverse literature), expand to **5-10 ideas** without asking.

Each idea should be:
- **Concrete** — specific enough that `research-brainstorming` could start refining it
- **Distinct** — ideas should not be minor variations of each other
- **Grounded** — connected to the actual inputs (data available, literature gap identified, trend observed)

## Step 4: Present Ideas

Each idea follows this template:

### N. [Idea Title]
[2-3 sentences: why this is interesting, what gap it fills]

| Item | Detail |
|------|--------|
| Difficulty | High / Medium / Low |
| Data needed | Already available / Additional collection required / Public dataset available |
| Estimated duration | ~2 weeks / ~1 month / ~3 months (one researcher, full-time, excluding data collection) |
| Core methodology | e.g., "transformer + EEG temporal features" |

## Step 5: Recommend and Propose

After presenting all ideas, recommend one:

> "I find **#N** most promising — [one-sentence reason]. Want to start `research-brainstorming` to shape this into a rigorous study design?"

The user may:
- **Pick the recommended idea** → invoke `research-brainstorming`
- **Pick a different idea** → invoke `research-brainstorming` with that idea
- **Ask for more ideas** → generate additional ideas
- **End the session** → suggest journaling (see Session End below)

All are valid outcomes. The handoff is a suggestion, never a forced transition.

## Session End Behavior

If the user ends the session without picking an idea:

> "Want me to save these ideas before we wrap up? `research-journal` can capture them so you don't lose them."

This is a gentle suggestion. Ideas are ephemeral by default — saved only if the user journals or picks one to develop.

## Anti-Patterns

| What you might do wrong | What to do instead |
|---|---|
| Start designing a study for one of the ideas | Stop. That's `research-brainstorming`'s job. Present ideas, don't refine them. |
| Generate only one idea | Always generate at least 3. The user needs options. |
| Ask 5 questions before generating | Collect inputs in one prompt, then work. |
| Force the user to pick an idea | Present, recommend, wait. The user decides. |
| Generate ideas unrelated to the inputs | Every idea must connect to at least one input (keyword, dataset feature, or literature gap). |
| Skip exploring the dataset | If a dataset is provided, you MUST look at its structure. Don't ideate in the abstract. |

## Integration

- **Called by:** `eureka:using-eureka` (when no formed question exists), `eureka:whats-next` (Pre-ideation diagnosis)
- **Hands off to:** `eureka:research-brainstorming` (when user selects an idea — suggestion only)
- **Does NOT invoke:** `hypothesis-first`, `experiment-design`, or any execution/review skill

## Skill Type

**FLEXIBLE** — The step order (collect → explore → generate → present → recommend) is fixed and must not be skipped. But how each step executes adapts to context:

- Dataset-heavy input → more structural analysis, fewer web searches
- Keyword-only input → heavier web search for trends and gaps
- Broad field → 5-10 ideas; narrow niche → 3-5 ideas

No scientific integrity is at stake at the ideation phase. The downstream rigid skills (`hypothesis-first`, `claims-audit`) enforce that discipline later.
