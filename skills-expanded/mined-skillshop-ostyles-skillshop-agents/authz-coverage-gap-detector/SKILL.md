---
name: authz-coverage-gap-detector
description: "Finds mutating endpoints that lack explicit authorization, relying solely on middleware inheritance - the dangerous gaps where middleware failure leaves endpoints unprotected. Read-only. Audience: Senior. Trigger: /authz-coverage"
trigger: /authz-coverage
---

## What this is for

Authorization-xray builds the permission matrix per route. What it does not surface: which mutating endpoint has NO explicit check because it inherits implicitly from middleware. The dangerous gaps are the ones where inheritance is the only protection - when middleware crashes or short-circuits, the endpoint has no fallback check. This skill catalogs every mutating route and classifies each as explicitly-checked, implicitly-inherited (gap), or unprotected.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## ## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

### Step 1

1. If `-help` is passed, print the `## Usage` block below and stop.

### Step 2

2. Confirm `-ProjectDir` is provided and the path exists.

### Step 3

3. Run: `scripts/authz-gaps.ps1 -ProjectDir "<path>"`

### Step 4

4. LLM reads the JSON output. Per unprotected mutating endpoint (`gapRoutes`):

### Step 5

- Does this route have an inherited middleware-mount before it (`onlyInheritsAuthz`)?

### Step 6

- What happens when the parent middleware fails silently or crashes?

### Step 7

- Does the handler have an early-exit local check in the first few lines (missed by proximity heuristic)?

### Step 8

- What is the concrete abuse path if an attacker hits this endpoint without valid auth?

### Step 9

- Severity: is the data at risk sensitive (PII, payment, admin)?

### Step 10

5. Write `authz-coverage-report.md` to the working directory.

## Usage

```
/authz-coverage                            # interactive
/authz-coverage <dir>                      # scan project
/authz-coverage -help                      # show usage
```

Returns JSON with:
- `mounts[]`: `{file, line, mountLine}` - middleware authz mount sites
- `localChecks[]`: `{file, line, checkLine}` - explicit local authz checks
- `mutatingRoutes[]`: `{file, line, routeLine}` - POST/PUT/PATCH/DELETE routes
- `gapRoutes[]`: `{file, line, route, onlyInheritsAuthz}` - mutating routes without explicit check
- `counts`: summary statistics
