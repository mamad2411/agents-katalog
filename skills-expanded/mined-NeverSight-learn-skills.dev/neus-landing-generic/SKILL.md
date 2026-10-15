---
name: neus-landing-generic
description: |
  Generates a flexible general-purpose landing page with hero, content sections, and CTA.
  Produces a .tsx file using Neus UI Button, Card, and Link. NO AppTemplate.
  Use whenever the user asks for: "landing genérica", "página de presentación", "landing de X"
  (when X is not a SaaS product), "portfolio landing", "landing de empresa", "landing de evento",
  "agency landing", "personal page". Use when neus-landing-saas doesn't fit the context.
od:
  mode: prototype
  platform: web
  scenario: marketing
  design_system:
    requires: true
  inputs:
    - name: page_name
      type: string
      required: true
      description: "Page name or topic"
  craft:
    requires: [anti-slop, neus-components, typescript]
  example_prompt: "Landing page for a design agency with hero, services, and contact form"
---

# Neus Landing Generic

Generates a general-purpose landing with hero, content sections, and CTA. Adapts to the user's purpose.

**IMPORTANT**: No AppTemplate. Public page.

---

## Before starting

The "Shared Rules" section below is always active. Additionally read ALL of these before Phase 0:

- `.agents/skills/_shared/anti-slop.md` — mandatory quality rules ("Marketing Pages" section)
- `.agents/skills/_shared/prop-constraints.md` — forbidden props and non-existent components
- `.agents/skills/_shared/component-catalog.md` — Button, Card, Link, Input sections
- `.agents/skills/_shared/design-personality.md` — personality axis, VISUAL DIRECTIVE format, Section 9 dark mode surface recipes
- `.agents/skills/_shared/dark-surfaces.md` — dark mode CSS recipes (read when Mode: dark)
- `.agents/skills/_shared/light-surfaces.md` — light mode CSS recipes (read when Mode: light)
- `.agents/skills/_shared/checklist.md` — P0/P1/P2 gates
- `.agents/skills/_shared/layout-patterns.md` — landing patterns (stats row, section-head split, hero eyebrow pill, mode-adaptive nav)
- `.agents/skills/neus-landing-generic/references/dark-landing-patterns.md` — section layout anatomy and JSX patterns for dark landings

---

## Phase 0 — Collect Data

Ask the user these questions and wait for their complete reply before proceeding:

---

1. What type of page is it? (portfolio, company, event, agency, blog, personal, other)
2. Page name / brand
3. Main headline (H1) — can include an accent word for gradient treatment
4. Tagline or subheading
5. Sections to include (list exactly — do not add more)
6. Primary CTA: label + action
7. Secondary CTA (optional): label + action
8. Primary theme color (hex or description)
9. **Mode**: light or dark?
10. **Personality**: clean/airy, editorial/layered, bold/kinetic, or structured? (if unsure, describe the vibe)
11. Does it include a contact form or newsletter? (yes/no — specify which)

---

## Phase 1 — Visual Resolution

Before writing any code, resolve the VISUAL DIRECTIVE from the intake answers.

**Palette mapping:**
- Vibrant / energetic colors → Vibrant
- Neutral / muted / gray tones → Neutral
- Corporate blues / greens → Corporate
- Purple / pink / creative → Creative

**Personality mapping from Q10:**
- clean / minimal / airy → Airy
- editorial / layered / asymmetric → Layered
- bold / strong / kinetic → Kinetic
- structured / formal / data-dense → Structured

**Build this block and carry it into Phase 2:**

```
VISUAL DIRECTIVE:
- Palette: [Vibrant / Neutral / Corporate / Creative]
- Personality: [Kinetic / Airy / Structured / Layered]
- Mode: [light / dark]
- Animation: [neus-fade-up on .hero-copy / none]
- Layout: [asymmetric 2-col hero 1.4fr/0.6fr / centered hero]
- H1: [clamp(2.5rem,6vw,4rem) weight-800 / clamp(2rem,4vw,3rem) weight-700]
- Gradient text: [yes — accent word: "[word]" / no]
- Surfaces: [glass (dark-surfaces.md) / standard var(--color-white)]
- Nav: [glass sticky / standard sticky / none]
```

