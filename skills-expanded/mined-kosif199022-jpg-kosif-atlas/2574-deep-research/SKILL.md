---
name: deep-research
description: >
  Prepares a fully filled-in research request prompt, ready to paste into any deep-research
  LLM (Perplexity Deep Research, OpenAI Deep Research, Gemini Deep Research, etc.). Gathers
  parameters interactively, then helps the user design high-quality sub-questions before
  assembling the final prompt. The sub-question design step is where Codex adds the most
  value — it surfaces the right analytical angles before handoff to the research tool.
when_to_use: >
  Use when the user wants to run a deep research query and wants help structuring it well
  before sending it to a research tool. Trigger phrases: "deep research", "research request",
  "help me research X", "prepare a research prompt", "I want to research X", "write a
  research query for".
---

# Deep Research Request Builder

Your job is to help the user build a high-quality, fully filled-in research request prompt ready to paste into a deep-research LLM (Perplexity, OpenAI Deep Research, Gemini, etc.). You add value in two places: gathering the right parameters, and designing the sub-questions that will guide the research.

Work through the three steps below in order. Don't skip ahead.

---

## Step 1 — Gather Parameters

Ask the user for the following in a single message. Ask for all of them at once — don't ask one at a time.

**Required:**
- **Research question** — the primary question the research should answer
- **Domain** — the subject area (used to calibrate the analyst role)
- **Audience** — who will read the report (e.g., "a non-technical executive", "a product team", "a policy researcher")
- **Timeframe** — how recent should sources be (e.g., "last 3 years", "2020–present", "no restriction")

**Optional (ask together, but note they have defaults):**
- **Scope** — anything specifically to include or exclude from the research
- **Sub-questions** — if they already have specific angles they want covered; otherwise you'll derive them in Step 2

Once you have the required fields, proceed.

---

## Step 2 — Design the Sub-Questions

This is the highest-value step. Good sub-questions determine whether a deep-research model produces a shallow topic survey or a genuinely useful report.

**First**, analyze the research question and propose 4–6 sub-questions. For each one:
- State the sub-question clearly
- Explain in one sentence *why* it matters to the primary question
- Note what kind of evidence would answer it (data, case studies, expert consensus, etc.)

**Criteria for good sub-questions:**
- Specific enough to guide targeted search (not "what is X?" but "what evidence exists for X under condition Y?")
- Collectively exhaustive — together they cover the primary question
- Mix of descriptive ("what is the current state of X?"), causal ("why does X happen?"), and analytical ("what are the implications of X for Y?")
- Answerable with available web evidence — avoid questions that require unpublished data
- Avoid overlap — each sub-question should pull from a distinct area

**Then**, ask the user: *"Do you want to add, remove, or reword any of these before I build the prompt?"*

Incorporate their feedback. Only move to Step 3 once they confirm the sub-questions.

---

## Step 3 — Assemble and Output the Prompt

With all parameters and sub-questions confirmed, assemble the complete research request prompt below. Output it inside a single fenced code block — ready to copy and paste directly into the research tool.

Fill in every placeholder. Do not leave any `{PLACEHOLDER}` text in the final output.

```
[SYSTEM]
You are a senior research analyst specializing in {DOMAIN}. Your task is to produce a rigorous, analytically deep research report — not a summary of what exists, but a synthesis that draws connections across sources, surfaces non-obvious insights, and explicitly accounts for uncertainty.

[USER]
## Research Request

**Primary Question:** {RESEARCH_QUESTION}

**Audience:** {AUDIENCE}
Calibrate technical depth, vocabulary, and assumed background knowledge accordingly. Prioritize what is decision-relevant or actionable for this audience.

**Timeframe:** Focus on {TIMEFRAME}. Where older foundational work is still the best available evidence, include it and note its age.

**Scope:**
- In scope: {WHAT_TO_COVER}
- Out of scope: {WHAT_TO_EXCLUDE}

---

## Sub-Questions

Answer each of the following before synthesizing. They should collectively cover the primary question.

{SUB_QUESTIONS — numbered list}

---

## Source Standards

Apply this hierarchy:
1. Peer-reviewed research, primary data, official institutional sources
2. Reputable investigative journalism, established industry reports — cite and flag as secondary
3. Expert commentary — use only to contextualize, not as primary evidence

If you cannot find reliable information on a sub-question, state this explicitly: "Reliable evidence on this point was not identified." Do not speculate or fill gaps.

---

## Report Structure

Produce the report in this exact order:

**1. Executive Summary** (150–200 words)
The single most important finding, the key tension or unresolved question, and the most actionable implication. Written for a reader with 90 seconds.

**2. Background & Context**
What the reader must know to evaluate the findings. Define contested terms. Frame the landscape. Keep this tight — no more than needed to make Section 3 intelligible.

**3. Key Findings**
Organized by sub-question. For each:
- State the finding directly and specifically
- Cite supporting evidence inline
- State contradicting evidence or alternative interpretations if they exist

**4. Synthesis**
What patterns emerge only when findings are viewed together? What is surprising given conventional understanding? What are the second-order implications? Do not restate findings — add new analytical value.

**5. Gaps & Uncertainties**
What remains unknown, contested, or under-researched? Where should the reader apply extra skepticism?

**6. Implications for {AUDIENCE}**
What does this mean specifically for this reader? Prioritize decision-relevant insights over general observations.

**7. Sources**
Cited inline throughout using [Author, Year] format. Full references listed here, including publication date and URL where available.

---

## Quality Constraints

- **Analyze, don't summarize.** Draw conclusions, identify patterns, surface tensions between sources.
- **Make claims.** Hedge only where evidence is genuinely contested or limited — and when you hedge, specify why.
- **No filler.** Every sentence carries information. Remove transitional summaries that restate what was just said.
- **Depth over breadth.** Go deep on the most consequential aspects rather than shallow coverage of everything.
- **No hallucination.** If a sub-question has no reliable evidence, say so. Do not present contested claims as settled consensus.
```

After outputting the prompt, add one line: *"Copy the block above and paste it directly into your deep-research tool."*
