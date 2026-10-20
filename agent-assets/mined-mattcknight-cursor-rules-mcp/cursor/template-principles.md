---
description: Core principles for template design and generation
globs: "**/*"
tags: [core, templates, principles, design]
priority: 2
version: 1.0.0
---

# Template Design Principles

## Overview

This document defines the core principles for creating reusable `.cursor/rules` templates that can be adopted by other development teams.

## Core Principles

### 1. Portability First

**Templates must work across different projects without modification.**

- ✅ Use generic terminology (avoid project-specific names)
- ✅ Provide clear customization points
- ✅ Include examples for common scenarios
- ✅ Document assumptions explicitly

**Example:**
```markdown
# Replace [PROJECT_KEY] with your JIRA project key
PROJ-1234 -feature [Component] Description

# For projects without JIRA:
feature/user-authentication-[initials]
```

### 2. Self-Contained Documentation

**Each template should be fully self-contained.**

- ✅ Include all necessary context within the template
- ✅ No external dependencies for understanding
- ✅ Provide implementation guidance
- ✅ Include troubleshooting tips

### 3. Progressive Disclosure

**Start simple, reveal complexity as needed.**

- ✅ Basic usage should be immediately clear
- ✅ Advanced features documented separately
- ✅ Quick-start guides for common use cases
- ✅ Deep-dive sections for complex scenarios

### 4. Concrete Examples

**Always provide working examples.**

- ✅ Real-world scenarios, not abstract concepts
- ✅ Before/after comparisons
- ✅ Common mistakes and how to avoid them
- ✅ Multiple examples for different contexts

### 5. Explain the "Why"

**Document rationale, not just rules.**

- ✅ Explain why a rule exists
- ✅ Describe the problem it solves
- ✅ Provide context for decisions
- ✅ Link to related best practices

### 6. Modular Architecture

**Templates should be composable.**

- ✅ Use `.mdc` files with `@import` support
- ✅ Organize by functional area
- ✅ Enable/disable modules independently
- ✅ Support customization without forking

### 7. Version Control

**Track template evolution.**

- ✅ Use semantic versioning
- ✅ Document changes in changelog
- ✅ Maintain backward compatibility when possible
- ✅ Provide migration guides for breaking changes

### 8. Metadata-Driven

**Use YAML frontmatter for configuration.**

- ✅ Description of file purpose
- ✅ Applicable file patterns (globs)
- ✅ Tags for categorization
- ✅ Priority for loading order
- ✅ Version tracking

**Example:**
```yaml
---
description: Git workflow standards
globs: ["**/*.py", "**/*.js"]
tags: [development, git, workflow]
priority: 2
version: 1.0.0
---
```

## Template Structure Standards

### Directory Organization

```
.cursor/
├── rules.mdc                    # Main entry point
└── rules/
    ├── 00-critical/            # Critical rules (priority 1)
    ├── core/                   # Core project rules (priority 2)
    ├── development/            # Development standards (priority 3)
    ├── documentation/          # Documentation standards (priority 4)
    ├── ai-guidelines/          # AI-specific guidance (priority 5)
    ├── personas/               # Persona definitions (priority 6)
    ├── integrations/           # External integrations (priority 7)
    └── templates/              # Template-specific rules (priority 8)
```

### File Naming Conventions

- **Use descriptive names:** `git-workflow.mdc` not `git.mdc`
- **Use kebab-case:** `code-style.mdc` not `CodeStyle.mdc`
- **Group related files:** `jira-integration.mdc`, `jira-worklog.mdc`
- **Number for priority:** `00-critical/`, `10-code-style.mdc`

### Main Entry Point Pattern

