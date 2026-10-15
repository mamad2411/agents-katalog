---
name: content-authoring
description: Patterns for storing and editing long-form (and optionally localized) content with Tiptap (Medium-style WYSIWYG) on Prisma + MongoDB. Covers markdown vs editor-JSON vs MDX storage, locale strategy (per-row variant vs Translation table vs slug-keyed siblings), Tiptap setup, sanitization, and the authoring-UX checklist. Use when adding a CMS-like surface, a rich-text field, or blog/changelog/newsletter authoring on a Mongo stack.
---

# Content Authoring (Prisma + MongoDB)

Storing and editing long-form content with **Prisma + MongoDB** and **Tiptap** as the editor. Framework runtime is pluggable, TanStack Query / TanStack Start / Next.js / Vite all work. This skill is **Mongo-specific**; if your project is on a SQL database, use a different schema-layer skill.

> **Notation.** `<entity>` / `<storage>` / `<server>` are placeholders for the project's actual model name, blob-storage SDK, and server-entry-point convention. Substitute as appropriate.

> **Precedence.** These rules apply only where they don't contradict the project's own enforced rules, ESLint / Biome / `tsconfig` / `CLAUDE.md` / `AGENTS.md` / contributing guides. Project rules win; defer and note the deviation.

> **Database.** Mongo + Prisma with `relationMode = "prisma"`. All schema examples are Mongo-flavored.

---

## Decision tree

1. **Is the content short, repeated UI copy?** → `Translation` table (`key`, `locale`, `value`).
2. **Is it long-form, single-author, one variant per language?** → row-per-locale on the entity (`Article.locale + body`).
3. **Does it need rich layout, embeds, or custom blocks?** → store Tiptap JSON as the source of truth, optionally with a markdown projection.
4. **Plain prose, headings, lists, links, images?** → store markdown.
5. **Technical / docs content with embedded React components?** → store **MDX**.

When in doubt, prefer **markdown + locale-on-entity**. It's portable, diff-friendly, AI-friendly, and the easiest to migrate later.

---

## Schema patterns

### Locale strategy

| Pattern | When | Example |
|---|---|---|
| `Translation` table (`key`, `locale`, `value`) | UI strings, short labels, ToS snippets, repeated copy | `Translation { key, locale, value }` |
| Row-per-locale on entity | Long-form documents with one editable variant per language | `Newsletter { locale, body, ... }` |
| Sibling rows linked by `slug` | Same logical document, multiple locales, shared identity | `Article { slug, locale, body, @@unique([slug, locale]) }` |

**Avoid an inline `Json` map keyed by locale** (`{ es: "...", en: "..." }`) for long-form content, it breaks per-locale indexing, audit, partial publishing, and search. It's fine for short translatable fields like `title` on a non-content entity.

### Canonical content model (markdown source of truth)

```prisma
model Article {
  id          String   @id @default(auto()) @map("_id") @db.ObjectId
  slug        String
  locale      String   // e.g. "en", "es", "ja"
  title       String
  excerpt     String?
  body        String   // markdown, the source of truth
  bodyJson    Json?    // optional Tiptap-JSON cache, regenerated on save
  bodyHtml    String?  // optional pre-rendered sanitized HTML cache
  status      ContentStatus @default(draft)
  authorId    String   @db.ObjectId
  publishedAt DateTime?
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt

  author      User     @relation(fields: [authorId], references: [id])

  @@unique([slug, locale])
  @@index([locale, status, publishedAt])
  @@index([authorId])  // required: relationMode = "prisma" doesn't auto-index FKs on Mongo
}

enum ContentStatus {
  draft
  published
  archived
}
```

`body` is canonical. `bodyJson` is a write-time cache for the editor; `bodyHtml` is a render-time cache. **Never read from the caches as the source of truth**, always treat `body` as authoritative and regenerate caches on save.

### Mongo schema rules

These are mandatory under `relationMode = "prisma"`:

- **Primaries:** `@id @default(auto()) @map("_id") @db.ObjectId` on every model's `id` field.
- **Foreign keys:** `@db.ObjectId` on every FK scalar (`authorId`, `categoryId`, etc.).
- **FK indexes:** **Every relation field gets an explicit `@@index([fkField])`**, Prisma does not auto-create these on Mongo. Without them, every `findMany` filtered by an FK does a full collection scan.
- **Transactions:** Multi-document transactions require Mongo 4.0+ on a replica set or Atlas. Prisma's `$transaction([...])` support on Mongo is partial, verify against your deployment before relying. For the publish-as-fork flow (write a new `Article` row + flip the previous version's `status`), prefer single-document writes or idempotent retries when transactions aren't available.
- **BSON document size limit: 16 MB.** Plan to keep individual `Article` documents under ~10 MB. Long-form content with `body` + `bodyJson` + `bodyHtml` caches usually stays well under, but very long collaborative documents can push it. If you approach the limit, split caches into a separate collection (`ArticleCache { articleId, bodyHtml, bodyJson }`) or move them to Redis.
- **Large binary blobs (>1 MB)**, images, video, PDFs, go in object storage (S3 / R2 / GCS / Vercel Blob / Supabase Storage). Don't use GridFS for content-authoring images; the editor flow already wants signed-URL uploads.
- **Full-text search over `body`**, Mongo's `$text` indexes work but are coarse. For real search, use **Atlas Search** (if you're on Atlas) or a separate index (Meilisearch, Typesense, OpenSearch). The `zod-prisma-tanstack` skill shows raw `aggregateRaw` patterns for `$text` if you go that route.
- **Mongo doesn't enforce enums.** `ContentStatus` is stored as a string in BSON; Prisma enforces the union at the type layer. Don't write to the collection from outside Prisma assuming type safety.

