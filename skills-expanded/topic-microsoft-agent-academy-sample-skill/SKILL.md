---
name: outlook-pre-onboarding-checklist-meeting
description: >-
  Create a 1-hour Outlook follow-up meeting for pre-onboarding after a successful
  Docusign workflow trigger, using the employee name and agreement effective date
  from workflow context.
license: MIT
metadata:
  author: elaiza-benitez
  version: 1.0.0
---

# Outlook Pre-Onboarding Checklist Meeting

Use this skill after the Docusign workflow trigger succeeds and workflow context includes
`Employee Full Name` and agreement `Effective Date`.

## Instructions

- After confirming the workflow was triggered successfully, automatically create a 1-hour Outlook meeting in the user's calendar without asking for any additional input by invoking the `Work IQ Calendar (Preview)` tool.
- Schedule the meeting exactly 2 workdays before the agreement `Effective Date`.
- Ensure the computed meeting date does not fall on Saturday or Sunday. Do not use modular arithmetic.
- Use the user's work hours for the meeting start time.
- Hardcode the time zone to `(UTC+12:00) Auckland, Wellington`.
- Set the meeting subject to: `Review pre-onboarding checklist for [Employee Full Name]`, where `[Employee Full Name]` is taken from the Docusign workflow context.
- Send a response confirming that the meeting has been created.
- If meeting creation fails, report the failure and include the error details.

## Rules

- Do not ask the user for any additional meeting details.
- Always use the `Employee Full Name` from workflow context.
- Always use the agreement `Effective Date` from workflow context.
- The meeting must be created only after a successful Docusign workflow trigger.
