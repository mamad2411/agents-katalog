---
name: blog-post
description: Author and publish a new blog post on the Tertiary Infotech Academy CMS — DB insert, branded R2 cover image, deep-funnel internal links, and SEO + lead-gen wiring. Use whenever the task is "write a blog post", "create a blog on X", "publish a journal entry", "add a new post about Y", or any request that produces a piece of long-form content for `/blog`. This skill coordinates with the `seo-audit` and `lead-magnets` skills — load both alongside it.
---

# Blog Post Authoring — Tertiary Infotech Academy

You are the in-house writer + publisher for the Tertiary Infotech Academy journal at `/blog`. Every post you ship must be **useful, specific, and verifiable**, score well in search, drive a measurable lead action, and look identical in format to every other post in the grid.

## Hard rules — do not violate

1. **Tone**: editorial and practical, not promotional. Write like a senior practitioner explaining a problem to a peer. Never use phrases like "Discover how", "Unlock the power of", "Industry-leading", "Best-in-class", "Revolutionary", "Cutting-edge". Lead with the user's problem, not our service.
2. **Storage**: post body lives in the `posts` table (`content` JSON + `contentHtml`); featured image **must** live in **Cloudflare R2**, never on the VPS / local disk / `public/` folder. Use `renderAndUploadCover()` from [src/lib/post-cover.ts](../../../src/lib/post-cover.ts) — it already uploads to R2.
3. **Format parity**: every published post must have `featuredImage` set to an `https://pub-62aa61537a134e9780c302c6f0795233.r2.dev/blog/...png` URL. A post without a cover renders the slug as text on `/blog` (visible regression). Run the missing-cover audit (see below) before declaring done.
4. **No AI tells**: no em-dash-followed-by-soft-rephrase tic, no "in conclusion", no "let's dive in". British / Singapore English spelling (organisation, utilise, programme).
5. **No Anthropic API**: when drafting via tooling, only use the Claude Agent SDK path already wired into [src/app/api/ai/assist/route.ts](../../../src/app/api/ai/assist/route.ts). Never add an `sk-ant-api*` key. Manual drafting in conversation is preferred for editorial control.
6. **Every link opens in a new tab**: every `<a>` in `contentHtml` — internal `/...` routes, external citations, `tertiarycourses.com.sg` deep links, and CTA links to `/contact` — **must** carry `target="_blank" rel="noopener noreferrer"`. The reader should never lose their place in the article. This is enforced by a post-processing pass in [src/lib/blog-jobs/link-enforcer.ts](../../../src/lib/blog-jobs/link-enforcer.ts), but write the attributes yourself so the raw HTML in the DB is correct from the start.

## Step-by-step workflow

### 1. Brief the post
Confirm with the user (or infer from the request):
- **Working title** and angle.
- **Target ICP** — pick from: SSG ATO operations lead, WSQ TP director, corporate L&D head, MOM compliance officer, school IT lead, government training partner.
- **Primary money keyword** (1) + **secondary keywords** (3–5). Run the keyword choice past the SEO conventions in [.claude/skills/seo-audit/SKILL.md](../seo-audit/SKILL.md).
- **Single CTA** — the one action you want the reader to take (book consultation, request demo, download checklist). Wire it via `/contact?source=blog-<slug-token>` per [.claude/skills/lead-magnets/SKILL.md](../lead-magnets/SKILL.md).

### 1b. Refresh sources via web search (mandatory for topical posts)

If the post covers a fast-moving topic (AI agents, new framework launches, regulator announcements, anything dated within the last 6 months), **run 1–2 targeted WebSearch / WebFetch queries** before drafting — don't write from memory. Goal: pull at least one 2025/2026 fact (release date, GitHub-star count, official URL, regulator quote) to make the post verifiable.

- Budget tightly: 1 search + at most 1 follow-up fetch. Skim, don't binge. The skill is "find the freshest credible source", not "read the whole internet".
- Capture the canonical **product / project URL** from the source (e.g. `openhands.dev`, `openhuman.ai`, `hermes-agent.nousresearch.com`) and hyperlink it inline on the relevant phrase — never paste bare URLs in prose.
- Cite at least one authoritative source (regulator, official blog post, founder announcement). Avoid linking to a competitor's marketing site as a citation.

### 2. Structure (≈ 1,500–2,500 words)

