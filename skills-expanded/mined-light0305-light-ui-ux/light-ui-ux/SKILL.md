---
name: light-ui-ux
description: Next-generation full-stack UI/UX design & engineering system powered by a 59,000-record local SQLite FTS5 arsenal (`assets/light-arsenal.db`). Use whenever creating new web/mobile/desktop interfaces from 0 to 1, polishing or redesigning existing UIs to eliminate AI slop, crafting high-precision interactive components or WebGL/GSAP motion, generating/blending visual media, or transpiling UI across React/Next.js/shadcn, Vue/Nuxt, Vanilla HTML/CSS/JS, React Native/Expo, SwiftUI, and Flutter.
---

# Light-UI-UX — Full-Stack Design & Engineering Orchestrator

You are operating **Light-UI-UX**, an evidence-driven UI/UX design and engineering system backed by a local zero-dependency SQLite FTS5 arsenal ([`assets/light-arsenal.db`](assets/light-arsenal.db), queried via [`scripts/arsenal.py`](scripts/arsenal.py)) containing **1,544 real-world website & award specs**, **1,250 interactive component references** (945 with source; 305 upstream links), **660 motion prompts & recipes**, **33,253 compliant vector SVGs**, **16 standalone WebGL2/Three.js shader stages**, **152 brand `DESIGN.md` systems**, **413 industry reasoning profiles**, and **1,395 cross-stack engineering rules**.

---

## 0. Non-Negotiable Pre-Flight Discipline (Read Before Writing Any Code)

1. **Never Design From Memory Alone — Query the Local Arsenal First**:
   Before proposing directions, picking colors/fonts, or coding components/icons, run `python scripts/arsenal.py` to ground your work in real-world benchmarks and available source code and upstream references:
   ```bash
   # 1. Industry token & anti-pattern deduction (192 industries)
   python scripts/arsenal.py industry "<domain_keyword>"
   # 2. Retrieve 3 real-world website benchmark specs (1,544 sites)
   python scripts/arsenal.py benchmark "<style_or_domain>" --theme light|dark --limit 3
   # 3. Search & extract interactive components (1,250 indexed entries)
   python scripts/arsenal.py component "<pattern_keyword>"
   # Product controls / AI chat: BoardUI source with internal imports and styles
   python scripts/arsenal.py component "<task_keyword>" --site boardui --framework react --mode full_source
   # Expressive interaction: LeiBox framework-aware source and upstream references
   python scripts/arsenal.py component "<interaction_keyword>" --site leibox --framework vue
   # 4. Search & extract compliant vector SVG icons (33,253 SVGs — NEVER use Emoji as UI icons)
   python scripts/arsenal.py icon "<keyword_zh_or_en>"
   # 5. Check target tech-stack rules (22 stacks, 1,395 rules)
   python scripts/arsenal.py stack "<nextjs|react|vue|react-native|flutter|swiftui|shadcn>"
   ```
2. **Enforce the Craft Floor & Anti-AI-Slop Iron Curtain ([`references/02-anti-ai-slop-gates.md`](references/02-anti-ai-slop-gates.md))**:
   - **Zero-Tolerance Bans**:
     - **NO Kicker / Eyebrow chips above headings** (delete uppercase mini-labels/pills above H1/H2; let the heading speak for itself).
     - **NO Nested Cards** (a bordered/shadowed card inside another card is always wrong) and **NO 3-equal-icon-card filler rows** directly below the hero.
     - **NO Side Stripes** (`border-left: 3px solid` or `border-t-4` on rounded cards/alerts).
     - **NO Unrequested Gradient Text (`background-clip: text`)**, **NO Indigo/Violet Neon Glow (`#6366f1`/`#8b5cf6`)**, and **NO Decorative Pulsing Dots**.
     - **NO Emoji / Unicode Symbols (`✨ 🚀 💡 🤖 ✓`) as UI icons** — always extract crisp SVGs via `python scripts/arsenal.py icon --svg <id>`.
     - **NO Meaningless `01 / 02 / 03` Section Numbering** on unordered content.
   - **Hard Page Budgets**:
     - Font families: `≤ 2` (or `≤ 3` with `1` monospace for code/metrics); font sizes: `4–6` steps; weights: `2–3`.
     - Accent color area: `≤ 10%` of viewport; semantic color roles: `≤ 4`.
     - Heavy visual ornament (WebGL shader / SVG filter / 3D stage): **at most `1` per page**.
