---
name: settings-architecture
description: "Organize preferences and controls so people find what they need without getting lost. Information grouping, search, and defaults. Use when building settings pages, preference panels, or admin surfaces."
---

# Settings Architecture

Organize preferences so people find what they need without getting lost.

## How to use

- `/settings-architecture` Apply settings constraints to this conversation.

## Constraints

### Organization
- MUST group by user task, not by system architecture
- Group order: Profile > Notifications > Integrations > Billing > Security > Advanced
- MUST include search for settings pages with 10+ options
- SHOULD show current value alongside each setting label
- NEVER nest settings more than 2 levels deep

### Defaults
- Every setting MUST have a sensible default that works for 80% of users
- MUST show what the default is so users know what they're changing
- Dangerous settings (delete account, data export) MUST require confirmation
- SHOULD explain the consequence of each setting in plain language

### Anti-Patterns
- Settings that require a page reload to take effect without warning
- Boolean toggles for things that need more nuance (use radio groups)
- Hiding essential settings behind "Advanced" labels
- Settings pages as the first screen after signup
- Settings that don't save automatically (or don't clearly indicate when they save)
