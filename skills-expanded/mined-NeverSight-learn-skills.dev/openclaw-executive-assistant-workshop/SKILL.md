---
name: openclaw-executive-assistant-workshop
description: Build local-first AI executive assistant workflows with OpenClaw for data intake, operational memory, and communications triage
triggers:
  - "help me build an executive assistant with OpenClaw"
  - "how do I use OpenClaw for email triage"
  - "show me OpenClaw operational memory patterns"
  - "create a data intake review with OpenClaw"
  - "set up local-first AI workflows"
  - "build offline communications triage"
  - "generate daily logs with OpenClaw"
  - "create weekly summary reports"
---

# OpenClaw Executive Assistant Workshop

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

This skill covers building local-first executive assistant workflows using OpenClaw. The workshop focuses on three core patterns: data intake review, operational memory (daily/weekly logs), and offline communications triage. All workflows stay local, produce markdown artifacts, and require no live integrations.

## What This Project Does

The OpenClaw executive assistant workshop teaches you to:

1. **Data Intake Review** — Turn unknown files into trustworthy intake reports
2. **Operational Memory** — Transform work residue into daily logs and weekly summaries
3. **Offline Communications Triage** — Process exported emails into actionable lists

All exercises use copy/paste prompts, local folders, and generate reviewable markdown outputs.

## Repository Structure

```text
.
├── webinar-runbook.html              # Main walkthrough guide
└── code-along/
    ├── INDEX.md
    ├── 01-data-intake-review/
    │   ├── incoming/                 # Files to inspect
    │   ├── prompts/intake-review.md  # Prompt instructions
    │   ├── outputs/                  # Generated reports
    │   └── expected/report-outline.md
    ├── 02-operational-memory/
    │   ├── inbox/                    # Work notes and residue
    │   ├── prompts/daily-log.md
    │   ├── prompts/weekly-hype.md
    │   ├── outputs/
    │   ├── schedule/cron-examples.md
    │   └── schedule/heartbeat-note.md
    ├── 03-offline-communications-triage/
    │   ├── eml/                      # Exported email files
    │   ├── prompts/email-triage.md
    │   ├── outputs/
    │   └── expected/report-outline.md
    └── mission-control/              # Optional dashboard
```

## Installation & Setup

### Clone the Repository

```bash
git clone https://github.com/dandenney/webinars-build-your-own-executive-assistant-with-openclaw.git
cd webinars-build-your-own-executive-assistant-with-openclaw
```

### Prerequisites

- OpenClaw AI assistant (Claude, ChatGPT, or similar)
- Text editor
- Web browser (for viewing `webinar-runbook.html`)

No additional dependencies required — this is a prompt-based workshop.

## Workshop Flow

### Exercise 1: Data Intake Review

Turn unknown files in `incoming/` into a structured intake report.

**Location:** `code-along/01-data-intake-review/`

**Steps:**

1. Review files in `incoming/` folder
2. Copy prompt from `prompts/intake-review.md`
3. Provide prompt and folder contents to your AI assistant
4. Save output to `outputs/intake-review.md`

**Expected Output Structure:**

```markdown
# Data Intake Review

## Summary
Brief overview of files received

## Files Analyzed
- filename1.ext — description and recommendation
- filename2.ext — description and recommendation

## Priority Actions
1. Action item based on file contents
2. Follow-up needed

## Next Steps
Recommendations for processing
```

**Example Prompt Pattern:**

```markdown
Review the following files in my incoming folder and create an intake report:

[List files and relevant contents]

For each file:
- Identify type and purpose
- Extract key information
- Note any actions needed
- Flag urgency or importance

Output a markdown report with summary, file details, and action items.
```

### Exercise 2: Operational Memory

Transform daily work notes into momentum documents.

**Location:** `code-along/02-operational-memory/`

#### Daily Log

**Steps:**

