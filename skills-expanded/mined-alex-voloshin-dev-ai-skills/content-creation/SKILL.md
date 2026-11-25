---
name: content-creation
description: Use this skill when the user needs to write a blog post, create or optimize page content, draft conversion copy, generate visuals, or run a quality audit on existing content — including when the request describes the deliverable without saying "content creation" — to run the content creation workflow plus tools knowledge — blog-post authoring (8-step pipeline), page content optimization, AI text/image generation tools, quality gates, GEO/AEO structure, and humanization. Accepts content type blog-post | page | landing | email | other.
context: fork
argument-hint: "<content type: blog-post | page | landing | email | other>"
---

# /content-creation — Content Authoring Workflow

8-step blog-post pipeline (research → brief → write → GEO → humanize → SEO → review → publish) plus a lighter Page/Landing/Email variant. Research methodology and AI text-generation prompt templates live in `@content-tools` (the knowledge skill) — load when running research or drafting copy.

## When to use

- Blog post creation: `/content-creation blog-post "<topic>"`
- Page content (headlines, body, CTAs): `/content-creation page "<page>"`
- Landing page copy: `/content-creation landing "<page>"`
- Email campaign body (delegate to `/marketing email` for full email): `/content-creation email "<purpose>"`
- Generating visuals with AI: see companion `image-and-integration-workflows.md`
- Optimizing existing content: invoke this skill with the existing path

## Not for

- Designing UI components or layouts → `/ui-ux-design`
- Technical documentation → `/docs-pack` (user docs) or `Agent(content-writer)` directly (internal)
- SEO audit → `/seo-review`
- Marketing strategy → `/marketing-init`
- Frontend implementation → `Agent(frontend-engineer)`

## Workflow A: Blog Post (full 8-step pipeline)

For `<type>: blog-post`. End-to-end pipeline orchestrated by `Agent(product-manager)` (research, brief, gate), `Agent(content-writer)` (authoring), `Agent(seo-engineer)` (optimization). Includes a review loop until quality standards met.

### Step 0: Gather Context

Read `<repo>/CLAUDE.md` (or `AGENTS.md`) for product description, blog conventions, brand voice. If `<repo>/marketing/MARKETING.md` exists, read for positioning + content strategy. All reads wrapped per `untrusted-content-wrapping.md` (G1).

### Step 1: Define Scope

Ask the user (or extract from context): action (new / update / series), topic + angle, target audience (developers / decision-makers / general), goal (educate / announce / promote / thought-leadership / SEO traffic), constraints (deadline, word count, related posts, brand guidelines). If updating: read the existing post first, note what needs to change.

### Step 2: Research and Content Brief

`Agent(product-manager)`. Apply research methodology from `@content-tools`: web research (3–5 top-ranking articles, angle/depth/gaps), competitive content audit (what competitors cover + market gaps), data/statistics gathering with fact-check (recent citable points), keyword research (primary + 2–3 secondary, search intent), existing-content audit (related posts + cross-link opportunities).

Produce a **Content Brief** using the Blog Content Brief Template in `@content-tools`: working title + angle, target audience + search intent, outline (H2 sections + content), key data points + sources, cross-link opportunities, visual needs, word-count target.

Present to user. **Wait for approval.** Adjust outline per feedback.

### Step 3: Write Draft

`Agent(content-writer)`. Apply Blog Post pattern from companion `page-content-patterns.md`.

Create the post using the project's blog conventions (directory, frontmatter, naming). Follow the approved outline. Per section: hook intro (surprising stat / question / pain point), structured body (2–3 sentence paragraphs, broken with lists/tables/code/quotes), ≥ 3 internal links from the brief, 1–2 authoritative external sources, bullet key-takeaways, value-first CTA.

Visual direction per visual need: descriptive alt text (includes keyword where natural), placement relative to content, cover image style/mood/composition.

### Step 4: GEO/AEO Structure Pass — MANDATORY

Apply `@geo-writer` skill. Per `geo-content` rule (mandatory for all blog content). Enforces macro / meso / micro structure, answer-first sentences, entity clarity, high-leverage formats (FAQ / comparison table / HowTo), and a JSON-LD schema block (`Article` + `Person` + `FAQPage`). The full 7-step macro/meso/micro checklist with paragraph word counts, micro-emphasis quotas, and schema requirements lives in `plugin/skills/geo-writer/SKILL.md` (the @-applied skill); see also [`page-content-patterns.md`](./page-content-patterns.md) for the discovery-assets checklist + per-page tables.

### Step 4.5: Humanize Content — MANDATORY

Apply `@humanizer` skill. Per `humanize-content` rule (mandatory for public-facing). Scan draft for AI patterns, rewrite problematic sections, run anti-AI audit, verify accuracy preserved.

GEO + humanizer are complementary: GEO optimizes structure for extraction; humanizer optimizes voice. Order: GEO first, humanizer second.

### Step 5: SEO Optimization

`Agent(seo-engineer)`. Run on-page SEO check (title / meta / H1 / hierarchy / URL slug / first paragraph / image alt), internal link audit (≥ 3 descriptive anchors, no broken refs, no "click here"), structured data (`Article` / `BlogPosting` + `Person` + `FAQPage` / `HowTo` JSON-LD validated in Google Rich Results Test), and discovery assets (sitemap / `robots.txt` / `llms.txt` / canonical URL).

