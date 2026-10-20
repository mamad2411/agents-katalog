---
description: Priority system standards for Cursor rules - 3-tier classification
alwaysApply: false
tags: [critical, priority, standards, classification]
priority: 1
version: 1.0.0
---

# Priority System Standards

**3-tier priority classification for Cursor rules.**

---

## Core Principle

**All rules MUST use a 3-tier priority system (1-3) to enable efficient context management and selective loading.**

---

## Priority Levels

### Priority 1: CRITICAL (Always Load)

**Definition:** Foundational rules that MUST be loaded in every context.

**Characteristics:**
- Core AI behavior standards
- Critical workflow rules
- Always-apply rules (`alwaysApply: true`)
- Non-negotiable standards
- Frequently referenced across all tasks

**Examples:**
- `ai-behavior-standards.mdc` (factual communication)
- `agentic-ai-implementation.mdc` (timeline estimation)
- `analysis-output-conventions.mdc` (output location)
- `audit-log.mdc` (interaction logging)
- `python-command-windows.mdc` (Windows compatibility)
- `terminal-automation.mdc` (command execution)

**Usage:** ~10-15 rules maximum
**Always Apply:** Most Priority 1 rules should have `alwaysApply: true`

---

### Priority 2: IMPORTANT (Load by Task)

**Definition:** Important rules loaded based on task context (documentation, development, testing).

**Characteristics:**
- Task-specific guidance
- Frequently used patterns
- Domain-specific rules
- Persona-specific rules
- Workflow standards

**Examples:**
- `documentation-naming-conventions.mdc`
- `analysis-methodology-and-standards.mdc`
- `progress-reporting.mdc`
- `git-workflow.mdc`
- `code-style.mdc`
- `testing.mdc`
- All persona files (persona-developer, persona-qa-engineer, etc.)

**Usage:** ~30-40 rules
**Always Apply:** Typically `alwaysApply: false`, loaded on-demand

---

### Priority 3: OPTIONAL (Load on Specific Need)

**Definition:** Specialized rules for specific scenarios, reference documents, or rare use cases.

**Characteristics:**
- Rarely used rules
- Highly specialized scenarios
- Reference documents
- Template-specific guidance
- Project-specific rules

**Examples:**
- `mermaid-diagram-syntax-rules.mdc` (only when creating diagrams)
- `jira-integration-best-practices.mdc` (only when using JIRA)
- `[project-name]-testing-requirements.mdc` (project-specific)
- `template-generation.mdc` (template repo specific)
- `terminology-standards.mdc` (reference document)
- Specialized persona rules

**Usage:** ~10-20 rules
**Always Apply:** Always `alwaysApply: false`, loaded only when explicitly needed

---

## Priority Assignment Guidelines

### Assign Priority 1 When

- [ ] Rule affects ALL AI responses (behavior standards)
- [ ] Rule prevents critical errors (command syntax, file operations)
- [ ] Rule is referenced by >50% of other rules
- [ ] Violation causes immediate failure
- [ ] Rule is foundational to workflow

### Assign Priority 2 When

- [ ] Rule is task-specific (dev, docs, testing)
- [ ] Rule is frequently used (>30% of tasks)
- [ ] Rule defines important patterns or standards
- [ ] Persona-specific guidance
- [ ] Domain-specific workflow

### Assign Priority 3 When

- [ ] Rule is rarely used (<10% of tasks)
- [ ] Rule is highly specialized (specific tools, integrations)
- [ ] Rule is reference-only (glossaries, examples)
- [ ] Rule is project-specific
- [ ] Rule is template repository-specific

---

## Priority Distribution Target

**Target distribution for optimal context usage:**

| Priority | Count | % of Total | Context Budget |
|----------|-------|------------|----------------|
| Priority 1 | 10-15 | 15-20% | Always loaded (~25K tokens) |
| Priority 2 | 30-40 | 50-60% | Load by task (~75K tokens) |
| Priority 3 | 10-20 | 15-25% | Load on-demand (~25K tokens) |
| **TOTAL** | **50-75** | **100%** | **~125K tokens max** |

