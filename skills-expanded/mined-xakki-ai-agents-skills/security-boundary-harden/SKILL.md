---
name: security-boundary-harden
description: 'Harden a scoped security boundary while preserving behavior and verifying the actual controls. Use when asked to tighten security of a component. RU: усилить безопасность.'
disable-model-invocation: true
---

# Security hardening

Establish the requested threat boundary, affected assets, supported behavior, current candidate and permitted observations before changing anything. Trace actual input, authorization and side-effect paths. Do not print credentials or inspect secret stores merely to understand a configuration schema; use controlled synthetic values when possible.

Define the promised security property and choose focused evidence that can exercise its failure mode. Validate public entrypoints and downstream boundaries, including refusal behavior, logs, network and persistence as relevant. A rejected request alone does not prove no side effect; a passing fake does not prove the real transport. Use isolation and negative controls where permitted and proportionate.

Implement the smallest authorized hardening that preserves supported behavior. Run relevant sanctioned checks and reverify the final artifact. Report what was observed, untested paths and residual risk; do not bypass a native security refusal or silently change unrelated authentication, deployment, firewall or runtime policy.
