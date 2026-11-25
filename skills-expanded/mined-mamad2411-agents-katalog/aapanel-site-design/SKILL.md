---
name: aaPanel Site Design
description: >
  Design a website's UI spec and author a complete static front-end (HTML/CSS/JS) — the model
  picks a style, fetches the UI spec, and writes clean static pages. The artifact is a static
  file set under the project dir (draft → generated). Use it to:
  design a website / landing page / portfolio / official site / business site / personal site /
  company homepage / brand site. Scope: UI design +
  static front-end ONLY (HTML/CSS/JS). Available in website-type sessions via the Skills tool (chat_type=website). NOT for: WordPress (use
  WordPress, empty/bare sites, deploying user-supplied source code, or any non-UI panel task —
  these are refused with a pointer to a chat session (this skill never exits the website session).
---

# aaPanel Site Design

> **Single Source of Truth**: tool-usage limits (ProjectSave only for info docs; no Write/cp/echo on them; memory ProjectSave only, no NoteSave/DocSave; Hard Red Lines scope) live in the **website system_prompt** (`dynamic.py designer_prompts`, `prompts_name="website"`) — prompts are maintained centrally in `dynamic.py`. This document governs the **design workflow** (S0–S3, state machine, iteration). Changes to those limits must be made in `dynamic.py`, not here.

> **STOP. Read this document completely before doing anything.** Do NOT skip sections.
> **1 session = 1 project**, bound under `memories/projects/<id>/` — this skill drives that project's design workflow (S0–S3). Scope, forbiddens, and Hard Red Lines are in the system prompt.

---

## Core Rules

1. **UI design + static front-end.** Always a **single-page UI** (one page, all
   sections + anchor nav; never multi-page). CSS hand-written inlined in `<style>`, JS inlined in
   `<script>`; all assets CDN-linked, zero framework, zero JS runtime (Lucide icons excepted).
2. **Three writers, three jobs** (workflow spine): `ProjectSave` → project info docs + `meta_snapshot` + session binding; `Write` → the UI artifact; `RunCommand` → shell (`curl` style-spec fetch, image search). Info docs always overwrite with current factual content (not a changelog), on BOTH init AND iteration. **Strict per-writer limits live in the system prompt.**
3. **One session = one project.** `project_id` is set at S2 and never changes; route by project
   existence (ITERATE vs NEW).
4. **website session only** — runtime-enforced (chat sessions cannot load this skill); no check needed.
5. **Track progress with `TodoWrite`** — create the task list before set-up, using **neutral step titles** (no internal phase codes or file names), e.g. *Plan · Recommend a style · Set up the project · Fetch images · Build the UI*; mark one `in_progress` at a time, flip to `completed` when done.
6. **Iteration resets to `generated`.** ANY write to the UI (re-generate) forces `status→generated`;
   sync `meta_snapshot` accordingly.
7. **Iteration spec judgment (autonomous).** Decide by the nature of the change (both overwrite
   the progress doc with current factual progress):
   - **Light edit** (color / copy / image swap) → edit the UI only; do NOT touch the spec / the design. Then `ProjectSave(project_id=<id>, files={"meta.md": <full, status=generated>, "progress.md": <full>}, meta_snapshot={"status":"generated"})`.
   - **Heavy edit** (style / layout / design system) → **re-fetch the style spec** (curl -o overwrite from the new stem) + rewrite the design + regenerate the UI, then `ProjectSave(project_id=<id>, files={"meta.md": <full, style field updated + status=generated>, "design.md": <full new>, "progress.md": <full>}, meta_snapshot={"style": <new-stem>, "status":"generated"})`. No new session needed.
8. **UI spec = remote fetch + persist**: at S2 download the chosen style's design spec from
   `https://node.aapanel.com/aapanel/awesome/<Style-File>.md` (fallback host `jp1-node.aapanel.com`)
   and save it as the project's style spec — a self-contained copy. After that the project never
   needs the network again. See S1 for the style-file list, S2 step 2 for the fetch.
9. **Every image slot gets a real photo** — fetch via the skill script BEFORE writing HTML (see S3 Images).

---

## Tooling

| step | tools (risk) |
|---|---|
| Load skill | `Skills` (low) |
| S0 Route | `TodoWrite` (low) · `Read` (low, iterate only) |
| S1 Style | — (chat-only; catalog self-contained) |
| S2 Init | `RunCommand` (high, curl style-spec) · `ProjectSave` (low, internal) · `TodoWrite` (low) |
| S3 Generate | `Read` (low) · `RunCommand` (high, images first) · `Write` (high) · `ProjectSave` (low) · `TodoWrite` (low) |

---

## State Machine

```
draft ──S3 generate──→ generated
              ↑               │
              └─ S3 iterate ──┘  re-generate forces generated
```

- `draft`: project init done, artifact not yet generated.
- `generated`: the static UI artifact has been written.
- Any UI rewrite (S3 iteration) → forces `generated` (Core Rules #6).

---

## S0 — Intent + Route

> Session type is runtime-enforced (chat sessions cannot load this skill) — reaching here means a
> website session. No session check needed.

**Scope & route** — one decision tree:

**Out of scope → refuse.** Scope + refusal wording live in the system prompt (UI design only; deploying THIS skill's generated artifact is the sole in-scope exception — only on explicit user request + Hard Red Lines consent; anything else — WordPress, empty/bare site, foreign source code, SSL/DB/firewall/service/file management — refuse and point the user to a new chat session, never exit). Route the in-scope request below.

**In scope → route by project existence** (check the injected `## Active project` block for current
`project_id` + `status`):
- **ITERATE** (project exists): `Read` the project info (meta for `status`, design, progress) + the style spec + the current UI. Skip S1/S2 — style and `project_id` are set. Pick up by `status`:
  - `draft` → read the existing UI to see what's done, then regenerate at S3 (overwrite it, preserving finished sections). If the UI is absent (init crashed mid-S2): **verify the style spec is complete** (Read it; if truncated — size well under ~30KB or cuts off mid-token — re-fetch via `curl -o`); **verify the design is well-formed** (if half-written, rewrite it); then generate fresh at S3.
  - `generated` → apply the iteration spec judgment at S3 (Core Rules #7).
  - Either way, Core Rules #7 decides at S3: re-fetch the spec (heavy) or edit the UI only (light).
  Listen for what the user wants changed (or ask one focused question), then go to S3. For a
  brand-new project, tell them to start a new website session (Core Rules #4).
- **NEW** (no current project): extract **topic/subject** + **purpose** from the user's one line. If the intent is thin (you can't yet say what the site is for and who it's for), **keep asking focused questions to draw it out — do NOT jump to init (S2) on a guess**. One question at a time, plain language, never an interrogation. Only once topic + purpose are clear enough for a one-line summary → S1 → S2 → S3.

---

## S1 — Style Recommendation (before project init, chat-only)

Recommend **autonomously by intent** from the **Full Style Catalog** below (74 neutral style files) —
you are NOT bound to any fixed subset, and this is independent of any front-end style API. Pick **2–3**
that fit the user's topic / industry, present each as `file — one-line tone — best-for hint`. If the
user doesn't like them, swap in a fresh batch from the catalog.

- Present 2–3; user picks one, swaps, or says "you decide" (you pick + say why).
- The user may also name any style file directly (e.g. "use `Emerald-Devtool`") — accept verbatim.
- Record the chosen **style file stem** (no `.md` suffix, e.g. `Brand-Marketing`) → it is the
  the project meta's `style` value. At S2 the fetch URL appends `.md`: `.../awesome/<stem>.md`.

### Full Style Catalog — 74 style files (hardcoded list below; fetch any as `<file>.md`)

| Theme | Style files |
|---|---|
| **Dev / AI tools** | `AI-Developer` `AI-Lab` `Agent-Engineering` `Refined-AI` `Sunset-AI` `Gradient-AI` `Frontier-AI` `Gradient-Infra` `Dark-Devtool` `Editorial-Devtool` `Emerald-Devtool` `Gradient-Devtool` `Midnight-Devtool` `Terminal-Devtool` `Warm-Devtool` `Terminal-Mono` `Docs-Platform` `Developer-Platform` `Dark-Builder` `Visual-Builder` `App-Showcase` `Content-Platform` `Playful-Devtool` |
| **Minimal / Tech** | `Minimal-Tech` `Minimal-Docs` `Software-Craft` `Engineering-Tech` `Aerospace-Mission` `Tech-Corporate` `Enterprise` `Tech-Magazine` |
| **Data / DB** | `Dark-Database` `Dual-Database` `Vibrant-Data` |
| **Finance / Crypto** | `Crypto-Finance` `Institutional-Fintech` `Dark-Crypto` `Gradient-Finance` `Fintech-Brochure` `Fintech-Editorial` `Financial-Brand` |
| **Auto / Mobility** | `Corporate-Auto` `Motorsport-Engineering` `Luxury-Automotive` `Cinematic-Luxury` `Supercar-Luxury` `Auto-Editorial` `Mobility-Mono` |
| **Commerce / Retail** | `E-Commerce` `Cinematic-Commerce` `Product-Commerce` `Retail-Lifestyle` |
| **Brand / Editorial / Media** | `Brand-Marketing` `Console-Marketing` `Telecom-Editorial` `Magazine-Editorial` `Voice-Magazine` `Warm-Editorial` `Productivity-Editorial` `Editorial-Workflow` `Museum-Gallery` `Studio-Monochrome` `Mono-Serif` `Generative-Studio` `Retro-Gaming` `Retro-Web` `Music-Streaming` |
| **Workspace / SaaS** | `Friendly-SaaS` `Customer-SaaS` `Playful-Workspace` `Illustrated-Workspace` `Workplace-Messaging` `Visual-Discovery` `Workflow-Warm` |

---

## S2 — Init Project (the moment style is chosen)

> Init when topic + style are both settled. Not earlier (empty shell), not later (nowhere to put files).

1. **Generate `project_id`**: `snake_case` topic + timestamp suffix `%Y%m%d%H%M%S` (e.g. `photo_studio_20260630120000`). Must match `^[a-z0-9_]+(?:_[a-z0-9]+)*$` (underscores only; no consecutive/trailing). This is the only id — no separate uuid.
2. **Fetch `ui_spec.md`** (remote style spec → write directly to disk, do NOT relay through the model):
   `mkdir -p /www/server/panel/data/agent/memories/projects/<id>/site && curl -fsSL --create-dirs https://node.aapanel.com/aapanel/awesome/<stem>.md -o /www/server/panel/data/agent/memories/projects/<id>/ui_spec.md`
   (`<stem>` from S1, e.g. `Brand-Marketing`). The `-o` writes the ~31KB spec straight to the project
   dir — it never enters the model context, so no truncation/distortion. Try `node` first; on failure
   retry once on `jp1-node.aapanel.com`; only if both fail, tell the user and pause. `Read` it back
   (large file ~31KB — use a large `limit`) only when you need its tokens for S3.
3. **Build `meta.md`** with this exact flat frontmatter (parsed as plain `key: value` — no YAML lists/nesting;
   `status` is the single field the active-project scan filters on):

   ```
   ---
   id: photo_studio_20260630120000
   subject: Photography Studio Official Site
   industry: photography / visual
   style: Brand-Marketing
   status: draft
   ---
   # Project meta — authoritative source
   One-paragraph positioning. Sections planned. Current phase.
   ```
   - `status` MUST be one of: `draft`, `generated`.

4. **Build `design.md`**: positioning + section tree + per-section outline + component list. It **references**
   `ui_spec.md` ("visual spec = see ui_spec.md") and does NOT duplicate it.
5. **Build `progress.md`**: phases S0–S3 each marked pending; note current = S2 done.
6. **Persist project info + bind session** — ONE `ProjectSave` call (batch all info docs + binding together):
   `ProjectSave(project_id=<id>, files={"meta.md": <full content>, "design.md": <full>, "progress.md": <full>}, meta_snapshot={"status": "draft", "subject": <topic>, "style": <stem>})`.
   This binds the session as a website session. (Per-writer limits — ProjectSave only for info docs — are in the system prompt.)
7. Update `TodoWrite` (set-up complete), advance to build the UI.

---

## S3 — Generate Static Artifact (`draft` → `generated`)

Generate the pure-static UI. **Always a single-page UI** (all sections + anchor nav) — one page, never multi-page. Everything is
**AI-authored + CDN-linked — zero local asset files**.

**Generation order (do not reorder):**
1. Read the style spec for tokens (colors / type / components) — **large spec (~31KB): use a large `limit` (e.g. 3000+) to avoid truncation; read what you need, not necessarily all**.
2. **Fetch images first** — run the skill script below for EVERY image slot, collect the direct
   image URLs. You must have these URLs in hand BEFORE writing the UI (Core Rules #9).
3. Write the UI with all CSS inlined in `<style>` and JS inlined in `<script>` — no external files.

Do NOT author the UI with placeholder / empty image `src` intending to "fill in later" — fetch first, then author.

### Iteration spec judgment (autonomous — Core Rules #7)
On re-entry (artifact already exists), judge the change:
- **Light edit** (color / copy / image swap) → edit the UI only; do NOT touch the spec / the design.
- **Heavy edit** (new style / layout / design system) → re-fetch the style spec (`curl -o` overwrite from
  the same or a new `<stem>.md`) + rewrite the design, then regenerate the UI.

Either way → `status→generated` (Core Rules #6).

### Asset policy — all external links, nothing local
- **CSS**: hand-write per the style spec's tokens (colors / typography / components / spacing) as `:root`
  CSS variables + structured rules, all inlined in `<style>` inside the UI. No CSS framework.
  The UI spec is **internalized into CSS variables** (tokens → `:root`).
- **Fonts**: Google Fonts via `<link>`. Map by **type**, NOT by the spec's font name — the fetched
  The style spec uses neutral fictitious names (e.g. `Brand Marketing Cereal VF`) that exist on no CDN.
  Translate the spec's *sans / serif / mono + weight* to reachable Google Fonts, then a system fallback:

  | spec type | Google Font (primary → alt → fallback) |
  |---|---|
  | sans | Inter → Manrope → system-ui |
  | serif | Playfair Display → Merriweather → Georgia |
  | mono | JetBrains Mono → Fira Code → monospace |

  **Weight map**: Thin 100 · Light 300 · Regular 400 · Medium 500 · SemiBold 600 · Bold 700 · Black 900.
  Always end the CSS `font-family` stack with the system fallback (e.g. `'Inter', system-ui, -apple-system, sans-serif`).
- **Icons**: Lucide via CDN — `<script src="https://unpkg.com/lucide@latest"></script>`, mark icons with
  `<i data-lucide="<name>"></i>`, then call `lucide.createIcons()` after DOM ready. (Pin a specific
  version like `lucide@0.460.0` instead of `@latest` if reproducibility matters.)
- **Images**: direct links via the skill script — see below.

### Images (MANDATORY, Core Rules #9)
Every image slot gets a real photo — fetch via the skill script BEFORE writing HTML (generation order step 2). Call it **once**, one `--block` per image group. The script path, full command, parameter format (incl. `primary`/`secondary` main+fallback), and output format are all in the **system prompt** — run it directly and fill `<img src>` from the `=== label ===` output.
**On repeated failure (both queries empty): drop that slot and render text-only — do not keep retrying or substitute placeholders. If ALL slots come back empty, stop and tell the user the image service is unavailable.**

### Persist + transition
- The UI artifact was already written in step 3 — no extra write needed.
- On completion: `ProjectSave(project_id=<id>, files={"meta.md": <full content>, "progress.md": <full>}, meta_snapshot={"status": "generated"})` (full overwrite; design.md unchanged since S2).
- Mark the UI build done in `TodoWrite`.
- **Then offer 2 next steps** (every generation): **preview** the UI · **iterate** (request changes). **Deployment (going live) is NOT a default suggestion** — proceed ONLY when the user explicitly asks, and ONLY after Hard Red Lines consent; at most a one-line nudge when they signal intent to publish, never push it. When it proceeds, use panel tools (`SiteCreate`/`RunCommand`); ensure every deployed file is owned `www:www` and mode `644` (directories `755`) — it does NOT exit the session, does NOT bind/track any address.

---

## Resume & Progress

- **The progress doc is the project's factual progress — the source of truth across sessions.** Every phase transition + iteration writes it (phase + iteration history). On re-entry, read it to know exactly where the project stands; it is authoritative — more precise than `status` alone.
- **Entry routing is the S0 route** (NEW vs ITERATE by project existence). On any re-entry — same session
  resumed or a fresh turn — re-run the S0 route: if the project exists, `Read` the project meta for `status` and follow
  the ITERATE branch (status tells you where to pick up).

---

## Output Format

Report to the user in plain natural language:

```
Style chosen: <name> — <tone>
Sections: <list>
Status: <draft | generated>
Artifact: the project UI (open to preview)
Next: preview · iterate (request changes)
```
