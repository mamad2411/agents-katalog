---
name: exec-summary-writer
description: Convert a structured findings JSON file into a polished executive summary with risk breakdown, key findings, and recommendations. Use this skill for leadership-facing audit reporting.
---

# Exec Summary Writer

Use this skill when the user asks for an executive summary, audit report, findings summary, risk summary, or audit summary.

## Goal
Turn structured findings into a concise executive-ready audit summary with risks, key findings, and recommendations.

## Workflow
1. Confirm the findings JSON is available and structured.
2. Collect optional report metadata such as scope, author, and date.
3. Review README.md if you need the expected findings format or report style.
4. Run main.py with the findings file and any optional metadata.
5. Return the executive summary and highlight the highest-risk items first.

## Inputs
- findings (string, required): Path to JSON containing audit findings.
- scope (string, optional): Scope description to include in the report header.
- author (string, optional): Report author name.
- date (string, optional): Report date in YYYY-MM-DD format.

## Bundled Files
- main.py: executable logic for the skill.
- README.md: detailed usage, input expectations, and example summary output.
- skill.yaml: existing repo manifest retained for this project's original packaging.

## Guidance
- Keep leadership-facing outputs concise and risk-prioritized.
- Preserve the source findings faithfully instead of inventing conclusions.
- If required findings fields are missing, state the issue before proceeding.
