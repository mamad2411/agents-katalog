---
name: summer-checkin-ui-skill
description: Audit, diagnose, and optimize the visual and interaction layer of existing web UIs without touching app logic. Use when Codex needs to fix messy or generic interfaces, elevate visual hierarchy and density, establish or repair a design-token system, or polish controls, spacing, typography, and responsive behavior. Applies to light and dark themes and to new or existing Next.js/React/Tailwind UIs; covers only visual/UX quality, never business logic, data, or backend work.
---

# UI Optimization Skill

## What This Skill Does

Make the interface better, not different. Improve how an existing product reads, scans, and
responds: visual hierarchy, density, consistency, contrast, affordance, spacing, responsive
behavior, and interaction polish. Keep the product and feature set unchanged.

The skill has two layers:

1. **The optimization process** (this file). A repeatable method to diagnose and improve any web
   UI, in light or dark themes, against a stable set of quality checks.
2. **A reference visual language** (`references/design-system.md`). A concrete dark glassy style —
   the scene tokens, surface/lighting 「质感」 recipes, and a full motion palette, distilled from
   the product's canonical spec page. Read it only when you decide to apply that treatment.

## Scope

- **In scope**: layout and spacing, visual hierarchy, color/contrast, typography, controls and
  states, responsive behavior, consistency, and motion polish.
- **Out of scope**: app functionality, data models, API wiring, business rules, routing, or
  feature work. Preserve the existing behavior exactly.

## Workflow

Follow this order. Do not jump straight to styling.

### 0. Entry decision — settle the target look, then work

Settle the *target look* with the user before anything else; it decides the lane and what to
replicate. Ask once, up front, and never re-ask.

**Look question（视觉工作每次先问，一次问完）.**
- **优化已有 UI** — offer the user exactly three options:
  1. **rain / snow / cloud** — 整体换成所选场景的 Summer Checkin UI；
  2. **自定义主色** — the user names one accent / brand color; derive the full token set from it;
  3. **只在原风格内修** — keep its own look and fix within its own tokens/patterns.
- **生成新页（in this language）** — this is Q1 below（rain / snow / cloud / 自定义主色）；没有
  "保持原风格"这一档。

**选了任一场景或自定义主色 → 整体颠覆为 Summer Checkin UI（不是局部微调）。**
The whole target surface is rebuilt in the chosen scene — hierarchy, layout, every control —
**in the style of the real Summer Checkin product, which is distilled and embedded in this skill**
(`references/design-system.md` §1–§10; buttons §7, signature motion §6, product-page shells §9,
device showcase §10). Apply that spec
directly and **replicate its button types & sizes, button hover · press · focus effects, and its
animations & micro-motions** onto the target — **self-contained, no other project required**. If a
folder matching the canonical product happens to exist on the current machine, you *may* consult it
for reference, but never depend on it; the embedded spec is the authority.

**质感 lane（§3 Glass vs §3.b Hard-solid）—— 基于用户语言自动切换，不要默认玻璃。**
只要用户原话出现任何一种"反光/反渐变"信号词（色不纯、荧光丑、渐变不要、实打实主
题色、界限分明、实心、不要发光、像 xxx 按钮那样），**不要走默认 5 层玻璃质感**，直接切
换到 `references/design-system.md` **§3.b Hard-solid**：纯色底、1.5px 粗实边、全局
`box-shadow:none`、徽章永远主色实心底。这是 2026-09 沉淀（L1）。不要只改半套，一
定整页贯彻。

**只在原风格内修（audit lane）.**
Keep the product's own tokens/patterns and scope to the surface the user named; no scene swap, no
new theme, no photography. If an imagery slot genuinely needs a photograph, you may ask one separate
yes/no about searching the web — **default no** — and never place a source/credit label on the page.

**Ask Q1 + Q2 together, once, only when the Summer Checkin look is being applied** — a chosen scene or
custom color above, or a page generated in this language. Stop before producing output and settle:
**Q1 theme palette**, then **Q2 image-sourcing consent**. Each is specified below.

- Presets — the three full 16-token scenes in `references/design-system.md` §1:
  - `rain` 雨林·深绿 — 柠檬绿强调（推荐默认）
  - `snow` 雪境·冷调蓝白
  - `cloud` 云端·暖灰夜色
- **自定义主色** — the user names one accent / brand color; derive a full token set from it per the
  custom-derivation rule in `references/design-system.md` §1. Only the color family changes; the
  「质感」 lighting/surface recipes and the motion palette stay identical.

