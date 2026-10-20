---
description: AI Interaction Audit Log - Mandatory logging of all AI interactions, prompts, responses, timing, and errors
alwaysApply: true
tags: [critical, ai-assistant, audit, logging, compliance]
priority: 1
version: 1.1.0
---

# AI Interaction Audit Log

## 🔴 MANDATORY: AI Interaction Logging

**ALL AI interactions MUST be logged automatically for audit and analysis purposes.**

---

## Core Requirements

### What Must Be Logged

**Every AI interaction MUST capture:**

1. **User Prompt** - Full text (truncate if >10,000 chars)
2. **Timestamps** - Request and response (ISO 8601: `YYYY-MM-DDTHH:mm:ss.sssZ`)
3. **Response Time** - Duration in milliseconds
4. **Error Status** - `success`, `error`, or `partial`
5. **Agentic Responses** - Tool call count, tools used list
6. **Metadata** - AI model name, IDE name, files modified/read, commands executed

---

## Log File Location

**Location:** `logs/audit/YYYY-MM-DD.jsonl` (JSON Lines format, one entry per line)  
**Archive:** Move files >30 days old to `logs/audit/archive/` and compress

---

## Log Entry Format

**Required JSON structure:**
```json
{
  "timestamp": {"request": "ISO8601", "response": "ISO8601"},
  "duration_ms": 1234,
  "status": "success|error|partial",
  "error": {"type": "...", "message": "..."} | null,
  "user_prompt": "...",
  "user_prompt_truncated": false,
  "user_prompt_length": 45,
  "ai_model": "Composer",
  "ide": "Cursor IDE",
  "agentic_responses": {
    "total_tool_calls": 8,
    "tools_used": ["read_file", "write", ...],
    "tool_call_count": {"read_file": 3, ...}
  },
  "files_modified": ["path/to/file"],
  "files_read": ["path/to/file"],
  "commands_executed": ["git status", ...],
  "response_length": 1234,
  "metadata": {"project": "...", "workspace": "..."}
}
```

---

## Automatic Logging Workflow

**After completing each user interaction:**

1. Capture request timestamp (when prompt received)
2. Track all tool calls during interaction
3. Capture response timestamp (when response complete)
4. Calculate duration: `response_timestamp - request_timestamp`
5. Collect metadata (model, IDE, files, commands)
6. Write JSON entry to `logs/audit/YYYY-MM-DD.jsonl` (append mode)
7. If logging fails, continue interaction (don't block user)

---

## Privacy & Security

**Do NOT log:** Passwords, API keys, PII, sensitive business data  
**Redact:** Replace sensitive data with `[REDACTED]` marker

---

## Remember

✅ **ALWAYS log every interaction** - No exceptions  
✅ **Capture all required fields** - Timestamps, duration, tool calls, errors  
✅ **Use JSON Lines format** - One entry per line  
✅ **Handle errors gracefully** - Don't block user if logging fails  
✅ **Protect sensitive data** - Redact passwords, API keys, PII

---

**For detailed examples, implementation code, and analysis tools, see:**  
`docs/audit-log-reference.md` (reference document, not loaded into context)

**Last Updated:** 2025-01-22  
**Version:** 1.1.0  
**Status:** MANDATORY  
**Priority:** CRITICAL
