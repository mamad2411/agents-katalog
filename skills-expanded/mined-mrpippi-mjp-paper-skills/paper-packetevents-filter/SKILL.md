---
name: paper-packetevents-filter
description: "不碰 NMS 的封包過濾：以 PacketEvents（主）或 ProtocolLib 軟依賴監聽封包，Hook + Bridge 隔離、Netty 執行緒只讀不可變快照、fail-open / Packet filtering without NMS via soft-dependent PacketEvents (primary) or ProtocolLib with Hook + Bridge, snapshot-only Netty-thread reads and fail-open"
---

# Paper PacketEvents Filter

## Skill Name

`paper-packetevents-filter`

## Purpose

Filter or rewrite packets sent to specific players **without NMS and without injecting into the Netty pipeline**: hide/rewrite system chat, inject per-viewer item lore, and mute sounds or hide particles for a single player.
The packet library is provided by the **PacketEvents** plugin (primary route) or the **ProtocolLib** plugin (secondary route) on the server. This plugin only uses `compileOnly`, **never shades** it, and declares it with `softdepend`, so the rest of the plugin keeps working when it is not installed.

Core rules (breaking any one of them causes trouble on a production server):

1. **Hook + Bridge**: any class that touches packet library types goes into the Bridge/Listener, and is only loaded after the library is enabled.
2. **Netty thread**: listeners do not run on the main thread. Read only an immutable volatile snapshot published by the main thread, **never call any Bukkit API**, and only modify cloned data.
3. **Fail-open**: on any exception, let the original packet through, disable that filter, and log only once. Code that blocks packets must not swallow packets because it is broken itself.
4. **Symmetric lifecycle**: register in `onEnable`, unregister in `onDisable`; do not call PacketEvents' `load()` / `init()` / `terminate()` (that is the packetevents plugin's own lifecycle).

> If you need to rewrite the Netty pipeline yourself or need NMS packet classes (the NMS/Netty route), use [`nms-packet-interceptor`](../../nms/nms-packet-interceptor/SKILL.md) instead.
> For the general soft-dependency approach (`getPlugin` checks, PlaceholderAPI, etc.) see [`paper-softdepend-hook`](../paper-softdepend-hook/SKILL.md).

## Paper Version Requirements

- Paper 1.21.11 / 26.3 (both compile-verified; the code in this skill is identical for both, with no `// @1.21.11:` difference lines)
- Pure Paper API, no Paperweight required
- The server needs **packetevents** (compiled against `packetevents-spigot:2.13.0`) or **ProtocolLib** (compiled against `5.3.0`); the MC versions actually supported depend on the version of that plugin on the server, so upgrade it before upgrading MC
- **Spigot**: Core portable — PacketEvents and ProtocolLib both support Spigot; replace Adventure and `ItemStack#editMeta`

## Triggers

- 「PacketEvents」「packetevents」「封包過濾」「packet filter」「packet listener」
- 「ProtocolLib」「PacketAdapter」「不用 NMS 攔封包」
- 「隱藏聊天」「SYSTEM_CHAT_MESSAGE」「per-viewer lore」「SET_SLOT」「WINDOW_ITEMS」
- 「取消粒子」「取消音效」「只對某玩家」「Netty thread」「fail-open」

## Inputs

| Parameter | Example | Description |
|------|------|------|
| `base_package` | `com.example.filter` | Package that holds the generated classes (split into `state` / `packet` / `integration`) |
| `backend` | `packetevents` / `protocollib` | Packet library; defaults to `packetevents` |
| `recipes` | `chat`, `lore`, `quiet` | Filter recipes to enable |
| `snapshot_fields` | `chatHidden`, `creative`, `quiet` | Data the main thread publishes to the Netty thread |

## Outputs

- `FilterSnapshot.java` / `FilterState.java` - immutable snapshot and volatile publication point
- `FailOpenGuard.java` - disables the filter on exception and logs only once
- `ChatPacketFilter.java` - hides/rewrites `SYSTEM_CHAT_MESSAGE` (`PacketListenerAbstract`)
- `LoreInjector.java` + `LorePainter.java` - per-viewer lore injection (`PacketListener`, skips creative mode)
- `QuietPacketFilter.java` - hides particles/sounds for a single player
- `PacketEventsHook.java` + `PacketEventsBridge.java` - soft-dependency entry points
- `ProtocolLibLoreAdapter.java` + `ProtocolLibHook.java` + `ProtocolLibBridge.java` - ProtocolLib variant
- `GameModeTracker.java` + `FilterPlugin.java` - main-thread snapshot publishing and lifecycle

## Build Setup

See [`references/paper-api-platform.md`](references/paper-api-platform.md). Both packet libraries are `compileOnly` only:

```groovy
repositories {
    maven { url = 'https://repo.codemc.io/repository/maven-releases/' }   // PacketEvents
    maven { url = 'https://repo.dmulloy2.net/repository/public/' }        // ProtocolLib
}

dependencies {
    compileOnly 'io.papermc.paper:paper-api:26.3.build.258-stable' // 1.21.11: '1.21.11-R0.1-SNAPSHOT'
    compileOnly 'com.github.retrooper:packetevents-spigot:2.13.0'
    compileOnly 'com.comphenix.protocol:ProtocolLib:5.3.0'
}
```

`plugin.yml` (list both; at runtime use whichever is installed; the PacketEvents plugin name is **lowercase** `packetevents`):

```yaml
name: Example
main: com.example.filter.FilterPlugin
api-version: '26.3'
softdepend: [packetevents, ProtocolLib]
```

The shadow config must not bundle the `com.github.retrooper`, `io.github.retrooper` or `com.comphenix` packages; confirm with `unzip -l` that the jar does not contain them.

