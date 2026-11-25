---
name: agentic-chat-interface
description: >-
  Build a production-grade streaming agentic chat front-end — the
  /paieska interface: an SSE-streamed conversation with a live
  tool-call timeline, collapsible "thinking" panel, typing/status
  animations, auto-growing input, stop/retry/abort, and graceful
  failure. Use when building ANY chat UI for an LLM/agent backend:
  a support assistant, a research agent, an admin copilot, a
  data-Q&A surface. Triggers on: "chat interface", "streaming
  assistant UI", "agent front-end", "tool-call timeline", "SSE chat",
  "real-time AI chat", or porting the /paieska UX to a new product.
  The canonical implementation is app/paieska/chat-view.tsx (client)
  + app/api/search/chat/route.ts (server) in this repo — read them
  alongside this skill.
---

# Agentic chat interface

A complete, battle-tested pattern for a streaming agent chat front-end.
This is the architecture behind `/paieska` (LIRR's AI company-search).
It is deliberately framework-light (React + `fetch` + the streams API +
Tailwind + lucide icons — **no chat library, no SSE library**) so it
ports cleanly into any Next.js/React product.

**Canonical files — read them as you build:**
- `app/paieska/chat-view.tsx` — the entire client (state machine,
  stream consumer, every animated component). ~1130 lines.
- `app/api/search/chat/route.ts` — the SSE producer (the `send()`
  helper, heartbeat, abort, interim/final bucketing). ~686 lines.
- `app/paieska/page.tsx` / `sidebar.tsx` — page shell + conversation
  list (optional; only needed for multi-thread logged-in chat).

The single most important idea: **the front-end and the agent backend
are decoupled by one thing — a well-defined SSE event contract.** Get
that contract right and you can swap either side freely. Everything
below serves that contract.

---

## 1. The reusable seam — the SSE event contract

The server streams `text/event-stream`. Each event is
`event: <type>\ndata: <json>\n\n`. Comment lines (`: ping …`) are
heartbeats and are ignored by the client. The client buffers raw bytes,
splits on `\n\n`, and dispatches on `<type>`.

**These ten event types are the entire interface.** A new agent backend
only has to emit these; a new front-end only has to consume them.

| `event:` | `data` payload | UI effect |
|----------|----------------|-----------|
| `status` | `{ step, round?, attempt? }` | sets the streaming status pill text ("Analizuoju užklausą", "Ieškau duomenų · 2 žingsnis", "Kartoju (bandymas 2/3)"…) |
| `phase` | `{ phase: "planning" \| "answering" }` | flips the message phase; "answering" clears the status pill |
| `tool_use` | `{ tool, input, round }` | pushes a step into the tool-call timeline (icon + verb + query hint, spinner running) |
| `tool_result` | `{ tool, summary }` | attaches the result summary to the most-recent matching unresolved tool step (spinner → "→ N rasta") |
| `interim_text` | `{ content }` | appends to the collapsible "AI mąstymas" (planning) text — reasoning **between** tool calls |
| `text` | `{ content }` | appends a delta to the **final answer** (the main bubble); clears status |
| `text_bulk` | `{ content }` | replaces the final answer wholesale (server decided the last round's text WAS the answer) |
| `interim_commit_final` | `{ length }` | trims the last `length` chars off interim text because they were promoted to the final answer (prevents duplication) |
| `error` | `{ message, canRetry, partial }` | injects a system message; arms the retry banner if `canRetry` |
| `done` | `{}` | marks the message `phase: "done"`, collapses the thinking block, shows the "✓ atsakymas pateiktas" chip |

**Why two text channels (`interim_text` vs `text`)?** An agent that uses
tools produces *reasoning between tool calls* (planning) and *a final
answer*. Conflating them makes the UI a wall of text. The contract
keeps them separate: planning text lives in a collapsible panel; the
answer is the clean main bubble. The `interim_commit_final` event
exists for the case where the agent's "planning" in the last round
turns out to be the answer — the server promotes it and tells the
client to de-dupe.

**Server-side producer shape** (`route.ts:339`):

```ts
const stream = new ReadableStream({
  async start(controller) {
    let closed = false
    const send = (event: string, data: unknown) => {
      if (closed) return
      try { controller.enqueue(encoder.encode(`event: ${event}\ndata: ${JSON.stringify(data)}\n\n`)) }
      catch { closed = true }
    }
    const heartbeat = setInterval(() => {        // keeps proxies from closing idle stream
      if (!closed) try { controller.enqueue(encoder.encode(`: ping ${Date.now()}\n\n`)) } catch { closed = true }
    }, HEARTBEAT_INTERVAL_MS)
    request.signal.addEventListener('abort', () => { abortController.abort(); closed = true })
    // … agentic loop: send('status',…); send('tool_use',…); send('text',…); send('done',{})
  }
})
return new Response(stream, { headers: {
  'Content-Type': 'text/event-stream', 'Cache-Control': 'no-cache, no-transform', 'Connection': 'keep-alive',
}})
```

---

## 2. Client architecture — the stream consumer

State (`chat-view.tsx:134`):

```ts
const [messages, setMessages] = useState<ChatMessage[]>([])   // the transcript
const [isStreaming, setIsStreaming] = useState(false)
const [streamStatus, setStreamStatus] = useState<string | null>(null)  // the pill text
const abortControllerRef = useRef<AbortController | null>(null)
const stallTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null)
```

Each `ChatMessage` carries: `role`, `content` (final answer only),
`interimText` (planning), `toolCalls[]`, `phase` (`planning` |
`answering` | `done`). One assistant message accumulates all four as
events arrive.

**The consume loop** (`chat-view.tsx:383`) — copy this almost verbatim;
it is the heart and it is correct:

```ts
const reader = res.body!.getReader()
const decoder = new TextDecoder()
let buffer = ""
while (true) {
  const { done, value } = await reader.read()
  if (done) break
  resetStallTimeout()                      // per-chunk 60s stall watchdog
  buffer += decoder.decode(value, { stream: true })
  const events = buffer.split("\n\n")
  buffer = events.pop() || ""              // keep the incomplete trailing event
  for (const rawEvent of events) {
    if (!rawEvent.trim() || rawEvent.startsWith(":")) continue   // skip heartbeats
    let eventType = "message", dataStr = ""
    for (const line of rawEvent.split("\n")) {
      if (line.startsWith("event: ")) eventType = line.slice(7).trim()
      else if (line.startsWith("data: ")) dataStr = line.slice(6)
    }
    if (!dataStr) continue
    let data; try { data = JSON.parse(dataStr) } catch { continue }
    switch (eventType) { /* …the 10 cases above… */ }
  }
}
```

Local accumulators (`interimText`, `finalText`, `phase`, `toolCalls[]`)
are mutated as events arrive, then flushed to React via a single
`updateAssistant()` that maps the in-flight assistant message. Mutate
locals, flush once per event — not a `setState` per token.

**Resilience primitives (all of them matter):**
- **AbortController** (`:238`) — `stopStreaming()` aborts the fetch; a
  new send aborts any in-flight one first.
- **60s stall watchdog** (`:322`) — a per-chunk timeout. If no bytes
  arrive for 60s, abort + inject a "took too long, retry" system
  message + arm retry. Reset on every chunk.
- **Heartbeat tolerance** — `:`-prefixed lines are skipped, so the
  server's keep-alive pings don't corrupt parsing.
- **Retry** (`lastFailedQuery`) — on `error{canRetry}` or stall, stash
  the query and show a retry banner; `retryLastMessage()` re-streams.
- **Graceful 401** — if the backend gates (auth/quota), it returns a
  JSON 401 *before* the stream; the client reads `requiresLogin` and
  renders a login CTA instead of erroring.

**Persistence** (optional): anonymous chats persist to
`localStorage` (last 50 msgs); logged-in chats load/save under a
`conversationId` via REST. Decouple this — it's not core to the UX.

---

## 3. Animations & micro-interactions — the complete inventory

This is the part that makes the interface feel alive. Every animation
below is real, in `chat-view.tsx`, with its exact Tailwind classes.
Reproduce them precisely; they are tuned.

### 3.1 Streaming status pill (`:817`)
The "what's happening right now" indicator. A **pulsing dot + text**:
```tsx
<span className="relative inline-flex h-1.5 w-1.5">
  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary/60 opacity-75" />
  <span className="relative inline-flex rounded-full h-1.5 w-1.5 bg-primary" />
</span>
{streamStatus}…
```
The `animate-ping` (Tailwind's scale+fade keyframe) on a translucent
clone over a solid dot = the classic "live" radar ping. Text comes from
`status` events ("Analizuoju užklausą", "Ieškau duomenų · 2 žingsnis").
Shown only while `isStreaming && streamStatus` is set; cleared the
moment `text`/`text_bulk` arrives.

### 3.2 Thinking block — collapsible tool timeline (`:872`)
Container border + tint **transition on active state**:
```
isActive → "border-primary/30 bg-primary/[0.03]"   (live, primary tint)
else     → "border-border/50 bg-muted/20"          (resting, muted)
with `transition-colors`
```
- Header left icon: `Loader2` with `animate-spin text-primary` while
  active; swaps to a static `Database` icon when done.
- Header label is **pluralised live** ("Atlikta 3 paieškos…" while
  running → "Mąstymo procesas · 3 paieškos" when done).
- Chevron: `transition-transform` + `rotate-180` when expanded.
- **Auto-expand while streaming, auto-collapse when the answer
  arrives** (`useEffect` on `hasAnswer`/`isActive`, `:858`). This is
  the key UX move: the user watches the agent think, then the noise
  folds away and the clean answer remains. They can re-expand any time.
- Expanded body reveals with the natural layout (no JS opacity tween) —
  base content is visible without animation; only the border/tint and
  chevron animate.

### 3.3 Tool step row (`:966`)
Each step in the timeline:
- **Icon-in-tile with a numbered badge.** A 6×6 rounded tile, tinted by
  the tool's *tone* (`search`/`profile`/`compare`/`risk`/`meta` → bg +
  text + ring classes in `TONE_CLASSES`), with a tiny step-number badge
  floated `-top-1 -right-1` (`tabular-nums`, original step index
  preserved even when older steps are hidden).
- **Running highlight:** the whole `<li>` gets `bg-primary/[0.03]` while
  `isRunning` (no result yet), via `transition-colors`.
- **Live verb → noun swap:** while running, shows the action verb +
  ellipsis ("ieškau…"); when done, shows the label ("paieška pagal
  vardą").
- **Result reveal:** when `tool_result` lands, append `→ <summary>` in
  `emerald-700/85` (or muted if the result matches the empty-result
  regex `0 / nerasta`). A trailing `Loader2 animate-spin` shows only
  while running.
- **Overflow cap:** at >5 steps, the oldest collapse behind a "Rodyti
  ankstesnius N veiksmų" button (`ToolStepList`, `:921`). Keeps long
  agentic sessions scannable; newest (running) step always visible.

### 3.4 Tool metadata registry (`:43`, `TOOL_META`)
The mapping `toolName → { label, icon, action(verb), tone }` is THE
thing you re-skin per product. The timeline reads it for every step.
A default (`DEFAULT_TOOL_META`) covers unknown tools so the UI never
breaks when the backend adds a tool. **This registry is your main
customization surface** — see §5.

### 3.5 Assistant header + completion chip (`:793`)
Small uppercase "Asistentas" eyebrow. On `done` with an answer, a
`CheckCircle2 + "atsakymas pateiktas"` chip appears in `emerald-700`.
A `Sparkles` avatar in a `bg-primary/10` circle anchors each assistant
turn.

### 3.6 Input composer (`:673`)
- **Auto-growing textarea** (`:678`): on every change, set
  `height="auto"` then `height = min(scrollHeight, 180)px`. Grows with
  content to a 180px cap, then scrolls. `rows={1}` baseline.
- **Focus-within ring** (`:674`): the wrapper gets
  `focus-within:border-primary/50` + a soft
  `focus-within:shadow-[0_0_0_3px_rgb(0_0_0_/_0.02)]` — a subtle 3px
  halo, via `transition-all`. While streaming the wrapper tints
  `border-primary/30 bg-primary/[0.02]` instead.
- **Send ↔ Stop swap** (`:691`): a `Send` submit button (disabled +
  greyed when input empty) becomes a `Square` (filled) stop button
  while streaming, same position, `transition-all` on hover. Both are
  absolutely positioned `right-2 bottom-2`, 8×8, rounded.
- **Placeholder swaps** with state ("Klauskite apie Lietuvos įmones…" →
  "Generuojamas atsakymas… galite sustabdyti.").
- **Keyboard:** `Enter` sends, `Shift+Enter` newlines (in
  `handleKeyDown`); global `⌘K`/`Ctrl+K` focuses the input (`:223`).
  Footer shows the `<kbd>` hints.

### 3.7 Welcome screen quick-prompts (`:598`)
Shown only when `messages.length === 0`. Grouped suggestion columns;
each row a button with a `ChevronRight` that slides on hover
(`group-hover:translate-x-0.5 group-hover:text-primary transition-all`)
and the text brightens (`group-hover:text-foreground`). Clicking sends
the prompt immediately. This is the empty-state that teaches users what
to ask.

### 3.8 Retry banner (`:651`)
On a recoverable failure, an amber banner shows the truncated failed
query + a `RefreshCw` "Pabandyti dar kartą" button. Disappears once
streaming resumes.

### 3.9 Auto-scroll — near-bottom only (`:211`)
The single most-respected detail: **only auto-scroll if the reader is
already within 150px of the bottom** (`scrollHeight - scrollTop -
clientHeight < 150`). If they've scrolled up to read, a streaming
answer must NOT yank them back. Fires on `messages` + `streamStatus`
change, `behavior:"smooth"`.

### 3.10 Markdown answer rendering (`MarkdownText`, `:1016`+)
A tiny hand-rolled markdown renderer (no library) so the answer is
typographically rich but tightly controlled:
- **Headings** → sized by level; `##` gets a little `bg-primary` dot
  pill before it.
- **Bullets** → custom `▸` marker in `text-primary/60`.
- **Tables** → bordered, `bg-muted/30` header, `tabular-nums` cells,
  row `hover:bg-muted/10`, horizontal-scroll wrapper.
- **Inline** (`renderInline`, `:1098`): `**bold**`, `*italic*`, and
  links `[text](href)`. Internal links (`/…`) get an `ArrowUpRight`
  icon; external get `ExternalLink` + `target="_blank" rel=noopener`.
  This is how the agent's answer links straight to company pages.

### 3.11 Reduced motion & tokens
All colour comes from the design-system tokens (`primary`, `muted`,
`border`, `foreground`, `emerald`/`amber`/`rose` for states) — re-skin
by changing the theme, not the components. Type scale runs small and
dense (10–15px) for an information-rich, calm feel. If you add
keyframes, gate them behind `@media (prefers-reduced-motion: reduce)`.

---

## 4. Layout shell

`flex h-full flex-col` with a scrollable transcript (`flex-1
overflow-y-auto min-h-0`) above a pinned composer
(`shrink-0 border-t bg-background/95 backdrop-blur-md`). Transcript and
composer share a `max-w-[900px]` centered column. The `min-h-0` on the
scroll area is load-bearing — without it the flex child won't scroll.
A `transcriptEndRef` sentinel `<div>` at the bottom is the scroll
target.

---

## 5. Reuse checklist — what to copy, swap, keep

**Copy verbatim** (it's correct, don't reinvent):
- The SSE event contract (§1) and the consume loop (§2, `:383`).
- The resilience set: AbortController, 60s stall watchdog, heartbeat
  skipping, retry, graceful pre-stream 401.
- The animation classes in §3 — they're tuned.
- The near-bottom-only auto-scroll (§3.9).

**Swap per product:**
- `TOOL_META` (§3.4) — your tools, icons, verbs, tones. This is the
  main re-skin. Keep `DEFAULT_TOOL_META` so unknown tools degrade.
- `QUICK_PROMPTS` and all UI copy/locale (currently Lithuanian).
- The backend `fetch` URL + request body shape, and the agent loop that
  produces the events.
- `MarkdownText` link targets (here they deep-link `/registras/...`).
- Auth/quota/persistence (anon localStorage, conversationId) — fully
  optional; strip if your chat is single-thread and open.

**Keep (the invariants that make it good):**
- Two text channels (planning vs answer) — never collapse them.
- Mutate locals, flush once per event — never setState-per-token.
- Status pill cleared the instant the answer starts.
- Thinking block auto-collapses on answer; user can re-open.
- Provenance/links preserved in the rendered answer.

---

## 6. Core principles (code-simplifier — mandatory)

Adapted from the official
[code-simplifier](https://github.com/anthropics/claude-plugins-official/blob/main/plugins/code-simplifier/agents/code-simplifier.md)
agent. Apply when you port or extend this interface:

1. **Preserve behaviour** — refactors change *how*, never *what*. The
   stream loop and event contract are correct; don't "improve" their
   semantics, only their clarity.
2. **`function` keyword over arrows** for top-level/components; explicit
   prop types (see the `ChatViewProps`, `TranscriptBlock`,
   `ThinkingBlock`, `ToolStep` shapes).
3. **No nested ternaries** — the label pluralisation uses readable
   chained conditionals, not deep `?:`. Keep it that way.
4. **One renderer, one contract.** Don't fork a second event format or a
   second markdown renderer. If you add an event type, add it to the
   contract table AND both ends.
5. **Remove redundancy; keep the *why* comments** — the comments
   explaining "two text buckets", "near-bottom only", "per-chunk stall
   reset" are load-bearing. Keep them.
6. **Scope discipline** — re-skinning is `TOOL_META` + copy + theme
   tokens, not a rewrite of the stream loop.

## 7. You may — and should — customise

This is a strong default, not a cage. Different products need different
shapes: a code-assistant might add a `diff` event and a monospace
block; a voice agent might add `audio_chunk`; a research agent might add
a `citation` event with a sources rail. **Add them — extend the
contract table, emit from the backend, handle in the switch, render a
new component.** The constraints in §6 govern *how* you change things
(cleanly, one contract, behaviour preserved); they don't forbid
changing them. If the default UX is wrong for your situation, notice,
act, and explain — don't follow it off a cliff.

---

## 8. Anti-patterns (recognise and avoid)

- **`setState` per streamed token.** Murders performance. Mutate locals,
  flush once per event.
- **Collapsing planning text into the answer.** Produces a wall of
  reasoning where users want a clean answer. Keep the two channels.
- **Auto-scrolling unconditionally.** Makes a long streaming answer
  unreadable — the user can't scroll up. Near-bottom-only or nothing.
- **No abort / no stall timeout.** A hung backend = a spinner forever +
  a leaked connection. Both watchdogs are mandatory.
- **Parsing SSE without skipping `:` heartbeats.** Corrupts the buffer.
- **A markdown library for three features.** The hand-rolled renderer
  (~80 lines) is faster, smaller, and fully controllable. Don't pull in
  a 200KB dependency for bold/links/tables.
- **Pulsing/"live" affordances on static content.** The ping dot means
  "happening now". Don't decorate idle UI with it.
