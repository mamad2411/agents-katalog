# Industrial Brutalist UI Design Skill

## Philosophy

Brutalism in UI rejects the smooth, polished, "friendly" design language of mainstream SaaS. It borrows from industrial design: **raw structure is the aesthetic**. Elements aren't dressed up — they ARE what they are. No shadows for depth, no gradients for warmth, no rounded corners for approachability. Presence through weight, contrast, and deliberate tension.

## Color System

**Stark B&W with a single neon accent:**
```css
:root {
  --bg:      #0A0A0A;   /* near-black */
  --surface: #111111;
  --border:  #FFFFFF;   /* white borders — exposed structure */
  --txt1:    #FFFFFF;
  --txt2:    #AAAAAA;
  --accent:  #00FF88;   /* single neon — green / yellow / orange / hot-pink */
}
/* Light variant: bg #F0F0F0, border #000000, accent stays neon */
```

Rules:
- No gradients — flat fills only.
- No opacity effects on borders — they are always full opacity.
- Accent is used ONCE as a highlight — not repeated across the page.
- Black and white carry the full informational weight.

## Typography

```css
/* Monospace as primary typeface */
font-family: 'JetBrains Mono', 'Fira Code', 'IBM Plex Mono', monospace;

/* OR: condensed grotesque for headlines */
font-family: 'Barlow Condensed', 'Bebas Neue', sans-serif;
font-weight: 700;
letter-spacing: -0.02em; /* tight tracking on headings */
text-transform: uppercase; /* headings always uppercase */
```

Type scale: exaggerated contrast. Headlines at `clamp(3rem, 8vw, 10rem)`. Body at `14–16px` monospace. No middle ground.

## Layout — Exposed Grid

```css
.brutalist-grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 0; /* NO gap — borders create separation */
  border: 2px solid var(--border);
}
.brutalist-grid > * {
  border: 1px solid var(--border); /* every cell has a border */
  padding: 24px;
}
```

Rules:
- Grid lines are VISIBLE — use borders, not gap.
- Asymmetry is intentional: `3:9`, `4:8`, `7:5` column splits.
- Columns can span unexpectedly — tension is the design.
- Overflow visible, text may bleed into adjacent zones.

## Component Patterns

### Buttons
```css
.btn-brutalist {
  border: 2px solid #FFFFFF;
  background: transparent;
  color: #FFFFFF;
  font-family: monospace;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  padding: 12px 24px;
  border-radius: 0; /* NEVER rounded */
  cursor: pointer;
  transition: background 100ms, color 100ms;
}
.btn-brutalist:hover {
  background: #FFFFFF;
  color: #000000;
}
.btn-brutalist.accent {
  border-color: var(--accent);
  color: var(--accent);
}
.btn-brutalist.accent:hover {
  background: var(--accent);
  color: #000000;
}
```

### Cards
```css
.card-brutalist {
  border: 2px solid var(--border);
  border-radius: 0;
  padding: 24px;
  background: var(--surface);
  position: relative;
}
/* Offset shadow instead of drop shadow */
.card-brutalist::after {
  content: '';
  position: absolute;
  inset: 4px -4px -4px 4px;
  border: 2px solid var(--border);
  z-index: -1;
}
```

### Input
```css
.input-brutalist {
  border: 2px solid var(--border);
  border-radius: 0;
  background: transparent;
  color: var(--txt1);
  font-family: monospace;
  padding: 10px 12px;
  outline: none;
}
.input-brutalist:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 2px var(--accent);
}
```

### Navigation
- Full-width `border-bottom: 2px solid` bar.
- Items spaced with `border-right: 1px solid` dividers.
- Active state: accent background, black text.
- No icons — labels only in monospace caps.

## Animation Rules

Brutalist UIs don't hide transitions — they make them mechanical:
```css
/* Instant or very short */
transition: background 80ms step-end; /* digital/binary feel */
/* OR deliberate mechanical */
transition: transform 200ms cubic-bezier(0.25, 0, 1, 1);
```

No smooth easing, no spring physics. Either instant or stiff linear/power curves.

## Signature Elements

- `>` / `_` / `//` text decorators before section headings
- Monospace numbers with tabular-nums
- Blinking cursor `|` animation on interactive elements
- `[LABEL]` bracket notation for metadata
- Horizontal rule `<hr>` as structural divider (full width)
- Status indicators: `● LIVE` / `○ OFFLINE` in monospace

## Checklist

- [ ] Zero border-radius on interactive elements?
- [ ] Grid borders visible (not gaps)?
- [ ] Single neon accent used ≤3 times per screen?
- [ ] All headings uppercase monospace or condensed?
- [ ] No gradients or shadows (except structural offset shadow)?
- [ ] Hover states are binary (inverted) not gradual?
