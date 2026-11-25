---
name: github-branch-management
description: Comprehensive branch lifecycle management, protection rules, and naming conventions
routing_criteria:
  - "branch protection"
  - "branch naming"
  - "branch lifecycle"
  - "merge conflicts"
  - "branch cleanup"
agent: paperclipforge-ai-github-operations-specialist
---

# GitHub Branch Management

## Overview

Specialized skill for managing Git branch lifecycles, implementing protection rules, enforcing naming conventions, and maintaining branch hygiene across repositories.

## Capabilities

### Branch Protection & Security
- **Protection Rules**: Configuration and enforcement of branch protection settings
- **Required Reviews**: Management of required reviewer counts and approval rules
- **Status Checks**: Integration with CI/CD pipelines and required status checks
- **Push Restrictions**: Control of who can push to protected branches

### Branch Naming & Organization
- **Naming Conventions**: Enforcement of consistent branch naming standards
- **Branch Categories**: Organization by feature, bugfix, hotfix, release branches
- **Semantic Naming**: Integration with conventional commit practices
- **Branch Prefixes**: Standardized prefixes for different branch types

### Lifecycle Management
- **Branch Creation**: Automated and standardized branch creation workflows
- **Branch Merging**: Safe merge operations with conflict resolution
- **Branch Deletion**: Automated cleanup of merged and stale branches
- **Branch Archiving**: Long-term storage of important historical branches

### Conflict Resolution
- **Merge Conflict Detection**: Early identification of potential conflicts
- **Resolution Strategies**: Automated conflict resolution where possible
- **Manual Resolution**: Guidance for complex conflict scenarios
- **Prevention Measures**: Best practices to minimize future conflicts

## Integration Points

### DevForge AI
- **Development Workflow**: Seamless integration with development branching strategies
- **Code Review**: Branch protection alignment with review requirements
- **Release Management**: Branch management for release processes

### QualityForge AI
- **Quality Gates**: Branch protection integration with quality standards
- **Testing Requirements**: Status check configuration for automated testing
- **Compliance Monitoring**: Enforcement of organizational branch policies

## Success Metrics

- **Protection Compliance**: >98% compliance with branch protection rules
- **Naming Consistency**: >95% adherence to branch naming conventions
- **Merge Success Rate**: >90% successful automated merges
- **Cleanup Efficiency**: <24 hours average time for branch cleanup

## Usage Examples

### Branch Protection Setup
```
Protected Branch: main
- Required reviews: 2
- Required status checks: CI, Security Scan, Code Coverage
- Restrict pushes: Allow only admins and maintainers
- Require linear history: Enabled
```

### Branch Naming Convention
```
feature/user-authentication
bugfix/login-validation-error
hotfix/security-patch-2026-04
release/v2.1.0
```

### Automated Branch Cleanup
```
Stale branches (>30 days):
- Delete merged feature branches
- Archive unmerged but inactive branches
- Notify owners of branches requiring attention