| Block | Purpose | Length |
| --- | --- | --- |
| Opening summary paragraph | One paragraph, ends with the primary CTA link. **Do NOT prefix it with the literal label "TL;DR —"** — write the summary directly. Readers find the inline label gimmicky. | 60–90 words |
| H2 — Problem framing | What's broken in the reader's world right now. Cite a regulator / public source. | 150–250 words |
| H2 — What "good" looks like | Define the standard / requirement / solution shape. Use H3s for sub-areas. | 350–500 words |
| H2 — Comparison or framework | Table, checklist, or rubric. Concrete, not abstract. | 250–400 words |
| H2 — What we recommend / our approach | Plug, but earned by the prior sections. Link to one service page + one course. | 200–350 words |
| H2 — FAQ | 3–5 real objections the ICP would raise. H3 per question. | 250–400 words |
| H2 — What to do next | Three numbered next-steps, each a different intent level (read, learn, buy). | 80–120 words |

### 3. Deep-funnel link plan (mandatory)

Place **at least 6 internal links** across the post:

- **3+ internal Tertiary Infotech Academy links** to service pages or related blog posts. Use real routes — check [src/app/](../../../src/app/) before writing. Examples: `/ssg-ato-application`, `/training-management-system`, `/learning-management-system`, `/ai-solutions`, `/wsq-course-development`, `/tpqa-consultancy`, `/blog/<related-slug>`, `/contact`.
- **2+ external links to Tertiary Courses Singapore** (`https://www.tertiarycourses.com.sg`). **Each must deep-link to the single most relevant page for the anchor topic — never the homepage and never a generic category index when a specific course page exists.** Example: a mention of Python basics links to `https://www.tertiarycourses.com.sg/wsq-python-beginner-course.html`, *not* `https://www.tertiarycourses.com.sg/` or `https://www.tertiarycourses.com.sg/python-courses-singapore.html`. Find the exact course page by searching the catalogue (`https://www.tertiarycourses.com.sg/` → site search, or `site:tertiarycourses.com.sg <topic>` via the WebSearch tool) and **verify the specific URL returns 200 before publishing**. Resolution order, most specific first:
  - **Specific course page** (preferred) — e.g. `https://www.tertiarycourses.com.sg/wsq-python-beginner-course.html`, `.../wsq-machine-learning-data-science-python-training-course.html`
  - Topic category index (only if no single course fits the anchor) — e.g. `https://www.tertiarycourses.com.sg/python-courses-singapore.html`, `.../data-science-courses-singapore.html`. **For anything AI-related the index is `https://www.tertiarycourses.com.sg/artificial-intelligence-courses.html` — there is no `ai-courses-singapore.html` page; linking it is a known recurring bug.**
  - The homepage `https://www.tertiarycourses.com.sg/` is **not** an acceptable destination for a content link — only ever a last-resort and a signal the link plan is too shallow; pick a real page instead.
- **1+ authoritative external citation** — SSG developer portal, MOM, IMDA, SkillsFuture, NIST, OWASP, official vendor docs. Never link to a competitor's marketing page.
- **CTA links** (in addition to the 6 above): every CTA must include `?source=blog-<topic-token>` so the lead lands in `leads.source` correctly. Use distinct tokens per CTA position (`-top`, `-demo`, `-quote`).

**Anchor text**: link the **money keyword phrase**, not "click here" or "read more". The keyword and the destination should match (e.g. anchor "SSG ATO application" → `/ssg-ato-application`).

#### Canonical link map (use these exact destinations — do not re-resolve)

These anchor → destination pairs are fixed. When the body mentions one of these topics, link to the URL below verbatim. **Never** point any of these anchors at `https://www.tertiarycourses.com.sg/` (the bare homepage) — a homepage link here is always a bug.

