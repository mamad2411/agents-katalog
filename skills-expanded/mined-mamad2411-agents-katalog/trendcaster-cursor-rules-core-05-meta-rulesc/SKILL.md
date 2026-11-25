---
description: Defines the core logic for the AI to determine its operational FOCUS
globs: 
alwaysApply: true
---

# Meta-Rules for AI Assistant Interaction

## Rule System Overview

**Rule Categories (Always Apply in This Order):**
1. **Core Rules** ([core/](rules/core)): Essential operational guidelines - ALWAYS APPLY
2. **Best Practices** ([best-practices/](rules/best-practices)): Project-wide standards - ALWAYS APPLY  
3. **Workflow Rules** ([workflow/](rules/workflow)): FOCUS-specific instructions - APPLY ONE SET

## FOCUS Determination (Critical)

**Your primary task: Identify the correct FOCUS and apply its workflow rules.**

### 1. Explicit User Command (HIGHEST PRIORITY)
- **Check:** User's request contains `FOCUS = PLANNING`, `FOCUS = IMPLEMENTATION`, or `FOCUS = DEBUGGING`
- **Action:** Use that FOCUS immediately. Apply workflow rules from [workflow/[FOCUS]/](rules/workflow/)
- **If a rule is mentioned by name (e.g., @rule-name), you MUST use and follow that rule.**

### 2. Infer from Task Intent (PRIMARY METHOD)
- **PLANNING:** Design, analysis, solution exploration, architecture discussions
  → Use [workflow/planning/](rules/workflow/planning)
- **IMPLEMENTATION:** Writing/modifying code, implementing known solutions
  → Use [workflow/implementation/](rules/workflow/implementation)  
- **DEBUGGING:** Fixing errors, diagnosing issues, troubleshooting
  → Use [workflow/debugging/](rules/workflow/debugging)
- **Unclear Intent:** ASK user to specify FOCUS

### 3. Internal Mode Conflicts (IF APPLICABLE)
- **Conflict:** Internal mode differs from inferred FOCUS
- **Action:** Notify user of conflict, prioritize inferred FOCUS, ask for confirmation

## Rule Application Matrix

**ALWAYS APPLY:**
- All Core Rules: [memory-bank-usage](mdc:.cursor/rules/core/memory-bank-usage.mdc), [general-coding-conventions](mdc:.cursor/rules/core/general-coding-conventions.mdc), [llm-interaction-guidelines](mdc:.cursor/rules/core/llm-interaction-guidelines.mdc)
- All Best Practices: [error_documentation_guidelines](mdc:.cursor/rules/best-practices/error-documentation-guidelines.mdc), [lessons-learned](mdc:.cursor/rules/best-practices/lessons-learned.mdc)

**APPLY ONE WORKFLOW SET:** Based on determined FOCUS from [workflow/[FOCUS]/](rules/workflow/)

**CONSULT MEMORY BANK:** Use [memory-bank/](mdc:memory-bank) files for context per [memory-bank-usage](mdc:.cursor/rules/core/memory-bank-usage.mdc)

## Key Memory Bank Files
- **Project Context:** [project_brief.md](mdc:memory-bank/project/project_brief.md), [product_context.md](mdc:memory-bank/project/product_context.md)
- **Architecture:** [architecture.md](mdc:memory-bank/project/architecture.md), [system_patterns.md](mdc:memory-bank/project/system_patterns.md)
- **Technology:** [tech_context.md](mdc:memory-bank/project/tech_context.md), [directory_structure.md](mdc:memory-bank/project/directory_structure.md)
- **Status:** [project_status.md](mdc:memory-bank/status/project_status.md)
- **Documentation:** 

## When You're Stuck - Escalation Guide
1. **Can't determine FOCUS:** Ask: "Is this task PLANNING, IMPLEMENTATION, or DEBUGGING?"
2. **Missing memory bank docs:** Say: "I need documentation for [LIBRARY] v[VERSION]. Please run: Update memory bank using @memory-bank-library-overview.mdc"
3. **Rule conflicts:** Explain: "Rules X and Y seem to conflict for situation Z. How should I proceed?"

## Example Scenarios

### Scenario: Adding a new React component
1. FOCUS = PLANNING or IMPLEMENTATION?
   → If you know exactly what to build: IMPLEMENTATION
   → If design unclear: PLANNING
2. Check [tech_context.md](mdc:memory-bank/project/tech_context.md) for React version (18.2.0)
3. Check [architecture.md](mdc:memory-bank/project/architecture.md) for component patterns
4. Implement following general-coding-conventions.mdc

## Rules Directory Structure
```text
.
└── rules
    ├── best-practices
    │   ├── error-documentation-guidelines.mdc
    │   ├── lessons-learned.mdc
    │   └── README.md
    ├── core
    │   ├── 00-meta-rules.mdc
    │   ├── general-coding-conventions.mdc
    │   ├── llm-interaction-guidelines.mdc
    │   ├── llm-memory-interaction.mdc
    │   ├── memory-bank-library-overview.mdc
    │   ├── memory-bank-section-summarize.mdc
    │   ├── memory-bank-usage.mdc
    │   └── README.md
    ├── project
    │   ├── code-style.mdc
    │   ├── documentation.mdc
    │   ├── file-organization.mdc
    │   ├── general-typescript-project-rules.mdc
    │   ├── naming-conventions.mdc
    │   ├── pnpm.mdc
    │   └── README.md
    ├── README.md
    └── workflow
        ├── debugging
        │   ├── debugging-rules.mdc
        │   └── README.md
        ├── implementation
        │   ├── implementation-rules.mdc
        │   └── README.md
        ├── planning
        │   ├── planning-rules.mdc
        │   └── README.md
        └── README.md
```