**Dark mode rule:** If `Mode: dark`, ALL surfaces use the recipes from `dark-surfaces.md`. Never use `var(--color-white)` as a page or section background. Use `<Card variant="glass">` for content cards — this is the Neus UI glass surface. Never replace it with a raw `<div>` + custom CSS.

**Light mode rule:** If `Mode: light`, use Neus UI `<Card>` for content cards, `var(--color-primary-light)` for alternating section backgrounds, `var(--color-white)` for the page root.

---

## Phase 2 — P0 Verification

- [ ] Output sections == intake sections (Q5). Zero extras.
- [ ] No invented copy — all text comes from intake or is explicitly prop-driven
- [ ] No AppTemplate or sidebar
- [ ] VISUAL DIRECTIVE built and carried forward
- [ ] Dark mode: all surfaces use glass recipes, no `var(--color-white)` backgrounds
- [ ] Light mode: Neus UI `<Card>` used for content, primary-light for alternating sections

---

## Phase 3 — Generate Artifact

Produce **three files** in this order: `PageName.types.ts` → `PageName.tsx` → `PageName.styles.css`.

---

### PageName.types.ts

```ts
import type { BadgeColor } from 'neus-ui';

export type NavItem = {
  label: string;
  href: string;
};

// Add section-specific types derived from intake only
export type Article = {
  id: string;
  title: string;
  href?: string;
  excerpt?: string;
  author?: string;
  meta?: string;
  categories?: string[];
};

// Category → Badge color mapping (dark mode: 4 visually distinct colors)
export const BADGE_COLOR: Record<string, BadgeColor> = {
  systems:  "primary",
  design:   "error",
  craft:    "neutral",
  tools:    "success",
  featured: "primary",
};

export type PageNameProps = {
  // Props only for data that comes from outside (articles list, form handlers, etc.)
  // Static marketing copy is hardcoded in the component — never as a prop
};
```

---

### PageName.tsx

**Dark mode structure — correct component usage:**

