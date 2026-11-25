---
alwaysApply: true
---

# Safety Requirements

## Critical Rules
All destructive operations MUST follow these rules without exception.

## 1. Explicit Confirmation Required
- **Delete operations**: Must show file details + require "yes" confirmation
- **Batch operations**: Must show count + total size + require confirmation
- **No auto-delete**: User must actively choose delete action
- **Case-sensitive confirmation**: Accept only exact "yes" or "y"

```python
# Good
if confirm_delete(file):
    delete_file(file)

# Bad - Never do this
delete_file(file)  # No confirmation!
```

## 2. Preview Before Execution
- Show what will happen before it happens
- Display affected files, destination, or action
- Provide summary of consequences (files affected, space freed)

```python
# Before delete
print(f"About to DELETE: {file.name} ({file.size})")
print(f"Last accessed: {file.last_access}")
if not confirm("Continue?"): return
```

## 3. Dry-Run Mode
- Must support `--dry-run` flag
- Shows all operations without executing
- Clearly label output as "DRY RUN"
- No filesystem modifications in dry-run

```python
if dry_run:
    logger.info(f"[DRY RUN] Would delete: {file}")
    return True
else:
    return delete_file(file)
```

## 4. Graceful Error Handling
- Permission denied: Skip file, log warning, continue
- File not found: Log and skip (may have been moved)
- Disk full: Abort safely, report partial completion
- Never crash mid-operation

```python
try:
    operation(file)
except PermissionError:
    logger.warning(f"Skipped (permission denied): {file}")
except Exception as e:
    logger.error(f"Failed: {file} - {e}")
```

## 5. Operation Logging
- Log all destructive actions
- Include timestamp, action type, file path
- Store in user-accessible location
- Format: human-readable text

```
2024-11-15 14:32:15 | DELETE | ~/Downloads/old-file.pdf | 2.3 MB
2024-11-15 14:32:18 | MOVE   | ~/Desktop/doc.txt → ~/Archive/
```

## 6. No Silent Failures
- All operations return success/failure status
- Report failures in final summary
- Never hide errors from user
- Distinguish between skipped and failed

## 7. Reversible When Possible
- **Move** over **Delete** as default suggestion
- Create archives before bulk delete (optional)
- Document that deletion is permanent
- No built-in undo (by design, keeps it simple)

## 8. Safe Defaults
- Default action: Keep/Skip
- No operation on Enter press
- Require explicit action selection
- Batch mode requires explicit flag

## Forbidden Patterns
- ❌ Auto-deletion based on criteria alone
- ❌ Background/scheduled operations
- ❌ Operating without user's current session
- ❌ Modifying system or hidden files
- ❌ Following symlinks (potential danger)
- ❌ Recursive deletion without per-file review