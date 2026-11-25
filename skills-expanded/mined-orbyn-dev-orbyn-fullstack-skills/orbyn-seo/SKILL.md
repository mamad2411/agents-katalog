---
name: orbyn-seo
description: "Make a site findable in search and AI answers: audit crawl and index blockers, internal links, URL migrations with checked redirects, answer-ready page structure, honest comparison pages and crawler policy. Use orbyn-ui-design for head tags, orbyn-content-design for copy."
---

# Search and answer-engine visibility

Use this when building, launching, moving or auditing a website that people should
find through search engines or AI answers. Page head tags (title, description,
canonical, social cards, JSON-LD) belong to
[page metadata](../orbyn-ui-design/references/page-metadata.md); interface copy to
[orbyn-content-design](../orbyn-content-design/SKILL.md); posts to
[social-content](../social-content/SKILL.md); market or competitor research to
[orbyn-research](../orbyn-research/SKILL.md).

## Authority

Work in the repository and on a local or preview build. Read the live site only
with plain requests to the person's own domains. Never publish, submit to
directories, send outreach, buy links or tools, sign up for a provider, or change
DNS, hosting or search-console settings without the person's own request. Use a
keyword or SERP provider (Search Console, Ahrefs, DataForSEO) only when the person
already has it connected, and label every number with its source and date. Without
data, work from the site's own evidence and say so.

No tricks that search engines treat as spam: no cloaking (crawlers and people see
the same page), doorway or thin generated pages, keyword stuffing, hidden text,
link schemes, invented reviews, ratings, counts or competitor claims.

## Method

1. **Name the pages that matter.** Ask or infer the money pages (signup, pricing,
   product, the pages that convert) and the question each page answers.
2. **Fix what blocks crawling first.** Run the [site audit](references/site-audit.md)
   in its order: robots and sitemap, soft 404s, leaked `noindex`, locale sprawl,
   content crawlers cannot read, programmatic traps, money-page indexation. A
   fatal blocker outranks every polish item.
3. **Check head tags** with [page metadata](../orbyn-ui-design/references/page-metadata.md),
   including its title rules.
4. **Measure internal links** on the built site:
   `python3 scripts/link_graph.py --site dist --money /pricing` (see
   [internal linking](references/internal-linking.md)). Fix orphans, broken links
   and deep money pages before adding content.
5. **Structure pages for answers.** Lead with the answer, phrase headings as the
   questions people ask, keep facts as text and every number from one source
   ([answer engines](references/answer-engines.md)).
6. **Comparison and alternative pages** only from verified, dated, sourced facts,
   including where the other product wins ([comparison pages](references/comparison-pages.md)).
7. **Moving URLs or domains:** a 1-to-1 redirect map, one permanent hop each,
   checked with `python3 scripts/verify_redirects.py --map redirects.csv`, then live
   against the person's own domain ([URL migration](references/url-migration.md)).
8. **Crawler policy:** decide which crawlers may read the site and say it honestly
   ([crawler policy](references/crawler-policy.md)).
9. **Verify and report.** Build, run the checks again, and report each issue as
   fixed, open or not checked, with the command or page that shows it. Search
   rankings and AI citations take weeks and are never claimed from a local change.

### Worked failure

A rebrand redirects every old URL to the new home page and ships with the staging
`noindex` still on. Search engines treat the mass redirects as soft 404s, the inner
pages' links are lost, and the new domain drops out of the index. The fix is a
1-to-1 map to each page's closest equivalent, one 301 hop, the production robots
setting checked before launch, and the redirect check passing on the live domain.

## Read when needed

- Launch, audit or "why is this page not found": [site audit](references/site-audit.md).
- Orphan pages, money pages too deep, anchor text: [internal linking](references/internal-linking.md).
- Domain change, subdomain to subfolder, slug clean-up, merging sites: [URL migration](references/url-migration.md).
- Being quoted by AI answers, featured snippets, `llms.txt`: [answer engines](references/answer-engines.md).
- "Us vs them", alternatives or best-for lists: [comparison pages](references/comparison-pages.md).
- AI training crawlers, bot rules, scraping: [crawler policy](references/crawler-policy.md).
- A redirect check or link check in CI: [orbyn-ci-design](../orbyn-ci-design/SKILL.md).
