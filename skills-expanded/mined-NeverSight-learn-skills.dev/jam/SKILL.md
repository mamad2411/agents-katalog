---
name: jam
description: Talk with the user in a browser window where your replies render as rich, beautifully-typeset HTML instead of terminal markdown. Use when a reply genuinely needs visual layout the terminal can't carry — diagrams, charts, or dense side-by-side comparisons — or when the user asks to move the conversation into a browser ("let's jam", "chat in the browser"), not for answers that read fine as terminal markdown.
---

# jam

`jam` opens a browser window where the user types to you and you reply with
**rich HTML** (or plain text) that renders full-width in a scrolling transcript.
Each message the user sends is a turn; you answer, your reply renders in the
browser, and you loop until they end the chat.

It's a two-process tool: `open` hosts the server and blocks; `poll` is a
short-lived call that waits for the next message. You run `open` once in the
background, then loop on `poll`.

## Running jam

Run every command below as `jam <command>` (e.g. `jam open`). If `jam` isn't
found, install it with `npm install -g jam-skill-cli` and retry. If that install
fails too, run it as `npx -y jam-skill-cli <command>`.

## Loop

1. **Open once, backgrounded.** Run `jam open` as a **background
   task**. It opens the chat in the user's browser and prints one JSON line —
   `{ "session": "brave-otter", "url": "http://127.0.0.1:<port>/" }` — then stays
   running to host the chat. Capture the `session` id; you pass it to every `poll`.
   To **open with your first turn already showing**, pass a format flag and pipe
   the message body on stdin, exactly as you send a reply (see **Composing a
   reply**): `jam open --html` (or `--text`). Only open with a turn
   when it carries something substantive — a summary of what you've prepared or a
   specific question. Don't open with a generic greeting like "Hi, how can I
   help?"; if you have nothing to lead with, just run `jam open` with
   no format flag and let the user's first message set the direction.
2. **Poll for the next message.** Run `jam poll <session>`. It
   **long-polls** — silent until the user sends a message or ends the chat — then
   prints one JSON envelope and exits. Leave it running; if your harness kills or
   times it out, re-run it.
3. **Act on the envelope's `status`:**
   - **`message`** — the user's turn (`{ status, id, text, at }`). Compose your
     reply (see below) and send it **with the next poll** by piping it on stdin:
     `jam poll <session> --html` (or `--text`) posts the reply and
     waits for the next message in one call.
   - **`ended`** — the user clicked **End chat**; the `open` task exits on its
     own. You're done.

## Talk through jam, not the terminal

While the chat is open the user is in the browser and the terminal goes unread.
Route **everything** meant for them — answers, questions, pushback — through the
reply on the next `poll`, never plain terminal output.

## Make it easy to understand

Optimize every reply for the user *getting it* — not for packing in the most
information. **Use plain language without sacrificing technical precision; simplify
the prose, not the substance.** Give ideas room to breathe: keep sentences short,
break things into steps, and define terms as you use them. The layout and visuals below serve comprehension, never
decoration. A reply that's dense, clever, and correct has still failed if the user
has to work to follow it.

## Composing a reply

Send your reply on **stdin**. Use a heredoc so the HTML never touches argv or the
filesystem:

```
jam poll brave-otter --html <<'HTML'
<h2>Two ways to cache this</h2>
<p>The tradeoff is freshness versus load. Here's the shape of each:</p>
<div class="jam-grid jam-cols-2">
  <div class="jam-card">
    <h3>Write-through</h3>
    <p>Every write updates the cache too. Always fresh; slower writes.</p>
  </div>
  <div class="jam-card">
    <h3>TTL</h3>
    <p>Entries expire after a fixed window. Fast writes; can serve stale reads.</p>
  </div>
</div>
<div class="jam-callout note"><strong>Recommendation:</strong> start with TTL —
it's simpler and your reads tolerate a few seconds of staleness.</div>
HTML
```

Lean into **rich, visually engaging HTML** whenever it makes the answer clearer —
comparisons, steps, code, stats, callouts, diagrams, charts, or an explanation
that simply reads better laid out. Make replies a pleasure to read, not markdown
in a window. Use `--text` when a reply is genuinely plain and layout would add
nothing. Prefer
the **design language** below over ad-hoc CSS. Inline `style` is fine for a
genuine one-off.

