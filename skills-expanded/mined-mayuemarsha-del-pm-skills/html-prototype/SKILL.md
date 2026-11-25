---
name: html-prototype
description: Generate HTML prototypes (single-file, browser-openable) for product mockups using the user's design system — fonts, color scales, radii, shadows, components, all driven by a tokens.css file. Use when the user asks to make a 原型 / mockup / HTML 设计图 / 设计图给前端 for a PRD module, OR redesign an existing prototype. Output goes to the PRD module's `prototype/` subfolder.
---

1. # HTML Prototype Generation

   Generate single-file HTML prototypes that can be opened directly in browser, look like real products, and align with the user's design system.

   **Important**: this skill expects a `references/example-tokens.css` file with the user's design tokens (colors, fonts, radii, shadows, etc.). **Replace it with your own company's tokens before using this skill in production**, otherwise all prototypes will share the example brand colors.

2. ## When to use

   2.1. User asks for: 原型 / mockup / 设计图 / HTML 给前端 / 给前端看的页面。
   2.2. User asks to **redesign** an existing prototype to match a reference design.
   2.3. Output is referenced from PRD `.md` files via `file:///` link or `[name](prototype/foo.html)` markdown link.

3. ## Output location

   Always save to `<PRD-module>/prototype/<page-name>.html`, beside the PRD `.md` file. Create the `prototype/` subdirectory if missing.

   Naming: `<module>-<view>.html` (e.g. `agent-management.html`, `reception-detail.html`, `knowledge-list.html`). One file per module is preferred — use page-switching JS to handle multiple states (list / detail / modal). Multiple files only when modules are unrelated.

4. ## Tech stack (always these three CDNs, no build)

   ```html
   <script src="https://cdn.tailwindcss.com"></script>
   <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>
   <link href="https://fonts.googleapis.com/css2?family=YourFontHere:wght@400;500;600;700&display=swap" rel="stylesheet">
   ```

   After page load, call `lucide.createIcons()` to render icons.

5. ## Inline the canonical tokens file

   **Always** copy the full contents of [references/example-tokens.css](references/example-tokens.css) (or whatever the user has replaced it with) into the prototype's `<style>` block at the top. This gives you all CSS variables (`--neutral-*`, brand scales, semantic tokens, type, spacing, radii, shadows) plus baseline typography.

   Then layer prototype-specific component CSS *below* it, referencing tokens via `var(--token)` rather than hardcoded hex.

   Example skeleton:

   ```html
   <style>
     /* PASTE ENTIRE references/example-tokens.css HERE */
     :root { ... }
     html, body { font-family: var(--font-sans); ... }
     h1, h2, h3 ...

     /* Then prototype-specific components */
     .btn { background: var(--primary); color: var(--primary-foreground); border-radius: var(--radius-md); ... }
     .card { background: var(--card); border: var(--border-100) solid var(--border); border-radius: var(--radius-md); box-shadow: var(--shadow-sm); ... }
   </style>
   ```

6. ## Design System Application

   The actual color values, font names, radii, etc. live in `references/example-tokens.css`. This section is about **how to apply** them, not what the specific values are.

   6.1. **Fonts (order matters for CJK + Latin)**

   If the product supports Chinese, put CJK font FIRST so Chinese characters render natively while Latin characters fall through to the Latin sans:

   ```
   "PingFang SC", "Geist", "Inter", system-ui, -apple-system, sans-serif
   ```

   Don't reverse this order — Latin glyphs in PingFang look thin / weak. Adjust based on your tokens file.

   | Role | Typical family | When |
   |------|----------------|------|
   | Sans (default) | CJK + Latin sans | All UI, body, headings |
   | Mono | Monospace (e.g. B612 Mono / JetBrains Mono) | IDs, code, numbers in tables |
   | Serif | Optional display | Marketing / hero only |

   Body: 16px / 24px line-height (`--text-base / --lh-base`). Use `var(--text-sm)` (14/20) for compact UI like sidebars or table cells.

   6.2. **Tailwind CDN preflight conflict**

   Tailwind CDN injects `@layer base { h1, h2, h3, h4 { font-size: inherit; font-weight: inherit; } }` AFTER your `<style>` block. This kills semantic heading styles unless you use `!important` on the base typography rules:

   ```css
   h1,.h1 { font-size: var(--text-2xl) !important; ... }
   h2,.h2 { font-size: var(--text-xl) !important; ... }
   ```

   Without `!important`, your `<h1>` will render at body-text size and your design will look broken. Test by inspecting an `<h1>`'s computed font-size before declaring done.

   6.3. **In-app heading scale (compact, NOT marketing scale)**

   Marketing scales (h1=36px / h2=30px / h3=24px / h4=20px) are too big for in-app surfaces (list pages, detail pages, modals). Use a tighter scale:

   | Token | In-app size | Use for |
   |-------|------------|---------|
   | `h1` | `22px` bold | Page title |
   | `h2` | `18px` semibold | Tab content title |
   | `h3` | `15px` semibold | Section heading |
   | `h4` | `13px` semibold | Sub-section / form group label |

   Form controls (`.input` / `.btn`) keep their original heights and radii — only the inner text drops to 13px so the visual proportions don't collapse.

   For marketing / hero blocks, override locally with `text-4xl`, `text-5xl` etc.

   6.4. **Accent scales**

   Most tokens files define multiple accent scales. Typical mapping:

   | Scale | Use when |
   |-------|----------|
   | `--neutral-*` | 90% of UI: text, surfaces, borders |
   | `--secondary-*` | Brand callouts, hero CTA, primary illustrations (sparing) |
   | `--tertiary-*` | AI / agent contexts: algo info, AI suggestions, generation |
   | `--quaternary-*` | Supporting accent: data viz, secondary info, third option |

   Use the `-500` step as the canonical hue; `-50/100` for subtle bg fills; `-700+` for high-contrast text or pressed states.

   6.5. **Status colors**

   Each alert ships **paired** bg + fg tokens:

   ```css
   background: var(--success-bg); color: var(--success-fg); /* and warning / error / info */
   ```

   Don't mix bg of one with fg of another.

   6.6. **Radii**

   Use `--radius-md` for cards / buttons / inputs. Whatever value your tokens file picks (8px shadcn default, 24px round style, etc.), use it consistently — don't mix multiple radii arbitrarily.

   6.7. **Borders**

   Three weights via `--border-100` (1px) / `--border-200` (1.33px) / `--border-300` (2px). Default border color `var(--border)`, input `var(--input)`. Pair with `--shadow-sm`, never heavy drop-shadow.

   6.8. **Shadows**

   5-step layered (`--shadow-xs` → `--shadow-xl`). Each = ambient + projection. Use `--shadow-sm` for cards, `--shadow-lg` for popovers, `--shadow-xl` for modals.

   6.9. **Hover / press / focus**

   1. Solid button hover: stack `var(--opacity-90)` overlay — `box-shadow: inset 0 0 0 999px var(--opacity-90)`.
   2. Outline / ghost hover: swap to `var(--accent)`.
   3. Press: deepen one shade; no scale transform.
   4. Focus ring: `box-shadow: 0 0 0 3px color-mix(in srgb, var(--ring) 25%, transparent)`.

   6.10. **Animation**

   Fades and slides only. 150–200ms ease-out. No bounces. Loaders use Lucide `loader-2` self-spinning.

   6.11. **Icons**

   1. **Lucide only** via CDN.
   2. Stroke 1.5–2px.
   3. 16×16 inline in buttons, 24×24 standalone.
   4. **Never use Unicode characters or emoji as icons.** Reserve emoji for user-generated content.

