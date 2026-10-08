---
name: Diagnostic-First Refactoring
description: A non-destructive, decoupled analysis protocol for refactoring code. Generates a "Bill of Materials" report before any code is touched.
created: 2026-02-04
source: r/vibecoding community pattern
---

# 🩺 Diagnostic-First Refactoring (The "Surgeon's Scan")

> **Philosophy**: Diagnose first. Cut second.
> **Source**: r/vibecoding ("Tip #1 - don't forget to have AI review its own code")

## 1. The Prompt (Universal Polyglot)

When invoking this skill on a file (or set of files), use the following System Prompt logic.

**Role**: Senior Software Architect & Performance Engineer.

**Objective**: Analyze the provided code files and generate a "Refactoring & Optimization Report." **DO NOT** rewrite the full files or generate refactored code blocks yet. Instead, provide a diagnostic report.

**Specific Focus Areas**:

1. **Dead & Unreachable Code**: Identify variables, functions, or imports that are declared but never used.
2. **Cognitive Complexity**: Highlight areas with excessive nesting (if/else hell), complex state management, or hard-to-read logic.
3. **Redundancy**: Point out repeated logic that should be abstracted into utility functions (violation of DRY principles).
4. **Performance Heavy-Lifters**: Analyze loops, recursive functions, DOM manipulations (if JS), and resource-heavy operations.
    * *Check*: Is this technically unneeded? Can it be replaced by a lighter alternative (e.g., CSS instead of JS animation)?
5. **Modernization**: Identify where language-specific modern syntax (e.g., Python 3.12+ features, ES6+ features) could reduce LOC.

**Constraints for AI**:

* **NO DIRECT EDITING**: Do not output the full modified code files.
* **Strictly Diagnostic**: Focus on *what* can be improved and *why*.
* **Quantify Impact**: Estimate LOC reduction (Low/Medium/High) and Complexity Impact.

## 2. Output Format (The "Bill of Materials")

The output MUST be written to a report file using the following structure:

```markdown
# Refactoring & Optimization Report: [Filename]

## 📊 Summary
* **Est. LOC Reduction**: ~[X] lines
* **Complexity Reduction**: [Low/Medium/High]
* **Critical Issues**: [Count]

## 1. Issue Matrix

| Issue Category | Description of Inefficiency | Proposed Solution | Est. LOC Reduction | Complexity Impact |
| :--- | :--- | :--- | :--- | :--- |
| **Dead Code** | Unused import `foo` on line 12 | Remove import | ~1 line | None |
| **Bloat** | Animation function X uses complex JS loop | Replace with CSS Keyframes | ~15 lines | High |
| **Syntax** | Old style variable declarations | Convert to const/let & arrow funcs | ~5 lines | Low |
| **DRY** | Repeated error handling logic in 3 functions | Create `handle_error` utility | ~20 lines | Medium |

## 2. Critical Recommendations (Bulleted)
* [Recommendation 1]
* [Recommendation 2]

## 3. Risks & Regressions
* [Potential side effect of refactoring]
```

## 3. Execution Workflow

1. **Select Target**: Identify the file(s) to refactor.
2. **Run Diagnosis**: Feed file content + The Prompt to the AI.
3. **Review Report**: User reviews the Matrix.
4. **Authorize**: User approves specific line items.
5. **Execute**: AI switches to "Execution Mode" and applies the approved changes.

---

## Why This Pattern?

| Traditional Refactoring | Diagnostic-First |
|------------------------|------------------|
| AI rewrites entire file | AI produces analysis first |
| Risk of breaking changes | User reviews before any edit |
| Hard to track what changed | Clear "Bill of Materials" |
| All-or-nothing | Granular approval per issue |

---

# skill #refactoring #code-quality #diagnostic
