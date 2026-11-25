---
name: messaging-integration
description: Production-ready patterns for integrating messaging platforms (WhatsApp, Slack, Telegram) into any application. Use when adding messaging channel support, implementing bots, or building multi-platform integrations.
---

# Messaging Platform Integration

## Overview

Production-ready patterns for integrating messaging platforms (WhatsApp, Slack, Telegram) into any application. This skill provides proven architectural patterns, shared implementation strategies, and platform-specific guidance extracted from battle-tested implementations.

## When to Use This Skill

- Adding messaging channel support to an app
- Implementing WhatsApp, Slack, or Telegram bots
- Building multi-platform messaging integrations
- Designing message routing and access control systems

## Platform Selection Matrix

| Factor | WhatsApp | Slack | Telegram |
|--------|----------|-------|----------|
| **Best For** | Personal messaging, groups | Workspace collaboration | Bots, channels, communities |
| **Auth Method** | QR code scan | OAuth + tokens | Bot token from BotFather |
| **Real-time** | WebSocket (Baileys) | Socket Mode / HTTP webhooks | Long polling / webhooks |
| **Library** | @whiskeysockets/baileys | @slack/bolt | grammy |
| **Rate Limits** | Unofficial, vary | Tiered (1-100/min) | 30 msg/sec, 1/sec same chat |
| **Media Support** | Images, video, audio, docs | Files up to 1GB | Photos, video, voice, docs |
| **Threading** | Reply quotes | Native threads | Reply quotes, forum topics |
| **Interactive** | Limited | Buttons, modals, shortcuts | Inline keyboards, callbacks |

### Decision Guide

**Choose WhatsApp when:**
- Users are on mobile and prefer personal messaging
- Need to reach users without app installation
- Group chat with mention-based activation

**Choose Slack when:**
- Building for workplace/team communication
- Need rich interactive components (modals, shortcuts)
- Integrating with other Slack apps
- Users already live in Slack

**Choose Telegram when:**
- Building public-facing bots
- Need forum-style threaded discussions
- Want easy bot creation (no approval process)
- Need inline mode for cross-chat interactions

---

## Shared Architectural Patterns

These patterns apply to ALL messaging integrations regardless of platform.

### 1. Multi-Account Architecture

Always design for multiple accounts from day one. Retrofitting is painful.

```typescript
type ResolvedAccount = {
  accountId: string;
  enabled: boolean;
  name?: string;
  token: string;
  tokenSource: "env" | "config" | "tokenFile" | "none";
  config: AccountConfig;
};

// Token resolution priority (all platforms):
// 1. Account-specific tokenFile (read from filesystem)
// 2. Account-specific token in config
// 3. Legacy global tokenFile (default account only)
// 4. Legacy global token (default account only)
// 5. Environment variable (default account only)

function resolveToken(cfg: Config, accountId: string): { token: string; source: string } {
  const accountCfg = cfg.accounts?.[accountId];

  // Account-specific sources first
  if (accountCfg?.tokenFile && fs.existsSync(accountCfg.tokenFile)) {
    return { token: fs.readFileSync(accountCfg.tokenFile, "utf-8").trim(), source: "tokenFile" };
  }
  if (accountCfg?.token?.trim()) {
    return { token: accountCfg.token.trim(), source: "config" };
  }

  // Legacy fallbacks (default account only)
  if (accountId === "default") {
    // ... check global config and env vars
  }

  return { token: "", source: "none" };
}
```

**Critical:** Only the default account can use environment variables. All other accounts must have explicit configuration.

### 2. Message Deduplication

All platforms can emit duplicate events (retries, race conditions). Track seen messages:

