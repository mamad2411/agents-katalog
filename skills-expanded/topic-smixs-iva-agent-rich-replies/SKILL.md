---
name: rich-replies
description: "Shape a reply for Telegram: headings, tables, folds, footnotes, formulas, pictures, slideshows, maps, and buttons (choice, link, copy, mini app) inside the text. Load before a structured answer, a comparison, a report in chat, or whenever you offer the user a choice or a link."
---

# Rich replies — what Telegram can render in your answer

Your reply is markdown. The host sends it as a Telegram **rich message** as soon
as it contains something ordinary messages cannot show (a table, a fold, a
footnote, a formula, a picture, any `<tg-*>` tag, a button). Otherwise it goes
as a plain formatted message. You never call anything: you write the markup and
the transport is chosen for you. Every construct below renders natively on a
Telegram client from summer 2026 or later.

This skill is about the reply in the **current chat**. A post to another chat
(digest, channel) with local pictures is `rich-post`.

## When to reach for rich constructs

Use them when they carry meaning the reader would otherwise have to dig out:

| Reader's need | Use | Don't |
|---|---|---|
| Compare 3+ things by 2+ attributes | table | a table for two numbers |
| Long answer with sections | `##` headings | headings in a three-line reply |
| Optional depth (logs, raw data, method) | `<details>` fold | hide the answer itself |
| Source or aside | footnote `[^1]` | footnotes instead of a link |
| Formula | `$x^2$`, `$$…$$` | LaTeX for "2 + 2" |
| Step status, checklist | `- [ ]` / `- [x]` | task list for prose |
| Picture or several by public URL | image line, `<tg-collage>`, `<tg-slideshow>` | local file paths (use `rich-post`) |
| Place | `<tg-map>` | a map for a city name |
| A moment in the reader's time zone | `<tg-time>` | for "tomorrow" in prose |
| Next step, choice, link, copyable value | **buttons** (below) | buttons on every reply |

Short conversational answers stay plain text. Rich formatting is for structure,
not decoration: one heading level per answer, one table per comparison, one row
of buttons per decision.

## Text and blocks

````
**bold**  *italic*  ~~strike~~  `code`  ==marked==  ||spoiler||  <u>underline</u>
<sub>x</sub> <sup>2</sup>   $x^2 + y^2$ (inline formula)
[link](https://example.com)  [mail](mailto:a@b.c)  [user](tg://user?id=123)

## Heading (levels # … ######)
Paragraphs separated by a blank line.

- bullet     1. numbered     - [ ] task     - [x] done

> quote
> continues

<aside>Pull quote<cite>Author</cite></aside>

| Feature | Value |
|:--------|------:|
| left    | right |

<table bordered striped compact> … </table>   (HTML form when you need borders)

Text with a note[^1].
[^1]: The note itself.

$$E = mc^2$$                       (block formula)

<details open><summary>Title **bold**</summary>
Anything markdown, shown collapsed unless `open`.
</details>

![](https://host/photo.jpg "caption")     picture, video, gif, audio by public URL
<tg-collage>
![](https://host/1.jpg)
![](https://host/2.jpg)
</tg-collage>                              grid of media
<tg-slideshow> … </tg-slideshow>           swipeable media

<tg-map lat="41.31" long="69.28" zoom="13"/>
<tg-time unix="1789300000" format="wDT">tomorrow 22:45</tg-time>   (formats: t, r, wDT)
<tg-emoji emoji-id="5368324170671202286">👍</tg-emoji>
````

Rules: table cells hold inline formatting only; formulas are raw LaTeX; media
needs an `https://` URL the Telegram server can fetch; markdown is not parsed
inside block HTML tags except `<details>`, `<tg-collage>`, `<tg-slideshow>`.
Escape `*`, `_`, `#`, `|`, `<` in user data you quote (file names, keys, paths).

## Buttons — a full-width row, with the explanation right under it

Put every button in its own `<tg-button-row>` block and write what it does on
the next line. Do not place a button inside a sentence (`RichTextButton`): Android
clients of summer 2026 draw the label outside the pill. Several equivalent
one-word choices (yes/no) share one row.

````
Напоминание на 14:30 поставил.

<tg-button-row><tg-button type="callback_data" data="Отложи на час">На час</tg-button></tg-button-row>
Напомню в 15:30.

<tg-button-row><tg-button type="callback_data" style="danger" data="Отмени напоминание">Отменить</tg-button></tg-button-row>
Сниму его.

<tg-button-row><tg-button type="url" url="https://iva-agent.com/docs">Документация</tg-button></tg-button-row>
Как настроить обзор дня.

<tg-button-row><tg-button type="copy_text" text="ssh c1">Скопировать</tg-button></tg-button-row>
Команда для входа на сервер.

<tg-button-row><tg-button type="callback_data" data="Да">Да</tg-button><tg-button type="callback_data" data="Нет">Нет</tg-button></tg-button-row>
````

Button types:

| `type` | What happens | Attributes |
|---|---|---|
| `callback_data` | the tap becomes **the user's next message**, text = `data` | `data` **≤ 64 bytes = at most 30 Cyrillic letters** (Cyrillic is 2 bytes each); longer → Telegram rejects the whole message and the buttons are lost |
| `url` | opens a link; the nice way to give a link instead of a bare URL | `url` |
| `copy_text` | copies a value to the clipboard (commands, ids, keys you were asked to show) | `text` |
| `web_app` | opens a Mini App; private chats only | `url` |
| `switch_inline_query` / `…_current_chat` | inserts `@bot query` into the input field | `query` |
| `disabled` | a greyed-out label, e.g. a step not yet available | — |

Styles: `style="success"` for confirm/enable/apply, `style="danger"` for
cancel/delete/turn off, `style="link"` for a quiet secondary action, none for
navigation. `<tg-button-row align="left|center|right">` holds up to 8 buttons.

### What the tap does (callback_data)

`data` **is the user's reply**: they tap, and exactly that text arrives as their
message in the same session. So write `data` in the user's words (`Отложи на
час`, `Покажи список`, `Да`), never codes (`confirm_1`, `opt:b`); make it
self-sufficient — next turn you see only that text; **count the bytes: 64 bytes
is 30 Cyrillic or 60 Latin characters**, so `data="Про таймер"` is fine and
`data="Расскажи подробнее про напоминания Ивы"` (70 bytes) kills every button in
the message — put the long wording in the paragraph next to the button, not in
`data`; never start it with `iva_` or `eve` (reserved for the host's own buttons —
such a tap never reaches you). 1-4 buttons per reply; more than that is a menu, and the
menu is `/menu`.

Private chats only: in a group a tap is not an address to the bot (only a
mention, a command or a reply is), so don't put `callback_data` buttons in group
replies. `url` and `copy_text` buttons work anywhere.

## Limits and gotchas

- 32768 characters, 500 blocks, 16 nesting levels, 50 media, 20 table columns.
- Old Telegram clients (before August 2026) don't show buttons; everything else
  degrades to text.
- The operator can set `TELEGRAM_RICH_REPLIES=never` (`/menu` → Rich replies):
  then tables, folds and pictures go as plain formatted text — but a reply with
  a button is still sent rich, buttons have no other form.
- Don't repeat the same reply as `iva post`: the rich reply already rendered.
