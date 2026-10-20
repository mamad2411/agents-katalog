---
name: uco-next-steps
description: Automatically draft and write next steps for all active UCOs assigned to the user (as AE or SA). Gathers context from Gmail, Google Calendar, Google Drive, Slack, and Salesforce to generate accurate, personalized next steps for UCOs in stages U1-U5. Use when the user wants to update their UCOs, prep for QBRs, or do a weekly pipeline refresh.
user-invocable: true
---

# UCO Next Steps Workflow

This skill automatically researches and drafts next steps for all of your active UCOs by pulling context from Gmail, Calendar, Drive, Slack, and Salesforce — then writes the updates directly to Salesforce after your review.

## Prerequisites

Before running, ensure the following are authenticated:
1. **Salesforce** - Run `/salesforce-authentication` if needed
2. **Google** - Run `/google-auth` if needed (for Gmail, Calendar, Drive)
3. **Slack** - MCP connection should be active (check with `/validate-mcp-access`)

## How to Invoke

Simply run `/uco-next-steps` with no arguments to process all your active UCOs.

You can optionally pass a filter:
- `/uco-next-steps acme` — only process UCOs for accounts matching "acme"
- `/uco-next-steps U3` — only process UCOs in stage U3
- `/uco-next-steps red` — only process Red health UCOs

## What This Skill Does

1. **Discovers** all UCOs assigned to you (as AE, SA, RSA, or DSA) in stages U1-U5
2. **Researches** each UCO by searching Gmail, Slack, Calendar, and Google Drive for recent activity
3. **Drafts** next steps for each UCO using the context gathered
4. **Presents** a review table showing all proposed updates
5. **Writes** confirmed updates to Salesforce after your approval

## Quick Start

**Invoke the `uco-next-steps` agent** to handle the full workflow:

```
Task tool with subagent_type='fins-canada-tools:uco-next-steps' and model='sonnet'
```

Pass the user's full request (including any filter arguments) directly to the agent. The agent will handle all data gathering, synthesis, and Salesforce updates.

## User Preferences

The skill respects your `~/.vibe/profile` settings:

```yaml
salesforce:
  next_steps_format: short   # or "verbose"
  ae_transcript_folder_id: <FOLDER_ID>   # optional: AE's Gemini recordings folder
```

- **short** (default): `Feb-26 - JD - <one-line update>`
- **verbose**: Structured multi-line format with Status, Last step, Next step, Risk

## Output

The skill presents a confirmation table before writing anything:

| Account | UCO | Stage | Health | Proposed Next Steps | Sources Used |
|---------|-----|-------|--------|---------------------|--------------|
| Acme Corp | Data Migration | U3 | Yellow | Feb-26 - RL - POC kickoff scheduled for Mar 3 | Gmail, Cal |
| ... | ... | ... | ... | ... | ... |

After your approval (`yes` / `no` / `edit <uco>`), updates are written to Salesforce.
