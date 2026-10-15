---
name: openclaw-executive-assistant-webinars
description: Build local-only executive assistant workflows with OpenClaw using file-based data intake, operational memory, and communications triage
triggers:
  - "help me set up an OpenClaw executive assistant"
  - "create a local file intake workflow with OpenClaw"
  - "build an operational memory system for daily logs"
  - "triage emails offline using OpenClaw"
  - "generate weekly summary reports from work notes"
  - "set up file-based AI assistant workflows"
  - "create markdown reports from incoming files"
  - "build a local-first executive assistant"
---

# OpenClaw Executive Assistant Webinars

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

## Overview

This project provides a workshop framework for building local-only executive assistant workflows using OpenClaw. It demonstrates three core patterns:

1. **Data intake review** — Turn unknown files into trustworthy intake reports
2. **Operational memory** — Convert work residue into daily and weekly momentum docs
3. **Offline communications triage** — Transform exported emails into action lists

All workflows use local folders, produce reviewable markdown artifacts, and require no live integrations.

## Installation

Clone the repository:

```bash
git clone https://github.com/dandenney/webinars-build-your-own-executive-assistant-with-openclaw.git
cd webinars-build-your-own-executive-assistant-with-openclaw
```

No dependencies required — this is a file-based workflow using OpenClaw prompts with copy/paste execution.

## Repository Structure

```
code-along/
├── INDEX.md
├── 01-data-intake-review/
│   ├── incoming/          # Files to inspect
│   ├── prompts/
│   │   └── intake-review.md
│   ├── outputs/           # Generated reports
│   └── expected/
│       └── report-outline.md
├── 02-operational-memory/
│   ├── inbox/             # Work notes and residue
│   ├── prompts/
│   │   ├── daily-log.md
│   │   └── weekly-hype.md
│   ├── outputs/
│   ├── schedule/
│   │   ├── cron-examples.md
│   │   └── heartbeat-note.md
├── 03-offline-communications-triage/
│   ├── eml/               # Exported email files
│   ├── prompts/
│   │   └── email-triage.md
│   ├── outputs/
│   └── expected/
│       └── report-outline.md
└── mission-control/       # Optional dashboard
```

## Workflow Patterns

### 1. Data Intake Review

Process unknown files in a folder and generate a structured intake report.

**Setup:**
```bash
cd code-along/01-data-intake-review
```

**Workflow:**
1. Place files to review in `incoming/`
2. Open `prompts/intake-review.md` to see the prompt template
3. Copy the prompt and provide context about files in `incoming/`
4. Save the generated output to `outputs/intake-review.md`

**Expected output structure:**
- File inventory
- Risk assessment
- Action recommendations
- Priority rankings

**Example prompt pattern:**
```markdown
Review all files in the incoming/ directory and create an intake report that includes:
- List of all files with size and type
- Security/privacy concerns
- Recommended actions for each file
- Overall priority assessment

Format as markdown with clear sections.
```

### 2. Operational Memory

Convert scattered work notes into structured daily logs and weekly summaries.

**Setup:**
```bash
cd code-along/02-operational-memory
```

**Daily log workflow:**
```markdown
# Daily Log Prompt Pattern
Review all notes in inbox/ from today and create a daily log with:
- Key accomplishments
- Decisions made
- Blockers encountered
- Tomorrow's priorities

Output to: outputs/daily-log.md
```

**Weekly summary workflow:**
```markdown
# Weekly Hype Prompt Pattern
Review all daily logs from this week and create a weekly summary with:
- Week's highlights
- Momentum indicators
- Patterns observed
- Next week's focus areas

Output to: outputs/weekly-hype.md
```

**Automation example (cron):**
```bash
# Daily log generation at 5pm
0 17 * * * /path/to/generate-daily-log.sh

# Weekly summary on Friday at 4pm
0 16 * * 5 /path/to/generate-weekly-hype.sh
```

### 3. Offline Communications Triage

Process exported email files (.eml) and generate action-oriented triage reports.

**Setup:**
```bash
cd code-along/03-offline-communications-triage
```