```typescript
const seenMessages = new Map<string, number>(); // key → timestamp
const DEDUPE_TTL_MS = 10 * 60_000; // 10 minutes
const MAX_CACHE_SIZE = 2000;

function isDuplicate(dedupeKey: string): boolean {
  const now = Date.now();

  // Check if seen recently
  const timestamp = seenMessages.get(dedupeKey);
  if (timestamp && now - timestamp < DEDUPE_TTL_MS) {
    return true; // Duplicate
  }

  // Mark as seen
  seenMessages.set(dedupeKey, now);

  // Prune old entries
  if (seenMessages.size > MAX_CACHE_SIZE) {
    for (const [key, ts] of seenMessages) {
      if (now - ts >= DEDUPE_TTL_MS) seenMessages.delete(key);
    }
  }

  return false; // First time
}

// Dedupe key format varies by platform:
// WhatsApp: ${accountId}:${remoteJid}:${messageId}
// Slack: ${channelId}:${messageTs}
// Telegram: update:${update_id} or message:${chatId}:${messageId}
```

### 3. Inbound Debouncing

Combine rapid sequential messages from the same sender:

```typescript
type DebounceEntry<T> = { entries: T[]; timer: NodeJS.Timeout };

function createInboundDebouncer<T>(opts: {
  debounceMs: number;
  buildKey: (entry: T) => string;
  shouldDebounce: (entry: T) => boolean;
  onFlush: (entries: T[]) => Promise<void>;
}) {
  const buffer = new Map<string, DebounceEntry<T>>();

  return {
    async add(entry: T): Promise<void> {
      if (!opts.shouldDebounce(entry)) {
        await opts.onFlush([entry]);
        return;
      }

      const key = opts.buildKey(entry);
      const existing = buffer.get(key);

      if (existing) {
        clearTimeout(existing.timer);
        existing.entries.push(entry);
      } else {
        buffer.set(key, { entries: [entry], timer: null as any });
      }

      const queue = buffer.get(key)!;
      queue.timer = setTimeout(async () => {
        buffer.delete(key);
        await opts.onFlush(queue.entries);
      }, opts.debounceMs);
    },
  };
}

// Don't debounce:
// - Media messages (process immediately)
// - Commands (e.g., /help, !stop)
// - Messages with control sequences
```

### 4. Exponential Backoff with Jitter

All platforms have rate limits. Use consistent retry strategy:

```typescript
type BackoffPolicy = {
  initialMs: number;
  maxMs: number;
  factor: number;
  jitter: number;
  maxAttempts: number;
};

const DEFAULT_BACKOFF: BackoffPolicy = {
  initialMs: 1000,
  maxMs: 30000,
  factor: 2,
  jitter: 0.25,
  maxAttempts: 5,
};

function computeBackoff(policy: BackoffPolicy, attempt: number): number {
  const base = Math.min(
    policy.initialMs * Math.pow(policy.factor, attempt - 1),
    policy.maxMs
  );
  const jitterRange = base * policy.jitter;
  const jitter = (Math.random() - 0.5) * 2 * jitterRange;
  return Math.max(0, Math.floor(base + jitter));
}

async function withRetry<T>(
  fn: () => Promise<T>,
  policy: BackoffPolicy = DEFAULT_BACKOFF
): Promise<T> {
  let lastError: unknown;

  for (let attempt = 1; attempt <= policy.maxAttempts; attempt++) {
    try {
      return await fn();
    } catch (err) {
      lastError = err;
      if (attempt < policy.maxAttempts) {
        const delay = computeBackoff(policy, attempt);
        await new Promise(r => setTimeout(r, delay));
      }
    }
  }

  throw lastError;
}
```

### 5. Access Control Layers

Implement layered access control consistently:

