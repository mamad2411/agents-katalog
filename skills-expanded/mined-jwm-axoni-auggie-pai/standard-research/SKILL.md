---
name: standard-research
description: Multi-source structured research with verified URLs and synthesized reports. The default research mode. USE WHEN research, do research, research this, look into, find out about, comprehensive research, multi-source.
---

# Standard Research

**Mode:** Multi-source structured research | **Time:** ~5 minutes
**This is the DEFAULT research mode.** When the user says "research" without qualification, use this.

## When to Use

- User says "do research", "research this", or just "research [topic]"
- Need a comprehensive answer drawing on multiple perspectives
- Want verified URLs and a structured report
- Default for any research request that is not explicitly "quick" or "deep investigation"

## Available Tools

| Tool | Use For |
|------|---------|
| **WebSearch** | Web queries from different angles; run multiple in parallel |
| **WebFetch** | Deep read of specific URLs; content extraction and verification |
| **claude-browser MCP** | Pages behind authentication or requiring JS rendering |

---

## Workflow

### Step 1: Decompose the Topic

Break the user's research question into 3-5 search angles that cover different facets:

**Example:** "Research the current state of AI code assistants"
1. "AI code assistant market landscape 2026 comparison"
2. "AI code assistant developer productivity studies results"
3. "AI code assistant limitations problems developers face"
4. "AI coding tools enterprise adoption trends"

**Angle selection guidelines:**
- One angle for the core factual question
- One angle for recent developments or news
- One angle for critical/contrarian perspectives
- One angle for practical implications or comparisons
- (Optional) One angle for historical context or trajectory

### Step 2: Parallel Search

Launch all WebSearch queries in parallel (multiple tool calls in one message).

```
WebSearch(query: "[angle 1 query]")
WebSearch(query: "[angle 2 query]")
WebSearch(query: "[angle 3 query]")
WebSearch(query: "[angle 4 query]")
```

### Step 3: Source Selection

From all search results, identify the **top 3-5 most valuable sources** based on:
- Authority (reputable publishers, primary sources, expert authors)
- Recency (prefer recent over dated)
- Relevance (directly addresses the research question)
- Diversity (avoid over-relying on one publisher)

### Step 4: Deep Reads

Use WebFetch on the top sources to extract full content.

```
WebFetch(url: "[source 1]", prompt: "Extract key findings about [topic]")
WebFetch(url: "[source 2]", prompt: "Extract data and evidence about [topic]")
WebFetch(url: "[source 3]", prompt: "Extract expert opinions and analysis on [topic]")
```

For pages that require authentication or heavy JavaScript rendering, use the claude-browser MCP server instead of WebFetch.

### Step 5: URL Verification (MANDATORY)

**Every URL included in the final report MUST be verified.** Research can produce hallucinated or dead URLs. Before delivering results:

1. Confirm each URL was actually returned by WebSearch or successfully fetched by WebFetch
2. If citing a URL you have not fetched, verify it with WebFetch first
3. If a URL fails (404, paywall with no content, unrelated content), remove it and find an alternative
4. NEVER include a URL you have not verified -- a broken link is a credibility failure

### Step 6: Synthesize and Deliver

Produce a structured research report:

```markdown
## Research Report: [Topic]

**Date:** [YYYY-MM-DD]
**Queries:** [number] search angles, [number] deep reads
**Confidence:** [HIGH / MEDIUM / LOW with brief justification]

### Executive Summary
[2-3 paragraph synthesis of the most important findings. Lead with the answer, not the process.]

### Detailed Findings

#### [Theme 1]
[Findings organized by theme, not by source. Cite sources inline.]

#### [Theme 2]
[Continue for each major theme discovered.]

#### [Theme 3]
[Include contrarian or minority views if found.]

### Key Data Points
- [Specific statistic or fact with source]
- [Specific statistic or fact with source]

### Open Questions
- [What remains unclear or contested]
- [What would require deeper investigation]

### Sources
1. [Source title](verified-URL) -- [one-line description of what it contributed]
2. [Source title](verified-URL) -- [one-line description]
3. [Continue for all sources used]

### Recommendations
- [Actionable next steps based on findings]
- [Suggest deep-investigation if warranted]
```

---

## Quality Standards

- **Minimum 3 search angles** -- Never research from a single query
- **Minimum 2 deep reads** -- Snippets alone are insufficient for standard research
- **All URLs verified** -- Zero tolerance for broken or hallucinated links
- **Findings organized by theme** -- Not by source; synthesize across sources
- **Confidence level justified** -- Explain why you are or are not confident
- **Contrarian views included** -- If they exist, report them

## Output Persistence

Standard research results are delivered inline. To persist, write to:

```
~/.augment/MEMORY/RESEARCH/{YYYY-MM-DD}_{topic-slug}/
  research-report.md    # The full report
  sources.md            # Detailed source list with notes
```

Create the directory and save automatically if the report exceeds 500 words or the user requests it.

## Escalation

If during research you discover the topic is vast and would benefit from entity tracking, iterative deepening, or cross-session persistence, suggest deep-investigation mode. Explain what additional coverage it would provide.
