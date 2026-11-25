---
name: execute-sandbox
description: Use `execute-sandbox` to get Execute Sandbox Instructions when accessing/manipulating sandboxes - run commands in, inspect, edit, copy files in isolated sandboxes.
---

# Execute Sandbox Instructions

Use sandbox tools for isolated command execution and file inspection without changing the host project.

## Lifecycle tools

- `autocode_sandbox_cli`: run shell commands inside an existing sandbox.

## File tools

- `autocode_sandbox_read`: read files inside a sandbox.
- `autocode_sandbox_glob`: find sandbox files by glob.
- `autocode_sandbox_grep`: search sandbox file contents.
- `autocode_sandbox_edit`: edit sandbox files.
- `autocode_sandbox_copy`: copy files between local project paths and sandbox paths.

## Sandbox paths

Special mounts inside sandbox relative to Sandbox root:

- `/sandbox`: writable sandbox directory for sandbox tasks: scratch area, generated outputs, experiments, etc.
- `/home`: writable home directory for config files, caches, package manager state, shell history, etc.
- `/workspace`: read-only mount of the project workspace for inspection only.

## Path rules

- Use relative paths only.
- Do not use absolute paths.
- Do not use `..` to escape roots.
- Do not include NUL bytes.
- Local paths are relative to the project root.
- Sandbox paths are relative to the sandbox root.
- Do not copy from `/workspace`; copy from local project paths into the sandbox instead.

## Copy behavior

`autocode_sandbox_copy` copies local project files to sandbox paths, or sandbox files back to local project paths when supported. Existing destinations are not replaced unless overwrite is enabled.