**Q2 · 联网找图许可.** Ask whether you may fetch photos from the web for this page — **default is
"no search", and offer it sparingly**. State plainly what "yes" means: the page may hotlink a
photograph and needs a working network to render it. The bundled language gives each page **one**
photograph, fixed behind the whole page (`references/design-system.md` §2) — a single full-bleed
backdrop that the opening copy and the closing CTA both sit over; every picture↔page transition is
a dark gradient (暗过渡), never a bright seam.

- **不搜图（默认，优先）** — the page runs on the user's own images if any are supplied, or on §2's
  built-in no-photo fallback (layered gradients + hairlines + oversized numeral/wordmark). No
  network; fully self-contained. **No source/credit label ever appears on the page.** Material-only
  fallback is rendered **without the 暗过渡 veil** — no photo ⇒ no veil (§2), so the base stays
  bright instead of dimmed for nothing.
- **允许联网找图（用户明确要大气的照片时才用）** — pull only from sources with clean terms that need
  **no on-page attribution**: Wikimedia **CC0 / public domain** files, or images the user owns.
  Every photo must fit the chosen scene's 意境. The page still shows **no source/credit label
  anywhere** — if a CC BY / CC BY-SA file is the only good fit, keep its author + license **only in
  an HTML comment**, never rendered. Never use copyrighted fan-art, watermarked stock, or random
  search hits as a background.
- Treat "must stay offline / fully self-contained" as "不搜图".
- **目标是 App / 产品界面展示页（手机格子、以屏为内容）时**：内容主体是屏内界面本身，§2 的整页固定摄影
  背板不适用——Q2 即"不搜图"，改走 §10 的设备陈列版式（产品屏幕当 set-piece，无需外部照片素材）。

Rules for the two asks:

- Present the three presets by name *and* hue so the question is meaningful; offer custom (and, when
  optimizing an existing UI, "只在原风格内修") as further options; recommend `rain` only when the
  user is already set on applying the language and has no preference.
- Ask Q1 then Q2 together, exactly once, up front. Never re-ask mid-flow, and never add palette
  pickers, image pickers, tuning panels, or a light mode to the page as a substitute for this
  pre-flight choice.
- If the user says "you decide" or gives nothing: generating → theme `rain`, Q2 → 不搜图（不联网）;
  optimizing an existing UI → 只在原风格内修（除非用户原话已表明要 Summer Checkin 风，则 `rain`）. Proceed;
  do not re-ask.
- When the user supplies a custom color, take it as the accent and build the derived token set — do
  not quietly fall back to `rain`.

When you apply the bundled language, treat `references/design-system.md` as the spec: component
classes read the 16 `--theme-*` tokens only, and the 「质感」 lighting/surface recipes plus the
motion palette are part of the finish — not optional garnish. Applying it means the full treatment,
never just a recolor — and component/button/motion fidelity stays anchored on the real product
(see §0).

### 1. Understand the product

Identify the domain and audience before anything else.

- Is this a work tool (SaaS, CRM, admin, dashboard) or a consumer/expressive product? Work tools
  read quiet, utilitarian, and dense; consumer and game surfaces can be more expressive.
- Read the existing code to learn the framework, styling approach, and what tokens exist
  (Tailwind semantics, CSS variables, or an existing design system).
- Note the primary user flows: what does a user do most? Optimize that path first.

### 2. Audit against quality checks

Open the app and capture real rendered output. Walk the primary flows on desktop and mobile.
Record concrete defects, not vague impressions. Use these checks:

#### Layout and structure
- Page sections are full-width bands or unframed layouts with constrained inner content. Avoid
  wrapping every section as a floating card, and never nest a card inside a card.
- Cards appear only for repeated items, modals, or genuinely framed tools (a chat bubble, a
  metric, an item row).
- `min-w-0`, `flex-1`, aspect-constrained tiles, and responsive grids are in place so flex
  children shrink instead of overflowing.
- Fixed-format elements (buttons, chips, tiles, counters) have stable dimensions so labels,
  hover states, and counters cannot resize or shift layout.

#### Hierarchy and density
- One clear primary action per view. Secondary actions are visually subordinate.
- Headings, body, and muted labels are distinct; not everything is the same weight and size.
- Dense but scannable. No oversized hero sections, no decorative card stacks, and no hero copy
  trapped inside a card.

#### Typography
- Use the existing type scale; dense panels at `text-xs`-`text-sm`, hero scale reserved for true
  heroes. Never scale font-size with viewport width. Keep letter-spacing at `0`.
