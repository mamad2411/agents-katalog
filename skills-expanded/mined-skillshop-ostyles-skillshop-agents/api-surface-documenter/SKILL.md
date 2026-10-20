---
name: api-surface-documenter
description: "API surface documenter: extracts ALL API surface types from a codebase - REST routes, event handlers, CLI commands, library exports. Classifies stability and generates a complete reference. No Swagger decorations needed. Read-only. Audience: Both. Trigger: /api-survey"
trigger: /api-survey
---

## What this is for

Every codebase has an API surface - REST endpoints, event listeners, CLI
commands, and library exports - but it's rarely documented in one place.
Swagger/OpenAPI only covers REST. This skill finds ALL four surface types
from source code patterns alone, classifies each by stability and audience
(internal vs external), and produces a complete reference.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## ## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

### Step 1

1. If `-help` is passed, print the `## Usage` block below and stop.

### Step 2

2. Confirm `-ProjectDir` is provided and the path exists.

### Step 3

3. Run: `scripts/api-survey.ps1 -ProjectDir "<path>"`

### Step 4

4. LLM reads the JSON output. For each API:

### Step 5

- **Usage pattern:** How is this API typically called? What are the

### Step 6

conventions in this codebase?

### Step 7

- **Breaking-change risk:** Would changing the signature/route/event-name

### Step 8

break callers? Is it exported externally?

### Step 9

- **Undocumented assumptions:** Are there implicit preconditions (auth

### Step 10

required, rate-limited, idempotent)?

### Step 11

- **Missing examples:** Is there a usage example in docs/tests? If not,

### Step 12

note it.

### Step 13

5. Write `api-surface-reference.md` to the working directory.

## Usage

```
/api-survey                          # interactive
/api-survey <dir>                    # scan project
/api-survey -help                    # show usage
```

Returns JSON with `apis[]`:
`{file, line, apiType (rest/event/cli/lib), name, method (for rest), route/event/command, params[], hasDocs}` plus summary counts.

<｜DSML｜tool_calls>
<｜DSML｜invoke name="write">
<｜DSML｜parameter name="filePath" string="true">C:\Users\ostol\Desktop\AGENTS\skills\understanding\api-surface-documenter\README.md