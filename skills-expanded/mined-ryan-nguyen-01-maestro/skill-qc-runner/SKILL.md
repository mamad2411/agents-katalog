---
name: skill-qc-runner
description: Run QC from the handoff document, record test results, and stop immediately on blocker bugs.
category: workflow
---

# Skill: QC Runner

Use when a task is QC_READY.

## Flow

```text
Read QC handoff
Create test cases
Test local before higher environments unless instructed otherwise
Record each case result
On blocker, stop and create blocker bug
On non-blocker, create bug and continue unaffected cases
QC_DONE requires zero open blockers
After QC_DONE, generate Postman collection from API changes in handoff
After QC_DONE, write qc-delivery-report.md with link to Postman collection
```

## Postman Collection Export

Generate after QC_DONE so the user can replay API tests independently.

```text
Read:  .maestro/work/tasks/<task-id>/qc-handoff.md  (section: API changes)
Read:  .maestro/work/tasks/<task-id>/coder-results.yaml  (endpoint details if handoff is thin)
Write: .maestro/work/tasks/<task-id>/postman-collection.json

Format: Postman Collection v2.1
  info.schema: https://schema.getpostman.com/json/collection/v2.1.0/collection.json
  info.name:   <task-id> — <feature summary>

Per endpoint item:
  name:            <METHOD> <path> — <short description>
  method:          HTTP verb
  url:             {{BASE_URL}}<path> with :param substitution
  headers:         Content-Type: application/json
                   Authorization: Bearer {{AUTH_TOKEN}} (only if endpoint requires auth)
  body (if applicable): raw JSON minimal valid example
  response example: paste evidence from QC run when available

Postman environment variables (placeholder values only):
  BASE_URL:   http://localhost:<port>
  AUTH_TOKEN: <your-token-here>

Security rules:
  Never include real tokens, passwords, or PII in the collection.
  Use {{VARIABLE}} placeholders for any sensitive value.

Skip if no API changes: note in delivery report as "No API endpoints changed — collection not generated."
```

## QC Delivery Report

After QC_DONE, write `qc-delivery-report.md` using the template:

```text
Include:
  - Tóm tắt: what was tested, overall verdict
  - Kết quả QC: stats (total/pass/fail/blocked/blocker count)
  - Những gì đã hoàn thành: completed features list
  - Files thay đổi: services and files
  - Test Results Summary: table by category
  - Known Limitations: deferred items with severity
  - Bugs mở: blockers and non-blockers
  - Hướng dẫn verify cho User: concrete steps user can run to verify
  - Đề xuất tiếp theo: recommendations for future work

Template: .maestro/engine/templates/qc-delivery-report.template.md
Target audience: the USER (not other agents)
```

## Rules

```text
QC does not fix code.
QC does not continue after blocker.
QC does not store real secrets.
After QC_DONE, always write delivery report before declaring done.
```
