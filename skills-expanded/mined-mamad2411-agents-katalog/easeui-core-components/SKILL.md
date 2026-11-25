---
name: easeui-core-components
description: "EaseUI's actual design tokens, component library, and animation patterns extracted from the production codebase. Reference this when building UI within EaseUI or generating components that must match the EaseUI design language."
disable-model-invocation: false
user-invocable: false
---
# EaseUI Core Components & Design Tokens

> **Source of truth.** Every token, component, and animation in this file is extracted from EaseUI's production codebase (`app/src/app/globals.css` + `project/css/design-system.css`). Do NOT invent values — use these exactly.

---

## 🎨 Color Tokens

### Accent Palette

| Token | Hex | Usage |
|-------|-----|-------|
| `--green` | `#49BA61` | Success, AI completion, streaming indicators, positive feedback |
| `--orange` | `#E36323` | In-progress status, warnings |
| `--red` | `#FE5938` | Errors, destructive actions, `btn-red` |
| `--blue` | `#3582FF` | Links, progress bars, info badges, focus rings |
| `--yellow` | `#FFB73A` | Paused status, warnings |
| `--purple` | `#8755E9` | Phase badges, AI gradient accents |

### Neutrals

| Token | Value | Usage |
|-------|-------|-------|
| `--bg-page` | `#F4F4F5` | Page background |
| `--bg-card` | `#FFFFFF` | Card surfaces |
| `--bg-nav` | `rgba(255,255,255,0.85)` | Frosted nav bars |
| `--text-primary` | `#121212` | Headings, primary content |
| `--text-secondary` | `#71717A` | Descriptions, metadata |
| `--text-muted` | `#A1A1AA` | Placeholders, disabled text |
| `--border-subtle` | `rgba(0,0,0,0.06)` | Card borders |
| `--border-light` | `#E4E4E7` | Dividers, separators |

### Selection

```css
::selection { background: rgba(73, 186, 97, 0.2); color: inherit; }
```

---

## 🔲 Shadow System

| Token | Usage | Light Layers |
|-------|-------|-------------|
| `--shadow-toolbar` | Floating toolbars, navbars | 2 layers, subtle |
| `--shadow-subtle` | Default card rest state | 5 layers, nearly invisible |
| `--shadow-slight-hover` | Light hover elevation | 1 layer |
| `--shadow-card-hover` | Card `:hover` lift | 2 layers |
| `--shadow-prompt-input` | Prompt bar input focus | 3 layers with inset white |
| `--shadow-popover` | Dropdowns, popovers, sidebar mobile | 4 layers |
| `--shadow-modal` | Modal overlays | 1 deep layer |
| `--shadow-btn-primary` | Primary button depth | 3 layers with inset highlight |
| `--shadow-btn-secondary` | Dark button depth | 4 layers with inset rim |
| `--shadow-btn-red` | Destructive button | 3 layers, orange-tinted |
| `--shadow-tab-active` | Active tab indicator | 2 layers with inset white |

---

## 📐 Radii

| Token | Value | Usage |
|-------|-------|-------|
| `--radius-sm` | `0.375rem` (6px) | Small badges, inputs |
| `--radius-md` | `0.625rem` (10px) | Ghost buttons, tags |
| `--radius-lg` | `0.75rem` (12px) | Buttons (.btn default: `0.875rem`) |
| `--radius-xl` | `1.25rem` (20px) | Cards |
| `--radius-full` | `9999px` | Badges, pills, scrollbars |

---

## ✏️ Typography

### Font Stack
```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
--font-code: 'JetBrains Mono', ui-monospace, monospace;
```

### Scale

> 🔴 **MINIMUM FONT SIZE: 12px (0.75rem).** Never use smaller. No exceptions.

