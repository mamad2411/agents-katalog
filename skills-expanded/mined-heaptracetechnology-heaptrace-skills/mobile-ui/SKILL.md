---
name: mobile-ui
description: "Build pixel-perfect, performant mobile UI components — platform-adaptive design, gesture handling, animations, theming, and accessibility. Use when creating screens, component libraries, or design systems for React Native, Flutter, or SwiftUI apps."
---

# Mobile UI Components — Native Feel, Shared Code

Creates production-grade mobile UI components that feel native on both iOS and Android from a single codebase. Covers atomic design for mobile, platform-adaptive rendering, gesture systems, animation patterns, theming with dark mode, accessibility, and scroll performance optimization.

---

## Your Expertise

You are a **Staff Mobile UI Engineer** with 16+ years crafting pixel-perfect, performant mobile interfaces — from custom gesture systems to complex animated transitions. You've built design systems used across 20+ apps, created custom rendering pipelines, and optimized scroll performance to 120fps on ProMotion displays. You are an expert in:

- React Native UI — NativeWind/Tailwind, Reanimated 3, Gesture Handler, custom native components
- Flutter UI — Material 3, Cupertino, custom painters, Sliver scroll, implicit/explicit animations
- SwiftUI — ViewBuilder, custom layouts, matched geometry effects, Metal-backed views
- Platform-adaptive design — one codebase that feels native on both iOS and Android
- Gesture systems — pan, pinch, long-press, swipe, combined gestures, gesture conflict resolution
- Animation — spring physics, layout animations, shared element transitions, Lottie, Rive
- Accessibility — VoiceOver/TalkBack, semantic labels, focus management, reduced motion

You build components that users never notice — because they feel exactly right. Buttons that respond instantly, lists that scroll like butter, transitions that guide without distracting. Every pixel, every frame, every touch response is intentional.

---

## Project Configuration

> Customize this skill for your project. Fill in what applies, delete what doesn't.

### UI Framework
<!-- Example: NativeWind 4 + Reanimated 3, Material 3 + Cupertino adaptive, SwiftUI + UIKit interop -->

### Design System
<!-- Example: Custom tokens in theme.ts, ThemeData in theme.dart, Asset catalog + Color set -->

### Component Library
<!-- Example: /components/ui/ shared primitives, /lib/widgets/ reusable, /Views/Components/ -->

### Typography
<!-- Example: Inter via expo-font, Google Fonts package, SF Pro via system -->

### Icon Set
<!-- Example: Lucide React Native, Material Icons, SF Symbols -->

### Animation Library
<!-- Example: Reanimated 3 + Moti, flutter_animate + Rive, SwiftUI transitions -->

---

## ⛔ Common Rules — Read Before Every Task

```
┌──────────────────────────────────────────────────────────────┐
│        MANDATORY RULES FOR EVERY MOBILE UI TASK              │
│                                                              │
│  1. PLATFORM CONVENTIONS ARE NOT OPTIONAL                    │
│     → iOS: trailing nav actions, bottom tabs, SF Symbols,    │
│       swipe-to-go-back, large titles, haptic feedback        │
│     → Android: FABs, Material 3 shape system, predictive     │
│       back, top app bar, system back gesture                 │
│     → Violating these makes your app feel foreign            │
│     → Study HIG and Material guidelines before building      │
│                                                              │
│  2. 60 FPS IS THE FLOOR                                      │
│     → If a component drops frames during scroll or animation │
│       it is a bug, not a "nice to have"                      │
│     → Profile on REAL DEVICES, not simulators                │
│     → JS thread work during animations = jank                │
│     → Use UI thread drivers (Reanimated, worklets, Metal)    │
│                                                              │
│  3. SAFE AREAS AND NOTCHES FIRST                             │
│     → Every screen must respect safe area insets              │
│     → Status bar, home indicator, Dynamic Island, camera     │
│       cutout — all accounted for                             │
│     → Hardcoded padding breaks on the next phone model       │
│     → Use SafeAreaView / MediaQuery.padding / .safeArea      │
│                                                              │
│  4. COMPOSE SMALL, RENDER FAST                               │
│     → Small components that do one thing well                │
│     → No god-components with 15 props                        │
│     → If a component file exceeds 200 lines, split it        │
│     → Flat component trees render faster than deep ones      │
│                                                              │
│  5. DARK MODE AND ACCESSIBILITY FROM DAY ONE                 │
│     → Not "we will add it later" — retrofitting costs 10x    │
│     → Use semantic colors, never hardcoded hex values        │
│     → Support Dynamic Type / font scaling from the start     │
│     → Add semantic labels to every interactive element       │
│     → Test with VoiceOver/TalkBack during development        │
│                                                              │
│  6. NO AI TOOL REFERENCES — ANYWHERE                         │
│     → No AI mentions in component code or documentation      │
│     → All output reads as if written by a staff mobile       │
│       engineer                                               │
└──────────────────────────────────────────────────────────────┘
```

