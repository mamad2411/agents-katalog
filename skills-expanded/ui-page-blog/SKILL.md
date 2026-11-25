---
name: ui-page-blog
description: "A blog or articles section: the index with titles, dates and excerpts, the article page set for reading (measure, type scale, headings with anchors, table of contents, code blocks, images with captions), author and dates, related posts, RSS, and article SEO. Read before building a blog, a changelog page or any long-form article page."
---

# A blog or articles section

The generated blog is a grid of cards with stock photos and "5 min read",
everything centred, grey 14px text running 120 characters wide, headings
barely larger than the text, code blocks with no language or copy button,
and no dates. People come to a blog to read, and come back when it is worth
it: set the page for reading, date everything, and make each post findable
and linkable. The measures are in `ui-layout`, the words in `writing`,
search engines in `frontend-seo`, documentation pages in `ui-page-docs`.

## 1. The index

```
│ [header]                                                                  │
│ Blog                                                       RSS · Tags ▾   │
│ Notes on how we build [product], and what we learn doing it.              │
│ ───────────────────────────────────────────────────────────────────────── │
│ 28 Sep 2026   Title of the newest post, as the link                       │
│               Two lines of excerpt in the post's own words, ending        │
│               at a sentence.                     Engineering · [Author]   │
│ ───────────────────────────────────────────────────────────────────────── │
│ 14 Sep 2026   Title of the post before it                                 │
│ ...                                                                       │
│ ‹ Newer posts                                            Older posts ›    │
```

