---
name: web-ui-polish
version: 0.3.0
description: Transform rough web pages into premium, polished interfaces with glassmorphism, Apple-inspired layouts, and three switchable themes
category: design
subcategory: ui-enhancement
author: AetherPane Team
license: MIT
allowed_tools:
  - read
  - write
  - bash
  - grep
  - glob
supported_agents:
  - claude-code
  - codex
  - glm
  - kimi
  - minimax
  - cursor
  - windsurf
themes:
  - classic
  - editorial
  - signal
page_types:
  - landing
  - showcase
  - dashboard
  - settings
output_format: html+css
requires:
  - modern browser
  - ES6+ support
tags:
  - ui
  - design-system
  - glassmorphism
  - apple-inspired
  - premium
  - accessibility
---
# Goal
Turn rough or ugly web pages into polished, premium interfaces with strong structure, spacing, typography, restrained motion, thoughtful media usage, and selective use of glass surfaces.
# Use When
- The user wants a page to look better, more premium, more polished, more modern, more Apple-inspired, or more structured
- The task involves landing pages, showcase pages, dashboard shells, settings pages, component galleries, or case-study pages
- The task is web-only
- The task should preserve existing business logic while upgrading presentation quality
# Do Not Use When
- The task is backend-only
- The task is unrelated to presentation or page quality
- The task is for native apps or non-web UI
- The user explicitly wants a raw utility layout with no polish pass
# Workflow
1. Inspect the current page or requested page type
2. Identify the page job before proposing visual changes
3. Fix structure first: section order, hierarchy, spacing, density, and focus
4. Apply an appropriate page pattern based on page type
5. Add surface treatment only where it improves hierarchy
6. Add media only where it improves storytelling or comprehension
7. Add restrained motion only after structure and readability are solid
8. Ensure responsive behavior and maintainable code structure
9. Review consistency across spacing, radii, borders, shadows, and transitions
10. Verify that the result still feels like one system rather than a collage of tricks
# Design Rules
- Avoid cheap glassmorphism
- Favor premium spacing and calm typography
- Use Apple-inspired module rhythm, not imitation for its own sake
- Keep content readable
- Prefer one focal point per section
- Keep visual systems consistent across the page
- Use large media sparingly and intentionally
- Treat media containers as part of the design system
- Use motion to reinforce hierarchy and continuity
- Reserve strong contrast shifts for actions and important state changes
- Let page type drive pattern choice before decoration choices
## Code Examples
### Example 1: Hero Section Before and After
Bad version:
```html
<section class="section">
  <div class="glass" style="padding: 20px;">
    <h1>Launch faster today with better tools and more powerful workflows</h1>
    <p>
      We help teams work better, ship faster, improve performance, stay aligned,
      collaborate better, and scale modern web products with confidence.
    </p>
    <button class="button primary" type="button">Start now</button>
    <button class="button primary" type="button">Book demo</button>
    <button class="button primary" type="button">Learn more</button>
  </div>
</section>
```
Why it is weak:
- The glass surface is doing all the work instead of the layout
- The headline is too broad and the paragraph is too dense
- Three equally loud CTAs create indecision
Improved version:
```html
<section class="page-hero section">
  <div class="page-hero-copy rise">
    <p class="eyebrow">Landing / Marketing</p>
    <h1>
      Premium pages begin with
      <span>clear narrative rhythm</span>
    </h1>
    <p class="lede">
      Lead with one promise, support it with one calm paragraph, and save heavier
      treatment for the surfaces that deserve lift.
    </p>
    <div class="hero-actions">
      <a class="button primary" href="#/showcase">Continue to showcase</a>
      <a class="button secondary" href="#/templates">Review starter templates</a>
    </div>
  </div>
</section>
```
Why it is better:
- `page-hero` and `page-hero-copy` establish hierarchy before effects
- The accent line in `h1 span` creates one premium moment
- The CTA cluster uses one primary and one quieter secondary action
### Example 2: Card Layout Before and After
Bad version:
```html
<section class="section">
  <div style="display: grid; gap: 12px;">
    <div class="glass" style="padding: 12px;">Fast setup</div>
    <div class="glass" style="padding: 12px;">Rich analytics</div>
    <div class="glass" style="padding: 12px;">Unlimited teams</div>
    <div class="glass" style="padding: 12px;">Secure by default</div>
  </div>
</section>
```
Why it is weak:
- Every card is glass, so nothing feels special
- The list has no pacing or supporting copy
- The layout does not adapt the card role to the content
Improved version:
```html
<section class="section card-row">
  <article class="principle-card rise">
    <span>Narrative rhythm</span>
    <p class="card-title">Lead with one idea, then open the system.</p>
    <p>
      Each card should explain one point and stay visually aligned with the rest
      of the family.
    </p>
  </article>
  <article class="principle-card rise" style="animation-delay: 90ms;">
    <span>Surface treatment</span>
    <p class="card-title">Use glass where hierarchy benefits from lift.</p>
    <p>
      Keep primary reading surfaces solid and reserve blur for shells, panels,
      and premium framing moments.
    </p>
  </article>
  <article class="principle-card rise" style="animation-delay: 180ms;">
    <span>Call to action</span>
    <p class="card-title">Finish with a confident next step.</p>
    <p>
      Strong cards still need readable spacing, obvious contrast, and a calm
      support paragraph.
    </p>
  </article>
</section>
```
Why it is better:
- `card-row` gives an intentional grid for three equal-value ideas
- `principle-card` provides consistent padding, shadow, and radius
- The reveal timing is restrained and system-wide
### Example 3: Glass Usage Before and After
Bad version:
```html
<section class="section">
  <div class="glass">
    <div class="glass">
      <div class="glass">
        <h2>Everything is floating</h2>
        <p>Every nested block uses blur, border, and shadow.</p>
      </div>
    </div>
  </div>
</section>
```
Why it is weak:
- Blur stops communicating hierarchy when every layer uses it
- Nested glass causes muddy contrast
- The surface language becomes decorative noise
Improved version:
```html
<section class="section hero-grid">
  <div class="hero-media rise">
    <div class="hero-panel glass">
      <div class="panel-caption">
        <span class="caption-dot"></span>
        Elevated shell
      </div>
      <div class="stage-grid">
        <article class="stage-card spotlight">
          <p>Module 1</p>
          <strong>Use glass on the parent shell only.</strong>
        </article>
        <article class="stage-card">
          <p>Module 2</p>
          <strong>Keep the child cards solid and readable.</strong>
        </article>
      </div>
    </div>
  </div>
  <div class="stacked-cards rise rise-delay">
    <article class="story-card">
      <p class="mini-label">Readability</p>
      <p class="card-title">The glass should frame the section, not flood it.</p>
      <p>
        Use one elevated shell and let the internal cards stay calm so the reading
        order remains obvious.
      </p>
    </article>
  </div>
</section>
```
Why it is better:
- `glass` is reserved for the elevated parent shell
- `stage-card` keeps the internal content grounded
- The section communicates depth with one premium move, not ten
## Common Mistakes
### 1. Hero-only delivery
Bad pattern:
- Only the hero is polished
- The page stops before proof, detail, and CTA
Fix:
- Add full-page rhythm: hero, support section, proof, next step
### 2. Every section has the same visual weight
Bad pattern:
- Equal card density and repeated layout blocks
Fix:
- Alternate densities
- Mix grid sections with single-focus sections
### 3. Too much glass
Bad pattern:
- All cards, lists, forms, and panels use `.glass`
Fix:
- Restrict `.glass` to topbars, sidebars, modals, floating panels, and selected hero shells
### 4. Too many CTAs
Bad pattern:
- Three or more equally styled primary actions in one view
Fix:
- Use one primary action and one quieter secondary action
### 5. Media without a job
Bad pattern:
- Decorative screenshots or loops that do not explain anything
Fix:
- Each media block should either prove a feature or anchor a section
### 6. Motion as decoration
Bad pattern:
- Bouncy or unrelated animations on unrelated elements
Fix:
- Use `.rise` and `.rise-delay` for reveal continuity and small hover shifts only
### 7. Weak heading rhythm
Bad pattern:
- Headline, section title, and body text feel too similar
Fix:
- Use `h1` for the page promise, `h2` for section jobs, `p.lede` for the support line
### 8. Responsive layout collapses too late
Bad pattern:
- Dense two-column or four-column layouts remain unchanged on narrow screens
Fix:
- Respect the current system breakpoints at `1100px` and `720px`
## CSS Class Reference
### Layout and spacing
- `.section`
  Use for standard vertical rhythm between major modules