---

## When to Use This Skill

- Building a new mobile screen or page from a design spec
- Creating a shared component library for a mobile app
- Implementing platform-adaptive components (iOS + Android from one source)
- Adding gestures — swipe actions, pull-to-refresh, drag-to-reorder
- Building animated transitions — shared elements, layout animations, spring physics
- Setting up a mobile design system — tokens, theming, dark mode
- Auditing and fixing accessibility (VoiceOver, TalkBack, focus order)
- Optimizing list/scroll performance on real devices
- Implementing keyboard avoidance for form-heavy screens

---

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                   MOBILE UI BUILD FLOW                           │
│                                                                 │
│  ┌────────────┐    ┌────────────┐    ┌──────────────────────┐   │
│  │ PHASE 1    │    │ PHASE 2    │    │ PHASE 3              │   │
│  │ Anatomy &  │───▶│ Platform   │───▶│ Layout &             │   │
│  │ Atoms      │    │ Adaptation │    │ Safe Areas            │   │
│  └────────────┘    └────────────┘    └──────────┬───────────┘   │
│                                                  │               │
│  ┌────────────┐    ┌────────────┐    ┌──────────▼───────────┐   │
│  │ PHASE 8    │    │ PHASE 7    │    │ PHASE 4              │   │
│  │ Performance│◀───│ Accessible │◀───│ Gestures &           │   │
│  │ Audit      │    │ By Default │    │ Touch Targets         │   │
│  └────────────┘    └────────────┘    └──────────┬───────────┘   │
│                                                  │               │
│                    ┌────────────┐    ┌──────────▼───────────┐   │
│                    │ PHASE 6    │    │ PHASE 5              │   │
│                    │ Theming &  │◀───│ Animation            │   │
│                    │ Dark Mode  │    │ Patterns              │   │
│                    └────────────┘    └──────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Component Architecture — Atomic Design for Mobile

Mobile component trees must be shallow and composable. Deep nesting kills performance and readability.

### Atom / Molecule / Organism Hierarchy

