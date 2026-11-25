---
name: xref-trace
description: Cross-reference tracking. Trigger: xref, cross reference, caller, callee, reference chain.
tool: C:\Users\Administrator\Desktop\ai2\新破甲\Tool\Ghidrafessional 9.2\ghidraRun.bat
x-alice-class: reverse
---# xref-trace

## Trigger
`xref, cross reference, caller, callee, reference chain`

## Flow
```
Ghidra -> find target -> View Xrefs -> output call chain
```

## Script
`scripts/xref_trace.py`