| Anchor topic in body | Destination URL |
| --- | --- |
| "Python courses" / Python training / learning Python | `https://www.tertiaryinfotech.com/blog/openclaw-vs-hermes-vs-paperclip-ai-agent-comparison` |
| Any "AI courses" / "AI training" / "AI courses at Tertiary Courses Singapore" / any generic AI-courses anchor | `https://www.tertiarycourses.com.sg/artificial-intelligence-courses.html` — **canonical AI category URL, single source of truth**. **Banned URLs (do NOT emit):** `ai-courses-singapore.html`, `ai-courses.html`, the bare homepage. The auto-blog pipeline rewrites `ai-courses-singapore.html` → `artificial-intelligence-courses.html` defensively (see `rewriteKnownBadLinks` in [src/lib/blog-jobs/link-enforcer.ts](../../../src/lib/blog-jobs/link-enforcer.ts)) but you should still emit the correct URL inline. |
| "Paperclip" (the AI agent) | `https://paperclip.ing/` |
| "Hermes" (the AI agent) | `https://hermes-agent.nousresearch.com/` |
| "OpenClaw" (the AI agent) | `https://openclaw.ai/` |

For any topic **not** in this table, fall through to the resolution order above (specific course page → category index → never the homepage).

### 4. SEO checklist (delegate detail to the `seo-audit` skill)

Required fields when inserting the post:
- `slug` — kebab-case, ≤ 60 chars, money keyword first.
- `title` — ≤ 65 chars, money keyword in the first half, year if topical.
- `seoTitle` — ≤ 70 chars, ends with `| Tertiary Infotech Academy`.
- `seoDescription` — 140–160 chars, includes the money keyword and the CTA verb.
- `seoKeywords` — comma-separated, money keyword first, ≤ 8 terms.
- `canonicalUrl` — `https://www.tertiaryinfotech.com/blog/<slug>`.
- `excerpt` — 150–220 chars, used as the listing card teaser (no HTML).
- `categoryId` — pick the closest existing row in `categories` (1=Uncategorised, 2=LMS & TMS, 3=AI & Automation, 4=Compliance & Audit, 5=Training Guides, 6=EdTech Trends, 7=Robotics). Don't invent new categories.
- `authorId` — the seeded admin (`2` for angch@tertiaryinfotech.com unless told otherwise).
- `publishedAt` — current timestamp (or backdate only if the user explicitly says so).
- **Headings**: exactly one `<h1>` (rendered from `title`, do not add one in `contentHtml`). Use H2 for sections, H3 for sub-areas.
- **Schema**: blog posts inherit `BlogPosting` JSON-LD from the article route — do not add inline JSON-LD inside `contentHtml`.

Before finishing, run the `seo-audit` skill against the new slug.

### 5. Lead-gen wiring (delegate detail to the `lead-magnets` skill)

- Every CTA link MUST point to `/contact` with a `?source=blog-<token>` query (so the lead is attributed). See [src/components/sections/ContactForm.tsx](../../../src/components/sections/ContactForm.tsx) for how `source` is captured.
- The post must have **at least 3 CTA placements**: end of TL;DR, after the comparison/framework section, and in the final "What to do next" block.
- Match the CTA verb to the funnel stage — top-of-funnel reads ("Read the guide"), middle ("Book a 30-minute walkthrough"), bottom ("Request a deployment quote"). All three should resolve to `/contact` with different `source` tokens.
- If the topic warrants a dedicated lead magnet (checklist PDF, calculator), invoke the `lead-magnets` skill to design it instead of forcing a generic CTA.

### 6. Publishing — the actual insert

Write a single-purpose script under `scripts/` (suggested name: `scripts/insert-<slug>.ts`). Pattern:

```ts
import { db } from "../src/db";
import { posts, postTags, tags } from "../src/db/schema";
import { eq } from "drizzle-orm";
import { getR2Config } from "../src/lib/r2";
import { renderAndUploadCover } from "../src/lib/post-cover";

// 1. Upsert the post row by slug (set status='published').
// 2. Upsert tags by slug, then upsert post_tags links.
// 3. Generate cover via renderAndUploadCover(r2, title, slug, kicker) — this uploads to R2.
// 4. Update posts.featuredImage with the returned URL.
// 5. Log local and production URLs.
```

Run it: `npx tsx --env-file=.env scripts/insert-<slug>.ts`.

### 7. Cover image — Cloudflare R2 only

- Use `renderAndUploadCover(r2, title, slug, kicker)` from [src/lib/post-cover.ts](../../../src/lib/post-cover.ts). It builds the branded SVG, renders to PNG via `sharp`, and uploads to R2 at `blog/ai-<ts>-<slug>.png`.
- **Never** write the image to `public/`, the VPS disk, or any local path. The CMS expects R2 URLs in `featuredImage`.
- Pick a 2–4-word `kicker` that matches the category (e.g. `TMS · SSG-Integrated`, `AI · Workflow`, `TPQA · Audit`).
- Verify the resulting URL returns HTTP 200 before declaring done.
- For deeper styling rules, load the `blog-cover-image` skill.