| Class | Size | Line Height | Tracking | Usage |
|-------|------|-------------|----------|-------|
| `.text-xs` | 0.75rem (12px) | 1.4 | — | Badge labels, timestamps, metadata |
| `.text-sm` | 0.8125rem (13px) | 1.5 | — | Button text, descriptions |
| `.text-base` | 0.875rem (14px) | 1.5 | — | Body text (EaseUI default) |
| `.text-lg` | 1rem (16px) | 1.5 | — | Emphasized body |
| `.text-xl` | 1.25rem (20px) | 1.3 | — | Subheadings |
| `.text-2xl` | 1.5rem (24px) | 1.2 | — | Section headings |
| `.text-3xl` | 1.875rem (30px) | 1.15 | -0.02em | Page titles |

### Weights
- `.font-medium` = 500 — Labels, interactive text
- `.font-semibold` = 600 — Buttons, subheadings
- `.font-bold` = 700 — Page titles, hero text

---

## 🔘 Button System

### Base `.btn`
```
Height: 2.75rem (44px) | Padding: 0 1.25rem | Radius: 0.875rem (14px)
Font: 0.8125rem/600/-0.01em | Transition: transform 0.25s spring + shadow/opacity 0.2s
```

### Variants

| Class | Background | Text | Shadow | Usage |
|-------|-----------|------|--------|-------|
| `.btn-primary` | `linear-gradient(#E5E5E5, #E2E2E2)` | `#121212` | `--shadow-btn-primary` | Primary actions (light button) |
| `.btn-secondary` | `linear-gradient(#323232, #222222)` | `#FCFCFC` | `--shadow-btn-secondary` | Secondary actions (dark button) |
| `.btn-red` | `linear-gradient(#E36323, #DF5A18)` | `#FCFCFC` | `--shadow-btn-red` | Destructive actions |
| `.btn-ghost` | `transparent` | `--text-secondary` | none | Tertiary, toolbar actions |

### States

| State | Behavior |
|-------|----------|
| `:hover` | `translateY(-1px)` + `::after` overlay opacity 1 |
| `:active` | `scale(0.96) translateY(0)` — 0.1s |
| `:focus-visible` | `0 0 0 2px #fff, 0 0 0 4px rgba(53,130,255,0.5)` |
| `:disabled` | `opacity: 0.55; cursor: not-allowed; transform: none` |
| `.btn-loading` | `pointer-events: none; opacity: 0.8` — label hidden, spinner shown |

---

## 🏷️ Badge System

### Base `.badge`
```
Display: inline-flex | Gap: 0.25rem | Padding: 0.125rem 0.5rem
Radius: --radius-full | Font: 0.6875rem/600/0.02em/uppercase
```

### Status Variants

| Class | Background | Text | Maps to |
|-------|-----------|------|---------|
| `.badge-shipped` | `#E8F5E9` | `#2E7D32` | Feature shipped |
| `.badge-specced` | `#E3F2FD` | `#1565C0` | Spec complete |
| `.badge-progress` | `#FFF3E0` | `#E65100` | In progress |
| `.badge-backlog` | `#F5F5F5` | `#757575` | Backlog |
| `.badge-paused` | `#FFF8E1` | `#F9A825` | Paused |
| `.badge-p1` | `#FFEBEE` | `#C62828` | Priority 1 |
| `.badge-p2` | `#FFF3E0` | `#EF6C00` | Priority 2 |
| `.badge-p3` | `#F5F5F5` | `#757575` | Priority 3 |
| `.badge-phase` | `rgba(0,0,0,0.05)` | `--text-secondary` | Phase label |

---

## 🃏 Card System

### Base `.card`
```css
background: var(--bg-card);
border: 1px solid var(--border-subtle);
border-radius: var(--radius-xl);     /* 1.25rem = 20px */
padding: 1rem 1.125rem;
transition: box-shadow 0.2s ease, transform 0.2s ease;
cursor: pointer;
```

### Hover State
```css
.card:hover {
  box-shadow: var(--shadow-card-hover);
  transform: translateY(-1px);
}
```

---

## ⌨️ Keyboard Shortcut Badge `.kbd`
```
Size: 1.25rem min-width/height | Padding: 0 0.3rem
Font: inherit/0.625rem/500 | Color: zinc-400
Background: zinc-100 | Border: 1px solid zinc-200 | Radius: 0.25rem
```

