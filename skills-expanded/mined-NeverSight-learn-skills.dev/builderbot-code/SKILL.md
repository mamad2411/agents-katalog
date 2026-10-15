---
name: builderbot-code-skill
description: >-
  Expert assistant for BuilderBot (v1.4.0) — a TypeScript/JavaScript framework for building multi-platform chatbots (WhatsApp, Telegram, Instagram, Email, etc.).
  Use when creating or editing flows (addKeyword, addAnswer, addAction), wiring EVENTS, managing per-user state or globalState, configuring providers (Baileys, Meta, Telegram, Evolution, etc.) or databases (Mongo, Postgres, MySQL, JSON), implementing REST API endpoints (handleCtx, httpServer), debugging flow control (gotoFlow, endFlow, fallBack, idle, capture, flowDynamic), or handling blacklist logic.
  Architecture: Provider + Database + Flow.
---

# BuilderBot Code Skill

## Operate

1. **Identify the stack** — confirm provider package, database adapter, and flow entrypoints before writing code.
2. **Type the callback signature correctly**:
   - `ctx: BotContext` → `{ body, from, name, host, ...platform fields }`
   - `methods: BotMethods` → `{ flowDynamic, gotoFlow, endFlow, fallBack, state, globalState, blacklist, provider, database, extensions }`
3. **Enforce flow-control semantics** — these three MUST be `return`ed:
   - `return gotoFlow(flow)` · `return endFlow('msg')` · `return fallBack('msg')`
   - These MUST be `await`ed: `await flowDynamic(...)` · `await state.update(...)` · `await globalState.update(...)`
4. **Prefer small, composable flows** — one responsibility per flow file.
5. **Keep secrets in env vars** — never hardcode tokens, keys, or credentials.
6. **After writing any flow, run through the UX Review Checklist below** — simulate the conversation as the end-user and verify every item before considering the flow done.
7. **Always validate lint before finishing** — run `eslint . --no-ignore` and fix every error before delivering code.

## Critical Rules (common bugs)

| Bug | Wrong | Right |
|-----|-------|-------|
| Missing `return` on flow control | `gotoFlow(flow)` | `return gotoFlow(flow)` |
| Missing `await` on state/dynamic | `state.update({...})` | `await state.update({...})` |
| `flowDynamic` with raw string array | `flowDynamic(['a','b','c'])` — sends 3 separate messages | `flowDynamic([{ body: ['a','b','c'].join('\n'), delay: rnd() }])` |
| `flowDynamic` + `endFlow` in same callback | `await flowDynamic(...); return endFlow()` | Split into two chained `addAction` — first sends `flowDynamic`, second calls `return endFlow(...)` |
| Unnecessary dynamic import | `await import('./flow')` when no circular dependency exists | Top-level `import { flow } from './flow'` — only use dynamic import when flow A → B AND B → A |
| Circular ESM import | Top-level `import` between flows that reference each other | Dynamic `const { xFlow } = await import('./x.flow')` inside the callback |
| `idle` without `capture` | `{ idle: 5000 }` | `{ capture: true, idle: 5000 }` |
| Using `require()` in ESM | `require('./flow')` | `await import('./flow')` — project is `"type": "module"`, `require` is not available |
| Using buttons | `{ buttons: [...] }` | Text-based numbered menu + `capture: true` |
| Checking `idleFallBack` | `if (ctx?.idleFallBack) { ... }` | Never use `idleFallBack` — just set `{ capture: true, idle: N }` and let the flow expire automatically |

## Flow Chain

```typescript
addKeyword(keywords, options?)        // ActionPropertiesKeyword: capture, idle, media, delay, regex, sensitive  ← NEVER use `buttons`
  .addAnswer(message, options?, cb?, childFlows?)
  .addAction(cb)
// cb: async (ctx: BotContext, methods: BotMethods) => void
```

## State Quick Reference

```typescript
// Per-user
await state.update({ key: value })
state.get('key')            // dot notation supported: 'user.profile.name'
state.getMyState()
state.clear()

// Global (shared across all users)
await globalState.update({ key: value })
globalState.get('key')
globalState.getAllState()
```

## UX Review Checklist

After building any flow, mentally walk through the conversation **as the end-user** and verify every point below. Fix anything that fails before delivering the code.

