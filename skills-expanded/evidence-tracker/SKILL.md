---
name: evidence-tracker
description: Manage audit evidence requests, collection progress, and status reporting so Claude can keep audits organized and identify overdue or blocked evidence items.
---

# Evidence Tracker

Use this skill when the user needs help organizing audit evidence requests, tracking collection status, or summarizing what evidence is still missing.

## Goal

Help Claude maintain a reliable picture of audit evidence progress, highlight blockers, and produce clear status summaries for audit coordination.

## Workflow

1. Review the audit program or evidence list the user wants to track.
2. Identify whether the task is to initialize, update, list, filter, or export evidence status.
3. Normalize the current status of each evidence item and note missing owners, dates, or dependencies.
4. Highlight overdue, blocked, or incomplete evidence that may put the audit timeline at risk.
5. Return an actionable status summary that supports follow-up with stakeholders.

## Inputs

Expected inputs from the bundled tool metadata:
- program: Path to an audit program or evidence definition file.
- init: Initialize a new tracker.
- update: Update the status of an evidence item.
- list: Display tracked evidence items.
- export: Produce a final evidence summary.

## Bundled Files

- main.py contains the executable tracking workflow.
- README.md provides usage guidance and examples.
- skill.yaml captures the repo-native metadata for this skill.
- sample_input may contain example audit programs or tracker data.

## Guidance

Keep outputs structured and audit-friendly. Be explicit about what is collected, what is outstanding, and what follow-up actions are needed to keep the audit moving.
