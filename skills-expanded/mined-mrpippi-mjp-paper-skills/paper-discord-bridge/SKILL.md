---
name: paper-discord-bridge
description: "只用 JDK 的 Discord 聊天橋接（不需 JDA／DiscordSRV）：遊戲 → Discord 以 webhook 佇列送出（429 照 Retry-After 重送一次、禁止 @提及、Markdown 跳脫），Discord → 遊戲以 Gateway WebSocket 狀態機（心跳、RESUME、致命關閉碼、退避）在單一執行緒接收後切回主執行緒；祕密不進 log / JDK-only Discord chat bridge (no JDA or DiscordSRV): outbound webhook queue with 429 retry, no mentions and markdown escaping; inbound Gateway WebSocket state machine (heartbeat, resume, fatal close codes, backoff) on one thread, hopping to the main thread; secrets never logged"
---

# Paper Discord Bridge

## Skill Name

`paper-discord-bridge`

## Purpose

Bridge in-game chat with **one Discord channel** using nothing but the JDK (`java.net.http.HttpClient` and `WebSocket`) and the Gson that ships with paper-api. No JDA, no DiscordSRV, nothing shaded into the jar.

Two usage tiers; pick the smallest one that does the job:

| Tier | Direction | What you need on Discord | What runs in the plugin |
|------|-----------|--------------------------|-------------------------|
| **1. Webhook only** | Game → Discord | A channel webhook URL (Channel settings → Integrations → Webhooks). No bot. | `PostQueue` (one daemon thread) |
| **2. Two-way** | Game ↔ Discord | Tier 1 **plus** a bot: token, **Message Content Intent** enabled (Developer Portal → Bot), invited to the server with the `bot` scope, and in the bridged channel the permissions **View Channel**, **Read Message History**, **Send Messages**; plus the channel id (Developer Mode → right-click channel → Copy Channel ID) | `PostQueue` + `GatewayClient` (one scheduled thread) |

Core design:

- **Outbound** (`PostQueue`): callers only `enqueue` and never wait on HTTP. A daemon thread posts in order; on **429** it sleeps `Retry-After` (capped) and retries **once**, any other failure logs one throttled WARNING with the **status code only**. Every payload carries `allowed_mentions.parse = []` (nothing in it can ping anyone) and `flags = 4` (SUPPRESS_EMBEDS); player text is markdown-escaped, including `<`, so `<@id>`, `<#id>`, `<t:…>` cannot render as mentions or timestamps.
- **Inbound** (`GatewaySession` + `GatewayClient`): the Discord Gateway protocol (HELLO → heartbeat with jitter → IDENTIFY/RESUME → READY/RESUMED, opcodes 1/7/9/11, `resume_gateway_url`, zombie detection, close codes that must not reconnect, exponential backoff with jitter) is a **pure state machine** that turns events into actions and is unit-tested without a socket. `GatewayClient` only performs those actions, all on **one** scheduled executor thread. Messages are cleaned (`InboundText`) and hop to the main thread with `runTask`.
- **Pluggable edges**: `AccountLinks` decides who may speak in game (default by config: everyone, or nobody), `ChatSink` delivers the line (default: broadcast via Adventure with MiniMessage `unparsed` placeholders, so Discord text can never inject tags).
- **Secrets never logged**: the bot token and webhook URLs are not written to the console, exceptions or status; `BridgeConfig#toString` masks them as `***`; HTTP failures log the status code or exception class name only (exception messages may contain the URL).

## Paper Version Requirements

- Paper 1.21.11 / 26.3 (identical on both; uses `AsyncChatEvent`, Adventure, the Bukkit scheduler and JDK 21+ APIs such as `HttpClient#shutdownNow`)
- Pure Paper API, no Paperweight needed
- Discord API v10, Gateway `encoding=json` (no zlib compression)
- **Spigot**: Core portable — the JDK webhook/Gateway client is server-independent; chat capture uses Paper `AsyncChatEvent` (Spigot: `AsyncPlayerChatEvent`) and Adventure

## Triggers

- 「Discord 橋接」「Discord bridge」「Discord 聊天同步」「Discord chat sync」「聊天互通」「two-way chat」
- 「webhook」「Discord webhook」「Discord Gateway」「Discord bot」「MESSAGE_CREATE」
- 「不用 JDA」「without JDA」「不用 DiscordSRV」「死亡訊息送 Discord」「announce to Discord」

## Inputs

| Parameter | Example | Description |
|------|------|------|
| `base_package` | `com.example.discordbridge` | Root package; pure logic in `.core`, Discord I/O in `.discord` |
| `tier` | `webhook-only` / `two-way` | Tier 1 needs only `webhook-url`; tier 2 also needs `bot-token` + `channel-id` |
| `account_links` | `everyone` / `nobody` / custom | Who may speak from Discord; replace with a real link lookup (see `examples.md`) |
| `inbound_format` | `<color:#5865F2>[Discord]</color> <name>: <message>` | MiniMessage format; `<name>` and `<message>` are inserted as **unparsed** text |
| `avatar_url` | `https://mc-heads.net/avatar/{name}/64` | Webhook avatar per player; empty = Discord's default |
| `max_length` | `200` | Max characters per inbound line (truncated with `…`) |

