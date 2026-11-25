---
name: trouble_shooter
description: Document bugs and problems that took effort to solve, including their solutions, when the user says things like "save the problem and solution", "remember this", or "document this".
---

## What This Skill Does

1. State briefly that the troubleshooting documentation workflow is being used.
2. Suggest a clear file title based on the problem.
3. Check if similar issues exist in `docs/resolved_problems/`.
4. Organize the debugging history from the conversation.
5. Create a clean summary with the problem and solution in markdown.

## Where Files Go

Save to: `docs/resolved_problems/{problem_description}.md`

File naming uses snake_case and should be specific:

- `cuda_out_of_memory_during_gaussian_blur.md`
- `spatial_categorizer_wrong_threshold_values.md`
- Avoid vague names like `plot_not_showing.md`.
- Avoid broad names like `buttons_not_working.md`.

## How To Organize Content

First, check what is already there:

- Look in `docs/resolved_problems/*.md` for similar issues.
- If you find the same bug, add to that file.
- If it is a new problem, create a new file.

## Markdown Format

```markdown
---
keywords: keyword1, keyword2, error_message_snippet
files_changed: path/to/file1.py, path/to/file2.py
severity: critical / major / minor
---

# 2026-01-30

## Problem Description

Brief summary of what went wrong and where it showed up.

### Symptoms

- What the user saw, including error messages or wrong behavior.
- When it happened.

### Example Error

```text
Paste actual error message here
```

## Root Cause

Explain what was actually causing the problem.

## Solution

### Files Changed

- `path/to/file.py:123` - What changed.
- `path/to/another.py:45` - Another change.

### Code Changes

```python
# Before
old_code_snippet

# After
new_code_snippet
```

### Why This Fixes It

Explain why the original code did not work and why the new code does.
```

## Quick Checklist

- Check `docs/resolved_problems/*.md` first for similar issues.
- Use descriptive file names that explain the actual problem.
- Include the error message or symptoms.
- Explain the root cause, not just the fix.
- List which files were changed.
- Add keywords for easy searching later.
- Note severity.

## Before Saving

Show the user:

1. The filename to use.
2. Brief summary of the problem and solution.
3. Which files were changed.
4. Whether the issue should merge with an existing file or create a new one, if that is not clear.
