---
description: Documentation workflow standards - Markdown to HTML conversion, Mermaid diagrams, source of truth hierarchy
alwaysApply: false
tags: [documentation, workflow, html-conversion, mermaid, standards]
priority: 2
version: 1.0.0
---

# Documentation Workflow Standards

**Priority:** MEDIUM  
**Applies To:** All documentation creation and maintenance  
**Status:** RECOMMENDED

---

## Markdown to HTML Conversion

### When to Generate HTML

**ALWAYS generate HTML when creating/updating:**
- Solution Architecture documents (all variants)
- Technical Design documents (all variants)
- Implementation Specifications
- Any document with Mermaid diagrams
- Documents intended for stakeholder review
- User Stories, User Journeys, Acceptance Criteria

### How to Generate

**If you have conversion scripts:**

**OS Detection:** Use `py` on Windows, `python` or `python3` on Unix/Linux/Mac

```powershell
# Windows (PowerShell) - Presentation files (ALWAYS use this for .presentation.md files)
py scripts\convert_md_to_html_for_presentation.py docs\presentation\<file>.presentation.md docs\presentation\<file>.html

# Unix/Linux/Mac - Presentation files
python scripts/convert_md_to_html_for_presentation.py docs/presentation/<file>.presentation.md docs/presentation/<file>.html
# OR
python3 scripts/convert_md_to_html_for_presentation.py docs/presentation/<file>.presentation.md docs/presentation/<file>.html

# Note: Scripts should be copied from template projects (e.g., Zero Payment) or created as generic reusable scripts
# Scripts location: scripts/ folder at repository root
```

### Important Rules

- ✅ Generate HTML automatically after updating .md files
- ✅ Don't announce HTML generation to user (silent operation)
- ❌ NEVER add warning banners to generated documents
- ❌ NO operational metadata visible to stakeholders
- ✅ Keep documents clean and professional
- ✅ Regenerate ALL HTML files in batch if multiple markdown files updated

### When NOT to Generate HTML

- Internal documentation (README files in /docs)
- Configuration files
- Source of Truth documents (unless requested)
- TODO lists and session notes
- Learning documents (/docs/learnings/)
- Recommendation documents (/docs/recommendations/)

---

## Mermaid Diagrams

### Required Usage

**ALWAYS use Mermaid for:**
1. Flows (process, workflow, data flow)
2. Sequences (API interactions, method calls)
3. Architecture (components, layers, integrations)
4. State Machines (status transitions)
5. Entity Relationships (database schemas)
6. Class Diagrams (inheritance, structure)
7. Decision Trees (validation chains)

**NEVER use:**
- ❌ Text-based pseudo-diagrams with arrows (→, ↓)
- ❌ ASCII art diagrams
- ❌ Indented text to show hierarchy

### Syntax Rules

**❌ FORBIDDEN (Causes parsing errors):**
1. Emoji characters: ❌ ✅ ⚠️ 🔴 🟠 🟡 🟢 ⚪
2. Special Unicode quotes: " " ' '
3. Special angle brackets: <<abstract>> with Unicode

**✅ USE INSTEAD:**
1. Plain text: "REJECT:", "PASS:", "WARNING:", "ERROR:"
2. Standard ASCII quotes: " " ' '
3. Style for visual indicators:
   ```mermaid
   style ErrorNode fill:#ffebee,stroke:#c62828
   style SuccessNode fill:#e8f5e9,stroke:#2e7d32
   style WarningNode fill:#fff3e0,stroke:#f57c00
   ```

### Character Replacements

| Don't Use | Use Instead |
|-----------|-------------|
| ❌ | REJECT: or ERROR: |
| ✅ | PASS: or SUCCESS: |
| ⚠️ | WARNING: |
| 🔴 | CRITICAL |
| " " | " " |

---

## Source of Truth Hierarchy

When conflicts arise, use this priority:

1. Requirements document (if exists) - Highest authority
2. Product decisions document - Product decisions
3. Original ticket/issue (may be outdated)
4. Technical design document - Technical design
5. Architecture decision records - Architecture decisions
6. Code comments - Implementation notes

---

## Traceability

### Every Code Change Should Have

**In code comments:**
```javascript
/**
 * [Description]
 * 
 * @requirement REQ-001: Feature Description
 * @design Technical_Design.md §5.1
 * @test testFeatureEnabledAllowsAccess
 * @throws {Error} When validation fails
 */
```

### Updates Required
- Requirement ID in comment
- Link to design document section
- Corresponding unit test reference
- Traceability matrix update (if applicable)

---

## Document Validation Checklist

Before finalizing any documentation:

- [ ] All code blocks have proper syntax highlighting
- [ ] Mermaid diagrams use safe characters only
- [ ] No internal file references in architecture docs
- [ ] Table of contents included (if architecture doc)
- [ ] HTML generated if stakeholder-facing
- [ ] No operational metadata visible
- [ ] Professional tone maintained
- [ ] Traceability links included
- [ ] Source of truth hierarchy respected

---

**Rule Status:** ACTIVE  
**Scope:** All documentation creation and maintenance  
**Purpose:** Ensure consistent, high-quality documentation workflow
