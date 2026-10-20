---
description: Deterministic demo mode and mock tools
globs: src/agent/**/*.ts
alwaysApply: false
---

# Demo mode

Talk demos must not depend on live travel APIs.

- Tools in `src/agent/tools.ts` simulate latency (500–1500ms) and return typed mock data.
- `src/agent/demo-script.ts` is the scripted talk path, triggered by “Plan the Spiti trip”: plan → adapt → weather → approve.
- Label mock inventory as demo data in the UI.
- Live mode is optional. Keep this scripted path as the fallback when there is no API key or the talk cannot depend on a network.