```typescript
type DMPolicy = "disabled" | "pairing" | "allowlist" | "open";
type GroupPolicy = "disabled" | "allowlist" | "open";

interface AccessCheckResult {
  allowed: boolean;
  reason?: string;
  pairingCode?: string;
}

// Layer 1: DM Policy (for direct messages)
function checkDMAccess(params: {
  userId: string;
  policy: DMPolicy;
  allowlist: string[];
}): AccessCheckResult {
  if (params.policy === "disabled") {
    return { allowed: false, reason: "DMs disabled" };
  }
  if (params.policy === "open") {
    return { allowed: true };
  }

  const isAllowed =
    params.allowlist.includes("*") ||
    params.allowlist.includes(params.userId);

  if (params.policy === "allowlist") {
    return isAllowed
      ? { allowed: true }
      : { allowed: false, reason: "User not in allowlist" };
  }

  if (params.policy === "pairing") {
    if (isAllowed) return { allowed: true };
    // Generate pairing code for unknown users
    const code = generatePairingCode(params.userId);
    return { allowed: false, pairingCode: code };
  }

  return { allowed: false };
}

// Layer 2: Group Policy (for group/channel messages)
function checkGroupAccess(params: {
  groupId: string;
  userId: string;
  policy: GroupPolicy;
  groupAllowlist: string[];
  userAllowlist: string[];
}): AccessCheckResult {
  if (params.policy === "disabled") {
    return { allowed: false, reason: "Groups disabled" };
  }
  if (params.policy === "open") {
    return { allowed: true };
  }

  // Check group allowlist
  const groupAllowed =
    params.groupAllowlist.includes("*") ||
    params.groupAllowlist.includes(params.groupId);

  if (!groupAllowed) {
    return { allowed: false, reason: "Group not allowed" };
  }

  // Check user allowlist within group
  const userAllowed =
    params.userAllowlist.includes("*") ||
    params.userAllowlist.includes(params.userId);

  return userAllowed
    ? { allowed: true }
    : { allowed: false, reason: "User not allowed in this group" };
}

// Layer 3: Mention Gating (optional, for groups)
function checkMentionGate(params: {
  isGroup: boolean;
  requireMention: boolean;
  wasMentioned: boolean;
  isReplyToBot: boolean;
  isCommand: boolean;
}): { shouldProcess: boolean } {
  if (!params.isGroup) return { shouldProcess: true };
  if (!params.requireMention) return { shouldProcess: true };
  if (params.wasMentioned) return { shouldProcess: true };
  if (params.isReplyToBot) return { shouldProcess: true };
  if (params.isCommand) return { shouldProcess: true };

  return { shouldProcess: false };
}
```

### 6. Message Chunking

All platforms have message length limits:

| Platform | Text Limit | Caption Limit |
|----------|------------|---------------|
| WhatsApp | ~65536 | ~1024 |
| Slack | 4000 | N/A |
| Telegram | 4096 | 1024 |

```typescript
function chunkMessage(text: string, limit: number): string[] {
  if (text.length <= limit) return [text];

  const chunks: string[] = [];
  let remaining = text;

  while (remaining.length > 0) {
    if (remaining.length <= limit) {
      chunks.push(remaining);
      break;
    }

    // Find safe split point
    let splitIndex = limit;

    // Try paragraph boundary
    const paraBreak = remaining.lastIndexOf("\n\n", limit);
    if (paraBreak > limit * 0.7) {
      splitIndex = paraBreak + 2;
    } else {
      // Try sentence boundary
      const sentenceEnd = Math.max(
        remaining.lastIndexOf(". ", limit),
        remaining.lastIndexOf("! ", limit),
        remaining.lastIndexOf("? ", limit)
      );
      if (sentenceEnd > limit * 0.7) {
        splitIndex = sentenceEnd + 2;
      } else {
        // Word boundary
        const space = remaining.lastIndexOf(" ", limit);
        if (space > 0) splitIndex = space + 1;
      }
    }

    chunks.push(remaining.slice(0, splitIndex).trim());
    remaining = remaining.slice(splitIndex);
  }

  return chunks;
}
```

### 7. Media Handling Pattern

Consistent media download/upload with size limits:

```typescript
type MediaResult = {
  buffer: Buffer;
  mimeType: string;
  fileName?: string;
};

async function downloadMedia(params: {
  url: string;
  maxBytes?: number;
  headers?: Record<string, string>;
}): Promise<MediaResult> {
  const response = await fetch(params.url, { headers: params.headers });

  // Check content-length before downloading
  const contentLength = response.headers.get("content-length");
  if (contentLength && params.maxBytes) {
    const size = parseInt(contentLength, 10);
    if (size > params.maxBytes) {
      throw new Error(`File size ${size} exceeds limit ${params.maxBytes}`);
    }
  }

  const buffer = Buffer.from(await response.arrayBuffer());

  // Double-check actual size
  if (params.maxBytes && buffer.length > params.maxBytes) {
    throw new Error(`Downloaded file exceeds size limit`);
  }

  const mimeType = response.headers.get("content-type") || "application/octet-stream";

  return { buffer, mimeType };
}

// Size limits by platform (recommended):
const MEDIA_LIMITS = {
  whatsapp: { image: 5 * 1024 * 1024, video: 16 * 1024 * 1024 },
  slack: { file: 20 * 1024 * 1024 },
  telegram: { photo: 10 * 1024 * 1024, video: 50 * 1024 * 1024 },
};
```

### 8. Reconnection Loop Pattern

For persistent connections (WhatsApp WebSocket, Slack Socket Mode):

```typescript
async function reconnectionLoop(params: {
  connect: () => Promise<{ onClose: Promise<CloseReason> }>;
  backoffPolicy: BackoffPolicy;
  shouldStop: () => boolean;
  onHealthyUptime: (uptimeMs: number) => void;
}) {
  let attempts = 0;
  const healthyThresholdMs = 60_000; // 1 minute = "healthy"

  while (!params.shouldStop()) {
    const startedAt = Date.now();

    try {
      const connection = await params.connect();
      attempts = 0; // Reset on successful connect

      const closeReason = await connection.onClose;
      const uptimeMs = Date.now() - startedAt;

      if (uptimeMs > healthyThresholdMs) {
        attempts = 0; // Reset backoff after healthy stretch
        params.onHealthyUptime(uptimeMs);
      }

      if (closeReason.isLoggedOut) {
        console.error("Session logged out. Manual re-auth required.");
        break;
      }
    } catch (err) {
      console.error("Connection error:", err);
    }

    if (params.shouldStop()) break;

    attempts++;
    if (attempts >= params.backoffPolicy.maxAttempts) {
      console.error("Max reconnect attempts reached.");
      break;
    }

    const delay = computeBackoff(params.backoffPolicy, attempts);
    await new Promise(r => setTimeout(r, delay));
  }
}
```

### 9. Echo Tracking (Prevent Self-Reply Loops)

Track outbound message IDs to skip when echoed back:

```typescript
function createEchoTracker(maxItems: number = 100) {
  const echoIds = new Map<string, number>();
  const TTL_MS = 5 * 60_000;

  return {
    track(messageId: string) {
      echoIds.set(messageId, Date.now());
      if (echoIds.size > maxItems) {
        const oldest = [...echoIds.entries()].sort((a, b) => a[1] - b[1])[0];
        echoIds.delete(oldest[0]);
      }
    },

    isEcho(messageId: string): boolean {
      const timestamp = echoIds.get(messageId);
      if (!timestamp) return false;
      if (Date.now() - timestamp > TTL_MS) {
        echoIds.delete(messageId);
        return false;
      }
      return true;
    },
  };
}
```

---

## Quick Start by Platform

### WhatsApp Quick Start

```typescript
import { createWaSocket, waitForWaConnection, monitorWebInbox } from "./whatsapp";

// 1. Login (scan QR code)
const sock = await createWaSocket(true, false, { authDir: "~/.myapp/wa/default" });
await waitForWaConnection(sock);
sock.ws?.close();

// 2. Monitor inbox
const listener = await monitorWebInbox({
  accountId: "default",
  authDir: "~/.myapp/wa/default",
  onMessage: async (msg) => {
    console.log(`From ${msg.senderName}: ${msg.body}`);
    await msg.reply(`Echo: ${msg.body}`);
  },
});
```