7. ## Component patterns (battle-tested, all token-based)

   7.1. **Button**

   ```css
   .btn{display:inline-flex;align-items:center;gap:6px;padding:0 var(--space-4);height:36px;
        border-radius:var(--radius-md);font-size:var(--text-sm);font-weight:var(--weight-medium);
        cursor:pointer;transition:background .15s;border:var(--border-100) solid transparent}
   .btn-primary{background:var(--primary);color:var(--primary-foreground)}
   .btn-primary:hover{box-shadow:inset 0 0 0 999px var(--opacity-90)}
   .btn-brand{background:var(--secondary-500);color:#fff}
   .btn-brand:hover{box-shadow:inset 0 0 0 999px var(--opacity-90)}
   .btn-brand:active{background:var(--secondary-700)}
   .btn-ai{background:var(--tertiary-500);color:#fff}
   .btn-ai:hover{box-shadow:inset 0 0 0 999px var(--opacity-90)}
   .btn-outline{background:var(--background);border-color:var(--border);color:var(--foreground)}
   .btn-outline:hover{background:var(--accent)}
   .btn-ghost{color:var(--foreground);background:transparent}
   .btn-ghost:hover{background:var(--accent)}
   .btn-icon{width:36px;height:36px;padding:0;border-radius:var(--radius-md)}
   .btn-sm{height:32px;padding:0 var(--space-3);font-size:var(--text-sm)}
   .btn:focus-visible{outline:none;box-shadow:0 0 0 3px #6a728240}
   ```

   7.2. **Input**

   ```css
   .input{width:100%;padding:0 var(--space-4);height:40px;
          border:var(--border-200) solid var(--input);border-radius:var(--radius-md);
          font-size:var(--text-sm);background:var(--background);color:var(--foreground);
          transition:border-color .15s,box-shadow .15s}
   .input:focus{outline:none;border-color:var(--foreground);box-shadow:0 0 0 3px #6a728240}
   .input::placeholder{color:var(--neutral-400)}
   .textarea{min-height:96px;padding:var(--space-3) var(--space-4);line-height:1.6;
             border-radius:var(--radius-sm);resize:vertical}
   ```

   7.3. **Card**

   ```css
   .card{background:var(--card);border:var(--border-100) solid var(--border);
         border-radius:var(--radius-md);padding:var(--space-6);box-shadow:var(--shadow-sm)}
   ```

   7.4. **Badge (status pills)**

   ```css
   .badge{display:inline-flex;align-items:center;gap:4px;padding:2px var(--space-3);
          height:22px;border-radius:var(--radius-full);font-size:var(--text-xs);
          font-weight:var(--weight-medium);background:var(--neutral-50);color:var(--neutral-500);
          border:var(--border-100) solid var(--border)}
   .badge-success{background:var(--success-bg);color:var(--success-fg);border-color:transparent}
   .badge-warning{background:var(--warning-bg);color:var(--warning-fg);border-color:transparent}
   .badge-error  {background:var(--error-bg);  color:var(--error-fg);  border-color:transparent}
   .badge-info   {background:var(--info-bg);   color:var(--info-fg);   border-color:transparent}
   .badge-ai     {background:var(--tertiary-50);color:var(--tertiary-700);border-color:var(--tertiary-200)}
   .badge-brand  {background:var(--secondary-50);color:var(--secondary-700);border-color:var(--secondary-200)}
   ```

   7.5. **Status dot pattern**

   ```html
   <span class="badge badge-success"><span class="dot dot-success"></span>已发布</span>
   ```

   ```css
   .dot{width:6px;height:6px;border-radius:50%;display:inline-block}
   .dot-success{background:var(--success-fg)}
   .dot-warning{background:var(--warning-fg)}
   .dot-error  {background:var(--error-fg)}
   .dot-info   {background:var(--info-fg)}
   ```

   7.6. **Avatar (single neutral tone, never rainbow)**

   ```css
   .avatar{display:inline-flex;align-items:center;justify-content:center;
           background:var(--neutral-950);color:var(--background);
           font-weight:var(--weight-semibold);border-radius:var(--radius-sm)}
   .avatar-lg{width:52px;height:52px;font-size:var(--text-lg);border-radius:14px}
   .avatar-md{width:36px;height:36px;font-size:var(--text-sm);border-radius:var(--radius-sm)}
   .avatar-sm{width:24px;height:24px;font-size:var(--text-xs);border-radius:8px}
   ```

   7.7. **AI / Agent affordances (use tertiary scale)**

   When the UI is showing AI behavior — algorithm info panels, "AI suggested" labels, generation indicators, agent reasoning traces — use the tertiary scale:

   ```css
   .ai-panel{background:var(--tertiary-50);border:var(--border-100) solid var(--tertiary-200);
             border-radius:var(--radius-md);padding:var(--space-4)}
   .ai-label{color:var(--tertiary-700);font-size:var(--text-xs);font-weight:var(--weight-semibold)}
   ```

   Don't use the AI scale for non-AI things. Don't use the brand scale for AI things. Keep the semantic mapping crisp.

   7.8. **Help icon (ⓘ) tooltip — must be complete, never empty**

   任何指标 / 字段 / 配置项旁边的 ⓘ 帮助图标，**title 不能为空、不能只写零碎补充语**。每个 ⓘ tooltip 必须自包含、能让运营单独读懂这个指标。

   **必含内容（按优先级排序）**：

   1. **计算公式**（指标类必填）：`{指标名} = {分子} / {分母} × 100%`。
   2. **业务含义**（一句话说明这指标看什么 / 反映了什么问题）。
   3. **适用范围**（如有限制：`仅 XX 模式 适用`）。
   4. **特殊计数 / 守恒约束**（如有：`独立计数，N 项率相加可能 ≥ 100%` / `一个 X 只计 1 次`）。
   5. **环比方向**（如有：`上升为正向（绿色 ↑）` / `上升为负向（红色 ↑）——通常说明 XX`）。

   格式：每条用 `&#10;` 换行，HTML title 属性原生支持多行展示。

   **反例（信息残缺）**：

   ```html
   <i data-lucide="info" title="上升为负向"></i>           <!-- 缺公式、缺业务含义 -->
   <i data-lucide="info"></i>                              <!-- 完全空 -->
   <i data-lucide="info" title="仅 XX 模式"></i>           <!-- 只有适用范围 -->
   ```

   **正例**：

   ```html
   <i data-lucide="info" title="动作执行率 = 动作执行数 / 资源回答数 × 100%&#10;调用动作（含 MCP Tool 调用 + FC 调用两类）后调用大模型回答。&#10;仅 自主决策模式 适用。&#10;与其他细分维度独立计数，5 项率相加可能 ≥ 100%。&#10;上升为正向（绿色 ↑）——说明机器人在用工具补全信息。"></i>
   ```

   **自检清单**（生成原型后过一遍）：

   1. 每个 ⓘ 都有 title 属性？
   2. 每个 title 包含公式 + 业务含义 + 适用范围（如有）？
   3. 业务零碎补充语（如"上升为负向"）从未单独出现，必须配合公式同时给？
   4. 多行用 `&#10;` 而非 `\n` 或省略换行？

