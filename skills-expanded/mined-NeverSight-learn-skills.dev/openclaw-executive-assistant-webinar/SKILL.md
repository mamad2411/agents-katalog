---
name: openclaw-executive-assistant-webinar
description: Build local-first AI executive assistant workflows with OpenClaw for data intake, operational memory, and communications triage
triggers:
  - build an executive assistant with openclaw
  - set up openclaw local workflows
  - create data intake review system
  - generate operational memory logs
  - triage emails with openclaw
  - implement openclaw executive assistant
  - use openclaw for communications management
  - create markdown artifacts with openclaw
---

# OpenClaw Executive Assistant Webinar

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

## Overview

This project provides starter files and a structured workshop for building a local-first AI executive assistant using OpenClaw. It demonstrates three core workflows:

1. **Data intake review** – Turn unknown files into trustworthy intake reports
2. **Operational memory** – Transform work residue into daily logs and weekly summaries
3. **Offline communications triage** – Convert exported emails into actionable lists

All workflows are local-only, produce reviewable markdown artifacts, and use copy/paste prompts with no live integrations.

## Repository Structure

```
.
├── webinar-runbook.html              # Main workshop walkthrough
└── code-along/
    ├── INDEX.md
    ├── 01-data-intake-review/
    │   ├── incoming/                  # Files to inspect
    │   ├── prompts/intake-review.md   # Report generation instructions
    │   ├── outputs/                   # Generated reports
    │   └── expected/report-outline.md
    ├── 02-operational-memory/
    │   ├── inbox/                     # Work notes and residue
    │   ├── prompts/daily-log.md       # Daily log prompt
    │   ├── prompts/weekly-hype.md     # Weekly summary prompt
    │   ├── outputs/                   # Generated logs
    │   └── schedule/                  # Cron examples
    ├── 03-offline-communications-triage/
    │   ├── eml/                       # Exported email files
    │   ├── prompts/email-triage.md    # Triage instructions
    │   ├── outputs/                   # Triage reports
    │   └── expected/report-outline.md
    └── mission-control/               # Optional dashboard
```

## Getting Started

### Installation

```bash
git clone https://github.com/dandenney/webinars-build-your-own-executive-assistant-with-openclaw.git
cd webinars-build-your-own-executive-assistant-with-openclaw
```

### Workshop Flow

1. Open `webinar-runbook.html` in a browser
2. Keep the `code-along/` folder visible in your editor
3. Work through exercises sequentially
4. Copy prompts from `prompts/` directories
5. Review generated artifacts in `outputs/` directories

## Exercise 1: Data Intake Review

**Goal:** Transform unknown incoming files into a structured intake report.

### File Structure

```
01-data-intake-review/
├── incoming/           # Place files to review here
├── prompts/
│   └── intake-review.md
├── outputs/
│   └── intake-review.md  # Generated report
└── expected/
    └── report-outline.md
```

### Usage Pattern

1. Place files to review in `incoming/`
2. Read the prompt from `prompts/intake-review.md`
3. Provide the prompt and file context to your AI assistant
4. Generate `outputs/intake-review.md`

### Expected Output Format

The intake review should produce a markdown report containing:

- **File inventory** – List of all files with types and sizes
- **Content summary** – Brief description of each file's purpose
- **Risk assessment** – Security/privacy concerns
- **Recommended actions** – Next steps for each file
- **Priority ranking** – Ordered by urgency/importance

## Exercise 2: Operational Memory

**Goal:** Create daily logs and weekly summaries from work residue.

### File Structure

```
02-operational-memory/
├── inbox/              # Work notes, snippets, residue
├── prompts/
│   ├── daily-log.md
│   └── weekly-hype.md
├── outputs/
│   ├── daily-log.md
│   └── weekly-hype.md
└── schedule/
    ├── cron-examples.md
    └── heartbeat-note.md
```

### Daily Log Pattern

1. Collect work residue in `inbox/`
2. Use `prompts/daily-log.md` to generate a daily log
3. Output to `outputs/daily-log.md`

**Daily log structure:**
- Date header
- Completed tasks
- In-progress work
- Blockers/questions
- Tomorrow's focus

### Weekly Summary Pattern

1. Accumulate daily logs over the week
2. Use `prompts/weekly-hype.md` to generate a weekly summary
3. Output to `outputs/weekly-hype.md`

