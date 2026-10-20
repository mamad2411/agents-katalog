---
description: Guidelines for generating reusable templates from project learnings
globs: ["docs/templates/**/*", ".cursor/rules/**/*"]
tags: [ai-guidelines, template-generation, meta-project]
priority: 5
version: 1.0.0
---

# Template Generation Guidelines

## Purpose

This document provides guidance for AI assistants on how to generate reusable `.cursor/rules` templates from project learnings and best practices.

## Template Generation Process

### Step 1: Identify Template Need

**Determine if a template is needed:**

- [ ] Pattern appears in 2+ projects
- [ ] Clear reusability potential
- [ ] Well-defined scope
- [ ] Sufficient documentation exists
- [ ] Positive feedback from users

**Template Candidates:**
- Git workflow standards
- Commit message formats
- Documentation structures
- Testing strategies
- CI/CD configurations
- Code style guidelines
- Persona definitions

### Step 2: Extract Core Pattern

**From project-specific implementation to generic template:**

**Original (Project-Specific):**
```markdown
# ClaimsPay Git Workflow

All commits must reference CLAIMSPAY JIRA tickets:
CLAIMSPAY-1234 -feature [WJS] Add payment validation

Branch format:
feature/CLAIMSPAY-1234-payment-validation-mbolyshkanov
```

**Template (Generic):**
```markdown
# Git Workflow Standards

All commits must reference issue tracker tickets:
[PROJECT_KEY]-[NUMBER] -[type] [Component] Brief description

Branch format:
[type]/[PROJECT_KEY]-[NUMBER]-[description]-[initials]

## Customization
- Replace [PROJECT_KEY] with your project identifier
- Adjust [Component] categories for your architecture
- Modify [type] options for your workflow
```

### Step 3: Add Metadata

**Every template file needs YAML frontmatter:**

```yaml
---
description: [What this template provides]
globs: [File patterns where this applies]
tags: [Relevant, categorization, tags]
priority: [1-10, lower = higher priority]
version: [Semantic version]
source: [Original project if applicable]
---
```

**Example:**
```yaml
---
description: Git workflow standards including commit messages and branch management
globs: "**/*"
tags: [development, git, workflow, commit, branch]
priority: 3
version: 1.0.0
source: DocOriginSmokeTestScripts - COMMIT_RULES_EXTRACTION_20251026.md
---
```

### Step 4: Structure the Template

**Standard template structure:**

```markdown
# [Template Title]

## Overview
[Brief description of what this template provides]

## When to Use
[Scenarios where this template is appropriate]

## Quick Start
[Minimal steps to get started]

## Detailed Guide
[Comprehensive implementation instructions]

## Customization Points
[What needs to be adapted for specific projects]

## Examples
[Multiple concrete examples]

## Validation
[How to verify correct implementation]

## Troubleshooting
[Common issues and solutions]

## Related
[Links to related templates and resources]
```

### Step 5: Provide Concrete Examples

**Always include multiple examples:**

**Bad (Abstract):**
```markdown
Use descriptive commit messages that explain what changed.
```

**Good (Concrete):**
```markdown
## Commit Message Examples

### Feature Addition
\`\`\`bash
PROJ-1234 -feature [API] Add user authentication with JWT tokens

- Implemented JWT token generation and validation
- Added user login and registration endpoints
- Created middleware for token verification
\`\`\`

### Bug Fix
\`\`\`bash
PROJ-4567 -bugfix [Frontend] Resolve memory leak in data table

- Fixed event listener cleanup in component unmount
- Optimized data rendering for large datasets
\`\`\`

### Documentation Update
\`\`\`bash
PROJ-7890 -documentation [Documentation] Add API integration guide

- Created step-by-step integration tutorials
- Added code examples for common use cases
\`\`\`
```

### Step 6: Document Customization

**Make customization explicit:**

```markdown
## Customization Guide

### Required Changes
1. **Project Key**: Replace `PROJ` with your project identifier
   - JIRA: Use project key (e.g., `TEAM`, `APP`)
   - GitHub: Use `#[NUMBER]` format
   - No tracker: Use descriptive branch names

2. **Component Categories**: Adjust for your architecture
   - Current: API, Frontend, Database, Documentation
   - Add your components: Mobile, Infrastructure, etc.

3. **Commit Types**: Modify for your workflow
   - Current: feature, bugfix, documentation, test, refactor
   - Add your types: hotfix, release, etc.

### Optional Changes
- Branch naming format
- Commit message structure
- Validation rules

### Example Customization
\`\`\`bash
# Template default
PROJ-1234 -feature [API] Add authentication

# Customized for your project
MYAPP-1234 -feature [Backend] Add authentication
\`\`\`
```

### Step 7: Add Implementation Scripts

**Provide ready-to-use scripts:**

```markdown
## Implementation Scripts

### Setup Script

**File:** `scripts/setup-git-workflow.sh`

\`\`\`bash
#!/bin/bash
# Setup git workflow standards

# Create commit-msg hook
cat > .git/hooks/commit-msg << 'EOF'
#!/bin/sh
commit_regex="^[A-Z]+-[0-9]+ -[a-z]+ \[.*\] .*"
if ! grep -qE "$commit_regex" "$1"; then
    echo "❌ Invalid commit message format!"
    exit 1
fi
EOF

chmod +x .git/hooks/commit-msg
echo "✅ Git workflow setup complete"
\`\`\`

### Usage
\`\`\`bash
bash scripts/setup-git-workflow.sh
\`\`\`
```

