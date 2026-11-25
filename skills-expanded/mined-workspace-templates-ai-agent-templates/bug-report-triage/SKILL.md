---
name: bug-report-triage
description: Triages an incoming bug report, tries to reproduce it, and writes a minimal repro with a severity and the next step for the owner.
---

# Bug report triage

Verdict and repro first. Do not fix the bug in this skill.

## Steps

1. Extract the claims: expected behavior, actual behavior, environment (version, platform, browser, account type), and the steps if any. List what is missing.
2. Check for duplicates and known fixes: search issues and the changelog for the error text and the feature name, and look at recent commits touching the area. If it is fixed in a newer version, say which.
3. Try to reproduce on the current main branch. Start from the reporter's steps. Capture exact commands, inputs and output. Try once more with a clean state to rule out leftover data.
4. If it reproduces, shrink it. Remove steps and data until each remaining one is needed. Aim for a failing test, a script of under ten lines, or at most five manual steps.
5. If it does not reproduce, say what you tried and in which environment, then list the specific facts that would help: version, logs, request ID, account type, time. Do not close the report yourself.
6. Locate, lightly. Name the module and the likely cause only if the evidence supports it. Mark the confidence as high, medium or low.
7. Rate severity. Critical: data loss, security or payment impact, or a total outage. High: a main flow is broken with no workaround. Medium: broken with a workaround. Low: cosmetic or rare. State the number of affected users when the logs show it.

## Rules

- Never edit source code. A repro test goes in a new file or the comment, not in the suite.
- Never include customer personal data in the report. Replace it with placeholders.

## Report

Verdict (reproduced, not reproduced, duplicate, needs info), severity, minimal repro, suspected area with confidence, and the suggested owner or label.
