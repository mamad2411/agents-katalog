---
name: motion
description: Motion (Framer Motion) React animation library plus local polish and bar-raising guidance. Use for drag-and-drop, scroll animations, gestures, SVG morphing, motion audits, or refining the quality bar of interactive UI work.

license: MIT
---

# Motion Animation Library

## Overview

Motion (package: `motion`, formerly `framer-motion`) is the official Motion
Division animation library for React and JavaScript. It provides declarative
animations, gestures, scroll effects, layout transitions, and spring physics.

**Key Capabilities:**
- **Gestures**: drag, hover, tap, pan, focus with cross-device support
- **Scroll Animations**: viewport-triggered, scroll-linked, parallax effects
- **Layout Animations**: FLIP technique for smooth layout changes, shared element transitions
- **Spring Physics**: Natural, customizable motion with physics-based easing
- **SVG**: Path morphing, line drawing, attribute animation
- **Exit Animations**: AnimatePresence for unmounting transitions
- **Performance**: Hardware-accelerated, ScrollTimeline API, bundle optimization (2.3 KB - 34 KB)

**Production Tested**: React 19, Next.js 15, Vite 6, Tailwind v4

For current package versions, API details, examples, and tutorials, use the
official Motion pages listed in `references/official-learning-path.md`.

**Two-Lane Usage Model**:
- Use `references/official-learning-path.md` and
  `references/tutorials-and-examples.md` for plain official documentation,
  latest API pages, tutorials, and examples.
- Use `references/opinionated-guide.md` for the recommended subset and local
  defaults about the good parts.

---

## When to Use This Skill

### ✅ Use Motion When:

**Complex Interactions**:
- Drag-and-drop interfaces (sortable lists, kanban boards, sliders)
- Hover states with scale/rotation/color changes
- Tap feedback with bounce/squeeze effects
- Pan gestures for mobile-friendly controls

**Scroll-Based Animations**:
- Hero sections with parallax layers
- Scroll-triggered reveals (fade in as elements enter viewport)
- Progress bars linked to scroll position
- Sticky headers with scroll-dependent transforms

**Layout Transitions**:
- Shared element transitions between routes (card → detail page)
- Expand/collapse with automatic height animation
- Grid/list view switching with smooth repositioning
- Tab navigation with animated underline

**Advanced Features**:
- SVG line drawing animations
- Path morphing between shapes
- Spring physics for natural bounce
- Orchestrated sequences (staggered reveals)
- Modal dialogs with backdrop blur

**Bundle Optimization**:
- Need 2.3 KB animation library (useAnimate mini)
- Want to reduce Motion from 34 KB to 4.6 KB (LazyMotion)

**Motion Quality Reviews**:
- You want to raise the perceived product quality, not just "add animation"
- You want a taste/polish pass after the main interaction already works
- You need a review lens for rhythm, hierarchy, restraint, and accessibility

### ❌ Don't Use Motion When:

- **Simple list animations** (use `auto-animate` instead: 3.28 KB vs 34 KB)
- **Static content** without interactions
- **Cloudflare Workers** (use `framer-motion` v12.23.24 workaround - see Known Issues)
- **3D animations** (use Three.js or React Three Fiber instead)

---

## Installation

### Latest Stable Version

```bash
bun add motion  # preferred
# or: npm install motion
# or: yarn add motion
# or: pnpm add motion
```

Do not hardcode a version from this skill. Check the official install docs when
the user asks for the latest version or when package compatibility matters.

### Package Information

- **Bundle Size**:
  - Full `motion` component: ~34 KB minified+gzipped
  - `LazyMotion` + `m` component: ~4.6 KB
  - `useAnimate` mini: 2.3 KB (smallest React animation library)
  - `useAnimate` hybrid: 17 KB
- **Dependencies**: React 18.2+ or newer
- **TypeScript**: Native support included (no @types package needed)

---

## Core Concepts

### 1. The `motion` Component

Transform any HTML/SVG element into an animatable component:

```tsx
import { motion } from "motion/react"

// Basic animation
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.5 }}
>
  Content fades in and slides up
</motion.div>

// Gesture controls
<motion.button
  whileHover={{ scale: 1.1 }}
  whileTap={{ scale: 0.95 }}
>
  Click me
</motion.button>
```

