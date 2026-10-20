---
description: Comprehensive documentation naming conventions - plans, requirements, recommendations, presentations
alwaysApply: false
tags: [documentation, file-naming, conventions, timestamp, versioning]
priority: 2
version: 2.0.0
consolidatedFrom: [plan-file-management.mdc, questions-and-decisions-file-naming.mdc, recommendation-file-management.mdc, presentation-document-versioning.mdc]
---

# Documentation Naming Conventions

**Consolidated documentation file naming rules across all document types.**

---

## Core Principle

**ALL documentation files MUST follow standardized timestamp and naming patterns for consistency, traceability, and organization.**

---

## Standard Timestamp Format

**Format:** `YYYYMMDD_HHMMSS` (24-hour format, ISO 8601 style)

**Examples:**
- `20251117_143522` (November 17, 2025 at 2:35:22 PM)
- `20251201_093000` (December 1, 2025 at 9:30:00 AM)

**Rules:**
- ✅ Use current date/time when creating file
- ✅ Use 24-hour format (00-23 for hours)
- ✅ No spaces, hyphens, or colons in timestamp
- ❌ Never use `YYYY-MM-DD HH:MM:SS` format (incompatible with filesystems)

---

## 1. Plan Files

### Directory Structure

```
docs/plans/YYYYMMDD_HHMMSS_[plan-name]/
└── plan.md
```

### Rules

- **Location:** `docs/plans/` directory
- **Directory Naming:** Timestamp + descriptive name (kebab-case or snake_case)
- **File Name:** Always `plan.md` inside directory
- **Use Cases:** Implementation plans, project plans, feature plans, phase plans

### Examples

```
docs/plans/20251112_141722_bank_name_matching_poc_architecture/
└── plan.md

docs/plans/20250122_140836_feature_implementation_plan/
└── plan.md

docs/plans/20251117_115500_rules_consolidation/
└── plan.md
```

### Mandatory Sections

All plan files MUST include:
1. **Metadata:** Title, date, status, version
2. **Overview/Summary:** Brief description
3. **Goals/Objectives:** What to achieve
4. **Implementation Steps/Phases:** How to execute
5. **Deliverables:** What will be produced
6. **Success Criteria:** How to measure completion
7. **Version History:** Track changes

---

## 2. Questions and Decisions Files

### File Naming Format

```
docs/requirements/YYYYMMDD_HHMMSS_questions-and-decisions-[descriptor].md
```

### Rules

- **Location:** `docs/requirements/` directory
- **Prefix:** Always `questions-and-decisions`
- **Descriptor:** Brief scope description (kebab-case)
- **Use Cases:** Decision records, requirement clarifications, option evaluations

### Examples

```
docs/requirements/20251114_143000_questions-and-decisions-testing-framework.md
docs/requirements/20251114_035000_questions-and-decisions-v1.8.0-data-seeder-fixes.md
docs/requirements/20251112_141722_questions-and-decisions-poc-architecture.md
docs/requirements/20251117_112408_questions-and-decisions-rules-optimization.md
```

### Mandatory Sections

All questions-and-decisions files MUST include:
1. **Metadata:** Date, status, decision owner
2. **Context:** Background and scope
3. **Questions:** Numbered list of questions
4. **Options:** Lettered options for each question (a, b, c, d)
5. **Recommendations:** Suggested option with rationale
6. **Decisions:** User-confirmed answers (format: `[a]`, `[b]`, etc.)
7. **Summary:** Decision matrix or summary table

### Question Format Rules

**Question Structure:**
- Maximum 200 characters per question
- Clear, specific, actionable
- Numbered list format (Q1, Q2, Q3...)

**Answer Options:**
- Lettered options (a, b, c, d)
- First option is default/recommendation
- Each option has description and trade-offs

**Decision Format:**
- `**Decision:** [a]` - User confirmed option A
- `**Decision:** [b, c]` - User confirmed multiple options
- `**Decision:** [PENDING]` - Awaiting user confirmation

---

