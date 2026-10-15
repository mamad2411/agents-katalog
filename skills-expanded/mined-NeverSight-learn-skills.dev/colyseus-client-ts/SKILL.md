---
name: colyseus-client-ts
description: >
  Use this skill when building a TypeScript or JavaScript client that connects
  to a Colyseus server, joining rooms, listening for state changes, sending
  messages, handling reconnection, or using @colyseus/sdk. Trigger for: Colyseus
  client, room joining, state sync callbacks, Callbacks.get, onAdd, onRemove,
  listen, message handling, reconnection, Client SDK, joinOrCreate, multiplayer
  client, real-time game client, @colyseus/sdk.
---

# Colyseus Client SDK (TypeScript)

Build TypeScript/JavaScript clients that connect to Colyseus multiplayer servers. This skill covers room joining, state sync callbacks, messages, reconnection, type safety, and latency handling.

## Quick Start

### Install

```sh
npm install @colyseus/sdk
```

### Minimal working client

```ts
import { Client, Callbacks } from "@colyseus/sdk";

const client = new Client("http://localhost:2567");

async function connect() {
  const room = await client.joinOrCreate("my_room");
  const $ = Callbacks.get(room);

  // Listen to top-level state property
  $.listen("phase", (current, previous) => {
    console.log("Phase changed:", previous, "->", current);
  });

  // Listen for player additions
  $.onAdd("players", (player, sessionId) => {
    console.log("Player joined:", sessionId);

    // Listen to nested property changes on this player
    $.listen(player, "x", (x) => updatePosition(sessionId, x, player.y));
    $.listen(player, "y", (y) => updatePosition(sessionId, player.x, y));
  });

  // Clean up when player leaves
  $.onRemove("players", (player, sessionId) => {
    console.log("Player left:", sessionId);
    removePlayerSprite(sessionId);
  });

  // Send messages to server
  room.send("move", { x: 100, y: 200 });

  // Handle reconnection
  room.onDrop((code, reason) => showReconnectingUI());
  room.onReconnect(() => hideReconnectingUI());
  room.onLeave((code) => returnToMenu());
}
```

### Debug panel (development only)

```ts
import "@colyseus/sdk/debug"; // Adds real-time state inspector and message log
```

## Type Safety

There are four levels of type safety you can opt into, depending on your project setup:

### Tier 1: Full-stack type safety (recommended for monorepos)

```ts
import { Client } from "@colyseus/sdk";
import type { server } from "../../server/src/app.config";

const client = new Client<typeof server>("http://localhost:2567");
const room = await client.joinOrCreate("my_room");
// State, messages, and room options are all type-checked
```

### Tier 2: Room type import

```ts
import type { MyRoom } from "../../server/src/rooms/MyRoom";

const room = await client.joinOrCreate<MyRoom>("my_room");
// State + message types inferred from room definition
```

### Tier 3: State type only

```ts
import type { MyState } from "../../server/src/rooms/schema/MyState";

const room = await client.joinOrCreate<MyState>("my_room");
// State properties autocomplete; messages untyped
```

### Tier 4: Shared Schema class (custom methods + bandwidth savings)

```ts
import { MyState } from "../../server/src/rooms/schema/MyState"; // NOT "import type"

const room = await client.joinOrCreate("my_room", {}, MyState);
// Custom methods on Schema classes are available
// Client uses same decoder — slightly less bandwidth
```

**tsconfig note:** If sharing Schema classes (Tier 4), your client tsconfig needs `"experimentalDecorators": true` and `"useDefineForClassFields": false`.

**Decision guide:** Use Tier 1 when client and server share a monorepo. Use Tier 2-3 when you can import types but not runtime code. Use Tier 4 when you need custom methods on state objects or want bandwidth optimization.

## Joining Rooms

| Method | Behavior | Use when |
|--------|----------|----------|
| `joinOrCreate(name, options?)` | Join existing or create new | Default choice for matchmaking |
| `create(name, options?)` | Always creates a new room | Private rooms, fresh sessions |
| `join(name, options?)` | Join existing only (throws if none) | Joining a friend's game |
| `joinById(roomId, options?)` | Join specific room by ID | Invite links, spectator mode |
| `consumeSeatReservation(reservation)` | Join with pre-reserved seat | Server-side matchmaking |

```ts
// Most common — automatic matchmaking
const room = await client.joinOrCreate("battle", { mode: "ranked" });

// Invite link pattern
const inviteLink = `https://mygame.com/join?roomId=${room.roomId}`;
// On the receiving end:
const room = await client.joinById(new URLSearchParams(location.search).get("roomId"));

