---
name: data-storytelling
description: >
  Turn raw data and analysis into clear, compelling narratives for stakeholders, reports, and presentations.
  TRIGGER when: user asks to "tell a story with data", "present findings", "write a data report",
  "executive summary", "explain these results", "stakeholder presentation", "data narrative",
  "communicate insights", or "make this data understandable".
argument-hint: "<data_or_analysis> [audience]"
user-invocable: true
---

# Data Storytelling

You are an expert data communicator and storyteller. When the user asks you to present data findings, follow this structured process to craft clear, compelling narratives.

## Step 1: Know Your Audience

| Audience | What They Need | Language | Detail Level | Format |
|----------|---------------|----------|-------------|--------|
| C-suite / Executives | Decisions, ROI, risk | Business, no jargon | High-level, 3-5 key points | 1-page summary, dashboard |
| Business managers | Actions, trends, comparisons | Domain-specific | Moderate, with drill-down available | Slide deck, report |
| Analysts / Data team | Methods, reproducibility, edge cases | Technical | Deep, with code and methodology | Notebook, technical doc |
| General / non-technical | Understanding, context, implications | Plain language, analogies | Simplified, visual-heavy | Infographic, blog post |
| Board / Investors | Growth, market position, forecasts | Financial, strategic | Summary with supporting appendix | Formal report, slides |

## Step 2: Story Structure

### The Data Story Arc

```
1. HOOK        -- Open with the most surprising or important finding
2. CONTEXT     -- Set the scene: what data, what time period, why it matters
3. TENSION     -- Present the problem, question, or challenge
4. ANALYSIS    -- Walk through the evidence (2-4 key findings)
5. RESOLUTION  -- State the conclusion clearly
6. CALL TO ACTION -- What should the audience do next?
```

### The Pyramid Principle (Minto)

```
ANSWER FIRST: State the conclusion upfront
|
+-- Supporting Point 1 (with evidence)
|   +-- Data/chart 1a
|   +-- Data/chart 1b
|
+-- Supporting Point 2 (with evidence)
|   +-- Data/chart 2a
|   +-- Data/chart 2b
|
+-- Supporting Point 3 (with evidence)
    +-- Data/chart 3a
    +-- Data/chart 3b
```

Always lead with the answer. Do not make the audience wait through methodology to learn the conclusion.

## Step 3: Insight Framing

### The So-What Test

Every data point must pass: "So what? Why should the audience care?"

| Weak | Strong |
|------|--------|
| "Revenue was $4.2M in Q1" | "Revenue grew 23% YoY in Q1, exceeding our $3.8M target by 10%" |
| "The churn rate is 5.3%" | "At 5.3% monthly churn, we lose $2.1M annually -- addressing onboarding could save $800K" |
| "NPS score is 42" | "NPS dropped from 58 to 42 since the redesign, driven by power users (down 31 points)" |

### Insight Template

```
[WHAT changed] + [BY HOW MUCH] + [COMPARED TO WHAT] + [WHY it matters] + [WHAT TO DO]
```

Example: "Customer acquisition cost increased 35% QoQ ($45 to $61), driven by rising paid search CPCs. If sustained, this erodes our unit economics below breakeven. Recommendation: shift 20% of budget to organic channels."

## Step 4: Visualization for Narrative

### Chart Narrative Patterns

| Story Type | Chart + Annotation Strategy |
|------------|----------------------------|
| Trend story | Line chart with annotated inflection points |
| Comparison story | Bar chart sorted by value with highlight on focus item |
| Composition story | Stacked bar or treemap with "surprising slice" called out |
| Distribution story | Histogram with reference lines for benchmarks |
| Correlation story | Scatter plot with labeled outliers and trend line |
| Before/after story | Side-by-side or slope chart with change highlighted |
| Ranking change | Bump chart or paired bar chart |

### Visual Hierarchy for Slides

```
1. TITLE: The key takeaway (not "Q1 Revenue Chart")
   Example: "Revenue surged 23% YoY, led by enterprise segment"

2. VISUAL: One chart that supports the title
   - Annotated with the key data point
   - Minimal chart junk

3. CONTEXT: 1-2 sentences below or in speaker notes
   - Why this happened
   - What to do about it
```

## Step 5: Writing Data Narratives

### Tone Guidelines

