---
name: fe-poc-doc
description: Create and maintain Proof of Concept documentation for customer engagements
user-invocable: true
---

# POC Documentation Workflow

This skill creates comprehensive Proof of Concept (POC) documentation for customer engagements with Databricks. POC docs serve as the single source of truth for scope, success criteria, timelines, staffing, and evaluation results throughout the engagement.

## Quick Start

**Invoke the `fe-poc-doc` agent** to handle the full POC documentation workflow:

```
Task tool with subagent_type='fe-workflows:fe-poc-doc' and model='opus'
```

Pass the user's request with available sources. The agent will:
1. Parse the sources from the user's request (customer name, Salesforce opportunity, existing docs)
2. Gather data from Salesforce, JIRA, Slack, Glean, and/or existing documents
3. Collaborate with the user to define scope, success criteria, and timeline
4. Generate a Google Doc following the POC document template
5. Output a shareable, customer-facing POC document

## Source Types

The skill accepts multiple source types to bootstrap the POC document:

| Source Type | Identifier Format | Example |
|-------------|-------------------|---------|
| Google Doc | URL or Doc ID | `https://docs.google.com/document/d/...` |
| Salesforce Opportunity | Opp ID or URL | `0061234567890ABCDEF` |
| Salesforce Account | Account name | `Meta`, `CrowdStrike` |
| JIRA Ticket | ES-XXXXXX | `ES-1234567` |
| Slack Channel | Channel ID or URL | `C0A4EHNKHLH` or Slack URL |
| Customer/Account Name | Company name | `Pinterest`, `Block`, etc. |

## Example Invocations

```
User: Create a POC doc for the Meta evaluation. Here's the Salesforce opp: 0061234567890ABCDEF
--> Agent gets opportunity details, gathers account context, creates POC doc framework

User: Build a POC document for CrowdStrike. They want to evaluate Unity Catalog and Managed Iceberg.
--> Agent searches for CrowdStrike context, asks for scope details, generates POC doc

User: I need a POC doc for Acme Corp. Here's the internal slack channel: #acme-poc-internal
--> Agent validates Slack MCP, reads channel history, extracts scope/goals, creates POC doc

User: Update the POC doc for Discord with the latest evaluation results
--> Agent reads existing doc, asks for results, updates the document
```

## Pre-Requisites

### Salesforce Access
The agent uses `sf` CLI to pull opportunity and account details. Ensure authentication is active via the `salesforce-authentication` skill.

### Slack Sources
If the user provides Slack channels/threads as sources, the agent will validate MCP access using the `validate-mcp-access` skill. The user must have active credentials for `slack` before proceeding.

### Glean Access
The agent uses Glean to search for additional context on the customer, related internal docs, and competitive intelligence. Glean MCP access should also be validated if not already active.

## Document Structure

The POC document follows this structure (based on exemplary POC documents for strategic accounts):

### 1. Header
- Company branding: `[Customer Name] // Databricks`
- Title: `[Use Case/Product] POC` (e.g., "Unity Catalog and Managed Iceberg POC")

### 2. Key Contacts
Two tables separating Databricks and customer contacts:

**Databricks Key Contacts** - Name and role for each (AE, SA, SA Manager, engineering overlays, PS resources)

**Customer Key Stakeholders** - Name and title/role for each decision maker and technical lead

### 3. Executive Alignment
Chronological list of executive-level meetings completed and upcoming:
- Date, attendees (customer exec + Databricks exec), and meeting purpose
- Include "Next Alignment" entry for scheduled upcoming meetings

### 4. Summary & Scope
- 1-2 paragraphs describing the customer's business context
- Why they are evaluating Databricks
- What teams/departments are involved
- Current pain points driving the evaluation

### 5. Business Use Cases
For each use case being evaluated:
- **Use case name** (e.g., "Supply Chain - Command Center")
- **Overview:** 2-3 sentences describing the business problem
- **Goals:** Bulleted list of measurable objectives

### 6. Positive Business Outcomes (PBOs)
3-4 outcomes that quantify the value of a successful POC:
- **Outcome title** (e.g., "Near real-time data availability")
- **Description:** How Databricks addresses the need and what value it delivers

