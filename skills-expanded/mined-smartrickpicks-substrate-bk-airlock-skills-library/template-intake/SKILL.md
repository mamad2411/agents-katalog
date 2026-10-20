---
name: template-intake
description: >
  Curating and cataloging templates dropped into the templates/ directory. ALWAYS use
  this skill when the user adds, pastes, uploads, or mentions a new template — whether
  it's a Vercel export, a zip file, a GitHub clone, or any UI reference. This skill
  runs an interview to capture WHY the template is interesting, tags it by what's
  worth extracting, and writes a structured intake card that other agents and skills
  can reference. Also use when the user says "I found this cool template", "check out
  this UI", "add this to our references", or drops any zip/folder into templates/.
---

# Template Intake

When a new template lands in this repo, don't just file it — **interview the user** to capture the creative intent behind it. This context is what makes the template useful later.

## The Intake Flow

### Step 1: Detect & Scan

When you notice a new template (user drops a zip, mentions a URL, or points to a folder):

1. Scan the template's file structure
2. Identify the tech stack (Next.js, Astro, plain HTML, etc.)
3. Look at the key visual files (CSS, global styles, layout components, animation configs)
4. Note anything that stands out — unusual techniques, interesting patterns, bold choices

### Step 2: The Interview

Ask the user what caught their eye. Frame it conversationally, not like a form. The goal is to capture their creative intent in their own words.

**Core questions** (adapt to context — don't fire all at once):

- "What grabbed you about this one?" — the hook, the first impression
- "Is there a specific element you want to steal?" — a dropdown, a hero animation, a color system, a layout trick, a hover effect
- "Where would you use this?" — which of your projects or components could benefit
- "Does this replace something we have, or is it net new?" — enhancement vs. addition

**Follow-up based on their answer:**

If they mention an **animation or transition**:
- "Is it the timing/easing, the choreography, or the visual effect itself?"
- "Should this become a reusable animation pattern in toolkits/css/animations?"

If they mention a **component** (dropdown, nav, card, hero, etc.):
- "Is this better than what we have in the component library, or is it a different variant?"
- "What makes this version special compared to a standard implementation?"

If they mention a **theme or aesthetic**:
- "Is it the color system, the typography, the spacing, or the overall vibe?"
- "Should this influence our design tokens or is it inspiration for a specific project?"

If they mention a **layout or structural pattern**:
- "Is it the grid system, the responsive behavior, or the spatial composition?"
- "Does this work for content-heavy pages, marketing pages, or dashboards?"

### Step 3: Write the Intake Card

Create a `INTAKE.md` file inside the template's folder. This is the structured record that all agents read.

```markdown
# [Template Name]

**Source**: [URL or "Vercel marketplace" etc.]
**Added**: [date]
**Tech stack**: [Next.js 14 / Astro / plain HTML / etc.]

## Why It's Here

[User's own words about what grabbed them — keep it authentic, not sanitized]

## What to Extract

[Specific elements worth pulling into the component library or toolkits]

Each item gets a tag from the taxonomy below:

- `animation` — [description of the specific animation/transition]
- `component` — [description of the specific component]
- `theme` — [description of the color/type/spacing system]
- `layout` — [description of the structural pattern]
- `interaction` — [description of the hover/click/scroll behavior]
- `technique` — [description of a CSS/JS technique worth learning from]

## Key Files

[Point to the specific files in this template that contain the interesting bits]

- `components/HeroSection.tsx` — the parallax scroll effect
- `styles/globals.css` — the gradient mesh background technique
- `lib/animations.ts` — the staggered reveal orchestration

## Extraction Status

- [ ] Not yet extracted
- [ ] Partially extracted → [link to where patterns landed]
- [ ] Fully extracted → component library updated

## Notes

[Any additional context — gotchas, dependencies, browser support, etc.]
```

### Step 4: Update the Catalog

After writing the intake card, update `templates/_index/catalog.json` so agents can search across all templates by tag, technique, or component type. See the catalog format below.

### Step 5: Flag for Component Library

If any extraction items map to existing components in `component-library/`, note it in the intake card AND create a `component-library/_inbox/` entry so the component-library skill knows there's an upgrade candidate waiting.

## The Catalog Format

`templates/_index/catalog.json` is the searchable index of all templates:

```json
{
  "version": 1,
  "templates": [
    {
      "name": "vercel-portfolio-starter",
      "path": "templates/vercel/portfolio/",
      "source": "Vercel marketplace",
      "added": "2026-03-08",
      "stack": ["next.js", "tailwind", "framer-motion"],
      "tags": ["animation", "layout", "theme"],
      "extractions": [
        {
          "type": "animation",
          "description": "Staggered page-load reveal with spring easing",
          "status": "pending",
          "target": "toolkits/css/animations/"
        },
        {
          "type": "component",
          "description": "Magnetic cursor hover effect on project cards",
          "status": "pending",
          "target": "component-library/official/"
        }
      ],
      "user_notes": "Love the page load feel — everything fades up with this organic spring timing"
    }
  ]
}
```

## Behavior Rules

1. **Always interview** — never silently file a template. The user's intent IS the value.
2. **Keep their voice** — write the "Why It's Here" in their words, not corporate-speak.
3. **Be specific about extractions** — "cool animation" is useless. "Staggered reveal with 80ms delay and cubic-bezier(.16,1,.3,1) easing on the hero section cards" is useful.
4. **Point to files** — always identify the specific source files that contain the interesting bits.
5. **Connect to component library** — every extraction should reference whether it's an upgrade, a variant, or net new relative to what we already have.
6. **One template, one intake** — even if a template has 10 interesting things, they all go in one INTAKE.md with separate extraction items.
