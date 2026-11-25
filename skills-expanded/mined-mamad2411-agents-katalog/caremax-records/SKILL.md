---
name: caremax-records
description: "Query and search medical records from CareMax Health API. Use when a user asks about medical reports, check-up history, hospital visits, test results, or wants to find specific records. Supports structured query and AI-powered semantic search. Trigger terms: medical record, check-up, hospital report, test result, health report, find report, search records, medical history, 体检, 报告, 检查."
license: MIT
---

# CareMax Medical Records

> **Requires `caremax-auth` skill.** If `~/.claude/skills/caremax-auth/` doesn't exist, tell the user to install it first.

This skill covers querying and searching medical records.

## Prerequisites — Auto-Auth (MANDATORY)

```bash
APICALL="bash ~/.claude/skills/caremax-auth/scripts/api-call.sh"
```

If `api-call.sh` returns `{"error":"no_credentials",...}` → **immediately run `bash ~/.claude/skills/caremax-auth/scripts/auth-flow.sh [base_url]`** in background. If the user specified a custom URL, pass it as the argument.

## Query Records (Structured)

```bash
# By date range
$APICALL POST /api/skill/records/query '{"dateRange":["2025-01-01","2025-12-31"]}'

# By indicator name
$APICALL POST /api/skill/records/query '{"indicatorName":"creatinine"}'

# By report title
$APICALL POST /api/skill/records/query '{"reportTitle":"血常规"}'

# By member + pagination
$APICALL POST /api/skill/records/query '{"memberId":"member-uuid","page":1,"limit":20}'
```

All fields optional. Response: `records[]` (id, test_date, hospital, department, report_title, has_abnormality, indicators[]), `total`, `page`.

## Semantic Search (AI-Powered)

```bash
$APICALL POST /api/skill/records/search '{"query":"肝功能异常","topK":5}'
# With member filter:
$APICALL POST /api/skill/records/search '{"query":"recent blood routine","memberId":"xxx"}'
```

Accepts Chinese and English natural language.

## Recommended Workflow

"show my recent check-up results":
```bash
$APICALL POST /api/skill/records/query '{"dateRange":["2025-01-01","2025-06-30"]}'
```

"find reports with abnormal results":
```bash
$APICALL POST /api/skill/records/search '{"query":"abnormal indicators"}'
```

"how's my liver":
```bash
$APICALL POST /api/skill/records/search '{"query":"肝功能"}'
```