```tsx
import { useState } from 'react';
import { Button, Card, Link, Input, Badge } from 'neus-ui';
import './PageName.styles.css';
import type { PageNameProps, Article } from './PageName.types';
import { BADGE_COLOR } from './PageName.types';

export const PageName = ({ articles, onSubscribe }: PageNameProps) => {
  const [email, setEmail] = useState('');
  const [subscribed, setSubscribed] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSubscribe = () => {
    setLoading(true);
    onSubscribe?.(email);
    setSubscribed(true);
    setLoading(false);
  };

  return (
    <div className="page-name">
      {/* Decorative background layers — aria-hidden, no interaction */}
      <div className="page-name__mesh" aria-hidden="true" />
      <div className="page-name__grid" aria-hidden="true" />

      <div className="page-name__content">
        {/* Sticky glass nav — links use <Link type="secondary"> */}
        <nav className="page-name__nav">
          <div className="page-name__nav-brand">
            <div className="page-name__brand-mark" aria-hidden="true">P</div>
            <span className="page-name__brand-name">PageName</span>
          </div>
          <div className="page-name__nav-links">
            {navItems.map(item => (
              <Link key={item.href} type="secondary" href={item.href} label={item.label} />
            ))}
          </div>
          <Button label="Subscribe" variant="solid" color="primary" size="small" onClick={() => {}} />
        </nav>

        <main>
          {/* Hero — asymmetric 2-col */}
          <section className="page-name__hero" aria-labelledby="page-name-title">
            <div className="page-name__hero-copy">
              {/* Eyebrow pill — raw div (no Neus UI equivalent) */}
              <div className="page-name__eyebrow-pill">
                <span className="page-name__eyebrow-dot" aria-hidden="true" />
                PAGENAME
                <span aria-hidden="true">/</span>
                KEYWORD
              </div>
              <h1 id="page-name-title">
                Headline{" "}
                <span className="gradient-text">accent</span>
              </h1>
              <p className="page-name__hero-sub">Tagline from intake.</p>
              <div className="page-name__hero-cta">
                <Button label="Primary CTA" variant="solid" color="primary" onClick={() => {}} />
                <Button label="Secondary CTA" variant="outlined" color="primary" onClick={() => {}} />
              </div>
            </div>
            <div className="page-name__hero-visual">
              {/* featured Card or art panel — see dark-landing-patterns.md §4 */}
            </div>
          </section>

          {/* Content sections from intake — use <Card variant="glass"> for cards */}
          {/* Example article grid section: */}
          <section className="page-name__articles">
            <div className="page-name__article-grid">
              {articles?.map(article => (
                <Card variant="glass" key={article.id} onClick={() => {}}>
                  <div className="page-name__article-inner">
                    <div className="page-name__pill-row">
                      {article.categories?.map(cat => (
                        <Badge
                          key={cat}
                          variant="solid"
                          color={BADGE_COLOR[cat] ?? "neutral"}
                          label={cat}
                        />
                      ))}
                    </div>
                    <h3>{article.title}</h3>
                    {article.excerpt && <p className="page-name__article-dek">{article.excerpt}</p>}
                  </div>
                </Card>
              ))}
            </div>
          </section>

          {/* Newsletter section (if requested) */}
          <section className="page-name__newsletter" aria-labelledby="page-name-nl-title">
            <div className="page-name__nl-card">
              <p className="page-name__sec-eyebrow">Newsletter</p>
              <h2 id="page-name-nl-title">
                Stay in the loop.{" "}
                <span className="gradient-text">No noise.</span>
              </h2>
              {subscribed ? (
                <p className="page-name__nl-success">✓ You're subscribed — thanks!</p>
              ) : (
                <div className="page-name__nl-form">
                  <Input
                    name="newsletter-email"
                    type="email"
                    label="Email"
                    placeholder="your@email.com"
                    value={email}
                    onChange={setEmail}
                    required
                  />
                  <Button
                    label="Subscribe"
                    type="submit"
                    variant="solid"
                    color="primary"
                    loading={loading}
                    onClick={handleSubscribe}
                  />
                </div>
              )}
            </div>
          </section>
        </main>

        {/* Footer — links use <Link type="secondary"> */}
        <footer className="page-name__footer">
          <span>© {new Date().getFullYear()} PageName.</span>
          <div className="page-name__footer-links">
            <Link type="secondary" href="/privacy" label="Privacy" />
            <Link type="secondary" href="/contact" label="Contact" />
          </div>
        </footer>
      </div>
    </div>
  );
};
```

**Light mode structure:** Omit mesh/grid divs and content wrapper. Use `<Card>` (no variant) for content cards. Alternate section backgrounds with `background: var(--color-primary-light)`. Use `<Link type="primary">` for primary links, `<Link type="secondary">` for nav/footer. Category pills still use `<Badge>`.

**Feature tile (both modes):**
- `<Card variant="glass" icon={...} title="..." description="..." />` (dark)
- `<Card icon={...} title="..." description="..." />` (light)

**Contact form (if requested):** Use Neus UI `<Input>` fields + `<Button type="submit">`. Same pattern as newsletter but without the glow card wrapper.

---

### PageName.styles.css

**Dark mode:** Start with canvas + mesh + grid + content recipes from `dark-surfaces.md §1`. Then add glass nav (`§3`), nl-card (`§4`), eyebrow pill (`§5`), gradient text (`§6`), art panel (`§8` if featured), meta row (`§9` if articles), footer (`§10`). No custom card CSS — `<Card variant="glass">` handles it. Apply layout from `dark-landing-patterns.md`.

**Light mode:** Start with `background: var(--color-white); color: var(--color-gray-900)`. Use `var(--color-primary-light)` for alternating section backgrounds. Follow `design-personality.md` Section 4–5 for typography and spacing.

