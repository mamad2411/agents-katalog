---
name: read-code-context
description: Reads source code around a specific line to provide context for debugging. This is a system tool.
version: 1.0.0
category: universal/debugging
level: atomic
execution_type: action
tags: [system, file-io, context]

input:
  type: object
  required: [file, line]
  properties:
    file:
      type: string
      description: Path to the source file
    line:
      type: integer
      description: The target line number
    source_path:
      type: string
      description: Optional base path to resolve relative file names
    window:
      type: integer
      description: Number of lines to read above and below (default 5)

output:
  type: object
  properties:
    code_context:
      type: string
      description: The extracted code lines with line numbers
    file_found:
      type: string
      description: Absolute path of the file read
---

# Read Code Context

## Goal
Fetch actual source code from disk to allow the Agent to see the buggy implementation.

## Instructions
This is a SYSTEM ACTION. The SkillExecutor will call a built-in Python function to read the file. 
No LLM reasoning is required for this specific skill.