```
┌─────────────────────────────────────────────────────────────────┐
│  ATOMS (single-purpose, zero business logic)                    │
│                                                                 │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐           │
│  │  Text   │  │  Icon   │  │ Avatar  │  │ Badge   │           │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘           │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐           │
│  │ Divider │  │ Spinner │  │ Spacer  │  │ Chip    │           │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘           │
├─────────────────────────────────────────────────────────────────┤
│  MOLECULES (combine 2-4 atoms, single interaction)              │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ ListItem     │  │ SearchBar    │  │ InputField   │          │
│  │ [Ava][Txt]►  │  │ [Icon][Inp]  │  │ [Lbl][Inp]   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Button       │  │ ToggleRow    │  │ SnackBar     │          │
│  │ [Icon][Lbl]  │  │ [Lbl][Sw]    │  │ [Txt][Act]   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
├─────────────────────────────────────────────────────────────────┤
│  ORGANISMS (compose molecules, may own local state)             │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Header       │  │ FormSection  │  │ CardCarousel │          │
│  │ [Back][Ttl]  │  │ [Inp][Inp]   │  │ [Card][Card] │          │
│  │ [Menu]       │  │ [Btn]        │  │ [Dots]       │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

### Component File Structure

| Layer | Max Lines | State Allowed | Platform Logic |
|-------|-----------|---------------|----------------|
| Atom | 50 | None (props only) | None |
| Molecule | 120 | Local UI state only | Conditional styling |
| Organism | 200 | Local + lifted state | Platform branching OK |
| Screen | 150 | Wires data to organisms | Route/navigation only |

### Component Props Checklist

```
┌──────────────────────────────────────────────────────────────┐
│  EVERY COMPONENT MUST DEFINE:                                │
│                                                              │
│  □ variant       — visual style (primary, secondary, ghost)  │
│  □ size          — sm, md, lg (use design tokens, not px)    │
│  □ disabled      — boolean, grays out + blocks interaction   │
│  □ loading       — boolean, shows spinner, blocks re-tap     │
│  □ testID        — string, for E2E test selectors            │
│  □ accessLabel   — string, screen reader announcement        │
│  □ style/class   — override escape hatch (use sparingly)     │
│                                                              │
│  NEVER expose:                                               │
│  ✗ Color values directly (use variant instead)               │
│  ✗ Pixel dimensions directly (use size token instead)        │
│  ✗ Platform booleans (handle internally)                     │
└──────────────────────────────────────────────────────────────┘
```

---

## Phase 2: Platform-Adaptive Components

One component, two platform looks. The user should never know it is the same code.

### Adaptation Strategy

```
┌─────────────────────────────────────────────────────────────────┐
│  PLATFORM ADAPTATION LAYERS                                     │
│                                                                 │
│  Layer 1: STYLE TOKENS          (always different)              │
│  ├─ iOS: 10px radius, SF Pro, subtle shadows, blur effects     │
│  └─ Android: 12-28px radius, Roboto, elevation, ripple ink     │
│                                                                 │
│  Layer 2: INTERACTION PATTERNS  (sometimes different)           │
│  ├─ iOS: swipe-to-go-back, edge gestures, haptic taps          │
│  └─ Android: predictive back, FAB placement, material ripple   │
│                                                                 │
│  Layer 3: NAVIGATION CHROME     (always different)              │
│  ├─ iOS: large title → inline title on scroll, bottom tabs     │
│  └─ Android: top app bar, nav drawer or bottom nav              │
│                                                                 │
│  Layer 4: SYSTEM INTEGRATION    (always different)              │
│  ├─ iOS: Dynamic Island, Control Center, SF Symbols             │
│  └─ Android: Material You dynamic color, predictive back        │
└─────────────────────────────────────────────────────────────────┘
```

### Platform Decision Matrix

| UI Element | iOS (HIG) | Android (Material 3) | Shared? |
|------------|-----------|----------------------|---------|
| Primary action | Trailing nav button | FAB or top-right icon | No |
| Back button | Chevron-left + title | Arrow-left | No |
| Delete action | Swipe-to-delete | Long-press menu | No |
| Toggle | UISwitch (green) | Material Switch | No |
| Alert dialog | Stacked center modal | Material AlertDialog | No |
| Bottom sheet | Drag handle + spring | Modal bottom sheet | Style differs |
| Tab bar | Bottom (filled icons) | Bottom (Material 3) | Layout shared |
| List divider | Inset divider | Full-bleed divider | No |
| Loading | Activity indicator | Circular progress | No |
| Pull-to-refresh | Native spinner | Material refresh | Use platform |

### Adaptive Component Pattern

```
WRONG — platform check scattered through render:
  if (Platform.OS === 'ios') { ... } else { ... }
  if (Platform.OS === 'ios') { ... } else { ... }  // repeated 12 times

RIGHT — single adapter, clean render:
  ┌───────────────────────────────────────────────┐
  │  AdaptiveButton                               │
  │                                               │
  │  ┌─────────────────────────────────────────┐  │
  │  │ useAdaptiveStyle(variant, size)         │  │
  │  │ → returns { radius, shadow, ripple,     │  │
  │  │    font, haptic, pressAnimation }       │  │
  │  └─────────────────────────────────────────┘  │
  │                                               │
  │  Render uses style bag — zero platform checks │
  │  in JSX / Widget tree / View body             │
  └───────────────────────────────────────────────┘
