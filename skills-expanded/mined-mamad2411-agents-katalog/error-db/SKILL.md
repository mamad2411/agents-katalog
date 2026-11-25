---
name: error-db
version: 1.0.0
description: Error pattern database. Stores every error with full context, auto-detects similar errors, suggests fixes based on history. Same error twice auto-generates a prevention rule. The brain's immune system. Triggers on: any error, crash, test failure, unexpected behavior.
---

# Error DB — Error Pattern Database

> **"不记错的脑子不算脑子。同错两次自动免疫。"**

## Core Principle

Every error is a learning opportunity. Store it, pattern-match it, never repeat it.

## What Gets Stored

Every error with full forensic context:

| Field | What | Example |
|-------|------|---------|
| **timestamp** | When | 2026-06-26T09:15:00 |
| **error_type** | Category | syntax / runtime / logic / config / dependency |
| **error_message** | Exact message | "UnicodeDecodeError: 'charmap' codec can't decode byte 0x90" |
| **context** | What was being done | "Writing SKILL.md with Chinese characters on Windows" |
| **root_cause** | Why it happened | "Python quick_validate.py reads with cp1252, file is UTF-8" |
| **fix** | How it was resolved | "Set PYTHONUTF8=1 or use encoding='utf-8' in open()" |
| **fix_type** | Category of fix | code-change / config / workaround / dependency-update |
| **files_involved** | Which files | quick_validate.py, SKILL.md |
| **recurrence_count** | How many times | 1 (first occurrence) |
| **prevention_rule** | Auto-generated? | "Python scripts must specify encoding" |

## Storage Backend

Same SQLite database, table `error_log`:

```sql
error_log(id, timestamp, error_type, error_message, context, root_cause, fix, fix_type,
          files_involved, recurrence_count, prevention_rule, session_id)
error_fts  -- FTS5 for full-text error search
```

PowerShell interface:
```powershell
memory-db.ps1 -Action err-store -Type "syntax" -Message "..." -Context "..." -RootCause "..." -Fix "..."
memory-db.ps1 -Action err-search -Query "UnicodeDecodeError" -Limit 5
memory-db.ps1 -Action err-stats   # most frequent errors, by type, by file
memory-db.ps1 -Action err-check  -Message "..."  # check if similar error exists
```

## Pattern Detection

### Similarity Scoring
When a new error occurs, compare against existing errors:
- Exact message match → **same error (recurrence++)**
- Same error_type + same file → **similar (85% match)**
- Same error_type + similar root_cause → **related (60% match)**
- Different type + different file → **new error**

### Auto-Rule Generation
| Recurrence | Action |
|-----------|--------|
| 1st time | Store, no alert |
| 2nd time | Alert: "This error happened before. Previous fix: [X]" |
| 3rd time | Auto-generate prevention rule → write to `.claude/rules/` |

### Auto-Fix Suggestion
When an error matches an existing pattern:
1. Retrieve fix from database
2. Apply fix automatically if fix_type = "code-change" and confidence > 80%
3. Suggest fix to user if confidence 50-80%
4. Flag for manual investigation if confidence < 50%

## Trigger

| Trigger | Action |
|---------|--------|
| Any error/exception | Store immediately (err-store) |
| Before fixing | Search error-db for similar (err-search) |
| After fixing | Update root_cause and fix fields |
| User says "this error again" | Check recurrence count, suggest permanent fix |

## Integration

- **memory-lora**: Errors stored as memory entities (score 0.7 initially, decay normally)
- **precommit-pipeline**: Pipeline catches syntax/ref errors → stored in error-db
- **failure-predictor**: Error-db patterns → feed into pre-mortem risk analysis
- **second-brain**: Brain 2 verifies root_cause analysis for complex errors
- **orchestrator**: Any task that errors → orchestrator routes to error-db before retry

## Anti-Patterns

- Storing errors without root_cause (just logging symptoms, not learning)
- Letting error-db grow unbounded (prune errors older than 90 days with recurrence_count=1)
- Applying auto-fix without verification (always test after auto-fix)
