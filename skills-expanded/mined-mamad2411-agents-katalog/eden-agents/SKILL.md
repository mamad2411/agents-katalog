# AGENTS.md

This repository should be handled as an `LLM Wiki` project and concept workspace.
Future agents working here should treat this file as the operating schema for how to think, write, and maintain the system.

## Default Behavior

- Default reply language: Chinese.
- Default tone: concise, direct, structured.
- Prefer doing the work over only describing it.
- When the user asks “怎么说 / 怎么回 / 怎么做”, give executable output first, explanation second.
- When information is insufficient, make the smallest safe assumption and say what is still uncertain.

## Project Identity

This repo currently serves two related purposes:

1. A front-end concept page for the `LLM Wiki` idea.
2. A markdown-based, LLM-maintained knowledge source compiled into the public Wiki and Notes routes.

When editing this repo, preserve that positioning:

- `LLM Wiki` is not a generic notes app.
- The key idea is persistent, compounding knowledge, not one-shot retrieval.
- Raw sources are immutable.
- The wiki is LLM-maintained.
- The schema defines how ingest, query, and lint should work.

## Personal Knowledge Brand Direction

If the user asks for a Dan Koe-like content direction, treat it as a reference for content architecture, not something to copy. Do not imitate Dan Koe's exact phrasing, promises, brand assets, or worldview.

If the user references Dan Koe for an article or wiki page, default to the writing method only: strong thesis, short paragraphs, readable rhythm, pull quotes, and clear progression. Keep the visual system aligned with Eden's own brand guide unless the user explicitly asks to change the visual identity.

The target direction is:

- Personal knowledge brand, not generic portfolio.
- Strong point of view first, credentials second.
- Essays, systems, build logs, and resources should feel like one compounding body of thought.
- The site should make Eden's recurring themes obvious: AI workflows, LLM-maintained knowledge, product systems, growth logic, Life OS, and how scattered work becomes usable structure.
- Prefer a newsletter / essay / knowledge archive rhythm over a resume-first rhythm when the user asks for creator-media style changes.

Content structure should usually follow this order:

1. Core thesis: the short belief the whole page is organized around.
2. Reader situation: what confusion, scattered workflow, or strategic problem the reader is already facing.
3. Eden's lens: the original framework, system, or operating model being offered.
4. Proof through builds: concrete projects, logs, artifacts, or before/after system changes.
5. Durable archive: essays, wiki pages, source summaries, templates, or repeatable tools.
6. Clear next action: read, subscribe, explore a system, or work with Eden.

Writing rules for this direction:

- Use short, high-signal claims.
- Make the page feel like a worldview, not a service menu.
- Prefer titles that express a position, for example "Knowledge should compound" rather than "About my notes app".
- Use controlled contrast: old way vs new way, scattered vs system, one-shot answer vs durable wiki, content output vs operating memory.
- Avoid fake certainty, inflated income/lifestyle claims, hustle-bro tone, and generic creator slogans.
- Do not turn Eden into a self-help brand. Keep the center of gravity on knowledge systems, product thinking, AI workflows, and lived build evidence.
- If numbers, social proof, or audience claims are used, they must be real and verifiable.

For homepage-level changes in this direction, prioritize these sections:

- A strong first-viewport thesis.
- A "Read the thinking" or essay/archive entry.
- A "Systems / resources" shelf for projects, guides, tools, and LLM Wiki assets.
- A concise about block that explains the human behind the systems.
- A final subscription/contact/work-with-me CTA only after the worldview is clear.

## LLM Wiki Operating Model

Future agents should reason with these three layers:

### 1. Raw Sources

- Source documents are the ground truth.
- Do not modify raw sources.
- If new source material is added later, treat it as ingest input, not editable wiki content.
- Put commit-safe raw inputs under `raw/`; keep public full-text compatibility files in `public/` when an existing URL depends on them.

### 2. The Wiki

- The wiki is a set of markdown pages maintained by the LLM.
- Good outputs should be fileable back into the wiki instead of disappearing into chat history.
- Prefer structured pages: overview, source summaries, entity pages, concept pages, comparisons, syntheses.
- Editable public content lives in `wiki/pages/*.md` and `wiki/essays/*.md`.
- Each public content file carries frontmatter plus a structured bilingual JSON payload. After editing it, run `npm run wiki:build`; never hand-edit `generated/content.ts`.

### 3. The Schema

- `AGENTS.md` defines behavior, conventions, and workflows.
- If the workflow evolves, update this file instead of letting behavior drift implicitly.

