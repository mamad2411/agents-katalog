# UI Design System: High-end Light SaaS (Strict Enforcement)

When generating or modifying React components that use Tailwind CSS, you MUST strictly follow this visual specification to match a premium light SaaS reference.

## 1. Colors

- **Global background**: very light cool off-white — `bg-slate-50`.
- **Card surface**: pure white — `bg-white`, always paired with a subtle border — `border border-slate-100/80`.
- **Primary (tech blue)**:
  - Highlight / primary text: `text-blue-600`.
  - Buttons, progress fills, etc.: `bg-blue-600`.
- **Danger (soft red)**:
  - Text: `text-red-500`.
  - Surfaces: `bg-red-50`.
- **Success (emerald)**:
  - Text: `text-emerald-500`.
  - Surfaces: `bg-emerald-50`.

## 2. Elevation & Shape

- **Corner radii**:
  - Primary cards: `rounded-2xl`.
  - Inner blocks / sub-areas: `rounded-lg` or `rounded-xl`.
  - Progress bars / pill labels: `rounded-full`.
- **Shadows**:
  - Default cards: no shadow (rely on the border for separation).
  - Floating layers or selected states only: very soft shadow — `shadow-[0_4px_20px_-4px_rgba(0,0,0,0.05)]`.

## 3. Typography

- **Section / module titles**: `text-base font-bold text-slate-800`.
- **Body copy**: `text-sm font-medium text-slate-600`.
- **Helper / micro copy**: `text-xs text-slate-400`.

Do not substitute arbitrary colors, radii, or typography tokens outside this system unless the user explicitly overrides it.