- `.page-hero`
  Use for top-of-page hero sections that need full-height presence
- `.hero-grid`
  Use for two-column hero compositions with media and supporting story cards
- `.showcase-layout`
  Use for media-led storytelling sections
- `.dashboard-shell`
  Use for sidebar plus working surface dashboards
- `.settings-layout`
  Use for support story plus grouped settings surfaces
- `.component-showcase`
  Use for side-by-side component demonstration sections
- `.cta-band`
  Use for strong closing sections with one message and one action
### Surfaces
- `.glass`
  Use on top-level elevated shells such as topbars, hero foreground panels, modals, drawers, or theme docks
- `.hero-panel`
  Use for the premium foreground shell inside a landing hero
- `.component-surface`
  Use for calm neutral component display containers
- `.story-card`
  Use for readable support cards with one short concept
- `.principle-card`
  Use for higher-emphasis informational cards with a label, title, and supporting copy
- `.settings-panel`
  Use for grouped settings shells
### Content and copy
- `.eyebrow`
  Use for uppercase section labels
- `.mini-label`
  Use for small metadata labels inside cards and controls
- `.lede`
  Use for page-intro support copy
- `.card-title`
  Use for the main title inside cards and utility surfaces
- `.panel-caption`
  Use for short elevated-shell captions above framed content