8. ## Color usage rules (HARD)

   **Hierarchy of accents**：

   1. **Neutral dark** — primary actions, current location / navigation, emphasis.
   2. **Brand secondary** — brand callout, hero CTA, illustration accents (use SPARINGLY).
   3. **AI tertiary** — AI-specific contexts (algorithm info, AI suggestions, agent reasoning).
   4. **Pastel semantic** — only for status (success / warning / error / info) badges and banners.
   5. **Neutral grays** — everything else.

   **What NOT to do**：

   1. ✗ Random multicolor avatars (blue / purple / green / orange) — use single dark tone.
   2. ✗ Type-coded badges in 4 colors (blue / purple / amber / green) — use neutral with one accent for primary status.
   3. ✗ Cream / beige for navigation active state — use the neutral dark.
   4. ✗ Cream / beige for status indicators — use neutral or pastel-semantic.
   5. ✗ Emoji as icons — Lucide only.
   6. ✗ Multiple shades of same hue competing for attention.

   **Selection state mapping**：

   | Context | Treatment |
   |---------|-----------|
   | Sidebar nav active | Light gray bg + dark text + medium font weight (shadcn sidebar style — see App shell) |
   | Tab switcher active | Neutral dark bg, white text (or white pill on muted track) |
   | Radio card selected | Light bg + dark border (only when user actively chose) |
   | Currently editing item | Subtle muted bg |
   | Reference / state indicator | Tiny gray icon + gray text, NOT colored badge |