| # | Question | What to check / fix |
|---|----------|----------------------|
| 1 | Does every prompt tell the user exactly what to type? | Each `addAnswer` with `capture: true` must state the expected input (e.g. "Reply with *1*, *2*, or *3*"). |
| 2 | Are all invalid inputs handled? | Every captured step must have a `fallBack('...')` branch for bad input. |
| 3 | Is there an idle timeout on long captures? | Add `{ capture: true, idle: 60000 }` — the flow will automatically expire after the timeout. |
| 4 | Can the user always exit? | Provide a cancel keyword (e.g. "cancel", "salir") or honour it inside captures and call `return endFlow('...')`. |
| 5 | Are messages short, mobile-friendly, and max 3-4 bubbles? | No wall-of-text AND no bubble spam. Group lines with `\n` inside one `FlowDynamicMessage.body`. Each string in a `flowDynamic([...])` array = a separate WhatsApp message — never spread long lists. Add random delay per bubble. |
| 6 | Is the user's name used where natural? | Greetings and confirmations should reference `ctx.name` when available. |
| 7 | Are menus numbered text lists (never `buttons`)? | Use `['Option 1', '1. Foo', '2. Bar']` + `capture: true` + `fallBack`. |
| 8 | Does each multi-step flow confirm before committing? | Before irreversible actions (order, payment, delete) show a summary and ask "confirm? *yes / no*". |
| 9 | Does the flow end with a clear closing message? | The final step must tell the user what happened and what to do next (or say goodbye). |
| 10 | Are error messages actionable? | Never say just "error". Say what went wrong and how to fix it: `return fallBack('That doesn\'t look like a valid email. Try again:')` |

## WhatsApp Text Formatting

WhatsApp uses its own markdown — always apply it in message strings.

| Style | Syntax | Example |
|-------|--------|---------|
| Bold | `*text*` | `*Pepperoni*` |
| Italic | `_text_` | `_Tomate y mozzarella_` |
| Strikethrough | `~text~` | `~$15~` |
| Monospace | ` ```text``` ` | ` ```CODE123``` ` |
| Bullet list | `•` or `-` | `• Opción 1` |

### Rules
- Use `*bold*` for product names, totals, section headers, and actions the user must take.
- Use `_italic_` for descriptions, hints, and secondary info.
- Use `•` (not `-`) for list items — renders cleaner on mobile.
- Use `━━━━━━━` (or `---`) as a visual divider between sections inside one bubble.
- **Never** use HTML tags (`<b>`, `<br>`, etc.) — WhatsApp ignores them.
- **Never** use standard markdown (`**bold**`, `## heading`) — not supported.

### Example — well-formatted bubble

```typescript
const body = [
    '*🍕 Tu pedido*',
    '━━━━━━━━━━━━━━',
    `• Pizza: *Pepperoni*`,
    `• Tamaño: *Mediana (30 cm)*`,
    `• Cantidad: *2*`,
    '',
    `💰 Total: *$26 USD*`,
    '',
    '_Responde *sí* para confirmar o *no* para cancelar._',
].join('\n')
```

## WhatsApp Messaging Norms

> These rules apply to every flow. Violating them makes the bot feel like spam.

**Critical distinction — `flowDynamic` vs `addAnswer` with arrays:**

| Call | Array behavior |
|------|---------------|
| `flowDynamic(['a','b','c'])` | ⚠️ Each string = **separate WhatsApp message** |
| `addAnswer(['a','b','c'])` | ✅ Joined into **one message** with line breaks |

> Always use `FlowDynamicMessage[]` with `.join('\n')` in `body` when calling `flowDynamic`. Never pass raw string arrays.

| Rule | Wrong | Right |
|------|-------|-------|
| Max 3-4 bubbles per turn | `flowDynamic(['line1','line2','line3',...])` → each string = 1 bubble | `flowDynamic([{ body: ['line1','line2','line3'].join('\n'), delay: rnd() }])` |
| Always use random delay | No delay between bubbles | `delay: Math.floor(Math.random() * 800) + 500` on each bubble |
| Never spread item lists | `flowDynamic([...items.map(...)])` | `flowDynamic([{ body: items.map(...).join('\n'), delay: rnd() }])` |

### Random delay helper (define once per file)

```typescript
const rnd = () => Math.floor(Math.random() * 800) + 500
```

### Correct pattern — 3 bubbles max

```typescript
await flowDynamic([
    {
        body: [
            '*Título*',
            '',
            items.map(i => `• ${i.name} — $${i.price}`).join('\n'),
        ].join('\n'),
        delay: rnd(),
    },
    {
        body: '*Sección 2*\nLínea A\nLínea B',
        delay: rnd(),
    },
])
// addAnswer o addAction siguiente = bubble 3
```

