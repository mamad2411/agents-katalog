---
name: skill-qc-handoff
description: Create the mandatory Dev-to-QC handoff document after Code Done.
category: workflow
---

# Skill: QC Handoff

Use only after dev verification returns DEV_DONE.

## Include

```text
summary
scope and out of scope
changed services/files
API/event/schema/UI/config changes
acceptance criteria
dev verification score
critical check evidence
manual verification notes
QC test suggestions
test data and environment notes
known risks
retest scope
```

## Rules

```text
No handoff without DEV_DONE.
Do not hide limitations.
Make QC steps executable and specific.
```
