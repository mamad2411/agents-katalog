---
name: integration-landscape
description: "Maps every external integration from code: HTTP APIs, databases, message queues, storage. Classifies protocol, auth type, criticality, retry/fallback coverage. Read-only. Audience: Senior. Trigger: /integrations"
trigger: /integrations
---

## What this is for

Every project calls external services. When Stripe is down, what breaks? When SendGrid times out, does the whole API fail or just the email feature? This skill maps all integrations with their criticality, resilience patterns, and outage impact.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## ## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

### Step 1

1. If `-help` is passed, print the `## Usage` block below and stop.

### Step 2

2. Confirm `-ProjectDir` is provided and the path exists.

### Step 3

3. Run: `scripts/integration-scan.ps1 -ProjectDir "<path>"`

### Step 4

4. LLM reads the JSON output. Per integration:

### Step 5

- What is this integration used for? What business feature depends on it?

### Step 6

- What happens when the service is down? Graceful degradation or crash?

### Step 7

- Is there a fallback/circuit-breaker/retry? If not, was the risk accepted?

### Step 8

- What monitoring signals exist (health check, timeout, error tracking)?

### Step 9

5. Write `integration-landscape.md` to the working directory.

## Usage

```
/integrations                            # interactive
/integrations <dir>                      # scan project
/integrations -help                      # show usage
```

Returns JSON with `integrations[]` each having `{type, target, protocol, authType, criticality, hasRetry, hasFallback}`.
