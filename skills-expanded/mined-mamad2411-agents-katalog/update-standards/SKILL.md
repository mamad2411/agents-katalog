---
name: update-standards
description: Update timesheet-bot coding standards from official sources - add rules for new patterns, re-verify all cited URLs, or audit the rule set - via the standards-curator agent.
argument-hint: "add <patterns or topics> | verify | audit"
disable-model-invocation: true
context: fork
agent: standards-curator
background: false
---

Mode and input: $ARGUMENTS

Working directory: the timesheet-bot repository root.

If no mode is given, run `verify` and then `audit`.

Follow your instructions for the mode. End with the changelog. If any rule became UNSUPPORTED or a security rule would weaken, the first line of the report must be `DECISION NEEDED: <summary>`.