- Newest first. Each entry: the title as the link and the largest text in
  the entry, the date in a `time` element, an excerpt of one or two lines
  (the post's own summary, not its first 160 characters cut mid-word), its
  tags, and the author when several people write.
- A list by default: titles scan faster than cards. A grid of cards only
  when every post has a real cover image of its own.
- A featured post only when one deserves it (a launch, a long essay), not
  the newest by default.
- 10 to 20 posts a page with real URLs (`/blog/page/2`); tag pages
  (`/blog/tag/engineering`) with their own titles; a search over the archive
  once it is large (Pagefind for a static site).
- A changelog uses the same index: entries by date and version, grouped as
  Added, Changed, Fixed (as in Keep a Changelog), an anchor per entry, and
  the same feed.

## 2. The article

```
│ [header]                                                                   │
│            Engineering · 28 Sep 2026 · Updated 30 Sep 2026                 │
│            The title in the display face,                                  │
│            over two lines at most                              (h1)        │
│            One sentence that says what the reader will get.                │
│            [photo] [Author name], [role]                                   │
│ ┌ On this page ┐  Body text at 65ch .................................       │
│ │ Why          │  A heading                                     #         │
│ │ How          │  Paragraphs, lists, a quote with a rule at its left.      │
│ │ Results      │  ┌ ts · retry.ts ───────────────────────── Copy ┐        │
│ └──────────────┘  │ code                                          │        │
│  sticky           └───────────────────────────────────────────────┘        │
│                 [ a figure wider than the text column             ]        │
│                   Caption, with its source.                                │
│            Next: [title] ›            Related: [title], [title]            │
```

## 3. Setting the text

- The text column 60 to 75ch (`max-width: 68ch`), left-aligned; body 17 to
  20px (18 is a good default) at line height 1.6, paragraphs 1em apart;
  17 to 18px on phones.
- A clear heading scale: `h1` 36 to 48px with `clamp()`, `h2` 24 to 30px,
  `h3` 20 to 22px, each with about twice as much space above as below;
  `text-wrap: balance` on headings and `text-wrap: pretty` on paragraphs
  where supported.
- Headings carry stable ids and anchor links (rehype-slug and
  rehype-autolink-headings in a markdown pipeline): a `#` shown on hover
  and focus, named "Link to this section"; `scroll-margin-top` clears the
  sticky header.
- A table of contents for posts with four or more `h2`s: sticky in a side
  column from about 1200px wide, the current section marked
  (`motion-reveal`, section 10); a `details` "On this page" above the text
  on narrower screens.
- Lists, blockquotes (a rule at the left and the source, no giant quote
  marks), footnotes with links back (remark-gfm), tables in a scroll
  container, `kbd` for keys, inline code on a quiet background.

## 4. Code blocks

- Highlighted at build time with Shiki (rehype-pretty-code or Expressive
  Code add titles, line highlights and copy buttons), with a theme per
  colour scheme: Shiki's dual themes (`themes: { light, dark }`) put the
  second theme's colours in CSS variables that switch with the page's
  theme (`ui-themes`).
- The language or file name shown; a Copy button that copies the code
  without line numbers or `$` prompts and says "Copied"; lines highlighted
  when the text points at them.
- 14 to 15px monospace, sideways scroll inside the block rather than
  wrapping, the full width of the text column; a very long block collapsed
  behind "Show all 80 lines".

## 5. Images and figures

- As wide as the text, or wider for screenshots and diagrams (a breakout
  column up to about 960 to 1100px), in `figure` with a `figcaption` saying
  what to look at and where it comes from.
- `width`, `height` and `srcset` on every image, lazy below the first
  screen, alt text that says what the image shows in this context
  (`ui-part-images`); screenshots open larger on click. Diagrams as SVG
  coloured from the tokens, video as in `ui-part-media`.

```css
.article {
  display: grid;
  grid-template-columns:
    [full-start] minmax(16px, 1fr)
    [wide-start] minmax(0, 12rem)
    [text-start] min(68ch, 100% - 32px) [text-end]
    minmax(0, 12rem) [wide-end]
    minmax(16px, 1fr) [full-end];
}
.article > * { grid-column: text; }
.article > .wide { grid-column: wide; }
.article > .full { grid-column: full; }
```

## 6. Authors and dates

- The author by name with a short, real bio, a photo only when one is
  given, and a link to their page; several authors in order.
- Published and updated dates in `time` elements; "Updated" only when the
  content changed in substance, with a line on what changed in technical
  posts.
- Reading time only when computed from the words (about 200 to 250 a
  minute) and only on long posts. No invented authors, dates or view
  counts.

## 7. After the article

- Next and previous posts, and 2 or 3 related ones chosen by tag or by
  hand.
- The ways to follow that exist: the feed, a newsletter if there is one.
- Plain share links rather than third-party widgets that load trackers;
  comments only when someone moderates them.

## 8. The feed

- An RSS or Atom feed (`/rss.xml` or `/feed.xml`) with absolute URLs,
  titles, dates and a summary or the full text, valid in the W3C Feed
  Validation Service.
- Announced in every page's head, and linked visibly from the index:

```html
<link rel="alternate" type="application/rss+xml" title="[Blog name]" href="/rss.xml">
```

## 9. SEO

- Static or server-rendered HTML with the full text in it.
- The title "[Post title] · [Blog name]" (50 to 60 characters), the
  description from the standfirst, one canonical URL per post, and the
  canonical on cross-posted copies pointing back to it.
- Open Graph: `og:type` set to `article`, `article:published_time`, and an
  `og:image` of 1200 by 630 per post (generated with the title when the
  post has no image of its own).
- `BlogPosting` (or `Article`) structured data with the headline, both
  dates, the author (name and url) and the image; BreadcrumbList; the
  sitemap with `lastmod`.

## 10. Themes, print, phone

- Dark theme: the code theme switches with it, screenshots get a hairline
  border, diagrams take the tokens (`ui-themes`).
- Print: hide the chrome, keep the text, show where links go:

```css
@media print {
  header, footer, nav, .toc, .share { display: none; }
  body { color: #000; background: #fff; }
  .article a[href^="http"]::after { content: " (" attr(href) ")"; }
  pre, figure { break-inside: avoid; }
}
```

- On a phone: side padding 16 to 20px, the table of contents as a
  `details` above the text, code blocks scrolling inside themselves,
  figures full width, and a back-to-top control on long posts
  (`ui-part-back-to-top`).

## Check it

- `preview` at 360, 768 and 1440px on the index and a long post: the text
  column stays 60 to 75ch, no code block or table widens the page, the
  table of contents sticks and marks the current section.
- Copy a heading's anchor link and open it: the heading lands below the
  sticky header.
- Copy a code block into a terminal: no prompts, no line numbers.
- Switch to the dark theme: code, diagrams and screenshots still read.
- The feed through the W3C validator, a post through the Rich Results Test,
  and `curl` on a post shows its full text in the HTML.
- Print preview of a long post.

## Avoid

Cards with stock photos for every post; centred body text; grey 14px text
or lines past 90 characters; headings barely larger than the text; code
without a language or a copy button; images without captions; missing or
invented dates and authors; reading time on a 300-word post; share widgets
that load trackers; a blog with no feed; posts rendered only in the browser
that search engines see empty.