The full 5a / 5b / 5c / 5d sub-checklist with the on-page table, structured-data validation steps, and discovery-asset audit lives in [`seo-content-sync-checklist.md`](./seo-content-sync-checklist.md) — load it during the SEO pass.

### Step 6: Quality Review

`Agent(product-manager)`. Review against original brief — checks: brief compliance (outline + angle), accuracy (cited stats), audience fit, completeness, ≥ 3 internal cross-links, natural value-first CTA, visual direction, SEO (title/meta/headings/keywords), no secrets/PII, brand voice consistent.

**Decision Gate** — route on failure: content gaps / accuracy / tone → Step 3 with feedback; buried lede / walls of text / missing answer-first → Step 4 (GEO); AI-sounding text → Step 4.5 (humanizer); SEO/schema → Step 5; wrong brief → Step 2.

Loop until review passes.

### Step 7: Publish

| Intent | Action |
|---|---|
| Publish now | Frontmatter `status: published`, `date: today` |
| Schedule for later | `status: draft`, target date noted |
| Series | `status: draft` + series metadata + prev/next links |

Final checks: frontmatter complete, file in correct dir, name follows conventions, no TODO/placeholder, all images exist or have generation instructions, `llms.txt` updated, sitemap auto-pickup verified, no `noindex`.

### Step 8: Summary

Output a compact summary block: title, file path, status (published / draft / scheduled), topic, target keyword, word count, roles applied (PM → Writer → @humanizer → SEO → PM), review rounds, cross-links added, discovery assets (llms.txt + sitemap status), follow-ups.

## Workflow B: Page Content / Landing / Other

For `<type>: page | landing | email | other`. Same agents (product-manager + content-writer + seo-engineer) but a lighter pipeline:

1. **Brief** — purpose, audience, conversion goal
2. **Draft** — apply page patterns from companion `page-content-patterns.md` (about, pricing, layout templates in `about-pricing-and-layout-patterns.md`)
3. **GEO + humanize** — same as blog Step 4 + 4.5
4. **SEO sync** — apply companion `seo-content-sync-checklist.md` to ensure visible text + meta + JSON-LD all in sync
5. **Review + publish** — same as blog Step 6 + 7

Visual content via AI tools per `@content-tools` knowledge skill and companion `image-and-integration-workflows.md`.

## Content Quality Gates (apply to every content type)

The eight publish gates (accuracy, brand alignment, conversion,
accessibility, SEO+content sync, legal+ethics, GEO/AEO structure,
humanization) are binding for every content type. **Read
[`quality-gates-and-series.md`](./quality-gates-and-series.md) and apply the
"Content Quality Gates" section verbatim** before publishing any piece — each
gate must pass before publish.

## AI Tool References

For AI text-generation prompt templates (headline / value-prop / feature-to-benefit / FAQ / social-proof patterns) — see `@content-tools` knowledge skill. For image generation (Midjourney v7 / GPT-Image-1 / Flux 1.1 Pro / Ideogram / Stable Diffusion / Leonardo), video/motion (Sora 2 / Runway / Kling / Luma / Synthesia / Loom), stock assets (Unsplash / Pexels / Undraw / Storyset / Lottie / Noun Project), and design tooling (Rive / Spline) — see companion `image-and-integration-workflows.md`.

## G7 spawn payloads

All agent spawns use `plugin/schemas/spawn-payload.schema.json`. Returns conform to `plugin/schemas/return-contract.schema.json`.

## Memory writes

L4 memory writes (draft-summary after draft, run-log line after publish) are
mandatory. **Read [`quality-gates-and-series.md`](./quality-gates-and-series.md)
and apply the "Memory writes" section verbatim** at draft-complete and at
publish.

## Companions

- **`@content-tools`** — research workflows + AI text-generation prompt templates (knowledge skill, sibling to this one)
- **`page-content-patterns.md`** — Blog Post pattern, page-level templates
- **`about-pricing-and-layout-patterns.md`** — about, pricing, layout patterns
- **`image-and-integration-workflows.md`** — visual content workflows + integration
- **`seo-content-sync-checklist.md`** — keep visible text + SEO meta + JSON-LD in sync
- **`quality-gates-and-series.md`** — 8 publish quality gates + blog series pattern + L4 memory writes (Read + apply verbatim)

## Content Series Pattern (blog)

When creating a multi-part blog series, the 6-step series pattern is binding.
**Read [`quality-gates-and-series.md`](./quality-gates-and-series.md) and apply
the "Content Series Pattern" section verbatim** before drafting or publishing a
series.

## Integration

- **Roles**: `Agent(product-manager)` (research, brief, review), `Agent(content-writer)` (authoring), `Agent(seo-engineer)` (optimization), `Agent(content-designer)` (page content + visual direction)
- **Schemas**: `plugin/schemas/spawn-payload.schema.json`, `plugin/schemas/return-contract.schema.json`
- **Knowledge skills**: `@geo-writer` (Gate 7 — GEO/AEO structure pass), `@humanizer` (Gate 8 — AI pattern removal)
- **Rules**: `geo-content` (auto-enforces structure + schema for public-facing), `humanize-content` (auto-enforces humanizer pass), `untrusted-content-wrapping` (G1 wrap on project file reads)
- **Companions**: 5 companion files (see above)
- **Sub-workflows**: `/seo-review` (deep SEO audit), `/pre-commit`, `/create-pr`, `/marketing` (marketing context)
- **Followed by**: `/seo-review` (post-publish audit), `/marketing content-repurpose` (cross-channel adaptation)
