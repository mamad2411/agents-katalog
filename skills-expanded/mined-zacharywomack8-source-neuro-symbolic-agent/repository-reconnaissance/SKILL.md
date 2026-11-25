---
name: repository-reconnaissance
purpose: Map repository structure, identify Bazel/pytest targets, and produce evidence-backed maps.
tools: filesystem_read, list_dir
verification_gate: None
---

# Repository Reconnaissance Skill
Maps files, build targets, and dependencies without modifying workspace state.
