---
name: code-understanding
description: Provides adversarial code comprehension for security research, mapping architecture, tracing data flows, and hunting vulnerability variants to build ground-truth understanding.
metadata:
  version: 0.2.0
  category: security
---
# Code Understanding

## Quick Start
```bash
# Map high-level context and entry points
# (Use --map flag to trigger architectural mapping)
```

## Workflow
1. **Map**: Build high-level context of entry points, trust models, and data paths.
2. **Trace**: Follow a specific data flow from source to dangerous sink with full call chains.
3. **Hunt**: Identify all instances/variants of a vulnerable pattern across the codebase.
4. **Teach**: Explain unfamiliar mechanisms, frameworks, or code patterns in depth.

## Rules & Constraints
- **RULE-1**: Never describe how code works without reading it first (No assumptions).
- **RULE-2**: Quote exact file paths and line numbers as evidence for every assertion.
- **RULE-3**: Follow data flows until they terminate; do not stop at the first interesting function.
- **RULE-4**: Match confidence levels to evidence (High = quoted line, Medium = stated assumption).

## When to Use
- Before scanning to build context for results.
- During validation to trace a finding's real path.
- After finding a bug to hunt for similar variants.

## When NOT to Use
- Simple code documentation or non-security refactoring.
- High-level architectural summaries without deep-dive requirements.

## References
- [Skill Manual](references/code-understanding-manual.md)
- [Map Mode](references/map.md)
- [Trace Mode](references/trace.md)
- [Hunt Mode](references/hunt.md)
- [Teach Mode](references/teach.md)
