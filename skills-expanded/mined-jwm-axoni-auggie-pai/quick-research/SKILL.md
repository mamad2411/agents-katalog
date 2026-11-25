---
name: quick-research
description: Single-pass web research for fast factual lookups in about 2 minutes. USE WHEN quick research, quick lookup, minor research, fast lookup, simple factual question, quick check.
---

# Quick Research

**Mode:** Single-pass web research | **Time:** ~2 minutes

## When to Use

- User says "quick research", "quick lookup", or "minor research"
- Simple factual questions needing web verification
- Time-sensitive requests where speed matters more than depth
- Surface-level understanding of a topic before deciding on deeper research

## Available Tools

| Tool | Use For |
|------|---------|
| **WebSearch** | Fast web queries, returns search result snippets with URLs |
| **WebFetch** | Deep read of a specific URL, extracts and processes page content |

---

## Workflow

### Step 1: Formulate Query

Analyze the user's request and craft ONE focused search query.

**Good queries are:**
- Specific and well-scoped (not overly broad)
- Include key terms that will surface authoritative results
- Framed to get factual answers, not opinion

**Example:** User asks "What's the current state of WebGPU adoption?"
- Query: "WebGPU browser adoption status 2026"

### Step 2: Execute Search

Run a single WebSearch call with the crafted query.

```
WebSearch(query: "[your focused query]")
```

Review the returned snippets. Identify the 1-2 most relevant and authoritative results.

### Step 3: Deep Read (If Needed)

If the search snippets alone do not provide a confident answer, use WebFetch on the most promising result URL to get full content.

```
WebFetch(url: "[best result URL]", prompt: "Extract the key facts about [topic]")
```

Skip this step if the search snippets already contain a clear, confident answer.

### Step 4: Assess Confidence

Rate your confidence in the findings:

- **HIGH** -- Multiple consistent sources, recent data, authoritative publishers
- **MEDIUM** -- Single source or partially dated information
- **LOW** -- Conflicting sources, no authoritative backing, or sparse results

### Step 5: Deliver Results

Present findings in this format:

```markdown
## Quick Research: [Topic]

**Query:** [what was searched]
**Confidence:** [HIGH / MEDIUM / LOW]

### Key Findings
- [Finding 1 with source attribution]
- [Finding 2 with source attribution]
- [Finding 3 if applicable]

### Sources
- [Source title](URL) -- [one-line relevance note]

### Recommendation
[If confidence is LOW or MEDIUM, suggest standard-research for deeper coverage]
```

---

## Constraints

- Do NOT run more than 2 WebSearch queries. This is quick mode.
- Do NOT use WebFetch on more than 2 URLs. Pick the best sources.
- If the topic requires multi-perspective analysis, recommend standard-research instead.
- Total elapsed time target: under 2 minutes.

## Output Persistence

Quick research results are delivered inline to the user. They are NOT automatically persisted to disk. If the user asks to save the results, write them to:

```
~/.augment/MEMORY/RESEARCH/{YYYY-MM-DD}_{topic-slug}/quick-research.md
```

## Escalation

If quick research reveals the topic is more complex than expected, tell the user:

> "This topic has more depth than a quick lookup can cover. I recommend running standard research for a comprehensive view."

Do not automatically escalate -- let the user decide.
