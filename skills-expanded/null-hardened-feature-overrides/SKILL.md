---
name: null-hardened-feature-overrides
description: "Validate remote numeric override maps defensively so null, non-finite, or negative flag payloads never corrupt runtime thresholds."
metadata:
  author: ychampion
---

# SKILL: Null-Hardened Feature Overrides
**Domain:** remote-bridge  
**Trigger:** Apply when remote feature flags or runtime override maps can influence thresholds, but the flag service may return null or malformed values.
**Source Pattern:** Distilled from reviewed remote override and transport-boundary patterns.

## Core Method
Treat remote override values as untrusted input rather than configuration you can index directly. Validate the flag payload type, require finite positive numbers, and fall back to the hardcoded default when the override is null, missing, non-object, or otherwise malformed. Preserve hard opt-outs, such as `Infinity` for tools that self-bound their output, before consulting the remote override layer.

## Key Rules
- Guard the override container itself before indexing into it; null or non-object flag payloads must fall back cleanly.
- Accept only finite positive numbers as overrides; reject zero, negatives, `NaN`, and infinities.
- Preserve hard opt-out semantics like `Infinity` before consulting override maps so remote flags cannot re-enable disabled behavior.
- Clamp fallback behavior against the declared local default instead of trusting remote values to stay within safe bounds.

## Example Application
If a growth experiment can adjust persistence thresholds per tool, validate the experiment payload before using it; malformed data should simply leave `getPersistenceThreshold` and `getPerMessageBudgetLimit` on their safe defaults rather than crashing the result-storage path.

## Anti-Patterns (What NOT to do)
- Do not assume the flag cache always returns a well-formed object; stale or null payloads are part of the contract.
- Do not let a remote override bypass a local hard opt-out, or tools that intentionally self-bound their output can become circular again.
