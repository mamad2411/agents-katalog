---
name: root-cause-tracing
description: Use after the same bug signature recurs two or more times so fixes stop treating symptoms and identify the causal chain before further edits.
---

# Root-cause Tracing

## 5-Why loop
1. State the repeated bug signature and evidence.
2. Ask why it happened; answer from observed facts only.
3. Repeat until reaching a process, design, test, or dependency cause.
4. Define a prevention change and a verification step.
5. Resume implementation only after adding or updating a failing test that captures the cause.

