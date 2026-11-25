---
name: telegram-output
description: How to shape replies for Telegram: Markdown that renders natively, files for long output, images inline.
---
# Writing for Telegram

- Replies are rendered by Telegram's rich Markdown: `# headings`, `**bold**`, `*italic*`,
  `` `code` ``, fenced code blocks with a language, bullet and numbered lists, task lists,
  `| tables |`, `> quotes`, `---` dividers, and collapsible `<details><summary>…</summary>…</details>`
  blocks. Use them; do not draw tables with spaces or write pseudo-headings in caps.
- Keep a reply to a few short paragraphs or a list. Anything longer than a screen (logs, full
  listings, generated code, long reports) goes to a file in the workspace, then `SendFile(path, caption)`.
  `.md` files render well as documents; images (png, jpg) render inline.
- Fold detail the operator may not need into a `<details>` block instead of dropping it.
- Progress is shown automatically in the status message; do not narrate every step.
- End with the outcome and, if relevant, one line about what you would do next.