9. ## Layout patterns

   9.1. **Full viewport (HARD rule, no max-width)**

   The page must always fill the entire viewport on any screen size. **Never** cap content width with `max-width` / `max-w-[Xpx]` — large screens (1920+) will look "small and lonely" with content centered and 400px of empty gray on each side.

   1. Root container: `width: 100vw; height: 100vh; padding: 32px`.
   2. Inside: `flex` row — sidebar fixed 240px, main `flex: 1` filling remainder.
   3. Main content vertically: `flex: 1` so it stretches the full viewport height.
   4. Tables / scrollable lists: `flex: 1` + `overflow-y: auto` — data overflows internally, never leaves bottom whitespace when data is sparse.

   9.2. **App shell (sidebar + main) — shadcn-style sidebar**

   The sidebar follows **shadcn/ui Sidebar visual spec** — a single flat list of menu buttons grouped under non-clickable text labels. **Replaces the old expand / collapse two-level nav; do not use `.nav-item` / `.nav-child` / `.nav-children` patterns anymore.**

   > **Why pure HTML + CSS rather than shadcn React components**: prototypes are single-file HTML opened in a browser, no React runtime. We replicate shadcn Sidebar's visual rules (colors, sizes, spacing, states) using plain CSS so the implementation team can swap in real `<Sidebar>` / `<SidebarMenuButton>` later.

   **Shell** (`.sb-shell`): width **240px** exactly, `flex-shrink: 0`, `display: flex; flex-direction: column`, font-size **13px** baseline. Background `#fafafa` (≈ `bg-sidebar` token). Right border `1px solid var(--border)`.

   **Header** (`.sb-header`): **64px** tall (matches the page topbar height so the two bottom borders align as a single line across the screen), `padding: 0 12px`, `gap: 10px`, `box-sizing: border-box`, bottom 1px border. Single row, **never two-line brand**.

   **Group label** (`.sb-group-label`) — pure text section header, **NOT clickable**, no icon, no chevron:

   1. 11px, font-weight 500, color `rgba(63,63,70,.6)` (≈ `text-sidebar-foreground/60`).
   2. `padding: 6px 8px`, `line-height: 1`.
   3. Sits above its `<ul class="sb-menu">`.
   4. ⚠️ **GroupLabel left padding MUST match MenuButton left padding (8px)** so the section header text and the icon column of menu buttons share the same left baseline.

   **Menu button** (`.sb-menu-btn`):

   1. Height 32px, `border-radius: 6px`, `padding: 0 8px`, `gap: 8px`.
   2. Lucide icon 16px (left), text 13px (middle, truncate), optional badge (right).
   3. Default: transparent bg, color `#3f3f46`, icon `#71717a`.
   4. Hover: bg `#f4f4f5`, color `#18181b`, icon `#18181b`.
   5. **Active: bg `var(--quaternary-50)`, text + icon `var(--quaternary-500)`, `font-weight: 500`** — NOT the gray hover bg. The active item reads as a soft brand-color affordance, not a hover holdover.

   **Sub-menu (third-level)** — for parents with grandchildren:

   1. `<li class="sb-menu-li">` wraps the parent MenuButton + the `<ul class="sb-menu-sub">`.
   2. Parent MenuButton ends with `<i class="sb-menu-caret" data-lucide="chevron-down">`; toggle by adding / removing `.collapsed` on the `.sb-menu-li`.
   3. `.sb-menu-sub`: `list-style: none; margin: 2px 0 2px 16px; border-left: 1px solid var(--border)`.
   4. **默认收起**：`<li class="sb-menu-li collapsed">` — 带子菜单的父项默认折叠，用户点击 chevron 才展开。

   **Footer** (`.sb-footer`): `padding: 8px`, top 1px border. Avatar 24×24 dark square + name (12px medium) + email (11px muted) + Lucide `chevrons-up-down` 14px caret. Hover bg `#f4f4f5`.

   9.3. **Dropdown menu**

   When a list row has more than two operations, the **first** operation stays inline as a ghost button; the **rest** collapse into a `more-horizontal` (⋮) icon button that opens a `.menu`. Required structure:

   ```html
   <div class="row-menu-wrap"><!-- position: relative -->
     <button class="btn btn-ghost btn-sm btn-icon" onclick="toggleRowMenu(this,event)">⋮</button>
     <div class="menu" style="right:0; top: calc(100% + 4px)">
       <div class="menu-item"><i data-lucide="copy"></i>复制</div>
       <div class="menu-item danger"><i data-lucide="trash-2"></i>删除</div>
     </div>
   </div>
   ```

   ```css
   .menu{position:absolute;background:var(--card);border:var(--border-100) solid var(--border);
         border-radius:var(--radius-sm);box-shadow:var(--shadow-lg);padding:4px;min-width:140px;
         z-index:50;display:none}
   .menu.open{display:block}
   .menu-item{display:flex;align-items:center;gap:8px;padding:7px 10px;border-radius:var(--radius-xs);
              font-size:14px;color:var(--foreground);cursor:pointer}
   .menu-item:hover{background:var(--accent)}
   .menu-item.danger{color:var(--error-fg)}
   .menu-item.danger:hover{background:var(--error-bg)}
   .menu-item .lucide{width:14px;height:14px;color:var(--neutral-500)}
   .menu-item.danger .lucide{color:var(--error-fg)}
   .menu-divider{height:1px;background:var(--border);margin:4px 0}
   ```

   Behavior: clicking ⋮ toggles `.open`; clicking outside closes it; only one menu open at a time. Don't fall back to "show all 3 buttons inline" — that's the legacy pattern.

   9.4. **Detail page (left tabs + main + floating debug)**

   When the page is a config / editor:

   1. Top bar: back link + avatar + title + status badge + ID + "last saved" line + actions (right).
   2. Left sub-sidebar: vertical tabs + 发布检查 / checklist panel below.
   3. Main: content area fills remaining width (no max-width), 32px padding.
   4. Right-side debug panel: per requirements doc; if user wants persistent, dock right-side; else FAB + drawer.

   9.5. **List page**

   1. H1 + subtitle (bigger entry feel).
   2. Tab filter row with counts: `全部 8 / 已发布 5 / 草稿 3`.
   3. Search + filter row (no sort dropdown unless explicitly required).
   4. Table fills full width of main area, no card wrapper — table border + header bg already provides visual containment.
   5. Hover row: subtle muted bg.

   9.6. **Table component (fixed spec, NOT tokens)**

   These are designer hard values — **do not** substitute with tokens like `var(--space-3)`. Use the literal px:

   | Element | Value |
   |---|---|
   | Header height | `40px` |
   | Header background | `#F9FAFB` |
   | Header bottom border | `1px solid #F3F4F6` |
   | Header corner radius | matches `--radius-md` (top-left + top-right of first / last `<th>`) |
   | Header text | `text-xs` (12px), `var(--muted-foreground)`, `font-weight: 500` |
   | Row height | `72px` (generous, not cramped) |
   | Row separator | `1px solid #F3F4F6` |
   | Row text color | `var(--foreground)` |
   | Status badge | height `20px`, radius `--radius-md`, padding `2px 8px`, font `12px`; bg = pastel by category, no border |
   | Action column buttons | All Ghost style (`btn-ghost`), no outline borders. **Left-aligned** (see Action column alignment section). Wrap multiple buttons in `inline-flex gap-1` |
   | Action column icon size | `16px` |

   9.7. **Modal**

   1. Width 480–560px, `border-radius` matches `--radius-lg` (large), `shadow-xl`.
   2. Header (title + small description) → body → footer (right-aligned actions).

