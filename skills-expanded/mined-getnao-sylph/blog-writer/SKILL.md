# Blog Article Writer

```yaml
name: blog-writer
description: >
  Writes, designs, and publishes blog articles for the company website.
  Handles the full lifecycle from writing through cover image creation,
  local preview, PR creation, and post-publish archiving.
triggers:
  - blog post
  - blog article
  - write a blog about
  - publish to the blog
```

---

## MCP connectors

| Connector | Purpose |
|-----------|---------|
| GitHub | Create PR for blog post, push to repo |
| Canva | Create cover images and blog graphics |

## Website Frontmatter Format

Every blog article must include this frontmatter. Adjust field names to match your static site generator.

```yaml
---
title: "Article Title Here"
description: "One sentence meta description for SEO (under 160 characters)"
date: YYYY-MM-DD
author: "[Author Name]"
author_role: "[Author Title]"
category: "[Category from the list below]"
tags: ["tag1", "tag2", "tag3"]
image: "/images/blog/YYYY-MM-DD-slug/cover.png"
image_alt: "Descriptive alt text for the cover image"
draft: false
featured: false
reading_time: "[X] min read"
---
```

### Categories

Use one of these categories (or define your own):

- Engineering
- Product Updates
- Benchmarks
- How-To Guides
- Company News
- Community
- Industry Analysis
- Customer Stories

---

## Voice and Style Rules

### Core Rules
- No em dashes (--) or en dashes. Use hyphens (-) or colons (:).
- Direct openings. Never start with "In today's world..." or "As we all know..."
- Evidence over assertion. Don't say "powerful" - show what it does.
- First person for personal experience, second person for instructions.
- Short paragraphs. 3-4 sentences max per paragraph.

### Opening Patterns
Strong blog openings:
- **Problem statement**: "Most data teams waste 3 hours a day on tasks that should take 10 minutes."
- **Specific finding**: "We tested 5 approaches to [X]. Only one consistently worked."
- **Story**: "Last Tuesday, a customer asked us something we couldn't answer. So we built it."

Weak openings (never use):
- "We're excited to share..."
- "In the ever-evolving landscape of..."
- "Today we're announcing..."

### Readability
- Use H2 for main sections, H3 for subsections
- Include a table of contents for articles over 1500 words
- Use code blocks for any technical content
- Use tables for comparisons
- Include images/diagrams where they add clarity
- Bold key terms on first use
- Link to related posts and external references

---

## Article Structure Patterns

### Benchmark Article
```
[Hook: the question you're answering]
[Methodology: what you tested, how]
[Results: data in tables or charts]
[Analysis: what the data means]
[Limitations: what this doesn't cover]
[Conclusion: the actionable takeaway]
```

### How-To Guide
```
[Problem: what the reader will accomplish]
[Prerequisites: what they need before starting]
[Steps: numbered, with code/screenshots]
[Verification: how to confirm it worked]
[Troubleshooting: common issues]
[Next steps: where to go from here]
```

### Product Update
```
[The problem this solves]
[What we built]
[How it works (with screenshots/examples)]
[Who this is for]
[What's next]
[CTA: try it]
```

### Multi-Feature Launch
```
[The theme connecting all features]
[Feature 1: problem + solution + screenshot]
[Feature 2: problem + solution + screenshot]
[Feature 3: problem + solution + screenshot]
[The bigger picture: where this is heading]
[CTA: try it / read more]
```

### Community Recap
```
[The event/milestone in one sentence]
[What happened - highlights]
[Key takeaways or quotes]
[What's next for the community]
[CTA: join / follow / attend next time]
```

---

## Cover Image Workflow

Every blog post needs a cover image. Three paths:

### Path 1: User-Provided Image
The user provides an image file or URL. Use it directly.
- Ensure it meets size requirements (typically 1200x630px for social sharing)
- Add descriptive alt text in the frontmatter

### Path 2: Reuse Existing Template
Check `brand/templates/blog-covers/` for existing cover templates.
- Swap the title text and any dynamic elements
- Maintain brand colors and typography

### Path 3: Create via Design Tool
If a design tool MCP is available (e.g., Canva):
- Use the brand's blog cover template
- Set the title text, subtitle, and any category badge
- Export at the correct dimensions
- Save to the blog images directory

---

## Publish Workflow

### Step 1: Create Branch
```bash
git checkout -b content/blog/YYYY-MM-DD-slug
```

### Step 2: Write Article
- Save the article file to the blog content directory (e.g., `content/blog/YYYY-MM-DD-slug.md`)
- Save the cover image to the images directory
- Ensure all frontmatter fields are filled

### Step 3: Commit and Create PR
```bash
git add content/blog/YYYY-MM-DD-slug.md images/blog/YYYY-MM-DD-slug/
git commit -m "content: publish blog article - [title]"
```

Create a PR with:
- Title: "content: [article title]"
- Body: summary of the article, target publish date, any review notes

### Step 4: Preview
If a local preview is available, start the dev server and verify:
- Article renders correctly
- Cover image displays properly
- Meta tags are correct for social sharing
- Links work
- Code blocks render with syntax highlighting

---

## Post-Publish Steps

After the article is live:

1. **Move to _published**: Copy the draft from `content/blog/_drafts/` to `content/blog/_published/`
2. **Update status**: Change `draft: true` to `draft: false` in frontmatter
3. **Update _insights**: Add an entry to `content/blog/_insights.md`:
   ```
   ## YYYY-MM-DD - [Title]
   - Topic: [topic]
   - Category: [category]
   - Performance: [add metrics after 7 days]
   - Notes: [anything learned from writing or publishing]
   ```
4. **Cross-promote**: Consider creating LinkedIn, X, or newsletter posts to drive traffic

---

## Review Checklist

Before creating the PR:

- [ ] Title is specific and under 70 characters
- [ ] Meta description is under 160 characters and includes the key topic
- [ ] Cover image is present and has alt text
- [ ] Opening sentence creates interest (no weak openers)
- [ ] H2/H3 structure is logical and scannable
- [ ] Code blocks have language tags for syntax highlighting
- [ ] All links are valid
- [ ] No em dashes or en dashes
- [ ] No banned vocabulary
- [ ] Reading time is accurate
- [ ] Category and tags are set
- [ ] Article reads well on mobile (short paragraphs, no wide tables)

## Self-improvement

After the CAO reviews and publishes a blog article:

1. Move the final version from `content/blog/_drafts/` to `content/blog/_published/`
2. Diff what was drafted vs what the CAO kept - identify patterns in her edits to structure, tone, or technical depth
3. Update `content/blog/_insights.md` with what worked, what she changed, and why (add performance metrics after 7 days)
4. If her edits reveal a new rule (e.g. "always include a code example in how-to posts", "cut the intro paragraph"), add it to the Writing rules or Article templates sections
5. If the article performs well (high traffic, shares, or engagement), promote it to `content/blog/_examples/` with annotated performance frontmatter
