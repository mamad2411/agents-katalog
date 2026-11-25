---
name: eni-supply-chain-assurance-lane
description: "[DOCUMENTATION ONLY] [仅文档] Supply-chain assurance workflow for sequential eni-solo execution."
x-alice-class: assist
---

# Supply-chain assurance workflow

> 仅文档：本 Skill 提供阶段方法，不自带审批或打分引擎。

Execute `manifest-inventory → sbom → provenance → advisory-match → reachability → build-ci-trust → remediation → regression → verify → deliver`. Use installed SBOM, signature, dependency, and build tools directly.