### Editor-JSON-as-source variant

When custom blocks dominate the content (callouts, embeds, structured product pages), flip the canonical:

```prisma
model Page {
  id          String   @id @default(auto()) @map("_id") @db.ObjectId
  slug        String
  locale      String
  title       String
  content     Json     // Tiptap JSON, the source of truth
  contentHtml String?  // sanitized rendered HTML cache
  authorId    String   @db.ObjectId
  // ... rest as above

  @@unique([slug, locale])
  @@index([authorId])
}
```

Trade-off: harder to diff, harder to feed to AI, locked to Tiptap's schema. Worth it only when block structure is the point. **Watch the 16 MB document limit**, Tiptap JSON inflates faster than markdown for the same prose.

### MDX variant (technical / docs content)

When content needs to embed live React components (interactive examples, custom callouts), use **MDX** stored as a string. Render with `next-mdx-remote` (any framework), `@mdx-js/react`, or the project's own MDX loader. Keep the same `body: String` shape, just process it through MDX instead of plain markdown on render.

---

## Editor: Tiptap

**Use Tiptap v3.** ProseMirror-based, headless, MIT, integrates cleanly with React 19 and Tailwind. Gives Medium-style floating toolbars, slash commands, smart paste, IME, mobile selection, none of which you'll get right by hand.

**Skip a custom `contenteditable`.** Selections, undo/redo, IME, paste sanitization, mobile carets, accessibility take months to get wrong. Browsers do not give you a Medium-like experience for free; Medium itself uses ProseMirror, which is what Tiptap wraps.

Capabilities you get out of the box (or via official extensions):

- Bubble menu on selection, slash menu on `/`, keyboard shortcuts, smart paste from Word / Google Docs / Notion.
- Markdown round-trip via `tiptap-markdown`; structured JSON for custom blocks.
- Real-time collaboration via Y.js + **Hocuspocus** (Tiptap's official collab server).
- AI commands wired through Tiptap's transaction API, inline completions, selection rewrites, slash actions.

See [EDITORS.md](EDITORS.md) for setup, markdown round-tripping, image upload, sanitization, AI/collab integration, and the Medium-like UX checklist.

---

## Render path

- **Server-side render** (RSC, SSR, or build-time): parse markdown with a hardened pipeline (`remark` + `remark-gfm` + `rehype-sanitize` + `rehype-stringify`). Cache the resulting HTML on the row (`bodyHtml`) or in a layer like Redis keyed by `(id, locale, updatedAt)`.
- **Client-side render** (plain SPA / Vite, no SSR): use `react-markdown` with `rehype-sanitize`. Acceptable for low-volume admin / preview surfaces; pre-render for public-facing high-traffic content.
- **MDX render**: process server-side at build or request time; never compile MDX on the client unless you've pinned the input source.
- **Never trust HTML stored alongside.** Always sanitize at render time, schemas drift, libraries get CVEs, and "we already sanitized on write" becomes a footgun the moment the sanitization library updates.

---

## Authoring UX rules (Medium-like)

- **One column**, generous line-height, real typography, Tailwind `@tailwindcss/typography` `prose` class with a custom theme. Tune to match the published render so WYSIWYG actually means it.
- **Floating bubble toolbar** on selection; **slash menu** on `/` at line start.
- **Inline image upload** writes to the project's blob storage (S3, R2, GCS, Vercel Blob, Supabase Storage, etc.) via a server endpoint or signed-URL flow; insert as markdown `![alt](url)`.
- **Autosave on idle** (~1s after last keystroke). Show a quiet "Saved" indicator, never a modal.
- **Drafts** are `status = draft`; publishing flips `status` and stamps `publishedAt`. If history matters, fork a new row on each publish rather than editing in place, keep an `articleId` / `versionOf` relation.
- **Word count / read time** computed off the markdown string and shown in the chrome.
- **Keyboard shortcuts** match Medium / Notion conventions: `Cmd+B` bold, `Cmd+I` italic, `Cmd+K` link, `Cmd+Shift+K` remove link, `Cmd+Enter` publish (with confirm).

---

## Don't

- ❌ Store **HTML** as the source of truth, locks you out of AI processing, makes diffs unreadable, and turns sanitization into a permanent project.
- ❌ Use a **locale-keyed JSON blob** for long-form content (see schema patterns).
- ❌ Skip the Mongo `@@index([fkField])` on relation fields under `relationMode = "prisma"`, Prisma will not warn loudly, and every FK-filtered query becomes a full collection scan.
- ❌ Render markdown on the client when a server entry point can hand back sanitized HTML, wasted bytes, slower TTI.
- ❌ Hand-roll `contenteditable` to "save a dependency." You will spend more time on IME bugs than the dep would have cost over the project's lifetime.
- ❌ Mix HTML and markdown loads into the editor in the same flow, pick one and round-trip through it.
- ❌ Trust user-supplied URLs in `<a href>` / `<img src>` without sanitizing the protocol (`javascript:`, `data:`).
- ❌ Edit published rows in place when version history matters, fork a new row.
