---
name: draft-rca
description: Draft Root Cause Analysis documents for incidents using Salesforce, JIRA, Slack, and email sources
user-invocable: true
---

# Draft RCA Workflow

This skill drafts Root Cause Analysis (RCA) documents by gathering information from multiple sources and creating a well-formatted Google Doc.

## Quick Start

**Invoke the `rca-doc` agent** to handle the full RCA workflow:

```
Task tool with subagent_type='fe-workflows:rca-doc' and model='opus'
```

Pass the user's request directly to the agent. The agent will:
1. Parse the sources from the user's request
2. Gather data from JIRA, Salesforce, Slack, and/or email
3. Cross-reference related artifacts
4. Validate sufficiency (95% confidence threshold)
5. Generate the Google Doc using the google-drive agent

## Supported Source Types

| Source Type | Identifier Format | Example |
|-------------|-------------------|---------|
| Salesforce Case | Case number or URL | `5001234567` or SF URL |
| JIRA ES Ticket | ES-XXXXXX | `ES-1667009` |
| Slack Thread | Channel ID + thread ts, or URL | `C0A4EHNKHLH` or Slack URL |
| Email | Email thread URL or subject | Gmail URL |

## Example Invocations

```
User: Create an RCA for ES-1667009 and slack channel C0A4EHNKHLH
→ Agent gathers data from JIRA and Slack, cross-references, creates doc

User: Draft RCA for the Block Iceberg incident
→ Agent uses Glean to search, asks for clarification if ambiguous

User: RCA for Salesforce case 5001234567
→ Agent gets case, finds linked JIRA, gathers Slack if linked, creates doc
```

## Agent Behavior

The `rca-doc` agent will:

1. **Parse sources** - Identify JIRA tickets, Slack channels, SF cases from user request
2. **Handle ambiguity** - Use Glean to search; ask user if multiple matches found
3. **Gather data** - Pull details from each source using appropriate tools
4. **Cross-reference** - Find linked artifacts (JIRA↔Salesforce, Slack links in comments)
5. **Validate** - Ensure 95%+ confidence before proceeding; request more info if needed
6. **Generate doc** - Create Google Doc following the template in `resources/RCA_TEMPLATE.md`

## Document Formatting Rules

The agent follows these formatting requirements:

| Element | Format |
|---------|--------|
| People | `@FirstName LastName` (never just first name) |
| Companies | Actual name (never "customer" or "the customer") |
| JIRA links | `[ES-XXXXXX](https://databricks.atlassian.net/browse/ES-XXXXXX)` |
| Slack links | `[#channel](slack-url)` or `[Thread](slack-url)` |
| SF links | `[Case XXXXXXXX](sf-url)` |
| Timeline | Customer-facing events only (reported → validated → resolved) |
| Root cause | Include triggering conditions; note uncertainty if applicable |
| Action items | Include lessons learned; must have owner and status |

## Document Structure

1. Incident Summary (table with company, JIRA, SF case, severity, status)
2. Problem Statement (2-4 sentences, use company name)
3. Root Cause (with triggering conditions)
4. Impact
5. Timeline (customer-facing events only - NO internal JIRA events)
6. Resolution (immediate mitigation, verification, long-term recommendations)
7. Key Personnel (@mentions, roles)
8. Action Items (with lessons learned incorporated)
9. References (all embedded links)

## Resources

- `resources/RCA_TEMPLATE.md` - Full document template
- `agents/rca-doc.md` - Agent implementation details