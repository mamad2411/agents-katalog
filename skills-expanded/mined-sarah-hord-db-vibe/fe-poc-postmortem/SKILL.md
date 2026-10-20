---
name: fe-poc-postmortem
description: Generate comprehensive post-mortem retrospectives for competitive POCs that we didn't win
user-invocable: true
---

# POC Post-Mortem Retrospective Skill

This skill generates comprehensive post-mortem retrospective documents for competitive Databricks POCs that we didn't win. The goal is to capture learnings that help the entire Field Engineering team improve for future engagements.

## Quick Start

**Invoke the `poc-postmortem` agent** to handle the full retrospective workflow:

```
Task tool with subagent_type='fe-workflows:poc-postmortem' and model='opus'
```

Pass the user's request with available sources. The agent will:
1. Parse the sources from the user's request
2. Validate MCP access if Slack sources are provided
3. Gather data from Salesforce, JIRA, Slack, Glean, and/or documents
4. Research any technical jargon or concepts for clarity
5. Synthesize findings into a narrative retrospective
6. Generate a Google Doc following the retrospective template

## Source Types

The skill accepts multiple source types:

| Source Type | Identifier Format | Example |
|-------------|-------------------|---------|
| Google Doc | URL or Doc ID | `https://docs.google.com/document/d/...` |
| Salesforce Opportunity | Opp ID or URL | `0061234567890ABCDEF` |
| JIRA Ticket | ES-XXXXXX | `ES-1234567` |
| Slack Channel | Channel ID or URL | `C0A4EHNKHLH` or Slack URL |
| Customer/Account Name | Company name | `Pinterest`, `Block`, etc. |

## Example Invocations

```
User: Create a POC postmortem for the Pinterest deal. Here's the internal POC doc: [Google Doc URL]
--> Agent reads doc, gathers related data, generates retrospective

User: Generate a postmortem for the Block POC loss. Slack channel is #block-poc-internal
--> Agent validates Slack MCP, gathers channel history, cross-references, generates retrospective

User: POC postmortem for Acme Corp opportunity 0061234567890ABCDEF
--> Agent gets Salesforce opp, finds related artifacts, generates retrospective
```

## Pre-Requisites

### Slack Sources
If the user provides Slack channels/threads as sources, the agent will first validate MCP access using the `validate-mcp-access` skill. The user must have active credentials for `slack` before proceeding.

### Glean Access
The agent uses Glean to:
- Search for additional context on the customer/POC
- Research technical jargon and concepts
- Find related internal documentation

Glean MCP access should also be validated if not already active.

## Document Structure

The generated retrospective follows this structure (based on exemplary POC retrospectives):

### 1. Header
- Title: `[Customer] + Databricks POC Retrospective`
- Authors: Primary FE and stakeholders involved
- Date range: POC start to end date
- Confidentiality notice

### 2. Summary
- 2-3 paragraph overview of the engagement
- High-level goals and scope
- Outcome and primary reasons for loss
- Key learnings teaser

### 3. Evaluation History and Progression
- Chronological narrative of the POC
- Key milestones and turning points
- Challenges encountered and how they were addressed
- This section should read like a story, not bullet points
- Include specific dates and events where known

### 4. Competition
- Overview of competitive landscape
- If multiple competitors, use subsections for each (e.g., "### Snowflake", "### Starburst")
- Description of competitor's solution(s)
- Key differentiators and advantages they had
- Analysis of why they were selected (if they won)
- Honest assessment of where we fell short

### 5. Evaluation Criteria
- How success was measured
- Customer's requirements and priorities
- Baseline vs optimized measurements
- What metrics mattered most to the customer

### 6. Challenges & Learnings
Organized by category. Common categories include:
- Technical challenges (performance, compatibility, etc.)
- Product gaps
- Process/engagement issues
- Competitive positioning
- Customer relationship/expectations

For each challenge:
- What happened
- Root cause (if known)
- How it was addressed (or not)
- Lesson learned for future POCs

### 7. Recommendations
- Product improvements needed
- Process changes for future POCs
- Competitive strategies
- Technical readiness improvements

### 8. Acknowledgments
- Team members who contributed
- Special recognition for above-and-beyond efforts

## Formatting Rules

### Writing Style
- **Narrative storytelling** for "Evaluation History and Progression" - tell the story
- **Technical but accessible** - explain jargon when first used
- **Honest and constructive** - acknowledge failures without blame
- **Specific and actionable** - include concrete examples and recommendations
- **Customer-centric** - use actual company name, never "the customer"
- **Professional headings** - use straightforward, descriptive section titles (not catchy ones)

### Paragraph Spacing
- Always include blank lines between paragraphs
- Use `\n\n` (double newline) between paragraphs in markdown
- Ensure visual separation between sections for readability

### People
- Use email-based @ mentions via Google Docs person chips (smart chips)
- Look up email addresses using Glean if only names are available
- Include roles where relevant (e.g., "Principal Solutions Architect")
- Person chips render as interactive elements with profile info on hover

### Companies
- Always use actual company name
- Never use "the customer" or "the prospect"

### Links
- JIRA: `[ES-1234567](https://databricks.atlassian.net/browse/ES-1234567)`
- Slack: `[#channel-name](slack-url)` or `[Thread](slack-url)`
- Salesforce: `[Opportunity](sf-url)`
- Docs: `[Document Title](doc-url)`

### Technical Content
- Include specific error messages, configurations, and metrics where relevant
- Explain technical concepts for readers who may not be SMEs
- Use tables for structured data (metrics, comparisons, timelines)

## What Makes a Great Retrospective

Based on exemplary retrospectives:

1. **Tells a compelling story** - Readers should understand not just what happened, but why
2. **Captures institutional knowledge** - Technical learnings that help others avoid the same pitfalls
3. **Honest about failures** - Acknowledges where we fell short without defensiveness
4. **Actionable recommendations** - Specific suggestions for product, process, and competitive strategy
5. **Respects the customer** - Professional tone even in discussing challenges
6. **Credits the team** - Acknowledges contributions from everyone involved

## Resources

- `resources/POC_RETROSPECTIVE_TEMPLATE.md` - Full document template
- `agents/poc-postmortem.md` - Agent implementation details