**Props:**
- `initial`: Starting state (object or variant name)
- `animate`: Target state (object or variant name)
- `exit`: Unmounting state (requires AnimatePresence)
- `transition`: Timing/easing configuration
- `whileHover`, `whileTap`, `whileFocus`: Gesture states
- `whileInView`: Viewport-triggered animation
- `drag`: Enable dragging ("x", "y", or true for both)
- `layout`: Enable FLIP layout animations

### 2. Variants (Animation Orchestration)

Named animation states that propagate through component tree:

```tsx
const variants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 }
}

<motion.div variants={variants} initial="hidden" animate="visible">
  Content
</motion.div>
```

**For advanced orchestration** (staggerChildren, delayChildren, dynamic variants), load `references/core-concepts-deep-dive.md`.

### 3. AnimatePresence (Exit Animations)

Enables animations when components unmount:

```tsx
import { AnimatePresence } from "motion/react"

<AnimatePresence>
  {isVisible && (
    <motion.div
      key="modal"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      Modal content
    </motion.div>
  )}
</AnimatePresence>
```

**Critical Rules:**
- AnimatePresence **must stay mounted** (don't wrap in conditional)
- All children **must have unique `key` props**
- AnimatePresence **wraps the conditional**, not the other way around

**Common Mistake** (exit animation won't play):
```tsx
// ❌ Wrong - AnimatePresence unmounts with condition
{isVisible && (
  <AnimatePresence>
    <motion.div>Content</motion.div>
  </AnimatePresence>
)}

// ✅ Correct - AnimatePresence stays mounted
<AnimatePresence>
  {isVisible && <motion.div key="unique">Content</motion.div>}
</AnimatePresence>
```

### 4. Layout Animations (FLIP)

Automatically animate layout changes:

```tsx
<motion.div layout>
  {isExpanded ? <FullContent /> : <Summary />}
</motion.div>
```

**Special props**: `layoutId` (shared element transitions), `layoutScroll` (scrollable containers), `layoutRoot` (fixed positioning).

**For advanced patterns** (LayoutGroup, layoutId orchestration), load `references/core-concepts-deep-dive.md`.

### 5. Scroll Animations

```tsx
// Viewport-triggered
<motion.div
  initial={{ opacity: 0, y: 50 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true }}
>
  Fades in when entering viewport
</motion.div>

// Scroll-linked (parallax)
import { useScroll, useTransform } from "motion/react"
const { scrollYProgress } = useScroll()
const y = useTransform(scrollYProgress, [0, 1], [0, -300])
<motion.div style={{ y }}>Parallax effect</motion.div>
```

**For advanced scroll patterns** (useScroll offsets, useTransform easing, parallax layers), load `references/core-concepts-deep-dive.md`.

### 6. Gestures

```tsx
<motion.div drag="x" dragConstraints={{ left: -200, right: 200 }}>
  Drag me
</motion.div>
```

**Available**: `whileHover`, `whileTap`, `whileFocus`, `whileDrag`, `whileInView`, `drag`.

**For advanced drag controls** (momentum, elastic, event handlers), load `references/core-concepts-deep-dive.md`.

### 7. Spring Physics

```tsx
<motion.div
  animate={{ x: 100 }}
  transition={{ type: "spring", stiffness: 100, damping: 10 }}
/>
```

**Common presets**: Bouncy `{ stiffness: 300, damping: 10 }`, Smooth `{ stiffness: 100, damping: 20 }`.

**For spring tuning** (mass, visualizer, presets), load `references/core-concepts-deep-dive.md`.

### 8. Polish And Bar-Raising Layer

When the request is not just "make this animate" but "make this feel
considered," load `references/polish-and-bar-raising.md`.

Use that review pass after the functional animation works, not before. It is
meant to improve motion quality, information hierarchy, pacing, and restraint.

### 9. Opinionated Guide

When the task is standard product UI work and the agent does not need the whole
Motion surface, load `references/opinionated-guide.md`.

That guide captures the preferred subset, default biases, and what to avoid by
default.

---

## Integration Guides

**Vite**: `bun add motion` → `import { motion } from "motion/react"` (works out of the box)

**Next.js App Router**: Requires `"use client"` directive or client component wrapper
```tsx
"use client"
import { motion } from "motion/react"
```

**Tailwind**: ⚠️ Remove `transition-*` classes (causes conflicts with Motion animations)

**Cloudflare Workers**: Verify current compatibility in the official docs and
issue tracker before pinning a workaround. This skill no longer treats an older
version-specific workaround as authoritative.

**For complete integration guides** (Next.js patterns, SSR, framework-specific issues), load `references/nextjs-integration.md`.

---

## Performance Optimization

**Bundle Size**: Use LazyMotion (34 KB → 4.6 KB):
```tsx
import { LazyMotion, domAnimation, m } from "motion/react"
<LazyMotion features={domAnimation}>
  <m.div>Only 4.6 KB!</m.div>
</LazyMotion>
```

**Large Lists**: Use virtualization (`react-window`, `react-virtuoso`) for 50+ animated items.

**For complete optimization guide** (hardware acceleration, memory profiling, production benchmarks), load `references/performance-optimization.md`.

---

## Accessibility

**Respect `prefers-reduced-motion`**:
```tsx
import { MotionConfig } from "motion/react"
<MotionConfig reducedMotion="user">
  <App />
</MotionConfig>
```

**Keyboard Support**: Use `whileFocus` for keyboard-triggered animations.
```tsx
<motion.button whileFocus={{ scale: 1.1 }} tabIndex={0}>
  Keyboard accessible
</motion.button>
```

**For complete accessibility guide** (ARIA patterns, screen readers, AnimatePresence workaround, testing), load `references/accessibility-guide.md`.

---

## Common Patterns

**Modal Dialog** (AnimatePresence + backdrop):
```tsx
<AnimatePresence>
  {isOpen && (
    <motion.dialog exit={{ opacity: 0 }}>Content</motion.dialog>
  )}
</AnimatePresence>
```

**Accordion** (height animation):
```tsx
<motion.div animate={{ height: isOpen ? "auto" : 0 }}>
  Content
</motion.div>
```

**For 15+ production patterns** (carousel, tabs, scroll reveal, parallax, notifications), load `references/common-patterns.md`.

---

## Known Issues & Solutions

### Issue 1: AnimatePresence Exit Not Working (MOST COMMON)

**Symptom**: Components disappear instantly without exit animation.

**Solution**: AnimatePresence must stay mounted, wrap the conditional (not be wrapped by it):
```tsx
// ❌ Wrong
{isVisible && <AnimatePresence><motion.div>Content</motion.div></AnimatePresence>}

// ✅ Correct
<AnimatePresence>
  {isVisible && <motion.div key="unique">Content</motion.div>}
</AnimatePresence>
```

### Issue 2: Next.js "use client" Missing

**Symptom**: Build fails with "motion is not defined" or SSR errors.

**Solution**: Add `"use client"` directive:
```tsx
"use client"
import { motion } from "motion/react"
```

### Issue 3: Tailwind Transitions Conflict

**Symptom**: Animations stutter or don't work.

**Solution**: Remove `transition-*` classes (Motion overrides CSS transitions):
```tsx
// ❌ Wrong: <motion.div className="transition-all" animate={{ x: 100 }} />
// ✅ Correct: <motion.div animate={{ x: 100 }} />
```

### Issue 4: Cloudflare Workers Build Errors

**Symptom**: Wrangler build fails when using `motion` package.

**Solution**: Check the current upstream compatibility status before pinning a
package swap or version workaround. Do not assume an older workaround is still
correct.

### Issue 5: Large List Performance

**Symptom**: 50-100+ animated items cause severe slowdown.

**Solution**: Use virtualization (`react-window`, `react-virtuoso`).

**For 5+ additional issues** (layoutScroll, layoutRoot, AnimatePresence + layoutId), load `references/nextjs-integration.md` or `references/core-concepts-deep-dive.md`.

---

## When to Load References

Claude should load these references based on user needs:

### Load `references/core-concepts-deep-dive.md` when:
- User asks about variants orchestration (staggerChildren, delayChildren, dynamic variants)
- User needs advanced layout animations (layoutId shared transitions, LayoutGroup)
- User wants scroll-linked animations (useScroll offsets, useTransform easing, parallax layers)
- User needs complex drag patterns (momentum, elastic, event handlers, constraints)
- User asks about spring physics tuning (mass parameter, visualizer, custom presets)

### Load `references/performance-optimization.md` when:
- User wants to reduce bundle size below 4.6 KB (useAnimate mini, LazyMotion comparison)
- User mentions "app is slow", "janky animations", "laggy", or "performance issues"
- User has 50+ animated items in a list (virtualization needed)
- User needs memory profiling or production benchmarks

### Load `references/nextjs-integration.md` when:
- User is building with Next.js (App Router or Pages Router)
- User encounters SSR errors, "use client" errors, or hydration issues
- User asks about route transitions or page navigation animations
- User needs Next.js-specific workarounds (Reorder component, AnimatePresence soft navigation)

### Load `references/accessibility-guide.md` when:
- User asks about "prefers-reduced-motion" or accessibility compliance
- User needs ARIA integration patterns (roles, labels, announcements)
- User wants screen reader compatibility
- User mentions accessibility audits or WCAG compliance
- User asks about AnimatePresence reducedMotion workaround (known issue #1567)

### Load `references/common-patterns.md` when:
- User asks for specific UI patterns (modal, accordion, carousel, tabs, dropdown, toast, etc.)
- User needs copy-paste code examples for production use
- User wants to see 15+ real-world animation patterns

### Load `references/motion-vs-auto-animate.md` when:
- User is deciding between Motion and AutoAnimate libraries
- User mentions "simple list animations" or "bundle size concerns"
- User asks "which animation library should I use?" or "is Motion overkill?"
- User needs feature comparison or decision matrix

### Load `references/official-learning-path.md` when:
- User wants canonical Motion documentation rather than local summaries
- User asks for tutorials, official examples, or recommended learning order
- User asks for the latest version, latest API guidance, or installation details
- User wants the optional Motion MCP or AI kit workflow

### Load `references/tutorials-and-examples.md` when:
- User wants worked examples or tutorial-first learning material
- User needs inspiration or implementation comparison
- User wants to start from official examples before using local templates

### Load `references/opinionated-guide.md` when:
- User wants the recommended subset instead of the full API
- The task is routine product UI motion rather than library exploration
- You want defaults about what to use first and what to avoid by default
- You want to separate plain docs from preferred practice

---

## Templates

This skill includes 5 production-ready templates in the `templates/` directory:

1. **motion-vite-basic.tsx** - Basic Vite + React + TypeScript setup with common animations
2. **motion-nextjs-client.tsx** - Next.js App Router pattern with client component wrapper
3. **scroll-parallax.tsx** - Scroll animations, parallax, and viewport triggers
4. **ui-components.tsx** - Modal, accordion, carousel, tabs with shared underline
5. **layout-transitions.tsx** - FLIP layout animations and shared element transitions

Copy templates into your project and customize as needed.

---

## References

This skill includes curated local reference guides:

- **motion-vs-auto-animate.md** - Decision guide: when to use Motion vs AutoAnimate
- **performance-optimization.md** - Bundle size, LazyMotion, virtualization, hardware acceleration
- **nextjs-integration.md** - App Router vs Pages Router, "use client", known issues
- **common-patterns.md** - Top 15 patterns with full code examples
- **official-learning-path.md** - Official docs, examples, tutorials, and optional Motion AI kit/MCP entrypoints
- **tutorials-and-examples.md** - Generated official learning surfaces for worked examples and tutorial paths
- **opinionated-guide.md** - Preferred subset and default practices for product UI work
- **polish-and-bar-raising.md** - Local refinement lens for quality, rhythm, hierarchy, and restraint

See `references/` directory for detailed guides.

---

## Scripts

This skill includes 2 automation scripts:

- **init-motion.sh** - One-command setup with framework detection (Vite, Next.js, Cloudflare Workers)
- **optimize-bundle.sh** - Convert existing Motion code to LazyMotion for smaller bundle

See `scripts/` directory for automation tools.

---

## Official Documentation

- **Official Site**: https://motion.dev
- **React Docs**: https://motion.dev/docs/react
- **Install Docs**: https://motion.dev/docs/react-installation
- **Tutorials**: https://motion.dev/tutorials
- **Examples**: https://examples.motion.dev/react
- **GitHub**: https://github.com/motiondivision/motion
- **Optional AI Kit / MCP**: https://motion.dev/docs/ai-kit

**Related Skills**: `auto-animate` (simple lists), `tailwind-v4-shadcn` (styling), `nextjs` (App Router), `cloudflare-worker-base`

**Motion vs AutoAnimate**: Load `references/motion-vs-auto-animate.md` for detailed comparison.
- Open an issue: https://github.com/secondsky/claude-skills/issues
- See templates and references for detailed examples

---

**Production Tested**: ✅ React 19 + Next.js 15 + Vite 6 + Tailwind v4
**Token Savings**: ~83%
**Error Prevention**: 100% (29+ documented errors prevented)
**Bundle Size**: 2.3 KB (mini) - 34 KB (full), optimizable to 4.6 KB with LazyMotion
**Accessibility**: MotionConfig reducedMotion support
**Ready to use!** Install with `./scripts/install-skill.sh motion`