**Current Status (Post-Consolidation):**
- Total rules: ~60 files
- Priority 1: 11 files (~18%)
- Priority 2: 10 files (~17%)
- Priority 3: 2 files (~3%)
- Unassigned: ~37 files (~62%)

**Action Required:** Assign priorities to unassigned rules based on guidelines above.

---

## Implementation Rules

### For New Rules

**When creating a new rule:**
1. Determine priority using guidelines above
2. Set `priority: 1|2|3` in frontmatter
3. Set `alwaysApply: true` only for Priority 1 rules
4. Document why this priority was chosen

**Example Frontmatter:**
```yaml
---
description: Rule description
alwaysApply: true  # Only for Priority 1
tags: [category, tags]
priority: 1        # Critical rule
version: 1.0.0
---
```

### For Existing Rules

**When updating existing rules:**
1. Review current priority (if set)
2. Validate against guidelines
3. Update if priority is incorrect
4. Document change in version history

---

## Priority Migration Strategy

### Phase 1: Critical Rules (Priority 1)
- Audit all `alwaysApply: true` rules
- Ensure all Priority 1 rules have `alwaysApply: true`
- Target: 10-15 rules maximum

### Phase 2: Important Rules (Priority 2)
- Identify frequently-used task-specific rules
- Assign Priority 2 to documentation, development, testing rules
- Assign Priority 2 to all persona files

### Phase 3: Optional Rules (Priority 3)
- Identify rarely-used specialized rules
- Assign Priority 3 to project-specific and template-specific rules
- Assign Priority 3 to reference documents

---

## Verification Checklist

Before finalizing rule priorities:

- [ ] Total Priority 1 rules ≤ 15
- [ ] All Priority 1 rules have `alwaysApply: true`
- [ ] Priority 2 rules cover main task categories
- [ ] Priority 3 rules are truly optional/specialized
- [ ] No critical rules assigned Priority 3
- [ ] No rarely-used rules assigned Priority 1

---

## Examples by Category

### Priority 1 Examples (CRITICAL)
```
.cursor/rules/00-critical/
├── agentic-ai-implementation.mdc (priority: 1, alwaysApply: true)
├── ai-behavior-standards.mdc (priority: 1, alwaysApply: true)
├── audit-log.mdc (priority: 1, alwaysApply: true)
└── python-command-windows.mdc (priority: 1, alwaysApply: true)
```

### Priority 2 Examples (IMPORTANT)
```
.cursor/rules/documentation/
├── documentation-naming-conventions.mdc (priority: 2, alwaysApply: false)
├── progress-reporting.mdc (priority: 2, alwaysApply: true)

.cursor/rules/development/
├── code-style.mdc (priority: 2, alwaysApply: false)
├── git-workflow.mdc (priority: 2, alwaysApply: false)

.cursor/rules/personas/
├── persona-developer.mdc (priority: 2, alwaysApply: false)
```

### Priority 3 Examples (OPTIONAL)
```
.cursor/rules/documentation/
├── mermaid-diagram-syntax-rules.mdc (priority: 3, alwaysApply: false)

.cursor/rules/integrations/
├── jira-integration-best-practices.mdc (priority: 3, alwaysApply: false)

.cursor/rules/testing/
├── [project-name]-testing-requirements.mdc (priority: 3, alwaysApply: false)
```

---

## Remember

✅ **Priority 1** = Critical, always load, `alwaysApply: true`
✅ **Priority 2** = Important, load by task, `alwaysApply: false`
✅ **Priority 3** = Optional, load on-demand, `alwaysApply: false`
✅ **Keep Priority 1 lean** - Maximum 15 rules
✅ **Most rules are Priority 2** - 50-60% of total

---

**Version:** 1.0.0  
**Last Updated:** 2025-11-17  
**Status:** ACTIVE  
**Priority:** 1 (this document is Priority 1)  
**Always Apply:** false (reference document)