// Browse available rooms
const rooms = await client.getAvailableRooms("battle");
rooms.forEach((r) => console.log(r.roomId, r.metadata, r.clients));
```

## State Sync Callbacks

This is the most important section for client development. State sync callbacks let you react to specific state changes efficiently, rather than diffing the entire state each frame.

### Getting the callbacks handler

```ts
import { Callbacks } from "@colyseus/sdk";

const $ = Callbacks.get(room); // Shorthand variable name — use any name you like
```

### Listening to property changes

```ts
// Top-level state property
$.listen("currentTurn", (currentValue, previousValue) => {
  console.log("Turn:", previousValue, "->", currentValue);
});

// Nested property on a specific Schema instance
$.listen(player, "hp", (currentHp, previousHp) => {
  updateHealthBar(player, currentHp);
});
```

### Tracking collection additions and removals

```ts
// onAdd fires immediately for existing items, then for each new addition
$.onAdd("players", (player, sessionId) => {
  // Create game object for this player
  const sprite = createPlayerSprite(sessionId);

  // Register nested listeners INSIDE onAdd — this is the standard pattern
  $.listen(player, "x", (x) => { sprite.x = x; });
  $.listen(player, "y", (y) => { sprite.y = y; });
  $.listen(player, "hp", (hp) => updateHealthBar(sprite, hp));
});

// onRemove — clean up game objects here
$.onRemove("players", (player, sessionId) => {
  destroyPlayerSprite(sessionId);
});
```

### Detecting any change on an instance

```ts
$.onAdd("entities", (entity, id) => {
  $.onChange(entity, () => {
    // Fires when ANY direct property of `entity` changes
    // Does NOT fire for changes in nested Schema children
    refreshEntityVisuals(entity);
  });
});
```

### Binding properties directly to game objects

```ts
$.onAdd("players", (player, sessionId) => {
  const sprite = PIXI.Sprite.from("player");
  $.bindTo(player, sprite); // Auto-syncs all @type() properties to sprite
});
```

### Removing callbacks

Every callback registration returns an unbind function:

```ts
const unbind = $.listen("currentTurn", (val) => { /* ... */ });
// Later:
unbind(); // Stop listening
```

### Key patterns and gotchas

- **Always register nested `listen()` inside `onAdd()`** — this ensures each new instance gets its own listeners
- **`onChange` only fires for direct property changes** — if `entity.nested.x` changes, `onChange(entity, ...)` does NOT fire; use `listen(entity.nested, "x", ...)` instead
- **`onAdd` fires immediately for existing items** — when you connect mid-game, you get callbacks for all current players/entities
- **Prefer fine-grained callbacks over `room.onStateChange`** — `onStateChange` triggers on every patch and gives you the entire state; callbacks are more efficient and targeted

> Read `references/callbacks-api.md` for the complete Callbacks API with all overloads.

## Messages

### Sending to server

```ts
// MsgPack-encoded (most common)
room.send("move", { x: 10, y: 20 });

// Raw bytes (custom encoding)
room.sendBytes("binary", new Uint8Array([0x01, 0x02]));
```

### Receiving from server

```ts
room.onMessage("powerup", (data) => {
  playEffect(data.type, data.x, data.y);
});

room.onMessage("chat", (message) => {
  addChatBubble(message.sender, message.text);
});
```

Messages sent during a temporary disconnect are **automatically buffered** (up to `maxEnqueuedMessages`, default 10) and sent when reconnected.

## Reconnection

Colyseus has built-in automatic reconnection with exponential backoff.

### Connection events

```ts
// Connection dropped — SDK auto-retries in background
room.onDrop((code, reason) => {
  showReconnectingOverlay();
});

// Reconnected successfully
room.onReconnect(() => {
  hideReconnectingOverlay();
  // Buffered messages were auto-sent
});

// Permanently left (by choice or reconnection failed)
room.onLeave((code, reason) => {
  if (code === CloseCode.FAILED_TO_RECONNECT) {
    showError("Connection lost. Please rejoin.");
  }
  cleanupAndReturnToMenu();
});
```

### Reconnection configuration

```ts
room.reconnection.enabled = true;            // default: true
room.reconnection.maxRetries = 15;           // default: 15
room.reconnection.delay = 100;               // initial delay ms
room.reconnection.maxDelay = 5000;           // max delay ms
room.reconnection.minUptime = 5000;          // min connected time before auto-reconnect
room.reconnection.maxEnqueuedMessages = 10;  // buffered messages during disconnect

