---
name: cross-service-verification
description: Use when verifying that a cross-service change was applied correctly. Checks for stale references, contract mismatches, uncommitted changes, and broken imports across all services.
---

# Cross-Service Verification

## Overview

After any multi-service change, verify that every service is consistent before declaring done.

**Core principle:** Evidence before claims, always. A passing grep is proof. "Should work" is not.

## Verification Checklist

### 1. No Stale References
```bash
# For a rename (e.g., role → account_type):
grep -rn "role" services/ --include="*.py" | grep -v "account_type"
# Must return 0 results
```

### 2. Contracts Match Code
For each service with API changes:
- Read the contract for that service
- Read the actual endpoint code
- Field names, types, and structure must match exactly

### 3. All Changes Committed
```bash
for svc in services/*/; do
  echo "=== $(basename $svc) ==="
  cd "$svc" && git status --short && cd ../..
done
# Must show no uncommitted changes
```

### 4. All Services Import
```bash
for svc in services/*/; do
  cd "$svc" && python -c "from app import app; print('OK')" 2>&1 && cd ../..
done
```

### 5. Downstream Consumers Handle New Shape
For each service that reads from a changed upstream:
- Does it use the new field names?
- Does it use `.get()` with defaults for optional fields?
- Would it crash if the field is null/missing?

## When Verification Fails

Report specific failures:
- File path and line number
- What's wrong (stale ref, missing field, wrong type)
- What the fix should be

Then delegate fixes to the service worker and re-verify.