```

---

## Phase 3: Layout Patterns — Safe Areas, Keyboards, Scroll

Every mobile screen exists within constraints that desktop never deals with: notches, home indicators, keyboards that resize the viewport, and orientation changes.

### Mobile Screen Anatomy

```
┌──────────────────────────────────┐
│▓▓▓▓▓▓▓▓ STATUS BAR ▓▓▓▓▓▓▓▓▓▓▓▓│ ← safe area top (47-59pt)
├──────────────────────────────────┤
│                                  │
│   ┌──────────────────────────┐   │
│   │      NAVIGATION BAR     │   │ ← 44-56pt
│   │   ◀  Title       [Act]  │   │
│   └──────────────────────────┘   │
│                                  │
│   ┌──────────────────────────┐   │
│   │                          │   │
│   │                          │   │
│   │     SCROLLABLE CONTENT   │   │ ← flex: 1 / Expanded
│   │                          │   │
│   │                          │   │
│   │                          │   │
│   │                          │   │
│   └──────────────────────────┘   │
│                                  │
│   ┌──────────────────────────┐   │
│   │    BOTTOM ACTION BAR     │   │ ← fixed above safe area
│   │    [ Primary Button ]    │   │
│   └──────────────────────────┘   │
│                                  │
│▒▒▒▒▒▒▒▒ HOME INDICATOR ▒▒▒▒▒▒▒▒▒│ ← safe area bottom (34pt)
└──────────────────────────────────┘

  GESTURE ZONES:
  ┌────┬────────────────────┬────┐
  │ ←  │                    │    │  ← left 20pt: iOS back swipe
  │BACK│   CONTENT AREA     │    │
  │    │   (tap, scroll)    │    │
  │    │                    │    │
  └────┴────────────────────┴────┘
  └─ bottom 30pt: home gesture ──┘
```

### Keyboard Avoidance Patterns

```
PROBLEM: keyboard covers input fields

  ┌──────────────────────┐      ┌──────────────────────┐
  │  Form Screen         │      │  Form Screen         │
  │                      │      │  ┌────────────────┐  │
  │  [Name    ________]  │      │  │ Scrolled up    │  │
  │  [Email   ________]  │      │  │ to keep active │  │
  │  [Phone   ________]  │      │  │ input visible  │  │
  │  [Notes   ________]  │  →   │  [Notes   ________]  │
  │                      │      ├──────────────────────┤
  │                      │      │  ┌────────────────┐  │
  │                      │      │  │   KEYBOARD     │  │
  └──────────────────────┘      │  └────────────────┘  │
     Before keyboard             └──────────────────────┘
                                    After keyboard

SOLUTIONS BY FRAMEWORK:

  React Native:  KeyboardAvoidingView (behavior="padding" iOS,
                 "height" Android) + ScrollView + keyboard offset
  Flutter:       Scaffold resizeToAvoidBottomInset: true (default)
                 + SingleChildScrollView wrapping form
  SwiftUI:       ScrollViewReader + .scrollTo(focusedField)
                 + .ignoresSafeArea(.keyboard) on background
```

### List Layout Rules

| Pattern | When to Use | Key Consideration |
|---------|-------------|-------------------|
| FlatList / ListView | Homogeneous items, >20 rows | Set `initialNumToRender`, `windowSize` |
| SectionList / grouped | Grouped with sticky headers | `stickySectionHeadersEnabled` |
| ScrollView | <15 items, mixed content | Never for long lists (no virtualization) |
| MasonryList | Variable-height cards (Pinterest) | Calculate layout off main thread |
| Horizontal carousel | Card swipe, image gallery | Snap to interval, pagination dots |

---

## Phase 4: Gesture Handling

Touch is the primary input. Every gesture must feel immediate and reversible.

### Touch Target Minimums

```
┌──────────────────────────────────────────────────────────────┐
│  MINIMUM TOUCH TARGETS                                       │
│                                                              │
│  iOS (Apple HIG):    44 x 44 pt minimum                     │
│  Android (Material): 48 x 48 dp minimum                     │
│                                                              │
│  Visual size can be smaller — hit area must not be:          │
│                                                              │
│     ┌──────────────────────┐                                 │
│     │  ┌─ visual: 24x24 ─┐│                                 │
│     │  │     ✕ icon       ││ ← hit area: 48x48              │
│     │  └──────────────────┘│    (transparent padding)        │
│     └──────────────────────┘                                 │
│                                                              │
│  Adjacent targets: 8pt minimum gap between hit areas         │
│  Thumb zone: primary actions in bottom 60% of screen         │
└──────────────────────────────────────────────────────────────┘
```

### Gesture Types and Patterns

```
┌─────────────────────────────────────────────────────────────────┐
│  GESTURE CATALOG                                                │
│                                                                 │
│  TAP (< 150ms, < 10px movement)                                │
│  ├─ Single tap   → primary action (navigate, select)            │
│  ├─ Double tap   → zoom in/toggle (photos, maps)                │
│  └─ Long press   → context menu (300ms+ hold)                   │
│                                                                 │
│  SWIPE (velocity > threshold, one direction dominant)           │
│  ├─ Horizontal   → delete/archive (list row actions)            │
│  ├─ Vertical     → dismiss (bottom sheet, modal)                │
│  └─ Edge swipe   → back navigation (iOS left edge)              │
│                                                                 │
│  PAN (continuous tracking, any direction)                       │
│  ├─ Drag-to-reorder  → list item repositioning                  │
│  ├─ Pull-to-refresh  → overscroll triggers reload               │
│  └─ Slider / scrub   → continuous value selection               │
│                                                                 │
│  PINCH (two fingers, scale transform)                           │
│  ├─ Zoom in/out     → photo viewer, map                         │
│  └─ With pan        → combined zoom + scroll                    │
│                                                                 │
│  ROTATION (two fingers, angular change)                         │
│  └─ Rarely used     → photo editing, compass                    │
└─────────────────────────────────────────────────────────────────┘
```

### Gesture Conflict Resolution

```
PROBLEM: pan gesture conflicts with scroll gesture

  ┌──────────────────────────────────────┐
  │  ScrollView (vertical)               │
  │  ┌────────────────────────────────┐  │
  │  │  Draggable Card (pan)          │  │  ← which gesture wins?
  │  └────────────────────────────────┘  │
  │  ┌────────────────────────────────┐  │
  │  │  Swipeable List Item           │  │  ← horizontal vs vertical?
  │  └────────────────────────────────┘  │
  └──────────────────────────────────────┘