## Outputs

- Core (no Bukkit, JUnit-testable): `Backoff`, `Payloads` (JSON + escaping), `InboundText` (cleanup + MESSAGE_CREATE filter), `GatewaySession` (protocol state machine)
- Discord I/O (JDK only): `PostQueue` (webhook / bot REST poster), `GatewayClient` (WebSocket driver)
- Plugin: `BridgeConfig` (immutable, masked `toString`), `AccountLinks`, `ChatSink`, `InboundRelay`, `DiscordBridgePlugin`
- Tests: `GatewaySessionTest`, `TextRulesTest`
- `config.yml`, `plugin.yml`

## Build Setup

See [`references/paper-api-platform.md`](references/paper-api-platform.md). **No extra dependencies**: `java.net.http` is part of the JDK and Gson comes transitively with `paper-api` (the server bundles it; do not shade it). Tests use plain JUnit:

```groovy
dependencies {
    compileOnly 'io.papermc.paper:paper-api:26.3.build.258-stable' // 1.21.11: '1.21.11-R0.1-SNAPSHOT'
    testImplementation 'io.papermc.paper:paper-api:26.3.build.258-stable' // Gson for the core tests
    testImplementation 'org.junit.jupiter:junit-jupiter:5.11.4'
    testRuntimeOnly 'org.junit.platform:junit-platform-launcher'
}

test {
    useJUnitPlatform()
}
```

## Alternatives

If the server **already runs DiscordSRV** (or another bridge plugin), do not build a second connection to the same bot: hook the existing plugin's API instead, following the [`paper-softdepend-hook`](../paper-softdepend-hook/SKILL.md) pattern (declare it in `softdepend`, keep every reference to its classes inside one Hook class that is only loaded after `isPluginEnabled` returns true, and degrade quietly when it is missing). Two bots on one token fight over the Gateway session, and two webhooks double every message. Build this skill's bridge when you want one channel without a large dependency, or when you need full control over escaping, filtering and who may speak.

## Code Template

The full source lives in [`template.md`](template.md) (about 1,950 lines, compiled against Paper 1.21.11 and 26.3 in CI). **Read `template.md` before writing any code for this skill**, and copy from it instead of rebuilding the classes from the table below: the Gateway details (heartbeat jitter, RESUME rules, fatal close codes, zombie detection) and the escaping rules are easy to get subtly wrong.

| File | Package | Role |
|------|---------|------|
| `Backoff.java` | `.core` | Reconnect delay: doubling with cap and jitter, reset on READY / RESUMED |
| `Payloads.java` | `.core` | Outbound JSON (webhook and bot reply) with `allowed_mentions.parse = []`, `flags = 4`, markdown escaping |
| `InboundText.java` | `.core` | Filters a MESSAGE_CREATE (channel, bots, webhooks) and cleans text (control / bidi chars, length) |
| `GatewaySession.java` | `.core` | Gateway protocol as a pure state machine: events in, actions out |
| `PostQueue.java` | `.discord` | Ordered poster on one daemon thread; one 429 retry after `Retry-After`; status-only logging |
| `GatewayClient.java` | `.discord` | Runs `GatewaySession` over a JDK `WebSocket` on one scheduled thread |
| `BridgeConfig.java` | root | Immutable config, validation, secrets masked in `toString` |
| `AccountLinks.java` | root | Extension point: who may speak from Discord |
| `ChatSink.java` | root | Extension point: where an inbound line goes (default MiniMessage broadcast with `unparsed` placeholders) |
| `InboundRelay.java` | root | Main thread: link check, then deliver or reply (with cooldown) |
| `DiscordBridgePlugin.java` | root | Wiring: chat listener, queues, gateway, shutdown |
| `GatewaySessionTest.java` | test | State machine tests without a socket or sleeping |
| `TextRulesTest.java` | test | Escaping, payload shape, inbound cleanup |
| `config.yml`, `plugin.yml` | resources | Commented config (secrets marked) and plugin descriptor |

### Discord setup checklist

| Step | Tier | Where |
|------|------|-------|
| Create a webhook in the channel, copy its URL into `discord.webhook-url` | 1, 2 | Channel settings → Integrations → Webhooks |
| Create an application + bot, copy the token into `discord.bot-token` | 2 | Developer Portal → Applications → Bot |
| Enable **Message Content Intent** (privileged; without it the gateway closes with 4014) | 2 | Developer Portal → Bot → Privileged Gateway Intents |
| Invite the bot with the `bot` scope | 2 | Developer Portal → OAuth2 → URL Generator |
| Grant **View Channel**, **Read Message History**, **Send Messages** in the bridged channel | 2 | Channel settings → Permissions |
| Copy the channel id into `discord.channel-id` | 2 | Discord settings → Advanced → Developer Mode, then right-click the channel |

## Recommended Directory Structure

