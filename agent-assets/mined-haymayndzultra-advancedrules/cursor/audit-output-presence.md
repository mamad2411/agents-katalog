---
description: "Ping kapag present ang Summary_Report.md (audit output)."
globs: ["memory-bank/plan/Summary_Report.md"]
alwaysApply: false
---

<rule>
name: audit_output_presence
description: Detect Summary_Report.md exists.
actions:
  - type: suggest
    message: "✓ Detected: memory-bank/plan/Summary_Report.md (audit output present)."
</rule>
