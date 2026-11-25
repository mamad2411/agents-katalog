---
name: claude-design
description: World-class frontend UI/UX design craft with dual-mode delivery (standalone HTML artifacts with Tweaks panel and production React/Tailwind/shadcn components), 4-layer atomic button craft, 7 surface-first composition archetypes, and 10-point anti-slop quality gates.
category: "04 - Web & Frontend"
tags:
  - agent-skill
  - frontend
  - design-system
  - ui-ux
  - stage-4
aliases:
  - claude-design
  - ui-craft
  - frontend-design
  - button-design
---

# Claude Design: World-Class Frontend UI/UX Craft

Use this skill when designing frontend interfaces, visual systems, component libraries, landing experiences, interactive prototypes, or production application UI. This skill equips agents with world-class aesthetic judgment, tactical design discipline, and dual-mode delivery capabilities for both standalone prototypes and production web applications.

---

## Runtime Mode & Operating Philosophy

You are running in **CLI/API mode**, not the hosted Claude Design web UI.
Preserve Claude Design's design behavior, taste, and craft while ignoring hosted-only tool plumbing that does not exist in local agent environments:

- Ignore hosted tool calls: `done()`, `fork_verifier_agent()`, `questions_v2()`, `copy_starter_component()`, `show_to_user()`, `show_html()`, `snip()`, `eval_js_user_view()`.
- Ignore hosted asset review panes, edit-mode toolbar callbacks, `/projects/<projectId>/...` cross-project paths, or built-in `window.claude.complete()` helpers.
- Use the real tools available in your environment (terminal, playwright, file tools).

### Core Designer Identity
Act as an expert designer working with the user as the design partner and manager:
- **UX designer** for user flows, mental models, and product surfaces
- **Interaction designer** for clickable prototypes and reactive states
- **Visual designer** for static explorations and art direction
- **Motion designer** for purposeful, micro-interactive transitions
- **Deck designer** for high-impact presentations
- **Design-systems architect** for tokens, components, and visual rules
- **Frontend engineer** when production code fidelity matters

---

## Dual-Mode Delivery Architecture

Modern frontend workflows require two distinct delivery modalities depending on the user's objective:

```
┌──────────────────────────────────────────────────────────────┐
│                     USER DESIGN REQUEST                      │
└──────────────────────────────┬───────────────────────────────┘
                               │
               ┌───────────────┴───────────────┐
               ▼                               ▼
    [Mode A: Standalone Artifact]    [Mode B: Production Codebase]
    - Single-file HTML/CSS/JS       - React / Next.js App Router
    - Live in-page Tweaks panel      - Tailwind CSS + shadcn/ui
    - Rapid client review/critique   - Production TypeScript & tests
    - LocalStorage persistence       - Accessible headless primitives
    - Zero dev-server friction       - Atomic component architecture
```

### Mode A: Standalone HTML Artifacts & Prototypes (with Live Tweaks Panel)

Used when exploring ideas, pitching visual directions, sharing standalone deliverables, or creating shareable interactive mockups without requiring build tools or dev servers.

- **Self-Contained File:** Everything in a single portable `.html` file with embedded `<style>` and `<script>`.
- **Live `Tweaks` Panel:** A lightweight, non-intrusive floating or docked drawer allowing users to interactively test variations:
  - Theme toggles (`Warm Ivory`, `Charcoal Dark`, `System`) via CSS custom properties.
  - Accent color swaps (e.g., Terracotta `#C96442`, Indigo `#4F46E5`, Emerald `#059669`, Neutral Slate `#475569`).
  - Typography scale adjustments (`Default`, `Compact`, `Editorial`).
  - Layout density modes (`Comfortable`, `Compact`, `Dense`).
  - Component variant switches.
- **State Persistence:** Tweak choices persist in `localStorage` across page reloads.
- **Zero Build Friction:** Double-clickable on any machine, works completely offline without network dependencies.

