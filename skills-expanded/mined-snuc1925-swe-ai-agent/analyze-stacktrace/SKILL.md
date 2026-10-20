---
name: analyze-stacktrace
description: Analyzes an exception stacktrace to pinpoint the exact source file, line number, and the variable or root cause.
version: 1.0.0
category: universal/debugging
level: atomic
tags: [stacktrace, debug, troubleshooting]

input:
  type: object
  required: [stacktrace, source_path]
  properties:
    stacktrace:
      type: string
      description: Full Java exception stacktrace text
    source_path:
      type: string
      description: Root path of the Java source code

output:
  type: object
  properties:
    file:
      type: string
      description: Source file where the error originated (prefer absolute path if present in the stacktrace)
    line:
      type: integer
      description: Line number where the exception occurred
    variable:
      type: string
      description: The variable, object reference, or expression most likely causing the error
    error_type:
      type: string
      description: The exception class name (e.g. AttributeError, NullPointerException)

constraints:
  host:
    os: [linux, darwin, windows]
  resources:
    memory: "256MB"
    timeout: "30s"
  safety:
    fs_access: read-only
    requires_approval: false
---

## Instructions

1. Parse the stacktrace line by line.
2. Find the FIRST stack frame that belongs to user project code — skip frames from standard libraries (java.*, sun.*, builtins, etc.) and third-party frameworks.
3. From that frame, extract: the file path and the line number. If the stacktrace includes an absolute path, output the absolute path. Otherwise output the most specific path you can.
4. Identify the exception type and the error message to pinpoint the problematic variable or root cause. In Python 3.11+, use the `^^^^` markers to find the exact expression. In Java, check the "Cannot invoke ... because X is null" message.
5. Return file, line, variable, and error_type as JSON — nothing else.