## Code Template

The full source lives in [`template.md`](template.md) (about 900 lines, compiled against Paper 1.21.11 and 26.3 in CI). **Read `template.md` before writing any code for this skill**, and copy from it instead of rebuilding the classes from the table below.

| File | Package | Role |
|------|---------|------|
| `FilterSnapshot.java` | `.state` | Immutable filter snapshot, no packet types |
| `FilterState.java` | `.state` | Volatile publication point for the snapshot |
| `FailOpenGuard.java` | `.state` | Fail-open: disable the filter and log once on error |
| `ChatPacketFilter.java` | `.packet` | Recipe 1: filter system chat (PacketEvents) |
| `LorePainter.java` | `.packet` | Rewrites lore on item clones only |
| `LoreInjector.java` | `.packet` | Recipe 2: per-viewer lore (PacketEvents) |
| `QuietPacketFilter.java` | `.packet` | Recipe 3: hide particles / sounds for one player (PacketEvents) |
| `PacketEventsBridge.java` | `.integration` | Only class that registers with PacketEvents |
| `PacketEventsHook.java` | `.integration` | Soft-dependency entry point, no PacketEvents types |
| `ProtocolLibLoreAdapter.java` | `.packet` | ProtocolLib variant of the lore recipe |
| `ProtocolLibBridge.java` | `.integration` | Only class besides the adapter that touches ProtocolLib types |
| `ProtocolLibHook.java` | `.integration` | ProtocolLib soft-dependency entry point |
| `GameModeTracker.java` | root | Main thread publishes game-mode snapshots |
| `FilterPlugin.java` | root | Lifecycle and hook selection |

## Recommended Directory Structure

```
src/main/java/com/example/filter/
├── FilterPlugin.java              <- lifecycle; depends only on the Hook, imports no packet types
├── GameModeTracker.java           <- main-thread events -> publish snapshot
├── state/                         <- no packet types, safe for Bukkit to load
│   ├── FilterSnapshot.java
│   ├── FilterState.java
│   └── FailOpenGuard.java
├── packet/                        <- only here and the Bridge import the packet library
│   ├── ChatPacketFilter.java
│   ├── LoreInjector.java
│   ├── LorePainter.java           <- Bukkit types only
│   ├── QuietPacketFilter.java
│   └── ProtocolLibLoreAdapter.java
└── integration/
    ├── PacketEventsHook.java      <- no packet types
    ├── PacketEventsBridge.java
    ├── ProtocolLibHook.java
    └── ProtocolLibBridge.java
```

## Thread Safety

| Rule | Description |
|------|------|
| Listeners run on the Netty thread | `onPacketSend` / `onPacketSending` are not on the main thread; one slow listener slows that player's whole connection |
| Read-only snapshot | Read `state.current()` once per packet and keep it in a local variable; the snapshot is immutable, so no lock is needed |
| No Bukkit API | Never touch `Bukkit.*`, `Player.*` (except the UUID), worlds, blocks or the scheduler. Use `event.getUser().getUUID()` for identity; when logging, log only the UUID |
| Modify clones only | The `ItemStack` produced by `SpigotConversionUtil` and the clone from `LorePainter` may be modified; server-side items and inventories must never be modified |
| Write state on the main thread only | Events, commands and reload build a new snapshot on the main thread and then call `state.update(...)`; listeners never write |
| Resending packets | Change state first, then resend (`player.updateInventory()` or PacketEvents `PlayerManager#sendPacket`, which goes through the listener chain again); call the resend on the main thread |
| Exceptions | Always fail-open: `catch (RuntimeException \| LinkageError)` -> `guard.trip(e)`; put `setCancelled(true)` / `markForReEncode(true)` on the last line of the try |

See [`references/paper-threading.md`](references/paper-threading.md).

## Fallback

| Error | Cause | Fix |
|------|------|------|
| `NoClassDefFoundError: com/github/retrooper/...` | packetevents is not installed, but Bukkit reflects on a class that references its types (fields, method signatures, lambda parameters) | Packet types appear only in `packet/` and the Bridge; they must not appear in Hook/Plugin/Listener member signatures; write a reflection test on a classpath without the library |
| `registerListener` throws `NoSuchMethodError` at startup | The packetevents version on the server has an API that differs from the compiled version | The Hook catches `LinkageError`, degrades and logs a WARNING; upgrade packetevents on the server |
| A filter suddenly stops working and the console shows one WARNING line | A packet failed to parse (newer MC version, another plugin injected an odd component) -> the guard has tripped | This is the expected fail-open behavior; confirm packetevents supports the current MC version |
| Players have no lore on login; it only appears after they move something in the inventory | There is no Bukkit player during the login handshake, so that batch of packets was skipped | Call `player.updateInventory()` one tick after joining (see `GameModeTracker`) |
| Creative-mode items do not stack | The client echoes the lore it sees back to the server unchanged | Skip creative-mode viewers and strip the marker line in `CREATIVE_INVENTORY_ACTION` |
| Two lore plugins show their lines in an inconsistent order | The resend sent an already-injected packet directly, bypassing the listener chain | Resend the original item so the packet goes through the normal listener chain |
| ProtocolLib: `UnsupportedOperationException` in `getUniqueId()` | The connection is still a `TemporaryPlayer` | Check `event.isPlayerTemporary()` first |
| Exception while unregistering | packetevents/ProtocolLib was disabled first | `uninstall()` catches `LinkageError \| RuntimeException` and logs only at FINE |
| The same packet is processed twice | `register` was called twice, or both backends registered at once | The Hook ignores the call when a handle already exists; PacketEvents takes priority and ProtocolLib is only a backup |