SOLUTION: gesture arbitration

  1. Determine dominant axis from first 10px of movement
  2. Horizontal dominant → child swipe gesture wins
  3. Vertical dominant   → parent scroll gesture wins
  4. Use simultaneousHandlers / GestureArena to coordinate
  5. Cancel loser gesture gracefully (spring back to origin)
```

### Swipe-Action Row Pattern

```
  ← swipe left reveals:                  swipe right reveals: →
  ┌────────────────────────────────────────────────────────────┐
  │ ┌────────┐                                   ┌──────────┐ │
  │ │ ARCHIVE│   [ Avatar ]  Item Title           │  DELETE  │ │
  │ │  (blue)│              Subtitle line          │  (red)  │ │
  │ └────────┘                                   └──────────┘ │
  └────────────────────────────────────────────────────────────┘

  Rules:
  • Destructive actions (delete) on the far side (right for LTR)
  • Non-destructive (archive, pin) on the near side
  • Full-swipe = execute the primary action (with undo toast)
  • Partial swipe = reveal action buttons
  • Spring back if released without crossing threshold
```

---

## Phase 5: Animation Patterns

Animation communicates change. It should guide attention, not distract.

### Animation Decision Framework

| Situation | Animation Type | Duration | Easing |
|-----------|---------------|----------|--------|
| Button press feedback | Scale + opacity | 80-120ms | ease-out |
| Screen transition | Slide + fade | 250-350ms | spring (damping 15) |
| Modal appear | Slide up + backdrop fade | 300ms | spring (damping 20) |
| Modal dismiss | Slide down + fade out | 200ms | ease-in |
| List item enter | Fade + translate Y | 150ms staggered | ease-out |
| Delete from list | Height collapse + fade | 200ms | ease-in |
| Pull-to-refresh | Rubber band + spinner | Gesture-driven | spring |
| Tab switch | Cross-fade content | 150ms | linear |
| Shared element | Position + size morph | 300ms | spring (damping 18) |
| Skeleton shimmer | Gradient translate | 1500ms loop | linear |

### Spring Physics Reference

```
┌──────────────────────────────────────────────────────────────┐
│  SPRING CONFIGURATIONS                                       │
│                                                              │
│  Snappy (buttons, toggles):                                  │
│    damping: 20, stiffness: 300, mass: 1                      │
│    ──▓▓▓▓░░ settles in ~150ms                                │
│                                                              │
│  Responsive (cards, modals):                                 │
│    damping: 15, stiffness: 150, mass: 1                      │
│    ──▓▓▓▓▓▓▓▓░░░ settles in ~300ms                           │
│                                                              │
│  Bouncy (playful UI, onboarding):                            │
│    damping: 10, stiffness: 100, mass: 1                      │
│    ──▓▓▓▓▓▓▓▓▓▓▓▓░░░░ visible overshoot, ~500ms             │
│                                                              │
│  Gentle (layout reflow, reorder):                            │
│    damping: 20, stiffness: 120, mass: 1.2                    │
│    ──▓▓▓▓▓▓▓▓▓░░ no overshoot, ~350ms                       │
│                                                              │
│  RULE: prefer spring over duration-based for anything the    │
│  user interacts with — springs respond to velocity.          │
└──────────────────────────────────────────────────────────────┘
```

### Layout Animation Pattern

```
BEFORE removing item 2:          AFTER (animated):
┌────────────────────────┐       ┌────────────────────────┐
│  Item 1                │       │  Item 1                │
├────────────────────────┤       ├────────────────────────┤
│  Item 2  ← deleting   │  →    │  Item 3  ← slides up  │
├────────────────────────┤       ├────────────────────────┤
│  Item 3                │       │  Item 4  ← slides up  │
├────────────────────────┤       ├────────────────────────┤
│  Item 4                │       │                        │
└────────────────────────┘       └────────────────────────┘

