---
name: interactive-answers
description: Answer in a hub chat with an interactive answer, a small HTML page shown inside the message in a sandboxed frame. Use when a comparison, figures, a diagram of how something works or a calculator helps the reader more than text; it says when text is enough, how to send the page, the bridge evo-answer/1, CDN libraries, the hub's colour tokens, both themes, 375 px, keyboard and focus, and how to check numbers.
---

# Interactive answers

In a chat of the hub you may answer with a page you write (HTML, CSS and script). The web shows it under your message,
in a frame with an opaque origin: it reads no cookie, reaches no server and submits no form. The reference is the
section "Interactive answers" of `docs/hub.md`.

## When to answer with a page

Make a page when the reader will do something with it:

- compare options on several axes (a table they can sort or filter, a chart they can switch);
- read figures (a chart, a breakdown, a timeline);
- see how a mechanism works (a diagram with steps they can step through);
- try values (a calculator, a what-if with sliders).

Answer in text alone when the question has a direct answer (a yes, a name, a command, a link, a short explanation), when
the page would only restate the text, or when you are asked to change code. A page never replaces the text.

## Send it

1. Write one HTML file, CSS and script inline, at most 1 MiB. Put the data in the page: the frame cannot fetch, so no
   `fetch`, XHR, WebSocket or form.
2. Post it with its message:

   ```
   evo-agents worker chat post "TEXT" --attach answer.html --interactive
   ```

   `evo-agents worker output --interactive answer.html` also marks it, and it goes under your next message.
3. TEXT must stand alone: the answer, its main figures and what you assumed. Telegram, bridged groups, notices and the
   mobile app show TEXT and no frame.

A file that is not HTML, or is over the limit, is refused with the reason. Fix it and send again.

## Libraries

- **A chat that is not restricted**: scripts, styles, fonts and images may come from the hub itself (its helper and
  tokens, below) and from `https://esm.sh`, `https://cdn.jsdelivr.net` and `https://cdnjs.cloudflare.com`, nowhere
  else. Pin the exact version in every CDN URL (`https://esm.sh/chart.js@4.4.1`,
  `https://cdn.jsdelivr.net/npm/d3@7.9.0/+esm`), never `latest` or a bare name. Load only what the page uses.
- **A restricted chat** (your prompt says so): nothing loads from outside, not even the hub's helper and tokens, so
  write plain SVG, canvas and DOM, or answer in text.

Prefer a small library over a framework: a chart, a diagram or a table needs no React.

## The bridge evo-answer/1

The page talks to the chat by `postMessage` on `parent`. Four methods:

| Method | params | Result | What it does |
| --- | --- | --- | --- |
| `context` | none | `{bridge, theme: "light" or "dark", locale}` | the viewer's theme and language |
| `resize` | `{height}` in px | `{height}`, the height kept (120 to 1600) | sizes the frame; send it after each change of layout |
| `sendPrompt` | `{text}`, 1 to 4000 characters after trimming | `{message_id}` | posts the reader's follow-up in this thread, which starts your next turn |
| `openLink` | `{url}`, https only | `{opened: true}` | opens it in a new tab |

An error carries `{code, message}` and, for `rate_limited` (429) and `hub_refused`, `status`. The web also posts
`{bridge, event: "theme", theme}` when the viewer switches theme.

### In a chat that is not restricted: the hub's helper

Load the hub's tokens and helper from the hub itself (`'self'` is allowed there):

```html
<link rel="stylesheet" href="/v1/plugin-ui/kit/1/evo-ui.css">
<script src="/v1/plugin-ui/kit/1/evo-answer.js"></script>
```

The helper gives `window.evoAnswer`: `ready` (a promise of the context), `sendPrompt(text)`, `openLink(url)`,
`resize(height?)`, `onTheme(listener)` (returns how to stop) and `call(method, params)`, each a promise of the result
that rejects with an `Error` carrying `code` (and `status`). It puts the theme on `<html>` as class `dark`, which
`evo-ui.css` reads, sets `<html lang>`, and keeps the frame's height to the page's own; `<html data-evo-resize="off">`
turns that off, and you call `resize` yourself.

```html
<script>
  evoAnswer.ready.then(({ theme, locale }) => draw(theme, locale));
  evoAnswer.onTheme((theme) => draw(theme));
</script>
```

### In a restricted chat: post the messages yourself

There the answer is served without `'self'`, so neither `evo-ui.css` nor `evo-answer.js` loads. Post the requests
yourself: a request is `{bridge: "evo-answer/1", id, method, params}`, the answer `{bridge, id, result}` or
`{bridge, id, error}`, and only messages from `parent` count. Copy the tokens below into the page.

