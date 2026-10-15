---
name: openclaw-executive-assistant-workflows
description: Build local-first executive assistant workflows with OpenClaw for data intake, operational memory, and communications triage
triggers:
  - "set up an OpenClaw executive assistant workflow"
  - "create a data intake review with OpenClaw"
  - "build operational memory tracking"
  - "triage emails with OpenClaw"
  - "generate daily logs and weekly summaries"
  - "set up local-first AI assistant workflows"
  - "create markdown artifacts from work residue"
  - "configure OpenClaw prompts for productivity"
---

# OpenClaw Executive Assistant Workflows

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

This skill covers building local-first executive assistant workflows using OpenClaw patterns. The project demonstrates three core workflows: data intake review, operational memory tracking, and offline communications triage. All operations use local files and produce reviewable markdown artifacts.

## What This Project Does

OpenClaw executive assistant workflows help you:

- **Data Intake Review**: Transform unknown files into trustworthy intake reports
- **Operational Memory**: Convert work residue into daily logs and weekly momentum documents
- **Offline Communications Triage**: Turn exported emails into prioritized action lists

All workflows are local-only with no live integrations, using copy/paste prompts and markdown outputs.

## Project Structure

```
code-along/
├── INDEX.md
├── 01-data-intake-review/
│   ├── incoming/           # Files to inspect
│   ├── prompts/
│   │   └── intake-review.md
│   ├── outputs/
│   │   └── intake-review.md
│   └── expected/
│       └── report-outline.md
├── 02-operational-memory/
│   ├── inbox/              # Notes and work residue
│   ├── prompts/
│   │   ├── daily-log.md
│   │   └── weekly-hype.md
│   ├── outputs/
│   │   ├── daily-log.md
│   │   └── weekly-hype.md
│   └── schedule/
│       ├── cron-examples.md
│       └── heartbeat-note.md
├── 03-offline-communications-triage/
│   ├── eml/                # Exported email files
│   ├── prompts/
│   │   └── email-triage.md
│   ├── outputs/
│   │   └── email-triage.md
│   └── expected/
│       └── report-outline.md
└── mission-control/        # Optional dashboard
```

## Workflow 1: Data Intake Review

Transform incoming files into structured reports.

### Setup

```bash
cd code-along/01-data-intake-review
```

### Usage Pattern

1. Place unknown files in `incoming/`
2. Read the prompt template in `prompts/intake-review.md`
3. Run the prompt against the incoming files
4. Generate `outputs/intake-review.md`

### Example Prompt Structure

```markdown
# Data Intake Review Prompt

Review all files in the incoming/ directory and create a structured report:

## Summary
- Total files reviewed
- File types present
- Overall assessment

## File-by-File Analysis
For each file:
- Filename
- Type
- Size
- Key contents
- Recommendation (keep/archive/delete/action)

## Action Items
List any files requiring immediate attention

## Archive Candidates
List files safe to archive
```

### Expected Output Format

```markdown
# Intake Review - [DATE]

## Summary
3 files reviewed
- 1 PDF document
- 1 CSV dataset
- 1 text note

## File Analysis

### document.pdf
- **Type**: PDF proposal
- **Size**: 2.4 MB
- **Contents**: Q2 budget proposal draft
- **Recommendation**: ACTION - Review by EOD Friday

### data.csv
- **Type**: CSV dataset
- **Size**: 145 KB
- **Contents**: Customer feedback responses
- **Recommendation**: KEEP - Reference for analysis

## Action Items
1. Review document.pdf budget proposal
2. Schedule feedback analysis meeting
```

## Workflow 2: Operational Memory

Convert daily work residue into structured logs and weekly summaries.

### Setup

```bash
cd code-along/02-operational-memory
```

### Daily Log Generation

```markdown
# Daily Log Prompt

Review all notes and work artifacts in inbox/ from today.

Generate a daily log with:

## Work Completed
- Tasks finished
- Decisions made
- Problems solved

## In Progress
- Ongoing work
- Blockers encountered

## Notes for Tomorrow
- Priorities
- Follow-ups needed

## Quick Wins
- Small achievements worth noting
```

### Weekly Summary Generation

```markdown
# Weekly Hype Prompt

Review the past week's daily logs.

Create a weekly summary:

## 🎯 Goals Achieved
What got done this week

## 📈 Progress Made
Movement on larger initiatives

## 🔥 Highlights
Wins worth celebrating

## 🚀 Next Week Focus
Top 3 priorities

## 💡 Lessons Learned
Key insights from the week
```

### Automation with Cron

Example cron configuration for daily logs:

```bash
# Daily log at 5 PM
0 17 * * * cd ~/code-along/02-operational-memory && ./generate-daily-log.sh

# Weekly summary on Friday at 4 PM
0 16 * * 5 cd ~/code-along/02-operational-memory && ./generate-weekly-hype.sh
```

