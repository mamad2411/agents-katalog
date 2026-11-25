---
name: llms-txt
description: Write and validate an llms.txt file — the /llms.txt convention that gives AI assistants a clean, curated map of a site instead of leaving them to guess from HTML. Covers the required format, what belongs in it and what does not, the optional llms-full.txt companion, and where to put both. Use when the user says "llms.txt", "llms-full.txt", "AI crawler file", "help AI understand my site", "make my site readable to ChatGPT", or is preparing a site to be cited by AI assistants.
---

# llms.txt

A single Markdown file at `/llms.txt` that tells an AI assistant what a site is and where the
good pages are. It exists because HTML is noisy — navigation, cookie banners, footers,
scripts — and a model reading a page has to guess what matters. `llms.txt` removes the guessing.

It is a convention, not a standard. No crawler is required to read it. Write one anyway: it
costs ten minutes, it is read by a growing number of assistants and tools, and the act of
writing it forces you to state plainly what the site is for.

## The format

Strict Markdown, in this order. The structure is the contract — a parser looks for exactly this
shape.

```markdown
# Site or business name

> One sentence saying what this is. Concrete. No marketing adjectives.

Optional free prose. A short paragraph or two of context that does not fit a link —
what the business does, who it serves, where it operates, what makes it different.
Keep it factual.

## Section name

- [Page title](https://example.com/page): what a reader gets from this page
- [Another page](https://example.com/other): one clause, not a sentence

## Optional

- [Lower-priority page](https://example.com/archive): things a model can skip if short on space
```

Rules that actually matter:

1. **One `# H1`**, the name. First line of the file.
2. **A `>` blockquote directly after it**, one sentence. This is the line most likely to be
   quoted back verbatim, so write it like a caption, not a slogan.
3. **`##` sections** group the links. Name them for what they are — `Services`, `Case studies`,
   `Docs`, `About` — not `Resources` or `More`.
4. **Every list item is a link followed by `:` and a description.** The description is the
   point. `[Pricing](/pricing): three plans, from €19/month, no setup fee` is useful.
   `[Pricing](/pricing): our pricing page` is noise.
5. **Absolute URLs.** A model may read the file with no knowledge of the origin.
6. **A section literally named `## Optional`** is the one piece of magic: anything under it is
   explicitly marked as skippable when context is tight. Use it. Do not use it for anything you
   actually want read.

## What goes in

Only pages a person would be glad to land on. A good `llms.txt` for a small site is ten links.
For a large one it is thirty, not three hundred.

Include: the home page, what you sell or do, pricing, about, contact, the three or four best
pieces of writing, documentation entry points, anything with real specifics in it.

Leave out: tag and category archives, pagination, login and account pages, checkout, thank-you
pages, anything `noindex`, anything thin, and anything duplicated across URLs.

## The one-page case

A single landing page still gets an `llms.txt`, and it is mostly prose rather than links.
The blockquote and the paragraph under it carry everything:

```markdown
# Panadería Aurora

> A wood-fired sourdough bakery in Malasaña, Madrid, open Tuesday to Sunday from 8am.

Aurora bakes four breads daily — country sourdough, seeded rye, olive fougasse and a
Saturday-only brioche — in a wood oven installed in 1974. Everything is sold from the
counter at Calle del Pez 14; there is no delivery and no online ordering. Wholesale
enquiries from restaurants are taken by phone.

## Pages

- [Home](https://panaderiaaurora.es/): breads, hours, address, and how to order wholesale

## Optional

- [Instagram](https://instagram.com/panaderiaaurora): daily bake announcements
```

That is a complete, correct file. Do not pad it.

## llms-full.txt

The optional companion at `/llms-full.txt` holds the actual **content** — the full text of the
important pages, concatenated as clean Markdown, so an assistant can read the substance without
fetching anything.

Write one when the site is documentation, a knowledge base, or anything where the value is in
the text. Skip it for a one-page landing site: `llms.txt` already contains everything.

Keep it plain Markdown: `# Page title`, then the page's prose. No navigation, no HTML, no
scripts, no repeated header and footer. Strip everything a reader would skip.

## Where the files go

Both live at the domain root, served as `text/plain` or `text/markdown`:

| Framework | Location |
|---|---|
| Next.js (App Router) | `public/llms.txt` |
| Astro, Vite, SvelteKit | `public/llms.txt` |
| Hugo, Jekyll, Eleventy | `static/llms.txt` |
| Plain static site | next to `index.html` |

Verify after deploying: `https://yourdomain.com/llms.txt` must return the raw file, not an HTML
404 page.

Then point `robots.txt` at it, so a crawler that does not know the convention still finds it:

```
User-agent: *
Allow: /

User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

Sitemap: https://yourdomain.com/sitemap.xml
```

`llms.txt` is not a `robots.txt` directive, so it has no line of its own there. Linking it from
the home page `<head>` is harmless and occasionally helps:

```html
<link rel="alternate" type="text/markdown" href="/llms.txt" title="llms.txt">
```

## Validating one

Read it back and check:

- [ ] Exactly one `#` heading, and it is the first line
- [ ] A `>` blockquote immediately after it, one sentence, factual
- [ ] Every `##` section has at least one item
- [ ] Every list item is `- [text](absolute-url): description`
- [ ] No relative URLs
- [ ] No link to a page that 404s, redirects, or is `noindex`
- [ ] Every description says something specific — no "our services page"
- [ ] Under about 100 links; if longer, most of them belong under `## Optional` or nowhere
- [ ] Nothing in it is untrue. A model will repeat this verbatim

The last one is the important one. `llms.txt` is the most quotable file on a site — everything
in it is written in a model's preferred format, pre-chewed and unambiguous. An invented claim
here does not get buried the way it would in a paragraph of HTML. It gets repeated.

## Writing the blockquote

It is one sentence and it does most of the work. Three failure modes:

| Bad | Why | Better |
|---|---|---|
| "Innovative solutions for modern businesses." | Says nothing. Fits any company. | "Payroll software for Spanish companies with 5–50 employees." |
| "The best bakery in Madrid." | Unverifiable claim, reads as marketing, gets discounted. | "A wood-fired sourdough bakery in Malasaña, Madrid." |
| "We are a full-service creative agency offering branding, web design, motion graphics, packaging and strategy for clients across sectors." | Too long, no shape, nothing to lift. | "A three-person branding studio in Lisbon working mostly with restaurants and hotels." |

Name the thing, the who, and the where. Numbers and place names survive summarisation; adjectives
do not.