### 7. Project Summary
- Brief paragraph describing the POC engagement
- Start and end dates
- High-level goal statement
- Reference to timeline chart (if applicable)

### 8. POC Scope & Success Criteria
Table organized by phase:

| OKR | Business Value | Scope | Success Criteria | Status |
|-----|---------------|-------|-----------------|--------|

Each row includes:
- Specific, measurable OKR
- Business value statement
- Data sources/tables/frameworks in scope
- Quantitative success criteria (latency, throughput, concurrency, etc.)
- Status tracking

### 9. Tasks and Timeline
Detailed task breakdown organized by phase:

| Task | Customer Owner | Databricks Owner | Comments | Target Due Date | Status | Notes |
|------|---------------|-----------------|----------|----------------|--------|-------|

Covering: kickoff, environment setup, data delivery, testing, validation, readout

### 10. POC Staffing Plan
Tables for both sides:

**Databricks Resources:** Name, Role, Focus Area, Engagement Model (full-time dedicated / full-time overlay / part-time overlay)

**Customer Resources:** Name, Role, Focus Area, Engagement Model

Meeting cadence: kickoff call, weekly progress reports, daily standups, final readout

### 11. Current State & Architecture
- Description of customer's current architecture and key components
- Challenges with current state
- Diagram placeholder
- Technologies being evaluated (Databricks and any competitors)

### 12. Mutual Success Plan
Execution plan table:

| Objective | Actions | Owner | Timeline | Status |
|-----------|---------|-------|----------|--------|

Covering: funding, executive alignment, workspace creation, POC phases, post-POC surveys

### 13. Evaluation Results
- Section to be filled during and post-POC
- Results against each OKR with quantitative metrics

### 14. Resources
- Links to relevant documentation, demo decks, and product docs

### 15. Notes
- Running notes section for meeting notes, decisions, and action items

## Formatting Rules

### Writing Style
- **Customer-facing document** - Professional, polished, suitable for sharing externally
- **Specific and measurable** - Success criteria must be quantitative where possible
- **Action-oriented** - Every task has an owner and timeline
- **Collaborative tone** - Joint effort between Databricks and the customer

### People
- Use `@FirstName LastName` format for Databricks employees
- Include title/role for all contacts
- Separate Databricks and customer contacts into distinct tables

### Companies
- Always use actual company name
- Never use "the customer" or "the prospect"
- Title format: `[Customer Name] // Databricks`

### Links
- JIRA: `[ES-XXXXXX](https://databricks.atlassian.net/browse/ES-XXXXXX)`
- Slack: `[#channel-name](slack-url)` or `[Thread](slack-url)`
- Salesforce: `[Opportunity](sf-url)`
- Docs: `[Document Title](doc-url)`

### Tables
- Use consistent column alignment
- Bold phase headers within tables
- Include status columns (empty for new docs, filled during POC)

### Success Criteria
- Must be **quantitative and measurable** (e.g., "<5 minute data delivery", "P95 SLA of 3-4 seconds", "600 concurrent users")
- Include units and thresholds
- Avoid vague criteria like "performs well" or "meets expectations"

### Paragraph Spacing
- Always include blank lines between paragraphs
- Use `\n\n` (double newline) between paragraphs in markdown
- Ensure visual separation between sections for readability

## What Makes a Great POC Document

Based on exemplary POC documents:

1. **Clear scope boundaries** - Explicitly defines what is in and out of scope per phase
2. **Measurable success criteria** - Every OKR has quantitative, testable metrics
3. **Defined ownership** - Every task and deliverable has a named owner on both sides
4. **Phased approach** - Logical progression from foundational (data delivery) to advanced (AI/analytics)
5. **Executive alignment documented** - Shows executive buy-in and engagement cadence
6. **Staffing clarity** - Clear roles, focus areas, and engagement models (full-time vs overlay)
7. **Business value articulated** - Connects technical OKRs to business outcomes
8. **Customer architecture context** - Documents current state to ground the evaluation
9. **Living document** - Includes status columns and evaluation results sections for ongoing updates

## Resources

- `resources/POC_DOC_TEMPLATE.md` - Full document template
- `resources/SECTION_GUIDANCE.md` - Detailed guidance for each section
- `agents/fe-poc-doc.md` - Agent implementation details
