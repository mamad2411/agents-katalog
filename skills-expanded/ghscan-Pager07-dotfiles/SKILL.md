---
name: review-ui2
description: Review a UI 2.0 frontend overhaul PR for breaking bugs, regressions, and issues
---

# UI 2.0 PR Review

You are reviewing a UI 2.0 frontend overhaul PR. This is part of an ongoing migration (Bootstrap to Tailwind, template redesigns, new JS patterns). Your job is to find breaking bugs, regressions, and issues introduced by this PR.

## Steps

### 1. Identify the PR and its base branch
- Determine the current git branch.
- Find the associated PR on GitHub using `gh pr view`.
- **CRITICAL**: Detect the PR's base branch from `gh pr view --json baseRefName -q .baseRefName`. This is the branch the PR is targeting — use THIS as the base for all diffs, NOT `master`.
- Read the PR description and understand the scope of changes.

### 2. Get all changed files
- Use `gh pr diff` or `git diff <base-branch>...HEAD` where `<base-branch>` is the base branch detected in Step 1.
- List all changed/added/deleted files.
- Categorize them: templates, Python views, CSS/SCSS, JavaScript, URLs, tests, etc.

### 3. Review Python changes (views, URLs, forms, context)
For every changed Python file:
- Read the full file (not just the diff) to understand context.
- Check for:
  - Broken URL patterns or missing `reverse()` references.
  - Missing or changed context variables that templates depend on.
  - Changed form classes, fields, or validation that could break rendering.
  - Permission or access control changes that might be unintentional.
  - Removed or renamed views that other parts of the codebase reference.
  - QuerySet changes that could cause N+1 queries or missing data.

### 4. Review template changes
For every changed template:
- Read the full template file.
- Check for:
  - Broken template tags or filters.
  - Missing `{% load %}` tags.
  - References to context variables that no longer exist or were renamed.
  - Broken links or hardcoded URLs (should use `{% url %}` tag).
  - Unclosed HTML tags or malformed structure.
  - Missing CSRF tokens on forms.
  - Broken template inheritance (`{% extends %}`, `{% block %}`).
  - Accessibility regressions (missing labels, alt text, ARIA attributes).
  - Responsive design issues (missing responsive classes).

### 5. Review JavaScript files (CRITICAL)
For every changed or newly introduced JS file:
- Read the entire file.
- Check for:
  - Syntax errors or obvious runtime errors.
  - References to DOM elements that may not exist in the new templates (broken selectors).
  - Event listeners attached to elements with old class names or IDs that were changed in templates.
  - Hardcoded URLs instead of using data attributes or Django-provided URLs.
  - Missing null checks on DOM queries (`querySelector` returning null).
  - Race conditions with DOM loading (scripts running before DOM is ready).
  - Broken imports or module references.
  - Console errors that would occur (undefined variables, missing functions).
  - jQuery vs vanilla JS inconsistencies if migrating.

### 6. Cross-file consistency checks
- Verify that CSS classes used in templates are actually defined in stylesheets.
- Verify that JS selectors match the actual DOM structure in templates.
- Verify that URL names used in templates match the URL configuration.
- Verify that form field names in templates match the form class definitions.
- Check that static file references are correct and files exist.

### 7. Test review
- If tests were changed or added, review them for correctness.
- Flag if views/templates were changed but corresponding tests were NOT updated.
- Flag any test that is now likely to fail due to the changes.

### 8. Summary
Produce a clear summary with:
- **Breaking bugs found**: Issues that WILL break functionality.
- **Potential issues**: Things that MIGHT cause problems.
- **JS concerns**: Specific JavaScript-related findings.
- **Missing test coverage**: Areas that should have tests but don't.
- **Suggestions**: Non-critical improvements.

Be thorough but practical. Focus on things that will actually break, not style preferences.
