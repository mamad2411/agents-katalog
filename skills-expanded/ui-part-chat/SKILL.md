---
name: ui-part-chat
description: "Chat and assistant interfaces: the message thread and its grouping, the composer, streaming answers with a stop button, rendering markdown and code safely, scrolling that follows unless the reader scrolled up, per-message errors and retry, attachments, and accessibility for new messages. Read before building a chat, messaging or AI assistant screen."
---

# Chat and assistant interfaces

The generated chat wraps every message in a coloured bubble, yanks the view
to the bottom while you read something above, re-renders the whole answer on
every token, shows a typing indicator that is only a timer, loses the
message when sending fails, and makes a screen reader read the answer one
word at a time. This skill covers the thread, the composer, streaming, safe
rendering, scrolling and failure, for people talking to people and for
people asking an assistant. Rendering safety is in `frontend-security`,
loading and real-time data in `frontend-data`.

## 1. Two kinds of thread

| | Messaging (people) | Assistant (AI) |
|---|---|---|
| Layout | Bubbles: mine at the right, theirs at the left | One reading column of 60 to 75ch; the user's turn as a quiet block at the right, the answer as plain text across the column |
| Width | Bubbles up to about 70% of the thread (85% on phones) | The column; code and tables may use all of it |
| Identity | Avatar and name on the first message of a group from others | A small label for the assistant, not an avatar per message |
| Status | Sending, sent, read (only with real receipts), not sent | Thinking, streaming, stopped, failed |

Long answers in bubbles are hard to read: markdown, code and tables need the
full column.

## 2. The thread

- Group consecutive messages from one author within about 5 minutes: author
  and time on the first, 2 to 4px between messages in a group, 16 to 24px
  between groups.
- Day separators ("Today", "Yesterday", "Mon 28 Sep") and a "New" line above
  the first unread message; the exact time on hover and focus
  (`ui-part-dates`).
- Status in words or a labelled icon under the last message of a group:
  "Sending", "Sent", "Read" (only when receipts exist), "Not sent. Retry".
- Each message an `article` (or list item) named by its author and time;
  links, images and files inside are real links.
- Long words and URLs wrap (`overflow-wrap: anywhere`) and never widen the
  thread.

## 3. The composer

- A `textarea` with a name (a visible label or `aria-label`: "Message Dina",
  "Ask about your invoices"), 16px text so iOS does not zoom, one line tall
  at first, growing with the text to about 8 lines or 40% of the screen,
  then scrolling. `field-sizing: content` does it where supported, a few
  lines of script elsewhere.
- Enter sends and Shift+Enter adds a line on desktop; on touch screens Enter
  adds a line and the button sends. Never send while an input method is
  composing (Chinese, Japanese, Korean): check `isComposing`.

  ```ts
  function onKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key !== "Enter" || e.shiftKey || e.nativeEvent.isComposing) return;
    if (matchMedia("(pointer: coarse)").matches) return; // touch: a new line
    e.preventDefault();
    if (text.trim()) send();
  }
  ```

- Send is an icon button named "Send", 36 to 44px, disabled while the text
  is empty or only spaces. While an answer streams it becomes Stop, in the
  same place.
- Attachments: a named "Attach" button, paste and drop for images
  (`ui-part-uploads`), files as removable chips above the text with their
  progress; sending waits for them.
- A character limit shown as a counter only from about 80% of it, before
  anything is cut.
- A draft per conversation, kept when switching threads and after a reload
  (`sessionStorage` keyed by thread).
- The composer sticks to the bottom; the thread keeps enough padding that
  its last message never hides under it.

## 4. Streaming answers

- The user's message appears at once, then a thinking indicator until the
  first token, then the answer growing in place.
- The indicator is honest: dots or "Thinking" while waiting; named steps
  ("Searching invoices", "Reading contract.pdf") only when the backend
  reports them. No fake typing delay, no invented progress.
- Render in batches (once per animation frame, or every 30 to 50ms), not
  per token, with a markdown renderer that copes with unfinished syntax:
  an open code fence renders as a code block that grows. Streamdown is a
  react-markdown replacement built for this.
- A Stop button visible for the whole stream: it aborts the request
  (`AbortController`), keeps the partial answer marked "Stopped", and offers
  Regenerate.
- The Vercel AI SDK's `useChat` handles the stream, stop and status in
  React; with your own backend, server-sent events or a streamed `fetch`
  body read through its `ReadableStream`.
- Highlight a code block once it closes, not again on every token.

## 5. Markdown and code, rendered safely

- Model output and other people's messages are untrusted. Render markdown
  to elements with react-markdown (raw HTML off, its default) and
  remark-gfm for tables and task lists; if HTML must pass, rehype-sanitize
  after it. Never `dangerouslySetInnerHTML`, `v-html` or `{@html}` on it
  (`frontend-security`).
- Links only for http, https and mailto, with
  `rel="noopener noreferrer nofollow ugc"`.