### 8. Verify

After insert + R2 upload:

```bash
# 1. Article loads locally
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:3070/blog/<slug>

# 2. Cover is reachable
curl -s -o /dev/null -w "%{http_code}\n" <featuredImage-url>

# 3. Listing shows the image (not the slug text)
curl -s http://localhost:3070/blog | grep -A1 "<slug>" | head -10
```

Then audit the rest of the grid — run a one-off script that selects `published` posts with `featuredImage IS NULL OR ''` and fix any gaps before deploying.

### 9. Push to production

Use the existing sync flow (see [.claude/skills/remote-db-sync/SKILL.md](../remote-db-sync/SKILL.md)):

```bash
npx tsx --env-file=.env scripts/push-to-remote.ts posts
```

Then verify on production:

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://www.tertiaryinfotech.com/blog/<slug>
curl -s https://www.tertiaryinfotech.com/blog/<slug> | grep -oE 'pub-62aa[^"]*<slug-token>[^"]*\.png' | head -1
```

### 10. Clean up

Delete the one-off `scripts/insert-<slug>.ts` script after a successful production push — these are not meant to be checked in. The post lives in the DB; the script's job is done.

## Editing an existing post — the body is `contentHtml`, not `content`

The article route ([src/app/blog/[slug]/page.tsx](../../../src/app/blog/[slug]/page.tsx)) renders **`posts.contentHtml`** verbatim via `dangerouslySetInnerHTML`. The `content` JSON (TipTap doc) is the editor's source-of-truth but is **not what the public page renders**. They can drift.

When changing the body of an already-published post (fixing a link, a typo, a fact):

1. **Update BOTH columns.** A string replace on `content` alone changes nothing the reader sees; a replace on `contentHtml` alone leaves the admin editor stale. Patch both in the same script.
2. **Re-push and verify against the rendered HTML**, not the JSON: `curl` the production article and grep for the new and old strings. Production blog routes send `cache-control: no-store`, so a correct push is visible immediately — if the old value still shows after a push, the DB wasn't actually changed (you patched the wrong column).
3. Then re-run `scripts/push-to-remote.ts posts`.

This is a recurring trap: "the sync said upserted 48 but the page didn't change" almost always means `contentHtml` was never touched.

## Lists — formatting note

Blog body HTML renders inside `.prose-dark` ([src/app/globals.css](../../../src/app/globals.css)), which gives `<ul>` and `<ol>` a custom marker design. Tailwind's preflight strips `list-style`, so do **not** try to put markers back with classes — the skill CSS handles it.

What the reader sees:

- **`<ul>` items** — a rounded square chip (1.25em) with a cyan→purple gradient fill, 1px cyan border, soft inner glow, and a **cyan check-tick SVG** centred inside. Marker is absolutely positioned at the top-left of each `<li>`; the text indents 1.85em.
- **Nested `<ul>` items** — same chip shape, but the SVG switches to a **purple chevron tick** (`›`) and the border softens to purple. Differentiates depth at a glance.
- **`<ol>` items** — a **monospaced cyan number chip** in a rounded cyan-tinted circle, auto-incremented via a CSS counter. Use `<ol>` whenever sequence matters (steps, ranked checklists).

Authoring rules:

- Emit **plain semantic `<ul>` / `<ol>`** with `<li>` children. No `class`, no inline `style`, no manual bullet characters (`•`, `–`, `*`) at the start of items.
- Don't wrap items in `<div>` or `<p>` — `<li>` is a block container already; extra wrappers misalign the marker.
- Don't use `<ul>` as a layout primitive (e.g. for cards or feature grids). Reserve it for actual short-line lists where the tick reads as a checked item.
- Sub-bullets are fine, but go no deeper than 2 levels — the chevron variant is the deepest marker defined.

If markers ever stop appearing or look wrong (regression), fix `.prose-dark ul > li::before` / `.prose-dark ol > li::before` in [src/app/globals.css](../../../src/app/globals.css). Do **not** rewrite the post to compensate.

## Tables — formatting note

`.prose-dark` styles `<table>` / `<thead>` / `<th>` / `<td>` automatically:

- **Outer container** — 1px hairline border, 0.65rem rounded corners, faint white-tinted background. The whole table is `display: block` with `overflow-x: auto` so it never bursts the column on mobile.
- **Header row (`<thead>`)** — cyan-tinted band, bold white labels, 1px bottom divider.
- **Body cells** — hairline column dividers (subtle, not blocky), zebra rows (every even row a touch lighter), purple-tinted hover state.
- **Anchors inside cells** — inherit cyan colour automatically.

Authoring rules:

- Use **plain semantic HTML** — no inline `style`, no Tailwind classes, no `<div>` wrappers around the table.
- Always wrap the header row in `<thead>` (not a `<tr>` inside `<tbody>`) so the cyan band renders.
- Keep cell content short. Long URLs or paragraphs belong in body prose, not in cells — wide cells force horizontal scroll on desktop too.
- Three to five columns is the readable maximum. If you need more, split into two tables or rethink the structure.

Canonical pattern:

```html
<table>
  <thead>
    <tr><th>Dimension</th><th>Option A</th><th>Option B</th></tr>
  </thead>
  <tbody>
    <tr><td>Pricing</td><td>…</td><td>…</td></tr>
    <tr><td>Lock-in</td><td>…</td><td>…</td></tr>
  </tbody>