10. ## Copy / voice rules

    10.1. **Sentence case** for everything except proper nouns / TitleCase identifiers.
    10.2. **"You"** addresses user directly; never "we" / "our" / "let's".
    10.3. **English first**, CN secondary; both at same font size (for products with mixed audience).
    10.4. **Two sentences max** for descriptions: define → "Use ..." imperative.
    10.5. **No emoji in chrome** (labels, buttons, nav). Reserve for user-generated content.
    10.6. **No internal-rule annotations leaking into the UI**. The prototype is a product view, not a PRD spec sheet. Any line that describes *why a behavior is designed this way* belongs in the PRD doc, NOT in a `.sub` subtitle, `.hint`, or trailing `.muted small` note. Heuristic: if you can lift the sentence verbatim into the PRD's 操作逻辑 section and it reads naturally, it doesn't belong in the prototype. Hints / banners are only for *operator-facing* in-task guidance.

11. ## Generation workflow

    11.1. **Read the PRD first**. Look for "原型示意" sections, field lists, operation logic. Don't invent fields not in the PRD.
    11.2. **Plan pages / states** — list / detail / modal / specific tab states. One HTML file with page-switch JS unless the user asks otherwise.
    11.3. **Reuse the existing prototype style** if there's already one in the same module's `prototype/` folder. Don't invent a third style.
    11.4. **Brief the user** on what's covered before generating: pages, states, design choices.
    11.5. **Generate single-file HTML** with all CSS inline, all JS inline.
    11.6. **Open in browser** with `open <path>` on macOS so the user can see it immediately.
    11.7. **Self-verify before reporting done** — this is mandatory, not optional:
        1. **PRD coverage**: walk the PRD's 功能清单 line by line; every listed feature must have a matching entry-point in the prototype (page / button / modal). List ✓ / ✗ in the summary.
        2. **Every clickable is wired**: every `<button>`, `onclick=`, nav-item, action-column link, dropdown menu item, tab, checkbox group must trigger something — open a modal, switch a page, swap state, or at minimum a `toast()` placeholder. No dead `onclick=""` or visual-only buttons that look interactive but do nothing.
        3. **Click behavior matches PRD**: cross-check that what happens on click matches the PRD's "操作逻辑" — second-confirmation copy, error message text, modal that opens, follow-up state, etc.
        4. When you find gaps, fix them **before** writing the summary. Don't surface the gaps in the summary as TODOs and stop.
    11.8. **End with a short summary**: pages covered, design choices, what's still open.

12. ## Iteration etiquette

    When the user says "ugly" / "weird color" / "the active state is wrong":

    1. Don't defend. Identify the specific element.
    2. Reference the **color usage rules** above to decide the right replacement.
    3. Tell them what changed and why (one or two lines, not paragraphs).
    4. Avoid full rewrites — surgical edits via Edit tool.

    When they share a reference screenshot:

    1. Look at: spacing density, radii, color usage, font weight, icon style.
    2. Don't blindly copy the reference's color palette if it conflicts with your tokens (the prototype is your product, not the reference brand).
    3. Adopt: layout patterns, component shapes, hierarchy. NOT necessarily color.