1. Place work residue (notes, snippets, thoughts) in `inbox/`
2. Copy prompt from `prompts/daily-log.md`
3. Generate daily log
4. Save to `outputs/daily-log.md`

**Expected Output:**

```markdown
# Daily Log — YYYY-MM-DD

## Completed Today
- Task or achievement
- Progress made on project X

## In Progress
- Item being worked on
- Blocked on Y

## Insights & Notes
- Learning or observation
- Idea to explore

## Tomorrow's Focus
- Priority 1
- Priority 2
```

#### Weekly Hype Summary

**Steps:**

1. Collect daily logs from the week
2. Copy prompt from `prompts/weekly-hype.md`
3. Generate weekly summary
4. Save to `outputs/weekly-hype.md`

**Expected Output:**

```markdown
# Weekly Hype — Week of YYYY-MM-DD

## Wins This Week
- Major accomplishment
- Milestone reached

## Key Themes
Pattern or focus area that emerged

## Momentum Builders
What's giving energy and progress

## Carry Forward
What needs attention next week
```

#### Automation with Cron

Reference: `schedule/cron-examples.md`

**Daily log generation:**

```bash
# Run every weekday at 5 PM
0 17 * * 1-5 /path/to/generate-daily-log.sh
```

**Weekly summary:**

```bash
# Run every Friday at 6 PM
0 18 * * 5 /path/to/generate-weekly-hype.sh
```

**Example script pattern:**

```bash
#!/bin/bash
# generate-daily-log.sh

INBOX_DIR="$HOME/code-along/02-operational-memory/inbox"
OUTPUT_DIR="$HOME/code-along/02-operational-memory/outputs"
PROMPT_FILE="$HOME/code-along/02-operational-memory/prompts/daily-log.md"

DATE=$(date +%Y-%m-%d)
OUTPUT_FILE="$OUTPUT_DIR/daily-log-$DATE.md"

# Collect inbox contents
CONTEXT=$(cat "$INBOX_DIR"/*.txt 2>/dev/null)

# Call AI assistant via API or CLI
# (Replace with your OpenClaw integration method)
echo "Generating daily log for $DATE..."

# Example: pipe prompt + context to AI CLI tool
cat "$PROMPT_FILE" | your-ai-cli --context "$CONTEXT" > "$OUTPUT_FILE"

echo "Daily log saved to $OUTPUT_FILE"
```

### Exercise 3: Offline Communications Triage

Process exported emails into actionable triage reports.

**Location:** `code-along/03-offline-communications-triage/`

**Steps:**

1. Export emails as `.eml` files to `eml/` folder
2. Copy prompt from `prompts/email-triage.md`
3. Provide email contents to AI assistant
4. Save triage report to `outputs/email-triage.md`

**Expected Output:**

```markdown
# Email Triage Report

## Urgent Actions Required
- From: sender@example.com | Subject: Critical issue
  Action: Respond by EOD
  
## Follow-up Needed
- From: colleague@company.com | Subject: Project update
  Action: Schedule call this week

## FYI / Low Priority
- From: newsletter@service.com | Subject: Weekly digest
  Action: Read when time permits

## Can Archive
- From: automated@system.com | Subject: Confirmation
  Action: None, archive

## Summary Stats
- Total emails: 15
- Urgent: 2
- Follow-up: 5
- FYI: 6
- Archive: 2
```

**Example Triage Prompt:**

```markdown
Analyze the following exported emails and create a triage report:

[Email contents from .eml files]

For each email:
- Extract sender, subject, key points
- Determine priority level
- Suggest action needed
- Estimate response timeframe

Group by urgency: Urgent Actions, Follow-up Needed, FYI, Can Archive.
Include summary statistics.
```

## Key Patterns

### Local-First Workflow

```bash
# Directory structure for each exercise
exercise/
├── incoming/     # Input files
├── prompts/      # AI instructions
├── outputs/      # Generated markdown
└── expected/     # Reference examples
```