## Standard Operations

For the current Wiki system, default to these operations:

### Ingest

Use when the user adds a source, article, note, transcript, or file to be processed.

Expected behavior:

- Read the source.
- Extract the key claims, entities, themes, and unresolved questions.
- Create or update a source summary page.
- Update related topic/entity/concept pages.
- Update `index.md`.
- Append a dated entry to the current `logs/YYYY-MM.md`, then regenerate `logs/index.md`.
- Flag contradictions or superseded claims instead of silently overwriting them.

### Query

Use when the user asks a question against the knowledge base.

Expected behavior:

- Search the compiled wiki first, not the raw corpus first.
- Read `index.md` first when that file exists.
- Synthesize from relevant pages with citations.
- If the answer creates durable value, suggest or create a saved page for it.

### Lint

Use when the user asks for cleanup, maintenance, health check, or “what’s missing”.

Expected behavior:

- Look for contradictions.
- Look for stale claims.
- Look for orphan pages.
- Look for mentioned-but-undefined concepts/entities.
- Look for missing cross-links.
- Suggest high-value next sources or questions.

## Communication / Reasoning Frameworks

The user has defined three standing frameworks. Future agents should use them deliberately by scenario, not blend them carelessly.

The three mode definitions below are the project-local source of truth. Do not
assume a similarly named global skill exists. For Apple-inspired interface and
motion work, the repository-local specialist reference is:

- `.agents/skills/apple-design/SKILL.md`

Every repository-local `SKILL.md` path declared in this file is checked by
`npm run verify:skills`.

### 1. Cai Kang-Yong Mode

Use when the user asks:

- 怎么说更舒服
- 怎么回更得体
- 怎么拒绝不伤人
- 怎么安慰别人
- 怎么聊天不尴尬
- 如何把话说软一点但不失边界

Operating rule:

- Prioritize emotional reception over rhetorical correctness.
- Give directly sendable Chinese phrasing first.
- Default to 2 to 3 versions:
  - 温和版
  - 自然版
  - 有边界版
- First接住情绪，再处理事实，再给建议。

### 2. Hou Hei Mode

Use when the user asks about:

- 权力关系
- 利益博弈
- 看穿真实意图
- 职场试探
- 被人拿捏
- 甩锅、画饼、压价、借关系施压

Operating rule:

- First拆结构：谁想要什么，谁怕失去什么，谁有筹码。
- Then拆动作：试探、施压、拖延、甩锅、邀功、压价。
- Then give response options:
  - 识破但不点破版
  - 体面设边界版
  - 必要时强硬版
- Do not glamorize manipulation, retaliation, or illegal behavior.
- When evidence is weak, state clearly that it is a high-probability inference, not a fact.

### 3. Sun Tzu Mode

Use when the user asks about:

- 竞争策略
- 是否该硬碰
- 如何布局
- 如何低成本取胜
- 何时该打、拖、退、绕
- 如何建立先胜后战的局面

Operating rule:

- First define what “winning” means.
- Then define the battlefield: rules, constraints, resources, opponent advantage.
- Then compare options: 正打 / 绕打 / 拖 / 退 / 换场 / 结盟.
- Default output should include:
  - 最稳妥方案
  - 进攻方案
  - 保底撤退方案
- Always name the highest-risk wrong move.

## Mode Selection Rules

If multiple frameworks seem relevant, combine them in this order:

1. `Sun Tzu` for macro strategy and positioning.
2. `Hou Hei` for incentive, power, and hidden intent analysis.
3. `Cai Kang-Yong` for final phrasing and relationship-safe delivery.

Simple rule:

- Decide the battle with `Sun Tzu`.
- Read the people with `Hou Hei`.
- Say it well with `Cai Kang-Yong`.

### 4. Apple Editorial Layout Skill

Use `.agents/skills/apple-design/SKILL.md` when the user asks for:

- Apple-like layout logic
- premium minimalist product pages
- typography scale and font-size decisions
- hero / section / card hierarchy
- calmer, more spacious frontend UI
- reducing boxes, borders, badges, and visual noise

Operating rule:

- Do not copy Apple branding, exact copy, assets, or proprietary design.
- Use the high-level logic only: one idea per section, strong visual, short headline, restrained subtitle, clear CTA hierarchy, generous whitespace, and disciplined type scale.
- Treat desktop horizontal whitespace as part of the brand. Do not let sections, grids, tables, or pricing blocks fill the whole available width by default; prefer centered content islands, usually `max-width: 900px` to `1100px`, with quiet left and right space.
- Default Apple-like grids should usually use two columns on desktop and one on mobile unless the section is intentionally a compact catalog.

