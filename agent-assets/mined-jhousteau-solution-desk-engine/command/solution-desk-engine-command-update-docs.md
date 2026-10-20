---
name: update-docs
description: Update project documentation - optionally scoped to a specific issue
argument-hint: [issue-number]
---

<role>
You are a documentation maintainer responsible for keeping project documentation accurate and up-to-date.
</role>

<purpose>
Ensure all documentation accurately reflects the current codebase, APIs, configurations, and features.
If an issue number is provided, focus documentation updates on changes related to that issue.
</purpose>

<procedure>

## 1. Scope Determination

If an issue number is provided:
```bash
# Get issue details and related changes
gh issue view $1 --json title,body,labels
# Find recent commits related to this issue
git log --oneline --grep="#$1" --since="30 days ago"
```
Focus documentation updates on areas affected by this issue.

If no issue number provided, perform comprehensive documentation review.

## 2. Documentation Inventory

Identify all documentation files:
```bash
# Find all markdown documentation
find . -name "*.md" -type f | grep -E "(README|DOCS?|docs?|GUIDE|ARCHITECTURE|API)" | sort

# Check for other documentation formats
find . -name "*.rst" -o -name "*.txt" | grep -iE "readme|install|guide"

# Look for inline documentation
grep -r "TODO.*doc" . --focus="*.py" --focus="*.js" --focus="*.ts" 2>/dev/null | head -20
```

## 3. Code-Documentation Alignment

### API Documentation
- Review all public APIs and ensure they're documented
- Update parameter descriptions and return types
- Add examples for complex functionality
- Verify all endpoints/methods are covered

### Configuration Documentation
- Check all environment variables are documented
- Update default values and required settings
- Document any new configuration files
- Ensure examples match current schema

### README Updates
- Verify installation instructions work
- Update dependency versions
- Check all commands and examples run correctly
- Ensure badges and links are valid

### Architecture Documentation
- Update component diagrams if structure changed
- Document new modules or services
- Update data flow descriptions
- Check technology stack listing

## 4. Specific Areas to Check

### Code Changes vs Documentation
```bash
# Find recently modified code files
git diff --name-only HEAD~10 | grep -E "\.(py|js|ts|go|rs)$"

# Check if corresponding docs exist
for file in $(git diff --name-only HEAD~10); do
    base=$(basename $file | cut -d. -f1)
    find docs -name "*${base}*" -type f 2>/dev/null
done
```

### Version Information
- Update version numbers in documentation
- Check changelog is current
- Update migration guides if needed

### Dependencies
- Verify requirements.txt/package.json match docs
- Update compatibility matrices
- Document any breaking changes

### Examples and Tutorials
- Test all code examples still work
- Update screenshots if UI changed
- Verify tutorial steps are accurate

## 5. Documentation Quality Checks

### Link Validation
```bash
# Find all markdown links and check they exist
grep -h "\[.*\](.*)" *.md | grep -oE "\([^)]+\)" | tr -d "()" | while read link; do
    if [[ $link == http* ]]; then
        echo "External: $link"
    elif [[ -f $link ]]; then
        echo "✓ Valid: $link"
    else
        echo "✗ Broken: $link"
    fi
done
```

### Consistency Checks
- Ensure consistent terminology throughout
- Verify command syntax is uniform
- Check code style in examples matches project standards
- Validate markdown formatting

## 6. Auto-Generation Where Applicable

### Generate API Documentation
```python
# For Python projects with docstrings
# Run appropriate doc generator (sphinx, mkdocs, etc.)
```

### Update Schema Documentation
```bash
# For projects with schemas
# Generate documentation from schema files
```

## 7. Create Update Summary

Document what was updated:
- List all files modified
- Summarize major changes
- Note any documentation gaps found
- Flag items needing expert review

## Key Principles

1. **Accuracy First**: Documentation must match actual behavior
2. **Completeness**: Cover all public interfaces and key features
3. **Clarity**: Use clear, concise language with examples
4. **Maintenance**: Flag or remove outdated information
5. **Accessibility**: Ensure docs are easy to find and navigate

## Focus Areas by Issue Type

If issue number provided, prioritize based on issue type:

- **Feature Issues**: Document new functionality, update examples
- **Bug Issues**: Update any incorrect documentation, add clarifications
- **Performance Issues**: Document optimizations, best practices
- **Security Issues**: Update security guidelines, configuration docs
- **Refactoring Issues**: Update architecture docs, API changes

Remember: Good documentation reduces support burden and accelerates development. Keep it current, clear, and comprehensive.
