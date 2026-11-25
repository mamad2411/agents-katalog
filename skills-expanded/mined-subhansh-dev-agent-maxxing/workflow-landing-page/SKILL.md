---
name: workflow-landing-page
description: Multi-agent workflow for shipping a conversion-optimized landing page in one day.
---

# Multi-Agent Workflow: Landing Page Sprint

> Ship a conversion-optimized landing page in one day using agent skills.

## The Scenario

You need a landing page for a new product. It needs to look great, convert visitors, and be live by end of day.

## Skills Used

| Skill | Role in this workflow |
|-------|----------------------|
| [Frontend Design](../frontend-design/01-FRONTEND-DESIGN/SKILL.md) | Design the layout and component specs |
| [Writing Style](../content/writing-style/SKILL.md) | Write the copy |
| [Artifact Design](../frontend-design/artifact-design/SKILL.md) | Visual identity and polish |
| [Anti-Patterns](../engineering/anti-patterns/SKILL.md) | Avoid AI-generated looks |
| [Polish](../frontend-design/07-POLISH/SKILL.md) | Final quality pass |

## The Workflow

### Step 1: Research & Plan

```
Load Frontend Design skill.
Analyze the product and target audience.
Decide: hero style, color palette, typography, layout structure.
Output: Design brief with specific choices.
```

### Step 2: Write Copy (Parallel)

```
Load Writing Style skill.
Write landing page copy:
1. Hero (headline + subheadline + CTA)
2. Problem statement (3 pain points)
3. How it works (3 steps)
4. Social proof (testimonial format)
5. Pricing (3 tiers)
6. Final CTA

Tone: confident, concise, slightly playful.
Avoid: AI slop words, hedging, sycophantic openers.
```

### Step 3: Build Layout

```
Load Frontend Design + Artifact Design skills.
Build the HTML/CSS:
- Hero with real image (not SVG gradient)
- Feature cards with icons (not emoji)
- Pricing table with clear hierarchy
- Mobile-responsive throughout
- No purple-blue gradients
- No glassmorphism everywhere
```

### Step 4: Apply Anti-Slop

```
Load Anti-Patterns skill.
Check for:
- Purple-to-blue gradients? → Replace
- Identical card grids? → Add variety
- "Leverage synergies" copy? → Rewrite
- Inter/Roboto fonts? → Pick something better
- Everything centered? → Add asymmetry
```

### Step 5: Polish

```
Load Polish skill.
Final pass:
- Spacing consistency
- Typography hierarchy
- Color contrast
- Animation timing
- Loading states
- Error states
```

## Expected Outcome

A landing page that:
- Looks handcrafted, not AI-generated
- Has real images and specific copy
- Converts with clear CTAs
- Works on mobile and desktop
- Loads fast (no unnecessary dependencies)