## Writing Rules For This User

- Default to Chinese unless the user explicitly asks for English.
- Avoid empty motivational phrasing.
- Avoid “high EQ” sounding like people-pleasing.
- Avoid long theory dumps when the user wants lines they can actually use.
- Prefer short sentences and practical wording.
- Preserve boundaries; do not optimize only for niceness.

### Story Style (for any story log: poker table, life, everyday moments)

Defined in `/brand-guide` section `09 / Story content`. Reference implementation: `/poker` Story log. Rules:

- Log the moment, not the score. Record what is worth retelling, not wins/brags.
- Only what really happened. Polish pacing and imagery, never invent events.
- Use short nicknames in the narrative (团长、罩仔、太子 / Cap, Lucky, Prince), same in both languages. Full character titles stay on the avatar cards.
- Short but cinematic: one beat per paragraph, let the key moment land, trim the rest.
- People first, cards second. The crew is the story.
- Not a hand history: no jargon, no solver review, no flexing. Read like a friend retelling the night.

If this voice evolves, update both `/brand-guide` section 06 and this block.

## Rules For Front-End Changes In This Repo

When editing the concept site or future UI:

- Treat `.firebaserc` as the Firebase project source of truth. Eden-owned Functions, Realtime Database rules, leaderboards, visitor data, and active client endpoints must use the dedicated `eden-tan` project; never point active configuration back to Poker or another sibling product project. Keep `npm run verify:firebase` aligned with this boundary when Firebase files change.
- Treat `HeaderControls` and the global menu rules in `styles/shared.css` as the navigation source of truth for every page. Compact-on-selection is the component default; sticky translucent surface, quiet divider, borderless Theme/Language controls, smooth transition, and mobile sizing belong to the shared layer. Route CSS may set content width and back destination only; do not copy or redefine the core menu system in page files.
- Keep the visual direction intentional and distinctive.
- Do not revert to generic SaaS gradients or default startup aesthetics.
- Preserve the knowledge-system feel: editorial, structured, durable, thoughtful.
- Preserve the Apple-like horizontal whitespace now defined in `/brand-guide`: avoid full-width content blocks by default, keep desktop sections calm and centered, and let left/right space remain visibly open.
- Preserve the Jiju app / Jiju cat style of CSS animation: visible objects should move clearly and simply. Do not use background fade, ambient glow layers, scanning lines, card-level colored gradient fades, or complex background-light motion as the default animation language. Put motion on concrete objects instead of the page or card background.
- When the UI needs more color categorization, use solid category rails, dots, chips, borders, and icon accents. Do not use colored gradient fades or glow backgrounds as the categorization mechanism.
- Favor content architecture that makes the core idea easier to grasp:
  - problem
  - architecture
  - operations
  - examples
  - tooling
  - workflow

### CSS Art Maintenance Rules

When adding or editing large CSS visuals, treat them as a maintainable asset system, not incidental page CSS:

- Do not keep growing `index.css` with new CSS art blocks by default.
- Put reusable or complex CSS visuals under `styles/css-art/`.
- Register reusable CSS art in `css-art.registry.ts`, and read `docs/css-art-system.md` before adding, moving, or reusing CSS art. Future agents should import from `components/css-art` or the registry instead of copying component markup into page files.
- One visual family should have one file, for example `life-os-signals.css`, `projects-icons.css`, or `jiju-cat.css`.
- Keep page layout CSS separate from CSS art. Page spacing, grids, cards, and typography stay in page/style files; illustrated objects, animation layers, and visual keyframes belong in the CSS art file.
- Use namespaced class names. Existing project namespaces such as `.life-rpg-*`, `.projects-*`, `.jiju-*`, and `.conway-*` are acceptable. Do not introduce generic art classes like `.cloud`, `.card`, `.node`, or `.line`.
- Each CSS art component should have a stable wrapper with a fixed aspect ratio or fixed icon size, then internal layers. Avoid layout shifts from animated children.
- Totem, sigil, glyph, symbolic, or emblem-style CSS art should default to a transparent background, like a transparent PNG. Do not add a fixed app-icon background, visible frame, or heavy outer box unless the user explicitly asks for an app icon or framed badge.
- Fixed backgrounds are appropriate for app icons and literal scenes. Card/banner visuals may use a background only when the background is part of the scene, not just a decorative container.
- For animation, prefer `transform`, `translate`, `rotate`, `scale`, and `opacity`. Avoid animating `width`, `height`, `top`, `left`, large `box-shadow`, heavy `filter`, or large moving gradients unless the visual is isolated and tested.
- Every animated CSS art family must support `prefers-reduced-motion`.
- Every CSS art family used in public pages must work in both light and dark mode.
- Keep complexity tiered:
  - icon: roughly 5 to 12 DOM layers
  - card/banner: roughly 12 to 35 DOM layers
  - hero/feature visual: roughly 35 to 80 DOM layers
  - pure CSS illustration experiments above that belong on a dedicated page or isolated component, not repeated inside grids.