</table>
```

If the table renders raw (unaligned, no borders, no header band), `.prose-dark` table rules have been lost — fix the CSS, not the post.

## Link conventions — every anchor in the body

Blog body HTML is rendered verbatim via `dangerouslySetInnerHTML` on [src/app/blog/[slug]/page.tsx](../../../src/app/blog/[slug]/page.tsx) — there is **no** post-processor that adds attributes. Whatever you author is exactly what ships, so the attributes below must be hand-written into every `<a>` you emit.

**Every link to an external domain** (Tertiary Courses Singapore, regulators, vendor docs — anything not `tertiaryinfotech.com`) must:

- Open in a new tab — `target="_blank"`.
- Be safe and clean — `rel="noopener noreferrer"`. Add `nofollow` for any third-party page you don't editorially endorse (it stays `rel="noopener noreferrer nofollow"`).
- Carry a `title` attribute — a short, human-readable description of the destination (8–12 words, includes the topic keyword). This is an SEO + accessibility signal and the hover tooltip; it must describe the page, not repeat the anchor text verbatim.

**Internal links** (`/ssg-ato-application`, `/blog/...`, `/contact?source=...`) stay in the **same tab** — no `target="_blank"` — but still take a descriptive `title`.

Canonical external link:

```html
<a href="https://www.tertiarycourses.com.sg/wsq-python-beginner-course.html"
   target="_blank" rel="noopener noreferrer"
   title="WSQ Python Beginner course in Singapore — Tertiary Courses">Python fundamentals course</a>
```

Canonical internal link:

```html
<a href="/ssg-ato-application"
   title="SSG ATO application support for training organisations">SSG ATO application</a>
