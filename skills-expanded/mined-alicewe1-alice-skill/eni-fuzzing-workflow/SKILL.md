---
name: eni-fuzzing-workflow
description: "[DOCUMENTATION ONLY] [仅文档] Coverage-guided fuzzing workflow for local or authorized targets, including harnesses, corpus design, sanitizers, campaigns, minimization, triage, and regression."
x-alice-class: reverse
---

> 仅文档：本 Skill 提供方法与检查表，不宣称自带可执行脚本。

# Fuzzing Workflow

Define the parser or API boundary. Build a deterministic harness, tiny valid seed corpus, dictionary, sanitizer build, and time budget. Run campaigns, minimize crashes, deduplicate root causes, reproduce under a debugger, and convert confirmed crashes into regression tests.

Persist checkpoints before long runs. Record commands, versions, hashes, evidence paths, assumptions, and verification results. Chain through eni-universal-workflow and finish with delivery.
