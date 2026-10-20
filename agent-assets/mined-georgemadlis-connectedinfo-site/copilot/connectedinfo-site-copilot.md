# Copilot Instructions for connectedinfo-site

## Project purpose

This repository powers the public website for **ConnectedInfo**.

ConnectedInfo publishes focused fact-checks of AI-assisted queries and widely shared claims. Each published page should begin from a concrete public claim, restate it as a testable question, check it against primary and high-quality secondary sources, and present conclusions with visible limits and uncertainty.

The site is a **static website** deployed with **Cloudflare Pages**.

## Current deployment assumptions

- This is a static site, not a full application framework.
- Public site files live in `site/`.
- The homepage is `site/index.html`.
- Additional articles are standalone HTML files in `site/`.
- Cloudflare Pages should publish from the `site` directory.
- Avoid introducing unnecessary frameworks, build systems, or runtime dependencies unless explicitly requested.

## What Copilot should optimize for

1. **Clarity over cleverness**
   - Prefer plain HTML and CSS.
   - Keep structure simple and inspectable.
   - Avoid hidden logic and unnecessary JavaScript.

2. **Credible publishing**
   - Pages should support serious, evidence-based writing.
   - Design should look calm, readable, and research-oriented.
   - Never make the site look like clickbait or social-media spam.

3. **Static-first architecture**
   - Prefer standalone HTML pages.
   - Prefer shared CSS over per-page styling duplication.
   - Use minimal vanilla JavaScript only when genuinely useful.

4. **Good reading experience**
   - Strong typography
   - Clear hierarchy
   - Comfortable line length
   - Mobile-friendly layout
   - Accessible contrast and semantic markup

5. **Maintainability**
   - Reuse shared header/footer/navigation patterns.
   - Keep filenames stable and human-readable.
   - Do not create complexity that would make hand-editing difficult.

## Content model

ConnectedInfo pages usually follow this structure:

1. Title
2. Claim or question
3. Why this matters
4. Method / how the claim was checked
5. Findings
6. Source notes / references
7. Limits and uncertainty
8. Bottom line

When generating article templates, default to this structure unless asked otherwise.

## Writing style for generated page copy

- Precise
- Sober
- Non-hype
- Evidence-aware
- Explicit about uncertainty
- Avoid overclaiming
- Avoid moralizing unless the page specifically calls for it
- Avoid generic marketing language

Preferred tone:

- "Here is the claim."
- "Here is what we checked."
- "Here is what the evidence supports."
- "Here is what remains unclear."

## HTML guidance

When editing or generating HTML:

- Use semantic tags: `header`, `main`, `article`, `nav`, `section`, `aside`, `footer`
- Use one `h1` per page
- Preserve logical heading hierarchy
- Add useful metadata in `<head>`
- Include:
  - `meta charset="utf-8"`
  - `meta name="viewport" content="width=device-width, initial-scale=1"`
  - descriptive `<title>`
  - useful meta description where appropriate
- Use accessible link text
- Use lists and tables only when they genuinely improve comprehension
- Prefer clean readable markup over deeply nested div structures

## CSS guidance

- Prefer one shared stylesheet when practical
- Design language should feel:
  - minimal
  - trustworthy
  - editorial
  - calm
- Avoid excessive animation
- Avoid flashy gradients unless explicitly requested
- Prefer spacing, typography, and layout over decorative effects
- Ensure responsive behavior for desktop and mobile
- Keep CSS organized by:
  - base
  - layout
  - components
  - article content
  - utilities

## JavaScript guidance

- Use JavaScript only when needed
- Prefer vanilla JS
- Avoid frameworks unless explicitly requested
- Do not introduce build tooling just to support small interactions
- Any JS should progressively enhance the static HTML rather than become required for basic reading

## File and page conventions

Use clear, durable filenames:

- `index.html`
- `about.html`
- `method.html`
- `airport-rules-for-seniors.html`

Slug rules:

- lowercase
- hyphen-separated
- descriptive
- no dates in filenames unless explicitly requested

## Navigation guidance

Default top-level navigation should remain simple. Typical items:

- Home
- Method
- About

Optionally:

- Articles
- Notes
- Sources

Do not bloat navigation.

## Source and citation presentation

When generating article markup, support references cleanly.

Preferred patterns:

- inline footnote markers
- endnotes section
- source list with publication/title/date/link
- separate "Limits" section where appropriate

Do not fabricate citations.
Do not insert placeholder citations that look real.
If placeholder text is needed, mark it clearly as placeholder.

## SEO and sharing guidance

For public pages, prefer basic but solid metadata:

- page title
- meta description
- canonical URL when known
- Open Graph title/description when requested

Do not over-optimize for SEO. The site should read like a credible publication, not a growth-hacking asset.

## Accessibility requirements

Always aim for:

- semantic HTML
- keyboard-usable navigation
- sufficient contrast
- visible focus states
- descriptive alt text for meaningful images
- decorative images marked appropriately
- readable font sizes and spacing

## What to avoid

Do not:

- add React, Next.js, Astro, Tailwind, or other frameworks unless explicitly asked
- add package managers or build steps unless explicitly asked
- add analytics scripts unless explicitly requested
- add dark patterns
- add newsletter popups
- add cookie banners unless actually required
- add autogenerated filler sections
- use fake testimonials, fake author bios, or fake metrics
- turn the site into a generic blog template without preserving ConnectedInfo's research-oriented identity

## Preferred workflow for changes

When asked to make changes:

1. inspect the existing files in `site/`
2. preserve current structure and style where reasonable
3. make the smallest clean change that solves the task
4. avoid unrelated refactors
5. keep deployment compatibility with Cloudflare Pages publishing from `site/`

## If asked to add a new article

Default behavior:

- create a new standalone HTML page in `site/`
- keep visual consistency with homepage
- add a link from `site/index.html` if appropriate
- include sections for:
  - claim
  - method
  - findings
  - limits
  - sources

## If asked to redesign

Preserve these core traits:

- editorial
- calm
- trustworthy
- static
- lightweight
- legible
- evidence-first

Redesign should improve typography, hierarchy, spacing, and navigation before introducing visual novelty.

## Deployment awareness

This site is deployed on Cloudflare Pages.
Assume:

- no server-side runtime
- no database
- no Node requirement unless explicitly introduced
- publish directory is `site`

Any generated solution should work in that environment by default.
