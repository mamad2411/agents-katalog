---
name: deep-dive
version: "2.0.0"
description: "Deep dive on any topic. Decomposes into subtopics, researches each in parallel with thorough source gathering, then synthesizes into a comprehensive report (4,000-10,000+ words, 40-100+ sources). Scales depth dynamically based on topic complexity. Use when asked for a deep dive, deep research, comprehensive analysis, or thorough investigation of a topic."
argument-hint: "deep-dive WebTransport vs WebSockets for real-time apps"
allowed-tools: Bash, Read, Write, WebSearch, WebFetch, Agent, AskUserQuestion
user-invocable: true
---

# Deep Dive

Produce comprehensive research reports by decomposing topics into subtopics, researching each in parallel with exhaustive source gathering, and synthesizing into a single deeply-analyzed report.

## Trigger

`/deep-dive <topic>` or when user asks for a deep dive, deep research, or comprehensive analysis of a topic.

---

## Phase 1: Scope and Decompose (do this yourself, no agent)

### 1a: Assess Topic and Set Research Tier

Before decomposing, assess the topic to determine how much research it warrants:

| | Focused | Standard | Comprehensive |
|---|---|---|---|
| **When** | Narrow comparison, specific technical question, well-defined scope | Most topics -- technology analysis, trend report, landscape overview | Broad survey, emerging field, multi-stakeholder analysis |
| **Subtopics** | 5-7 | 7-9 | 9-12 |
| **Word target** | 4,000-6,000 | 6,000-8,000 | 8,000-10,000+ |
| **Source target** | 40-60 | 60-80 | 80-100+ |
| **Example** | "WebTransport vs WebSockets" | "State of real-time web protocols in 2026" | "Complete guide to building real-time infrastructure" |

Choose the tier based on:
- **Breadth**: How many distinct dimensions does the topic have?
- **Maturity**: Established topics have more sources; emerging ones may max out at fewer
- **Comparison surface**: Binary comparisons need fewer subtopics than landscape surveys
- **User signal**: If user says "quick" or "focused", go Focused. If "comprehensive" or "exhaustive", go Comprehensive. Default to Standard.

### 1b: Interpret the Research Question

Determine:
- **Scope**: Is this a comparison, a landscape survey, a how-to, a trend analysis, or an investigation?
- **Audience**: Technical practitioners, executives, researchers, or general?
- **Depth signals**: What would a domain expert want to know that a surface-level article would miss?

### 1c: Generate Subtopics

Generate subtopics according to the selected tier. Each subtopic should be:
- Distinct (minimal overlap)
- Specific enough to yield targeted search results
- Substantial enough to produce 500-1500 words of findings (scale with tier)

Structure subtopics to cover these angles where relevant (not all will apply to every topic -- use judgment):
- **History/Origins** -- how did this emerge, key milestones, timeline
- **Current State** -- what exists today, major players, market landscape
- **Technical Deep-Dive** -- architecture, implementation details, how it actually works
- **Comparisons/Alternatives** -- head-to-head analysis, trade-offs, benchmarks
- **Real-World Usage** -- case studies, production deployments, who uses this and why
- **Performance/Data** -- benchmarks, metrics, quantitative evidence
- **Limitations/Criticism** -- what doesn't work, known issues, contrarian takes
- **Economics/Business** -- pricing, market size, business models, ROI
- **Ecosystem/Tooling** -- related tools, integrations, community
- **Future Direction** -- roadmaps, trends, predictions, open research questions

Output format:
```
Researching: {topic}
Tier: {Focused | Standard | Comprehensive}
Scope: {comparison | landscape | deep-technical | trend-analysis | investigation}
Targets: ~{N} words, {N}-{N} sources, {N} subtopics

Subtopics:
1. {subtopic_1} -- {why this angle matters}
2. {subtopic_2} -- {why this angle matters}
...
```

Show this to the user before proceeding. If the user wants adjustments (including tier), incorporate them.

---

## Phase 2: Parallel Research (launch ALL agents at once)

Launch agents simultaneously (one per subtopic) using the Agent tool with `run_in_background: true`.

Each agent must be a **thorough researcher**, not a skimmer. Use this prompt template:

```
You are a research specialist investigating ONE subtopic for a larger comprehensive report. Your job is to be EXHAUSTIVE -- find every important detail, data point, and perspective.

Main topic: {topic}
Your subtopic: {subtopic_N}
Why this matters: {subtopic_rationale}

## Research Process

### Step 1: Broad Search (5-7 queries)
Run 5-7 WebSearch queries with varied phrasings, angles, and specificity levels:
- 2 broad queries to find major sources
- 2 specific/technical queries for depth
- 1-2 queries targeting data, benchmarks, or statistics
- 1 query targeting criticism, limitations, or contrarian views

### Step 2: Deep Read (5-8 sources)
Use WebFetch on the 5-8 most substantive results. Prioritize:
- Primary sources (official docs, research papers, company blogs) over aggregators
- Sources with original data, benchmarks, or case studies
- Recent sources (last 12-18 months) for fast-moving topics

### Step 3: Follow-up Search (2-3 queries)
Based on what you learned in Steps 1-2, run 2-3 targeted follow-up searches to fill gaps:
- Names, projects, or tools mentioned in sources but not yet explored
- Statistics or claims that need verification from a second source
- Specific technical details that were referenced but not explained

### Step 4: Compile Findings

Return your findings as structured text. Be DETAILED -- aim for 800-1500 words of substance.

## {subtopic_N}

### Key Findings
- [finding with specific details] ([Source Title](url))
- [finding with data points] ([Source Title](url))
...

### Detailed Analysis
[4-8 paragraphs of thorough findings. Include:
- Specific numbers, dates, versions, metrics
- Named examples (companies, projects, people)
- Direct quotes where impactful
- Technical details where relevant
- Comparisons and context
Every claim must have an inline citation as [text](url).]

### Data Points & Evidence
[Bullet list of specific quantitative findings:
- Market size, growth rates, adoption numbers
- Performance benchmarks, speed comparisons
- Survey results, usage statistics
- Pricing, cost comparisons
Include source for each.]

### Contrarian Views & Limitations
[What are the criticisms, downsides, or alternative perspectives on this subtopic?]

### Sources (with annotations)
- [Title](url) -- what this source uniquely contributed
- [Title](url) -- what this source uniquely contributed
...

IMPORTANT: Target 8-15 unique, high-quality sources for your subtopic. Do NOT pad with low-value results.
```

**CRITICAL: Launch ALL agents in a single message so they run truly in parallel.**

---

## Phase 3: Collect and Audit

Wait for all agents to complete. Then audit the raw material:

1. **Source count check** -- compare total unique URLs against your tier target. If you're more than 20% below target, identify the thinnest subtopics and run 1-2 supplementary agents to fill gaps.
2. **Quality check** -- scan for agents that returned shallow results (under 300 words, fewer than 4 sources). Re-run those with more specific queries.
3. **Contradiction check** -- note where agents found conflicting data. These become valuable discussion points in the report.
4. **Deduplication** -- identify sources cited by multiple agents. These are likely the most authoritative -- weight them higher.
5. **Sufficiency check** -- is the raw material enough to hit the word target? If total agent output is less than 1.5x the word target, the synthesis will be thin. Run supplementary agents on the weakest areas.

---

## Phase 4: Synthesize the Report

Write the final report yourself (do NOT delegate synthesis to an agent). You have all the raw research -- now produce a report that rivals professional research output.

### Report Structure