#### Standalone HTML Tweaks Panel Blueprint
```html
<!-- Live In-Page Tweaks Panel Blueprint -->
<div id="tweaks-dock" style="position:fixed;bottom:20px;right:20px;z-index:9999;font-family:system-ui,sans-serif;">
  <button id="tweaks-toggle" onclick="document.getElementById('tweaks-drawer').classList.toggle('open')"
    style="background:#18181b;color:#f4f4f5;border:1px solid rgba(255,255,255,0.15);padding:8px 14px;border-radius:9999px;font-size:13px;font-weight:500;box-shadow:0 4px 12px rgba(0,0,0,0.15);cursor:pointer;display:flex;align-items:center;gap:6px;">
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
    <span>Tweaks</span>
  </button>
  <div id="tweaks-drawer" style="display:none;margin-top:8px;background:#ffffff;border:1px solid #e4e4e7;padding:16px;border-radius:12px;box-shadow:0 10px 25px rgba(0,0,0,0.1);width:260px;">
    <div style="font-size:12px;font-weight:600;text-transform:uppercase;letter-spacing:0.05em;color:#71717a;margin-bottom:12px;">Display Controls</div>
    <div style="margin-bottom:10px;">
      <label style="display:block;font-size:12px;color:#27272a;margin-bottom:4px;">Theme Mode</label>
      <select onchange="updateTheme(this.value)" style="width:100%;padding:6px 8px;border:1px solid #d4d4d8;border-radius:6px;font-size:13px;">
        <option value="light">Warm Ivory (Light)</option>
        <option value="dark">Charcoal (Dark)</option>
      </select>
    </div>
    <div style="margin-bottom:10px;">
      <label style="display:block;font-size:12px;color:#27272a;margin-bottom:4px;">Density</label>
      <select onchange="updateDensity(this.value)" style="width:100%;padding:6px 8px;border:1px solid #d4d4d8;border-radius:6px;font-size:13px;">
        <option value="comfortable">Comfortable</option>
        <option value="compact">Compact</option>
      </select>
    </div>
  </div>
</div>
<style>
  #tweaks-drawer.open { display: block !important; }
</style>
<script>
  function updateTheme(mode) {
    document.documentElement.setAttribute('data-theme', mode);
    localStorage.setItem('claude_design_theme', mode);
  }
  function updateDensity(density) {
    document.documentElement.setAttribute('data-density', density);
    localStorage.setItem('claude_design_density', density);
  }
  // Initialize from storage
  (function() {
    const t = localStorage.getItem('claude_design_theme') || 'light';
    const d = localStorage.getItem('claude_design_density') || 'comfortable';
    document.documentElement.setAttribute('data-theme', t);
    document.documentElement.setAttribute('data-density', d);
  })();
</script>
```

### Mode B: Production React / Next.js / Tailwind CSS / shadcn/ui

Used when implementing within an existing project repository or building scalable enterprise applications.

- **Framework Native:** Next.js App Router (`app/`), React Server Components by default, Client Components (`"use client"`) strictly where interactivity or browser APIs are required.
- **Tailwind Utility Stack:** Tailored Tailwind CSS classes adhering to strict design tokens (spacing, shadows, typography).
- **Accessible Primitives:** Built atop Radix UI (`@radix-ui/react-*`) and `shadcn/ui` conventions for robust keyboard navigation and screen-reader accessibility.
- **Component Modularity:** Strict separation into reusable atomic components (`components/ui/button.tsx`, `components/ui/card.tsx`), composite feature widgets, and page views.
- **Class Variance Authority (`cva`):** Predictable variant management with type-safe props.

### Mode C: Generative UI & Google Antigravity Native Artifacts

Used when generating interactive widgets inline within chat responses or persistent workspace artifacts:

- **Embed Tag:** Render inline widgets via `<agent-embed src="file:///<artifact_path>/widget.html"></agent-embed>`.
- **Semantic CSS Variables:** Inherit the host theme automatically via injected CSS variables:
  - Surfaces: `--background`, `--card`, `--sidebar`, `--content`
  - Borders: `--border`, `--ring`
  - Text: `--foreground`, `--muted-foreground`, `--placeholder`
  - Accents: `--primary`, `--primary-foreground`, `--accent`, `--secondary`
- **Tailwind In-Iframe Dependency:** Load the gstatic Tailwind script allowlisted by CSP:
  `<script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>`
- **No Local Fallbacks on `:root`**: Never declare hardcoded color overrides on `:root`; let host environment dictate contrast.

---

## 2026 Modern Web Standards & Platform Primitives

Do not use heavy legacy JavaScript libraries when modern browser primitives natively solve the problem with zero bundle weight and 60 FPS performance:

1. **Native Popover API (`popover="auto"`):**
   - Replaces floating-ui / popper for dropdowns and tooltips.
   - Automatically handles top-layer promotion, click-outside dismissal, and ESC key closure:
     ```html
     <button popovertarget="user-menu">Account</button>
     <div id="user-menu" popover>...</div>
     ```
