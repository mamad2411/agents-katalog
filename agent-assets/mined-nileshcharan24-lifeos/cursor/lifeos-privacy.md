---
auto_attach:
  - "src/features/**"
  - "src/context/**"
---

## Privacy & Deep Mode Rules (Auto-Attached)

- Always check the **Deep Mode** toggle state before rendering or returning `is_private` or otherwise sensitive data.
- In **Normal Mode**, hide, redact, or aggregate sensitive Deep Mode data.
- Ensure that logs, analytics, and error messages **never leak Deep Mode details**.
