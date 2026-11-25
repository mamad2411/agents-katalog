---
name: ui-color-palettes
description: Twelve professional UI colour palettes with full 50-900 shade scales in HSL and hex, plus semantic error/warning/success ramps, mapped directly onto shadcn CSS variables and Tailwind themes. Use when choosing or defining a product colour system, filling in tailwind.config.ts or globals.css tokens, or fixing a UI that looks generically AI-generated. Includes WCAG-checked text pairings.
---

# UI colour palettes

Twelve palettes, each a full 50–900 scale. Given in **HSL triplets** because that is the format
shadcn's CSS variables take (`--primary: 222 47% 11%`), with hex alongside for design tools.

Pairs with `ui-design-principles` (which governs *how* contrast is used) and `minimalist-ui` or
`impeccable` (which govern the overall aesthetic). This skill only answers: *which colours, and
which shade for which job.*

---

## How to choose

Pick **one** primary and **one** neutral. That is the whole system. Supporting hues are accents,
not co-primaries — a second saturated hue competing with the first is the single most common way a
product UI starts looking amateur.

| If the product is… | Primary | Neutral |
|---|---|---|
| A workspace/document tool, editorial | Slate or Ink | Warm grey |
| Finance, enterprise, trust-forward | Indigo or Navy | Cool grey |
| Developer tooling, technical | Cyan or Teal | True grey |
| Healthcare, calm, care | Teal or Sage | Warm grey |
| Consumer, energetic | Violet or Coral | Cool grey |
| Luxury, restrained | Ink or Bronze | Warm grey |

**Anti-generic rule.** The default AI palette is `#3B82F6` blue on pure `#FFFFFF` with
`#6B7280` grey text. If that is what you have, you have not chosen a palette — you have accepted
one. Shift the primary off the stock hue and give the neutral a temperature.

---

## Neutrals

Neutrals are 80% of a product UI's surface area. Choosing a *tinted* neutral rather than pure grey
is the cheapest way to stop looking templated.

### Warm grey — paper-like, editorial, easy on long reading
```
50  40 20% 98%   #FAFAF9      500 25  6% 46%   #78716C
100 40 12% 96%   #F5F5F4      600 33  5% 32%   #57534E
200 30  8% 91%   #E7E5E4      700 30  6% 25%   #44403C
300 24  6% 83%   #D6D3D1      800 12  6% 15%   #292524
400 24  5% 64%   #A8A29E      900 20 14%  4%   #1C1917
```

### Cool grey — crisp, corporate, screen-native
```
50  210 40% 98%  #F8FAFC      500 215 16% 47%  #64748B
100 210 40% 96%  #F1F5F9      600 215 19% 35%  #475569
200 214 32% 91%  #E2E8F0      700 215 25% 27%  #334155
300 213 27% 84%  #CBD5E1      800 217 33% 17%  #1E293B
400 215 20% 65%  #94A3B8      900 222 47% 11%  #0F172A
```

### True grey — maximum neutrality, lets an accent sing
```
50    0 0% 98%   #FAFAFA      500   0 0% 45%   #737373
100   0 0% 96%   #F5F5F5      600   0 0% 32%   #525252
200   0 0% 90%   #E5E5E5      700   0 0% 25%   #404040
300   0 0% 83%   #D4D4D4      800   0 0% 15%   #262626
400   0 0% 64%   #A3A3A3      900   0 0% 9%    #171717
```

---

## Primaries

### Indigo — trust, enterprise, finance
```
50  226 100% 97% #EEF2FF      500 239 84% 67%  #6366F1
100 226  100% 94% #E0E7FF     600 243 75% 59%  #4F46E5
200 228  96% 89% #C7D2FE      700 245 58% 51%  #4338CA
300 230  94% 82% #A5B4FC      800 244 55% 41%  #3730A3
400 234  89% 74% #818CF8      900 242 47% 34%  #312E81
```

