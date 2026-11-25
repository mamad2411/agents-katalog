---
name: research
version: 1.0.0
description: Systematically gather, evaluate, and synthesize information from available sources
uses: []
requires:
  tools: []
  env: []
security:
  risk_level: read
  capabilities:
    - source:read
    - search:execute
  requires_approval: false
---

# Research

Systematically gather, evaluate, and synthesize information from available sources to answer questions or build understanding.

## Execution Model

This is an **agent-handled skill** (`handler: type: agent`). When `research_query` is invoked, you (the agent) execute the methodology below using your available tools (file reading, search, web access, etc.) and reasoning. There is no backing code — you follow these instructions directly. The tool schema in tool.yaml defines the external contract; this document guides how you fulfill it. An orchestrator may route this skill to any agent that has `analysis/research` in its skill list.

## When to Use

- Answering factual questions that require multi-source verification
- Building understanding of an unfamiliar domain, system, or codebase
- Gathering evidence to support a decision or recommendation
- Investigating a problem where the root cause is unknown
- Preparing input for analysis, planning, or content generation

## Methodology

### 1. Define Scope

Before gathering anything, clarify what you need to know:
- **Question**: What specific question are you answering?
- **Boundaries**: What is in-scope and out-of-scope?
- **Depth**: Surface overview, working knowledge, or deep expertise?
- **Constraints**: Time limits, source restrictions, confidentiality?

### 2. Discover Sources

Identify all available sources relevant to the scope:
- **Primary sources**: Code, configuration files, logs, databases, APIs
- **Documentation**: READMEs, wikis, specs, design docs, comments
- **External references**: Standards, RFCs, vendor docs, research papers
- **Human knowledge**: Team members, domain experts, stakeholders
- **Historical data**: Git history, issue trackers, decision records

### 3. Extract Information

From each source, extract relevant facts:
- Read carefully — skim for structure, then read relevant sections in depth
- Note exact quotes and locations for citation
- Distinguish facts from opinions and assumptions
- Flag contradictions between sources immediately
- Record what you did NOT find (absence of information is information)

### 4. Cross-Reference

Validate findings across sources:
- Do multiple sources agree on key facts?
- Where sources disagree, identify which is more authoritative and why
- Look for patterns across sources — recurring themes indicate importance
- Identify gaps — what questions remain unanswered?

### 5. Synthesize

Combine findings into a coherent understanding:
- Organize by theme, not by source
- Lead with the most important findings
- Clearly separate confirmed facts from inferences
- State confidence level for each major finding (high / medium / low)
- List remaining unknowns and how they could be resolved

### 6. Cite Sources

Every claim must be traceable:
- Reference specific files, line numbers, URLs, or documents
- Include timestamps for time-sensitive information
- Note the reliability of each source

## Output Format

```
## Research: [Topic]

### Scope
- Question: [What we're investigating]
- Depth: [Overview | Working Knowledge | Deep Dive]

### Key Findings
1. [Finding] — Confidence: [High/Medium/Low]
   Source: [citation]

2. [Finding] — Confidence: [High/Medium/Low]
   Source: [citation]

### Contradictions / Conflicts
- [Source A] says X, [Source B] says Y
  Resolution: [which is correct and why, or "unresolved"]

### Gaps
- [What remains unknown]
- [How it could be resolved]

### Sources Consulted
- [Source 1]: [what it provided]
- [Source 2]: [what it provided]
```

## Quality Criteria

- Every finding has a cited source
- Confidence levels are assigned honestly (not everything is "high")
- Contradictions are surfaced, not hidden
- Gaps are explicitly identified
- Scope boundaries were respected
- Synthesis is organized by theme, not by source order

## Common Mistakes

- **Starting without a clear question**: Always define what you're looking for before searching
- **Trusting a single source**: Cross-reference whenever possible
- **Treating absence as evidence**: "I didn't find X" is different from "X doesn't exist"
- **Burying contradictions**: Surface them — they often reveal the most important insights
- **Over-researching**: Stop when you have enough to answer the question at the required depth
- **Failing to cite**: Every factual claim needs a traceable source

## Completion

Research is complete when:
- The original question can be answered at the requested depth
- Key findings are cross-referenced across multiple sources
- Contradictions are identified and (where possible) resolved
- Remaining gaps are documented with suggested next steps
- All claims are cited with specific sources