13. ## Interactivity (HARD)

    **Every visually-clickable element must actually be clickable.** Dead visual elements (a styled button with no `onclick`) feel broken and undermine the prototype's credibility.

    Rules:

    13.1. **Buttons** (`.btn`, `.btn-icon`, `.btn-ghost`, `.btn-outline`, etc.): always have `onclick`. Use `onclick="toast('...')"` as a placeholder if the destination doesn't exist yet.
    13.2. **Table rows with `cursor-pointer`**: always have `onclick="openX(...)"` on the `<tr>`; secondary buttons inside the row need `onclick="event.stopPropagation()"` on their wrapping `<td>` (or per-button) so the row click doesn't fire when clicking a sub-action.
    13.3. **Dropdown items, menu links, chips, tabs, segmented controls**: always have `onclick`. A purely decorative chip should not look like a button (no hover, no cursor change).
    13.4. **Icons used as actions** (e.g., `<i data-lucide="more-horizontal">` inside a `.btn`): the parent button takes the `onclick`, not the `<i>` itself.
    13.5. **Toggles / switches / checkboxes**: at minimum, `onclick="this.classList.toggle('on')"` so the visual state changes.
    13.6. **Avatar / link / hover-able cards**: if hover styling implies it's clickable, give it `onclick`; if it isn't clickable, drop the hover styling.
    13.7. **Tab filters in a list**: clicking should at minimum re-render the list count or toggle visible rows; never leave them as static.
    13.8. **Modal triggers** (open / close / cancel / confirm): all four states must work — open, close (×), cancel button, confirm button. Confirm should at least show a `toast` and close.

    Self-check before declaring a prototype ready:

    1. Click every button at least once. Each one must do *something* (navigate, open modal, toggle state, or show toast).
    2. Click every table row in the list. Should open the detail view.
    3. Open every modal and try every button inside it (close, cancel, primary action).
    4. Open every dropdown and click each item.
    5. If using `cursor-pointer` class anywhere, that element must have `onclick`.

14. ## List rules — apply to EVERY list-style table

    Mandatory checklist whenever you create or modify a list:

    14.1. **Container**: `.table-wrap` (`overflow: auto` + border + `--radius-md`) — never wrap a list table in a generic `<div class="border rounded">` that lacks horizontal scroll.
    14.2. **Per-column `min-width`** inline on each `<th>` — never hardcode a table-wide min-width.
    14.3. **First column `.sticky-l`, action column `.sticky-r`**: applied on `<th>` in thead and on every `<td>` in tbody.
    14.4. **Pagination** → always the shadcn Data Table style Detailed Pagination: `已选 X / Y 行` (left) + `每页 [select]` + `第 N / M 页` + 4 round icon buttons `«‹›»` (right). Round buttons, not square. Always include the rows-per-page selector. Never just `共 N 条` text. No variants across the product.
    14.5. **Action column = LEFT-aligned**, not right-aligned. With `.sticky-r` it already hugs the right edge; left-aligning the cell content keeps the operation buttons close to the column header.
    14.6. **Search input** above the table = `.input-search` (36px), not the global 40px `.input`.
    14.7. **Hover state** on sticky cells must re-apply `--neutral-50`, see Responsive table pitfalls.
    14.8. **Filter tabs** (e.g. 全部 / 已发布 / 草稿) = `.cfg-tab-h` inside `.cfg-tabs` — the **same** shadcn segmented control used on detail-page top tabs. Do NOT use the underline-style `.tab-filter`.

    If any list violates one of these, treat it as a bug — fix even when the user only asked about something else.

15. ## List page chrome (search + pagination)

    15.1. **Search input — list page filter row**

    The list-page search input is **36px tall** with a 1px border (lighter than the global 40px `.input`). Reason: shadcn "With Icon" input scale; full-height 40px feels too dense in a filter row.

    ```css
    .input-search { height: 36px; border-width: 1px; border-color: #D1D5DC }
    ```

    Use as `<input class="input input-search pl-10">` with a left-positioned Lucide search icon. Don't override `.input` globally.

    15.2. **Detailed Pagination (shadcn Data Table style)**

    Three-block footer with the canonical shadcn data-table layout:

    1. **Left**: `已选 <strong>X</strong> / <strong>Y</strong> 行` — text-sm muted; X/Y in mono font medium weight.
    2. **Right cluster** (flex, gap 24px):
        1. `每页` label + `<select class="pgn-select">` (10 / 20 / 50 / 100), 32px tall, mono font, custom chevron-down arrow.
        2. `第 <strong>N</strong> / <strong>M</strong> 页` — text-sm, mono font on N/M.
        3. 4 round 32×32 icon buttons in a row (gap 4px): `chevrons-left` / `chevron-left` / `chevron-right` / `chevrons-right`, `border-radius: var(--radius-full)`, 1px border, ghost when enabled, neutral-300 when disabled.

    ```html
    <div class="pagination">
      <div class="pagination-meta">已选 <strong>0</strong> / <strong>8</strong> 行</div>
      <div class="pagination-ctrl">
        <div class="pagination-rows">
          <span>每页</span>
          <select class="pgn-select"><option>10</option><option>20</option><option>50</option><option>100</option></select>
        </div>
        <div class="pagination-page">第 <strong>1</strong> / <strong>1</strong> 页</div>
        <div class="pagination-nav">
          <button class="pgn-icon" disabled><i data-lucide="chevrons-left"></i></button>
          <button class="pgn-icon" disabled><i data-lucide="chevron-left"></i></button>
          <button class="pgn-icon" disabled><i data-lucide="chevron-right"></i></button>
          <button class="pgn-icon" disabled><i data-lucide="chevrons-right"></i></button>
        </div>
      </div>
    </div>
    ```

    ⛔ **Don't** use simpler patterns instead:

    1. ❌ `共 N 条` text only (no controls).
    2. ❌ prev / number / next buttons without rows-per-page selector.
    3. ❌ square buttons or pill buttons — must be **round** (`--radius-full`) icon-only.