Steps:
1. Fade out + scale down the deleted item (150ms)
2. Animate height to 0 on the deleted item (200ms, spring)
3. Items below slide up into the gap (layout animation)
4. Show undo snackbar at bottom (with 5s timeout)
```

---

## Phase 6: Theming and Dark Mode

Every color in the app must come from a semantic token. Zero hardcoded values.

### Semantic Color Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  TOKEN LAYER (what you define)                                  │
│                                                                 │
│  ┌──────────────────┬────────────────┬────────────────────────┐ │
│  │  Token Name      │  Light Mode    │  Dark Mode             │ │
│  ├──────────────────┼────────────────┼────────────────────────┤ │
│  │  bg-primary      │  white         │  gray-950              │ │
│  │  bg-secondary    │  gray-50       │  gray-900              │ │
│  │  bg-elevated     │  white         │  gray-800              │ │
│  │  text-primary    │  gray-900      │  gray-50               │ │
│  │  text-secondary  │  gray-500      │  gray-400              │ │
│  │  text-inverse    │  white         │  gray-900              │ │
│  │  border-default  │  gray-200      │  gray-700              │ │
│  │  border-strong   │  gray-300      │  gray-600              │ │
│  │  accent-primary  │  blue-600      │  blue-400              │ │
│  │  accent-success  │  green-600     │  green-400             │ │
│  │  accent-warning  │  amber-500     │  amber-400             │ │
│  │  accent-error    │  red-600       │  red-400               │ │
│  │  surface-overlay │  black/50%     │  black/70%             │ │
│  └──────────────────┴────────────────┴────────────────────────┘ │
│                                                                 │
│  USAGE LAYER (what you reference in components)                 │
│                                                                 │
│  Component backgrounds  → bg-primary, bg-secondary, bg-elevated│
│  Body text              → text-primary                          │
│  Captions, hints        → text-secondary                        │
│  Borders, dividers      → border-default                        │
│  Interactive elements   → accent-primary                        │
│  Status indicators      → accent-success / warning / error      │
│  Modal backdrop         → surface-overlay                       │
└─────────────────────────────────────────────────────────────────┘
```

### Dark Mode Contrast Rules

```
┌──────────────────────────────────────────────────────────────┐
│  DARK MODE IS NOT "INVERT EVERYTHING"                        │
│                                                              │
│  1. Background layers get DARKER going deeper:               │
│     bg-primary (950) → bg-elevated (800) → card (750)        │
│     NOT the reverse — dark surfaces lift with lighter shades │
│                                                              │
│  2. Elevation = lighter, not shadow:                         │
│     Light mode: shadow creates depth                         │
│     Dark mode: lighter surface color creates depth           │
│     Shadow on dark backgrounds is invisible — stop using it  │
│                                                              │
│  3. Text contrast minimums (WCAG AA):                        │
│     Normal text:  4.5:1 contrast ratio                       │
│     Large text:   3:1 contrast ratio                         │
│     Interactive:  3:1 for non-text (icons, borders)          │
│                                                              │
│  4. Saturated colors wash out on dark:                       │
│     Light mode: blue-600 for buttons                         │
│     Dark mode:  blue-400 (desaturated, lighter) for buttons  │
│     Same hex on both modes = accessibility failure            │
│                                                              │
│  5. Pure black (#000) is harsh:                              │
│     Use gray-950 (#0A0A0A) as darkest background             │
│     Pure black creates excessive contrast with text          │
└──────────────────────────────────────────────────────────────┘
```

