---
name: neurocode
description: >-
  Use NeuroCode to slice codebases using in-memory Tree-sitter Code Property Graphs, trace execution
  call-paths in <1ms, generate zero-token Mermaid maps, and graft AST subtrees under edge VRAM budgets.
---

# NeuroCode Agent Skill

NeuroCode is a high-performance in-memory Code Property Multigraph (CPG) reachability engine that reduces token overhead by 97.1% and prevents Out-of-Memory (OOM) crashes.

## Quick CLI Invocations

### 1. Bounded Context Slicing (< 1,500 tokens)
Instead of dumping full files, extract the relevant reachability closure:
```bash
neurocode slice --query "<bug or symbol>" <filepath>
```

### 2. Sub-Millisecond Call Tracing
Trace execution paths from an entry point to a target function:
```bash
neurocode trace --entry <func_name> --target <target_symbol>
```

### 3. Zero-Token Architecture Diagram
Generate zero-token Mermaid.js diagrams for code comprehension:
```bash
neurocode map <directory_or_file>
```

### 4. AST Subtree Grafting with Auto-Rollback
Safely apply a syntax-verified patch with automatic rollback if tests fail:
```bash
neurocode graft --file <filepath> --test "pytest tests/"
```
