---
name: semi-formal-reasoning
description: >
  Use for code verification, debugging, and deep code analysis without running tests.
  This skill should be used when the user asks to "verify my changes", "check my patch",
  "find the bug", "why does this test fail", "are these changes correct", "review this diff",
  or when analyzing code semantics that require tracing execution paths. It applies
  semi-formal structured reasoning from the Agentic Code Reasoning paper (Ugare & Chandra,
  Meta, 2026) to prevent unsupported claims and force evidence-based analysis.
version: 1.0.0
---

# Semi-Formal Code Reasoning

Structured reasoning for code verification, fault localization, and semantic analysis —
without running tests. Based on the [Agentic Code Reasoning](https://arxiv.org/abs/2603.01896)
paper which showed 10-12pp accuracy gains over unstructured chain-of-thought.

## Overview

Standard LLM reasoning about code makes unsupported claims — assumes function behavior
without tracing, skips edge cases, concludes equivalence without checking all paths.

Semi-formal reasoning fixes this by requiring a structured certificate: explicit premises,
execution traces with file:line citations, and formal conclusions. The agent cannot skip
cases or make claims without evidence.

## When to Use

- Verifying code changes are correct before committing (patch verification)
- Finding the root cause of a test failure (fault localization)
- Answering deep questions about code behavior (code QA)
- Reviewing diffs for semantic correctness, not just style
- Checking if two implementations are equivalent

## When NOT to Use

- Simple typo fixes or formatting changes
- When tests can be run directly (just run them)
- Style/lint reviews (use a linter)

## Core Method

### Step 1: Identify the Task Type

| Task | Trigger | Template |
|-|-|-|
| Patch Verification | "verify my changes", "check this diff", "is this correct" | Patch Equivalence |
| Fault Localization | "find the bug", "why does this test fail", "where's the error" | Fault Localization |
| Code QA | "how does this work", "what does this do", "explain this behavior" | Code Question Answering |

### Step 2: Gather Context (Agentic Exploration)

Before reasoning, explore the codebase to build sufficient context:

1. Read the diff/patch or code in question
2. Trace imports and dependencies of modified files
3. Find call sites — who calls the changed functions
4. Read relevant test files to understand expected behavior
5. Check for shadowed names, overrides, or monkey-patching

Do NOT start reasoning until sufficient context is gathered. The paper showed
agentic exploration (multi-step) consistently outperforms single-shot analysis.

### Step 3: Apply the Semi-Formal Template

Select the template matching the task type from `references/templates.md` and
fill it in completely. Every section is mandatory — skipping sections defeats
the purpose.

**Critical rules:**
- Every claim must cite file:line evidence
- Trace actual execution paths, do not assume function behavior
- Check for shadowed names, imports, and indirect calls
- State counterexamples explicitly when found
- If uncertain about a claim, explore more code before asserting

### Step 4: Derive Formal Conclusion

The conclusion must follow logically from the premises and analysis. Format:

```
FORMAL CONCLUSION:
By [definition], since [evidence summary from analysis],
[the patches are EQUIVALENT/NOT EQUIVALENT | the bug is at FILE:LINE | the behavior is X].
```

### Step 5: Report

Present findings as a structured report:

- **Verdict:** One-line answer
- **Confidence:** High/Medium/Low with justification
- **Evidence:** Key file:line citations
- **Risk areas:** Anything not fully verified (third-party libs, untraceable paths)

## Quick Reference: Semi-Formal vs Standard Reasoning

| Aspect | Standard | Semi-Formal |
|-|-|-|
| Claims | Natural language, can be unsupported | Must cite file:line evidence |
| Execution tracing | Optional, often skipped | Mandatory for each code path |
| Edge cases | Frequently missed | Template forces exhaustive analysis |
| Conclusion | Can be premature | Must follow from stated premises |
| Accuracy (patch equiv) | 78% | 88-93% |
| Accuracy (fault loc) | 60% Top-5 | 72% Top-5 |
| Accuracy (code QA) | 78% | 87% |

## Common Mistakes

| Mistake | Fix |
|-|-|
| Assuming function behavior from name | Trace the actual implementation, check for shadowing |
| Concluding equivalence without checking all tests | Analyze each F2P and P2P test separately |
| Skipping edge cases | Template forces exhaustive path tracing |
| Guessing third-party library behavior | Note as uncertainty, probe with independent scripts if possible |
| Starting analysis before gathering context | Explore codebase first — read imports, call sites, test files |
| Claiming "obvious" equivalence for similar diffs | Similar syntax can have different semantics (the Django-13670 lesson) |

## Key Insight from the Paper

The Django-13670 example: two patches for 2-digit year formatting looked equivalent.
Standard reasoning said yes. Semi-formal analysis discovered that `format` was shadowed
by a module-level function expecting a datetime object — Patch 1 would raise
AttributeError. Similar syntax, completely different semantics. The template forced
the agent to trace the actual `format` call instead of assuming it was Python's builtin.

## Additional Resources

- `references/templates.md` — Full semi-formal templates for all three task types
- Paper: [arxiv.org/abs/2603.01896](https://arxiv.org/abs/2603.01896)