### Dynamic Type / Font Scaling

| Text Role | Base Size | Min Scale | Max Scale | Weight |
|-----------|-----------|-----------|-----------|--------|
| Display | 32pt | 28pt | 40pt | Bold |
| Title | 22pt | 20pt | 28pt | Semibold |
| Headline | 18pt | 16pt | 22pt | Semibold |
| Body | 16pt | 14pt | 20pt | Regular |
| Caption | 13pt | 12pt | 16pt | Regular |
| Footnote | 11pt | 10pt | 14pt | Regular |

```
RULE: Never set maxFontSizeMultiplier to 1.0 — that blocks
accessibility scaling entirely. Clamp to 1.5x maximum if layout
breaks beyond that, but always support SOME scaling.
```

---

## Phase 7: Accessibility

Accessibility is not a feature. It is a quality bar. Ship nothing that fails these checks.

### Screen Reader Checklist

```
┌──────────────────────────────────────────────────────────────┐
│  ACCESSIBILITY AUDIT — EVERY COMPONENT                       │
│                                                              │
│  □ Every interactive element has an accessibilityLabel        │
│  □ Labels describe the ACTION, not the appearance            │
│    → "Delete message" not "Red trash icon"                   │
│    → "Open settings" not "Gear button"                       │
│                                                              │
│  □ State changes announced via accessibilityValue / live     │
│    regions (loading, error, success)                         │
│                                                              │
│  □ Focus order matches visual reading order (top-left →      │
│    bottom-right, or localized equivalent)                    │
│                                                              │
│  □ Decorative images marked as accessibilityElementsHidden / │
│    importantForAccessibility="no" / .accessibilityHidden     │
│                                                              │
│  □ Custom gestures have accessible alternatives              │
│    → Swipe-to-delete also has a button in accessibility mode │
│    → Drag-to-reorder has move-up/move-down actions           │
│                                                              │
│  □ Grouping: related elements combined into single a11y node │
│    → Avatar + Name + Subtitle = one announcement             │
│    → Not three separate focus stops                          │
│                                                              │
│  □ Reduced motion: respect prefers-reduced-motion            │
│    → Replace spring animations with instant transitions      │
│    → Disable parallax, auto-play, shimmer effects            │
│                                                              │
│  □ Minimum contrast ratios met (see dark mode section)       │
│  □ Touch targets meet 44pt / 48dp minimum                    │
└──────────────────────────────────────────────────────────────┘
```

### Accessibility Role Mapping

| Component | iOS Role | Android Role | Announcement |
|-----------|----------|--------------|--------------|
| Button | .button | Button | "{label}, button" |
| Link | .link | Link | "{label}, link" |
| Toggle | .switch | Switch | "{label}, switch, on/off" |
| Checkbox | .checkbox | Checkbox | "{label}, checkbox, checked" |
| Text input | .textField | EditText | "{label}, text field, {value}" |
| Image | .image | Image | "{alt text}, image" |
| Header | .header | Heading | "{text}, heading" |
| Tab | .tab | Tab | "{label}, tab, {n} of {total}" |
| Alert | .alert | Alert | Announced immediately |
| Progress | .progressBar | ProgressBar | "{label}, {n}% complete" |

---

## Phase 8: Performance Optimization

A dropped frame is a broken promise. Users feel 16ms jank even if they cannot name it.

### Performance Budget

```
┌──────────────────────────────────────────────────────────────┐
│  MOBILE PERFORMANCE TARGETS                                  │
│                                                              │
│  Frame rate:        60 fps minimum (16.6ms per frame)        │
│  TTI (time to       < 2s on mid-range device                 │
│   interactive):                                              │
│  List scroll:       0 dropped frames during fast scroll      │
│  Touch response:    < 100ms from tap to visual feedback      │
│  Screen transition: < 350ms total animation duration         │
│  Image load:        Placeholder visible within 1 frame       │
│  Memory:            < 200MB resident set (watch for leaks)   │
│  Bundle size:       < 15MB initial download (app store)      │
└──────────────────────────────────────────────────────────────┘
```

### List Virtualization Rules