2. **CSS Anchor Positioning (`anchor-name` & `position-anchor`):**
   - Anchor floating elements directly to trigger buttons without JS coordinate math:
     ```css
     #user-menu {
       position-anchor: --user-btn;
       top: anchor(bottom);
       left: anchor(left);
     }
     ```
3. **Native `<dialog>` with Dynamic Backdrop:**
   - Fully accessible modal dialogs with native focus trapping:
     ```html
     <dialog id="confirm-modal">
       <form method="dialog">...</form>
     </dialog>
     <style>
       dialog::backdrop {
         background: rgba(0, 0, 0, 0.45);
         backdrop-filter: blur(8px);
       }
     </style>
     ```
4. **View Transitions API (`document.startViewTransition`):**
   - Seamless cross-fade and morph animations during DOM updates:
     ```javascript
     function navigateTab(newTab) {
       if (document.startViewTransition) {
         document.startViewTransition(() => renderTab(newTab));
       } else {
         renderTab(newTab);
       }
     }
     ```
5. **Tailwind CSS v4 `@theme` Engine & OKLCH Color Space:**
   - Use perceptual uniform color spaces (`oklch`) for smooth color gradients and high-contrast palettes:
     ```css
     @theme {
       --color-canvas: oklch(0.98 0.005 85);
       --color-ink: oklch(0.18 0.01 60);
       --color-accent: oklch(0.55 0.16 35);
     }
     ```
6. **CSS Container Queries (`@container`) & `:has()`:**
   - Style components based on container width, not screen viewport:
     ```css
     .card-container { container-type: inline-size; }
     @container (min-width: 420px) {
       .card-body { display: grid; grid-template-columns: 1fr 1fr; }
     }
     ```


---

## Atomic Button Craft: The 4-Layer Construction

Buttons are the primary physical touchpoint in UI. Generic AI designs produce flat, lifeless rectangles. Master-level UI craft treats buttons as tangible, micro-machined physical elements built in **4 distinct visual layers** with **5 interactive states** and **asymmetric optical balancing**.