### Prompt Engineering Pattern

All prompts follow this structure:

1. **Context:** What you're working with
2. **Task:** What to analyze or generate
3. **Output format:** Specific markdown structure
4. **Quality criteria:** What makes a good result

### Markdown Artifact Generation

All outputs are markdown files for:
- Version control tracking
- Easy diff viewing
- Plain text searchability
- No vendor lock-in

## Configuration

### Custom Prompt Templates

Edit prompt files in each exercise's `prompts/` folder:

```markdown
# prompts/custom-intake.md

Review these files with focus on [YOUR_CRITERIA]:

[FILE_CONTENTS]

Generate a report with:
1. [YOUR_SECTION_1]
2. [YOUR_SECTION_2]
3. [YOUR_SECTION_3]
```

### Output Customization

Modify expected output structure by updating `expected/` reference files.

## Common Issues & Troubleshooting

### Issue: Prompt Not Generating Expected Output

**Solution:** Check that you're including:
- Full context from input files
- Clear output format specification
- Examples from `expected/` folder

### Issue: Daily Log Missing Important Items

**Solution:** Ensure all work residue is in `inbox/` before generation. Create a checklist:

```markdown
## Pre-Log Checklist
- [ ] Notes from meetings
- [ ] Code commit messages
- [ ] Slack/email snippets
- [ ] TODO items completed
- [ ] Ideas or blockers
```

### Issue: Email Triage Misclassifying Priority

**Solution:** Enhance prompt with specific criteria:

```markdown
Priority levels:
- URGENT: deadline < 24hrs, blocks others, executive request
- FOLLOW-UP: deadline < 1 week, requires response
- FYI: informational, no response needed
- ARCHIVE: confirmation, automated, already resolved
```

### Issue: Weekly Summary Too Generic

**Solution:** Include more context signals in prompt:

```markdown
For each day's log, identify:
- Completed items (look for "done", "shipped", "merged")
- Momentum patterns (recurring themes, growing projects)
- Energy indicators (excited, blocked, breakthrough)
- Connections (how items relate across days)
```

## Best Practices

1. **Review Before Saving:** Always review AI-generated outputs before committing
2. **Iterate Prompts:** Refine prompts based on output quality
3. **Version Control:** Git-track all prompts and outputs for improvement tracking
4. **Schedule Consistency:** Run daily logs at same time each day
5. **Folder Hygiene:** Clear `inbox/` after processing, archive old outputs

## Integration Tips

### Git Workflow

```bash
# Track generated artifacts
git add code-along/*/outputs/*.md

# Commit with context
git commit -m "Daily log 2026-05-11: shipped feature X, blocked on Y"

# Review changes over time
git log --oneline -- code-along/02-operational-memory/outputs/
```

### Dashboard Setup

Create a simple `mission-control/index.html`:

```html
<!DOCTYPE html>
<html>
<head>
  <title>Executive Assistant Dashboard</title>
</head>
<body>
  <h1>Mission Control</h1>
  
  <section>
    <h2>Latest Reports</h2>
    <ul>
      <li><a href="../01-data-intake-review/outputs/intake-review.md">Latest Intake Review</a></li>
      <li><a href="../02-operational-memory/outputs/daily-log.md">Today's Log</a></li>
      <li><a href="../02-operational-memory/outputs/weekly-hype.md">This Week's Hype</a></li>
      <li><a href="../03-offline-communications-triage/outputs/email-triage.md">Email Triage</a></li>
    </ul>
  </section>
</body>
</html>
```

## Additional Resources

- **Main Walkthrough:** Open `webinar-runbook.html` in browser
- **Exercise Index:** `code-along/INDEX.md`
- **DataCamp Webinar:** https://www.datacamp.com/webinars/build-your-own-executive-assistant-with-openclaw

---

This skill enables AI coding agents to guide developers through building practical, local-first executive assistant workflows using OpenClaw patterns.
