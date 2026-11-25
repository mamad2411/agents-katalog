# Skill: Research

## When to Use
Activate when a task requires gathering information from multiple sources, comparing options,
or synthesizing findings into a recommendation. This includes technology comparisons, market
research, architecture decisions, and "how does X work" questions that need depth.

## Process

### 1. Decompose the Question
Break the research question into 2-5 independent sub-questions. Each sub-question should be
answerable on its own.

Example: "Should we use Postgres or MongoDB for this project?" breaks into:
- What are the data modeling requirements?
- What are the read/write patterns?
- What does each database handle well at our expected scale?
- What is the operational complexity of each?
- What does the team already know?

### 2. Research in Parallel
Investigate sub-questions independently. For each sub-question:
- Search for primary sources (official docs, benchmarks, case studies)
- Look for counter-arguments and failure cases, not just success stories
- Note the recency and credibility of each source
- If using web search, run multiple queries with different phrasings

### 3. Synthesize
Combine findings into a coherent picture. Look for:
- Points where sources agree (high confidence)
- Points where sources conflict (flag these explicitly)
- Gaps where no good data exists (say "I don't know" rather than guessing)

### 4. Form a Recommendation
Take a position. "It depends" is not a recommendation. State:
- What you recommend and why
- What the key tradeoff is
- What would change your recommendation

## Output Format

```
## Research: [Topic]

### Question
[The original question, restated clearly]

### Key Findings
- [Finding 1] -- [Source]
- [Finding 2] -- [Source]
- [Finding 3] -- [Source]

### Analysis
[2-4 paragraphs synthesizing findings. Flag conflicts and unknowns.]

### Recommendation
[Clear recommendation with reasoning. State the tradeoff.]

### Sources
1. [URL or reference] -- [what it contributed]
2. [URL or reference] -- [what it contributed]
```

## Rules
- Never present a single source as definitive. Cross-reference.
- Always include at least one counterpoint to the recommendation.
- Date-stamp findings when recency matters (APIs change, benchmarks age).
- If the research is inconclusive, say so. A clear "not enough data" beats a confident guess.
