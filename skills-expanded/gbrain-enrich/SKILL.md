---
name: gbrain-enrich
description: Enrich person and company pages from external sources (Crustdata, Happenstance, Exa). Validation rules enforced.
metadata:
  openclaw:
    emoji: "✨"
    requires:
      bins: [gbrain]
---

# Enrich Skill

## Sources

| Source | Best for | Auth |
|--------|----------|------|
| Crustdata | LinkedIn profile data (90+ fields) | `Token` header (NOT Bearer) |
| Happenstance | Career history, network search | credits |
| Exa | Web search, articles, mentions | API key |

## Person enrichment workflow

1. **Find LinkedIn URL** — check existing page frontmatter, or search:
   `gbrain get people/<slug>` → look for `linkedin:` in frontmatter

2. **Hit Crustdata**
   ```
   GET https://api.crustdata.com/screener/person/enrich?linkedin_profile_url=<url>
   Authorization: Token <key>
   ```
   Returns: name, title, location, headline, skills, work history, education, twitter, email

3. **Validate before writing:**
   - Connection count < 20 → likely wrong person. Store raw with flag, skip page update.
   - Name mismatch (different last name) → skip.
   - Obviously test/joke profiles → skip.

4. **Store raw data:**
   ```bash
   gbrain call brain_raw '{"slug":"people/name","source":"crustdata","data":{...}}'
   ```

5. **Distill to page** — Update compiled_truth with:
   - Location, current title, company
   - Education (one line, most recent degree)
   - Career arc (condensed: "Google → Stripe → founded Acme")
   - Top 3-5 skills
   - Twitter handle, LinkedIn URL

6. **DO NOT dump full data into the page.** 50 skills, 10 full job descriptions → raw_data only.

## Company enrichment workflow

1. Search by company name or domain via Exa or Crustdata company search
2. Store raw response
3. Distill: founding year, stage, investors, headcount, what they build
4. Update page State section

## Batch rules

- Checkpoint every 20 items
- Exponential backoff on 429s: 10s → 20s → 40s → ... → 5min cap
- Never re-enrich already-enriched pages: check `gbrain call brain_raw '{"slug":"...", "source":"crustdata"}'` first
- Dry-run: show what would be enriched without making API calls