16. ## Top segmented tabs (in-page Tabs replacement)

    Use shadcn segmented tabs (`.cfg-tabs` + `.cfg-tab-h`) for **two scenarios** — they share the exact same control:

    16.1. **Detail-page top tabs**. Replaces left-side vertical tab columns when the page has a heavy toolbar (debug / publish-check / save / publish), which would otherwise create a three-column layout that crushes main content below 600px on 1280 viewports.
    16.2. **List-page filter tabs** (全部 / 已发布 / 草稿 above a list, etc.). Replaces the older underline-style `.tab-filter` — keeps filter UI consistent with detail-page tabs across the product.

    ```css
    .cfg-tabs-bar { padding: 14px 32px; background: var(--card); border-bottom: 1px solid var(--border) }
    .cfg-tabs     { display: inline-flex; gap: 2px; background: #F3F4F6; border-radius: var(--radius-sm); padding: 4px }
    .cfg-tab-h    { height: 32px; padding: 6px 14px; gap: 6px; border-radius: 8px;
                    font-size: var(--text-sm); color: var(--neutral-600); font-weight: 500;
                    background: transparent; border: none; cursor: pointer }
    .cfg-tab-h.active { background: #FFFFFF; color: var(--foreground); box-shadow: var(--shadow-xs) }
    .cfg-tab-h:hover:not(.active) { color: var(--foreground) }
    .cfg-tab-h .lucide { width: 14px; height: 14px }
    ```

17. ## Responsive table with sticky columns (HARD rules)

    For list pages where the table can overflow horizontally (typically when viewport drops below ~1200px), enable horizontal scroll with sticky first / last columns. Do **not** hardcode a fixed table min-width.

    ```css
    .table-wrap            { position: relative; overflow: auto;
                             border-radius: var(--radius-md);
                             background: var(--card);
                             border: 1px solid var(--border) }
    .table-wrap .table     { min-width: max-content }
    .table .sticky-l       { position: sticky; left: 0;  z-index: 1 }
    .table .sticky-r       { position: sticky; right: 0; z-index: 1 }
    .table thead .sticky-l,
    .table thead .sticky-r { z-index: 3; background: #F9FAFB }
    .table tbody td.sticky-l,
    .table tbody td.sticky-r        { z-index: 2; background: var(--card) }
    .table tbody tr:hover td.sticky-l,
    .table tbody tr:hover td.sticky-r { background: var(--neutral-50) }
    .table-wrap.scrolled-left  .sticky-l { box-shadow:  4px 0 6px -2px rgba(0,0,0,0.05) }
    .table-wrap.scrolled-right .sticky-r { box-shadow: -4px 0 6px -2px rgba(0,0,0,0.05) }
    ```

    JS — toggle shadow classes only when actually scrolled:

    ```js
    function refreshTableShadow(wrap){
      const sl = wrap.scrollLeft, sw = wrap.scrollWidth, cw = wrap.clientWidth;
      wrap.classList.toggle('scrolled-left',  sl > 0);
      wrap.classList.toggle('scrolled-right', sl + cw < sw - 1);
    }
    window.addEventListener('load',   () => document.querySelectorAll('.table-wrap').forEach(w => { refreshTableShadow(w); w.addEventListener('scroll', () => refreshTableShadow(w)); }));
    window.addEventListener('resize', () => document.querySelectorAll('.table-wrap').forEach(refreshTableShadow));
    ```

    ⚠️ Critical pitfalls:

    1. **Sticky cells without opaque bg** → scrolling content shows through, looks like rendering bug.
    2. **Thead sticky z-index ≤ tbody sticky z-index** → tbody covers header on scroll.
    3. **Forgetting `tr:hover td.sticky-*` rule** → sticky cells stay white while the rest of the row tints, splitting the row visually.
    4. **Always-on shadows** → users see fake "two columns" with no actual scroll happening; toggle via JS scroll/resize listeners.
    5. **JS-positioned columns instead of `position: sticky`** → slow, broken on async row updates, fights row hover.

    17.1. **Action column alignment (left-align, not right)**

    The action column header **and** the buttons inside cells are both left-aligned — column header sits flush with the column's left padding edge, and operation buttons sit underneath, vertically aligned to that same edge.

    Three rules:

    1. ⛔ **Don't** add `text-right pr-3` / `pr-5` to the action `<th>` / `<td>` — that pushes content to the right edge, which then no longer aligns with the column header.
    2. ⛔ **Don't** wrap action buttons in `<div class="inline-flex justify-end">` — `justify-end` defeats left alignment.
    3. ✅ **Do** offset the first action button by `margin-left:calc(-1 * var(--space-3))`. Reason: `.btn-sm` has 12px horizontal padding, so the button's text starts 12px inside its border. The negative margin pulls the button left so its text lines up with the column header text, not its border.

