---
name: config-surface-documenter
description: "Extracts the full configuration surface from code (env vars, config files, CLI flags) and generates a human-readable reference with descriptions, types, defaults, and effects. Read-only. Audience: Both. Trigger: /config-docs"
trigger: /config-docs
---

## What this is for

Every env var, config file, and CLI flag lives in code - but none is documented. New developers hunt through code to find what PORT defaults to. This skill extracts the entire configuration surface and generates a reference manual.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## ## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

### Step 1

1. If `-help` is passed, print the `## Usage` block below and stop.

### Step 2

2. Confirm `-ProjectDir` is provided and the path exists.

### Step 3

3. Run: `scripts/config-doc-scan.ps1 -ProjectDir "<path>"`

### Step 4

4. LLM reads the JSON output. Per config key:

### Step 5

- What does this key control? Describe in one sentence.

### Step 6

- What is the effect of changing the value?

### Step 7

- Is this safety-critical (secret, production flag)?

### Step 8

- Is there a recommended default for production vs development?

### Step 9

- Is the key orphaned (defined but never read)?

### Step 10

5. Write `config-reference.md` to the working directory.

## Usage

```
/config-docs                            # interactive
/config-docs <dir>                      # scan project
/config-docs -help                      # show usage
```

Returns JSON with `configKeys[]` each having `{name, source, type, defaultValue, usageSites[], isSecret}`.
