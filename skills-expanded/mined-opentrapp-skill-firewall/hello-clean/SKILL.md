---
name: hello-clean
description: A minimal benign skill used to dogfood the Skill Firewall action in CI.
---

# Hello, clean skill

This skill does nothing dangerous. It exists so the action can scan a known clean
input on every push and prove the gate passes. A malicious skill in its place would
fail the job, which is the whole point.
