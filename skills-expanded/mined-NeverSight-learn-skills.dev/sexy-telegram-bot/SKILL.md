---
name: sexy-telegram-bot
description: Production-grade Telegram bot guidance with grammY and TypeScript. Safe message editing, callback routing, session flows, rate-limited dispatch, inline keyboard UX, and permission layers. Use this skill whenever the user is building a Telegram bot, adding buttons or callbacks, handling bot errors, structuring a growing bot, or designing multi-step conversational flows, even if they don't explicitly ask for architecture guidance.
---

# sexy-telegram-bot

Everything you need to ship Telegram bots with grammY and TypeScript that hold up under real traffic. Covers message editing, callback routing as features grow, session state for multi-step DM flows, rate-limited notifications, and getting inline keyboards to feel right.

The user might be starting a new bot, adding a feature, building a flow, or fixing something that's misbehaving. They may or may not mention their stack or what specifically they're stuck on.

## How We Build

- **grammY over Telegraf.** grammY has stronger TypeScript support, active maintenance, and a cleaner plugin system.
- **HTML over Markdown.** HTML with `<b>`, `<i>`, `<code>`, `<a>` handles everything cleanly, including underscores in URLs and asterisks in usernames. Always pass `parse_mode: "HTML"`.
- **One callback router.** A single `callback_query:data` handler that dispatches by prefix keeps routing clean as the bot grows.
- **safeEdit everywhere.** A wrapper around `editMessageText` that handles the common race conditions from double-clicks, stale messages, and retries. Write it once, use it for every edit.
- **Sessions in memory.** DM flows last seconds to minutes, so a `Map<number, DmSession>` is all you need. If the bot restarts the user just starts the flow over.
- **Formatters are pure functions.** Data goes in, HTML string comes out. No side effects, no API calls inside formatters, easy to test and reuse.
- **Rate-limit your dispatch.** Telegram allows ~30 msg/sec globally and ~1 msg/sec per chat. Use Bottleneck with a per-chat queue to stay within limits.

## Architecture

```
Commands (entry points)
  └── Callback Router (inline keyboard dispatch)
       └── Session Manager (multi-step DM flows)
            └── Services (business logic, APIs, DB)
                 └── Dispatcher (rate-limited message delivery)
```

## Safe Message Editing

`editMessageText` can throw when users double-click buttons, when messages go stale, or on network retries. A `safeEdit` wrapper catches those specific cases and lets the rest through:

```typescript
const EDIT_IGNORE = [
  "message is not modified",
  "message to edit not found",
  "query is too old",
];

async function safeEdit(ctx, text, opts?) {
  try {
    await ctx.editMessageText(text, { parse_mode: "HTML", ...opts });
  } catch (err) {
    if (EDIT_IGNORE.some((m) => err?.message?.includes(m))) return;
    throw err;
  }
}
```

Do the same for `answerCallbackQuery` with a `safeAnswer` wrapper so the button spinner always clears.

## Callback Routing

One handler, prefix dispatch. Callback data format is `prefix:action:id[:extra]` and prefixes stay short since Telegram caps callback data at 64 bytes. Always match against known prefixes and validate IDs before acting on them since callback data comes from the client and can be spoofed.

```typescript
bot.on("callback_query:data", safe(async (ctx) => {
  const data = ctx.callbackQuery?.data ?? "";
  if (data.startsWith("usr:"))  return handleUserCallback(ctx);
  if (data.startsWith("proj:")) return handleProjectCallback(ctx);
  if (data.startsWith("grp:"))  return handleGroupCallback(ctx);
  await safeAnswer(ctx);
}));
```

## Everything Else

- **Session state.** A typed union like `{ flow: "create_project"; step: "name" | "description"; data: { name?: string } }` stored in a `Map<number, DmSession>`. Three helpers: `getSession`, `setSession`, `clearSession`. Private message handlers check for an active session first and fall through if there isn't one.
- **Inline keyboards.** Pagination with `« Prev` / `Next »` buttons using `prefix_pg:N` callbacks. Checklists with `☑` / `☐` toggling via callback data. Confirmation with two buttons (action + cancel). Every detail view gets a `« Back` button. Always edit in place with `safeEdit`.
- **DM deep links.** Move users from group to private chat with a URL button to `https://t.me/${BOT_USERNAME}?start=${payload}`. Parse the payload in `/start` and match it against known routes before acting on it since the start parameter is user-controlled.
- **Rate-limited dispatch.** Bottleneck with `maxConcurrent: 1`, `minTime: 50`, one queue per chat. Batch and send sequentially. Disable link previews on notifications.
- **Permissions.** Role hierarchy: owner > admin > manager > member, each inheriting from below. Early-return checks (`if (isOwner(userId)) return true`). Per-resource granularity with `canAdd`, `canRemove`, `canManage` when needed.
- **Formatting.** Escape `&`, `<`, `>` in user content. Build messages as `string[]` joined with `\n`. Use `<b>` for headers, `┄┄┄┄` separators for structure. Stay under 4096 chars.
- **Error handling.** Wrap every handler in `safe()` that catches and logs the update ID. Set `bot.catch()` as the global fallback.

## Watch Out For

- **Multiple `callback_query:data` handlers** can cause ordering issues. One router with prefix dispatch keeps it clean.
- **Markdown parse mode** has trouble with underscores and asterisks in user content. HTML is more reliable.
- **Long callback data strings** can exceed Telegram's 64-byte cap. Short prefixes and numeric IDs like `p:d:5` keep you safe.
- **Always call `answerCallbackQuery`** even with no text, so the button spinner clears properly.

## Project Structure

```
src/
  index.ts              # bot setup, handler registration
  config.ts             # env vars and flags
  lib/
    prisma.ts           # db client
    session.ts          # DM session map
    msg.ts              # formatters and builders
    utils.ts            # safeEdit, safeAnswer, escaping
  bot/
    commands/            # one file per command
    middleware/          # auth checks
  services/
    feature/             # business logic, dispatchers
```
