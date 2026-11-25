---
name: safe-patch
purpose: Apply one approved bounded patch, respecting file leases, protected paths, and hash tracking.
tools: safe_patch, code_tools
verification_gate: Hash_And_Diff_Check
---

# Safe Patch Skill
Surgically modifies source files while preserving public contracts.
