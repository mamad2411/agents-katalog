---
name: systematic-debugging
description: Use when a verification gate fails and the next fix needs reproducible diagnosis instead of speculative patching.
---

# Systematic Debugging

## Loop
1. Reproduce the failure with the smallest exact command.
2. Capture expected vs actual behavior.
3. Form one hypothesis at a time.
4. Add instrumentation or a focused test to falsify it.
5. Apply the smallest fix, then rerun the failing command and the relevant regression suite.

Never batch unrelated fixes in one debugging loop.