**Workflow:**
1. Export emails as .eml files to `eml/` directory
2. Use the triage prompt from `prompts/email-triage.md`
3. Generate report to `outputs/email-triage.md`

**Example triage prompt pattern:**
```markdown
Process all .eml files in eml/ and create a triage report with:

## Urgent Actions
- Emails requiring immediate response
- Deadlines within 24 hours

## This Week
- Items needing response this week
- Grouped by topic/project

## FYI / Archive
- Informational items
- No action needed

## Delegatable
- Items that could be handled by others

For each item include:
- Sender
- Subject line
- Key points
- Recommended action
```

**Expected output:**
- Categorized action items
- Priority rankings
- Response drafts for urgent items
- Delegation opportunities

## Common Patterns

### File-Based Prompt Execution

All exercises follow this pattern:

```bash
# 1. Navigate to exercise directory
cd code-along/01-data-intake-review

# 2. Review the prompt template
cat prompts/intake-review.md

# 3. Provide context files
# (Files already in incoming/ or inbox/ directories)

# 4. Copy prompt + execute with OpenClaw
# (Manual copy/paste to AI assistant)

# 5. Save output
# Save response to outputs/[exercise-name].md
```

### Markdown Output Structure

All outputs should be markdown files with:

```markdown
# Report Title

**Generated:** YYYY-MM-DD HH:MM

## Executive Summary
[2-3 sentence overview]

## [Section 1]
[Detailed content]

## [Section 2]
[Detailed content]

## Recommendations
- [ ] Action item 1
- [ ] Action item 2

## Next Steps
1. Step one
2. Step two
```

### Scheduling Automated Runs

For operational memory workflows:

```bash
# Create a simple shell script wrapper
#!/bin/bash
# generate-daily-log.sh

WORKSPACE="/path/to/code-along/02-operational-memory"
cd "$WORKSPACE"

# Your OpenClaw execution command here
# This could be an API call, CLI command, etc.
openclaw execute \
  --prompt "$(cat prompts/daily-log.md)" \
  --context "inbox/" \
  --output "outputs/daily-log-$(date +%Y-%m-%d).md"
```

## Configuration

### Environment Variables

If integrating with OpenClaw APIs:

```bash
export OPENCLAW_API_KEY=your_api_key_here
export OPENCLAW_MODEL=claude-3-5-sonnet
export WORKSPACE_ROOT=/path/to/code-along
```

### Directory Conventions

Maintain this structure for each workflow:

- `incoming/` or `inbox/` — Input files
- `prompts/` — Reusable prompt templates
- `outputs/` — Generated reports (gitignored if desired)
- `expected/` — Example outputs for reference

## Troubleshooting

**No outputs generated:**
- Verify files exist in the input directory
- Check prompt file is readable
- Ensure output directory has write permissions

**Reports missing sections:**
- Review the prompt template for completeness
- Check that all input files were accessible
- Verify markdown formatting in output

**Automation not running:**
- Test cron syntax with `crontab -l`
- Check script permissions: `chmod +x generate-*.sh`
- Verify paths are absolute in cron jobs
- Check cron logs: `grep CRON /var/log/syslog`

**File encoding issues:**
- Ensure .eml files are UTF-8 encoded
- Check for special characters in filenames
- Verify file extensions match expected types

## Best Practices

1. **Review before committing** — All outputs are markdown for human review
2. **Version control prompts** — Keep prompt templates in git
3. **Iterate on prompts** — Refine based on output quality
4. **Archive outputs** — Date-stamp reports for historical reference
5. **Local-first** — No API calls until you're ready to automate

## Workshop Usage

To follow the webinar:

```bash
# Open the walkthrough
open webinar-runbook.html

# Work through exercises in order
cd code-along/01-data-intake-review
# ... complete exercise 1

cd ../02-operational-memory
# ... complete exercise 2

cd ../03-offline-communications-triage
# ... complete exercise 3
```

Each exercise builds on patterns from the previous one, demonstrating progressively sophisticated file-based AI workflows.
