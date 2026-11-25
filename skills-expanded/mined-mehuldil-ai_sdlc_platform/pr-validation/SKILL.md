---
name: pr-validation
description: Validate PR structure, naming, metadata, and file location conventions
model: sonnet-4-6
token_budget: {input: 4000, output: 2000}
---

# PR Validation Skill

Validates pull request submissions against file structure, naming conventions, and metadata requirements.

---

## Validation Dimensions

### 1. Type Detection
- Identify change type: RULE, AGENT, SKILL, STAGE, TEMPLATE, STACK, or WORKFLOW
- Determine operation: NEW, MODIFY, REMOVE, REFACTOR, CONSOLIDATE
- Verify appropriate scope (new vs modification)

### 2. File Location & Naming
- [ ] File in correct directory for type (rules/ vs stacks/*/rules/, skills/role/, agents/role/, etc.)
- [ ] Kebab-case file naming (my-file-name.md, not my_file_name or MyFileName)
- [ ] Title Case headers (#, ##, ###, etc.)
- [ ] Correct file extension (.md for most, .json for configs)

### 3. Required Metadata
- [ ] YAML frontmatter present (for skills/agents)
- [ ] name, description, model fields present
- [ ] token_budget specified (input and output)
- [ ] No hardcoded absolute paths
- [ ] No embedded API keys, tokens, or secrets

### 4. Content Structure
- [ ] Required sections present for file type
- [ ] All sections properly formatted with headers
- [ ] Examples included (for rules, agents, skills)
- [ ] Cross-references use relative paths only
- [ ] Images/assets properly linked

### 5. Quality Checks
- [ ] Line count reasonable for type (rules: <100, agents: <150, skills: <200)
- [ ] No typos or grammar errors
- [ ] Markdown formatting correct (lists, tables, code blocks)
- [ ] Consistent language style (formal, technical, clear)
- [ ] No forbidden patterns (hardcoded configs, absolute paths, secrets)

---

## Validation Report Format

```markdown
## PR VALIDATION REPORT
PR Title: {title}
PR Type: [RULE / AGENT / SKILL / STAGE / TEMPLATE / STACK / WORKFLOW / OTHER]
Change Type: [NEW / MODIFY / REFACTOR / REMOVE / CONSOLIDATE]

### Type & Location
Status: [PASS / WARN / FAIL]
Details: {Specific checks for file location and naming}

### Guideline Compliance
Status: [PASS / WARN / FAIL]
Issues Found:
- {Issue 1 with details}
- {Issue 2 with details}
Required Fixes:
- {Fix 1}

### Quality Check
Issues:
- {Typos, formatting, clarity issues}

## Recommendations
### What to Fix (MUST FIX before merge)
1. {Issue with suggested fix}

### What to Improve (NICE TO HAVE)
1. {Improvement}
```

---

## Triggers

Use this skill when:
- PR submitted for structure/metadata validation
- Checking file location conventions
- Before passing to duplication or breaking-change analysis
- Validating formatting and naming consistency

---
