# /audit-solution

Comprehensive audit of git changes to ensure clean, lean solutions free of errors and omissions.

## Purpose

Reviews all git status and diff changes in the current session to:
- Remove dead code and failed attempts
- Ensure no accidental deletions or missing functionality
- Clean up orphaned files and test artifacts
- Verify version consistency across files
- Assess solution completeness and quality

## Usage

```
/audit-solution
```

Optional parameters:
- `--detailed` - Show detailed file-by-file analysis
- `--base-branch <branch>` - Compare against specific branch (default: main)

## What It Checks

### 🧹 Code Quality
- **Dead code**: Commented-out blocks, unused imports
- **Development artifacts**: TODO, FIXME, HACK comments
- **Incomplete edits**: Malformed JSON, unclosed strings/brackets
- **Large deletions**: Suspiciously large code removals

### 📋 Consistency
- **Version numbers**: Inconsistent versions across files
- **File completeness**: Incomplete function/class definitions
- **Import statements**: Unused or missing imports

### 🗑️ Cleanup
- **Orphaned files**: Temporary files, .bak files, test scripts
- **Failed approaches**: Code from abandoned implementation attempts
- **Debug code**: Console logs, print statements, debug flags

### ⚠️ Risk Assessment
Categorizes each file change as:
- **High risk**: Core files, large changes, many issues
- **Medium risk**: Moderate changes with some concerns
- **Low risk**: Small, clean changes

## Output

### Summary Report
```
🔍 Solution Audit Report
==================================================
Solution audit complete: 8 files changed (247+ 89- lines).
✅ High confidence - solution looks clean.
Confidence Score: 85/100
```

### Issue Categories
- **💀 Dead Code Found**: Commented code to remove
- **📋 Version Inconsistencies**: Mismatched version numbers
- **🗑️ Orphaned Files**: Temporary files to delete
- **🧹 Recommended Actions**: Specific cleanup tasks

### Detailed Analysis (--detailed flag)
```
📁 File Analysis:
  M genesis/core/dependencies.py (medium risk)
    ⚠️ Multiple versions found: v0.11.1, v0.12.0, v0.12.1
  A scripts/test-container-install.sh (low risk)
    ⚠️ Temporary test file detected
```

## Confidence Score

**90-100**: Excellent - Clean, comprehensive solution
**70-89**: Good - Minor issues, mostly cosmetic
**50-69**: Fair - Some concerns, review recommended
**0-49**: Poor - Significant issues, major cleanup needed

## Integration

The command automatically:
1. Analyzes all modified/added/deleted files
2. Reviews git diffs line by line
3. Applies pattern matching for common issues
4. Generates actionable cleanup recommendations
5. Provides confidence assessment

## Use Cases

- **Before committing**: Ensure changes are clean
- **After refactoring**: Verify no functionality lost
- **Code review prep**: Self-audit before PR
- **Session cleanup**: Remove development artifacts
- **Quality gate**: Enforce solution standards

## Example Workflow

```bash
# After making changes
/audit-solution

# Review issues and fix them
# Run detailed analysis
/audit-solution --detailed

# When confidence > 80, proceed with commit
genesis commit -m "feature: clean implementation"
```

## Best Practices

✅ **Always run** after major refactoring sessions
✅ **Fix issues** before committing changes
✅ **Use detailed mode** for high-risk changes
✅ **Aim for 80+** confidence score
✅ **Document** any intentional "issues" (like TODOs)

❌ **Don't ignore** high-risk file warnings
❌ **Don't commit** with confidence < 60
❌ **Don't skip** cleanup recommendations