**Never include** `<script>`, `<style>`, `<link>`, or `on*` handlers. Write
plain, semantic HTML; the app's stylesheet already themes it.

## The design language

Everything below is already defined in the app's CSS and in scope for your turn.
Compose with these classes and tokens instead of reinventing styles.

### Prose

Plain semantic tags are themed for you — a warm serif reading column, sans
headings, mono code. Just write `<h2>`, `<p>`, `<ul>`, `<blockquote>`,
`<table>`, `<pre><code>…</code></pre>`. **Always** name the language on real code
with a `language-xxx` class — `<pre><code class="language-python">` — and the app
highlights it. Write the code as plain source (no token `<span>`s), HTML-escaped
like any other markup you emit. For preformatted **non-code** — a log, a shell
transcript, ASCII, a directory tree — use a plain `<pre>` on its own (no inner
`<code>`); it renders monospaced but uncolored. Supported
languages: `bash`, `c`, `cpp`, `csharp`, `css`, `diff`, `go`, `java`,
`javascript`, `json`, `markdown`, `python`, `ruby`, `rust`, `sql`, `typescript`,
`xml`/`html`, `yaml`.

### Math (LaTeX)

Write math as raw LaTeX inside a tagged element and the app typesets it in place —
the element holds only the bare expression, **no** `$…$` or `\(…\)` delimiters. The
class picks the mode:

- **Inline**, within a sentence — a `<span class="jam-math">`:
  `the area is <span class="jam-math">\int_0^1 x^2\,dx = \tfrac13</span>, so…`
- **Display**, a centered block on its own line — a `<div class="jam-math-display">`:
  `<div class="jam-math-display">E = mc^2</div>`

The TeX lives in HTML, so escape `<` and `&` like any markup (`a &lt; b`); the
`\lt \gt \le \ge \ne` commands sidestep the comparison escapes.

### Visualizations

Reach for hand-authored inline `<svg>` when a diagram or chart lands an idea
better than prose (there are no scripts, so no charting libraries). Give it a
`viewBox` and `style="width: 100%; height: auto"` so it scales to the column.

### Component classes

- **`.jam-card`** — an elevated panel. Group a chunk of the reply.
- **`.jam-callout`** with a variant — a colored aside:
  `.jam-callout.note` (accent), `.jam-callout.success`, `.jam-callout.warn`,
  `.jam-callout.danger`.
- **`.jam-grid`** + **`.jam-cols-2`** / **`.jam-cols-3`** — an even multi-column row
  (collapses to one column when narrow). Wrap `.jam-card`s in it for side-by-side.
- **`.jam-metric`** with **`.jam-metric-value`** + **`.jam-metric-label`** — a big
  number over a label, for a stat:
  `<div class="jam-metric"><span class="jam-metric-value">3.2s</span><span class="jam-metric-label">p95 latency</span></div>`
- **`.jam-badge`** — a small inline pill for a tag or status.
- **`.jam-divider`** — a hairline rule (`<hr class="jam-divider">`) between sections.

### Tokens (CSS custom properties)

Use these in an inline `style` for a one-off so it stays on-palette:

- Color: `--jam-bg`, `--jam-surface`, `--jam-ink`, `--jam-ink-muted`, `--jam-accent`,
  `--jam-border`, and semantic `--jam-success` / `--jam-warn` / `--jam-danger`.
- Type scale: `--jam-text-sm`, `--jam-text-base`, `--jam-text-lg`, `--jam-text-xl`,
  `--jam-text-2xl`.
- Spacing: `--jam-space-1` … `--jam-space-8`.
- `--jam-radius`, `--jam-shadow`, and the fonts `--jam-font-serif` / `--jam-font-sans`
  / `--jam-font-mono`.

## Ending

You have no end command — the chat ends when the user clicks **End chat** in the
browser, which tears down the `open` task and makes `poll` return
`{ status: "ended" }`. Stop the loop; the conversation continues back in the
terminal.

## Commands

```
jam open                   # host the chat (run backgrounded); prints { session, url }
jam open --html            # host the chat, seeding an opening HTML message from stdin
jam open --text            # host the chat, seeding an opening text message from stdin
jam poll <session>         # wait for the next message
jam poll <session> --html  # post an HTML reply on stdin, then wait
jam poll <session> --text  # post a text reply on stdin, then wait
```