### Cyan — technical, developer tooling, clarity
```
50  183 100% 96% #ECFEFF      500 189 94% 43%  #06B6D4
100 185  96% 90% #CFFAFE      600 192 91% 36%  #0891B2
200 186  94% 82% #A5F3FC      700 193 82% 31%  #0E7490
300 187  92% 69% #67E8F9      800 194 70% 27%  #155E75
400 188  86% 53% #22D3EE      900 196 64% 24%  #164E63
```

### Teal — calm, healthcare, balance
```
50  166  76% 97% #F0FDFA      500 173 80% 40%  #14B8A6
100 167  85% 89% #CCFBF1      600 175 84% 32%  #0D9488
200 168  84% 78% #99F6E4      700 175 77% 26%  #0F766E
300 171  77% 64% #5EEAD4      800 176 69% 22%  #115E59
400 172  66% 50% #2DD4BF      900 176 61% 19%  #134E4A
```

### Violet — creative, consumer, distinctive
```
50  250 100% 98% #F5F3FF      500 258 90% 66%  #8B5CF6
100 251  91% 95% #EDE9FE      600 262 83% 58%  #7C3AED
200 251  95% 92% #DDD6FE      700 263 70% 50%  #6D28D9
300 252  95% 85% #C4B5FD      800 263 69% 42%  #5B21B6
400 255  92% 76% #A78BFA      900 264 67% 35%  #4C1D95
```

### Slate — the quiet default, workspace tools
Use the Cool grey scale above as a primary, taking 800–900 for actions. Deliberately
low-chroma: the interface recedes and the content carries the colour. This is what shadcn ships
with, and it is a legitimate choice — just make the *neutral* warm so the two are distinguishable.

### Ink — near-black primary, luxury and editorial restraint
```
50  240  5% 96%  #F4F4F5      500 240 4% 46%   #71717A
100 240  5% 92%  #E9E9EB      600 240 5% 34%   #52525B
200 240  5% 84%  #D4D4D8      700 240 5% 26%   #3F3F46
300 240  5% 65%  #A1A1AA      800 240 4% 16%   #27272A
400 240  4% 55%  #8B8B93      900 240 6% 10%   #18181B
```

### Navy — institutional, calm authority
```
50  213 100% 96% #EBF3FF      500 217 91% 45%  #0B69D4
100 214  95% 91% #D6E6FF      600 219 85% 38%  #0F55B3
200 215  92% 82% #ADCCFF      700 221 78% 31%  #11418C
300 216  88% 70% #7DACFF      800 223 70% 25%  #12356E
400 217  85% 58% #3D84FA      900 226 60% 19%  #122450
```

### Sage — soft, natural, low-tension
```
50  140 20% 97%  #F5F8F5      500 145 22% 45%  #5A8C6E
100 140 18% 93%  #E6EFE8      600 147 26% 36%  #437054
200 142 16% 85%  #CEDDD3      700 148 28% 28%  #325841
300 143 15% 72%  #ABC3B3      800 150 30% 20%  #23402F
400 144 18% 58%  #85A892      900 152 32% 14%  #17291F
```

### Coral — warm, human, consumer
```
50    9 100% 97% #FFF1EF      500  10 78% 57%  #E85D4A
100  10  95% 93% #FFE0DC      600  10 68% 47%  #C9452F
200  10  92% 86% #FFC4BC      700  10 66% 38%  #A33526
300  10  88% 76% #FF9E92      800  10 62% 30%  #7D291D
400  10  83% 67% #F87A69      900  10 58% 22%  #5A1C14
```

### Amber — attention, warmth, energy
```
50   48 100% 96% #FFFBEB      500  38 92% 50%  #F59E0B
100  48  97% 89% #FEF3C7      600  32 95% 44%  #D97706
200  48  97% 77% #FDE68A      700  26 90% 37%  #B45309
300  46  97% 65% #FCD34D      800  23 83% 31%  #92400E
400  43  96% 56% #FBBF24      900  22 78% 26%  #78350F
```

### Bronze — premium, tactile, understated
```
50   36 33% 96%  #F8F4EF      500  30 38% 45%  #9E6B3F
100  35 30% 91%  #EFE5D9      600  28 42% 36%  #855434
200  34 28% 82%  #DECBB4      700  26 45% 28%  #6B4029
300  32 26% 68%  #C4A583      800  24 48% 21%  #52301E
400  31 31% 56%  #B08554      900  22 50% 15%  #3A2115
```

