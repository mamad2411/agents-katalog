---
name: string-extract
description: Extract strings from binary for pattern matching. Trigger: strings, extract strings, ascii, unicode, text search, hardcoded values.
tool: C:\Users\Administrator\Desktop\ai2\新破甲\scripts\pe_analyzer.py --strings
x-alice-class: reverse
---# string-extract

## Trigger
`strings, extract strings, ascii, unicode, text search, hardcoded values`

## Flow
```
pe_analyzer.py --file $TARGET --strings -> grep patterns -> output offset:value pairs
```

## Script
`scripts/string_extract.py`
