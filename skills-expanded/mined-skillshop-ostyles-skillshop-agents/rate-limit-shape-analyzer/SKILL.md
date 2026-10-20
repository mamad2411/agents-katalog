---
name: rate-limit-shape-analyzer
description: "Rate-limit shape analyzer: inventories rate-limit decorators per-route (express-rate-limit, flask-limiter, DRF throttle, Spring). Per endpoint, classifies whether it has a decorator, on what limit (max, window, per-tier), and whether mutating endpoints that should be limited are. Read-only. Audience: Senior. Trigger: /rate-shape"
trigger: /rate-shape
---

## What this is for

Rate-limits exist or not - but how are they CONFIGURED. Per endpoint per
user-tier per action-tier? Where is the gap (cheap read open, expensive
export with no limit)? `input-validation-audit` looks at inputs, not at
abuse-surfaces. Missing: which endpoints are expansive but unprotected.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## ## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

### Step 1

1. If `-help` is passed, print the `## Usage` block below and stop.

### Step 2

2. Confirm `-ProjectDir` is provided and the path exists.

### Step 3

3. Run: `scripts/rate-policy-scan.ps1 -ProjectDir "<path>"`

### Step 4

4. LLM reads the JSON output. For each missing-limit finding:

### Step 5

- Is this endpoint expansive? (costly DB query, file/external call,

### Step 6

bulk operation)

### Step 7

- Is the protection only on read but not on write?

### Step 8

- Is the limit per-tier (free vs pro) different than per-IP?

### Step 9

5. Recommend: same limit everywhere, with auth-tier differentiation.

### Step 10

6. Write `rate-shape-report.md` to the working directory.

## Usage

```
/rate-shape                              # interactive
/rate-shape <dir>                        # scan project
/rate-shape -help                        # show usage
```

Returns JSON with `limitedRoutes[]`, `mutatingRoutes[]`,
`missingLimits[]` plus summary counts.
