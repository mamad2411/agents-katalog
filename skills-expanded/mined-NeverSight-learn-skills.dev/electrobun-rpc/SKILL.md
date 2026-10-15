---
name: electrobun-rpc
description: "Typed bidirectional RPC between Bun and webview in Electrobun. Covers schema design, defineElectrobunRPC, createRPC, request/response patterns, fire-and-forget messages, Electroview setup, and encryption. Use when setting up communication between main process and browser views."
---

# Electrobun RPC — Typed Bun ↔ Webview Communication

> **Electrobun is NOT Electron.** Do not use Electron APIs (ipcMain, ipcRenderer, contextBridge, etc.).

## Mental Model

- **Schema-first:** Define types → derive handlers and callers. Types flow through generics to auto-complete method names, params, and responses.
- **Two sides:** `"bun"` (main process, runs in Bun) and `"webview"` (browser). Each side defines what it **handles** (incoming requests) and what it **receives** (incoming messages).
- **Two patterns:** Requests (async, returns a response) and messages (fire-and-forget, no response).
- **Bun side** uses `BrowserView.defineRPC("bun", ...)`. **Browser side** uses `Electroview.defineRPC(...)`.
- **Transport is automatic:** Encrypted WebSocket (per-webview AES-256-GCM) with native bridge fallback. You never configure transport manually.

## Decision Tree

| Need | Pattern |
|---|---|
| Response from other side? | Use **request** (`rpc.request.methodName(params)`) |
| Fire-and-forget notification? | Use **message** (`rpc.send.messageName(payload)`) |
| Setting up bun-side RPC? | `BrowserView.defineRPC<Schema>({ handlers: { ... } })` |
| Setting up browser-side RPC? | `Electroview.defineRPC<Schema>({ handlers: { ... } })` |
| Multiple webviews communicating? | Relay through bun process — no direct webview-to-webview |
| Need a catch-all request handler? | Use `_` key in request handler object |
| Need to listen for all messages? | Use `"*"` wildcard message handler |
| No RPC needed but need Electroview? | `Electroview.defineRPC<any>({ handlers: { requests: {}, messages: {} } })` |

## Canonical Patterns

### 1. Define a Shared Schema Type

The schema describes **both sides** in one type. `bun.requests` = what bun handles (webview calls these). `webview.requests` = what webview handles (bun calls these). Messages follow the same logic.

```ts
// src/shared/types.ts (or define in each file separately)
import type { RPCSchema } from "electrobun/bun";

type MyAppRPC = {
  bun: RPCSchema<{
    requests: {
      // Bun HANDLES these (webview calls them)
      getUser: { params: { id: string }; response: { name: string; email: string } };
      saveNote: { params: { title: string; content: string }; response: { success: boolean } };
    };
    messages: {
      // Bun RECEIVES these (fire-and-forget from webview)
      logEvent: { eventName: string; timestamp: number };
    };
  }>;
  webview: RPCSchema<{
    requests: {
      // Webview HANDLES these (bun calls them)
      getDocumentTitle: { params: {}; response: string };
    };
    messages: {
      // Webview RECEIVES these (fire-and-forget from bun)
      showNotification: { text: string };
    };
  }>;
};
```

**Request shape:** `{ params: ParamType; response: ResponseType }`. Use `{}` for no params, `void` for no response.

**Message shape:** Just the payload type directly — no `params`/`response` wrapper. Use `void` for no payload.

### 2. Bun-Side: Create RPC with Handlers

```ts
// src/bun/index.ts
import { BrowserView, BrowserWindow, type RPCSchema } from "electrobun/bun";

const rpc = BrowserView.defineRPC<MyAppRPC>({
  maxRequestTime: 5000, // optional, default 1000ms
  handlers: {
    requests: {
      // Sync handler
      getUser: ({ id }) => {
        return { name: "Alice", email: "alice@example.com" };
      },
      // Async handler
      saveNote: async ({ title, content }) => {
        await Bun.write(`notes/${title}.json`, JSON.stringify({ title, content }));
        return { success: true };
      },
    },
    messages: {
      logEvent: ({ eventName, timestamp }) => {
        console.log(`Event: ${eventName} at ${timestamp}`);
      },
      // Optional wildcard — receives ALL messages
      "*": (messageName, payload) => {
        console.log("Any message:", messageName, payload);
      },
    },
  },
});

const win = new BrowserWindow({
  title: "My App",
  url: "views://mainview/index.html",
  rpc, // ← pass RPC to window
});
```

### 3. Browser-Side: Create Electroview with RPC

```ts
// src/mainview/index.ts
import Electrobun, { Electroview } from "electrobun/view";

// Browser-side type — same structure, RPCSchema wrapper optional
type MyAppRPC = {
  bun: {
    requests: {
      getUser: { params: { id: string }; response: { name: string; email: string } };
      saveNote: { params: { title: string; content: string }; response: { success: boolean } };
    };
    messages: {
      logEvent: { eventName: string; timestamp: number };
    };
  };
  webview: {
    requests: {
      getDocumentTitle: { params: {}; response: string };
    };
    messages: {
      showNotification: { text: string };
    };
  };
};

const rpc = Electroview.defineRPC<MyAppRPC>({
  maxRequestTime: 5000,
  handlers: {
    requests: {
      getDocumentTitle: () => document.title,
    },
    messages: {
      showNotification: ({ text }) => {
        alert(text);
      },
    },
  },
});

const electrobun = new Electrobun.Electroview({ rpc });
```

### 4. Bun Calling Webview (Request)

```ts
// Bun side — call a webview handler, await response
const title = await win.webview.rpc?.request.getDocumentTitle({});

// Built-in: evaluate arbitrary JS in the webview
const result = await win.webview.rpc?.request.evaluateJavascriptWithResponse({
  script: "return document.title",
});
```

