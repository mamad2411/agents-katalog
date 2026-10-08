---
name: forge-surface-audit
description: Check background color hierarchy. Verifies that surfaces, cards, and modals use the correct token from your system.
user-invokable: true
---

# /forge-surface-audit — Surface Audit

Scan all background-color declarations:

1. Page background should use --surface
2. Cards should use --surface-elevated
3. Inputs/recessed areas should use --surface-sunken
4. Modals should use --surface-elevated with shadow
5. Flag backgrounds using raw hex instead of tokens
