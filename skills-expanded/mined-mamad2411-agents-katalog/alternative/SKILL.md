---
name: alternative
description: Find and recommend better alternatives for whatever the user specifies
argument-hint: "<subject>"
allowed-tools:
  - read
  - write
  - edit
  - grep
  - exec
  - ask_user_question
  - todo_write
  - skill
  - web_search
  - webfetch
  - mcp_call_tool
triggers:
  - user
  - model
related:
  - deep-research
  - learn
  - compare-competitors
  - apply
  - follow-best-practice
  - deep-review-codebase
  - suggest-next-action
  - resolve-errors

---

## Goal

Find and recommend better alternatives for whatever the user specifies.

## Scope

Use when the user asks about libraries, tools, frameworks, patterns, or other solutions.

See also: /learn-from-web, /apply choose, /follow-best-practice, /deep-review-codebase, /suggest-next-action, /resolve-errors

## Execute

### 1. Identify Subject

> Goal: Identify what needs an alternative

1. Identify what the user is asking about (library, tool, framework, pattern)
2. Extract the key terms and requirements
3. Define the context and use case

### 2. Deep Research

> Goal: Gather alternative data

1. Run `/deep-research` to gather information from multiple sources
2. Use CRW for web search and scraping
3. Search the NPM Registry and GitHub
4. Use DeepWiki and Context7 for documentation

### 3. Compare Alternatives

> Goal: Compare the alternatives

1. Gather the relevant alternatives
2. Compare features, performance, and maintenance
3. Analyze the pros/cons of each option
4. Check community support and ecosystem

### 4. Recommend Best Option

> Goal: Recommend the most suitable option

1. Recommend the most suitable option
2. Explain the reasoning behind the choice
3. Provide examples or migration guides
4. Note the trade-offs to consider

## Rules

### Research Strategy

- Always run `/deep-research` before recommending
- Use multiple sources (CRW, NPM, GitHub, DeepWiki, Context7)
- Verify the credibility of the sources
- Compare data across several sources
- Check that the information is up to date

### Comparison Criteria

- Features and capabilities
- Performance and benchmarks
- Maintenance and updates
- Community support and ecosystem
- Learning curve and documentation
- License and commercial support

### Context Awareness

- The tech stack in use
- Team expertise and experience
- Project requirements and constraints
- Long-term maintenance considerations
- Migration cost and effort

### Recommendation Guidelines

- Explain the reasoning clearly
- Note the trade-offs to consider
- Provide examples or code snippets
- Recommend migration paths when needed
- Give references for deeper learning
- Use /compare-competitors when needed

## Expected Outcome

- Better alternatives with a comparison
- A recommendation suited to the context
- Clear pros/cons and trade-offs
- Examples or migration guides
- References for deeper learning