```
┌─────────────────────────────────────────────────────────────┐
│ 4. Ambient Drop Shadow & 1px Containment Ring (Outer Depth) │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ 2. Hairline Structural Border (1px Contrast Border)   │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │ 3. Sub-Pixel Inner Highlight (Top Bevel Inset)   │  │  │
│  │  │  ┌───────────────────────────────────────────┐  │  │  │
│  │  │  │ 1. Base Surface (Solid / Micro-Gradient)  │  │  │  │
│  │  │  │    [ ◄ Icon ]  Action Label               │  │  │  │
│  │  │  └───────────────────────────────────────────┘  │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 1. The 4 Layers of Button Construction

| Layer | Name | Technical Implementation | Visual Purpose |
| :--- | :--- | :--- | :--- |
| **Layer 1** | **Base Surface** | `bg-zinc-900 dark:bg-zinc-100` or subtle 1% vertical gradient | Establishes the foundational color volume and tactile material. |
| **Layer 2** | **Hairline Border** | `border border-black/10 dark:border-white/15` | Defines crisp boundary separation against varied backgrounds. |
| **Layer 3** | **Sub-Pixel Inner Highlight** | `shadow-[inset_0_1px_0_rgba(255,255,255,0.2)] dark:shadow-[inset_0_1px_0_rgba(255,255,255,0.35)]` | Simulates overhead light reflection on the top beveled edge. |
| **Layer 4** | **1px Ring Shadow Tokens** | `shadow-sm ring-1 ring-black/5 dark:ring-white/10` | Grounds the button to the surface with ambient contact occlusion. |

### 2. The 5 Interactive States

Every production button must implement all 5 states with micro-interactions:

1. **Default (Resting):**
   - Full 4-layer composition visible.
   - Smooth transition timing: `transition-all duration-150 ease-out`.
2. **Hover:**
   - Subtle brightness lift: `hover:brightness-105 dark:hover:brightness-110`.
   - Subtle elevation increase: `hover:shadow-md`.
3. **Active / Pressed (Micro-Compression):**
   - Mechanical compression feel: `active:scale-[0.98]`.
   - Highlight shifts to inset depth: `active:shadow-[inset_0_2px_4px_rgba(0,0,0,0.18)]`.
4. **Focus-Visible (Keyboard Navigation):**
   - Clean, high-contrast offset outline: `focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-zinc-950 focus-visible:ring-offset-background`.
5. **Disabled:**
   - De-emphasized and non-interactive: `disabled:opacity-50 disabled:pointer-events-none disabled:shadow-none disabled:cursor-not-allowed`.

### 3. Asymmetric Icon Padding (Optical Weight Compensation)

When an icon is placed next to text inside a button, standard equal padding (`px-4`) causes the icon side to appear optically heavier than the text side.
**Rule:** Always apply asymmetric horizontal padding:

- **Leading Icon (Icon Left):** Reduce left padding by 25%:
  - Standard: `pl-3 pr-4` (e.g., `py-2 pl-3 pr-4 text-sm font-medium gap-2`)
- **Trailing Icon (Icon Right):** Reduce right padding by 25%:
  - Standard: `pl-4 pr-3` (e.g., `py-2 pl-4 pr-3 text-sm font-medium gap-2`)
- **Icon Sizing:** Keep icons proportional (16px / `w-4 h-4` for standard 36px–40px buttons).

### 4. Production Code Implementations

#### Mode B: Production React + `cva` Component
```tsx
import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center whitespace-nowrap rounded-lg text-sm font-medium transition-all duration-150 ease-out focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-zinc-950 focus-visible:ring-offset-background disabled:pointer-events-none disabled:opacity-50 active:scale-[0.98]",
  {
    variants: {
      variant: {
        primary:
          "bg-zinc-900 text-white border border-black/10 shadow-sm shadow-black/10 ring-1 ring-black/5 shadow-[inset_0_1px_0_rgba(255,255,255,0.2)] hover:bg-zinc-800 hover:shadow-md active:shadow-[inset_0_2px_4px_rgba(0,0,0,0.2)] dark:bg-zinc-100 dark:text-zinc-900 dark:border-white/20 dark:shadow-[inset_0_1px_0_rgba(255,255,255,0.4)] dark:hover:bg-zinc-200",
        secondary:
          "bg-white text-zinc-900 border border-zinc-200 shadow-sm ring-1 ring-black/5 shadow-[inset_0_1px_0_rgba(255,255,255,1)] hover:bg-zinc-50 hover:border-zinc-300 dark:bg-zinc-800 dark:text-zinc-100 dark:border-zinc-700 dark:hover:bg-zinc-700",
        destructive:
          "bg-rose-600 text-white border border-rose-700/20 shadow-sm shadow-rose-600/20 shadow-[inset_0_1px_0_rgba(255,255,255,0.25)] hover:bg-rose-700 active:shadow-inner",
      },
      size: {
        default: "h-9 px-4 py-2",
        sm: "h-8 rounded-md px-3 text-xs",
        lg: "h-10 rounded-md px-6 text-base",
        iconLeading: "h-9 pl-3 pr-4 py-2 gap-2",
        iconTrailing: "h-9 pl-4 pr-3 py-2 gap-2",
      },
    },
    defaultVariants: {
      variant: "primary",
      size: "default",
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, ...props }, ref) => {
    return (
      <button
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    )
  }
)
Button.displayName = "Button"
```

#### Mode A: Standalone HTML/CSS Button
```html
<button class="atomic-btn atomic-btn-primary">
  <svg class="atomic-icon" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5">
    <path d="M8 3v10M3 8h10"/>
  </svg>
  <span>Create Production Workspace</span>
</button>

