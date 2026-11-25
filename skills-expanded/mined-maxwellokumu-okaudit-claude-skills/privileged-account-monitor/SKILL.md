---
name: privileged-account-monitor
description: Review privileged account activity logs for baseline exceedances, off-hours access, sensitive actions, and new unknown users. Use this skill for admin activity review and privileged access monitoring.
---

# Privileged Account Monitor

Use this skill when the user asks about privileged accounts, admin activity, CloudTrail review, off-hours access, or sensitive privileged actions.

## Goal
Inspect privileged account activity to identify unusual behavior, baseline exceedances, off-hours access, and risky administrative actions.

## Workflow
1. Confirm whether the user is providing local logs or wants AWS-based analysis.
2. Gather the log source, baseline threshold, and business-hours window if they differ from defaults.
3. Review README.md for supported log formats and example outputs if needed.
4. Run main.py with the relevant inputs and mode.
5. Summarize the accounts, actions, and time periods that most need follow-up.

## Inputs
- logs (string, optional): Path to CSV or JSON log file for local mode.
- baseline (integer, optional): Maximum actions per day before flagging.
- hours (string, optional): Business-hours window in HH:MM-HH:MM format.
- mode (string, optional): Execution mode: local or aws.
- dry_run (boolean, optional): Use bundled sample data.

## Bundled Files
- main.py: executable logic for the skill.
- README.md: detailed usage, log expectations, and sample outputs.
- sample_input: bundled example log data.
- skill.yaml: existing repo manifest retained for this project's original packaging.

## Guidance
- Distinguish normal privileged activity from baseline deviations.
- Highlight the most sensitive actions and off-hours patterns first.
- If the log source is incomplete, state the visibility limits clearly.
