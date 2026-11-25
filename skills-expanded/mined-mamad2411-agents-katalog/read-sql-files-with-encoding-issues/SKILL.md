---
name: "read-sql-files-with-encoding-issues"
description: "Read SQL Server script files that have UTF-16, BOM, or wide character encoding issues that prevent normal read operations"
version: 1
created: "2026-06-11"
updated: "2026-06-11"
---
## When to Use
When read tool shows garbled text, wide characters, or binary data when opening .sql files, typically from SQL Server Management Studio script exports

## Procedure
1. First attempt: Use read tool with default encoding - if text is readable, proceed normally
2. If garbled: Check file encoding with bash: file {filename} or head -c 100 {filename} | od -c to see byte patterns
3. Common SQL Server encodings: UTF-16 LE (little-endian), UTF-16 BE (big-endian), UTF-8 with BOM, Windows-1252
4. Try UTF-16 LE conversion: bash -c "iconv -f UTF-16LE -t UTF-8 '{filename}'" (most common for SSMS exports)
5. If iconv not available or fails, use Python: python -c "import sys; print(open(sys.argv[1], 'rb').read().decode('utf-16-le', errors='ignore'))" {filename}
6. If still garbled, try UTF-16 BE: python -c "import sys; print(open(sys.argv[1], 'rb').read().decode('utf-16-be', errors='ignore'))" {filename}
7. For files with mixed encoding or corruption: Use errors='replace' or errors='ignore' to skip bad bytes: python -c "print(open('{filename}', 'rb').read().decode('utf-16-le', errors='replace'))"
8. Extract key sections even if some text is corrupted: Look for CREATE PROCEDURE (usually readable), parameter list (@param), table names (FROM/JOIN/INTO), function calls (dbo.fn*)
9. Save converted text to temp file if needed for further analysis: bash -c "iconv -f UTF-16LE -t UTF-8 '{filename}' > /tmp/converted.sql" then read /tmp/converted.sql
10. Document encoding issue in analysis: Note "File had UTF-16 encoding, converted for analysis" so future readers know why manual conversion was needed

## Pitfalls
- Do NOT give up if first encoding attempt fails - try at least 3 encodings (UTF-16LE, UTF-16BE, UTF-8)
- Do NOT use read tool's offset parameter with binary/encoded files - convert entire file first, then use offset on converted version
- If bash/iconv/python all fail, try: file {filename} to identify exact encoding, then search for encoding-specific conversion tool
- On Windows (Git Bash), iconv may be missing - use Python approach as fallback
- Do NOT assume all .sql files in same folder have same encoding - SSMS may export different files with different encodings based on original database collation

## Verification
1. Converted text contains readable CREATE PROCEDURE statement
2. Parameter declarations (@param) are visible and readable
3. Table names and SQL keywords (SELECT, INSERT, FROM, WHERE) are readable
4. No garbled characters in critical business logic sections (even if some comments/headers are corrupted)
5. If verification fails, document what IS readable (e.g., signature but not body) and mark for manual review