# Website Content Updater

```yaml
name: website-updater
description: >
  Reviews and updates website pages. Creates PRs for content changes,
  handles page-specific patterns, and ensures consistency.
triggers:
  - update the website
  - website copy
  - landing page
  - fix the homepage
```

---

## MCP connectors

| Connector | Purpose |
|-----------|---------|
| GitHub | Push changes, create PRs for site updates |

## Review Workflow

### Step 1: Audit Current State
Before making changes, review:
- Fetch the live page via `WebFetch` to see current copy
- Read the source files in the repo
- Note what needs updating and why

### Step 2: Make Changes
- Edit source files directly
- Follow page-specific patterns (below)
- Maintain consistent voice and formatting across pages

### Step 3: Create PR
```bash
git checkout -b content/website/YYYY-MM-DD-description
# make changes
git add [changed files]
git commit -m "content: update [page] - [what changed]"
# create PR for review
```

### Step 4: Preview
- Run the local dev server if available
- Verify changes render correctly
- Check mobile responsiveness
- Verify all links work

---

## Page-Specific Patterns

### Homepage
- Hero: one sentence value proposition + one sentence supporting detail
- Social proof: specific numbers or customer logos, not vague claims
- CTA: one primary action, one secondary
- Keep above-the-fold tight - no scrolling to understand what you do

### Product/Features Page
- Lead with the problem each feature solves
- Use before/after or with/without framing
- Screenshots or GIFs for every feature
- Keep descriptions to 2-3 sentences per feature

### Pricing Page
- Make the recommended plan obvious
- List what's included, not what's excluded
- Address "What happens when I hit the limit?" upfront
- Include FAQ section for common pricing questions

### About Page
- Team section: real photos, real titles, one sentence per person
- Mission: what you do and why, in 2 sentences
- Values: only if they're specific enough to be actionable

### Blog Index
- Show title, date, author, and reading time
- Category filters should work
- Featured post gets prominent placement

---

## Content Rules

- No em dashes. Use hyphens (-) or colons (:).
- No "cutting-edge", "revolutionary", or "world-class"
- Specific numbers beat vague claims ("500+ teams" beats "many teams")
- Every page should have exactly one primary CTA
- Alt text on every image
- Meta descriptions on every page (under 160 characters)
- Check that Open Graph tags are set for social sharing

## Self-improvement

After the CAO reviews and approves website copy:

1. Move the final version from `_drafts/` to `_published/`
2. Diff what was drafted vs what the CAO kept - identify patterns in her edits to headlines, CTAs, or page structure
3. Update `content/website/_insights.md` with what worked and what she changed
4. If her edits reveal a new rule (e.g. "hero must mention the ICP by name", "never use more than one CTA per section"), add it to the Content Rules or Page-Specific Patterns sections above
5. If a page performs well (high conversion, low bounce), save it to `content/website/_examples/` with performance annotations
