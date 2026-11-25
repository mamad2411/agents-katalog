---
name: knowledge-synthesis
description: >
  Synthesize information from multiple enterprise sources into a coherent,
  well-structured summary. Combines data from email, chat, docs, wikis, and
  tickets to produce unified knowledge artifacts that eliminate information
  silos and surface connections across tools.
  TRIGGER when: user asks to synthesize, combine, consolidate, or merge
  information from multiple sources, create a knowledge summary, build a
  briefing document, or asks "what do we know about X".
argument-hint: "<topic or question> [--sources SOURCE1,SOURCE2] [--depth shallow|deep]"
user-invocable: true
---

# Knowledge Synthesis

Combine and reconcile information scattered across enterprise tools into a single, authoritative summary with proper attribution and confidence scoring.

## Synthesis Process

### Step 1: Understand the Knowledge Request

Classify the request type:

| Request Type        | Description                                | Depth   |
|---------------------|--------------------------------------------|---------|
| Quick Answer        | Simple factual question                    | Shallow |
| Topic Briefing      | Overview of a subject or project           | Medium  |
| Decision Support    | Comprehensive analysis for a decision      | Deep    |
| Onboarding Package  | Everything a new person needs to know      | Deep    |
| Competitive Intel   | Aggregated info about a competitor/market  | Deep    |
| Incident Postmortem | Timeline and facts about an event          | Deep    |

Extract from the user's request:
- **Core topic or question** being investigated
- **Scope boundaries** — what to include and exclude
- **Target audience** — who will consume this synthesis
- **Desired format** — narrative, bullet points, Q&A, timeline

### Step 2: Multi-Source Information Gathering

Query each relevant source with topic-appropriate search terms:

1. **Wiki / Knowledge Base** — Canonical documentation, policies, architecture docs
2. **Documents** — Specs, proposals, meeting notes, design docs
3. **Email** — Decisions, approvals, context from stakeholder threads
4. **Chat / Messaging** — Informal decisions, real-time discussions, shared links
5. **Tickets / Issues** — Implementation details, bugs, feature requests
6. **Code Repositories** — READMEs, comments, commit messages (if connected)

For each source, capture:
- The specific information found
- The date of the information
- The author or contributor
- The confidence level (verified, likely, uncertain)

### Step 3: Reconcile and Cross-Reference

| Situation                    | Resolution Strategy                                      |
|------------------------------|----------------------------------------------------------|
| Consistent across sources    | High confidence; cite multiple sources                   |
| Info only in one source      | Medium confidence; note single-source limitation         |
| Conflicting information      | Flag the conflict explicitly; show both versions + dates |
| Outdated in one, current in another | Prefer the most recent; note the evolution        |
| Informal vs. formal sources  | Prefer formal docs; note informal context if relevant    |

### Step 4: Structure the Synthesis

## Output Format

```
# Knowledge Synthesis: [Topic]
Generated: [date] | Sources: [count] sources across [count] tools
Confidence: [High/Medium/Low] — [reason]

## Executive Summary
[2-4 sentence overview of key findings]

## Key Facts
| Fact                     | Source          | Date       | Confidence |
|--------------------------|-----------------|------------|------------|
| [Fact 1]                 | [Source + link] | [date]     | High       |
| [Fact 2]                 | [Source + link] | [date]     | Medium     |

## Detailed Findings

### [Subtopic 1]
[Narrative synthesis of what is known]

**Sources:**
- [Source 1]: [what it contributed]
- [Source 2]: [what it contributed]

### [Subtopic 2]
[Narrative synthesis of what is known]

**Sources:**
- [Source 1]: [what it contributed]

## Conflicts and Ambiguities
- **[Topic]**: [Source A] says X (as of [date]), but [Source B] says Y (as of [date]).
  Recommended resolution: [suggestion]

## Knowledge Gaps
- [ ] [What is unknown or not found in any source]
- [ ] [Questions that remain unanswered]
- [ ] [Areas where information is stale and needs refresh]

## Timeline of Key Events
| Date       | Event                           | Source        |
|------------|---------------------------------|---------------|
| [date]     | [Event description]             | [Source]      |

## Source Index
| # | Source                | Type   | Last Updated | Items Used |
|---|----------------------|--------|--------------|------------|
| 1 | [Document name/link] | Doc    | [date]       | [count]    |
| 2 | [Channel name]       | Chat   | [date]       | [count]    |
| 3 | [Ticket ID]          | Ticket | [date]       | [count]    |
```

## Synthesis Depth Levels

### Shallow (Quick Answer)
- Search top 5 results per source
- Return the most authoritative single answer
- Include 1-2 supporting citations
- Target: under 200 words

### Medium (Topic Briefing)
- Search top 15 results per source
- Cross-reference across 2-3 sources minimum
- Identify key facts, people, and dates
- Target: 300-800 words

### Deep (Comprehensive Analysis)
- Exhaustive search across all sources
- Full cross-referencing and conflict resolution
- Timeline construction and trend analysis
- Knowledge gap identification
- Target: 800-2000 words

## Quality Standards

- **Attribution**: Every claim must cite at least one source
- **Recency**: Always note the date of information; flag anything older than 90 days
- **Neutrality**: Present conflicting viewpoints without bias
- **Completeness**: Explicitly state what was NOT found (knowledge gaps)
- **Traceability**: Reader should be able to verify any claim by following the source link
- **No hallucination**: Never infer or fabricate information not found in sources

## Edge Cases

- **No results found**: Report clearly that no information was found; suggest alternative search terms or sources to check manually
- **Single source only**: Produce the synthesis but prominently note the single-source limitation
- **Highly conflicting sources**: Escalate to the user before choosing a "winner"; present both sides
- **Sensitive or restricted content**: If a source indicates restricted access, note the existence of the source without revealing restricted content
- **Stale information**: If all sources are older than 6 months, add a staleness warning to the synthesis

## Follow-Up Options

After delivering the synthesis, offer:
1. "Want me to go deeper on any subtopic?"
2. "Should I search for additional sources to fill the knowledge gaps?"
3. "Want me to turn this into a shareable document or wiki page?"
4. "Should I set up alerts for new information on this topic?"

## Quality Checklist

- [ ] Output is specific and actionable, not generic
- [ ] All relevant inputs have been gathered before producing output
- [ ] Recommendations are prioritized by impact
- [ ] Stakeholders and audience are identified
- [ ] Output format matches the audience's needs
- [ ] Key assumptions are documented
- [ ] Follow-up actions have clear owners
