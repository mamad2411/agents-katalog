---
name: cross-post-syndication
description: Cross-post published ArtStroy articles to dev.to and Hashnode with correct canonical URLs, metadata mapping, and formatting. Handles API integration for automated posting and creates manual-assist drafts for platforms without API access.
---

# Cross-Post Syndication

Syndication multiplies article reach without duplicating SEO signals — as long as the canonical URL points back to artstroy.net on every platform.

**The canonical URL is non-negotiable.** A syndicated article without `canonical_url: https://artstroy.net/{slug}` is an SEO liability.

## Pre-Syndication Gate

Do NOT syndicate until:
- [ ] Publisher has applied the `live` label
- [ ] QA gate has passed (Lighthouse ≥90 performance, no broken links)
- [ ] `https://artstroy.net/{slug}` returns HTTP 200

## Platform 1: dev.to

Uses the dev.to REST API with `DEVTO_API_KEY`.

**Create article:**
```bash
curl -X POST https://dev.to/api/articles \
  -H "api-key: ${DEVTO_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "article": {
      "title": "{frontmatter.title}",
      "body_markdown": "{article body with frontmatter stripped}",
      "published": true,
      "canonical_url": "https://artstroy.net/{slug}",
      "tags": ["{tag1}", "{tag2}", "{tag3}"],
      "series": "{optional series name}",
      "description": "{frontmatter.description}"
    }
  }'
```

**Tag mapping** (dev.to allows up to 4 tags):
- `category: pentesting` → tags: `["security", "pentesting", "owasp", "webdev"]`
- `category: programming` → tags: `["programming", "javascript", "typescript", "webdev"]`
- `category: technology` → tags: `["technology", "testing", "automation", "qa"]`

**dev.to-specific MDX handling:**
- Remove Astro-specific imports (`import { Component } from '...'`)
- Replace `<Component client:load />` with a note: `> Interactive demo available at [artstroy.net/{slug}](https://artstroy.net/{slug})`
- Code blocks render correctly — no changes needed

## Platform 2: Hashnode

Uses the Hashnode GraphQL API with `HASHNODE_TOKEN`.

**Create article mutation:**
```graphql
mutation CreatePost($input: CreateStoryInput!) {
  createStory(input: $input) {
    post {
      id
      slug
      url
    }
  }
}
```

Variables:
```json
{
  "input": {
    "title": "{frontmatter.title}",
    "contentMarkdown": "{article body}",
    "isPartOfPublication": {"publicationId": "{artstroy hashnode publication ID}"},
    "canonicalUrl": "https://artstroy.net/{slug}",
    "metaTitle": "{frontmatter.title}",
    "metaDescription": "{frontmatter.description}",
    "tags": []
  }
}
```

Hashnode publication ID is stored in `docs/project_notes/key_facts.md`.

## Platform 3: LinkedIn (Manual Assist)

No automation — generate a draft for human posting:

```markdown
## LinkedIn Post Draft — {slug}

{frontmatter.title}

{first 2 paragraphs of article, adapted for LinkedIn's professional tone}

Full article: https://artstroy.net/{slug}?utm_source=linkedin&utm_medium=social

#QualityAssurance #Pentesting #Programming #SoftwareTesting
```

Post as a comment on the syndication issue for human to copy-paste.

## UTM Tagging

All social links must include UTM parameters:
- dev.to bio link: `https://artstroy.net/{slug}?utm_source=devto&utm_medium=social`
- Hashnode: canonical URL has no UTM (canonical should be clean)
- LinkedIn draft: `utm_source=linkedin&utm_medium=social`
- Twitter: `utm_source=twitter&utm_medium=social`

## Syndication Log

After completing each platform, record in the article tracking comment:

```markdown
## Syndication Status — /{slug}

| Platform | Status | URL | Date |
|---|---|---|---|
| dev.to | ✅ Published | https://dev.to/azanir/{slug} | {date} |
| Hashnode | ✅ Published | https://hashnode.com/post/... | {date} |
| LinkedIn | 📋 Draft ready | — | {date} |
| Twitter | 📋 Draft ready | — | {date} |
```
