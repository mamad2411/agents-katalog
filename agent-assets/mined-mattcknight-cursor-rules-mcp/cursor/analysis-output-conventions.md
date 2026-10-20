---
description: Analysis output conventions - location and naming rules for storing analysis outputs in template repository
alwaysApply: true
tags: [critical, documentation, analysis, file-location, file-naming]
priority: 1
version: 2.0.0
consolidatedFrom: [analysis-output-location.mdc, analysis-document-naming.mdc]
---

# Analysis Output Conventions

**CRITICAL rules for storing analysis outputs: location, naming, and organization.**

---

## Core Principle

**ALL analysis outputs MUST be stored in the template repository's `docs/` directory with timestamped, versioned filenames. NEVER store in target codebase.**

---

## Section 1: Output Location Rules

### Mandatory Location: Template Repository `docs/`

**CRITICAL:** When analyzing external codebases or target projects:

- ✅ **ALWAYS** store analysis outputs in `docs/[PROJECT_NAME]-analysis/` directory
- ✅ **ALWAYS** use relative paths from template repository root
- ❌ **NEVER** create analysis directories in the target codebase
- ❌ **NEVER** store analysis files in the project being analyzed

### Rationale: Why Template Repository?

1. **Separation of Concerns**: Analysis outputs are meta-project artifacts, not part of the analyzed codebase
2. **Template Knowledge**: Analysis learnings contribute to template knowledge base
3. **Version Control**: Analysis outputs should be versioned with the template, not the target project
4. **Reusability**: Analysis patterns and learnings can be referenced across multiple projects
5. **Clean Target Codebase**: Keeps analyzed projects clean without analysis artifacts

---

### Standard Directory Structure

```
docs/
├── [PROJECT_NAME]-analysis/
│   ├── tech-stack/
│   ├── data-flow/
│   ├── design-patterns/
│   ├── prerequisites/
│   ├── requirements/
│   ├── concerns/
│   ├── integrations/
│   ├── business-logic/
│   └── synthesis/
│       ├── comprehensive-analysis.md
│       └── [PROJECT_NAME]-analysis.presentation.md
└── learnings/
    └── [PROJECT_NAME]-analysis-[DATE].md
```

### Example: [Project Name] Analysis

```
docs/
├── [project-name]-analysis/
│   ├── tech-stack/
│   │   ├── project-structure.md
│   │   ├── backend-tech-stack.md
│   │   ├── frontend-tech-stack.md
│   │   └── infrastructure-stack.md
│   ├── data-flow/
│   │   ├── api-data-flow.md
│   │   ├── payment-flow.md
│   │   ├── database-flow.md
│   │   └── frontend-data-flow.md
│   ├── design-patterns/
│   │   ├── backend-patterns.md
│   │   └── architecture-patterns.md
│   ├── prerequisites/
│   │   └── system-prerequisites.md
│   ├── requirements/
│   │   ├── functional-requirements.md
│   │   └── non-functional-requirements.md
│   ├── concerns/
│   │   ├── security-assessment.md
│   │   ├── security-architecture.md
│   │   ├── technical-concerns.md
│   │   └── risk-assessment.md
│   ├── integrations/
│   │   ├── external-integrations.md
│   │   ├── scheduled-jobs.md
│   │   └── hooks-events.md
│   ├── business-logic/
│   │   ├── business-rules.md
│   │   └── domain-logic.md
│   └── synthesis/
│       ├── comprehensive-analysis.md
│       ├── [project-name]-analysis.presentation.md
│       └── [project-name]-analysis.html
└── learnings/
    └── [project-name]-analysis-2025-01-22.md
```

---

## Section 2: File Naming Conventions

### Naming Format

**Pattern:** `YYYYMMDD_HHMMSS_{description}_{version}.md`

**Components:**
- **Timestamp:** `YYYYMMDD_HHMMSS` (24-hour format, creation time)
- **Description:** Descriptive name in kebab-case
- **Version:** Git tag or relevant version (e.g., `v3.0.1`, `v3.0.0`)
- **Extension:** `.md`

### Examples

#### ✅ CORRECT

```
20251116_140500_investigation-results_v3.0.1.md
20251116_211500_questions-and-decisions-matchsource-performance-fix_v3.0.1.md
20251116_211500_matchsource-performance-fix.plan_v3.0.1.md
20251115_220538_v3.0.0-mortgagee-refactor.plan_v3.0.0.md
20251116_holistic-refactoring-failure-analysis_v3.0.0.md
```

#### ❌ WRONG

```
INVESTIGATION_RESULTS.md                    ❌ No timestamp, no version
analysis.md                                  ❌ No timestamp, no version, generic name
questions-and-decisions.md                   ❌ No timestamp, no version
results_v3.0.1.md                           ❌ No timestamp
20251116_results.md                          ❌ No version suffix
```

### Rationale

**Why Timestamp Prefix?**
1. Chronological order - files naturally sort by creation date
2. Context - immediately know when analysis was done
3. Version comparison - easy to see analysis progression
4. Uniqueness - prevents file name collisions

**Why Version Suffix?**
1. Git tag correlation - links document to specific codebase version
2. Traceability - know which version the analysis applies to
3. Historical reference - easy to find analysis for specific releases
4. Clarity - no confusion about which version is being discussed

**Problems This Prevents:**
- ❌ "Which version was this analysis for?"
- ❌ "When was this document created?"
- ❌ "Is this the latest analysis or old?"
- ❌ "Swimming in random ass md files that make no sense timewise and version wise"
- ❌ Files scattered without clear chronology
- ❌ Cannot find relevant analysis for specific version