### Step 8: Include Validation

**Help users verify correct implementation:**

```markdown
## Validation Checklist

### Immediate Validation
- [ ] Commit message hook is installed
- [ ] Test commit passes validation
- [ ] Branch naming follows format
- [ ] Team understands standards

### Ongoing Validation
- [ ] All commits follow format (check weekly)
- [ ] PR reviews verify compliance
- [ ] New team members trained
- [ ] Standards updated as needed

### Automated Validation
\`\`\`yaml
# .github/workflows/validate-commits.yml
name: Validate Commits
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Validate Commit Messages
        run: |
          # Add validation script here
\`\`\`
```

## Template Types

### 1. Rule Templates

**Purpose:** Define standards and guidelines

**Structure:**
- Clear rules and requirements
- Rationale for each rule
- Examples of compliance
- Anti-patterns to avoid

**Example:** Git workflow standards, code style guidelines

### 2. Process Templates

**Purpose:** Document workflows and procedures

**Structure:**
- Step-by-step instructions
- Decision points and criteria
- Tools and automation
- Success metrics

**Example:** CI/CD pipeline, release process

### 3. Configuration Templates

**Purpose:** Provide ready-to-use configuration files

**Structure:**
- Complete configuration file
- Comments explaining each section
- Customization instructions
- Validation steps

**Example:** `.pre-commit-config.yaml`, `tsconfig.json`

### 4. Persona Templates

**Purpose:** Define AI assistant personas

**Structure:**
- Role description
- Responsibilities
- Communication style
- Domain expertise
- Example interactions

**Example:** Developer persona, Architect persona

### 5. Documentation Templates

**Purpose:** Standardize documentation structure

**Structure:**
- Required sections
- Optional sections
- Examples for each section
- Formatting guidelines

**Example:** README template, API doc template

## Quality Standards

### Template Quality Checklist

- [ ] **Portable:** Works without project-specific dependencies
- [ ] **Complete:** All necessary information included
- [ ] **Clear:** Easy to understand and follow
- [ ] **Concrete:** Multiple working examples provided
- [ ] **Customizable:** Clear customization points documented
- [ ] **Validated:** Tested with at least 2 projects
- [ ] **Versioned:** Semantic version and changelog
- [ ] **Maintained:** Owner and review cycle defined
- [ ] **Metadata:** Complete YAML frontmatter
- [ ] **Structured:** Follows standard template structure

### Documentation Quality

- [ ] **Rationale:** Explains "why" not just "what"
- [ ] **Examples:** Concrete examples for all features
- [ ] **Customization:** Clear guidance for adaptation
- [ ] **Validation:** How to verify correct implementation
- [ ] **Troubleshooting:** Common issues and solutions
- [ ] **Related:** Links to related templates and resources

## Best Practices

### Do's ✅

1. **Start with proven patterns** from successful projects
2. **Generalize gradually** - don't over-abstract too early
3. **Test thoroughly** with multiple project types
4. **Gather feedback** from actual users
5. **Iterate based on usage** - templates evolve
6. **Document rationale** - explain why, not just what
7. **Provide multiple examples** - cover different scenarios
8. **Make customization explicit** - mark what needs changing
9. **Include validation** - help users verify correctness
10. **Version properly** - track evolution over time

### Don'ts ❌

1. **Don't create templates prematurely** - need 2+ projects
2. **Don't over-generalize** - maintain practical utility
3. **Don't skip examples** - abstract rules aren't enough
4. **Don't ignore feedback** - users know what works
5. **Don't hardcode specifics** - use placeholders
6. **Don't assume context** - make everything explicit
7. **Don't skip validation** - help users succeed
8. **Don't forget maintenance** - templates need updates
9. **Don't create monoliths** - keep templates focused
10. **Don't skip metadata** - YAML frontmatter is required

## Template Lifecycle

### Creation

1. Identify pattern in 2+ projects
2. Extract and generalize
3. Add metadata and structure
4. Provide examples and customization
5. Test with new project
6. Gather initial feedback
7. Publish v1.0.0

### Maintenance

1. Monitor usage and feedback
2. Identify improvement opportunities
3. Update based on learnings
4. Test changes
5. Publish new version
6. Update changelog
7. Notify users of changes

### Evolution

```markdown
## Version History

### v1.0.0 (2025-10-27)
- Initial release
- Basic git workflow standards
- Commit message format
- Branch naming conventions

### v1.1.0 (2025-11-15)
- Added: PR template
- Added: Branch version management script
- Improved: Customization guidance

### v2.0.0 (2025-12-01)
- Breaking: Changed commit message format
- Added: Pre-commit hooks
- Added: Automated validation
- Migration guide provided
```

## Validation and Testing

### Pre-Publication Testing

1. **Syntax validation:** All code examples work
2. **Portability testing:** Works in different projects
3. **Customization testing:** Customization points work
4. **Documentation review:** Clear and complete
5. **Peer review:** Another developer can use it
6. **Feedback incorporation:** Address review comments

### Post-Publication Monitoring

1. **Usage tracking:** How many projects adopt?
2. **Feedback collection:** What works/doesn't work?
3. **Issue tracking:** Common problems?
4. **Success metrics:** Does it improve outcomes?
5. **Iteration planning:** What needs improvement?

---

**Last Updated:** 2025-10-27  
**Version:** 1.0.0  
**Maintained By:** AI Research Team  
**Review Cycle:** Quarterly
