---
description: Recommendation File Management - Rules for creating and managing permanent recommendation files with timestamps
alwaysApply: false
---

# Recommendation File Management

## Core Principle

**ALL recommendations MUST be saved permanently in timestamped files.**

---

## Mandatory Rules

### 1. When User Requests Recommendations

When user says:
- "prepare recommendations"
- "provide recommendations"
- "analyze and recommend"
- "evaluate and suggest"
- Any variation requesting analysis with suggestions

**ALWAYS create a recommendation file.**

---

### 2. File Location

```
docs/recommendations/YYYY-MM-DD_HH-MM_Title_Of_Recommendation.md
```

**Format:**
- Directory: `docs/recommendations/` (create if doesn't exist)
- Timestamp: `YYYY-MM-DD_HH-MM` (24-hour format, based on current time)
- Title: Snake_case, descriptive
- Extension: `.md`

**Examples:**
```
docs/recommendations/2025-10-22_21-29_Rules_Consolidation_Analysis.md
docs/recommendations/2025-10-22_14-30_Architecture_Refactoring_Proposal.md
docs/recommendations/2025-10-23_09-15_Database_Optimization_Strategy.md
```

---

### 3. File Naming Rules

- ✅ Use current date/time
- ✅ Use underscores for spaces
- ✅ Descriptive title (not generic)
- ✅ Title case for readability
- ❌ No spaces in filename
- ❌ No special characters except underscore and hyphen
- ❌ Generic titles like "Recommendations.md"

---

### 4. File Permanence

**CRITICAL:** Recommendation files are PERMANENT

- ✅ Create in `docs/recommendations/`
- ✅ Keep forever (never delete)
- ✅ Add to git
- ✅ Can be superseded by new recommendations
- ❌ NEVER delete recommendation files
- ❌ NEVER move out of `docs/recommendations/`
- ❌ NEVER overwrite existing recommendations

---

### 5. If Superseding Previous Recommendation

If a new recommendation supersedes an old one:

1. Create NEW timestamped file
2. Reference the old recommendation at the top:
   ```markdown
   # New Recommendation Title
   
   **Supersedes:** docs/recommendations/2025-10-20_15-30_Old_Recommendation.md
   **Reason for Update:** [Explain what changed]
   ```
3. Keep both files (never delete old one)

---

### 6. Content Requirements

Every recommendation file MUST include:

```markdown
# [Title]

**Date:** YYYY-MM-DD HH:MM
**Purpose:** [Why this recommendation exists]
**Context:** [What triggered this analysis]

---

## Current State - Facts Only
[Document what exists now - NO assumptions]

## Analysis
[Detailed analysis with evidence]

## Recommendations
[Specific, actionable recommendations]

## Decision Points Required
[Questions user must answer before proceeding]

## Risk Assessment
[Risks and mitigations]

---

**Status:** [Draft | Approved | Implemented | Superseded]
**Last Updated:** YYYY-MM-DD
```

---

### 7. Process Flow

```
User requests recommendations
    ↓
Check if docs/recommendations/ exists
    ↓ (if not)
Create docs/recommendations/ directory
    ↓
Generate timestamp: YYYY-MM-DD_HH-MM
    ↓
Create descriptive title from topic
    ↓
Create file: docs/recommendations/[timestamp]_[title].md
    ↓
Write comprehensive analysis
    ↓
NEVER delete this file
```

---

## Examples

### WRONG ❌
```markdown
# Location: docs/ANALYSIS.md
# Location: temp/recommendations.md
# Location: recommendations.md (root)
# Filename: recommendations.md (no timestamp)
# Action: Delete old recommendation file
```

### RIGHT ✅
```markdown
# Location: docs/recommendations/2025-10-22_21-29_Rules_Consolidation_Analysis.md
# Filename: Timestamped + descriptive
# Action: Keep file forever
# If update needed: Create NEW timestamped file
```

---

## Directory Structure

```
docs/
└── recommendations/
    ├── 2025-10-15_10-00_Initial_Architecture_Analysis.md
    ├── 2025-10-18_14-30_Feature_Flow_Optimization.md
    ├── 2025-10-22_21-29_Rules_Consolidation_Analysis.md
    └── README.md  (optional index of recommendations)
```

---

## Verification Checklist

Before completing a recommendation task:
- [ ] File created in `docs/recommendations/`
- [ ] Filename has timestamp (YYYY-MM-DD_HH-MM)
- [ ] Filename has descriptive title
- [ ] Content includes: Date, Purpose, Context
- [ ] Analysis is fact-based (no assumptions)
- [ ] Recommendations are specific and actionable
- [ ] Decision points are clearly stated
- [ ] Status is indicated
- [ ] File will NEVER be deleted

---

## Zero Tolerance

- **NEVER** create recommendation files outside `docs/recommendations/`
- **NEVER** create recommendation files without timestamps
- **NEVER** delete recommendation files
- **NEVER** use generic filenames like "recommendations.md"
- **NEVER** overwrite existing recommendations

---

## Remember

✅ **Permanent Records**: Recommendations are historical records showing evolution of decisions  
✅ **Timestamp Required**: Always include timestamp in filename  
✅ **Never Delete**: Keep all recommendation files forever  
✅ **Supersede, Don't Replace**: Create new file if updating old recommendation  
✅ **Specific Location**: Always in `docs/recommendations/` directory