---

## Section 3: Document Type Guidelines

### Document Types Requiring These Conventions

**MANDATORY for:**
- ✅ Analysis documents (tech stack, data flow, design patterns)
- ✅ Investigation results
- ✅ Questions and decisions
- ✅ Implementation plans
- ✅ Recommendation files
- ✅ Learning documents
- ✅ Progress reports
- ✅ Synthesis documents

**OPTIONAL for:**
- README files (permanent documentation)
- Template files
- Configuration files

---

## Section 4: Implementation Rules

### ✅ DO:

1. **Create project-specific subdirectory** in `docs/`
   - Format: `docs/[PROJECT_NAME]-analysis/`
   - Use kebab-case for project names
   - Example: `docs/[project-name]-analysis/`

2. **Organize by analysis type**
   - Create subdirectories for each analysis category
   - Follow standard structure (tech-stack, data-flow, etc.)

3. **Store learnings separately**
   - Use `docs/learnings/` for captured insights
   - Filename format: `[PROJECT_NAME]-analysis-[DATE].md`

4. **Use relative paths**
   - All paths relative to template repository root
   - Never use absolute paths to target codebase

### ❌ DON'T:

1. ❌ **NEVER** create analysis directories in target codebase
   - Wrong: `C:\Work\Repositories\Company\project-name\src\analysis/`
   - Correct: `docs/[project-name]-analysis/`

2. ❌ **NEVER** store analysis files in target project
   - Wrong: `[TARGET_PROJECT]/analysis/`
   - Correct: `docs/[PROJECT_NAME]-analysis/`

3. ❌ **NEVER** use absolute paths to target codebase
   - Wrong: `C:\Work\Repositories\Company\project-name\src\...`
   - Correct: `docs/[project-name]-analysis/...`

4. ❌ **NEVER** mix analysis outputs with target project files

---

## Section 5: Workflow & Helpers

### Creating Analysis Documents

**Step-by-Step:**
1. Generate timestamp: `Get-Date -Format "yyyyMMdd_HHmmss"`
2. Determine version: Use current git tag or relevant version
3. Create descriptive name: Use kebab-case, be specific
4. Combine: `{timestamp}_{description}_{version}.md`
5. Store in: `docs/[PROJECT_NAME]-analysis/{category}/`

### PowerShell Helper

```powershell
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$description = "investigation-results"  # Change as needed
$version = "v3.0.1"  # Current git tag or relevant version
$filename = "${timestamp}_${description}_${version}.md"
Write-Host "Create file: docs/$filename"
```

### Bash Helper

```bash
timestamp=$(date +"%Y%m%d_%H%M%S")
description="investigation-results"  # Change as needed
version="v3.0.1"  # Current git tag or relevant version
filename="${timestamp}_${description}_${version}.md"
echo "Create file: docs/$filename"
```

---

## Section 6: Verification Checklist

Before completing analysis, verify:

### Location Check
- [ ] All outputs stored in `docs/[PROJECT_NAME]-analysis/`
- [ ] No files created in target codebase
- [ ] All paths are relative to template repository
- [ ] Subdirectories follow standard structure
- [ ] Learnings stored in `docs/learnings/`

### Naming Check
- [ ] Timestamp prefix present (`YYYYMMDD_HHMMSS`)
- [ ] Descriptive name in kebab-case
- [ ] Version suffix present (`_v{version}`)
- [ ] `.md` extension used
- [ ] No generic names ("analysis.md", "results.md")

### Organization Check
- [ ] Files categorized appropriately
- [ ] Synthesis documents in `synthesis/` subdirectory
- [ ] HTML conversions (if any) in `synthesis/` subdirectory
- [ ] Cross-project learnings in `docs/learnings/`

---

## Section 7: Examples by Use Case

### Use Case: Codebase Analysis

**Location:**
```
docs/[project-name]-analysis/
├── tech-stack/
├── data-flow/
├── design-patterns/
└── synthesis/
    └── 20251122_comprehensive-analysis_v1.0.0.md
```

### Use Case: Investigation Results

**Location:**
```
docs/[project-name]-analysis/concerns/
└── 20251116_140500_investigation-results_v3.0.1.md
```

### Use Case: Learning Capture

**Location:**
```
docs/learnings/
└── 20251122_[project-name]-analysis-learnings_v1.0.0.md
```

---

## Remember

✅ **Template Repository** - All analysis outputs belong in template repository `docs/` directory  
✅ **Project-Specific** - Use `[PROJECT_NAME]-analysis/` subdirectory structure  
✅ **Timestamp + Version** - Every analysis file must have timestamp prefix and version suffix  
✅ **Relative Paths** - Always use relative paths from template repository root  
✅ **Separation** - Keep analysis artifacts separate from target codebase  
✅ **Learnings** - Store insights in `docs/learnings/` for cross-project knowledge  
✅ **Zero Tolerance** - NEVER create analysis files in target codebase

---

**Rule Status:** 🔴 CRITICAL - ALWAYS APPLY  
**Enforcement:** ZERO TOLERANCE  
**Priority:** 1  
**Version:** 2.0.0  
**Last Updated:** 2025-11-17  
**Consolidation:** Merged analysis-output-location.mdc and analysis-document-naming.mdc  
**Savings:** -1 file, ~6 KB, ~1,500 tokens
