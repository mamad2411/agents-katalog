---
name: code-standards-check
description: Enforce coding standards, guidelines compliance, and language style consistency
model: sonnet-4-6
token_budget: {input: 4000, output: 2000}
---

# Code Standards Check Skill

Enforces platform coding standards, guideline compliance, and consistent language style across the repository.

---

## Standards Validation

### 1. Naming Conventions
- [ ] Kebab-case for files (my-file.md, not my_file or MyFile)
- [ ] Title Case for headers (# Proper Header)
- [ ] Consistent terminology across codebase
- [ ] No abbreviations without definition
- [ ] Function/variable names are descriptive

### 2. Structure & Format
- [ ] Proper Markdown formatting (lists, tables, code blocks)
- [ ] Tables use pipe syntax: | header | content |
- [ ] Code blocks use language tags (```markdown, ```json, ```bash)
- [ ] Consistent indentation (spaces, not tabs)
- [ ] Line length reasonable (< 120 chars preferred)

### 3. Content Organization
- [ ] Logical section ordering
- [ ] Clear hierarchy (h1 → h2 → h3)
- [ ] No orphaned sections
- [ ] Related content grouped together
- [ ] Examples provided for clarity

### 4. Cross-References
- [ ] All references use relative paths (not absolute)
- [ ] Links point to existing files
- [ ] No broken cross-references
- [ ] Clear reference text (not "see here")
- [ ] Consistent reference format

### 5. Language & Style
- [ ] Formal, technical tone
- [ ] Active voice preferred
- [ ] Clear, concise explanations
- [ ] No colloquialisms or slang
- [ ] Consistent terminology throughout

### 6. Forbidden Patterns
- [ ] No hardcoded values (use variables/configs)
- [ ] No absolute paths (/usr/local, C:\, etc.)
- [ ] No API keys, tokens, or credentials
- [ ] No sensitive information
- [ ] No external service dependencies in code examples

---

## Validation Checklist

- [ ] Naming conventions followed
- [ ] Markdown formatting correct
- [ ] All sections properly structured
- [ ] No typos or grammar errors
- [ ] Cross-references valid
- [ ] Language style consistent
- [ ] No forbidden patterns present
- [ ] Examples are accurate
- [ ] Links work and point to correct files
- [ ] Content is clear and complete

---

## Common Issues & Corrections

| Issue | Fix |
|-------|-----|
| File named MyFileName.md | Rename to my-file-name.md |
| Header in title case "# Proper Header" as "# proper header" | Use Title Case: # Proper Header |
| Absolute path /home/user/files | Use relative: ../files/ |
| API key in example | Remove, use {API_KEY} placeholder |
| Inconsistent section naming | Standardize terminology |
| Table without pipes \| | Use proper table syntax |
| Broken link to nonexistent file | Verify file exists or update link |
| Vague reference "see here" | Use descriptive text: "See Configuration section" |

---

## Triggers

Use this skill when:
- Validating PR for standards compliance
- After PR-validation passes
- Checking guideline adherence
- Before passing to duplication and impact analysis

---
