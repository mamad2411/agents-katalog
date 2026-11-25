---
name: debug-java-null-pointer
description: Full pipeline to debug a Java NullPointerException. Analyzes the stacktrace, locates the null variable, and provides actionable fix suggestions.
version: 1.0.0
category: java/debugging
level: composite
tags: [java, debug, null-pointer, pipeline, composite]

# Sub-skills are executed in ORDER. Output of each is merged into shared state
# and made available as input to the next sub-skill.
sub_skills:
  - analyze-stacktrace      # step 1: find file + line + variable
  - read-code-context       # step 2: read source context
  - suggest-java-fix        # step 3: generate fix using step 1 & 2

input:
  type: object
  required: [stacktrace, source_path]
  properties:
    stacktrace:
      type: string
      description: Full Java exception stacktrace
    source_path:
      type: string
      description: Root path of the Java source code

output:
  type: object
  properties:
    file:
      type: string
    line:
      type: integer
    variable:
      type: string
    fix_suggestion:
      type: string
    code_snippet:
      type: string

constraints:
  host:
    os: [linux, darwin, windows]
  resources:
    memory: "1GB"
    timeout: "120s"
  safety:
    fs_access: read-only
    requires_approval: false
---

## Instructions

This is a composite skill. The SkillExecutor handles the pipeline automatically:
1. Runs `analyze-stacktrace` → produces {file, line, variable}
2. Runs `read-code-context` → produces {code_context} from disk
3. Runs `suggest-java-fix` with all context → produces {fix_suggestion, code_snippet}
4. Returns the merged result as the final output.
