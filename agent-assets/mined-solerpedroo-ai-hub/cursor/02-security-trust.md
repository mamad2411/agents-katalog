---
description: Trust boundary — secrets, IPC, redaction, no silent fallback
alwaysApply: true
---

# Security and trust

```text
Renderer → Preload (Zod DTOs) → Main (keys, db, net, fs)
```

## Must

- Secrets only in **keytar**. Never SQLite, git, logs, React state, or full key over IPC (mask `sk-…xxxx`).
- Provider HTTP, SQLite, `fs`, `child_process` only in **main**.
- Validate every IPC payload with Zod.
- Redact API keys, tokens, Bearer headers in errors, debug UI, packets, exports.
- Crash reporter / telemetry: opt-in, no conversations, no PII, no keys.
- Spend caps are hard-stops. Fallback to another model is **user-confirmed**.

## Must not

```ts
// ❌ renderer
import { chat } from "openai";
webPreferences: { nodeIntegration: true }

// ✅ renderer talks DTO only
const result = await window.hub.chat.send(input); // input zod-parsed in preload/main
```

If a feature needs Node APIs in the UI, add a main-process method. Do not weaken the boundary.
