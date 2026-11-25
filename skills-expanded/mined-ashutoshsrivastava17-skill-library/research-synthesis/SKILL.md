---
name: research-synthesis
description: >
  Synthesize user research into actionable themes, insights, and recommendations.
  TRIGGER when: user says "synthesize research", "analyze interviews", "find patterns",
  "research themes", "insight mapping", or has raw research data to distill.
argument-hint: "[research data file or description]"
user-invocable: true
---

# Research Synthesis

Transform raw user research (interviews, surveys, usability tests, support tickets) into structured insights that drive design and product decisions.

## Synthesis Process

### Phase 1 — Ingest Raw Data

1. If `$ARGUMENTS` is a file path, read it.
2. Identify the research type:
   - **Interviews**: transcripts, notes
   - **Surveys**: quantitative + open-ended responses
   - **Usability tests**: task success/failure, observations, quotes
   - **Support tickets**: categorized complaints, feature requests
   - **Analytics**: behavioral data, funnel metrics
3. If data is insufficient, ask what research was conducted and key findings.

### Phase 2 — Code & Cluster

#### Affinity Mapping

1. **Extract observations**: Pull discrete data points — quotes, behaviors, pain points, needs.
2. **Tag each observation** with:
   - Participant/source ID
   - Sentiment: positive / negative / neutral
   - Category: behavior / pain-point / need / workaround / delight / confusion
3. **Cluster into themes**: Group related observations. A theme needs 3+ observations from 2+ sources.
4. **Name each theme**: Use user-centric language ("Users distrust auto-save" not "Save feature issue").

### Phase 3 — Generate Insights

For each theme, produce a structured insight:

```
### Insight: {descriptive title}

**Observation**: {What we saw — grounded in data}
- "{direct quote}" — P3
- "{direct quote}" — P7
- {N} of {total} participants exhibited this behavior

**Interpretation**: {What it means — our analysis}

**Implication**: {What we should do about it — actionable recommendation}

**Confidence**: High / Medium / Low
- Based on: {N} sources, {method type}, consistency of signal

**Priority**: {Critical / High / Medium / Low}
- Impact: {how many users affected, severity of pain}
- Effort: {estimated implementation complexity}
```

### Phase 4 — Prioritization Matrix

Plot insights on an impact/effort matrix:

```
## Priority Matrix

### High Impact, Low Effort (Do First)
1. {Insight title} — {one-line summary}

### High Impact, High Effort (Plan)
1. {Insight title} — {one-line summary}

### Low Impact, Low Effort (Quick Wins)
1. {Insight title} — {one-line summary}

### Low Impact, High Effort (Deprioritize)
1. {Insight title} — {one-line summary}
```

### Phase 5 — Output Report

```
## Research Synthesis — {project/study name}

### Study Overview
- **Method**: {interviews / survey / usability test / mixed}
- **Participants**: {N} participants, {demographics or segments}
- **Date**: {when research was conducted}
- **Research questions**: {what we were trying to learn}

### Key Themes
1. {Theme name} — {N} observations from {N} sources
2. {Theme name} — ...

### Insights (ordered by priority)
{structured insights from Phase 3}

### Recommendations
1. **{Action}** — addresses insights {1, 3}. Priority: {High}
2. **{Action}** — addresses insight {2}. Priority: {Medium}

### Open Questions
- {Questions the research raised but didn't answer}
- {Suggested follow-up research}

### Raw Data Summary
- Total observations coded: {N}
- Themes identified: {N}
- Insights generated: {N}
```

## Quality Standards

- **Ground every insight in data**: No interpretation without at least 2 supporting observations.
- **Distinguish observation from interpretation**: Keep them separate — observations are facts, interpretations are analysis.
- **Include dissenting data**: If 8/10 users loved a feature but 2 hated it, note both.
- **Quantify where possible**: "Most users" is weak. "7 of 10 users" is strong.
- **Preserve participant voices**: Include direct quotes — they're the most compelling evidence.
- **Flag confidence levels**: Be honest about what the data supports vs. what's inferred.

## Quality Checklist

- [ ] Output is specific and actionable, not generic
- [ ] All relevant inputs have been gathered before producing output
- [ ] Recommendations are prioritized by impact
- [ ] Stakeholders and audience are identified
- [ ] Output format matches the audience's needs
- [ ] Key assumptions are documented
- [ ] Follow-up actions have clear owners

## Edge Cases

- If input data is incomplete, state assumptions explicitly and flag gaps
- For time-sensitive situations, prioritize speed over comprehensiveness
- If multiple stakeholders have conflicting needs, document the tradeoffs
- For first-time use, start with a simplified version and iterate
- Adapt the depth and detail to the audience's expertise level