- Images in model output are not loaded from any address: an injected
  prompt can leak data through an image URL. Allow your own domains (and a
  CSP `img-src` that says so), or show the rest as links.
- Code blocks name the language and have a Copy button ("Copy code", then
  "Copied" for 2 seconds, announced); Shiki for highlighting; sideways
  scroll inside the block, never the page.
- Tables in a scroll container; math (KaTeX) only when the product needs it.

## 6. Scrolling

- Follow the bottom while content arrives only if the reader is there
  (within about 80px). Once they scroll up to read, stop following and show
  a "Jump to latest" pill centred above the composer (with the number of
  new messages when messaging); it scrolls down when pressed and goes away
  at the bottom.

  ```ts
  const atBottom = (el: HTMLElement) => el.scrollHeight - el.scrollTop - el.clientHeight < 80;
  // before adding content: const follow = atBottom(thread)
  // after it renders:      if (follow) thread.scrollTop = thread.scrollHeight
  ```

- Opening a thread: at the first unread message in messaging, at the bottom
  in an assistant.
- Older messages load at the top (an IntersectionObserver on a sentinel,
  with a "Load earlier messages" button as the fallback) without moving what
  the reader sees: CSS scroll anchoring (`overflow-anchor`) keeps the place
  where the browser supports it; otherwise add the height difference to
  `scrollTop` after inserting.
- Very long threads are virtualised (TanStack Virtual, react-virtuoso);
  `use-stick-to-bottom` does the following logic in React.
- No smooth scrolling of long jumps under reduced motion.

## 7. Failure and retry

- A message that failed stays in the thread, marked "Not sent", with Retry
  and Delete. The composer never clears the text of a message that did not
  go.
- An answer cut off by the network keeps what arrived, says "The answer was
  interrupted", and offers Retry.
- Rate limits say when to try again (from `Retry-After`); provider errors in
  plain words, never raw JSON (`frontend-errors`).
- After a dropped connection: reconnect with backoff, fetch what was
  missed, and never show a message twice (ids made by the client,
  duplicates dropped by the server).
- Edited messages say "Edited"; in messaging a deleted one leaves "Message
  deleted" so the replies still make sense.

## 8. The empty thread, and assistant specifics

- An empty assistant says what it can do with this product's data in one
  line, and offers 3 or 4 real example prompts as buttons that fill the
  composer ("Which invoices are overdue this month?"). A new conversation
  in messaging names the person. Not "How can I help you today?" over
  sparkles (`ui-part-empty-states`).
- Say once, near the composer, that answers are generated and can be wrong;
  not on every message.
- Sources as real links when the answer comes from retrieval; Copy and
  Regenerate per answer; feedback buttons only when their result is stored
  and someone reads it.
- Anything the assistant proposes that changes data (send, delete, pay)
  asks the user to confirm, showing what will happen.

## 9. Accessibility

- The thread is `role="log"` (polite by default), so new messages from
  others are announced. A streaming answer is not read token by token: mark
  it `aria-busy="true"` while it streams, then announce "Answer ready"
  through a separate status region.
- Each message reachable as an `article` with its accessible name, so a
  screen reader can move from message to message.
- Focus stays in the composer after sending; Stop is reachable by Tab, and
  Escape in the composer stops the stream.
- Shortcuts you add are listed in a help dialog and never take keys the
  browser or the screen reader needs.

## 10. On a phone, themes, motion

- The thread fills the screen (`100dvh`); the composer sits above the
  on-screen keyboard with `env(safe-area-inset-bottom)` padding.
  `interactive-widget=resizes-content` in the viewport meta helps in
  Chromium; test iOS Safari on a real phone, it resizes differently.
- Actions hidden behind a long press (copy, reply, retry) also have a
  visible button.
- New messages fade and rise 8px over 150 to 200ms, nothing animates per
  token, and a blinking caret stops under reduced motion
  (`motion-interface`); bubbles and code themes from tokens in both themes
  (`ui-themes`).

## Check it

- Send while offline, then reconnect: the message is kept and Retry works.
- Stream a long answer and scroll up while it streams: the view stays put;
  Jump to latest works; Stop keeps the partial answer.
- Feed it markdown with `<script>`, a `javascript:` link and an image from
  an unknown domain: nothing runs or loads.
- Type Japanese with an input method and press Enter to confirm a word:
  nothing is sent.
- VoiceOver or NVDA: a new message is read once; a streamed answer is
  announced when it completes.
- `preview` at 360px, and a real phone with the keyboard open: the composer
  stays in view.

## Avoid

Bubbles for long assistant answers; scroll that jumps while someone reads;
a Stop button that is hidden or missing; a partial answer thrown away;
model output rendered as raw HTML; remote images loaded from model output;
a typing indicator on a timer; errors that clear the composer; Enter sending
during composition; every token announced; feedback buttons wired to
nothing; a greeting over sparkles as the empty state.