**Weekly summary structure:**
- Week range header
- Key accomplishments
- Metrics/progress
- Challenges addressed
- Next week priorities

### Automation with Cron

Reference `schedule/cron-examples.md` for automation patterns:

```bash
# Daily log generation (5 PM weekdays)
0 17 * * 1-5 /path/to/generate-daily-log.sh

# Weekly summary (Friday 5 PM)
0 17 * * 5 /path/to/generate-weekly-summary.sh
```

## Exercise 3: Offline Communications Triage

**Goal:** Convert exported email files into an actionable triage report.

### File Structure

```
03-offline-communications-triage/
├── eml/                    # Exported .eml files
├── prompts/
│   └── email-triage.md
├── outputs/
│   └── email-triage.md     # Generated triage
└── expected/
    └── report-outline.md
```

### Usage Pattern

1. Export emails as `.eml` files into `eml/`
2. Use `prompts/email-triage.md` with your AI assistant
3. Generate `outputs/email-triage.md`

### Expected Triage Format

The email triage report should contain:

- **Urgent actions** – Emails requiring immediate response
- **This week** – Items to address within 5 business days
- **Backlog** – Lower-priority or FYI items
- **Archive candidates** – No action needed
- **Summary counts** – Total emails by category

Each email entry should include:
- Sender
- Subject
- Date received
- Recommended action
- Priority level

## Key Principles

### Local-First Architecture

All data stays on your machine:
- No cloud uploads
- No API calls to external services
- Reviewable markdown outputs
- Version-controllable artifacts

### Copy/Paste Workflow

1. Navigate to exercise directory
2. Copy prompt from `prompts/*.md`
3. Paste into AI assistant (Claude, ChatGPT, etc.)
4. Provide file context as needed
5. Review and save output to `outputs/`

### Markdown Artifacts

All outputs are markdown for:
- Easy version control with Git
- Plain-text searchability
- Cross-platform compatibility
- Human readability

## Common Patterns

### Adding Custom Prompts

Create new prompt files following the structure:

```markdown
# [Task Name]

## Context
[What you're working with]

## Goal
[What you want to produce]

## Instructions
[Step-by-step guidance]

## Output Format
[Expected structure]
```

### Chaining Workflows

Combine exercises for compound workflows:

```bash
# 1. Review incoming files
# outputs/intake-review.md

# 2. Log the review work
# outputs/daily-log.md (includes intake work)

# 3. Triage any emails found
# outputs/email-triage.md
```

### Customizing Output Formats

Edit prompt files to adjust output structure:
- Change heading levels
- Add custom sections
- Modify priority categories
- Include additional metadata

## Troubleshooting

### Missing Expected Output

**Issue:** AI generates different format than expected

**Solution:** Reference `expected/*.md` files to see the target structure, then refine your prompt with specific format requirements.

### File Context Too Large

**Issue:** Too many files to process at once

**Solution:** 
- Break into batches
- Process high-priority files first
- Create summary reports for large sets

### Inconsistent Daily Logs

**Issue:** Daily logs vary in format day-to-day

**Solution:**
- Keep prompt files consistent
- Use the same AI model
- Reference previous logs as examples
- Create a template in the prompt

### Cron Jobs Not Running

**Issue:** Automated generation fails

**Solution:**
- Check cron syntax with `crontab -l`
- Verify script paths are absolute
- Ensure scripts have execute permissions: `chmod +x script.sh`
- Check logs in `/var/log/cron` or system journal

## Best Practices

1. **Review all AI output** – Never blindly accept generated reports
2. **Version control artifacts** – Commit outputs to track changes over time
3. **Iterate on prompts** – Refine instructions based on output quality
4. **Keep raw inputs** – Preserve original files alongside processed outputs
5. **Regular cleanup** – Archive old outputs to maintain focus

## Integration Ideas

While this workshop is local-only, you can extend it with:

- File watching scripts to auto-trigger processing
- Static site generation from markdown outputs
- Notification systems when new reports are ready
- Dashboard aggregation in `mission-control/`
- Integration with note-taking tools (Obsidian, Logseq)

## Related Resources

- DataCamp webinar: https://www.datacamp.com/webinars/build-your-own-executive-assistant-with-openclaw
- OpenClaw documentation (check project homepage)
- Markdown syntax reference: https://www.markdownguide.org/