// Custom backoff
room.reconnection.backoff = (attempt, delay) => {
  return Math.floor(Math.pow(2, attempt) * delay);
};
```

### Manual reconnection

For cases where you need to store the token and reconnect later (e.g., page refresh):

```ts
// Save token
const token = room.reconnectionToken;
localStorage.setItem("reconnectionToken", token);

// Later, reconnect manually
try {
  const newRoom = await client.reconnect(localStorage.getItem("reconnectionToken"));
  // IMPORTANT: newRoom is a NEW instance — reattach all listeners
  setupCallbacks(newRoom);
} catch (e) {
  console.error("Reconnection failed");
}
```

**Key rule:** Manual `client.reconnect()` returns a **new** Room instance. You must reattach all callbacks, `onMessage`, `onDrop`, etc. to the new instance.

> Read `references/reconnection-reference.md` for full configuration table, close codes, and backoff details.

## Connection Lifecycle

### Error handling

```ts
room.onError((code, message) => {
  console.error("Room error:", code, message);
});
```

### Leaving a room

```ts
room.leave();        // Consented leave — triggers onLeave with CloseCode.CONSENTED (4000)
room.leave(false);   // Simulate unexpected disconnect — triggers onDrop + reconnection
```

### Removing all listeners

```ts
room.removeAllListeners(); // Detach all event handlers
```

### Close codes reference

| Code | Name | Meaning |
|------|------|---------|
| 1000 | `NORMAL_CLOSURE` | Normal WebSocket closure |
| 1001 | `GOING_AWAY` | Browser/tab closing |
| 1006 | `ABNORMAL_CLOSURE` | Connection lost unexpectedly |
| 4000 | `CONSENTED` | Client called `room.leave()` |
| 4001 | `SERVER_SHUTDOWN` | Server graceful shutdown |
| 4002 | `WITH_ERROR` | Closed due to error |
| 4003 | `FAILED_TO_RECONNECT` | All reconnection attempts exhausted |
| 4010 | `MAY_TRY_RECONNECT` | Dev mode server restart |

## Latency & Server Selection

```ts
// Measure latency to current server
const latency = await client.getLatency(); // single ping
const avgLatency = await client.getLatency({ pingCount: 5 }); // average of 5

// Ping during active connection
room.ping((latency) => {
  document.getElementById("ping").textContent = `${latency}ms`;
});

// Multi-region: auto-select fastest server
const client = await Client.selectByLatency([
  "https://us-east.gameserver.com",
  "https://eu-west.gameserver.com",
  "https://asia.gameserver.com",
]);
const room = await client.joinOrCreate("game");
```

## HTTP Requests

Call server-defined API endpoints with built-in auth:

```ts
// GET request
const profile = await client.http.get("/profile/123");

// POST with body
const result = await client.http.post("/profile/123", {
  body: { name: "New Name" },
});

// Also available: client.http.put(), client.http.delete(), client.http.patch()
```

The auth token is sent automatically with each request.

## Common Mistakes

- **Not using `Callbacks.get(room)`** — Accessing `room.state` directly works but you miss reactive updates. Always use Callbacks for UI sync
- **Using `onStateChange` instead of fine-grained callbacks** — `onStateChange` fires on every single patch; use `listen`/`onAdd`/`onRemove` to react to specific changes efficiently
- **Forgetting to clean up in `onRemove`** — When entities leave the state, destroy their game objects (sprites, DOM elements) in the `onRemove` callback to prevent memory leaks
- **Not showing reconnection UI** — Always handle `onDrop` to show "reconnecting..." feedback. Without it, users see a frozen game with no explanation
- **Reusing room instance after manual reconnect** — `client.reconnect(token)` returns a NEW Room instance. All callbacks must be reattached to the new instance
- **Using `http://` in production** — Always use `https://` (or `wss://`) for production deployments
- **Missing tsconfig decorators for shared schemas** — If importing Schema classes (not just types), your client tsconfig needs `"experimentalDecorators": true` and `"useDefineForClassFields": false`
- **Not handling `FAILED_TO_RECONNECT`** — Check for `CloseCode.FAILED_TO_RECONNECT` in `onLeave` to show an appropriate error instead of silently failing
- **`sendUnreliable()` during disconnect** — Unlike `room.send()`, unreliable messages are NOT buffered and are dropped if the connection is down
