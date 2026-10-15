---
name: openclaw-executive-assistant-local
description: Build local-first AI executive assistant workflows with OpenClaw for data intake, operational memory, and communications triage
triggers:
  - how do I set up a local executive assistant with OpenClaw
  - create an intake review workflow for unknown files
  - build operational memory with daily and weekly logs
  - triage emails offline using OpenClaw
  - set up local-only AI assistant workflows
  - create markdown artifacts from work residue
  - build a communications triage system
  - use OpenClaw for executive assistant tasks
---

# OpenClaw Executive Assistant (Local)

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

## Overview

This project provides a local-first OpenClaw workflow system for building AI-powered executive assistant capabilities. It focuses on three core operations:

1. **Data intake review** - Transform unknown files into structured intake reports
2. **Operational memory** - Convert work residue into daily logs and weekly summaries
3. **Offline communications triage** - Process exported emails into action lists

All operations use local files only, produce reviewable markdown artifacts, and require no live integrations.

## Repository Structure

```
code-along/
├── INDEX.md
├── 01-data-intake-review/
│   ├── incoming/          # Files to inspect
│   ├── prompts/           # Prompt templates
│   ├── outputs/           # Generated reports
│   └── expected/          # Reference outputs
├── 02-operational-memory/
│   ├── inbox/             # Notes and work residue
│   ├── prompts/           # Daily/weekly prompts
│   ├── outputs/           # Generated logs
│   └── schedule/          # Cron examples
├── 03-offline-communications-triage/
│   ├── eml/               # Exported email files
│   ├── prompts/           # Triage prompts
│   ├── outputs/           # Triage reports
│   └── expected/          # Reference outputs
└── mission-control/       # Dashboard (optional)
```

## Exercise 1: Data Intake Review

### Purpose
Transform unknown files in an `incoming/` folder into a trustworthy intake report.

### Workflow

1. **Place files to review:**
```bash
# Add files to the incoming folder
cp ~/Downloads/unknown-file.pdf code-along/01-data-intake-review/incoming/
```

2. **Use the intake review prompt:**

The prompt template is in `prompts/intake-review.md`. Pass it to your AI assistant along with the contents of `incoming/`:

```markdown
# Intake Review Prompt

You are an executive assistant performing a data intake review.

Review all files in the incoming/ folder and produce a report that includes:

1. File inventory (name, type, size, date)
2. Content summary for each file
3. Suggested categorization
4. Action items or next steps
5. Priority flags (urgent, routine, archive)

Output format: Markdown
Output location: outputs/intake-review.md
```

3. **Expected output structure:**

```markdown
# Data Intake Review
*Generated: YYYY-MM-DD*

## Summary
- Total files: X
- Urgent items: Y
- Requires action: Z

## File Inventory

### [filename.ext]
- **Type:** Document/Image/Data
- **Size:** XXX KB
- **Date:** YYYY-MM-DD
- **Summary:** Brief content description
- **Category:** Work/Personal/Archive
- **Action:** Review/File/Respond
- **Priority:** High/Medium/Low

[Repeat for each file]

## Recommended Actions
1. ...
2. ...
```

## Exercise 2: Operational Memory

### Purpose
Convert daily work residue into structured logs and weekly summaries.

### Daily Log Workflow

1. **Add work residue to inbox:**
```bash
# Add notes, snippets, or quick captures
echo "Met with design team - new mockups ready" > code-along/02-operational-memory/inbox/note-$(date +%Y%m%d).txt
```

2. **Use the daily log prompt** (`prompts/daily-log.md`):

```markdown
# Daily Log Prompt

You are an executive assistant creating a daily work log.

Review all items in the inbox/ folder from today and produce:

1. **Date header**
2. **Wins** - Completed items
3. **Progress** - Items in motion
4. **Blockers** - Issues or delays
5. **Tomorrow** - Planned next actions
6. **Notes** - Observations or reminders

Output format: Markdown
Output location: outputs/daily-log.md
Filename pattern: daily-YYYY-MM-DD.md
```

3. **Expected daily log output:**

```markdown
# Daily Log: 2026-05-11

## Wins
- ✅ Completed data intake review system
- ✅ Shipped v2.1 of client dashboard

## Progress
- 🔄 OpenClaw workshop prep (80% complete)
- 🔄 Q2 planning document (draft stage)

## Blockers
- ⚠️ Waiting on legal review for contract
- ⚠️ Need API keys from DevOps

## Tomorrow
- [ ] Finalize workshop slides
- [ ] Review Q2 budget proposal
- [ ] Team sync at 2pm

## Notes
- Design team shared new mockups in Figma
- Consider async standup format for remote team
```

### Weekly Summary Workflow

**Use the weekly hype prompt** (`prompts/weekly-hype.md`):

```markdown
# Weekly Hype Prompt

You are an executive assistant creating a weekly summary.

Review all daily logs from this week (outputs/daily-*.md) and produce:

1. **Week of [date range]**
2. **Highlights** - Major wins and milestones
3. **Momentum** - Projects advancing
4. **Attention needed** - Recurring blockers
5. **Next week focus** - Priorities for the week ahead
6. **Metrics** (optional) - Quantifiable progress

Output format: Markdown
Output location: outputs/weekly-hype.md
Filename pattern: weekly-YYYY-Www.md
```

### Automation Example

Schedule daily log generation with cron (see `schedule/cron-examples.md`):

```bash
# Run daily at 6pm
0 18 * * * cd ~/openclaw-assistant && ./generate-daily-log.sh

# generate-daily-log.sh example:
#!/bin/bash
DATE=$(date +%Y-%m-%d)
AI_PROMPT=$(cat code-along/02-operational-memory/prompts/daily-log.md)
# Pass inbox contents and prompt to your AI CLI tool
# ai-cli "$AI_PROMPT" --context "code-along/02-operational-memory/inbox/*" \
#   > "code-along/02-operational-memory/outputs/daily-$DATE.md"
```

