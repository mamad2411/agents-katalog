# Customer Report (360)

Build a comprehensive report on a single client by pulling structured data from Twenty CRM and conversational context from Gmail, Slack, Notion, Granola, and LinkedIn.

## MCP connectors

| Connector | Purpose |
|-----------|---------|
| CRM | Pull customer data and deal history |
| Notion | Read project notes and meeting logs |
| LinkedIn (TalkToHumans) | Search contacts, pull DM history and connection status |

## When to use

- "Everything we know about [client]"
- Pre-meeting brief
- Account health check
- Renewal or upsell prep

## Data sources

| Source | What to pull |
|--------|-------------|
| **Twenty CRM** | Company record, contacts, deal stage, ARR, contract dates, tags |
| **LinkedIn (TalkToHumans)** | Connection status, last DM date, conversation highlights, pending invitations |
| **Gmail** | Last 10 threads with the client domain - key topics, tone, open asks |
| **Slack** | Mentions of the client name in relevant channels - support issues, internal notes |
| **Granola** | Meeting transcripts with the client in last 90 days - decisions, commitments, sentiment |
| **Notion** | Any client-specific pages or project boards |

## Process

1. **Identify the client** - resolve the name to a CRM record; confirm if ambiguous
2. **Pull CRM data** - company, contacts, deal, contract, ARR, tags
3. **Pull LinkedIn data (TalkToHumans)** - search contacts, pull DM history, connection status
4. **Pull email threads** - summarize last 10 threads, flag open asks
5. **Pull Slack mentions** - summarize relevant messages, flag unresolved issues
6. **Pull meeting notes** - summarize last 3 meetings, extract commitments
7. **Pull Notion pages** - link any client-specific docs
8. **Reconcile** - flag contacts in LinkedIn/Gmail/Slack not in CRM, flag stage mismatches, flag commitments without tasks
9. **Synthesize** - identify patterns, risks, opportunities
10. **Output the report** using the template below

## Output template

```markdown
# [Client Name] - 360 Report
Generated: YYYY-MM-DD

## Quick facts
- **Stage**: [deal stage]
- **ARR**: [amount]
- **Contract**: [start] to [end]
- **Primary contact**: [name, role]
- **Health**: [green/yellow/red] - [one-line reason]

## Recent activity (last 90 days)
- LinkedIn: connection status, last DM <date>, conversation summary
- Gmail: <N> threads, last inbound <date>, last outbound <date>
- Slack: <N> mentions, channel: #<name> if any
- Granola: <N> meetings, most recent <date> with <attendees>

## Timeline (last 90 days)
- [date] - [event summary]
- ...

## Open items
- [ ] [item from email/Slack/meetings]
- ...

## Internal context
[What we've discussed internally about this client - from Slack and Notion]

## Recommended next step
[One clear action with owner and deadline]
```

## Guardrails

- **Read-only** - never modify CRM records, send emails, or post messages
- **Flag data gaps** - if a source returns nothing, say so explicitly
- **No speculation** - report what the data shows; flag inferences clearly
- **Respect PII** - the report is internal-only; still avoid unnecessary personal details
- **Ask for confirmation** if the client name is ambiguous or matches multiple records

## Self-improvement

After the CAO reviews a customer report:

1. Diff what was drafted vs what the CAO found useful vs what she cut - identify patterns
2. Update `customer-success/_insights.md` with what sections added value and which were noise
3. If the CAO consistently skips a data source or section, note it (may not be worth pulling)
4. If she adds context the report missed, add that source or check to the Data sources table
5. If a report format works well for a specific use case (e.g. pre-meeting vs renewal), save it to `customer-success/_examples/` as a reference template