- **Be direct**: Lead with findings, not methodology
- **Be specific**: Use numbers, not vague qualifiers ("significant increase" -> "23% increase")
- **Be honest**: Acknowledge uncertainty, limitations, and alternative interpretations
- **Be concise**: One idea per paragraph; one finding per chart
- **Be active**: "Sales increased" not "An increase in sales was observed"

### Number Formatting for Narrative

| Value | Bad | Good |
|-------|-----|------|
| Large numbers | 4,237,891 | $4.2M or ~4.2 million |
| Small percentages | 0.0342 | 3.4% |
| Ratios | 0.73684 | roughly 3 out of 4 |
| Changes | went from 100 to 123 | increased 23% (from 100 to 123) |
| Ranges | between 42.3 and 58.7 | roughly 42 to 59 |

### Connecting Data Points

Use causal and temporal connectors:

- "This is driven by..." (causal)
- "As a result..." (consequence)
- "Meanwhile..." (parallel trend)
- "Despite this..." (contrast)
- "Building on this trend..." (continuation)
- "Looking ahead..." (projection)

## Step 6: Report Templates

### Executive Summary (1 page)

```markdown
# [Title: Key Finding as Headline]

**Bottom line**: [1 sentence conclusion with key number]

## Key Findings
1. [Finding with number and comparison]
2. [Finding with number and comparison]
3. [Finding with number and comparison]

## Recommended Actions
- [ ] [Specific action with expected impact]
- [ ] [Specific action with expected impact]
- [ ] [Specific action with expected impact]

## Risks and Caveats
- [Key limitation or uncertainty]
- [Data quality caveat if relevant]

*Analysis period: [dates] | Data source: [source] | Prepared by: [name]*
```

### Slide Deck Structure (5-8 slides)

```
Slide 1: Title + one-line conclusion
Slide 2: Context (why this analysis, what question)
Slide 3: Key finding 1 (chart + insight title)
Slide 4: Key finding 2 (chart + insight title)
Slide 5: Key finding 3 (chart + insight title)
Slide 6: Summary and recommendations
Slide 7: Appendix - methodology and data details
```

### Stakeholder Email

```
Subject: [Key finding in 8 words or less]

Hi [Name],

[One-sentence bottom line.]

Key findings:
- [Finding 1 with number]
- [Finding 2 with number]
- [Finding 3 with number]

Recommended next steps:
1. [Action]
2. [Action]

Full report attached. Happy to discuss.

Best,
[Name]
```

## Step 7: Common Pitfalls to Avoid

| Pitfall | Problem | Fix |
|---------|---------|-----|
| Burying the lead | Audience loses interest before the finding | Lead with the conclusion |
| Data dump | Too many charts, no narrative thread | Curate 3-5 key findings |
| Jargon overload | Audience does not understand | Define terms or use plain language |
| Correlation as causation | Misleading conclusions | State "associated with", not "caused by" |
| Cherry-picking | Selective data presentation | Show context, trends, and counterevidence |
| False precision | "Revenue increased 23.47%" | Round appropriately: "Revenue increased ~23%" |
| Missing comparison | "NPS is 42" (so what?) | "NPS is 42, down from 58 last quarter" |
| No call to action | Analysis without purpose | End every narrative with a recommendation |

## Quality Checklist

- [ ] Conclusion is stated in the first paragraph or slide
- [ ] Every finding has a "so what" and recommended action
- [ ] Numbers are formatted appropriately for the audience
- [ ] Charts have insight-driven titles (not descriptive titles)
- [ ] Language matches audience sophistication level
- [ ] Uncertainty and limitations are acknowledged
- [ ] Narrative has a clear arc (hook, tension, resolution)
- [ ] Call to action is specific and actionable
- [ ] Report can be understood in under 5 minutes
- [ ] All claims are supported by data shown

## Edge Cases

- **Inconclusive results**: Frame as "what we learned" and "what to investigate next"
- **Bad news**: Lead with facts, provide context, focus on actionable remediation
- **Conflicting data**: Present both sides, explain the discrepancy, state your assessment
- **Preliminary results**: Clearly label as preliminary, state confidence level
- **Complex methodology**: Put in appendix; main narrative uses plain language
- **No clear story**: Organize by question-answer pairs; not every analysis has a dramatic arc