---

## 🎬 Animation Library

### Page Transitions

| Class | Keyframes | Duration/Easing |
|-------|-----------|----------------|
| `.page-transition` | `page-enter` — opacity 0→1, translateY 8px→0 | 0.4s `cubic-bezier(0.16, 1, 0.3, 1)` |
| `.reveal` | `reveal-up` — opacity 0→1, translateY 12px→0 | 0.4s same easing |
| `.reveal-1` through `.reveal-8` | Staggered delays: 0ms, 50ms, 100ms, 150ms, 200ms, 250ms, 300ms, 350ms | Use for sequential entrance |
| `.device-switch` | opacity 0.5→1, scale 0.97→1 | 0.35s same easing |

### AI / Streaming Animations

| Class | Keyframes | Duration | Usage |
|-------|-----------|----------|-------|
| `.streaming-border` | `gradient-rotate` — conic gradient 0°→360° | 2.5s linear ∞ | Active AI generation border |
| `.streaming-shimmer` | `streaming-shimmer` — translateX -100%→100% | 2s ease-in-out ∞ | Shimmer overlay during generation |
| `.streaming-dot` | `pulse-glow` — opacity + box-shadow pulse | 1.5s ease-in-out ∞ | AI activity indicator dot |
| `.streaming-progress` | `progress-indeterminate` — translateX -100%→400% | 1.5s ease-in-out ∞ | Indeterminate progress bar |
| `.radiant-ai-border` | `radiant-rotate` — conic gradient rotation | 4s linear ∞ | Premium AI processing border |
| `.skeleton-shimmer` | `shimmer` — background-position sweep | 1.8s ease-in-out ∞ | Loading placeholder |
| `.animate-gradient-border` | `rotation` — conic gradient rotation | 4s linear ∞ | Rainbow gradient border |

### Feedback Animations

| Class | Keyframes | Duration | Usage |
|-------|-----------|----------|-------|
| `.animate-completion` | `completion-flash` — scale + green glow burst | 0.6s ease-out | Generation complete |
| `.feedback-success-ring` | Ring burst scale + fading box-shadow | 0.6s spring | Positive rating |
| `.feedback-sparkle` | Scale 0→1.2→0 + rotate 0→360° | 0.5s spring | Sparkle on positive feedback |
| `.animate-shake` | `input-shake` — horizontal shake ±4px | 0.3s ease-out | Validation error |

### Reduced Motion

All animations respect `prefers-reduced-motion: reduce` — durations set to 0.01ms, animations disabled, scroll-behavior set to auto.

---

## 🧩 Responsive Breakpoints

| Breakpoint | Behavior |
|-----------|----------|
| `< 768px` | Sidebar: full-width overlay |
| `< 1024px` | Sidebar: slides out (`translateX(-100%)`), header goes full-width |
| `≥ 1024px` | Sidebar: persistent, content offset |

---

## 📜 Scrollbar

```css
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(0,0,0,0.12); border-radius: 999px; }
::-webkit-scrollbar-thumb:hover { background: rgba(0,0,0,0.22); }
```

Hide scrollbar: `.scrollbar-none`

---

## 🔑 EaseUI Easing Curves

| Name | Value | Usage |
|------|-------|-------|
| **Default** | `0.2s ease` | Standard transitions (buttons, cards) |
| **Spring** | `0.25s cubic-bezier(0.34, 1.56, 0.64, 1)` | Button press/release |
| **Smooth decelerate** | `0.4s cubic-bezier(0.16, 1, 0.3, 1)` | Page transitions, reveal, device switch |
| **Quick feedback** | `0.1s` | Active press states |
| **Toast exit** | Paired `toast-in` + `toast-out` animations | Toast notifications |

---

## 📊 Design Knowledge Databases

Searchable CSV data for UX patterns, accessibility, performance, and more. Grep these when you need specific guidance:

