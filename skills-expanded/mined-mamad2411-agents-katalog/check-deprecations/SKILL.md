---
name: check-deprecations
description: Check a file for usage of symbols marked @deprecated via JSDoc. Use when asked to "check for deprecated usage", "find deprecated calls", "are there any deprecated APIs here", or "/check-deprecations <file>".
allowed-tools: Bash(npx --yes check-deprecations *), Bash(check-deprecations *)
---

# check-deprecations

Scan a source file for calls to symbols tagged `@deprecated` in their JSDoc.

## Usage

```bash
npx --yes check-deprecations <file>
```

If the binary is already on PATH, you may use it directly:

```bash
check-deprecations <file>
```

## Determining the file

- If the user supplied a path as an argument, use it.
- If there is an active editor selection or recently mentioned file, use that.
- Otherwise ask the user which file to check.

## Interpreting results

| Exit code | Meaning                                                               |
| --------- | --------------------------------------------------------------------- |
| `0`       | No deprecated usage — tell the user the file is clean.                |
| `1`       | Deprecated usage found — report each hit to the user.                 |
| `2`       | Error (file not found or missing argument) — relay the error message. |

Each hit is formatted as:

```
<file>:<line>:<col> - <message>
  <source line>
```

Report hits exactly as printed. If there are many, summarise the count and list them.