- Long labels truncate or clamp, with a themed tooltip showing the full value.
- Text always fits its container. Wrap or dynamically size the longest word; nothing clips,
  overflows, or overlaps sibling content.

#### Color and contrast
- Not one-note. Avoid interfaces dominated by a single hue family, and avoid dominant
  purple/purple-blue gradients, beige/cream/sand/tan, dark blue/slate, or brown/orange/espresso
  palettes.
- One dominant accent, used sparingly. Never make the whole page one accent color.
- Maintain readable contrast for body and muted text. Prefer CSS variables or semantic tokens over
  raw hex.
- Text over photography (the fixed backdrop's seating zones, set-pieces) sits in a dark veil/scrim
  zone or on a glass surface — never on busy midtones of the photo, and the backdrop only meets the
  page through darkness.

#### Controls and affordance
- Use icons in buttons for tools and clear commands; add tooltips that name unfamiliar icons.
  Icon buttons expose `aria-label` plus a themed tooltip, not a native `title`.
- Match control to intent: segmented controls for modes, toggles/checkboxes for binary settings,
  sliders/steppers for numeric values, menus for option sets, tabs for views.
- Every interactive element has visible hover, focus-visible, active, and disabled states.
  Suspense, empty, and error states are present and intentional.

#### Motion and polish
- Full state battery on every control: 150-200ms hover, focus-visible ring in the accent, an
  `:active` press scale (~0.97), and intentional disabled/empty/error states.
- Content reveals on scroll with a 650ms fade+rise and staggered `--d` delays; nothing stays
  permanently hidden if the observer or reduced-motion guard is absent.
- Scene/theme changes cross-fade the whole page (~380ms, `cubic-bezier(.4,0,.2,1)`) by animating
  color-family properties only, so layout never animates.
- No gradient orbs, bokeh blobs, or decorative animated decorations. Radial *lighting* washes and a
  single ambient float on one hero object are allowed; gratuitous looping is not.
- Film-grain/noise overlays, if used, sit at ≤ ~4% opacity: texture, not dirt.
- Every page honors `prefers-reduced-motion`: transitions collapse to ~0 and reveal fires instantly.
- On touch, secondary actions stay reachable even without hover.

### 3. Prioritize the fixes

Rank by impact and blast radius:

1. Broken layout, overflow, overlap, and accessibility problems first (contrast, labels, focus,
   tap targets).
2. Structural consistency and typography/hierarchy problems that make the primary task harder.
3. Controls, states, and interaction polish.
4. Only after the above is solid, refine color and any hero composition if the product needs it.

Prefer a smaller set of high-impact changes over wide cosmetic churn. Skip unrelated refactors.

### 4. Implement — per the lane chosen in §0

**只在原风格内修（audit）** — Extend the product's existing token and component patterns rather than
inventing a new style. Map colors and surfaces to the semantic layer the app already uses (Tailwind
`border-border`, `bg-foreground/[0.06]`, `bg-primary`, `text-primary-foreground`, CSS
`--surface-*`), use `cn()` / `tailwind-merge`, keep fixed geometry stable, and fix within the
product's own language. Do not force a new theme.

**选了场景 / 自定义主色（整页颠覆为 Summer Checkin）** — apply the language fully from
`references/design-system.md` (self-contained — buttons §7, signature motion §6, product-page
shells §9, device showcase §10) so the target's
buttons and motion match the Summer Checkin product. Applying it means the full finish — the
surface/lighting recipes **and** the motion palette (button hover/press/focus, reveal stagger,
theme cross-fade, reduced-motion fallback) **and** product-fidelity buttons — never just a color
swap.

### 5. Verify before finishing

- Render the app and capture desktop and mobile screenshots. Confirm they are non-blank, correctly
  framed, and not overlapping.
- Check text fit at every viewport; fix any clipping or overlap with wrapping or dynamic sizing.
- Click through the primary flows on desktop and mobile, including hover, focus, empty, disabled,
  and error states.
- Confirm controls do not shift layout and buttons/levels of hierarchy remain stable.
- Re-check the primary flows under `prefers-reduced-motion: reduce`: everything reveals instantly,
  nothing is permanently hidden, and no reveal/float animation runs.
- Confirm scene/theme switching cross-fades smoothly and reveal/tooltip/press micro-interactions
  fire without JS errors.
- **（§2.1 & L7 沉淀）热链图 / 背景图交付核查。**
  - **200ms 首帧**：Ctrl+F5 硬刷新后 200ms 内，backdrop 已出画面（不是灰占位）。
  - **Network**：状态码必须 200，看到 `ERR_BLOCKED_BY_ORB / 404 / CORS` 任一 → 失败，切换
    inline SVG 兜底（`references/design-system.md` §2 Inline-SVG fallback 直接拷贝模板），
    不要再赌另一条外链 URL。
  - **不得给 `<img>` 加 `crossorigin="anonymous"`**（这是触发 CORS → 触发 ORB 的导火索）。
- **（§6 & L4 沉淀）首屏 reveal 核查。**
  硬刷新后 100ms 内：Hero 大标题/副标题/眉标/两个按钮必须 opacity=1（不能是空的透明，等待
  IO 回调的会被判失败）；`rootMargin` 必须是扩张 +12%，不能用负值裁切。首屏 reveal 必须
  先"视口判定后立即 in"的代码块跑在 IO 之前。
- **（§3.b / L1–L3 沉淀）若用户说不要渐变/光 → 核查 Hard-solid lane：**
  - 卡片背景：只有一个 `background:#XX` 纯色值，没有 `,` 分隔的多层 layer。
  - `box-shadow`：feature-cards、icon-box、surface 容器全部 `computed.boxShadow === 'none'`
    （`btn-primary` 的 inset 顶高光例外）。
  - `.feat-icon` 字符：没有彩色 emoji（⚡❤️🌞🎵✅ 都 fail），只能是单调 Unicode/SVG。
  - `.badge`/药丸：`background` 必须是主色 token，不能是透明/半透明空心；border-radius 必须
    ≤12px（紧凑圆角方，不能是 999 超长胶囊）。
- **（§10.b / L8 沉淀）三件套/多物品产品条的几何核查。**
  - 截图确认 3 个物品的左/右/上/下 12 条边界**没有一条**被 overflow 切。
  - 每个物品到最近媒体边界必须有正白边（像素间隙 ≥ 8px），不能贴边。
  - translate 绝对定位中央物品只能是 -50% 正居中，不能是 -52%+。
- **（L5–L6 叠图字色 + btn-outline 来源核查。）**
  - 首屏叠图的大标题颜色：computed `color === rgb(255,255,255)`（纯白色，不是主题 fg 米黄）。
  - 副按钮 `btn-outline` 的 computed `border-width` ≥ 1.8px 且 `border-color` rgba 的 alpha ≥
    0.52（不能是 1px 淡发丝边）。
  - 以上规则的定义**必须在 `.btn-outline` 与 `.btn` 紧邻的原始位置**，不能是文件后半段
    追加的后置覆盖（避免 cascade 吞掉导致 computed 还是 1px）。
- **（L10–L12 spec 清单核查。）**核心配置/规格列表 `.spec-list` 的 CSS 规则必须存在，且
  `row-gap` ≥ 22px、每项有独立的 left border 主色节奏条（不是一堵字墙）。
- Every hotlinked photo loads and that **no source/credit label renders anywhere** on the
  page (a required author+license lives only in an HTML comment); a broken or blank image must not
  ship — swap to another licensed source or the §2 fallback first.
- Scroll the full page: the fixed backdrop never shows a bright seam or an unreadable text zone at
  any offset — opening and closing sit on ink, glass panels stay readable over the picture, and
  every picture↔page junction is a dark transition.
- Start the local dev server and give the user the URL.

## Reference Style

For the bundled dark glassy visual language, read `references/design-system.md`. That file contains
the three scene token sets, the 「质感」 lighting/surface recipes, the full motion palette
(scroll reveal, theme cross-fade, hover/press, micro-interactions, reduced-motion fallback),
component rules, typography, and accessibility details for that treatment. The design principles
above apply regardless of theme. When imagery consent is granted, the page runs on one full-bleed
photograph fixed behind the whole page — the opening copy and the closing CTA both seat over it, and
every picture↔page transition is a dark gradient (暗过渡). The backdrop + veil recipe, mood-matching,
and the no-photo fallback are spec'd in `references/design-system.md` §2. When the ask is an App /
product showcase whose set-piece is the product's own screens (手机格子、屏面陈列), use §10's phone-shell
device register instead of a photographic backdrop. When the language is applied
to an existing UI (a scene or custom color chosen in §0), replicate the Summer Checkin product's
buttons and motion from the embedded spec (§6–§7, product-page shells §9, device showcase §10) —
self-contained, no external project required.