### Motion
- `.rise`
  Use for the base reveal entrance on major blocks
- `.rise-delay`
  Use for the second item in a paired reveal sequence
### Actions and controls
- `.button.primary`
  Use for the single most important action
- `.button.secondary`
  Use for the quieter companion action
- `.toggle`
  Use for precise utility state switches
- `.segmented-control`
  Use for grouped selection controls and tab-like options
## Responsive Guidelines
### Current system breakpoints
- Above `1100px`
  Multi-column layouts may stay in two-column or dashboard-shell form
- At `1100px` and below
  `hero-grid`, `showcase-layout`, `settings-layout`, `component-showcase`, `dashboard-shell`, `card-row`, `metric-row`, `panel-grid`, `footer`, `cta-band`, and `template-grid` collapse to one column
- At `720px` and below
  The page shell narrows, section padding uses `--space-section-mobile`, and dense controls or media frames need smaller radii and tighter spacing
### Responsive rules to follow
- Collapse layout before content starts to feel cramped
- Do not keep sidebars side-by-side on tablets if the reading width becomes weak
- Preserve headline breathing room even when stacking sections
- Keep `hero-actions` wrapped naturally instead of forcing one line
- Reduce media frame padding on mobile before shrinking the media area too far
- Avoid fixed-width decorative elements inside cards
- Let the page height grow naturally instead of trapping content inside short rigid panels
### Responsive checklist
- Does the hero still read top-to-bottom in a single pass on mobile?
- Does every four-column metric row collapse cleanly?
- Does the footer remain readable when links wrap?
- Does the floating tool or overlay avoid blocking critical CTA content?
- Are `h1` and `h2` still clearly distinct after font scaling?
## Quick Decision Tree
```text
What page type is it?
|
|-- Landing / marketing
|   |-- Need one premium first impression?
|   |   |-- Yes -> Use page-hero + hero-grid + hero-panel glass
|   |   |-- Then -> Add card-row or stacked-cards for proof
|   |   |-- Finish -> Use cta-band
|
|-- Product showcase
|   |-- Need visual proof?
|   |   |-- Yes -> Use showcase-layout + display-frame + timeline-strip
|   |   |-- Keep copy short -> Add InsightCards or story-card stack
|
|-- Dashboard / overview
|   |-- Need dense but readable utility UI?
|   |   |-- Yes -> Use dashboard-shell + ShellNav + MetricGrid + PanelGrid
|   |   |-- Avoid -> Widespread glass on every panel
|
|-- Settings / profile
|   |-- Need grouped controls?
|   |   |-- Yes -> Use settings-layout + settings-panel + settings-group
|   |   |-- Keep motion minimal and actions clear
|
|-- Component gallery or templates
|   |-- Need reusable references?
|   |   |-- Yes -> Use component-showcase or template-grid
|   |   |-- Add copyable code examples and explain usage
```
# Page-Type Guidance
## Landing / Marketing
- Strong hero
- Clear section rhythm
- High visual clarity
- Selective premium media
- Strong CTA ending
- Use `hero-grid`, `story-card`, and `cta-band` heavily
## Product Showcase
- Focus on display and product storytelling
- Use larger media sections
- Support scroll rhythm and reveal transitions
- Keep copy concise
- Use `showcase-layout`, `display-frame`, and `timeline-strip`
## Dashboard / Overview
- Prioritize order, density control, readability, and calm surfaces
- Use media lightly
- Emphasize hierarchy through layout more than decoration
- Use `dashboard-shell`, `metric-row`, and `panel-grid`
## Settings / Profile / Panel
- Prioritize clarity, grouping, and usability
- Use very little large media
- Keep transitions minimal and clean
- Use `settings-panel`, `settings-group`, and `story-card`
# Output Expectations
- Return production-usable frontend code
- Keep code maintainable
- Preserve business logic unless explicitly asked to change it
- Complete the whole page structure, not just a hero block
- Make the result responsive and coherent
- Reuse existing classes and variables before inventing new ones
- Prefer code that can pass the repository test and build flow without extra dependencies
# Final Checklist
- Does the page have one clear job per section?
- Is glass used only where elevation matters?
- Is there one obvious primary action?
- Does the page still feel readable on narrow screens?
- Do spacing, radii, borders, and shadows feel like one family?
- Does the motion stay calm?
- Could another agent pick up this code and extend it without confusion?