| File | Entries | Content | When to Use |
|------|---------|---------|-------------|
| [ux-guidelines.csv](data/ux-guidelines.csv) | 99 | UX rules: smooth scroll, z-index, animation duration, loading states, form patterns | Any UX decision |
| [web-interface.csv](data/web-interface.csv) | 31 | WCAG: aria-labels, focus management, keyboard nav, semantic HTML | Accessibility work |
| [react-performance.csv](data/react-performance.csv) | 45 | Async waterfall, memo, rerender, cache, suspense, bundle optimization | Performance tuning |
| [charts.csv](data/charts.csv) | 25 | Chart type selection, color guidance, a11y notes, library recommendations | Data visualization |
| [nextjs.csv](data/stacks/nextjs.csv) | ~40 | SSR, routing, images, API routes, caching — EaseUI's stack | Next.js-specific patterns |
| [icons.csv](data/icons.csv) | 101 | Lucide icon name → keyword mapping | Finding the right icon |

**Quick search example:**
```bash
# Find UX rules about animation
grep -i "animation" .agent/skills/easeui-core-components/data/ux-guidelines.csv

# Find React performance rules about memo
grep -i "memo" .agent/skills/easeui-core-components/data/react-performance.csv

# Find the right Lucide icon
grep -i "search" .agent/skills/easeui-core-components/data/icons.csv
```

---

## 🧩 Component Registry (NEVER REINVENT — REUSE FIRST)

> 🔴 **Before creating ANY new component, check this registry.** If it exists here, use it. Only create new components if confirmed absent.

### Shared Components (`components/`)

| Component | File | Purpose |
|-----------|------|---------|
| `Tooltip` | `tooltip.tsx` | Hover tooltip with positioning |
| `Toast` | `toast.tsx` | Notification toasts |
| `Skeleton` | `skeleton.tsx` | Loading placeholders |
| `CopyButton` | `copy-button.tsx` | Copy-to-clipboard with feedback |
| `EmptyState` | `empty-state.tsx` | Zero-data state with CTA |
| `ErrorBoundary` | `error-boundary.tsx` | React error boundary |
| `PageTransition` | `page-transition.tsx` | Page entrance animation |
| `KeyboardShortcuts` | `keyboard-shortcuts.tsx` | Shortcut modal/handler |
| `ColorPickerPopover` | `color-picker-popover.tsx` | Color picker dropdown |
| `TagPopover` | `tag-popover.tsx` | Tag management popover |
| `Sidebar` | `sidebar.tsx` | Main app sidebar navigation |
| `GenerationHUD` | `generation-hud.tsx` | AI generation progress overlay |
| `BackgroundTaskBar` | `background-task-bar.tsx` | Background task status |
| `FeedbackModal` | `feedback-modal.tsx` | User feedback collection |
| `UpgradeModal` | `upgrade-modal.tsx` | Plan upgrade prompt |
| `DSExportModal` | `ds-export-modal.tsx` | Design system export |
| `NotificationCenter` | `notification-center.tsx` | Notification panel |
| `VariantRating` | `variant-rating.tsx` | Rate generated variants |
| `ProjectCostPanel` | `project-cost-panel.tsx` | Token/cost tracking |
| `PropertiesInspector` | `properties-inspector.tsx` | CSS property editor |
| `AiSparkleIcon` | `ai-sparkle-icon.tsx` | Animated AI indicator |
| `LayerTree` | `layer-tree.tsx` | HTML layer tree panel |
| `InteractiveWavesBackground` | `InteractiveWavesBackground.tsx` | Animated wave background |
| `SoundProvider` | `SoundProvider.tsx` | Sound effects context provider |
| `AdminSidebar` | `admin/admin-sidebar.tsx` | Admin panel navigation |
| `BubbleMenu` | `admin/editor/bubble-menu.tsx` | Rich text floating menu |
| `CommandList` | `admin/editor/command-list.tsx` | Slash command menu |
| `MarkdownEditor` | `admin/editor/markdown-editor.tsx` | Markdown WYSIWYG editor |

### Editor Components (`components/editor/`)

