---
name: github-commit-management
description: Expert management of Git commit standards, atomic commits, and commit history integrity
routing_criteria:
  - "commit message standards"
  - "conventional commits"
  - "atomic commits"
  - "commit history cleanup"
  - "semantic versioning"
agent: paperclipforge-ai-github-operations-specialist
---

# GitHub Commit Management

## Overview

Specialized skill for managing Git commit standards, ensuring atomic commits, maintaining commit history integrity, and enforcing conventional commit practices across the Paperclip ecosystem.

## Capabilities

### Commit Standards Enforcement
- **Conventional Commits**: Implementation and enforcement of conventional commit format
- **Semantic Versioning**: Integration with semantic versioning practices
- **Message Quality**: Automated validation of commit message quality and completeness
- **Template Enforcement**: Standardized commit message templates and guidelines

### Atomic Commit Management
- **Logical Changes**: Ensuring commits represent single, logical units of change
- **Change Isolation**: Proper separation of concerns in commit content
- **Revert Safety**: Commits designed for safe and clean reversion
- **Review Readiness**: Commits structured for efficient code review

### History Integrity
- **Clean History**: Maintenance of readable, meaningful commit histories
- **Interactive Rebasing**: Safe history rewriting and cleanup operations
- **Branch History**: Management of branch-specific commit policies
- **Merge Strategies**: Appropriate merge strategy selection and execution

## Integration Points

### DevForge AI
- **Code Review Coordination**: Commit standards alignment with review processes
- **Quality Standards**: Integration with code quality and testing standards
- **Development Workflow**: Seamless integration with development pipelines

### QualityForge AI
- **Standards Validation**: Automated validation of commit standards compliance
- **Quality Metrics**: Commit quality metrics and reporting
- **Process Compliance**: Enforcement of organizational commit policies

## Success Metrics

- **Standards Compliance**: >95% adherence to commit message standards
- **Atomic Commit Rate**: >90% of commits represent single logical changes
- **History Quality**: Maintain clean, readable commit histories
- **Review Efficiency**: Improved code review efficiency through better commit structure

## Usage Examples

### Commit Message Validation
```
feat: add user authentication system

- Implement JWT token-based authentication
- Add user registration and login endpoints
- Include password hashing and validation
- Add session management utilities
```

### Atomic Commit Structure
```
refactor: extract authentication middleware

- Move auth logic to dedicated middleware module
- Update route handlers to use new middleware
- Add comprehensive error handling
- Update documentation and tests
```

### History Cleanup
```
Interactive rebase to:
- Squash related commits
- Fix commit message formatting
- Remove temporary/debug commits
- Ensure logical commit progression