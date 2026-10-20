---
name: weekly-reflect
description: Synthesize weekly activity data from multiple sources into a formatted PERF doc summary. Triggers on weekly recap formatting, activity synthesis, or PERF doc entries.
---

# Recap synthesizer

Combine raw activity data from Slack, Calendar, JIRA, and Git into a formatted weekly summary matching the PERF Google Doc style. Focus on impactful activities, not exhaustive logging.

## Input

You receive:
1. **User highlights** (optional): What the user said stood out this week. These are the most important signal - use them to guide prioritization and add context.
2. **Raw outputs from up to 4 data collection agents**:
   - Slack: messages sent, threads participated in, key discussions
   - Calendar: meetings attended with attendees and topics
   - JIRA: ES tickets worked on, comments, status changes
   - Git: commits across local repos

Some sources may be missing if their MCP server wasn't connected. Work with whatever data is available.

## Synthesis process

### 0. Start with user highlights

If the user provided highlights, these drive the recap:
- User-mentioned activities should appear first and get the most detail
- Use highlights to add context that raw data can't capture (e.g. outcomes, significance)
- Data from agents fills in the gaps and adds supporting entries

### 1. Deduplicate

The same activity often appears in multiple sources. Merge these:
- A customer meeting shows up in Calendar AND Slack (discussion about it) - combine into one entry
- A JIRA ticket shows up in JIRA AND Slack (discussion in thread) - combine, prefer JIRA details
- A tool/plugin shows up in Git AND Slack - combine into one entry

### 2. Filter out noise

Aggressively skip low-value entries:
- **Skip routine weekly cadences**: standups, weekly syncs, 1:1s, team meetings that happen every week
- **Skip calendar events that are just recurring meetings** with no notable outcome
- **Skip trivial Slack messages**: reactions, short replies, routine channel chatter
- **Only include internal meetings if something noteworthy happened** (decision made, new initiative, enablement worth mentioning)
- Calendar data is useful for identifying customer meetings and their attendees, not for listing every meeting attended

### 3. Categorize

Group entries by these categories (in order):
- **Customer meetings**: External meetings with customers or partners (only those with substance)
- **Customer work**: POCs, demos, deliverables for specific accounts
- **ES tickets**: Escalation engineer tickets worked on
- **Internal**: Only noteworthy enablement sessions, decisions, or initiatives
- **Tools/Development**: Plugins, scripts, tools built or updated
- **Slack discussions**: Notable threads or conversations worth capturing

### 4. Prioritize

Within each category, order by importance:
- Customer-facing work with outcomes first
- Tickets with resolution or significant progress
- Work that demonstrates impact or moves things forward
- Skip anything that doesn't pass the "would someone care about this in a performance review?" test

## Output format

Use this exact format, matching the existing Google Doc style:

```
WE [MM/DD]
  - [Account] Meeting with [person/role] re: [topic] - [outcome/next steps]
  - [Account] Delivered/built/demoed [thing] - [result]
  - [ES-XXXXX] [Brief description] for [Account] - [status/resolution]
  - [Internal] [Session/meeting name] - [key takeaway]
  - [Tools] Built/updated [thing] - [what it does]
  - [Slack] Key discussion in #[channel] about [topic]
```

### Style rules

- Use telegraphic style: no articles ("a", "the"), short phrases
- Include account names in brackets where applicable
- Include ES ticket numbers where applicable
- Use spaced hyphens ` - ` to separate topic from outcome
- Keep each bullet to one line (wrap at ~120 chars if needed)
- No sub-bullets - keep it flat
- Aim for 5-15 bullets total - quality over quantity

### Example output

```
WE 01/31
  - [Acme Corp] Meeting with Jane (DE lead) re: Unity Catalog migration - agreed on 3-phase rollout starting Feb
  - [Acme Corp] Delivered POC notebook for Delta Live Tables pipeline - customer testing next week
  - [ES-14523] Resolved cluster auto-scaling issue for BigCo - was IAM role misconfiguration
  - [ES-14531] Investigated query performance regression for MegaCorp - escalated to Photon team
  - [Internal] Enablement session on new SDK features - 15 attendees
  - [Tools] Built weekly-recap plugin for Claude Code - automates PERF doc entries
  - [Slack] Discussion in #field-engineering about new customer onboarding process
```

## Missing data

If a source was unavailable, append at the bottom:

```
---
Note: Could not reach [source]. Connect [MCP server/tool] to include this data.
```

List each missing source on its own line.
