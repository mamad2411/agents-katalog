---
name: eni-code-security-workflow
description: "[DOCUMENTATION ONLY] [仅文档] Source, dependency, supply-chain, SAST, SCA, and remediation workflow for operator-owned repositories."
x-alice-class: assist
---

> 仅文档：本 Skill 提供方法与检查表，不宣称自带可执行脚本。

# Code Security Workflow

Build a language and dependency inventory. Threat-model entry points. Combine Semgrep-style pattern scans, OSV dependency matching, Trivy-style SBOM and configuration review, and manual data-flow validation. Reproduce each finding, fix a copy or branch, and add regression tests.

Persist checkpoints before long runs. Record commands, versions, hashes, evidence paths, assumptions, and verification results. Chain through eni-universal-workflow and finish with delivery.