3. **Use Structure Before Explanatory Copy**:
   - Let layout, visual hierarchy, grouping, spacing, and a clear primary action explain the screen. Omit secondary labels, subtitles, descriptions, and helper text that add no information needed to decide or act; do not fill these slots by default.
   - Keep necessary field labels, accessible names, units, status/error guidance, and material action or billing consequences. Apply the [copy necessity check](references/02-anti-ai-slop-gates.md#31-copy-necessity) before delivery.
4. **Enforce the CJK vs. Latin Dual-Track Typography Law ([`references/03-typography-and-color.md`](references/03-typography-and-color.md))**:
   - **Latin Display H1**: `line-height: 0.95–1.10`, `letter-spacing: -0.02em to -0.04em`.
   - **Chinese / CJK Display H1**: **`line-height: 1.25–1.40` (NEVER `< 1.20` or glyphs collide!)**, **`letter-spacing: 0 to 0.02em` (NEVER negative tracking on CJK!)**.
   - **Body Measure**: Latin `45–75ch`; Chinese `25–40` characters per line (`line-height: 1.65–1.80`).
   - **Numeric Discipline**: Every vertical column, counter, price, or timestamp MUST set `font-variant-numeric: tabular-nums`. Never use fake round numbers (`100`, `50%`, `1,000`); use realistic domain numbers (`1,238`, `+1.83%`, `42ms`).

---

## 1. Dual-Axis Intent Expander (Visitor Mode × Target Platform)

Before writing UI, classify every surface along two orthogonal axes and translate vague user adjectives into concrete physical specifications.

### Axis 1: Visitor Mode (Determines World-Building Boundary)

| Visitor Mode | Typical Surfaces | World-Building & Layout Boundary | Default Build Path |
| :--- | :--- | :--- | :--- |
| **1. Persuade** | Landing page, product launch, brand site, pricing page | **World owns the composition.** Must pass the **Peer Replacement Test** (anchor the hero in a concrete artifact/ritual unique to this domain). Hero must expose a real primary CTA in the first viewport. Limit split left-text/right-image heroes to `≤ 1` candidate direction. Include `≥ 1` scroll-driven (`scrub`) narrative moment. | Benchmark Briefs → Optional `style-explorer.html` → Full Dual-Viewport Build |
| **2. Experience** | Portfolio, exhibition, interactive story, game/habit stage | **Work/stage leads from pixel zero; UI chrome recedes.** Use tactile physics, WebGL shader stages (`arsenal.py shader`), or layered illustration + SVG/Canvas interactive overlays. | Benchmark Briefs → Stage Prototype → Full Build |
| **3. Operate** | SaaS workbench, dashboard, IDE, admin panel, settings | **World lends ONLY 4 things: `Font`, `Palette`, `Density`, and `1 Signature Micro-Detail`.** NEVER put costumes on standard controls. **No marketing slogans in the first viewport**: header + toolbar `≤ 1–2` rows (`28–34px` height), exposing `10–20+` operable items immediately (`32–40px` row height, `13–14px` body, `85%` quiet surface + Inset Canvas). Pick layout by **Primary Verb** (Queue, Table, Canvas, Timeline, Map, Board, Actionable Monitor, Chat+Artifact, Index Gallery). | Primary-Verb Skeleton → Token Lock → Code-Led Build |
| **4. Read** | Documentation, long-form article, research/financial report | **World owns the outer frame** (masthead, side rail, callouts, code blocks); **the inner reading column stays dead quiet** (`60–75ch` Latin / `25–40` CJK chars, high contrast, zero background texture under prose). | Typography & Frame Lock → Code-Led Build |

### Axis 2: Vague Prompt → Physical Parameter Translation Table

| User's Vague Word | Mandatory Physical Translation |
| :--- | :--- |
| **"高级感 / 质感" (Premium)** | Inset Canvas (`1px` subtle border + `R_inner = R_outer - G` concentric radii) + OKLCH hue-tinted dual-layer shadow + `0.5px` hairlines + `≥ 4:1` display-to-body ratio + themed `::selection`, `caret-color`, and scrollbar. |
| **"科技感 / 未来感" (Tech / AI)** | Avoid cliché purple glow & sparkle emojis! Use monochrome deep obsidian (`#08090a`) or lab silver (`#f2f2f0`) + crisp `1px` grid hairlines + tabular monospace telemetry + 1 focal WebGL2 shader (`webgl-liquid-metal` or `webgl-aurora-veil`) or real interactive product slice (`ui-slice`). |
| **"极简 / 干净" (Minimalist)** | `≤ 3` colors total, `≤ 5` font sizes, zero card borders (use `80–160px` vertical rhythm, `2–3` shared left alignment anchor lines, and `4–6×` display scale contrast to carry weight without boxes). |
| **"温暖 / 人文 / 编辑感" (Editorial)** | Avoid the stale `#F5EFE6 + terracotta + italic Fraunces` AI cliché! Draw saturate tactile pigments from real domain materials (bookbinding cloth, dyed endpapers, archival ink) + high-contrast editorial serif + asymmetric staggered columns. |
| **"灵动 / 丝滑" (Fluid / Playful)** | Apple critical/under-damped spring physics (`stiffness: 280, damping: 22`), `pointerdown` instant scale (`0.97`), shared-element indicator glide, and `4` staging containers (Horizontal Accordion / Curved Depth / Stacked Deck / Orbital Lens) instead of static grids. |

---

## 2. Four-Scenario Execution Router

Route the user's request into one of four workflows:

### Scenario A: `0 → 1` New Page or Application Creation
Follow the **5-Step Agile Creation Pipeline** (detailed in [`references/01-benchmark-selection.md`](references/01-benchmark-selection.md)):
1. **Step 1 — Domain Grounding & 3 Real-World Benchmark Briefs**:
   - Run `arsenal.py industry` and `arsenal.py benchmark` (plus `arsenal.py brand` if relevant).
   - Formulate **3 Distinct Direction Briefs** (across `[Hero Skeleton, Typography, Color System, Focal Visual]`, any two directions may overlap on at most `1` dimension; at least `1` direction must invert industry clichés).
   - **Present the 3 Direction Briefs in concise text first** (with a clear recommendation) and ask the user to pick.
   - *Visual Preview Trigger*: If the user asks to see visuals or says *"你定 / 看着办"* (unattended mode), run [`scripts/style_explorer.py`](scripts/style_explorer.py) to generate an interactive side-by-side `style-explorer.html`.
2. **Step 2 — Token Lock & Architecture Blueprint**:
   - Export or synthesize the chosen benchmark's `:root` CSS Custom Properties / Tailwind v4 `@theme` tokens (`arsenal.py benchmark --id <id> --export-tailwind`).
   - Lock the layout skeleton (`references/01-benchmark-selection.md`) and verify WCAG AA contrast (`≥ 4.5:1` body, `≥ 3.0:1` large type).
3. **Step 3 — Arsenal Assembly & Adaptive Media Generation**:
   - Pull matching interactive components (`arsenal.py component`), vector icons (`arsenal.py icon`), and optional WebGL stage (`arsenal.py shader`). For product controls, agentic chat, grids, and settings, check BoardUI; for expressive interactions, check LeiBox. Read [component sources and integration](references/09-component-sources.md) when using either library. Prefer native framework packages when present, preserve internal imports and source notices, and adapt their semantic tokens to the target product.
   - When custom photography/illustration/plates are needed, execute the **3-Tier Adaptive Image Pipeline** via [`scripts/media_gen.py`](scripts/media_gen.py) and blend images using the **6-Step Page-Blending Law** ([`references/05-media-and-imagegen.md`](references/05-media-and-imagegen.md)).
   - **Host-first routing**: If an actual host image-generation tool is available, use it first, even when a custom API key is configured. If no host tool is available, use `generate --tier auto --host-unavailable` to select the configured API or the CC0 fallback. Honor an explicit user choice of provider. The script's host response is a prompt/delegation contract, not an image; invoke the host tool and verify the saved image before reporting generation as complete.
4. **Step 4 — Production Implementation & Mandatory Motion**:
   - Implement responsive desktop (`1440×900`) and mobile (`390×844`) views in the target stack following the **Cross-Stack 1:1 Transpilation Protocol** ([`references/04-motion-and-components.md`](references/04-motion-and-components.md)).
   - Include the **3 Mandatory Baseline Motions**: ① Instant press/hover feedback (`scale(0.97)`), ② Stateful origin-to-destination transition, ③ Staggered initial choreography (`40–80ms` stagger, `≤ 600ms` total; skip on `Operate` workbenches) + `1` `scrub` scroll narrative on `Persuade` pages.
5. **Step 5 — Tiered Visual Verification & Blind Review Loop**:
   - Review visible secondary copy in context: remove repetition, fix ambiguous grouping or actions, and verify that the primary task remains clear after subtraction.
   - Run [`scripts/inspect_ui.py`](scripts/inspect_ui.py) to capture desktop, `@2x` detail, mobile, and `--mask` text-masked screenshots + execute the **67-Rule DOM & Style Auto-Linter**.
   - For full pages or major builds, dispatch an independent blind-review subagent following [`references/07-visual-blind-review.md`](references/07-visual-blind-review.md) (target score `≥ 9.0/10`, max 3 iterations).

### Scenario B: Existing UI Polish & Anti-AI-Slop Redesign
Follow the **Two-Round Non-Destructive Protocol** ([`references/06-polish-and-redesign.md`](references/06-polish-and-redesign.md)):
- **Round 1 (Diagnose Only — Touch Zero Code Files)**:
  1. Inventory existing brand assets vs. accidental framework defaults.
  2. Run `scripts/inspect_ui.py` on the live URL or local entry to capture baseline screenshots, `--mark` numbered issue overlays, and auto-lint violations across 7 dimensions (Alignment/Rhythm, Type Hierarchy, Color/Contrast, States, AI Slop Tells, Narrow-Viewport Overflow, Media/Icons).
  3. Present a structured report split into **`[Direct Fixes]`** and **`[Confirm Scale: Tidy / Upgrade / Reshape]`**, then wait for user confirmation.
- **Round 2 (Root-Cause Refactoring)**:
  - Fix from the design token root (`globals.css` / `theme.ts`) and shared primitives outward, then verify with before/after diff screenshots.

### Scenario C: Single Component Extreme Craft & Cross-Stack 1:1 Transpilation
Follow the **5-Element Component Craft & Transpilation Protocol** ([`references/04-motion-and-components.md`](references/04-motion-and-components.md)):
1. Define the **5 Component Elements**: ① User's 1-sentence question, ② Primary changing quantity (Protagonist), ③ Supporting metadata only when needed for a decision, ④ Single primary gesture + physical feel (drag/press/scrub + snap damping), ⑤ Complete state matrix (`default / hover / active / focus / loading / empty / error / extreme-values`).
2. Enforce the **Single-Ruler Law** (never draw both a read-only progress bar and a separate slider; merge into one interactive track) and **Number-Deduplication Law** (never repeat the same number in title, slider, and caption).
3. Search `arsenal.py component` for the closest high-craft reference. Prefer an existing native package (`--framework`) before transpiling; extract bundled source with `--extract`. For BoardUI, preserve React Aria semantics; for LeiBox, inspect the actual renderer and dependencies rather than assuming every framework wrapper is dependency-free. Follow [component sources and integration](references/09-component-sources.md). When a port is required, preserve interaction intent and equivalent motion while using the target platform's accessibility, lifecycle, and layout APIs.

### Scenario D: Direct Local Arsenal Query & Extraction
When the user asks to browse or pull benchmarks, components, icons, shaders, or brand systems directly, run `scripts/arsenal.py` and deliver clean, copy-ready code or extracted files immediately.

---

## 3. Progressive Disclosure Reference Manuals & CLI Tools

Load only the reference manual required for your active phase:

| File Path | When to Read |
| :--- | :--- |
| [`references/01-benchmark-selection.md`](references/01-benchmark-selection.md) | Starting a new page/app, choosing between Persuade/Operate skeletons, running Peer Replacement Test or 5-subagent brainstorming |
| [`references/02-anti-ai-slop-gates.md`](references/02-anti-ai-slop-gates.md) | Checking the 19 zero-tolerance bans, 5 stale clusters, hard page budgets, and 67 deterministic lint rules |
| [`references/03-typography-and-color.md`](references/03-typography-and-color.md) | Setting CJK/Latin typography scales, OKLCH palettes, dark-mode compensation, concentric radii, and optical alignment |
| [`references/04-motion-and-components.md`](references/04-motion-and-components.md) | Writing spring animations, GSAP ScrollTrigger `scrub` narratives, 4 staging containers, WebGL shaders, or cross-stack transpilation (React/shadcn/Vue/RN/SwiftUI/Flutter) |
| [`references/05-media-and-imagegen.md`](references/05-media-and-imagegen.md) | Generating images (Tier 1 Host / Tier 2 Custom API / Tier 3 CC0 + WebGL), crafting Atelier Zero prompts, IP-as-Logo icons, or blending media into web layouts |
| [`references/06-polish-and-redesign.md`](references/06-polish-and-redesign.md) | Auditing and refactoring an existing project or eliminating AI template feel |
| [`references/07-visual-blind-review.md`](references/07-visual-blind-review.md) | Capturing multi-viewport evidence packages and dispatching the isolated Visual & UX Blind-Review Subagents |
| [`references/09-component-sources.md`](references/09-component-sources.md) | Choosing BoardUI/LeiBox resources, filtering frameworks, extracting complete source closures, mapping semantic tokens, and integrating agentic UI or expressive interactions |

### Built-In Zero-Dependency Python CLI Tools (`scripts/`)
- [`scripts/arsenal.py`](scripts/arsenal.py): Local search and extraction, including component library/framework/source-mode filters and source/dependency metadata.
- [`scripts/import_components.py`](scripts/import_components.py): Maintainer tool to merge inspected BoardUI/LeiBox snapshots into the existing database, with dependency closure, hash checks, and repeat-safe source indexing. See [component sources](references/09-component-sources.md#maintaining-the-import).
- [`scripts/media_gen.py`](scripts/media_gen.py): 3-tier adaptive image generation (`host` / `api` / `cc0`), Atelier Zero optical prompt builder, `3×3` `calm` text-zone pixel analyzer, and `@2x` responsive image post-processor.
- [`scripts/style_explorer.py`](scripts/style_explorer.py): Generates a standalone single-file `style-explorer.html` for interactive 3-direction side-by-side comparison.
- [`scripts/inspect_ui.py`](scripts/inspect_ui.py): Headless browser multi-viewport screenshotter (`1440×900`, `@2x`, `390×844`, `--mask` text-masked view, `--mark` issue callouts) and 67-rule DOM/CSS linter.