### Example Script

```bash
#!/bin/bash
# generate-daily-log.sh

DATE=$(date +%Y-%m-%d)
PROMPT_FILE="prompts/daily-log.md"
OUTPUT_FILE="outputs/daily-log-${DATE}.md"

# Read prompt and process inbox
echo "Generating daily log for ${DATE}..."

# Copy prompt template
cp "$PROMPT_FILE" "$OUTPUT_FILE"

# Add date header
echo "# Daily Log - ${DATE}" >> "$OUTPUT_FILE"

# Process would happen here via AI agent
# This is a manual copy/paste workflow in the workshop
```

## Workflow 3: Offline Communications Triage

Transform exported emails into actionable reports.

### Setup

```bash
cd code-along/03-offline-communications-triage
```

### Email Export Process

Export emails to `.eml` format and place in the `eml/` directory.

### Triage Prompt Structure

```markdown
# Email Triage Prompt

Review all .eml files in the eml/ directory.

Create a triage report:

## 🚨 Urgent - Respond Today
Emails requiring immediate attention

## 📋 Action Required - This Week
Emails needing response within 3-5 days

## 📖 For Review
Informational emails worth reading

## 🗑️ Low Priority
Can be archived or handled later

For each email include:
- From
- Subject
- Date
- Brief summary
- Recommended action
- Estimated time required
```

### Expected Output

```markdown
# Email Triage Report - 2026-04-25

## 🚨 Urgent - Respond Today

### Email 1
- **From**: sarah@company.com
- **Subject**: Q2 Budget Approval Needed
- **Date**: 2026-04-25 09:15 AM
- **Summary**: Budget requires sign-off before Monday meeting
- **Action**: Review and approve budget spreadsheet
- **Time**: 30 minutes

## 📋 Action Required - This Week

### Email 2
- **From**: team@project.com
- **Subject**: Design Review Feedback
- **Date**: 2026-04-24 02:30 PM
- **Summary**: Design mockups ready for review
- **Action**: Provide feedback on 3 design options
- **Time**: 45 minutes

## 📖 For Review

### Email 3
- **From**: newsletter@industry.com
- **Subject**: Weekly Industry Update
- **Date**: 2026-04-24 08:00 AM
- **Summary**: Market trends and competitor news
- **Action**: Read when available
- **Time**: 15 minutes
```

## Mission Control Dashboard

Optional central hub for linking all artifacts.

```markdown
# Mission Control

Last updated: 2026-04-25 17:00

## 📥 Latest Intake Review
[View Report](../01-data-intake-review/outputs/intake-review.md)
- 3 files processed
- 1 action item pending

## 📝 Today's Log
[View Log](../02-operational-memory/outputs/daily-log-2026-04-25.md)
- 5 tasks completed
- 2 in progress

## 📧 Email Triage
[View Report](../03-offline-communications-triage/outputs/email-triage.md)
- 1 urgent response needed
- 3 actions this week
```

## Best Practices

### Prompt Design

- Keep prompts clear and structured
- Define expected output format explicitly
- Include examples in prompt templates
- Use consistent markdown formatting

### File Organization

```
workflow-name/
├── incoming/     # Raw inputs
├── prompts/      # Reusable prompt templates
├── outputs/      # Generated artifacts
└── expected/     # Reference outputs
```

### Artifact Naming

Use consistent naming conventions:

```
daily-log-YYYY-MM-DD.md
weekly-hype-YYYY-WW.md
intake-review-YYYY-MM-DD.md
email-triage-YYYY-MM-DD.md
```

### Workflow Execution

1. Read the prompt template
2. Customize for current context
3. Process input files
4. Generate markdown artifact
5. Review and refine output
6. Archive or act on results

## Troubleshooting

### Prompt Not Producing Expected Output

- Check that input files are in correct location
- Verify prompt includes output format specification
- Add explicit examples to prompt
- Break complex prompts into smaller steps

### Missing Context in Reports

- Include date/time stamps in prompts
- Reference previous artifacts when needed
- Add context sections to prompt templates

### Automation Issues

- Verify file paths in cron scripts
- Check script permissions: `chmod +x script.sh`
- Test scripts manually before scheduling
- Log script output for debugging

### File Format Problems

- Ensure `.eml` files are properly exported
- Check markdown syntax in outputs
- Validate file encoding (UTF-8)

## Integration with AI Coding Agents

This workflow integrates with AI agents by:

1. **Structured Prompts**: Templates that agents can execute
2. **File-Based I/O**: Clear input/output locations
3. **Markdown Artifacts**: Reviewable, versionable outputs
4. **Local-First**: No API dependencies

Agents can automate:
- Reading prompt templates
- Processing input directories
- Generating formatted outputs
- Updating mission control dashboard
