---
name: forge-harden
description: Add error states, loading states, i18n safety, and edge case handling using your design system's tokens.
user-invokable: true
---

# /forge-harden — Production Hardening

Make the interface production-ready:

1. Error states using --danger and --danger-subtle tokens
2. Loading states (skeleton using --surface-sunken)
3. Empty states with centered messaging
4. Text overflow handling (ellipsis, word-break)
5. Logical properties for RTL support (padding-inline, margin-block)
6. @supports checks for modern CSS features

All states use your system tokens, not hardcoded values.
