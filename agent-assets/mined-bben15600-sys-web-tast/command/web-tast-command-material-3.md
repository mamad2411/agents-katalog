# Material Design 3 (Material You) Skill

## Core Concepts

Material 3 is built on three pillars:
1. **Dynamic Color** — tonal palettes generated from user's wallpaper or brand seed color
2. **Expressive Motion** — physics-based, purposeful animation (spring curves, emphasis arcs)
3. **Adaptive Layouts** — compact → medium → expanded breakpoints

## Color System

M3 generates a complete set of tonal palettes from a single seed color:

```dart
// Flutter: MaterialApp with ColorScheme.fromSeed
MaterialApp(
  theme: ThemeData(
    colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF006874)),
    useMaterial3: true,
  ),
)
```

### Color Roles
| Role | Purpose |
|---|---|
| `primary` | Key UI elements — buttons, active states |
| `on-primary` | Text/icons on primary |
| `primary-container` | Prominent background for primary components |
| `on-primary-container` | Text on primary-container |
| `secondary` | Complementary — filter chips, tabs |
| `tertiary` | Contrasting accent |
| `surface` | Background of cards, sheets |
| `surface-variant` | Alternative surface tone |
| `outline` | Borders, dividers |
| `error` + `on-error` | Error states |

**Rule:** Never use hex directly in components. Always reference `colorScheme.<role>`.

## Typography Scale (Type Roles)

```dart
// M3 type roles — map to semantic usage
displayLarge   // 57sp — hero, splash
displayMedium  // 45sp
displaySmall   // 36sp
headlineLarge  // 32sp — page headers
headlineMedium // 28sp
headlineSmall  // 24sp
titleLarge     // 22sp — app bar title
titleMedium    // 16sp, medium weight — card titles
titleSmall     // 14sp, medium weight
bodyLarge      // 16sp — primary body
bodyMedium     // 14sp — secondary body
bodySmall      // 12sp
labelLarge     // 14sp, medium — buttons, tabs
labelMedium    // 12sp
labelSmall     // 11sp — captions, badges
```

## Elevation & Surfaces

M3 uses **tonal color** for elevation, not shadows:
```
Level 0: surface (no overlay)
Level 1: +5% primary overlay  — cards, menus
Level 2: +8%                   — floating buttons
Level 3: +11%                  — dialogs, navigation drawers
Level 4: +12%                  — FAB pressed
Level 5: +14%                  — navigation bars
```

```css
/* Web implementation */
--md-elevation-1: color-mix(in srgb, var(--md-primary) 5%, var(--md-surface));
```

## Components

### Buttons (5 variants by emphasis)

| Variant | Use |
|---|---|
| Filled | Primary action (highest emphasis) |
| Filled Tonal | Secondary action |
| Outlined | Medium emphasis |
| Text | Low emphasis — inline actions |
| Elevated | Subtle, shadow-based |

```html
<!-- Web: material-web library -->
<md-filled-button>Primary Action</md-filled-button>
<md-outlined-button>Secondary</md-outlined-button>
<md-text-button>Cancel</md-text-button>
```

### Navigation

| Screen size | Pattern |
|---|---|
| Compact (< 600dp) | Navigation Bar (bottom, 3–5 icons) |
| Medium (600–840dp) | Navigation Rail (left side) |
| Expanded (> 840dp) | Navigation Drawer (persistent left) |

### Cards (3 variants)
- **Elevated** — default, subtle shadow
- **Filled** — surface-variant background, no shadow
- **Outlined** — border only, no shadow/fill

### FAB
- FAB (56dp) — primary action
- Small FAB (40dp) — secondary placement
- Large FAB (96dp) — prominent single action
- Extended FAB — icon + text label, most affordance

## Motion

M3 defines 5 easing curves:
```
Emphasized:          cubic-bezier(0.2, 0, 0, 1.0)    — large spatial transitions
Emphasized Decelerate: cubic-bezier(0.05, 0.7, 0.1, 1.0)  — elements entering
Emphasized Accelerate: cubic-bezier(0.3, 0, 0.8, 0.15)    — elements exiting
Standard:            cubic-bezier(0.2, 0, 0, 1.0)    — simple spatial
Linear:              linear                           — color, opacity fades
```

Duration tokens:
- Short (50–200ms): micro-interactions, icon animations
- Medium (250–400ms): transitions within a screen
- Long (450–600ms): full-screen transitions, complex sequences

## Adaptive Layout Breakpoints

```css
/* Window size classes */
@media (max-width: 599px)   { /* Compact — phone portrait */ }
@media (min-width: 600px)   { /* Medium — phone landscape, tablet portrait */ }
@media (min-width: 1240px)  { /* Expanded — tablet landscape, desktop */ }
```

Behavior per breakpoint:
- **Compact**: single column, bottom nav, full-width sheets
- **Medium**: two-column optional, rail nav, side sheets
- **Expanded**: two/three columns, persistent drawer, inline dialogs

## State Layers

M3 communicates interaction via tonal overlays:
```
Hovered: +8% on-color overlay
Focused: +10% on-color overlay
Pressed: +10% on-color overlay (with ripple)
Dragged: +16% on-color overlay
Disabled: 38% opacity
```

```css
.md-button:hover::before {
  content: '';
  background: currentColor;
  opacity: 0.08;
  position: absolute;
  inset: 0;
  border-radius: inherit;
}
```

## Icons

Use **Material Symbols** (variable font — fill, weight, grade, optical size axes):
```html
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0" rel="stylesheet">
<span class="material-symbols-outlined">favorite</span>
```

Prefer **Outlined** style for most UI; **Filled** for active/selected states.
