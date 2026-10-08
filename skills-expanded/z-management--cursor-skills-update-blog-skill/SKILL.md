---
name: update-blog
description: Update or create a Z-Management blog post in Orbitype CMS from pasted article text and a featured image. Finds an existing post by German title (or id) and updates it; inserts if missing. Use when the user runs /update-blog, asks to update/refresh blog content, or provides blog copy plus a hero image.
disable-model-invocation: true
---

# Update Blog Post

Upsert a bilingual (de + en) blog post into the Orbitype `posts` table. Prefer
**update** when a matching post already exists (seeded or draft); **create** only
when none is found.

Rendered by `pages/posts/[id]/[[slug]].vue` + `_BlogArticle.vue`, listed on
`pages/posts/index.vue`.

## Minimum input

1. **Blog text** (required) — pasted copy or file path. First line is usually the
   **title**; the rest is the article body.
2. **Featured image** (required) — file path in the repo, new file to add under
   `public/blog/`, or an existing `/blog/…` path.

If either is missing, ask before continuing.

Optional: `id` in the payload when you already know the CMS post id.

## Workflow

```
- [ ] 1. Read blog text + handle featured image
- [ ] 2. Find existing post (title.de, then optional id)
- [ ] 3. Draft title + lead HTML (de + en)
- [ ] 4. Write payload JSON
- [ ] 5. Run update-blog.mjs
- [ ] 6. Verify rendered post
```

### Step 1 — Source + image

- Extract the **title** from the first line or heading in the source text.
- Place the featured image in `public/blog/` (landscape, no baked-in title text).
- Set `img` to `/blog/<filename>` (path under `public/`).

### Step 2 — Match existing post

Before writing content, check CMS for an existing post:

```bash
node -e "
import fs from 'node:fs'
const env = Object.fromEntries(fs.readFileSync('.env','utf8').split('\n').filter(l=>l&&!l.startsWith('#')).map(l=>{const i=l.indexOf('='); let v=l.slice(i+1).trim(); if((v.startsWith('\"')&&v.endsWith('\"'))||(v.startsWith(\"'\")&&v.endsWith(\"'\")))v=v.slice(1,-1); return [l.slice(0,i),v]}))
fetch(env.ORBITYPE_API_SQL_URL,{method:'POST',headers:{'X-API-KEY':env.ORBITYPE_API_SQL_KEY,'Content-Type':'application/json'},body:JSON.stringify({sql:\"SELECT id, title FROM posts ORDER BY created_at DESC\"})}).then(r=>r.json()).then(r=>console.log(JSON.stringify(r,null,2)))
"
```

Match order used by the script:

1. `payload.id` if provided
2. Exact `title.de` match
3. Fuzzy `title.de` ILIKE (first 48 chars) — for minor title drift in seeded data

### Step 3 — Draft `title` and `lead`

Same rules as [new-blog](../new-blog/SKILL.md):

| Tag                      | Use for                       |
| ------------------------ | ----------------------------- |
| `<h2>`                   | Section headings              |
| `<h3>`                   | Sub-headings / numbered steps |
| `<p>`                    | Paragraphs                    |
| `<ul>` / `<ol>` + `<li>` | Lists                         |
| `<strong>`               | Bold emphasis                 |
| `<em>`                   | Italic                        |
| `<a href="…">`           | Links                         |
| `<br>`                   | Line break inside an item     |

Rules:

- Body starts with `<h2>`, not `<h1>` (hero shows the title).
- Paragraphs in `<p>`; no `<img>`, `<style>`, `class`, or inline styles.
- Write fluent **de** and **en** (translate if only one language is given).

### Step 4 — Payload

See `payload.example.json`:

```json
{
  "title": { "de": "…", "en": "…" },
  "lead": { "de": "<h2>…</h2><p>…</p>", "en": "<h2>…</h2><p>…</p>" },
  "img": "/blog/your-hero.jpg",
  "keywords": ["einkauf", "…"],
  "status": "published",
  "id": "optional-existing-id"
}
```

- `img` — **required**; hero + card image path.
- `keywords` — optional SEO tags (derive from topic).
- `status` — default `"published"`.
- `id` — optional; forces update of that post.

Write to a temp file, e.g. `/tmp/update-blog.json`.

### Step 5 — Upsert

```bash
node .cursor/skills/update-blog/scripts/update-blog.mjs /tmp/update-blog.json
```

Prints `Updated post` or `Created post` with id and URL.

### Step 6 — Verify

With dev server running, open the printed `/posts/<id>/…` URL. Confirm hero
image, article sections, related posts, and newsletter CTA.

## Notes

- List excerpts are derived from `lead` — no separate excerpt field.
- URL slug comes from the English title at render time.
- For **create-only** (never update), use [new-blog](../new-blog/SKILL.md).
- Legacy one-off script: `_scripts/seed-blog-interim.mjs` — prefer this skill.
