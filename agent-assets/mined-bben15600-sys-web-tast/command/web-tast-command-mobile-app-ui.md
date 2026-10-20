# Mobile App UI/UX Design Skill

## Core Philosophy

Every element serves the user. Design decisions answer three questions:
1. What is the user trying to accomplish?
2. What emotion should they feel?
3. What is the clearest visual hierarchy?

## 5-Step Design Process

### Step 1 — Context Understanding
Identify: app category, user stage (onboarding/returning/power), primary action per screen, relevant industry conventions (fintech ≠ fitness ≠ social).

### Step 2 — UX Structure
- Map the user flow before touching visuals.
- Place primary CTAs in the **thumb zone** (bottom 40% of screen).
- Follow F-pattern reading order for content-heavy screens.
- Turn empty states into guidance: illustration + headline + CTA.
- One primary action per screen.

### Step 3 — Visual Design
**Typography:** Max 1 font family, max 4 sizes (e.g. 28/20/16/12px). Weight conveys hierarchy.
**Color:** 60/30/10 rule — dominant neutral / secondary brand / accent action.
**Spacing:** 8-point grid (`4 8 12 16 24 32 48px`). Consistent rhythm.
**Shadows:** Soft, single-direction (`shadow-sm` to `shadow-lg`). No harsh borders.
**Imagery:** Meaningful, not decorative. Alt text always.

### Step 4 — Emotional Design
"Users remember the peak moment and the last impression."
- Design **celebratory feedback** for key milestones (confetti, checkmark animation, progress rings).
- Micro-animations: 150–300ms, `ease-out` enter, `ease-in` exit.
- Rewarding success states (not just toast — full visual moment).
- Haptic feedback on confirmations.

### Step 5 — Polish
- Glow/inner shadow on primary elements.
- Tap targets minimum **44×44pt** — extend hit area with padding.
- Contrast: 4.5:1 body text, 3:1 large/UI text.
- Design all system states: loading, error, empty, success, offline.
- Test in landscape + portrait.

## Smart Patterns

| Pattern | Implementation |
|---|---|
| Personalized by stage | New: guided tour. Returning: quick access. Power: shortcuts. |
| Search | Recent searches + smart suggestions above keyboard. |
| Progress | Animated rings, step bars — make it visible. |
| Order/status tracking | Color-coded visual timeline. |
| Category selection | Visual cards with color coding > dropdown. |
| Form input | Native keyboard types (`email`, `tel`, `number`). |

## Anti-Patterns to Avoid

- Overused gradients on every surface
- More than 3 font weights per screen
- Arbitrary spacing (not on the 8pt grid)
- Content hidden behind gestures with no affordance
- Primary CTA outside the thumb zone
- Generic "No data" empty states
- Layouts without clear hierarchy

## Technical Stack

```tsx
// Mobile-first base width: 375px
// Tailwind CSS with 8-point spacing
// Lucide React icons (never emoji as icons)
// Recharts for data visualization
// Framer Motion for micro-animations

const THUMB_ZONE_HEIGHT = '60vh'; // bottom 60% of viewport
```

## Screen Archetypes

| Screen | Key pattern |
|---|---|
| Onboarding | Full-bleed hero + single CTA + skip |
| Home/Feed | Card list, sticky filter bar, FAB |
| Detail | Hero media, sticky header-on-scroll, bottom action bar |
| Form | Progressive disclosure, inline validation on blur |
| Profile | Stat summary + action grid + content list |
| Empty state | Centered illustration + headline + primary CTA |