## Exercise 3: Offline Communications Triage

### Purpose
Process exported email files into structured action lists.

### Workflow

1. **Export emails to .eml format:**
```bash
# Place exported emails in the eml/ folder
cp ~/exported-emails/*.eml code-along/03-offline-communications-triage/eml/
```

2. **Use the email triage prompt** (`prompts/email-triage.md`):

```markdown
# Email Triage Prompt

You are an executive assistant performing email triage.

Review all .eml files in the eml/ folder and produce:

1. **Urgent** - Requires immediate response
2. **Action Required** - Needs response (24-48h)
3. **FYI** - Informational, no action needed
4. **Delegate** - Should be handled by someone else
5. **Archive** - Safe to file away

For each email include:
- From/Subject
- Brief summary
- Suggested response or action
- Priority level

Output format: Markdown
Output location: outputs/email-triage.md
```

3. **Expected triage output:**

```markdown
# Email Triage Report
*Generated: YYYY-MM-DD HH:MM*

## Urgent (Response Today)

### From: client@example.com | Re: Production Issue
- **Summary:** Database timeout errors affecting users
- **Action:** Coordinate with DevOps for immediate fix
- **Priority:** 🔴 Critical

## Action Required (24-48h)

### From: legal@company.com | Re: Contract Review
- **Summary:** Q2 vendor contract needs signature
- **Action:** Review terms, sign if acceptable
- **Priority:** 🟡 High

## FYI (No Action)

### From: team@company.com | Re: Weekly Newsletter
- **Summary:** Company updates and team wins
- **Action:** None - informational
- **Priority:** 🟢 Low

## Delegate

### From: recruiter@agency.com | Re: Candidate Pipeline
- **Summary:** Three candidates ready for interviews
- **Action:** Forward to hiring manager Sarah
- **Priority:** 🟡 Medium

## Archive

[Emails that can be filed with no action]
```

## Common Patterns

### Pattern 1: Copy-Paste Workflow
```markdown
1. Open AI assistant (Claude, ChatGPT, etc.)
2. Copy prompt from prompts/*.md
3. Attach or paste relevant files from incoming/inbox/eml/
4. Run generation
5. Save output to outputs/*.md
6. Review and edit as needed
```

### Pattern 2: Scripted Automation
```bash
#!/bin/bash
# automated-intake.sh

PROMPT=$(cat code-along/01-data-intake-review/prompts/intake-review.md)
FILES=$(ls code-along/01-data-intake-review/incoming/*)

# Use your AI CLI tool of choice
# ai-cli "$PROMPT" --files "$FILES" > outputs/intake-review-$(date +%Y%m%d).md
```

### Pattern 3: Scheduled Heartbeat
```bash
# Add to crontab
# Daily log at 6pm weekdays
0 18 * * 1-5 cd ~/openclaw-assistant && ./daily-log.sh

# Weekly summary Friday at 5pm
0 17 * * 5 cd ~/openclaw-assistant && ./weekly-summary.sh
```

## Configuration

### Environment Setup

Create a `.env` file for AI API configuration:

```bash
# .env
ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
OPENAI_API_KEY=${OPENAI_API_KEY}
AI_MODEL=claude-3-5-sonnet-20241022
```

### Prompt Customization

Edit prompt files to match your workflow:

```bash
# Customize intake review categories
nano code-along/01-data-intake-review/prompts/intake-review.md

# Adjust daily log sections
nano code-along/02-operational-memory/prompts/daily-log.md

# Modify email triage buckets
nano code-along/03-offline-communications-triage/prompts/email-triage.md
```

## Troubleshooting

### Issue: AI output not matching expected format

**Solution:** Add explicit format instructions to prompts:

```markdown
CRITICAL: Output must be valid Markdown with exactly these sections:
- Summary
- File Inventory
- Recommended Actions

Use ## for section headers. Use - for bullet lists.
```

### Issue: Large files causing context limits

**Solution:** Process in batches:

```bash
# Split incoming files into chunks
for file in incoming/*.pdf; do
  # Process individually
  echo "Processing $file..."
done
```

### Issue: Automation script not running

**Solution:** Check cron logs and permissions:

```bash
# View cron logs
grep CRON /var/log/syslog

# Ensure scripts are executable
chmod +x *.sh

# Test script manually
./daily-log.sh
```

### Issue: Email .eml parsing errors

**Solution:** Ensure proper export format from email client. Most clients support "Save as .eml" or "Export to file" options. If parsing fails, extract plain text first:

```bash
# Extract text from .eml
grep -A 1000 "^$" email.eml | tail -n +2 > email.txt
```

## Integration Tips

### With Obsidian/Notion
```bash
# Symlink outputs to your notes folder
ln -s ~/openclaw-assistant/code-along/02-operational-memory/outputs ~/Obsidian/Daily-Logs
```

### With Git for Versioning
```bash
# Track generated logs
cd code-along/02-operational-memory/outputs
git init
git add daily-*.md weekly-*.md
git commit -m "Daily log archive"
```

### With Markdown Viewers
```bash
# Serve outputs as local site
cd code-along
python -m http.server 8000
# Open http://localhost:8000
```

## Best Practices

1. **Review before archiving** - Always human-review AI outputs before filing
2. **Consistent naming** - Use ISO date formats (YYYY-MM-DD) in filenames
3. **Regular cleanup** - Archive old logs monthly to keep folders manageable
4. **Prompt iteration** - Refine prompts based on output quality over time
5. **Local-first** - Keep sensitive data local; only upload sanitized examples
