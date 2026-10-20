---
name: full-reverse
description: Complete reverse engineering chain. Trigger: full reverse, complete analysis, reverse workflow, 完整逆向.
type: chain
x-alice-class: reverse
---# full-reverse

## Chain
1. `string-extract` — Extract strings from binary
2. `import-analyze` — Analyze import table
3. `function-decompile` — Decompile key functions
4. `xref-trace` — Cross-reference analysis

## Execution
Execute each step sequentially. Output combined results.
