---
name: Pull Request Description Rules
alwaysApply: false
description: >-
  Generate comprehensive pull request descriptions from commit history and
  changes

  Use when: Creating PR/MR descriptions, analyzing commit ranges between
  branches, or documenting feature implementations

  Input: Git commit history, commit ranges (e.g., main..feature-branch), branch
  comparisons

  Output: Structured markdown with summary, changes, breaking changes, and
  testing notes
---


# Pull Request Description Rules

These rules define how to analyze commit history and generate comprehensive PR descriptions. These same rules should work consistently across GitHub, GitLab, Bitbucket, and any other platform.

## Template Structure

```markdown
## Summary
Brief overview of what this PR accomplishes

## Changes Made
- Key change 1
- Key change 2  
- Key change 3

## Breaking Changes
- Breaking change 1 (if any)
- Migration steps

## Testing
- Test approach
- Coverage notes
- Manual testing performed

## Additional Notes
- Performance implications
- Security considerations
- Follow-up tasks
```

## Analysis Patterns

### Extracting Summary from Commits

Look for patterns in commit messages:
- **feat commits** → New functionality being added
- **fix commits** → Problems being resolved  
- **refactor commits** → Code improvements
- **Multiple related commits** → Larger feature implementation

Generate summary that captures the **why** and **what** at a high level.

### Categorizing Changes

Group commits by impact area:

**Features**
- New user-facing functionality
- API endpoints
- UI components
- Business logic

**Bug Fixes**  
- Error handling improvements
- Logic corrections
- Edge case handling
- Performance fixes

**Infrastructure**
- Build system changes
- CI/CD updates
- Dependencies
- Configuration

**Code Quality**
- Refactoring
- Documentation
- Testing improvements
- Style/formatting

### Identifying Breaking Changes

Look for patterns that indicate breaking changes:
- Removed public APIs or endpoints
- Changed function signatures
- Modified response formats
- Removed or renamed configuration options
- Database schema changes
- Updated dependencies with breaking changes

### Testing Analysis

Analyze test-related changes:
- New test files → Describe testing approach
- Modified tests → Note coverage changes
- Performance tests → Mention benchmarks
- Integration tests → Describe scenarios

## Content Guidelines

### Summary Section
- **One paragraph** explaining the core purpose
- **Focus on user impact** or business value
- **Avoid technical jargon** when possible
- **Include motivation** - why was this needed?

### Changes Made Section
- **Group related changes** together
- **Use action verbs** (Added, Updated, Removed, Fixed)
- **Be specific** but not exhaustive
- **Focus on significant changes**, not every line

### Breaking Changes Section
- **List all breaking changes** explicitly
- **Provide migration guidance** when possible
- **Include version information** if relevant
- **Highlight deprecation timelines**

### Testing Section
- **Describe test strategy** for new features
- **Note manual testing performed**
- **Mention performance testing** if applicable
- **Include edge cases covered**

## Analysis Rules for Commit History

When processing commits between base and head:

### 1. Commit Message Analysis
```
feat(auth): add OAuth integration → Feature addition
fix(api): resolve timeout issues → Bug fix  
refactor(db): optimize query performance → Code improvement
test(auth): add OAuth test coverage → Testing improvement
```

### 2. File Change Analysis
```
New files in src/ → New feature
Modified existing src/ → Enhancement or fix
Changes in tests/ → Testing improvements  
Changes in docs/ → Documentation updates
Changes in config/ → Infrastructure changes
```

### 3. Scope and Impact Assessment
```
Single component changes → Focused feature
Multiple component changes → Large feature
Cross-cutting concerns → Architecture change
Performance-related changes → Optimization
Security-related changes → Security improvement
```

## Quality Indicators

### Good PR Descriptions Include:
- Clear business justification
- Comprehensive change summary
- Testing approach description
- Breaking change documentation
- Performance/security notes

### Red Flags to Avoid:
- Vague summaries ("Fixed stuff")
- Missing breaking change documentation
- No testing information
- Technical jargon without explanation
- Missing context for large changes

## Context-Specific Rules

### Feature PRs
- Emphasize user value and use cases
- Include screenshots/demos if UI changes
- Document configuration changes
- Explain feature flags or rollout strategy

### Bug Fix PRs  
- Describe the problem being solved
- Explain root cause if complex
- Include reproduction steps if helpful
- Note if hotfix or requires backporting

### Refactoring PRs
- Explain motivation for refactoring
- Highlight benefits (performance, maintainability)
- Note that behavior shouldn't change
- Include before/after metrics if relevant

### Infrastructure PRs
- Explain impact on development workflow
- Note any required environment changes
- Include rollback procedures
- Document new tools or dependencies

## Automation Guidelines

For tools generating PR descriptions:

1. **Parse commit messages** for conventional commit types
2. **Analyze file changes** to understand scope of impact
3. **Identify patterns** in commits (all tests, all docs, etc.)
4. **Group related changes** logically
5. **Extract key information** from commit bodies
6. **Preserve important details** from individual commits
7. **Generate appropriate sections** based on change types
8. **Include relevant links** to issues or documentation

## Template Variations

### Simple Bug Fix
```markdown
## Summary
Fixes [brief description of bug] that was causing [impact].

## Changes Made
- [Specific fix implemented]

## Testing
- [How the fix was verified]
```

### Major Feature
```markdown
## Summary
Implements [feature name] to [business value/user benefit].

## Changes Made
- **Core Feature**: [main functionality]
- **API Changes**: [new endpoints/modifications]  
- **UI Updates**: [user interface changes]
- **Database**: [schema changes if any]

## Breaking Changes
- [Any breaking changes with migration notes]

## Testing
- Unit tests for [coverage areas]
- Integration tests for [scenarios]
- Manual testing: [specific test cases]

## Performance Impact
- [Any performance considerations]

## Security Considerations  
- [Security implications if any]
```

### Documentation Update
```markdown
## Summary
Updates documentation for [area] to [improvement].

## Changes Made
- [Specific documentation changes]

## Additional Notes
- [Context or follow-up items]
```