---
name: microsoft-store-readiness
description: Prepare Microsoft Store release readiness for Windows apps, desktop utilities, games, PWAs, and packaged software including package identity, MSIX/AppX packaging, Store listing, screenshots, age ratings, privacy, capabilities, in-app purchases, subscriptions, updates, certification, installer behavior, Windows integration, telemetry, crash quality, support links, and release rollout. Use when submitting or auditing products for Microsoft Store.
---

# Microsoft Store Readiness

Use this skill to reduce Microsoft Store submission risk and make Windows distribution supportable.

## Workflow

1. Identify app type, package model, Store category, monetization, capabilities, supported devices, and Windows integration.
2. Read `references/microsoft-store-systems.md`.
3. Audit package identity, manifest capabilities, listing assets, privacy/support, monetization, quality, certification, rollout, and support readiness.
4. Separate Store-specific requirements from general Windows release readiness.
5. Produce a submission matrix, blockers, reviewer notes, telemetry plan, and support checklist.

## Guardrails

- Do not claim Store features, device support, privacy behavior, or in-app purchase support that the build does not implement.
- Do not hide background tasks, restricted capabilities, or external payment flows from review notes.
- Verify current Microsoft Store policies before submission; this skill is product readiness guidance, not policy/legal advice.

## Output format

```text
Microsoft Store context:
Package/monetization model:

Submission matrix:
- package identity:
- listing/assets:
- capabilities/privacy:
- monetization:
- quality/certification:
- rollout/support:

P0 blockers:
- <blocker> -> evidence needed

Reviewer notes:
- <note>
```