```markdown
# {Topic}: A Comprehensive Analysis

> **Research Date:** {YYYY-MM-DD}
> **Sources Analyzed:** {N} unique sources across {N} subtopics
> **Word Count:** ~{N}
> **Method:** Multi-agent parallel research with {N} specialized research agents

---

## Table of Contents
[Auto-generated with anchor links to all sections]

---

## Executive Summary

[500-800 words. This should stand alone as a complete briefing. Cover:
- What this topic is and why it matters right now
- 5-7 key findings with the most important data points
- The central tensions/trade-offs discovered
- Bottom-line assessment or recommendation
- Who should care about this and what they should do]

---

## Background and Context

[Set the stage. History, origins, why this topic exists. Timeline of key milestones if relevant. Define key terms. 500-1000 words.]

---

## {Thematic Section 1}

[Organize by THEME, not by subtopic. Cross-reference findings from multiple research agents. Each section should be 800-1500 words with:
- Opening paragraph framing why this dimension matters
- Detailed findings with inline citations
- Specific examples, case studies, or data
- Comparison tables where relevant (use markdown tables)
- Sub-sections (###) for distinct aspects within the theme]

## {Thematic Section 2}
...

## {Thematic Section N}
[Typically 5-8 thematic sections for thorough coverage]

---

## Comparative Analysis

[If the topic involves alternatives, competitors, or approaches -- provide structured comparison:
- Markdown comparison table(s) with key dimensions
- Prose analysis of trade-offs
- Situational recommendations ("Use X when..., Use Y when...")]

---

## Data & Evidence Summary

[Consolidate the most important quantitative findings into a reference section:
- Key statistics and metrics in a scannable format
- Benchmark results if available
- Market data, adoption numbers, growth trends
- Use tables or bullet lists for scannability]

---

## Limitations, Criticisms, and Open Questions

[What the research revealed as unresolved, debated, or problematic:
- Known limitations of the technologies/approaches covered
- Active debates in the community
- Gaps in available data
- Questions that couldn't be fully answered]

---

## Future Outlook

[Where is this heading? Based on evidence found:
- Announced roadmaps or upcoming releases
- Trend lines from the data
- Expert predictions (cited)
- Emerging approaches or disruptors]

---

## Conclusions and Recommendations

[Actionable synthesis:
- Key takeaways (numbered list, 5-10 items)
- Specific recommendations based on different use cases/audiences
- What to watch for next]

---

## Sources

[Deduplicated, organized by section. Full list of every URL cited in the report.
Format: numbered list with title, URL, and brief annotation of what it contributed.

### {Section Name} Sources
1. [Title](url) -- contributed: {what}
2. [Title](url) -- contributed: {what}
...

### {Section Name} Sources
...]
```

### Synthesis Quality Standards

Scale with tier, but never compromise on signal density:

**Length and source targets by tier:**
| | Focused | Standard | Comprehensive |
|---|---|---|---|
| Words | 4,000-6,000 | 6,000-8,000 | 8,000-10,000+ |
| Sources | 40-60 | 60-80 | 80-100+ |
| Thematic sections | 3-5 | 5-7 | 6-9 |

If you're more than 25% below your tier's word floor, go back and expand thin sections. If you're below the source floor, run supplementary research.

**Universal standards (all tiers):**
- **Every factual claim** must have an inline citation as `[text](url)` or `([Source](url))`.
- **Cross-referencing**: Findings from one subtopic must inform analysis in other sections. Do not just concatenate agent outputs.
- **Comparison tables**: Include at least 1-2 structured comparison tables where the topic warrants it.
- **Specificity**: Use real names, real numbers, real dates. Vague statements like "many companies use this" are unacceptable -- name them.
- **Balanced perspective**: Include contrarian views, limitations, and criticism. One-sided analysis is shallow analysis.
- **Readable structure**: Use headers, sub-headers, tables, bullet lists, and bold text for scannability. Dense walls of text are a failure mode.
- **No filler**: Every paragraph must contain information or analysis. Remove throat-clearing, transitions-for-transitions-sake, and restating what was just said.
- **Signal density over word count**: A 5,000-word report packed with data and insight is better than a 10,000-word report padded with filler. Hit the target by going deeper, not wider.

---

## Phase 5: Save

Save the report to the path the user specified. If no path specified, save to the current working directory as `{date}-{topic-slug}.md`.

After saving, output a brief summary:
```
Report saved: {path}
Words: ~{N}
Sources: {N} unique URLs
Sections: {N}
Research agents: {N}
```

---

## What NOT to Do

- Do NOT create outline.yaml, fields.yaml, or per-item JSON files
- Do NOT create README, MANIFEST, or INDEX files
- Do NOT ask the user questions mid-research (decompose and go, only pause after Phase 1)
- Do NOT run agents sequentially -- launch all in parallel
- Do NOT just concatenate subtopic findings -- synthesize across themes
- Do NOT produce reports significantly below your tier's word floor -- that means insufficient research or lazy synthesis
- Do NOT use vague language when specific data exists -- find the number
- Do NOT skip WebFetch -- search result snippets alone are too shallow for deep analysis
- Do NOT settle for significantly fewer sources than your tier targets -- run supplementary agents if needed
- Do NOT pad word count with filler -- every paragraph earns its place with information or analysis
