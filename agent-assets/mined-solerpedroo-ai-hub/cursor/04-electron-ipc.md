---
description: Electron main/preload/renderer split, typed IPC, Windows-first
globs: "apps/desktop/**"
alwaysApply: false
---

# Electron IPC

Three processes, three folders. Do not leak Node into the renderer.

- `main`: gateway, db, keytar, net, filesystem, global shortcuts, tray
- `preload`: `contextBridge` + allowlisted methods; parse with Zod
- `renderer`: React UI only

```ts
// preload: expose a narrow API
contextBridge.exposeInMainWorld("hub", {
  chat: { send: (dto: unknown) => ipcRenderer.invoke("chat:send", dto) },
});
```

- Disable `nodeIntegration`; enable `contextIsolation`.
- Channel names namespaced (`chat:send`, `keys:test`). No wildcard IPC.
- Overlay / tray / Quick AI are still renderer surfaces — they use the same preload. Caps and receipts still apply.
- Abstract OS differences (Ctrl vs Cmd, keytar backend). Verify on Windows first.

Conversation lists: virtualize when rendering history. Do not block main with heavy CPU on the send path.