**See:** `references/whatsapp.md` for full implementation details.

### Slack Quick Start

```typescript
import { App } from "@slack/bolt";

const app = new App({
  token: process.env.SLACK_BOT_TOKEN,
  appToken: process.env.SLACK_APP_TOKEN,
  socketMode: true,
});

app.event("message", async ({ event, say }) => {
  if (event.subtype) return; // Skip system messages
  await say(`Echo: ${event.text}`);
});

await app.start();
```

**See:** `references/slack.md` for full implementation details.

### Telegram Quick Start

```typescript
import { Bot } from "grammy";
import { apiThrottler } from "@grammyjs/transformer-throttler";

const bot = new Bot(process.env.TELEGRAM_BOT_TOKEN!);
bot.api.config.use(apiThrottler());

bot.on("message:text", async (ctx) => {
  await ctx.reply(`Echo: ${ctx.message.text}`);
});

await bot.start();
```

**See:** `references/telegram.md` for full implementation details.

---

## Platform-Specific Guides

For detailed implementation patterns, see the platform-specific references:

| Platform | Reference | Key Topics |
|----------|-----------|------------|
| **WhatsApp** | `references/whatsapp.md` | QR auth, Baileys, credential backup, group history, media optimization |
| **Slack** | `references/slack.md` | OAuth, Socket Mode vs HTTP, threading, slash commands, Block Kit |
| **Telegram** | `references/telegram.md` | Grammy, webhooks vs polling, inline keyboards, forum topics, reactions |

---

## Configuration Template

```yaml
messaging:
  # Common settings
  mediaMaxMb: 5
  historyLimit: 50
  debounceMs: 1500

  # Access control defaults
  dmPolicy: pairing        # pairing | allowlist | open | disabled
  groupPolicy: open        # open | allowlist | disabled
  allowFrom: ["*"]

  # Platform-specific
  whatsapp:
    enabled: true
    authDir: ~/.myapp/credentials/whatsapp
    accounts:
      default:
        enabled: true
    reconnect:
      initialMs: 2000
      maxMs: 30000
      maxAttempts: 12

  slack:
    enabled: true
    mode: socket           # socket | http
    accounts:
      default:
        enabled: true
        botToken: ${SLACK_BOT_TOKEN}
        appToken: ${SLACK_APP_TOKEN}
    replyToMode: all       # off | first | all

  telegram:
    enabled: true
    accounts:
      default:
        enabled: true
        botToken: ${TELEGRAM_BOT_TOKEN}
    requireMention: true
    reactionLevel: ack     # off | ack | minimal | extensive
```

---

## Testing Checklist

Before deploying any messaging integration:

- [ ] Multi-account token resolution works correctly
- [ ] Message deduplication prevents double-processing
- [ ] Inbound debouncing combines rapid messages
- [ ] Access control blocks unauthorized users
- [ ] Media download respects size limits
- [ ] Message chunking handles long content
- [ ] Rate limiting/backoff prevents API errors
- [ ] Reconnection loop handles disconnects gracefully
- [ ] Echo tracking prevents self-reply loops
- [ ] Error responses are user-friendly

---

## Error Handling Summary

| Error Type | All Platforms |
|------------|---------------|
| Rate limit | Exponential backoff with jitter |
| Auth failure | Log, notify, stop reconnect loop |
| Network error | Retry with backoff |
| Invalid content | Fallback to plain text |
| Size exceeded | Chunk or reject with message |

---

## Resources

### Platform Documentation
- WhatsApp: [Baileys GitHub](https://github.com/WhiskeySockets/Baileys)
- Slack: [Bolt JS](https://slack.dev/bolt-js/), [API Reference](https://api.slack.com/methods)
- Telegram: [Grammy](https://grammy.dev/), [Bot API](https://core.telegram.org/bots/api)

### Reference Implementation
- Clawdbot: `/Users/tinnguyen/clawd/src/{web,slack,telegram}/`
