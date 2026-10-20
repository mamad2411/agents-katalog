---
name: search-papers
description: Search academic papers, technical reports, and research publications for data, statistics, and authoritative citations to support ArtStroy articles. Supports GEO optimization (Statistics +37%, Cite Sources +40%).
---

# Search Papers

ArtStroy articles rank better and get cited by AI search engines when they include real statistics and authoritative citations. This skill finds those sources.

## Why This Matters

From the GEO optimization research (Princeton study):
- **Cite Sources**: +40% AI search engine visibility
- **Statistics**: +37% AI search engine visibility

An article with "43% of security incidents involve exposed API keys" (with a citation) performs significantly better than one that vaguely says "many security incidents involve credentials."

## Where to Search

**Primary sources:**
- Use `EXA_API_KEY` for semantic search across academic and research content
- Google Scholar (no API — use Exa to surface Scholar URLs)
- NIST (security): `https://csrc.nist.gov/publications`
- ACM Digital Library
- arXiv (for CS/programming research)

**Authoritative reports (bookmarkable):**
- OWASP Top 10 reports (annual)
- Verizon DBIR (Data Breach Investigations Report)
- Stack Overflow Developer Survey
- GitHub Octoverse
- Playwright release notes and adoption stats

**For search:**
```
Search queries:
- "{topic} statistics 2024 OR 2025 site:nist.gov OR site:owasp.org OR site:stackoverflow.com"
- "{topic} research paper findings percentage"
- "{tool name} adoption rate survey"
```

## What to Extract

For each relevant paper or report:
1. **Citation**: Author(s), title, publication, year, URL
2. **Key statistic**: the number + context
3. **Direct quote** (if attributable): the exact sentence for block-quoting
4. **Confidence level**: peer-reviewed journal > industry report > blog post

## Output Format

For passing to the Writer:

```markdown
### Source: {Title}
- **Citation**: {Author(s)}. "{Title}." {Publication}, {Year}. {URL}
- **Key finding**: "{exact statistic or finding}"
- **Usage**: Include in {section name} as supporting evidence for {claim}
- **Confidence**: Peer-reviewed / Industry report / Survey / Blog
```

Provide 2–5 sources per article. More citations don't necessarily help — depth on 3 strong sources beats breadth on 10 weak ones.

## Citation Format in MDX

Writers should use inline citation links:

```markdown
According to the [Verizon DBIR 2024](https://verizon.com/dbir), 
74% of breaches involve the human element.
```

Or footnote-style for academic citations:

```markdown
Research shows that CSP headers reduce XSS success rate by 
approximately 60% when properly configured [^1].

[^1]: Smith et al. "Content Security Policy Effectiveness." 
IEEE S&P 2024. https://example.org/paper
```
