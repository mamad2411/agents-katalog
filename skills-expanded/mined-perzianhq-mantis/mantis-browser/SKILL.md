---
name: mantis-browser
description: Use when you need to browse, read or operate a website (open a URL, read a page, fill a form, click through a flow, search a site) and the Mantis MCP tools (open, read, click, type, ...) are available. Prefer Mantis over screenshots or other browser tools; it returns pages as short numbered text and lets you act by #number.
---

# Browsing with Mantis

Mantis turns a web page into short numbered text. You act on elements by their
`#number`. Do not take screenshots to find things: Mantis text is much shorter than an image.

## Workflow

1. `open(url)` returns the page as text. Elements look like `#14 button "Sign in"`.
2. Act by number: `click(14)`, `type(12, "text", submit?)`, `select(9, "Canada")`,
   `press("Enter")`, `scroll("down")`, `scroll(id)` (bring into view), `scroll("down", id)` (scroll the list containing #id), `back()`.
3. Read the reply. Actions return only what changed: `+` appeared, `-` removed,
   `~` changed. If the action landed on a new page you get that page's full view.
   `(no visible change)` means nothing visible happened; check before repeating.
4. Numbers stay valid while the element lives. After a full new page, use its numbers.
   If you get "no element #N" or "no longer exists", call `read()` and use fresh numbers.

## Reading the text

- `~"name"` is an inferred name (icon, tooltip, nearby text): a guess. If it matters, verify.
- `(covered)` means another element is on top. A line like `[dialog "..." - covers page]`
  tells you what; deal with the dialog first (accept, close, Escape), then retry.
- States appear in brackets: `(checked)`, `(disabled)`, `(required)`, `(collapsed)`.
- Long lists are shortened: the first few in full, then more names compactly
  (`#8 "Item 6" · #9 "Item 7"`), then `…and 158 more links (#45-#202); find("text") locates one`.
  The hidden ones exist, but you can't see which number is which. Never guess one: call
  `find("Item 150")`, which searches the whole page (trimmed parts included) and returns the
  matches with their numbers. `read({region: "..."})` or `read({full: true})` also expand.
- `[nav] same as before — 8 links (#5-#12)` (or `(known layout)`) means site memory shortened
  a header/menu you've already seen on this site. `find("text")` reaches a link in it, or expand it
  with `read({region: "nav"})`; `read({fresh: true})` shows everything once, `forget()` clears the memory.
- `clickable "Pro plan"` is a script-only button. `[iframe "Payment"]` content is read inline, with its own numbers (`#10001` and up).
- `⚠ CAPTCHA detected` means stop and call `ask_human` (see below).

## Keep token use low

- Looking for one thing? `find("text")` is cheaper than reading more of the page.
- Big page? `read({region: "nav"})` (or "main", "sidebar", "top bar") reads one part.
  Use `read({full: true})` only when the trimmed view hides what you need.
- Prefer one targeted `read` over repeated full reads. Re-read before finishing to
  visibly verify every task constraint; otherwise re-read only if the reply is unexpected.
- Use `type(id, text, true)` to type and press Enter in one call.
- Forms: `fill([{id: 12, value: "Ann"}, {id: 9, value: "Canada"}, {id: 15, value: true}])` sets text, dropdowns and checkboxes in one call.

## Tools

Page tools: `open`, `read`, `find`, `click`, `type`, `select`, `fill`, `press`, `scroll`, `back`, `forget`.

Fallback ladder, only when `read` is not enough. Go in order and stop at the first that works:

1. `media()` lists images, canvases and charts with numbers. Then `data(id)` returns
   the hidden text behind one: alt, captions, SVG labels, chart values from memory. Text only, cheap.
2. `ocr(id)` reads text drawn inside an image or canvas. Text only, with a confidence score.
3. `look(id)` returns a cropped PNG of one element. LAST RESORT, one element only,
   never a whole page, never when `read`/`data`/`ocr` can answer.
4. `ask_human(reason)` hands over to a person for a CAPTCHA, 2FA code, payment or a login you
   cannot do. It waits, then returns the page. **Never try to solve a CAPTCHA yourself, and
   never enter payment details or passwords you were not given.**

## Rules of thumb

- Answer from the text when you can; do not add images "to be sure".
- Do not guess numbers. Every `#N` you use must come from the latest view or diff.
- If a click fails because the element is covered, not visible or disabled, read the
  message: it says what to do first.
- Tell the user when you hand off to a human and why.