## 3. Recommendation Files

### File Naming Format

```
docs/recommendations/YYYYMMDD_HHMMSS_[Title-Of-Recommendation].md
```

### Rules

- **Location:** `docs/recommendations/` directory
- **Timestamp:** Current date/time when created
- **Title:** Descriptive, kebab-case or Title_Case with underscores
- **Use Cases:** Analysis recommendations, best practices, improvement proposals

### Examples

```
docs/recommendations/20251117_171500_persona_updates_for_clean_architecture.md
docs/recommendations/20251022_212900_Rules_Consolidation_Analysis.md
docs/recommendations/20251023_091500_Database_Optimization_Strategy.md
docs/recommendations/20251117_112408_cursor_rules_consolidation_plan.md
```

### Mandatory Sections

All recommendation files MUST include:
1. **Metadata:** Date, purpose, status, version
2. **Context/Background:** Why recommendations are needed
3. **Current State Analysis:** What exists today
4. **Recommendations:** Specific, actionable suggestions
5. **Rationale:** Why each recommendation is important
6. **Implementation Plan:** How to apply (if applicable)
7. **Expected Outcomes:** Benefits and impacts

### Triggers for Creating Recommendations

**User requests:**
- "prepare recommendations"
- "provide recommendations"
- "analyze and recommend"
- "evaluate and suggest"
- Any variation requesting analysis with suggestions

**ALWAYS create a permanent recommendation file when user requests recommendations.**

---

## 4. Presentation Documents

### File Naming Format

```
[document-name]-v[VERSION].presentation.md
```

### Rules

- **Suffix:** Always `.presentation.md`
- **Version:** Semantic versioning (MAJOR.MINOR.PATCH)
- **Use Cases:** Solution architecture, technical design, formal documents
- **Audience:** Stakeholders, reviewers, formal presentations

### Examples

```
solution-architecture-v2.2.0.presentation.md
technical-design-v1.5.0.presentation.md
implementation-spec-v3.0.0.presentation.md
[project-name]-analysis-v1.0.0.presentation.md
```

### Semantic Versioning Rules

**Version Format:** `vMAJOR.MINOR.PATCH`

#### Major Version (X.0.0) - Increment when:
- Architecture changes (new/removed components)
- Technology stack changes
- Significant content restructuring
- Breaking changes
- Scope changes
- Format changes (e.g., from TDD to SA)

#### Minor Version (X.Y.0) - Increment when:
- New sections added
- Additional diagrams/visualizations
- Enhanced explanations
- New examples or use cases
- Clarifications that don't change meaning
- Non-breaking content additions

#### Patch Version (X.Y.Z) - Increment when:
- Typo fixes
- Grammar corrections
- Formatting improvements
- Link updates
- Minor wording changes
- Metadata updates

### Document Version Must Match Git Tag

**CRITICAL RULE:** Presentation document version MUST match git tag version for that release.

**Examples:**
- Git tag: `v2.2.0` → Document version: `2.2.0`
- Git tag: `v3.0.0` → Document version: `3.0.0`

**File Naming (Formal Approach - v2.2.0 onwards):**
- File name AND internal version BOTH match git tag
- File name: `solution-architecture-v2.2.0.presentation.md`
- Version inside: `2.2.0`

### Mandatory Sections

All presentation documents MUST include:
1. **Document Header:** Title, version, date, status, authors
2. **Document History:** Version history table
3. **Table of Contents:** Section navigation
4. **Executive Summary:** High-level overview
5. **Main Content:** Detailed sections
6. **Diagrams:** Visual representations (Mermaid preferred)
7. **Glossary:** Key terms and acronyms (if applicable)
8. **References:** Sources and related documents

---

## 5. Specification Documents

### File Naming Format

```
[document-name]-v[VERSION].spec.md
```

### Rules

- **Suffix:** Always `.spec.md`
- **Version:** Semantic versioning
- **Use Cases:** API specs, implementation specs, technical specifications
- **Audience:** Developers, implementers, technical reviewers

