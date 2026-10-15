---
name: zh-tw
description: "Rewrite the previous reply in Traditional Chinese"
---

# 繁體中文翻譯

## Trigger

- Keywords: 翻譯, zh-tw, 繁體中文, traditional chinese, rewrite in chinese

## When NOT to Use

- Translating code comments only (do inline)
- Translating to other languages (not zh-TW)

## Task

Rewrite English or Simplified Chinese content from the conversation into **Traditional Chinese**.

### Arguments

```
$ARGUMENTS
```

### Target Selection

| Parameter | Translation Target |
|-----------|-------------------|
| No parameter | Previous reply |
| Has description (e.g. "the report above") | Content in conversation matching description |

### Requirements

| Item | Description |
|------|-------------|
| Language | Traditional Chinese (Taiwan usage) |
| Terms | Keep technical terms, code, and filenames in original language |
| Format | Preserve original markdown format (tables, code blocks, lists, etc) |
| Content | Full rewrite, do not omit any part |

### Conversion Rules

- Simplified Chinese -> Traditional Chinese (vocabulary conversion, not just font)
- English descriptions -> Traditional Chinese
- Maintain technical term consistency

### Execution

Output the fully rewritten content directly, no additional explanation needed.