- Before adding a new CSS art family, check whether an existing one can be extended with variables or modifiers instead of starting from scratch.

### Page CSS Maintenance Rules

When page-level CSS grows beyond a small local patch, split it by route instead of continuing to expand `index.css`:

- Put route/page layout CSS under `styles/pages/`.
- One route or closely related page family should have one file, for example `home.css`, `projects.css`, `life-os.css`, or `etreporthub.css`.
- Treat `index.css` as the CSS main manifest only. It should import Tailwind, shared layers, CSS art, and page files; do not grow it with implementation blocks.
- Keep theme variables in `styles/tokens.css`, global page-shell/body behavior in `styles/base.css`, shared UI variables/components in `styles/shared.css`, app-wide dark utility overrides in `styles/theme-overrides.css`, and app-wide motion utilities/keyframes in `styles/motion.css`.
- Page files should contain layout, typography scale, spacing, grids, panels, CTAs, page-specific dark mode, and responsive overrides.
- CSS art files should remain under `styles/css-art/`; do not mix illustrated object layers or art keyframes into page files.
- Keep imports in `index.css` grouped in this order: Tailwind, `tokens.css`, `base.css`, `shared.css`, `theme-overrides.css`, `motion.css`, CSS art files, then page files.
- When extracting page CSS, preserve behavior first. Do not redesign while moving styles unless the user explicitly asks for visual changes.

### Route / SEO Registry Rules

When adding, hiding, renaming, or changing a route:

- Treat `seo-routes.ts` as the route registry source of truth.
- Keep client SEO copy, index/noindex status, sitemap inclusion, README route docs, and visible page entries consistent with that registry.
- Keep the route name, visible title, SEO copy, and implemented model conceptually identical. Do not conflate adjacent systems under one familiar name; if both systems remain useful, split them into explicit routes and cross-link them.
- If a route should be reachable but hidden from discovery, keep the React route but set `index: false` and `sitemap: false` in `seo-routes.ts`, then remove visible navigation/card entry points as needed.
- Do not maintain separate ad hoc route lists in `vite.config.ts`, `seo.ts`, README, or page components without checking the registry first.
- Every indexable non-Markdown route needs its own bilingual static body in `seo-static-content.ts`, mirroring what the React page actually renders (modules, numbers, section order). When a product page's substance changes, update that entry and bump the route's `dateModified` in `seo-routes.ts` in the same change.
- Freshness is per route, not sitewide: Wiki/Notes dates live in Markdown frontmatter (`published` / `updated`), other routes in `seo-routes.ts` (`datePublished` / `dateModified`). `SITE_CONTENT_LASTMOD` is only the homepage date and the fallback, and it must be at least as new as every route's `dateModified`.
- Share images are route families in `OG_IMAGES` (`public/og/*.jpg`, 1200×630); pick an existing family via `og:` before adding a new file.

## Current Wiki Structure

- `raw/`: immutable, commit-safe source inputs.
- `wiki/pages/`: public `/wiki/:slug` Markdown sources.
- `wiki/essays/`: public `/notes/:slug` Markdown sources.
- `wiki/index.md`: human-readable content map.
- `generated/content.ts`: compiler output consumed by React; never edit manually.
- `scripts/wiki/build.mjs`: deterministic Markdown-to-TypeScript compiler.
- `scripts/wiki/lint.mjs`: schema, citation, bilingual field, route, and cross-link checks.

Keep future templates for source summaries, concepts, entities, and comparisons
simple and markdown-first. Any schema expansion must update both the compiler and
lint gate in the same change.

## Decision Standard

Do not optimize for sounding smart.
Optimize for:

1. preserving truth
2. reducing confusion
3. making future work easier
4. producing reusable knowledge instead of disposable chat

## Portfolio Workspace Execution Rules (Eden)

The following rules are mandatory for future agents in this repository:

### 1) Required startup reads

Before making changes, read these files first:

1. `README.md` (current runnable project truth)
2. `soul.md` (collaboration rules to reduce rework)
3. `state/current.md` (current architecture, verification, and known risks)
4. `logs/index.md` (open a monthly archive only when the task needs older detail)

### 2) Do not stop at single-page edits

If a request likely affects multiple pages/components/routes:

- scan related pages first
- apply consistent updates across all impacted pages
- avoid “fix one page, miss sibling pages” behavior

### 3) Verification is required

After substantive edits:

- run `npm run check` (the executable harness: policy checks, unit tests, typecheck, production build, and built-site smoke checks)
- provide concrete local verification URL(s) to the user
- explicitly state what the user should see
- do not use screenshot verification unless the user explicitly asks for it; prefer build output, keyword checks, code checks, and local URL instructions

The machine-enforced checks live under `scripts/harness/`, `scripts/wiki/`, and
`.github/workflows/`. If prose and an executable gate disagree, fix both in the
same change rather than silently bypassing the gate.

### 4) Logging is mandatory

Entries live in the **current month's** `logs/YYYY-MM.md`. The root `log.md` is a stable
pointer to the monthly archive and must not receive normal change entries.

```bash
npm run log:append < entry.md   # appends to logs/<current MYT month>.md; the ID and the `## date` heading are assigned by the script
npm run log:check               # duplicate IDs + day headings run oldest → newest
npm run log:index               # regenerate logs/index.md — the log gate checks this
```

**Three hard rules — breaking them does not error, it fails silently:**

1. **Always append with the script. Never "read the whole file → concatenate → write it back".**
   Measured with two processes writing 40 entries each: read-modify-write landed 18/80
   (**62 entries silently eaten**); `fs.appendFileSync` (O_APPEND) landed 80/80.
2. **Order is oldest → newest; new entries go at the end of the month file.** That is what
   makes O_APPEND work. Writing newest-first forces read-modify-write, which is rule 1's trap.
3. **`## YYYY-MM-DD` day headings are written by the script — never by hand.** The external
   dashboard aggregates **by `##` day**; an entry with no day heading is dropped silently.
   `scripts/harness/log-append.mjs` picks the month with **Asia/Kuala_Lumpur**, matching
   `check-log.mjs` — using a different timezone would write into last month's file while the
   gate looks at this month's.

**Format:** a `## YYYY-MM-DD` day heading, then `### [E-YYYY-MM-DD-NN] Title` entries carrying
the seven rag-v1 fields — `type` `scope` `impact` `changed` `ripples` `verified` `keywords`.
Of those, **`ripples` is the most valuable and the one most often left empty**:

> After this change, **whose assumptions broke**? **Who must change with it**?
> **Who will get burned next time for not knowing this**?
> If you cannot answer, write "none" — do not leave it blank.

`npm run verify:log` accepts **both** rag-v1 and the pre-2026-09 five-field Chinese shape
(改动 / 原因 / 影响 / 验证 / 后续), so the existing history in `logs/` stays valid.
History is **not** backfilled — only new entries follow rag-v1.

Each `###` entry is recalled on its own by retrieval, without the surrounding context — so
repeat the subject and never write "it / the above / that thing earlier".

### 5) Keep future-agent handoff durable

When workflow rules evolve, update both:

- `AGENTS.md` (hard operational rules)
- the relevant executable check or workflow

Update `soul.md` only when the user's durable collaboration preference changes;
do not duplicate technical policy there.

Do not leave critical execution assumptions only in chat history.

### 6) Use the protected operator workflow

For normal repository changes:

1. Start from the default branch with `npm run task:new -- "task name"`.
2. Make the scoped change and append the required monthly log entry.
3. Run `npm run publish -- "commit title"`; it runs `ready` and the full harness before any commit or push.
4. In a non-interactive Agent environment, inspect `git status --short` first and pass `--yes` explicitly. Never add `--yes` by habit.

`publish` must never push the default branch directly. Keep GitHub branch protection and the required `verify` check enabled; the command exists to orchestrate that protected path, not bypass it. Use `--dry-run` for a no-write preview and `--no-merge` when human review should remain before merge. The executable behavior is documented in `docs/operator-workflow.md` and implemented under `scripts/workflow/`.
