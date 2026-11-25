---
name: rev-symbol
description: Restore function symbols by analyzing code patterns, strings, constants, and cross-references
---

# rev symbol

Use this skill when the task matches the description above.
Keep the initial response concise and only open bundled references or scripts when they are clearly needed.

## Quick cues

- func-name: sub_401000
- func-address: 0x401000
- callers: 0x402000, 0x403000    // List of functions that call this function
- callees: 0x404000, 0x405000    // List of functions called by this function
- **String constants**: Strings used in the function may reveal its purpose
- **Numeric constants / Magic Numbers**:
- MD5: `0x67452301`, `0xEFCDAB89`, `0x98BADCFE`, `0x10325476`
- CRC32: `0xEDB88320`

## Available sections

- rev-symbol - Symbol Recovery
- Pre-check
- Export Directory Structure
- Function File Format (decompile/*.c)
- Symbol Recovery Steps
- Step 1: Analyze Internal Characteristics
- Step 2: Analyze Cross-References
- Step 3: Information Gathering and Search
- Output Format
- Symbol Recovery Analysis: <function_address>
- Function Characteristics
- Cross-Reference Analysis