```

Anchor text is still the money keyword phrase (never "click here"); the `title` is the *description*, the anchor is the *keyword* — they are not the same string.

## Anti-patterns — flag and refuse

- **Generic AI-marketing fluff**. If a paragraph could be on any vendor's blog, rewrite it with a Singapore-specific or regulator-specific detail.
- **Stuffed keywords**. Each money keyword appears 3–6 times in the body, naturally. No "AI TMS AI TMS AI TMS" headings.
- **Dead links**. Every external link must be `curl`-verified to return 200 before publishing. Tertiary Courses Singapore changes its catalogue routes — re-check, don't assume.
- **Lazy Tertiary Courses links**. A `tertiarycourses.com.sg` link pointing at the homepage (or a broad category when a specific course page exists) is a defect — deep-link to the exact relevant course page.
- **Bare external anchors**. Any external `<a>` without `target="_blank"`, `rel="noopener noreferrer"`, and a descriptive `title` is non-conforming — fix it before publishing.
- **Image on VPS**. If you ever see code writing to `public/blog/`, the local filesystem, or the Docker container's disk for cover images, stop and route through R2.
- **Missing CTA source**. A `/contact` link without `?source=blog-...` is a leak — it loses the attribution that makes the funnel measurable.
- **Skipped SEO audit**. Don't claim done without running the `seo-audit` skill against the new slug.

## Quick reference

- Posts schema: [src/db/schema.ts](../../../src/db/schema.ts) (search for `posts = pgTable`)
- Article route: [src/app/blog/[slug]/page.tsx](../../../src/app/blog/[slug]/page.tsx)
- Listing route: [src/app/blog/page.tsx](../../../src/app/blog/page.tsx)
- Cover renderer: [src/lib/post-cover.ts](../../../src/lib/post-cover.ts)
- R2 config: [src/lib/r2.ts](../../../src/lib/r2.ts)
- Sync script: [scripts/push-to-remote.ts](../../../scripts/push-to-remote.ts)
- Contact form / lead intake: [src/components/sections/ContactForm.tsx](../../../src/components/sections/ContactForm.tsx), [src/app/api/contact/route.ts](../../../src/app/api/contact/route.ts)
- Related skills to load alongside: `seo-audit`, `lead-magnets`, `blog-cover-image`, `remote-db-sync`.

## Rules imported from the group's latest blog skills (Nov 2026)

Taken from `blog-pipeline` and `blog-publish` (`ai-mms`, Oct 2026) and `ai-pei`, adapted for this site. This file still wins on anything specific to this repo.

**Scope and honesty**

- A draft-only request does not authorise publishing. Only publish or sync when the user asked for that.
- Treat facts the user gives you about an event as authoritative, but do not add unsupported quotes, outcomes or job titles.
- Never invent likes, ratings, testimonials, attendance details or class photos. Do not reveal sensitive client data.
- Check course URLs, availability, fees and funding claims against current data before writing them.
- Write **SWDA** for the regulator. SSG merged into SWDA on 1 Jul 2026, so use "SSG" only in search keywords and old document titles.
- Never promise an approval, a pass or a TPQA grade. SWDA and IBF decide.
- Never say a consultant attends the TPQA on-site assessment; SWDA's advisory does not allow it.

**Topics that bring in leads**

Case studies from real work are the best performers: a concrete build log, what was learned, and a CTA to the matching service. Otherwise, write for what a buyer is searching for and route them to one service page:

| Reader's question | Link to | `source` token example |
|---|---|---|
| Can my course still be WSQ? WSQ 2.0, CASL, entry criteria | `/wsq-course-development` | `blog-wsq-route` |
| How do I get TPQA Grade 1, Tier 1 funding at up to 90%, or SCTP? | `/tpqa-consultancy` | `blog-tpqa-grade1` |
| Why was my IBF application rejected? Assessor Coach, FS SME | `/ibf-ato-application`, `/ibf-course-development` | `blog-ibf-gonogo` |
| What is new in SWDA ATO? Mock-up website, on-site assessment | `/ssg-ato-application` | `blog-ato-new-rules` |
| Do I need a PEI? Academic and Examination Boards | `/pei-ato-application` | `blog-pei-route` |
| I got a CQC outcome. What do I do? | `/cqc-consultancy` | `blog-cqc-outcome` |
| How do I design an SCTP and its job placement? | `/sctp-module-development` | `blog-sctp` |
| How do I become an approved CPD provider, such as for TAEPP? | `/cpd-course-development` | `blog-cpd-taepp` |

**Images inside a post**

- Compress photos before uploading to R2. Posts render them about 700–760px wide, so 1100px on the long edge is enough, at about JPEG quality 62, with a target under 150KB.
- Never upscale; cap at the smaller of the target and the original size.
- Crop from the original file rather than re-encoding a compressed copy, and look at the result before uploading.
- Before deleting a superseded R2 object, confirm nothing in **production** still references it. A local check is not enough.

**Editing existing content**

- Do not round-trip a post through a lossy decode such as `errors='replace'`. Decode strictly, and check the result has no `�` and the same number of em-dashes.

**Not imported, because it does not apply here**

- `MMD_Blog`, SQL migrations and the OpenMage steps are specific to `ai-mms`.
- FAQ `<details>` accordions: this repo renders from TipTap StarterKit, which has no `details` node, so they would be lost when the post is re-rendered. Keep FAQs as H3s.
- List markers and `<pre>` fixes: `.prose-dark` already handles lists, and TipTap keeps `<pre>` newlines.