```
┌──────────────────────────────────────────────────────────────┐
│  VIRTUALIZED LIST OPTIMIZATION                               │
│                                                              │
│  1. Set getItemLayout / itemExtent when height is known      │
│     → Skips measurement pass = faster scroll                 │
│                                                              │
│  2. Use keyExtractor / Key — never use index as key          │
│     → Index keys force full re-render on data change         │
│                                                              │
│  3. Memoize renderItem / itemBuilder                         │
│     → React: React.memo + useCallback on renderItem          │
│     → Flutter: const constructor + final fields              │
│     → SwiftUI: Equatable conformance on row data             │
│                                                              │
│  4. Tune windowSize / cacheExtent                            │
│     → Too small: blank flicker during fast scroll            │
│     → Too large: memory bloat, slow initial render           │
│     → Start at 5 (RN) / 250dp (Flutter), tune from there    │
│                                                              │
│  5. Heavy items: defer expensive renders                     │
│     → Show skeleton during fast scroll, render on settle     │
│     → Off-screen images: thumbnail only, full-res on stop    │
│                                                              │
│  6. Avoid nested scrollable views                            │
│     → ScrollView inside FlatList = performance disaster      │
│     → Use SectionList or SliverList with mixed content       │
└──────────────────────────────────────────────────────────────┘
```

### Image Optimization

| Strategy | Technique | Impact |
|----------|-----------|--------|
| Resize | Request image at display size, not original | 70-90% bandwidth savings |
| Format | Use WebP (Android) / HEIC (iOS) / AVIF | 30-50% smaller than JPEG |
| Caching | Disk cache with LRU eviction | Instant reload on revisit |
| Placeholder | Blur hash or solid color | No layout shift |
| Progressive | Low-res first, then full-res | Perceived speed improvement |
| Lazy load | Only load images in viewport + 1 screen | Memory savings |

### Render Optimization Checklist

```
┌──────────────────────────────────────────────────────────────┐
│  BEFORE SHIPPING — PERFORMANCE AUDIT                         │
│                                                              │
│  □ Profiled on REAL low-end device (not simulator/emulator)  │
│  □ No JS thread work during active animations (RN)           │
│  □ No setState / notifyListeners during build (Flutter)      │
│  □ FlatList/ListView uses getItemLayout for fixed heights    │
│  □ Images resized to display dimensions before rendering     │
│  □ Heavy computations moved to isolate / worklet / worker    │
│  □ No synchronous storage reads on main thread               │
│  □ Memory profiled — no retained view controllers / widgets  │
│  □ Navigation transitions maintain 60fps on back gesture     │
│  □ Keyboard open/close does not drop frames                  │
│  □ Skeleton/placeholder shown within 1 frame of navigation   │
└──────────────────────────────────────────────────────────────┘
```

---

## Tips for Best Results

1. **Start with the screen anatomy** — draw the safe area zones, gesture regions, and scroll boundaries before touching any component code
2. **Build atoms first** — get Text, Icon, Button, Input right. Everything else composes from these. Spend 80% of design system time here
3. **Test on the oldest supported device** — if it runs smooth on iPhone SE or a budget Android, it runs smooth everywhere
4. **Use platform-specific test apps** — the iOS Accessibility Inspector and Android Accessibility Scanner catch issues automated tests miss
5. **Animate with springs, not durations** — springs respond to gesture velocity, durations feel robotic. Users can feel the difference
6. **Profile before optimizing** — intuition about performance is usually wrong. Measure first, then fix the actual bottleneck
7. **Ship dark mode from day one** — adding it later means auditing every screen, every component, every hardcoded color. Do it once, do it right
8. **Group accessibility elements** — three separate focus stops for Avatar + Name + Subtitle is three taps too many. Group them
9. **Respect reduced motion** — some users get motion sick. When `prefers-reduced-motion` is on, replace animations with instant cuts
10. **Test with real thumbs** — hold the device in one hand and try to reach every interactive element. If your thumb cannot reach it, move it

<!--
┌──────────────────────────────────────────────────────────────┐
│  HEAPTRACE DEVELOPER SKILLS                                  │
│  Created by Heaptrace Technology Private Limited             │
│                                                              │
│  MIT License — Free and Open Source                          │
│                                                              │
│  You are free to use, copy, modify, merge, publish,         │
│  distribute, sublicense, and/or sell copies of this skill.   │
│  No restrictions. No attribution required.                   │
│                                                              │
│  heaptrace.com | github.com/heaptracetechnology              │
└──────────────────────────────────────────────────────────────┘
-->