## Presence Update (Baileys / Sherpa only)

> Simulates "typing..." or "recording..." before sending a message. Makes the bot feel human. Only available with `BaileysProvider` and `SherpaProvider`.

```typescript
type WAPresence = 'unavailable' | 'available' | 'composing' | 'recording' | 'paused'
// composing = typing bubble   recording = audio bubble
```

### Pattern — typing indicator before each message

```typescript
const waitT = (ms: number) => new Promise(resolve => setTimeout(resolve, ms))

.addAction(async (ctx, { provider, flowDynamic }) => {
    await provider.vendor.sendPresenceUpdate('composing', ctx.key.remoteJid)
    await waitT(1500)
    await flowDynamic([{ body: 'Mensaje que parece escrito por humano', delay: rnd() }])
    await provider.vendor.sendPresenceUpdate('paused', ctx.key.remoteJid)
})
```

### Rules
- Always call `sendPresenceUpdate('paused', ...)` after sending — clears the indicator.
- Combine with `rnd()` delays: presence update → wait → `flowDynamic` → paused.
- Use `composing` for text replies, `recording` for audio context.
- **Never use on non-Baileys/Sherpa providers** — will throw at runtime.

## Debug Checklist

- Flow not switching → `return gotoFlow(...)`
- Session not ending → `return endFlow(...)`
- Fallback not repeating → `return fallBack(...)`
- State not saved → `await state.update(...)`
- Idle not firing → add `capture: true` alongside `idle` (never check `idleFallBack`)
- EVENTS flow not triggering → verify provider maps the event payload to `EVENTS.*`
- Circular import crash → use dynamic `await import()` inside the callback (never `require()`)
- Language server shows "Cannot find module" on dynamic imports → check if a circular dep actually exists; if not, replace with static top-level `import`
- ESLint errors after changes → run `eslint . --no-ignore` and fix before finishing
- `builderbot/func-prefix-endflow-flowdynamic` error → `flowDynamic` and `endFlow` are in the same callback; split into two chained `addAction`:
  ```typescript
  .addAction(async (_, { flowDynamic }) => { await flowDynamic(lines) })
  .addAction(async (_, { endFlow }) => { return endFlow('bye') })
  ```

## Module System

This project uses **ESM** (`"type": "module"` in package.json, `"module": "ES2022"` in tsconfig).
- **NEVER** use `require()` — it is not available in ESM.
- **Default: use static top-level imports.** Dynamic imports cause TypeScript language server errors when no circular dependency exists.
- **Before using `await import()`**, draw the dependency graph. Dynamic import is only justified when flow A calls flow B **and** flow B calls flow A (a real cycle).

```
✅ Static (no cycle):  welcome → menu → order → payment
   import { orderFlow } from './order.flow'   ← top of file

✅ Dynamic (real cycle): welcome ↔ order
   const { orderFlow } = await import('./order.flow')  ← inside callback
```

When flows reference each other (circular), use **dynamic `import()`** inside the callback:

```typescript
.addAction(async (ctx, { gotoFlow }) => {
    const { targetFlow } = await import('./target.flow')
    return gotoFlow(targetFlow)
})
```

## Modular Structure (recommended)

Organize flows in a `src/flows/` directory with a barrel `index.ts` that exports the assembled flow:

```
src/
├── app.ts
├── flows/
│   ├── index.ts            # createFlow([...all flows])
│   ├── welcome.flow.ts
│   └── order.flow.ts
└── services/
```

```typescript
// src/flows/index.ts
import { createFlow } from '@builderbot/bot'
import { welcomeFlow } from './welcome.flow'
import { orderFlow } from './order.flow'

export const flow = createFlow([welcomeFlow, orderFlow])
```

```typescript
// src/app.ts
import { createBot, createProvider } from '@builderbot/bot'
import { MemoryDB as Database } from '@builderbot/bot'
import { BaileysProvider as Provider } from '@builderbot/provider-baileys'
import { flow } from './flows'

const main = async () => {
    const provider = createProvider(Provider)
    const database = new Database()
    await createBot({ flow, provider, database })
    provider.initHttpServer(+(process.env.PORT ?? 3008))
}
main()
```

## References

- Code patterns (scaffold, capture, gotoFlow, media, idle, flowDynamic, fallBack, REST, EVENTS, UX patterns): [patterns.md](patterns.md)
- Provider configs, database configs, TypeScript types: [providers.md](providers.md)
