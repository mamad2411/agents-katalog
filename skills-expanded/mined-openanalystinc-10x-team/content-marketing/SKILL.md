---
name: content-marketing
description: Activate for content strategy, editorial calendars, content pillar mapping, blog planning, and content audit. Use when planning content programs, creating editorial workflows, or building topic clusters.
license: MIT
---

# Content Marketing

Strategic content planning, editorial workflows, and content optimization frameworks.

## When to Use

- Content strategy development
- Editorial calendar creation
- Blog post planning
- Content pillar/cluster mapping
- Content audit needed
- Repurposing workflows

## Core Capabilities

### Content Strategy
Load: `references/content-strategy-framework.md`

### Editorial Calendar
Load: `references/editorial-calendar-template.md`

### Blog Post Templates
Load: `references/blog-post-templates.md`

### Content Audit
Load: `references/content-audit-checklist.md`

## Quick Reference

**Content Pillars:** 3-5 core themes aligned with business goals

**Content Types:** Blog, video, podcast, social, email

**Audit Actions:** Keep, Update, Consolidate, Redirect, Delete

## Workflow

### Content Strategy Workflow
1. Audit existing content
2. Define audience personas
3. Identify content pillars (3-5)
4. Map topic clusters per pillar
5. Create editorial calendar
6. Define production workflow
7. Set measurement framework

### Blog Planning Workflow
1. Keyword research (use seo-optimization skill)
2. Select template based on intent
3. Create content brief
4. Outline → Draft → Edit → Publish

### Content Repurposing
- Blog → Social posts, email sequence, video script
- Podcast → Blog post
- Webinar → Multiple blogs

## MCP Server Guidelines

**Content marketing uses MCPs for research and inspiration.**

### When to Use Exa MCP (`exa-mcp-server`)

Use for **quick content research**:

| Task | Example |
|------|---------|
| Topic research | "What are trending topics in AI?" |
| Competitor content | "Find competitor blog posts on SaaS pricing" |
| Content inspiration | "Popular articles on product marketing" |
| Quick reference | "Best practices for B2B content" |

**Characteristics:**
- Fast response for inspiration
- Good for topic ideation
- Quick competitive research

### When to Use Websets MCP (`websets-mcp-server`)

Use for **comprehensive content analysis**:

| Task | Example |
|------|---------|
| Full content audit | "All competitor content in fintech space" |
| Topic cluster research | "Comprehensive topic map for AI marketing" |
| Influencer research | "Find all content creators in SaaS marketing" |
| Deep market analysis | "Content strategies of top 50 B2B SaaS companies" |

**Characteristics:**
- Exhaustive research
- Comprehensive competitor analysis
- Deep topic exploration

### MCP Selection Matrix

| Content Task | MCP | Reason |
|--------------|-----|--------|
| Blog topic ideas | Exa | Quick inspiration |
| Content pillar research | Websets | Comprehensive mapping |
| Competitor post analysis | Exa (quick) | Fast research |
| Full content audit | Websets | Exhaustive analysis |
| Trending topics | Exa | Real-time search |
| Influencer discovery | Websets | Comprehensive list |

### Auto-Selection Logic

```python
def select_mcp_for_content(task: str, scope: str) -> str:
    if scope in ['comprehensive', 'full', 'all', 'exhaustive']:
        return 'websets'
    if 'audit' in task and 'quick' not in task:
        return 'websets'
    return 'exa'  # Default for most content tasks
```

## Report Output

**Activate:** `assets-organizing` skill for report file paths

Content reports go to `assets/reports/content/{date}-{content-type}-audit.md`

## Agent Integration

**Primary Agents:** content-creator, campaign-manager, attraction-specialist

**Skill Dependencies:** seo-optimization, brand-guidelines, creativity, assets-organizing (report organization)

## Best Practices

1. Lead with value, not promotion
2. Match content to buyer journey stage
3. Maintain consistent publishing schedule
4. Update evergreen content quarterly
5. Repurpose before creating new
6. Measure content ROI, not just traffic