```html
<script>
  const BRIDGE = "evo-answer/1";
  let next = 0;
  const waiting = new Map();
  addEventListener("message", (event) => {
    const m = event.data;
    if (event.source !== parent || !m || m.bridge !== BRIDGE) return;
    if (m.event === "theme") return document.documentElement.classList.toggle("dark", m.theme === "dark");
    if (!waiting.has(m.id)) return;
    const { resolve, reject } = waiting.get(m.id);
    waiting.delete(m.id);
    m.error ? reject(m.error) : resolve(m.result);
  });
  function call(method, params = {}) {
    const id = ++next;
    return new Promise((resolve, reject) => {
      waiting.set(id, { resolve, reject });
      parent.postMessage({ bridge: BRIDGE, id, method, params }, "*");
    });
  }
  const fit = () => call("resize", { height: Math.ceil(document.documentElement.scrollHeight) });
  new ResizeObserver(fit).observe(document.body);
  call("context").then(({ theme, locale }) => {
    document.documentElement.classList.toggle("dark", theme === "dark");
    document.documentElement.lang = locale;
  });
</script>
```

A follow-up button carries what the reader chose, so your next turn knows it without asking:

```js
const text = `Compare plan ${plan.value} at ${users.value} users over ${months.value} months`;
ask.onclick = () => evoAnswer.sendPrompt(text); // restricted chat: call("sendPrompt", { text })
```

Disable the button while its call is pending, and show the error when one comes back (a person may send at most 6
such messages a minute).

## Look like the hub

Use the hub's tokens and its font, IBM Plex Sans (`ui-sans-serif, system-ui, sans-serif` after it), and follow the
theme `context` gives, defaulting to light. In a chat that is not restricted, `evo-ui.css` brings them; in a restricted
one, copy them:

```css
:root {
  color-scheme: light;
  --font-sans: "IBM Plex Sans", ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
  --font-mono: "IBM Plex Mono", ui-monospace, "SF Mono", Menlo, Consolas, monospace;
  --canvas: #ffffff; --surface-sunken: #f4f4f5; --surface-hover: #f4f4f5; --surface-selected: #eef0fd;
  --border: #e4e4e7; --border-strong: #d4d4d8; --border-control: #8b8b94;
  --fg: #09090b; --fg-muted: #52525b; --fg-subtle: #6b6b73;
  --brand: #2f4bd8; --brand-soft: #ebeefd; --on-brand: #ffffff;
  --success: #11713d; --attention: #8a4b00; --danger: #b3261e;
  --chart-1: #2f4bd8; --chart-2: #bc7800; --chart-3: #0f8c80; --chart-4: #7c4de8; --chart-5: #85858d;
  --radius-sm: 6px; --radius-md: 8px; --space-2: 8px; --space-3: 12px; --space-4: 16px;
}
:root.dark {
  color-scheme: dark;
  --canvas: #09090b; --surface-sunken: #18181b; --surface-hover: #18181b; --surface-selected: #1c2147;
  --border: #27272a; --border-strong: #3f3f46; --border-control: #71717a;
  --fg: #fafafa; --fg-muted: #a1a1aa; --fg-subtle: #8b8b94;
  --brand: #8c9dff; --brand-soft: #19204a; --on-brand: #09090b;
  --success: #5fd394; --attention: #f2b54a; --danger: #ff8178;
  --chart-1: #8c9dff; --chart-2: #e9a23b; --chart-3: #2dc2b0; --chart-4: #9d7df6; --chart-5: #71717a;
}
body { margin: 0; padding: var(--space-3); background: var(--canvas); color: var(--fg); font: 14px/1.5 var(--font-sans); }
```

These are the values of `evo_agents/hub/server/static/plugin-kit/1/evo-ui.css` (built from `web/src/app/globals.css`);
read that file for more. A chart library takes its colours from these variables, read with `getComputedStyle`, and
redraws when the theme changes. Check both themes: no colour written for one theme only, text contrast at least 4.5:1.

## Fit 375 px

The frame is as wide as the message, down to 375 px on a phone. Design for that first: one column, wrap or scroll a
wide table inside its own box, charts that take the width (`width: 100%`, a `viewBox` for SVG), touch targets of 44 px.
No horizontal scroll of the page, and no fixed heights: call `resize` after a layout change.

## Keyboard and focus

Use real controls (`button`, `input`, `select`, `label for`), never a clickable `div`. Every control works with the
keyboard, in reading order, and shows its focus (`:focus-visible { outline: 2px solid var(--brand); outline-offset:
2px }`). Name what has no text (`aria-label`), give a chart a text summary or a table next to it, and do not rely on
colour alone.

## Numbers

- Check the bounds of every input: clamp or refuse a value out of range, a negative count, a zero divisor, `NaN`, and
  show why instead of `Infinity` or a blank.
- Say where each figure comes from. Mark every assumption on the page next to it ("assumed: 22 working days a month")
  and in TEXT, and keep given figures and assumed ones apart.
- Round for reading, keep units, and format with the locale `context` gives (`Intl.NumberFormat(locale)`).
- Test the formulas on two or three cases you can do by hand before you send the page.

## Before you send

- The page opens with no network but the hub's kit and the pinned CDN URLs, and with none at all in a restricted chat.
- Both themes, 375 px, keyboard only.
- TEXT answers the question without the frame.