```markdown
---
description: Main Cursor rules configuration
globs: "**/*"
tags: [main, configuration]
priority: 1
version: 2.0.0
---

# Main Cursor Rules Configuration

## CRITICAL RULES
@import ./rules/00-critical/meta-project-purpose.mdc

## Core Rules
@import ./rules/core/project-overview.mdc
@import ./rules/core/template-principles.mdc

## Development Standards
@import ./rules/development/code-style.mdc
@import ./rules/development/git-workflow.mdc

## Personas
@import ./rules/personas/persona-developer.mdc
```

## Customization Guidance

### For Template Users

1. **Copy the template** to your project's `.cursor/` directory
2. **Review `rules.mdc`** and enable/disable modules as needed
3. **Customize project-specific values:**
   - Project name
   - JIRA project key
   - Technology stack
   - Team conventions
4. **Add project-specific rules** to appropriate directories
5. **Update metadata** (version, last updated, maintainer)

### For Template Creators

1. **Start with existing templates** when possible
2. **Extract common patterns** from multiple projects
3. **Generalize project-specific details**
4. **Document customization points** clearly
5. **Test with multiple projects** before publishing
6. **Gather feedback** and iterate

## Quality Checklist

Before publishing a template, verify:

- [ ] **Portability:** Works without project-specific dependencies
- [ ] **Documentation:** All sections are clear and complete
- [ ] **Examples:** Concrete examples for all major features
- [ ] **Metadata:** YAML frontmatter is complete and accurate
- [ ] **Structure:** Follows recommended directory organization
- [ ] **Versioning:** Version number and changelog are current
- [ ] **Testing:** Tested with at least 2 different project types
- [ ] **Customization:** Clear guidance for adaptation
- [ ] **Rationale:** "Why" is documented, not just "what"
- [ ] **Maintenance:** Owner and update schedule defined

## Anti-Patterns to Avoid

### ❌ Don't: Hardcode Project-Specific Values

```markdown
# Bad
CLAIMSPAY-1234 -feature [API] Description
```

```markdown
# Good
[PROJECT_KEY]-1234 -feature [Component] Description
# Replace [PROJECT_KEY] with your JIRA project key (e.g., PROJ, TEAM, etc.)
```

### ❌ Don't: Assume Specific Tools or Technologies

```markdown
# Bad
Run: npm install pre-commit
```

```markdown
# Good
# For Node.js projects:
npm install pre-commit

# For Python projects:
pip install pre-commit

# For other projects, see: https://pre-commit.com/#install
```

### ❌ Don't: Create Monolithic Files

```markdown
# Bad: Single 3000-line rules.md file
```

```markdown
# Good: Modular structure with @import
@import ./rules/development/git-workflow.mdc
@import ./rules/development/code-style.mdc
```

### ❌ Don't: Skip the "Why"

```markdown
# Bad
Use semantic versioning.
```

```markdown
# Good
Use semantic versioning to track template evolution and enable users to:
- Understand breaking vs. non-breaking changes
- Safely upgrade templates
- Reference specific versions in documentation
```

## Template Validation

### Automated Checks

Create validation scripts to verify:

1. **File structure** matches expected layout
2. **Metadata** is present and valid
3. **@import paths** resolve correctly
4. **Examples** are syntactically correct
5. **Links** are not broken

### Manual Review

Have another developer:

1. **Try to use the template** without guidance
2. **Identify unclear sections**
3. **Test customization points**
4. **Verify examples work**
5. **Provide feedback**

## Continuous Improvement

### Feedback Loop

1. **Collect usage data** from teams using templates
2. **Gather feedback** on pain points
3. **Identify common customizations**
4. **Update templates** based on learnings
5. **Publish new versions** with improvements

### Evolution Strategy

- **Minor updates** (1.x.y): Clarifications, examples, bug fixes
- **Feature additions** (1.x.0): New optional modules, enhanced guidance
- **Breaking changes** (2.0.0): Structural changes, removed features

---

**Last Updated:** 2025-10-27  
**Version:** 1.0.0  
**Maintained By:** AI Research Team  
**Review Cycle:** Quarterly