**Both modes:**

```css
@keyframes neus-fade-up {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}

.page-name__hero-copy {
  animation: neus-fade-up 0.5s ease both;
}

/* Gradient text utility */
.gradient-text {
  background: linear-gradient(135deg, #22d3ee 0%, #818cf8 45%, #d946ef 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Max-width containers */
.page-name__hero,
.page-name__articles,
.page-name__newsletter,
.page-name__footer {
  max-width: min(72rem, 100%);
  margin: 0 auto;
}

/* Section padding */
.page-name__hero       { padding: 6rem 2rem; }
.page-name__articles   { padding: 6rem 2rem; }
.page-name__newsletter { padding: 5rem 2rem; }

/* Hero grid */
.page-name__hero {
  display: grid;
  grid-template-columns: 1.4fr 0.6fr;
  gap: 3rem;
  align-items: center;
}

/* H1 */
.page-name__hero h1 {
  font-family: var(--font-display);
  font-size: clamp(2.5rem, 6vw, 4rem);
  font-weight: 800;
  letter-spacing: -0.04em;
  line-height: 0.98;
  margin: 0.5rem 0 1rem;
}

/* Newsletter form — flex row */
.page-name__nl-form {
  display: flex;
  gap: 1rem;
  align-items: flex-end;
  max-width: 520px;
  margin: 0 auto;
}

/* Article grid */
.page-name__article-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

/* Pill row */
.page-name__pill-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

/* Responsive */
@media (max-width: 960px) {
  .page-name__hero { grid-template-columns: 1fr; }
  .page-name__article-grid { grid-template-columns: 1fr; }
}
@media (max-width: 640px) {
  .page-name__hero,
  .page-name__articles,
  .page-name__newsletter { padding: 5rem 1.25rem; }
}
```

---

## Shared Rules (Embedded)

> These rules are always active. They apply even if `_shared/` files are not read.

### Output — always three files

Every skill output: `ComponentName.types.ts` → `ComponentName.tsx` → `ComponentName.styles.css`.
No inline styles (`style={{}}`). No `<style>` tags inside components. CSS only in `.styles.css`.

### Imports

```tsx
import { Button, Card, Input, Badge, Link, Select, Modal, DataTable } from 'neus-ui';
```

Never import from internal paths like `../../components/Button/Button`.

### Types

All `type` / `interface` declarations → `ComponentName.types.ts`. Never declare types in `.tsx`.

### React 19 — No FormEvent

Never `import { FormEvent } from 'react'`. Use `<Button type="submit" onClick={...} />` instead.

### Component Prop Constraints

- **Button** `variant`: `"solid"` | `"outlined"` | `"text"` — `"ghost"` does NOT exist
- **Button** `color`: `"primary"` | `"success"` | `"error"` | `"info"` | `"white"` — `"white"` for dark canvas only
- **Button** `size`: `"small"` | `"medium"` | `"large"`
- **Card** `variant`: `"default"` | `"glass"` — `"glass"` for dark canvas
- **Badge** `color`: `"primary"` | `"success"` | `"error"` | `"info"` | `"neutral"`
- **Link** `type`: `"primary"` (brand) | `"secondary"` (muted gray)
- **Select**: no `required` prop — handle validation externally
- **FormTemplate**: only `children`, `submitLabel`, `loading` — no `onSubmit`/`onCancel`

### Slop Blacklist

- No inline styles / `style={{}}` / `<style>` tags
- No hardcoded data arrays when data comes from API — use typed props
- No invented copy (fake testimonials, placeholder names, fake metrics)
- No `any` TypeScript type
- No raw `<a>`, `<span>`, `<input>`, `<button>` when a Neus UI component exists
- No hardcoded font stacks — use `var(--font-display)` / `var(--font-mono)`
- In dark mode: no `var(--color-primary-light)` as section background; no raw div cards — use `<Card variant="glass">`
