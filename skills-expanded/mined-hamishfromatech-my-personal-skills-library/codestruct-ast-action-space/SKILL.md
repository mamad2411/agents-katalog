---
name: codestruct-ast-action-space
description: Reframe codebases as structured AST action spaces for coding agents, enabling agents to operate on named program entities rather than text spans. Use when building structure-aware coding agent interfaces, reducing brittle string-matching edits, improving token efficiency in code agents, or designing tools that bridge AST structure and LLM agents.
---

# CODESTRUCT: Code Agents over Structured Action Spaces

## Overview

CODESTRUCT reframes the codebase as a structured action space where agents operate on named AST entities (functions, classes, methods) rather than text spans. Two structure-aware primitives — readCode for retrieving complete syntactic units and editCode for applying syntax-validated transformations — replace brittle string matching. Evaluated on SWE-Bench Verified across six LLMs, CODESTRUCT improves Pass@1 by 1.2-5.0% while reducing token consumption by 12-38%. Models that frequently fail under text-based interfaces benefit most: GPT-5-nano improves by 20.8% as empty-patch failures drop from 46.6% to 7.2%.

## When to Use

- Building coding agent interfaces that operate on program structure, not text
- Reducing brittle string-matching failures in code editing tools
- Improving token efficiency for repository-level coding tasks
- Designing MCP-based tools that bridge AST structure and LLM agents
- Addressing empty-patch failures in smaller/weaker coding models
- NOT for: single-function generation, non-code tasks, or when text-based editing already works reliably

## Core Process / Workflow

### 1. Recognize the Abstraction Mismatch

Current agents interact with code through a fundamental mismatch:
- **Reading**: choose between entire files (irrelevant context degrades reasoning) or line ranges (truncate functions mid-statement)
- **Editing**: string-based replacement is brittle — "no occurrence" errors from formatting drift, "multiple occurrence" errors from repeated patterns
- **Wasteful**: even minor edits require regenerating significant code verbatim
- **Failure cascades**: string-match failures force costly trial-and-error cycles

### 2. Implement readCode (Structure-Aware Retrieval)

**Three modes:**

**Repository browsing (directory input):**
- Input: directory path
- Returns: list of files (optionally filtered to source files)
- Enables agent to navigate repository layout before selecting a file

**File summarization (file input, no selector):**
- If file small (< threshold τ, e.g., 10K chars): return full content
- If file large: return compact structural summary (signatures of top-level entities + scoped names)
- Agent identifies relevant entities without loading entire file

**Entity retrieval (file + selector):**
- Parse file into AST
- Extract signatures of functions, classes
- Fuzzy-match selector σ to entities
- Return complete implementation of matched entities (AST subtree rendered as code)
- Selectors can be unscoped (`load`) or scoped (`User.load`)

**Key property:** Returns complete syntactic units without truncation or excess context, reducing irrelevant input and avoiding line-number dependence.

### 3. Implement editCode (Structure-Aware Modification)

**Operations:**
- `insert`: insert after target AST node
- `replace`: replace target AST node with new content
- `removal`: remove target AST node

**Algorithm:**
1. Parse file into AST (or reuse cached)
2. Locate target AST node via selector
3. Compute local indentation context
4. Apply indentation to replacement code
5. Apply transformation within node's syntactic scope
6. **Validate**: reject if modified AST has syntax errors (HASSYNTAXERROR check)
7. Write file only if syntactically valid

**Key property:** Each editCode invocation produces a syntactically valid AST by construction. Edits that would introduce syntax errors are rejected before committing.

### 4. Integrate via MCP

CODESTRUCT is exposed through standard tool interfaces (MCP), allowing integration into existing agent frameworks without modifying planning or execution logic.

```
# Conceptual interface
readCode(filePath, selector=None, lineRange=None)
editCode(filePath, operation, selector, replacementCode)
```

### 5. Match to Model Capability

**High-capability models (GPT-5, GPT-5-mini, Qwen3-Coder-480B):**
- CODESTRUCT reduces tool-level errors by 76-88%
- Accuracy gains: +1.2 to +5.0% Pass@1
- Token reductions: 12-38%

**Smaller models (GPT-5-nano):**
- Empty-patch failures drop from 46.6% to 7.2% (-84.5%)
- Accuracy gain: +20.8 percentage points
- Trade-off: increased compute (structured actions enable sustained exploration)
- Interpretation: CODESTRUCT unlocks solutions for models with correct intent but unable to express valid text edits

**Weakest models (Qwen3-8B):**
- Maintains high error rates (11.966/instance) despite 16% reduction
- Accuracy gains limited — failures stem from reasoning capacity, not interface brittleness

## Performance Results (SWE-Bench Verified)

| Model | Interface | Pass@1 (%) | Input Tokens | Cost ($) |
|-------|-----------|------------|--------------|----------|
| GPT-5 | Baseline | 66.0 | 452.7M | 574.0 |
| | CODESTRUCT | 67.2 (+1.2) | 366.3M (-19.1%) | 462.2 (-19.5%) |
| GPT-5-mini | Baseline | 60.4 | 593.7M | 151.0 |
| | CODESTRUCT | 62.0 (+1.6) | 404.5M (-31.9%) | 101.8 (-32.6%) |
| GPT-5-nano | Baseline | 19.6 | 808.0M | 40.7 |
| | CODESTRUCT | 40.4 (+20.8) | 1,137.4M (+40.8%) | 57.3 (+40.8%) |
| Qwen3-Coder | Baseline | 61.2 | 805.8M | 365.3 |
| | CODESTRUCT | 66.2 (+5.0) | 705.3M (-12.5%) | 321.3 (-12.1%) |

## References

- See [references/evidence-base.md](references/evidence-base.md) for full ablation studies, error analysis, and CodeAssistBench results.