<style>
.atomic-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 38px;
  padding-left: 12px;
  padding-right: 16px;
  gap: 8px;
  font-size: 14px;
  font-weight: 500;
  border-radius: 8px;
  cursor: pointer;
  white-space: nowrap;
  transition: all 150ms ease-out;
  outline: none;
}
.atomic-btn:active {
  transform: scale(0.98);
}
.atomic-btn:focus-visible {
  box-shadow: 0 0 0 2px #fff, 0 0 0 4px #18181b;
}
.atomic-btn-primary {
  background: #18181b;
  color: #fafafa;
  border: 1px solid rgba(0, 0, 0, 0.12);
  box-shadow: 0 1px 2px rgba(0,0,0,0.06), 0 0 0 1px rgba(0,0,0,0.05), inset 0 1px 0 rgba(255,255,255,0.2);
}
.atomic-btn-primary:hover {
  background: #27272a;
  box-shadow: 0 4px 12px rgba(0,0,0,0.12), inset 0 1px 0 rgba(255,255,255,0.25);
}
.atomic-btn-primary:active {
  box-shadow: inset 0 2px 4px rgba(0,0,0,0.25);
}
.atomic-icon {
  width: 16px;
  height: 16px;
}
</style>
```

---

## Surface-First Composition: The 7 Archetypes

Most AI design failures are **compositional, not cosmetic**. Naive generation repeatedly defaults to a centered hero banner followed by three equal-width feature cards. This layout is completely broken for dashboards, settings, data grids, or consoles.

**Mandatory Rule:** Before writing any tokens, colors, or CSS, **commit out loud to exactly ONE surface archetype**:

| Archetype | Primary User Mission | Composition Pattern | Forbidden Traps |
| :--- | :--- | :--- | :--- |
| **1. Monitor** | Watching state change, telemetry, observability, system status | High-density grids, glanceable metric hierarchy, sparklines, status indicators | **NO** centered hero banners. **NO** marketing copy. |
| **2. Operate** | Taking actions on queues, batch processing, inboxes, admin lists | Action affordances, sticky toolbars, bulk selection bars, tabular data | **NO** oversized decorative images. Speed beats fluff. |
| **3. Compare** | Weighing options, pricing tiers, spec sheets, feature matrices | Perfectly aligned columns, structural parity, clear singular focal differentiator | **NO** unequal vertical alignment. Don't hide differences. |
| **4. Configure** | Setting preferences, multi-step wizards, account setup, forms | Progressive disclosure, clear field grouping, explicit save/validation states | **NO** decorative clutter. Zero ambiguous validations. |
| **5. Decide / Learn** | Understanding value proposition, product education, landing page | High-impact headline, single focal concept per fold, social proof, clear CTA | **The ONLY surface** where a centered hero + cards is valid. |
| **6. Explore** | Browsing large catalog spaces, media galleries, map locators | Faceted filters, responsive grid cards, quick-peek modals, scroll memory | **NO** dead ends. Filter count must always be clear. |
| **7. Command / Inspect** | Driving via keyboard, deep drilling into single object properties | Split-pane inspector, property drawers, command palette (`Cmd+K`), mono keys | **NO** multi-column sprawling layouts. Focus is paramount. |

---

## The 10-Point Slop Diagnostics & Scoring Protocol

Before declaring any UI artifact complete, run this strict 10-point audit. Score the design from 0 to 10 (each occurrence adds 1 penalty point; 0 is perfection):

1. **Tech Gradient:** Unmotivated blue/violet/fuchsia background blurs or glossy gradient buttons.
2. **Generic Tech Hue:** Defaulting to arbitrary Tailwind `indigo-600` or `violet-500` instead of intentional brand identity.
3. **Feature-Tile Grid:** Exactly 3 cards with an icon + title + generic sentence, repeated endlessly.
4. **Accent Rail:** A colored 3px vertical strip on the left of cards pretending to be organization.
5. **Unearned Blur:** Glassmorphism (`backdrop-blur`) slapped onto surfaces without an actual physical depth hierarchy.
6. **Monument Stat:** Giant arbitrary numbers ("99.9%", "10x", "$5M") taking up valuable real estate without context.
7. **Icon Topper:** Centered rounded square containing an icon hovering over every single heading.
8. **Center Stack:** Everything center-aligned because the model lacked conviction to build a structured layout.
9. **Default Type:** Falling back to unstyled system fonts without optical sizing or line measure control.
10. **Wrong Surface:** Using a marketing hero on a Monitor/Operate surface (the #1 AI giveaway).

### Targeted Repair Hierarchy
- **Tells 3, 8, 10 Fired?** **Re-layout / Re-compose immediately.** Revisit the surface archetype. Do NOT just change colors.
- **Tells 1, 2, 9 Fired?** **Re-palette / Re-typeset.** Establish strict neutral shades with ONE purposeful accent.
- **Tells 4, 5, 6, 7 Fired?** **Strip the decoration.** Replace with genuine whitespace, font weight contrast, and clean hairlines.

**Mandatory Gate:** Diagnose first, treat second. Never claim an artifact is finished while compositional tells (3, 8, 10) are still firing.

---

## Variation Discipline & Slide Decks

### 1. The 3-Variation Exploration Rule
When exploring design directions for the user, default to 3 divergent options:
1. **Conservative:** Closest to existing established patterns / lowest implementation risk.
2. **Strong-Fit:** The sharpest, most balanced interpretation of the specific brief.
3. **Divergent:** Novel, bold, exploring boundary aesthetics (layout asymmetry, high contrast, unique type).
*Never produce variations that are merely color swaps.*

### 2. Slide Deck Craft (16:9 Presentation Decks)
When asked for presentation slides:
- Fixed-size canvas: **1920 × 1080 (16:9 widescreen)**.
- Keyboard navigation: Left/Right arrow keys and Spacebar.
- Visible slide counter: e.g. `03 / 12`.
- Slide state persistence: Persist current slide index in `localStorage`.
- Negative space: Keep at least **35% of the slide area empty**.
- Headlines: **28pt–36pt+** summarizing the core takeaway, not generic headers.

---

## Accessibility & Quality Gates

Every component and surface created must satisfy the following non-negotiable gates:

1. **WCAG 2.1 AA Contrast Ratios:**
   - Body copy and interactive labels: **Minimum 4.5:1** contrast against background.
   - Large headings (18pt+ or 14pt bold) and UI border indicators: **Minimum 3:1**.
   - Test both Light mode (`#FAF9F6` or `#FFFFFF`) and Dark mode (`#141413` or `#09090B`).
