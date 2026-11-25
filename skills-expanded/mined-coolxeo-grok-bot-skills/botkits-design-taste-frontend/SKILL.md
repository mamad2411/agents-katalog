---
name: botkits-design-taste-frontend
description: >-
  Use when building a landing page, portfolio, or marketing site from a brief, so
  the result looks chosen for this subject instead of like a template. Reads the
  brief, plans tokens, builds, then checks the rendered page.
---
# Design taste: frontend

Build a page that looks like someone made choices for this subject and this audience. Most generated pages fail by reaching for the same defaults every time; this skill exists to stop that.

## 1. Read the brief

Before any code, write a one-line **design read**: what the page is for, who it's for, the one action it should drive, and the mood in three words. Pull it from the brief, linked references, screenshots, existing brand assets, and the audience. If a key piece is missing, ask one question; otherwise state your assumptions and go.

Constraints win over taste: accessibility needs, regulated industries, kids, public sector, or an existing brand system. If the brand has a design system or official component package, use it.

## 2. Plan before building

Write a compact plan and check it against the brief:

- **Color:** 4-6 named hex values with roles (background, text, accent, muted, border).
- **Type:** one or two families, chosen for this subject, with a clear size scale. Body lines under about 75 characters.
- **Layout:** a one-line idea per section plus a rough ASCII wireframe of the hero.
- **The one bold thing:** the single element people will remember. Everything else stays quiet.

Then ask: would I have produced this plan for any similar page? If yes, change that part and say why.

## 3. Defaults to avoid (unless the brief asks)

- Warm cream background with a serif headline and a terracotta accent.
- Near-black page with one neon accent; purple-blue gradients; glow.
- Identical rounded cards with the same soft shadow, used for everything.
- An all-caps eyebrow over every heading, `01 / 02 / 03` markers on content that isn't a sequence, one word in the headline highlighted in a different color.
- Centered hero, three feature cards, logo strip, testimonial carousel, in that order, for every product.
- Fake product screenshots built from divs, stock "Jane Doe" testimonials, invented logos or metrics.
- Fade-and-slide on every section. Use one deliberate motion moment, or none.

## 4. Build

- Real copy written for the end user: plain verbs, sentence case, buttons that say what happens ("Start free trial", not "Submit"). Run headlines through botkits-no-ai-slop. No em dashes in UI copy.
- Real images if they exist. If they don't, leave clearly labeled slots and list them at the end instead of faking them.
- Check that every dependency exists in the project before importing it.
- Quality floor, no announcement needed: responsive to 360px, visible keyboard focus, `prefers-reduced-motion` respected, text contrast at WCAG AA, links are links and buttons are buttons, no `transition: all`.

## 5. Look at it

Open the page in a browser at mobile and desktop widths and take screenshots. Check the hero above the fold, spacing rhythm, contrast, and that the bold thing reads as intended. Fix what looks off, then hand over the screenshots with the code.

## Inspired by

- [Leon Lin, Taste Skill](https://github.com/Leonxlnx/taste-skill) (MIT). Does well: reads the brief before choosing a look, a one-line design read, a long list of generated-design tells, and a ban on fake screenshots. Missing: about 1,200 lines to load, it rules out dashboards and product UI, and it makes dark mode mandatory for consumer pages.
- [Anthropic, frontend-design skill](https://github.com/anthropics/skills/tree/main/skills/frontend-design) (Apache 2.0). Does well: plan a small token system, review it against the brief before building, and spend boldness in one place. Missing: no step to open the rendered page and look at it.
- [Vercel, Web Interface Guidelines](https://github.com/vercel-labs/web-interface-guidelines) (MIT). Does well: a concrete checklist for keyboard, focus, motion, forms, and layout. Missing: no aesthetic direction at all.

## What this version adds

- A short, loadable skill: design read, token plan, defaults to avoid, build, look.
- A browser screenshot check at two widths before handing over.
- Copy rules tied to botkits-no-ai-slop, and an accessibility floor drawn from interface guidelines.
