---
name: anti-slop-ui
description: Enforces clean, neutral, human-designed UI aesthetics in FigCraft and eliminates generic AI-generated design clichés ("AI slop") such as gratuitous sparkle badges, loud neon/orange/purple fills, redundant buttons, and emoji icons.
---

# Anti-Slop UI Design System for FigCraft

AI models often default to noisy, over-decorated interfaces ("AI slop"). Apply this skill whenever designing new screens or auditing existing screens in FigCraft so the output looks crafted by a senior product designer (Shadcn UI / Radix / Apple HIG standard).

---

## 1. Banned AI-Slop Patterns (What to Remove Immediately)

1. **Gratuitous AI & Sparkle Badges**:
   - Remove badges like `"✨ Hasil Scan Struk AI"`, `"AI Matched"`, `"✨ Food is your largest category..."`, or `"Rekomendasi otomatis dari AI"` from headers, dropdown triggers, and summary cards.
2. **Loud Colored Input & Dropdown Fills**:
   - Never style form inputs or dropdown triggers with bright orange (`#FFF7ED` / `#EA580C`) or purple (`#F3F0FF` / `#6C5CE7`) backgrounds. Keep triggers neutral (`#FFFFFF` fill, `#CBD5E1` border).
3. **Icons Inside Segmented Tabs**:
   - Do not put red/green arrows (`↗ Expense`, `↙ Income`) or wallet icons inside segmented tab switchers. Use a clean `#F1F2F6` pill track, a `#FFFFFF` active pill, `#1E1E2D` bold active text, and `#8F92A1` muted inactive text.
4. **Redundant Action Buttons & Meta-Labels**:
   - Never place two `+ Add Wallet` buttons on the same screen (e.g., top-right header AND bottom). Place a single clean `+ Add Wallet` button directly below the `TOTAL ASSETS` card.
   - Remove meta-labels above inputs such as `"Scrollable Dropdown"` or `"Kategori Baru Terdeteksi"`.
5. **Unicode Emojis**:
   - Never use Unicode emojis (`🍔`, `🚗`, `💰`, `📈`). Always use `place_lucide_icon` or neutral text rows.

---

## 2. Neutral Design Tokens

| Token | Hex | Usage |
| :--- | :--- | :--- |
| `surface.primary` | `#FFFFFF` | Cards, modals, bottom sheets, active segmented pill, dropdown menu |
| `surface.canvas` | `#F8F9FA` | App screen background for card-based dashboards and reports |
| `surface.input` | `#F8FAFC` | Text inputs, search bars inside dropdowns, neutral secondary buttons |
| `surface.track` | `#F1F2F6` | Segmented switcher background track |
| `surface.selected` | `#F1F5F9` | Selected row highlight inside dropdown menus & scrollbar track |
| `border.subtle` | `#E2E8F0` | Card borders, input borders, dividers |
| `border.default` | `#CBD5E1` | Dropdown trigger border, scrollbar thumb |
| `text.primary` | `#1E1E2D` | Titles, amounts, input values, active tab labels |
| `text.secondary` | `#475569` | Unselected dropdown items, secondary body text |
| `text.muted` | `#8F92A1` | Section labels (`TITLE`, `AMOUNT`, `CATEGORY`), inactive tab labels |
| `text.placeholder` | `#94A3B8` | Input placeholders (`Search category...`, `Tidak ditemukan`) |
| `brand.primary` | `#6C5CE7` | Primary CTA button (`Save Transaction`, `Save Wallet`), FAB `+` |

---

## 3. Standard Component Anatomy

### Searchable & Scrollable Dropdown (`height: 132px..180px`)
- **Trigger (`320 x 42`)**: `#FFFFFF` fill, `#CBD5E1` stroke, `12px` radius, `#1E1E2D` SemiBold value at `x: 14`, `#64748B` `chevronDown` at `x: 290`.
- **Menu Container (`320 x 180`)**: `#FFFFFF` fill, `#E2E8F0` stroke, `12px` radius, subtle drop shadow `#0F172A0D`.
- **Search Bar (`300 x 34` at `10, 10`)**: `#F8FAFC` fill, `#E2E8F0` stroke, `8px` radius, `14px` `#94A3B8` search icon + `Search category...`.
- **Scrollable Rows (`292 x 28`)**:
  - Selected row: `#F1F5F9` fill, `7px` radius, `#1E1E2D` SemiBold text (`x: 12`), `#1E1E2D` `check` icon (`x: 268`).
  - Unselected rows: `#FFFFFF` fill, `#475569` Regular text (`x: 12`). No colorful category icons inside dropdown rows.
- **Scrollbar (`x: 308, y: 50, w: 4, h: 88`)**: Track `#F1F5F9`, Thumb `#CBD5E1` (`h: 32`).
- **Footer / Not-Found Action**:
  - `1px` `#F1F5F9` divider + clean `+ Category Baru` row (`#1E1E2D` SemiBold).
  - When search has no match: 1 line `Tidak ditemukan` (`#94A3B8`) + 1 bordered `#F8FAFC` action row `+ Category Baru "<query>"`.

---

## 4. Multi-Style Presets & Few-Shot Learning

Anti-Slop is **not** restricted to Shadcn neutral design. It is a set of universal quality heuristics. You can request or adopt different style presets via `get_anti_slop_guidelines(style=...)`:

| Preset Style | Canvas | Cards / Surfaces | Accent / Brand | Font Family |
| :--- | :--- | :--- | :--- | :--- |
| `neutral_clean` *(default)* | `#F8F9FA` | `#FFFFFF` (16px radius, subtle border) | `#6C5CE7` | Plus Jakarta Sans |
| `ios_hig` | `#F2F2F7` | `#FFFFFF` (14px radius, hairline border) | `#007AFF` | Inter / SF Pro |
| `material_m3` | `#FEF7FF` | `#F7F2FA` (16px radius, filled tonal) | `#6750A4` | Roboto |
| `dark_modern` | `#09090B` | `#18181B` (16px radius, `#27272A` border) | `#6366F1` | Plus Jakarta Sans |

### Few-Shot Canvas Style Learning
When an existing project already contains established screens:
1. Inspect top-level frames using `list_screens`.
2. Find clean, mature screens (e.g., Screen 4 - Review Transaction, Screen 6 - Manage Wallets in `FinFlow.figcraft`).
3. Imitate the established canvas background, card corner radii, and input field styling rather than imposing a different preset.