```
src/main/java/com/example/discordbridge/
├── core/                      <- no Bukkit, no network; tested with JUnit
│   ├── Backoff.java
│   ├── GatewaySession.java    <- the protocol, as a state machine
│   ├── InboundText.java
│   └── Payloads.java
├── discord/                   <- JDK HttpClient / WebSocket only; no Bukkit
│   ├── GatewayClient.java     <- the only class that owns the gateway thread
│   └── PostQueue.java         <- one daemon thread per Discord URL
├── AccountLinks.java / ChatSink.java   <- extension points (main thread)
├── BridgeConfig.java
├── InboundRelay.java
└── DiscordBridgePlugin.java
src/test/java/com/example/discordbridge/core/
├── GatewaySessionTest.java
└── TextRulesTest.java
src/main/resources/{config.yml,plugin.yml}
```

## Thread Safety

| Code | Thread | Rule |
|------|--------|------|
| `onChat(AsyncChatEvent)` | Async chat thread | Reads the event only, then `PostQueue#enqueue` (thread-safe, non-blocking) |
| `PostQueue` worker | Its own daemon thread | The only place that blocks on HTTP or sleeps for `Retry-After`; never the main thread or Bukkit's async pool |
| `GatewaySession`, all `GatewayClient` state | One `DiscordBridge-Gateway` thread | WebSocket callbacks only `post` to it; never touch Bukkit here |
| `InboundText.parse` | Gateway thread | Pure; produces an immutable `Message` that is safe to hand over |
| `InboundRelay`, `AccountLinks`, `ChatSink` | **Main thread** (via `runTask`) | Bukkit API and other plugins' main-thread APIs are allowed here |
| `onDisable` | Main thread | Queues drop their backlog, the gateway sends close 1000; total wait is bounded (2 s + 3 s) |

- Never call `Bukkit.broadcast`, `getPlayer`, `getOfflinePlayer` etc. inside the `GatewayClient` consumer: hop first. `runTask` throws `IllegalPluginAccessException` while the plugin is disabling, so `runOnMain` checks `isEnabled()` and catches it.
- Do not replace the single gateway thread with a pool: heartbeats must carry the latest sequence number and an old socket's late close must not reconnect a second time.
- See [`references/paper-threading.md`](references/paper-threading.md).

## Security

- **Secrets**: bot token and webhook URLs are never logged (`BridgeConfig#toString` masks them; `Send#toString` hides IDENTIFY; HTTP failures log status code / exception class only). Never put them in `/status` output, error messages or bug reports.
- **No pings**: every payload has `allowed_mentions.parse = []`; replies also set `replied_user: false`.
- **No markdown / mention injection** from players: `escapeMarkdown` escapes `<`, so `<@id>`, `<@&id>`, `<#id>`, `<t:…>` stay literal. Embeds are suppressed (`flags: 4`), so links do not unfurl.
- **No MiniMessage injection** from Discord: `Placeholder.unparsed`; colour codes, control and bidi characters are stripped by `InboundText`.
- **Impersonation**: with `allow-unlinked: true` the in-game name is the Discord display name, which anyone can choose. Keep a visible `[Discord]` marker in `format`, or use a real link lookup and show the **Minecraft** name (never fall back to the Discord name for a linked player who has no Minecraft name yet).
- **Echo loop**: messages with `webhook_id` or `author.bot` are ignored, so the plugin's own outbound webhook messages never come back in game.
- **Redirects** are not followed: a redirect could carry the `Authorization` header to another host.

## Fallback

| Error | Cause | Fix |
|------|------|------|
| SEVERE `Disallowed intents (4014)` | Message Content Intent not enabled | Developer Portal → Bot → enable MESSAGE CONTENT INTENT, restart |
| SEVERE `rejected the bot token (4004)` | Wrong / reset token | Paste the current token into `discord.bot-token`, restart (the bridge does not retry fatal codes) |
| Connected but inbound messages arrive with empty `content` | Intent missing on an old session, or messages from a thread / other channel | Enable the intent; only `channel-id` itself is bridged (threads have their own ids) |
| WARNING `not in any Discord server` | Bot never invited | OAuth2 URL Generator with the `bot` scope |
| `post failed (HTTP 403)` on replies | Bot lacks Send Messages / View Channel in the channel | Fix channel permission overrides |
| `post failed (HTTP 404)` on chat | Webhook deleted | Create a new webhook, update `webhook-url` |
| `queue is full` | Discord unreachable for a long time | Nothing is lost in game; the relay drops new lines and recovers by itself |
| Players can ping `@everyone` / roles | Custom payload built without `allowed_mentions` | Always build bodies through `Payloads` |
| Messages appear twice in game | Two bridges on one channel (e.g. DiscordSRV too) | Run one bridge; see Alternatives |
| Server stalls on shutdown | HTTP called on the main thread | Only `enqueue` from game threads; shutdown waits are capped |
| Every reconnect IDENTIFYs again | Session cleared on every close | Expected only after 4007/4009, INVALID_SESSION `false`, or 3 closes without HELLO; otherwise RESUME is used |
