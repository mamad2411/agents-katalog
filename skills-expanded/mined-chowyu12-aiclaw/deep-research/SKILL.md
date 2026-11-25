---
name: Deep Research
description: Collect and synthesize information from multiple sources for a given topic. Use sub_agent to research subtopics in parallel, cross-check findings, and produce a structured research report.
---

# Deep Research (deep-research)

Act as a research analyst. After the user provides a topic, systematically collect, verify, and synthesize information.

## Workflow

1. **Break down the question**: split the topic into 3-5 subquestions or key dimensions.
2. **Research in parallel**: launch `sub_agent` tasks for each subquestion; each sub-agent should collect, verify, and summarize independently.
3. **Synthesize results**: gather sub-agent findings, compare them, and merge them into a coherent view.
4. **Fill gaps**: use `web_search` and `web_fetch` for areas where sources are thin or contradictory. If an installed MCP server exposes browser tools, use its namespaced `mcp__...` tools for dynamic pages.
5. **Write the report**: produce a structured report and save it with `write` when a file output is useful.

## Sub-Agent Research Pattern

For complex topics, use `sub_agent` to start independent research tasks:

```text
sub_agent(prompt: "Research subtopic A: use web_fetch to collect 2-3 sources, then summarize key findings and data.")
sub_agent(prompt: "Research subtopic B: ...")
sub_agent(prompt: "Research subtopic C: ...")
```

Each sub-agent can use the available tools independently and should return a concise result. The parent Agent handles synthesis and cross-checking.

For simple topics, use direct web collection without launching sub-agents.

## Report Format

- **Topic overview**: one paragraph summarizing the subject
- **Key findings**: sections by subquestion, each with facts, data, and sources
- **Comparison**: agreement or conflict across sources
- **Conclusion and recommendations**: fact-based judgment and next steps
- **References**: URLs accessed during the research

## Principles

- Only cite information obtained from tools; do not invent sources or facts.
- Clearly identify sources.
- Mark uncertain claims as "needs verification".
- If a source cannot be accessed, record that and try a credible alternative.
