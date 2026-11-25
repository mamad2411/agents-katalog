---
name: minimal-patch
description: Make a small, targeted code change when the user asks for a surgical fix or scope control matters. Use for bug fixes and local behavior changes, not broad redesigns.
---

# Minimal patch

Reproduce or identify the precise failing behavior and its owner. Preserve public interfaces and nearby conventions unless the requirement needs them changed. Prefer the smallest coherent edit that fixes the cause; avoid unrelated formatting, refactors, dependency updates, and speculative hardening.

Run the narrowest meaningful verification, then inspect the diff for unintended edits. Report the behavioral change, evidence, and any remaining risk. If a wider change is necessary, explain the coupling before expanding scope.