18. ## Right-side drawer (publish-check / verification panel)

    When a config page has a long, tab-grouped verification list (publish check, lint, dependency check, etc.), don't pin it to the left rail — it grows unboundedly with new check items and competes with config tabs. Use a right-side drawer triggered from the toolbar.

    1. **Trigger**: outline button in page-header right cluster, with `check-circle-2` icon + label. If unresolved warnings exist, attach a small absolute-positioned badge (top: -5px right: -5px) with `--warning-fg` bg, white text, 16px round, count number, font-weight bold.
    2. **Drawer**: 420px wide, slides in from right (`transform: translateX(100%)` → `0`), `--shadow-xl`, white bg, left border. z-index above main page content but below modals.
    3. **Drawer body**: group rows by config tab. Each group has small uppercase label header (`text-xs muted, letter-spacing 0.05em`) followed by rows.
    4. **Each row**: status icon (success `check`, warn `alert-circle`, fail `x-circle` — colored via `--success-fg` / `--warning-fg` / `--error-fg`) + label + right `chevron-right` arrow. Row has 1px border, `--radius-sm`, hover gets `--accent` bg. Click closes the drawer + switches to the corresponding config tab + scrolls/highlights the section.

19. ## 弹窗放页面里，不做浮层

    **所有"弹窗"都嵌入到页面布局里，不要做成 position: fixed + 半透明遮罩的中央浮层**。

    **为什么**：

    1. 浮层挡住主内容，用户失去上下文（看不到自己刚才在哪里、改了什么）。
    2. 多步操作场景下，浮层之间切换更打乱注意力。
    3. 嵌入式更接近"工作流就是页面本身"的设计哲学。

    **改造思路**：

    1. 触发"弹窗"的入口（按钮 / 链接）原地展开成内嵌区块（accordion 风格），或推到右侧 Panel 作为新 tab。
    2. CSS 上：去掉 `position: fixed` + `modal-mask` 遮罩；用 `border + radius + shadow` 在页面里圈出区域。
    3. 关闭按钮 → 折叠回去 / 关闭 tab，不是"取消模态"。
    4. 如果一定需要打断当前流程的强提示（如"删除二次确认"这种破坏性操作），用底部 toast / inline confirm bar 而不是浮层。

    **Anti-patterns**：

    1. ❌ `<div class="modal-mask"><div class="modal">...</div></div>` 中央浮层 + 遮罩。
    2. ❌ 把"打开新建数据集"做成 modal，把"添加用例"做成 modal，把"提交"做成 modal——一连串浮层互相叠。
    3. ❌ 简单的"确认 / 取消"也做成 modal——用 inline confirm。

    **例外**（可保留浮层）：

    1. `mention-popup`（@提及候选列表）—— 依附在输入位置的轻量级浮层 OK。
    2. `tooltip`（悬停提示）—— 本来就是浮层。
    3. 文件上传系统调起的原生文件选择器 —— 浏览器自带，无法控制。

20. ## Anti-patterns (learned from past iterations)

    20.1. ❌ Multiple gradient avatar colors (blue / purple / green / orange / pink / indigo) — "rainbow" avatars look amateurish.
    20.2. ❌ Cream / yellow active state on a multi-language tab switcher — too emphatic for navigation.
    20.3. ❌ Cream badge for "已引用" status — competes with main content; use tiny gray icon + text.
    20.4. ❌ Generic 6–8px border radius when your tokens dictate otherwise — follow your `--radius-md`.
    20.5. ❌ Putting `<h1>` without `!important` — Tailwind CDN preflight kills semantic heading styles. Either use `!important` or class-based `.h1`.
    20.6. ❌ Using full marketing scale (h1 = 36px) for in-app pages — feels comically large. Use the in-app heading scale above.
    20.7. ❌ Showing entity ID as a separate column in a list table — prefer compact format: ID in mono font under the entity name (saves a column).
    20.8. ❌ Showing operator name in a separate column from update time — combine: large date + small "由 X 更新" caption underneath.
    20.9. ❌ Gray bg on sub-sidebars / panels (`var(--neutral-50)` etc.) when spec says **pure white default** — separate via `border-right` only. Gray fills are reserved for hover / secondary buttons.
    20.10. ❌ `font-family: var(--font-mono)` on text containing CJK — most mono fonts have no Chinese glyphs; CJK falls back but keeps mono spacing → looks broken. Apply `<code>` only to the actual numeric / ID / date span, not the surrounding sentence.
    20.11. ❌ Tab filter row using `flex items-center` together with parent `border-b` — tab bottom border lands at row middle while parent border sits at row bottom, creating two parallel lines. Use `flex items-end`.
    20.12. ❌ Mixing `btn-sm` (32px) with default `btn-icon` (36px) in a row — heights don't match. Use `btn-sm.btn-icon` (32×32) when paired with `btn-sm`.
    20.13. ❌ Sidebar header height set by padding + content (variable), while topbar uses fixed `h-16` (64px) — borders end up 1–2px apart. Always set the sidebar header to an **explicit height matching the topbar**.
