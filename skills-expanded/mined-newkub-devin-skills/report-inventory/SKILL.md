---
name: check-secrets-report-inventory
description: Build a secrets inventory report — keys/vars in use, missing, leaked — with redaction rules
argument-hint: "[scope]"
related:
  - report
  - follow-secret-manager
  - open-web-for-config-secret
---

## Goal

Build a secrets inventory report from the findings of the `check-secrets` workflows — covering env vars, hardcoded values, and leaks — with safe redaction

## Scope

- Use when `/check-secrets` dispatches to `report`/`inventory`, or invoke standalone
- Output: inventory table in chat — for a persistent artifact use `/create-report-in-dot-devin` (caution: the artifact must contain no secret values)

## Execute

### 1. Aggregate Findings

> Goal: combine the results of every secrets check

1. Merge findings from the `env-vars`, `hardcoded-values`, `secrets-leak` workflows (or only the ones that ran)
2. Group by: `required-but-missing`, `present-and-used`, `hardcoded`, `leaked`, `unused`

### 2. Build Inventory

> Goal: an inventory that points to where to fill/edit values without exposing them

1. Table: `No.`, `Key`, `Location`, `Status`, `Used By`, `Action`
2. Redaction rules: show only the key name + type (`sk_...`, `whsec_...`) — never print a value, not even part of one
3. For missing env vars → build an inventory table pointing to the key/URL/entry point, then recommend `/open-web-for-config-secret`

### 3. Report

> Goal: summarize the secrets posture

1. Counts per status + verdict (`clean` / `gaps` / `leaks-found`)
2. Leaks are always Critical — recommend rotating and moving to `/follow-secret-manager`
3. Run `/suggest-next-action`

## Rules

- Never print secret values in the report under any circumstance — mask everything except the key name
- Leaked secrets → note which commit/file so rotation can be tracked
- If persisting an artifact → double-check that the report file holds no real values

## Expected Outcome

- Inventory table with status and actions per key
- Secrets posture verdict without exposing any values
