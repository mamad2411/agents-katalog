---
name: file-ops
version: 1.0.0
description: Read and write files in the workspace
uses: []
requires:
  tools: []
  env: []
security:
  risk_level: write
  capabilities:
    - file:read
    - file:write
  requires_approval: false
---

# File Operations

Read and write files within the workspace. This is a foundational skill that all agents use to interact with the file system.

## Execution Model

This is a **builtin skill** (`handler: type: builtin`). When `read_file` or `write_file` is invoked, the executor performs the file I/O operation directly. Paths are resolved relative to the workspace root. The tool schema in tool.yaml defines the external contract; the executor handles the operations directly.

## When to Use

- Reading source code, configuration, or documentation files
- Writing new files (code, config, docs)
- Updating existing files
- Reading agent memory or skill files
- Writing artifacts, reports, or analysis results

## Methodology

### 1. Reading Files

Before reading, verify:
- **Path exists**: Ensure the file path is valid
- **Purpose**: Know what information you need from the file
- **Size**: Large files may need partial reading or summarization

### 2. Writing Files

Before writing, verify:
- **Read first**: Understand existing content before overwriting
- **Path is correct**: Verify you're writing to the intended location
- **Content is complete**: Don't write partial content that corrupts a file
- **Not sensitive**: Don't write credentials, tokens, or other secrets

### 3. File Path Conventions

- Use relative paths when possible (keeps files within workspace)
- Use forward slashes for cross-platform compatibility in configuration
- Never write outside the workspace without explicit permission

## Output Format

```
## File Operation

### Read
- Path: [file path]
- Size: [bytes]
- Content: [file content or summary]

### Write
- Path: [file path]
- Bytes written: [count]
- Created directories: [yes/no]
```

## Quality Criteria

- Paths are resolved within the workspace boundary
- Sensitive files (.env, credentials) are blocked from read/write
- Parent directories are created automatically when writing
- Existing files are read before being overwritten (when modifying)
- File content is complete and valid (not truncated or corrupted)
- Operations report success or failure clearly

## Common Mistakes

- **Writing without reading first**: Overwriting a file you haven't read loses existing content. Always read before modifying.
- **Writing sensitive data**: Never write API keys, passwords, or tokens to files. These end up in version control.
- **Using absolute paths unnecessarily**: Absolute paths break when the workspace moves. Use relative paths unless you need to reference files outside the workspace.
- **Partial writes**: Writing incomplete content (e.g., truncated JSON or YAML) corrupts files. Ensure content is complete before writing.
- **Not checking blocked patterns**: Files matching blocked patterns (.env, credentials, secrets) are protected. Don't try to circumvent this.
- **Forgetting file encoding**: Always write text as UTF-8. Don't assume a particular encoding without checking.

## Completion

A file operation is complete when:
- Read: File content is returned successfully, or a clear error is reported
- Write: File is written to the correct path with the correct content
- The operation result is confirmed (file exists, content matches)
