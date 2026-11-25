---
name: review-pr-changes
description: "Review PR changes with structured checklist for quality and standards compliance. Use for comprehensive PR code review."
category: review
---

# Review PR Changes

Perform structured review of PR changes against project quality standards.

## Quick Reference

```bash
# Get PR files changed
gh pr diff <pr> --name-only

# View specific file diff
gh pr diff <pr> -- path/to/file

# Get PR review status
gh pr view <pr> --json reviews

# Check file statistics
gh pr diff <pr> | diffstat

# Get PR body/description
gh pr view <pr> --json body
```

## Review Checklist

**Code Quality**:

- [ ] Code is readable and well-structured
- [ ] Functions/classes have clear purposes
- [ ] No code duplication (DRY principle)
- [ ] Proper error handling
- [ ] No unnecessary complexity

**Testing**:

- [ ] Tests present for new functionality
- [ ] Tests are passing (CI shows green)
- [ ] Edge cases covered
- [ ] Adequate coverage for changes

**Documentation**:

- [ ] Docstrings for public APIs
- [ ] Type hints present
- [ ] Comments for non-obvious code

**Security & Git**:

- [ ] No hardcoded secrets/tokens
- [ ] Input validation present
- [ ] PR linked to issue (in description)
- [ ] No unintended files included

## Review Workflow

1. **Check context**: View PR description and linked issue
2. **Scan changes**: Review file list and statistics
3. **Read code**: Examine actual changes carefully
4. **Run checklist**: Go through each category
5. **Test locally**: Pull and test changes if needed
6. **Create comments**: Flag issues as code comments
7. **Provide verdict**: Approve, request changes, or comment

## Output Format

Report review results with exactly these sections:

1. **Summary** — 1-2 sentence overall assessment
2. **Issues Found** — Problems that must be fixed (omit if none)
3. **Verdict** — Approve / Request Changes / Comment

## Error Handling

| Problem | Solution |
|---------|----------|
| Can't access PR | Check gh auth status |
| Can't understand code | Ask clarifying question in comment |
| Needs local testing | Use worktree-create skill to test |
| Multiple issues | Prioritize critical first, optional second |
| Disagreement on style | Refer to CLAUDE.md for standards |

## References

- See CLAUDE.md for project standards
- See verify-pr-ready for merge readiness check
- See gh-batch-merge-by-labels for batch review workflow