### Examples

```
api-specification-v1.2.0.spec.md
implementation-spec-v2.0.0.spec.md
database-schema-v3.1.0.spec.md
```

### Differentiation: `.spec.md` vs `.presentation.md`

**Use `.spec.md` when:**
- Document contains implementation details
- Audience is primarily developers
- Focus is on HOW to implement
- Contains code samples, API contracts, schemas

**Use `.presentation.md` when:**
- Document is for stakeholder review
- Audience includes non-technical stakeholders
- Focus is on WHAT and WHY
- Contains high-level architecture, business context

**See:** `spec-vs-presentation-file-pattern.mdc` for detailed differentiation rules.

---

## 6. General Documentation Files

### File Naming Format

```
docs/[category]/YYYYMMDD_HHMMSS_[descriptive-name].md
```

### Common Categories

- `docs/learnings/` - Lessons learned, post-mortems, insights
- `docs/analysis/` - Analysis documents, evaluations
- `docs/proposals/` - Feature proposals, RFC documents
- `docs/guides/` - How-to guides, tutorials
- `docs/progress_reports/` - Progress tracking, status updates

### Rules

- ✅ Use timestamp prefix for traceability
- ✅ Use descriptive names (kebab-case)
- ✅ Categorize appropriately
- ❌ Avoid generic names like "document.md" or "file.md"

---

## File Naming Checklist

Before creating ANY documentation file, verify:

- [ ] Correct directory (`docs/plans/`, `docs/requirements/`, `docs/recommendations/`)
- [ ] Timestamp format: `YYYYMMDD_HHMMSS` (no spaces, hyphens in timestamp)
- [ ] Descriptive name (not generic)
- [ ] Appropriate suffix (`.md`, `.presentation.md`, `.spec.md`)
- [ ] Version number (for presentation/spec documents)
- [ ] Required sections included
- [ ] Frontmatter metadata complete

---

## Cross-References

**Related Rules:**
- `spec-vs-presentation-file-pattern.mdc` - Specification vs presentation differentiation
- `document-version-matches-git-tag.mdc` - Version and git tag alignment
- `clear-documentation-principles.mdc` - Documentation quality principles
- `table-of-contents-requirement.mdc` - TOC requirements for long documents

---

## Examples by Use Case

### Use Case: New Feature Implementation

1. **Questions:** `docs/requirements/20251117_140000_questions-and-decisions-feature-x.md`
2. **Plan:** `docs/plans/20251117_140500_feature-x-implementation/plan.md`
3. **Recommendations:** `docs/recommendations/20251117_141000_feature-x-best-practices.md`
4. **Specification:** `feature-x-spec-v1.0.0.spec.md`

### Use Case: Architecture Design

1. **Questions:** `docs/requirements/20251117_140000_questions-and-decisions-architecture.md`
2. **Recommendations:** `docs/recommendations/20251117_141000_architecture-options-analysis.md`
3. **Presentation:** `solution-architecture-v1.0.0.presentation.md`
4. **Technical Design:** `technical-design-v1.0.0.presentation.md`

### Use Case: Code Analysis

1. **Analysis:** `docs/analysis/20251117_140000_codebase-analysis.md`
2. **Recommendations:** `docs/recommendations/20251117_141000_refactoring-recommendations.md`
3. **Plan:** `docs/plans/20251117_142000_refactoring-plan/plan.md`

---

## Remember

✅ **Consistency** - Use standard formats across all documents
✅ **Traceability** - Timestamps enable historical tracking
✅ **Clarity** - Descriptive names communicate purpose
✅ **Version Control** - Semantic versioning for formal documents
✅ **Organization** - Proper categorization in directory structure

---

**Version:** 2.0.0  
**Last Updated:** 2025-11-17  
**Consolidation:** Merged 4 files (plan-file-management, questions-and-decisions-file-naming, recommendation-file-management, presentation-document-versioning)  
**Savings:** -3 files, ~15 KB, ~3,750 tokens
