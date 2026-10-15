---
name: seo-links
description: "Backlink acquisition engine. Mines competitor backlinks, finds unlinked brand mentions, discovers broken link opportunities, audits internal linking, and prospects resource pages. Turns link building from guesswork into a repeatable system."
metadata:
  openclaw:
    version: "1.0"
    author: "Matt Berman"
    emoji: "🔗"
    homepage: https://bigplayers.co
    user-invocable: true
    category: "seo"
    requires:
      env: []
      tools: ["curl", "jq"]
    optional_env:
      - DATAFORSEO_LOGIN
      - DATAFORSEO_PASSWORD
---

# SEO Links — Backlink Acquisition Engine

Content without backlinks is a prayer. This skill turns link building from a manual grind into a repeatable, agent-driven system.

Five scripts. Each one finds a different type of link opportunity. Run them weekly and you'll never run out of outreach targets.

---

## Scripts

### 1. `link-mine.sh` — Competitor Backlink Mining

Pulls every site linking to your competitors. Finds the ones most likely to link to you.

**Usage:**
```bash
bash skills/seo-links/scripts/link-mine.sh <competitor-domain> [--limit 50]
```

**What it does:**
- Pulls competitor's backlink profile via DataForSEO Backlinks API
- Filters for dofollow links with Domain Rating > 20
- Categorizes by type: resource pages, roundups, directories, editorial, guest posts
- Cross-references against your existing backlinks (if you provide your domain)
- Outputs prioritized list with: URL, anchor text, DR, page type, contact suggestion

**Without DataForSEO:** Falls back to web search queries like `"competitor.com" + "resources"` and `"competitor.com" + "best tools"`. Less data but still finds resource pages and roundups.

### 2. `link-mentions.sh` — Unlinked Brand Mentions

Finds pages that mention your brand/product but don't link to you. Easiest links to get — they already know you exist.

**Usage:**
```bash
bash skills/seo-links/scripts/link-mentions.sh <brand-name> <your-domain>
```

**What it does:**
- Searches web for brand name mentions excluding your own domain
- Filters out pages that already link to you
- Checks each result for actual brand mention vs false positive
- Outputs list with: URL, mention context, contact suggestion, draft outreach snippet

**Outreach template:**
"Hey, noticed you mentioned [brand] in [article]. Thanks for the shoutout! Would you mind adding a link so your readers can find us? Here's the URL: [link]"

This converts at 15-25% because there's zero friction. They already wrote about you.

### 3. `link-broken.sh` — Broken Link Building

Finds dead links on sites in your niche, then suggests your content as the replacement.

**Usage:**
```bash
bash skills/seo-links/scripts/link-broken.sh <niche-keyword> [--limit 30]
```

**What it does:**
- Finds resource pages and roundups for your niche keyword
- Crawls each page checking for 404/dead outbound links
- Matches dead links to content you already have (or suggests content to create)
- Outputs: page URL, dead link URL, your replacement URL, contact suggestion, draft pitch

**Why this works:** You're doing them a favor by reporting broken links. The ask ("replace it with my link") is natural, not pushy.

### 4. `link-internal.sh` — Internal Link Audit

Audits your own site's internal linking structure. Finds orphan pages, suggests cross-links, builds hub-and-spoke connections.

**Usage:**
```bash
bash skills/seo-links/scripts/link-internal.sh <your-domain> [--sitemap URL]
```

**What it does:**
- Crawls your sitemap (or top pages from GSC)
- Maps internal link structure: which pages link to which
- Identifies orphan pages (no internal links pointing to them)
- Suggests new internal links based on keyword overlap between pages
- Flags pages with thin internal linking (< 3 inbound internal links)
- Outputs actionable list: "Add link from [Page A] to [Page B] with anchor text [keyword]"

**Run this every time you publish a new article.** The agent should automatically check if any existing content should link to the new piece, and if the new piece should link to existing content.

### 5. `link-prospect.sh` — Resource Page Prospecting

Finds pages that curate links in your niche — "best tools," "top resources," "ultimate guides" — and haven't listed you yet.

**Usage:**
```bash
bash skills/seo-links/scripts/link-prospect.sh <niche-keyword> [--limit 20]
```

**What it does:**
- Searches for resource pages using queries like: "[keyword] + resources", "[keyword] + best tools", "[keyword] + ultimate guide"
- Filters for pages that actually curate external links (vs single-product pages)
- Checks if you're already listed
- Scores by Domain Rating and relevance
- Outputs: URL, page type, DR, whether you're listed, draft pitch

---

## Weekly Link Building Workflow

```
Monday:    link-internal.sh  → Fix orphan pages, add cross-links
Tuesday:   link-mine.sh      → Pull competitor backlinks, find targets
Wednesday: link-mentions.sh  → Find unlinked mentions, send quick emails
Thursday:  link-broken.sh    → Find broken links, pitch replacements
Friday:    link-prospect.sh  → Find resource pages, submit listings
```

The agent handles discovery. You (or your team) handle outreach. 30 minutes a day gets you 10-20 new backlink opportunities per week.

---

## How This Connects to the Loop

The SEO Agent discovers keywords and monitors rankings. The SEO Forge writes content. SEO Links gets that content linked to.

Without links, your content sits on page 3 waiting for a miracle. With links, the content the agent wrote last month gets the authority boost it needs to break into page 1.

The loop becomes: Discover → Write → Link → Monitor → Repeat.