2. **Touch Target Dimensions:**
   - All interactive controls on mobile and touch viewports must have a minimum physical target size of **44 × 44 pixels** (can use transparent padding / pseudo-elements if visual size is smaller).
3. **Action-Oriented Microcopy:**
   - Write clear, verb-led labels describing the exact outcome:
     - ✅ `"Export Quarterly Report (PDF)"` instead of ❌ `"Submit"` or `"Click here"`.
     - ✅ `"Create Production Workspace"` instead of ❌ `"Save"`.
     - ✅ `"Delete Invoice #1042"` instead of ❌ `"Remove"`.

---

## Built-in Template Gallery (54 Production Archetypes)

This skill includes 54 fully documented design system templates located in `templates/`:

- **SaaS & Cloud:** `stripe.md`, `linear.md`, `vercel.md`, `hashicorp.md`, `clickhouse.md`, `supabase.md`
- **Productivity & Workspace:** `notion.md`, `airtable.md`, `cal.md`, `raycast.md`, `framer.md`, `figma.md`
- **Consumer & Hardware:** `apple.md`, `airbnb.md`, `bmw.md`, `coinbase.md`, `uber.md`, `spotify.md`
- **AI & Modern Labs:** `claude.md`, `elevenlabs.md`, `cohere.md`, `scale.md`, `midjourney.md`

### How to Apply Templates
When the user asks for a specific visual identity (e.g., *"Make it look like Stripe"* or *"Use Linear's dark mode palette"*):
1. Locate and inspect the matching file in `templates/<name>.md`.
2. Extract the exact token definitions: Background hexes, Ink shades, Accent colors, Typography scale, Border radii, and Shadow tokens.
3. Apply those tokens directly to your Mode A or Mode B implementation.

---

## 🔗 Connected Skills
- [[Skills/modern-web-guidance/SKILL|modern-web-guidance]] — มาตรฐาน Web API และเทคนิค CSS ล่าสุด
- [[Skills/canvas/SKILL|canvas]] — สร้าง Live React Canvas สำหรับวิเคราะห์ข้อมูลคู่ขนาน
- [[Skills/document-design/SKILL|document-design]] — แปลงผลงาน UI สู่เอกสารสิ่งพิมพ์และรายงาน Web-to-PDF
- [[Skills/playwright-cli/SKILL|playwright-cli]] — ตรวจสอบภาพหน้าจอและทดสอบ Interaction จริงในเบราว์เซอร์
- [[Skills/playwright-trace/SKILL|playwright-trace]] — วิเคราะห์ Trace เมื่อ UI ทำงานผิดพลาด
- [[Skills/chrome-extensions/SKILL|chrome-extensions]] — พัฒนา UI ในรูปแบบส่วนขยายเบราว์เซอร์
- [[Skills/tdd-workflow/SKILL|tdd-workflow]] — พัฒนา Component ด้วยหลักการ Test-Driven Development
- [[Skills/verification-before-completion/SKILL|verification-before-completion]] — ตรวจสอบและยืนยันคุณภาพก่อนส่งมอบงาน

<!-- v1.1.0 synchronized: 2026-09-29 -->
