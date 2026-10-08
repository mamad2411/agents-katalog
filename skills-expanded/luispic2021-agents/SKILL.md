# AGENTS.md

Guidance for AI coding agents (and future-you) working in this repo.

## What this is

A static Jekyll site for luispe.me, deployed via classic GitHub Pages (no
`.github/workflows` — GitHub builds the `github-pages` gem branch directly on
push to the default branch). See `README.md` for project structure and local
setup.

## Always build before pushing

GitHub Pages builds this site with Jekyll on every push to the default
branch. A page with broken front matter, a bad Liquid tag, or an include that
doesn't exist can silently degrade instead of failing loudly — the build
often "succeeds" while quietly skipping the broken page's layout. **Never
push a change to a `.html`/`.md` page, a layout, or an include without
running a full local build first and reading the output.**

```bash
gem install bundler   # first time only
bundle install
rm -rf _site .jekyll-cache .sass-cache
bundle exec jekyll build --trace
```

Treat any of the following in the build output as a blocking failure, even
if the command exits 0:

- `YAML Exception reading ...` — front matter failed to parse. Jekyll then
  serves the file as a static file with **no layout applied**, which means
  no `<head>`, no stylesheet link, no header/footer include. This is exactly
  what broke the homepage's CSS: `assets/css/style.scss` compiled fine, but
  `index.html`'s front matter didn't parse, so `layout: default` (and its
  `<link rel="stylesheet" href="/assets/css/style.css">`) never got applied.
- `Liquid Warning` / `Liquid Exception`
- `Could not find document` or `Include ... not found`

Then spot-check the generated output before pushing:

```bash
grep -n '<link rel="stylesheet"' _site/index.html   # homepage still styled?
head -c 200 _site/assets/css/style.css               # CSS actually compiled?
```

## YAML front matter rules (the bug that prompted this file)

Front matter is parsed as YAML. Common ways to break it silently:

- **Block scalars (`>-`, `|-`, `>`, `|`) must have their continuation lines
  indented** relative to the key. This is invalid and fails to parse:

  ```yaml
  description: >-
  This line is not indented, so YAML sees a new top-level key and fails.
  ```

  This is valid:

  ```yaml
  description: >-
    This line is indented under the key.
    Continuation lines fold into one string.
  ```

- Don't let colons, unescaped `#`, or leading `- ` appear at the start of an
  unquoted scalar value — quote the string if it needs any of those.
- Keep front matter delimited by exactly `---` on its own line, at the very
  top of the file (line 1, no leading blank line or BOM).

A failed front matter parse does not always throw a build error you'll
notice in a quick skim — always grep the build log for `YAML Exception` per
above, and preview the rendered page.

## Structure

- `index.html` — homepage (front matter + Liquid/HTML body, `layout: default`)
- `cv.md` — `/cv/`, Markdown with embedded HTML sections
- `posts.html` — `/posts/`, post index
- `_posts/` — dated posts, `YYYY-MM-DD-title.md`, `layout: post`
- `_layouts/default.html` — the only layout that emits `<head>`; `page.html`
  and `post.html` both declare `layout: default` in their own front matter
- `_includes/header.html`, `_includes/footer.html`
- `assets/css/style.scss` — hand-written design system (not the `minima`
  theme's default styles); compiles to `assets/css/style.css`
- `assets/js/site.js` — mobile nav toggle only

## Conventions

- New pages need `layout: default` (directly, or via `page`/`post`) or they
  render without the site header/footer/stylesheet.
- New posts: copy an existing `_posts/*.md` front matter block rather than
  writing one from scratch, to avoid YAML mistakes.
- `_config.yml` changes require restarting `jekyll serve` — it's not
  hot-reloaded.