---

## Semantic colours

Never reuse the primary for state. A success that looks like a button teaches users nothing.

```
Error    50  0 86% 97%  #FEF2F2    500  0 84% 60%  #EF4444    700  0 74% 42%  #B91C1C
Warning  50 48 100% 96% #FFFBEB    500 38 92% 50%  #F59E0B    700 26 90% 37%  #B45309
Success  50 138 76% 97% #F0FDF4    500 142 71% 45% #22C55E    700 142 72% 29% #15803D
Info     50 204 100% 97% #F0F9FF   500 199 89% 48% #0EA5E9    700 201 90% 34% #0369A1
```

Use **50** for backgrounds, **500** for icons and borders, **700** for text on the 50 background.
`500` on white is usually *not* accessible for body text — see below.

---

## WCAG pairings

Verified combinations. Body text needs **4.5:1**; large text and UI boundaries need **3:1**.

| Foreground | Background | Ratio | Safe for |
|---|---|---|---|
| neutral-900 | neutral-50 | ~17:1 | anything |
| neutral-700 | white | ~8.6:1 | body text |
| neutral-500 | white | ~4.6:1 | body text, only just |
| neutral-400 | white | ~2.8:1 | **decorative only** — never body text |
| white | primary-600 | ~5–7:1 | button labels |
| white | primary-500 | ~3–4:1 | large text only; check per hue |
| error-700 | error-50 | ~7:1 | error messages |

**The recurring mistake:** `neutral-400` as "muted text". It fails at 2.8:1. Muted body text is
`neutral-500` minimum, and `neutral-600` if it matters.

---

## Mapping to shadcn

shadcn reads HSL **without** `hsl()` and without commas. Fill `styles/globals.css`:

```css
:root {
  --background:          0 0% 100%;
  --foreground:          <neutral-900>;
  --card:                0 0% 100%;
  --card-foreground:     <neutral-900>;
  --popover:             0 0% 100%;
  --popover-foreground:  <neutral-900>;
  --primary:             <primary-600>;
  --primary-foreground:  0 0% 100%;
  --secondary:           <neutral-100>;
  --secondary-foreground:<neutral-900>;
  --muted:               <neutral-100>;
  --muted-foreground:    <neutral-500>;
  --accent:              <neutral-100>;
  --accent-foreground:   <neutral-900>;
  --destructive:         0 84% 60%;
  --destructive-foreground: 0 0% 100%;
  --border:              <neutral-200>;
  --input:               <neutral-200>;
  --ring:                <primary-600>;
  --radius:              0.5rem;
}

.dark {
  --background:          <neutral-900>;
  --foreground:          <neutral-50>;
  --card:                <neutral-800>;
  --primary:             <primary-400>;   /* lighter: 600 is too dark on a dark ground */
  --primary-foreground:  <neutral-900>;
  --muted:               <neutral-800>;
  --muted-foreground:    <neutral-400>;
  --border:              <neutral-700>;
  --input:               <neutral-700>;
}
```

**Dark mode is not an inversion.** Two rules that are always violated:

1. The primary must get *lighter* (use 400), not stay at 600 — a mid-dark hue on a dark ground
   loses all contrast.
2. Surfaces get lighter as they rise. Background `neutral-900`, card `neutral-800`, popover
   `neutral-700`. In light mode the opposite: background white, card white with a border, elevated
   surfaces cast shadow instead. Never use shadow for elevation in dark mode — it is invisible.

---

## Checklist

1. One primary, one neutral. Supporting hues are accents only.
2. The neutral has a temperature, or you chose true grey deliberately.
3. The primary is not stock `#3B82F6`.
4. Semantic colours are distinct from the primary.
5. Every pairing checked against the WCAG table; no `neutral-400` body text.
6. Dark mode lightens the primary and lightens surfaces as they rise.
7. Colours live in tokens. No hex literals in components.
8. Nothing is communicated by colour alone.
