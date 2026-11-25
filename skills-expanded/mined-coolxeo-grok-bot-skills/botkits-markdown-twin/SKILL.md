---
name: botkits-markdown-twin
description: >-
  Use this when adding a clean markdown twin for one HTML page: a .md
  copy at the same path, a rel=alternate type=text/markdown link, and
  one line for it in /llms.txt.
---
# Markdown twin

For one HTML page, publish a clean markdown copy that an agent can read instead of scraping the rendered page. The twin must carry the same facts as the HTML. Do not cloak.

## Three steps

1. Write a clean `.md` copy at the same path as the page, using one of the forms from the [llms.txt v2 spec](https://llmstxt.org/): append `.md` (`page.html.md`) or replace the extension (`page.md`). For a URL with no filename, use `index.html.md` or `index.md`.
2. Advertise the twin from the HTML page:

   ```html
   <link rel="alternate" type="text/markdown" href="/docs/install.md">
   ```

3. Add one line for that twin in `/llms.txt` (create the file if the site does not have one yet), in the spec's file-list form: a markdown link, optionally a colon, and a short note.

Do this for the one page you were asked to cover. Do not invent a site-wide crawl, a Worker router, or content negotiation unless that work is already in scope.

## Example

HTML page at `/docs/install/` (or `/docs/install.html`). Twin at `/docs/install.md` (or `/docs/install/index.md`).

```html
<!doctype html>
<html lang="en">
  <head>
    <link rel="alternate" type="text/markdown" href="/docs/install.md">
    <title>Install</title>
  </head>
  <body>
    <h1>Install</h1>
    <p>Run <code>npm install example</code>, then start the app with <code>npm start</code>.</p>
  </body>
</html>
```

`/docs/install.md`:

```markdown
# Install

Run `npm install example`, then start the app with `npm start`.
```

One new line in `/llms.txt`:

```markdown
# Example

> Product docs for agents.

## Docs

- [Install](/docs/install.md): How to install the product
```

The markdown has the same facts as the HTML, without navigation or other chrome. Point the `llms.txt` link at the twin, not the HTML page.

## Inspired by

Inspired by [Jeremy Howard's /llms.txt v2 proposal](https://llmstxt.org/) (clean markdown at the same URL with `.md` or `index.md`, and `rel="alternate" type="text/markdown"`). The spec defines the file forms, the link relation, and the `/llms.txt` format, but it is not a one-page recipe that does all three together. This skill adds that per-page sequence and a tiny worked example.