Always use `?.` — `rpc` can be undefined before the webview connects.

### 5. Webview Calling Bun (Request)

```ts
// Browser side — call a bun handler, await response
const user = await electrobun.rpc!.request.getUser({ id: "123" });
const result = await electrobun.rpc!.request.saveNote({
  title: "Hello",
  content: "World",
});
```

### 6. Sending Messages (Fire-and-Forget)

```ts
// Bun → webview (no response)
win.webview.rpc?.send?.showNotification({ text: "Saved!" });

// Webview → bun (no response)
electrobun.rpc!.send.logEvent({ eventName: "click", timestamp: Date.now() });
```

### 7. Wildcard Message Listener

Use `addMessageListener("*", ...)` to receive all incoming messages. Wildcard listeners fire **before** specific listeners.

```ts
// On either side (after createRPC or defineRPC)
rpc.addMessageListener("*", (messageName, payload) => {
  console.log(`Received message: ${String(messageName)}`, payload);
});

// Remove with the same function reference
rpc.removeMessageListener("*", myHandler);
```

### 8. Cross-Webview Communication via Bun Relay

Webviews cannot communicate directly. Route through bun:

```ts
// Bun side — relay from child to main window
const mainRpc = BrowserView.defineRPC<MainRPC>({
  handlers: {
    requests: {
      sendToChild: ({ message }) => {
        childWindow.webview.rpc?.send?.receiveMessage({ from: "Main", message });
        return { success: true };
      },
    },
    messages: {},
  },
});

const childRpc = BrowserView.defineRPC<ChildRPC>({
  handlers: {
    requests: {
      sendToMain: ({ message }) => {
        mainWindow.webview.rpc?.send?.receiveMessage({ from: "Child", message });
        return { success: true };
      },
    },
    messages: {},
  },
});
```

### 9. Wait for DOM Ready Before Sending Messages from Bun

```ts
win.webview.on("dom-ready", () => {
  win.webview.rpc?.send?.showNotification({ text: "Page loaded!" });
});
```

## Non-Negotiable Rules

1. **Always define schema types** for type safety — without them, you lose auto-complete and type checking on all RPC calls.
2. **Bun side = `"bun"`**, browser side = `"webview"` — don't mix. `bun.requests` = what bun **handles**, `webview.requests` = what webview **handles**.
3. **Request handlers must return the declared response type** — the return value is sent back as the RPC response.
4. **Messages are fire-and-forget** — no response is ever sent or received. Use requests if you need a return value.
5. **Don't communicate between webviews directly** — always relay through the bun process.
6. **Always pass `rpc` to `BrowserWindow`** on the bun side — without this, the transport is never connected.
7. **Always instantiate `Electroview`** on the browser side — `new Electrobun.Electroview({ rpc })` wires up the WebSocket transport.

## Common Pitfalls

### 1. Confusing which side handles which requests

`bun.requests` are what bun **handles** (incoming to bun), not what bun sends. The webview **calls** `bun.requests`. This is the most common source of confusion.

```ts
// ❌ WRONG mental model: "bun.requests = what bun sends"
// ✅ CORRECT: bun.requests = what bun HANDLES (webview calls these)
```

### 2. Forgetting schema types (losing type safety)

```ts
// ❌ No type safety — methods and params are untyped
const rpc = BrowserView.defineRPC<any>({ ... });

// ✅ Full type safety — auto-complete on request/send methods
const rpc = BrowserView.defineRPC<MyAppRPC>({ ... });
```

### 3. Sending messages before transport is ready

On the bun side, wait for `"dom-ready"` before sending messages to the webview:

```ts
// ❌ May fail — webview hasn't connected yet
win.webview.rpc?.send?.showNotification({ text: "Hello" });

// ✅ Wait for DOM ready
win.webview.on("dom-ready", () => {
  win.webview.rpc?.send?.showNotification({ text: "Hello" });
});
```

### 4. Missing optional chaining on bun-side RPC calls

```ts
// ❌ May throw if rpc is undefined
win.webview.rpc.request.getDocumentTitle({});

// ✅ Safe access
win.webview.rpc?.request.getDocumentTitle({});
win.webview.rpc?.send?.showNotification({ text: "Hello" });
```

### 5. Request timeout too short

Default is **1000ms**. Increase for slow operations:

```ts
BrowserView.defineRPC<MyRPC>({
  maxRequestTime: 5000,  // 5 seconds
  handlers: { ... },
});
```

### 6. Import from wrong package

```ts
// Bun side
import { BrowserView, BrowserWindow, type RPCSchema } from "electrobun/bun";

// Browser side
import Electrobun, { Electroview } from "electrobun/view";
```

## Quick Reference

| Concept | Bun Side | Browser Side |
|---|---|---|
| Import | `from "electrobun/bun"` | `from "electrobun/view"` |
| Define RPC | `BrowserView.defineRPC<Schema>({...})` | `Electroview.defineRPC<Schema>({...})` |
| Initialize | Pass `rpc` to `new BrowserWindow({...})` | `new Electrobun.Electroview({ rpc })` |
| Make request | `win.webview.rpc?.request.method(params)` | `electrobun.rpc!.request.method(params)` |
| Send message | `win.webview.rpc?.send?.messageName(payload)` | `electrobun.rpc!.send.messageName(payload)` |
| Request handler | `handlers: { requests: { method: (params) => response } }` | Same |
| Message handler | `handlers: { messages: { name: (payload) => void } }` | Same |
| Wildcard messages | `handlers: { messages: { "*": (name, payload) => void } }` | Same |
| Catch-all request | `handlers: { requests: { _: (method, params) => response } }` | Same |
