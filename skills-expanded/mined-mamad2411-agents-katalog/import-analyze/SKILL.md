---
name: import-analyze
description: Analyze binary import table. Trigger: imports, import table, dll list, api dependencies, IAT.
tool: C:\Users\Administrator\Desktop\ai2\新破甲\Tool\die\die.exe
x-alice-class: reverse
---# import-analyze

## Trigger
`imports, import table, dll list, api dependencies, IAT`

## Flow
```
DIE open $TARGET -> Import tab -> list suspicious APIs (Crypt*, Internet*, IsDebugger*)
```

## Script
`scripts/import_analyze.py`