| Component | File | Purpose |
|-----------|------|---------|
| `CanvasLayer` | `canvas-layer.tsx` | Canvas layer container |
| `CanvasViewport` | `canvas-viewport.tsx` | Main canvas with pan/zoom |
| `DSCanvasViewport` | `ds-canvas-viewport.tsx` | Design system canvas |
| `ArtboardRenderer` | `artboard-renderer.tsx` | Render artboard iframes |
| `ArtboardContextMenu` | `artboard-context-menu.tsx` | Right-click menu |
| `SelectionRing` | `selection-ring.tsx` | Blue selection border |
| `DotGrid` | `dot-grid.tsx` | Canvas background grid |
| `CanvasMinimap` | `canvas-minimap.tsx` | Overview minimap |
| `ConnectionLines` | `connection-lines.tsx` | Artboard connection lines |
| `ZoomToolbar` | `zoom-toolbar.tsx` | Zoom controls |
| `RadialDial` | `radial-dial.tsx` | Circular control dial |
| `EditorSidebar` | `editor-sidebar.tsx` | Editor right panel |
| `EditorDrawer` | `editor-drawer.tsx` | Slide-out drawer |
| `GenerationPanel` | `generation-panel.tsx` | Prompt input panel |
| `ComponentSelectorModal` | `component-selector-modal.tsx` | Pick wireframe component |
| `SlidePresenter` | `slide-presenter.tsx` | Slide presentation mode |
| `SlideFilmstrip` | `slide-filmstrip.tsx` | Slide thumbnails |
| `SlideExportMenu` | `slide-export-menu.tsx` | Export slide options |
| `DSCardRenderer` | `ds-card-renderer.tsx` | Design system card |

### Sidebar Panels (`components/editor/sidebar-panels/`)

| Component | File | Purpose |
|-----------|------|---------|
| `VariantPanel` | `variant-panel.tsx` | Selected variant details |
| `ProjectOverviewPanel` | `project-overview-panel.tsx` | Project summary |
| `EmptyCanvasPanel` | `empty-canvas-panel.tsx` | Empty canvas CTA |
| `MultiSelectPanel` | `multi-select-panel.tsx` | Bulk actions |
| `GenerationOverlay` | `generation-overlay.tsx` | Generation progress |
| `InspectorGuidePanel` | `inspector-guide-panel.tsx` | Inspector help |
| `DSComponentPanel` | `ds-component-panel.tsx` | DS component view |
| `DSOverviewPanel` | `ds-overview-panel.tsx` | DS overview |
| `DSFoundationPanel` | `ds-foundation-panel.tsx` | DS foundations |
| `DSGuidelinesPanel` | `ds-guidelines-panel.tsx` | DS usage guidelines |
| `DSItemPreviewPanel` | `ds-item-preview-panel.tsx` | DS item detail |
| `DSEmptyPanel` | `ds-empty-panel.tsx` | DS empty state |

### Icons (`components/icons/`) — 40 custom icons

Search before creating: `grep -l "icon-name" app/src/components/icons/`

---

## 📁 Source Files

| File | Contains |
|------|----------|
| [globals.css](file:///Users/jangtrinh/Desktop/Design/EaseUI/app/src/app/globals.css) | Main app design tokens, buttons, animations (799 lines) |
| [design-system.css](file:///Users/jangtrinh/Desktop/Design/EaseUI/project/css/design-system.css) | PM Hub tokens, badges, cards, utilities (238 lines) |
| [design-tokens.ts](file:///Users/jangtrinh/Desktop/Design/EaseUI/app/src/lib/design-tokens.ts) | Token parser (markdown → structured tokens) |
| [color-scales.ts](file:///Users/jangtrinh/Desktop/Design/EaseUI/app/src/lib/color-scales.ts) | OKLCH perceptual color scale generator |
| [component-catalog.ts](file:///Users/jangtrinh/Desktop/Design/EaseUI/app/src/lib/component-catalog.ts) | 24 wireframe component templates |

## Done Condition

Correct token/component identified + registry consulted before creating new components + sync script passes
