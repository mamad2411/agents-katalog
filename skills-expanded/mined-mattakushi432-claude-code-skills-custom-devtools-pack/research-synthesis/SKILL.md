---
name: research-synthesis
description: "When to activate: research synthesis, thematic analysis, insight triangulation, research presentation, executive summaries, actionability, qualitative coding, findings communication"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: business
  domain: research
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Research Synthesis Patterns

## Synthesis Process

### Four-Stage Synthesis Model
```
1. IMMERSE — read all data without categorizing
   - Get a feel for the whole dataset
   - Note initial impressions (don't act on them yet)

2. CODE — tag segments with labels
   - Apply descriptive codes to raw data
   - Multiple codes per segment is fine

3. THEME — cluster codes into themes
   - Group related codes
   - Name themes with a verb phrase ("Users struggle to...")

4. INTERPRET — draw meaning and implications
   - What does this mean for the question?
   - What action does this suggest?
```

## Thematic Analysis

### Coding Approaches
| Approach | Description | When to Use |
|----------|-------------|-------------|
| **Inductive** | Codes emerge from data | Exploratory, no prior theory |
| **Deductive** | Codes applied from existing framework | Validating hypotheses |
| **Hybrid** | Start with framework, add new codes | Most research contexts |

### Coding Process
```
Raw data:
"I spend 20 minutes every morning just figuring out what to work on first.
 It's really frustrating because I have 50 emails and 30 Slack messages."

Descriptive codes:
- time_waste: 20 min daily on task prioritization
- frustration: negative emotion about process
- information_overload: 50+ inputs to process
- prioritization_difficulty: unclear what to do first

Interpretive codes:
- cognitive_overhead: mental effort required before productive work
- tool_fragmentation: multiple channels creating decision paralysis
```

### Affinity Diagram in Practice
```
Step 1: Write each insight on separate card/sticky
Step 2: Silently group related cards (no talking during sort)
Step 3: Name each cluster with a label that captures the theme
Step 4: Look for patterns across clusters

Example output:
THEME: "Prioritization is the hidden tax on productivity"
  • Users spend 15-30 min daily on task selection
  • No single source of truth for what matters
  • Manager interruptions reset prioritization work
  • 7/12 participants mentioned this unprompted

THEME: "Notifications create reactive not proactive work mode"
  • Push notifications pull attention from planned work
  • Average 23 context switches per hour (literature)
  • Users feel guilty ignoring notifications
  • High performers had turned off most notifications
```

## Triangulation

### Types of Triangulation
| Type | Method |
|------|--------|
| **Data** | Use multiple data sources (interviews + analytics + surveys) |
| **Investigator** | Multiple researchers analyze same data independently |
| **Method** | Quantitative + qualitative on same question |
| **Theory** | Apply multiple theoretical lenses to same data |

### Convergent Finding Statement
```
Strong finding (triangulated):
"Users struggle with task prioritization" is supported by:
✅ Interview data: 10/14 participants mentioned unprompted
✅ Survey data: 68% rated "knowing what to work on first" as a top 3 challenge
✅ Analytics: Average session starts with browsing/inbox-checking (not working)
✅ Support tickets: 12% of tickets tagged "confused about workflow"

Weak finding (single source only):
"Users want a dedicated mobile app" is supported by:
⚠️ 3 users requested it in open-ended survey question
❌ Not validated by behavior data or interviews
→ Flag as hypothesis to validate, not a confirmed insight
```

## Insight Framework

### Insight Statement Structure
```
Template:
[Who] experiences [what problem] when [context/trigger] because [root cause].
This matters because [business impact / opportunity size].

Example:
"New team managers experience decision paralysis when onboarding their first
direct report because they have no template or process to follow. This matters
because poor first onboarding experiences correlate with 2x higher 6-month
turnover rate."
```

### Prioritizing Insights
Score each insight on:
- **Frequency** — How many participants mentioned it? (1-5)
- **Intensity** — How strongly did they feel it? (1-5)
- **Actionability** — Can we do something about it? (1-5)
- **Business impact** — What does solving it mean for revenue/retention? (1-5)

Plot on 2x2: Frequency × Impact = prioritization matrix

## Executive Summary Structure

### Research Brief Format (1 page)
```
RESEARCH QUESTION
[Specific question the research answers]

METHODOLOGY
[What methods, N participants, timeframe]

TOP 3 FINDINGS

1. [Finding headline]
   Evidence: [Data point or quote]
   Implication: [What it means]

2. [Finding headline]
   Evidence: ___
   Implication: ___

3. [Finding headline]
   Evidence: ___
   Implication: ___

RECOMMENDED ACTIONS
□ [Action 1] — Owner: [Team] — Timeline: [Quarter]
□ [Action 2] — Owner: ___ — Timeline: ___

OPEN QUESTIONS
• [What remains unknown]
```

### Presenting to Leadership
```
Slide 1: The question we set out to answer
Slide 2: How we researched it (credibility)
Slide 3: Finding 1 + evidence + "so what"
Slide 4: Finding 2 + evidence + "so what"
Slide 5: Finding 3 + evidence + "so what"
Slide 6: Recommendations with prioritization
Slide 7: What we still don't know (shows rigor)
Appendix: Full data, participant quotes, methodology detail
```

## Qualitative Analysis Tools

### Software Options
| Tool | Best For | Cost |
|------|---------|------|
| NVivo | Complex qualitative research, large datasets | Paid |
| Atlas.ti | Academic research, team collaboration | Paid |
| Dovetail | UX research teams, tagging + insights | Paid SaaS |
| Notion | Simple research with small teams | Freemium |
| FigJam/Miro | Affinity mapping with distributed teams | Freemium |
| Excel/Airtable | Structured synthesis for mixed methods | Freemium |

### Simple Coding in Spreadsheet
```
Participant | Quote | Code 1 | Code 2 | Theme | Sentiment
P01 | "Takes forever to find X" | findability | frustration | navigation | negative
P02 | "I always know where to go" | findability | ease | navigation | positive
P03 | "Had to ask colleague" | findability | workaround | navigation | negative
```

## Research Output Types

### Deliverable Selection Guide
| Audience | Format |
|----------|--------|
| Engineering team | Jobs-to-be-done, pain point list, annotated journeys |
| Product team | Opportunity areas, prioritized insights, personas |
| Leadership | Executive brief, strategic implications |
| Design team | Journey maps, mental models, quotes wall |
| Sales team | Buyer insights, objection research, use case profiles |
| Marketing | Messaging insights, positioning inputs, voice of customer |
