---
name: search-strategy
description: >
  Plan and execute a multi-source search strategy for complex queries that
  require searching across multiple enterprise tools with different query
  syntaxes, filters, and relevance models. Decomposes broad questions into
  targeted sub-queries and merges results into a ranked answer set.
  TRIGGER when: user asks to plan a search, needs help finding something
  complex, wants a search strategy, asks "how should I search for X",
  or has a multi-faceted research question.
argument-hint: "<complex query or research question> [--sources SOURCE1,SOURCE2]"
user-invocable: true
---

# Multi-Source Search Strategy

Plan, execute, and refine search strategies for complex enterprise queries that span multiple tools and require iterative refinement.

## Strategy Planning Process

### Step 1: Analyze the Query

Break down the user's question into searchable components:

| Component          | Description                                    | Example                          |
|--------------------|------------------------------------------------|----------------------------------|
| Core concepts      | Primary topics or entities                     | "authentication", "SSO"         |
| Qualifiers         | Narrowing attributes                           | "for mobile app", "in Q3"       |
| Entity types       | People, projects, teams, dates                 | "by security team", "Project X" |
| Intent             | What the user actually needs                   | Decision history, how-to, status|
| Time constraints   | Recency requirements                           | "last month", "current"         |

### Step 2: Select Target Sources

Evaluate which sources are most likely to contain relevant results:

| Source Type      | Best For                                          | Query Style          |
|------------------|---------------------------------------------------|----------------------|
| Email            | Decisions, approvals, external communication      | People + topic       |
| Chat / Slack     | Quick decisions, links, informal context           | Channel + keywords   |
| Documents        | Specs, proposals, formal write-ups                 | Title + content      |
| Wiki             | Processes, architecture, onboarding, policies      | Topic + category     |
| Tickets / Issues | Implementation details, bugs, requirements         | Labels + text        |
| Code             | Technical implementation, comments, configs        | Symbol + file path   |
| Calendar         | Meeting context, attendees, scheduling             | People + date range  |

Source selection matrix:

| Query Intent            | Primary Sources         | Secondary Sources     |
|-------------------------|-------------------------|-----------------------|
| "How does X work?"      | Wiki, Docs, Code        | Tickets, Chat         |
| "What was decided?"     | Email, Chat, Docs       | Tickets, Wiki         |
| "Who is responsible?"   | Tickets, Wiki, Chat     | Email, Calendar       |
| "What is the status?"   | Tickets, Chat, Email    | Docs, Calendar        |
| "When did X happen?"    | Email, Chat, Tickets    | Docs, Calendar        |
| "Why was X done?"       | Email, Chat, Docs       | Tickets, Code         |

### Step 3: Formulate Sub-Queries

Transform the original query into source-specific sub-queries:

```
Original: "Why did we switch from Redis to DynamoDB for session storage?"

Sub-queries:
1. Wiki     → "session storage" OR "DynamoDB" OR "Redis migration"
2. Docs     → "session" AND ("DynamoDB" OR "Redis") — type:proposal OR type:design-doc
3. Email    → "session storage" OR "Redis replacement" — from:engineering-leads
4. Chat     → "DynamoDB sessions" OR "Redis sessions" — channels:#backend,#architecture
5. Tickets  → labels:infrastructure "session" AND ("Redis" OR "DynamoDB")
6. Code     → path:*session* OR path:*config* "dynamodb" — recent commits
```

### Step 4: Define Execution Plan

```
# Search Execution Plan

## Query: [original query]
## Decomposition:
- Concept A: [term variations and synonyms]
- Concept B: [term variations and synonyms]
- Filter: [time range, people, teams]

## Execution Order:
1. [High-priority source] — [specific query] — Expected: [what we hope to find]
2. [Medium-priority source] — [specific query] — Expected: [what we hope to find]
3. [Lower-priority source] — [specific query] — Expected: [what we hope to find]

## Refinement Triggers:
- If Step 1 finds [X], narrow Step 2 to [Y]
- If Step 1 finds nothing, broaden Step 2 to [Z]
- If conflicting results, add Step 4: [verification query]
```

### Step 5: Execute and Merge Results

## Result Ranking Framework

Score each result on four dimensions:

| Dimension     | Weight | Criteria                                              |
|---------------|--------|-------------------------------------------------------|
| Relevance     | 40%    | How directly it answers the query                     |
| Authority     | 25%    | Source reliability, author expertise, formality level  |
| Recency       | 20%    | How current the information is                        |
| Uniqueness    | 15%    | Does it add information not found in other results    |

Composite score: `(Relevance * 0.4) + (Authority * 0.25) + (Recency * 0.2) + (Uniqueness * 0.15)`

## Output Format

```
# Search Strategy Report
Query: [original question]
Sources searched: [N] | Results found: [N] | Top results: [N]

## Search Plan Executed
| Step | Source   | Query Used                    | Results |
|------|----------|-------------------------------|---------|
| 1    | [Source] | [query]                       | [N]     |
| 2    | [Source] | [query]                       | [N]     |

## Top Results (Ranked)
### 1. [Result Title] — [Source] — Score: [X/10]
- **Relevance**: [why this matches]
- **Key excerpt**: "[relevant quote]"
- **Date**: [date] | **Author**: [author]

### 2. [Result Title] — [Source] — Score: [X/10]
- **Relevance**: [why this matches]
- **Key excerpt**: "[relevant quote]"
- **Date**: [date] | **Author**: [author]

## Answer Summary
[Synthesized answer based on top results]

## Search Refinement Suggestions
- To find more: try [broader query suggestion]
- To narrow down: add [filter suggestion]
- Unexplored sources: [sources not yet queried and why they might help]
```

## Query Optimization Techniques

| Technique            | When to Use                        | Example                              |
|----------------------|------------------------------------|--------------------------------------|
| Synonym expansion    | Initial search yields few results  | "auth" → "authentication", "login"  |
| Phrase matching      | Too many irrelevant results        | "session storage" (exact phrase)     |
| Author filtering     | Known domain experts exist         | from:jane.doe OR from:john.smith     |
| Date narrowing       | Topic changed over time            | after:2025-01-01                     |
| Negative filtering   | Known false positives              | NOT "session recording"              |
| Channel scoping      | Known relevant channels            | in:#backend-eng                      |
| Label/tag filtering  | Structured metadata available      | label:architecture, tag:approved     |

## Iterative Refinement

After initial results, determine if refinement is needed:

- **Too many results (>50)**: Add filters, use phrase matching, narrow date range
- **Too few results (<3)**: Expand synonyms, broaden date range, add sources
- **Wrong results**: Analyze why results are off-topic, add negative filters
- **Partial answer**: Identify the gap and formulate a targeted follow-up query

## Edge Cases

- **Ambiguous queries**: Ask the user to clarify before executing; present 2-3 interpretations
- **No results anywhere**: Suggest the information may not exist in connected sources; recommend who to ask
- **Cross-language content**: Note if sources contain content in multiple languages; expand queries accordingly
- **Acronyms and jargon**: Expand acronyms in queries and search for both forms
- **Stale indexes**: If a source's index is known to be delayed, warn about potential missing recent items

## Quality Checklist

- [ ] Query decomposed into at least 2 sub-queries
- [ ] At least 3 sources considered
- [ ] Results ranked by composite score
- [ ] Conflicting information flagged
- [ ] Knowledge gaps identified
- [ ] Refinement suggestions provided
