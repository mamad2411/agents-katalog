---
name: claude-seo
description: Audit, plan, and improve technical SEO, on-page content, structured data, sitemaps, hreflang, local/ecommerce visibility, and AI-search citability using evidence-first workflows and a safe Rust static-analysis CLI. Use for SEO audits, page reviews, traffic or ranking investigations, content plans, schema, crawlability, indexation, migration drift, competitor research, and GEO. Never invent search, analytics, backlink, or performance data.
tags: [general]
---

# Claude SEO

Build SEO decisions from observed evidence. Keep three states distinct:

- **observed**: source, URL/property, market, capture time, and value exist;
- **inferred**: mechanism is plausible but not directly measured;
- **setup required**: credential, export, crawler, browser, or paid dataset is absent.

Do not convert missing evidence into a score, benchmark, ranking, volume, traffic,
backlink, Core Web Vital, or indexation claim.

## Establish scope

Record:

- site/property, environment, markets, languages, page types, and business goal;
- audit mode: full site, single page, technical, content, migration, local,
  ecommerce, programmatic, or AI-search/GEO;
- available first-party evidence: Search Console, analytics, logs, crawl exports,
  CMS data, release history, and conversions;
- available external evidence: live SERPs, backlinks, maps, competitors, CrUX,
  and PageSpeed;
- constraints: robots policy, authentication, crawl budget, PII, and production
  safety.

Read [references/audit-playbooks.md](references/audit-playbooks.md) for mode-specific
coverage. Read [references/migration-ledger.md](references/migration-ledger.md)
when parity with upstream `claude-seo` matters.

## Collect evidence

1. Start with source files, generated HTML, sitemaps, robots directives, and
   first-party exports already available.
2. Fetch current public facts only when needed. Prefer official Google,
   Schema.org, platform, and vendor documentation for rules.
3. Use browser automation for rendered DOM, JavaScript, screenshots,
   interactions, or consent-dependent behavior. Static HTML is not rendered DOM.
4. Use credentialed APIs only when configured. Record property, date range,
   filters, timezone, sampling, and row limits.
5. For competitors or SERPs, record query, locale, device, and collection time.
   A search result snapshot is not durable rank truth.

## Run Rust audit

Runtime lives at `scripts/Cargo.toml`. Resolve its path relative to installed
`SKILL.md`; use an absolute manifest path. Rust/Cargo is required. First build
uses locked crates from local Cargo cache or crates.io.

Audit one public URL:

```bash
cargo run --quiet --locked --manifest-path <claude-seo-manifest> -- \
  audit --input https://example.com/page --format markdown
```

Audit local HTML with explicit resolution base:

```bash
cargo run --quiet --locked --manifest-path <claude-seo-manifest> -- \
  audit --input page.html --base-url https://example.com/page --format json
```

Exit `0` means no high/critical static finding. Exit `2` means findings need
review, not command failure. Runtime rejects private/local network targets,
revalidates redirects, pins validated DNS resolution, and caps time and bytes.

Inspect sitemap:

```bash
cargo run --quiet --locked --manifest-path <claude-seo-manifest> -- \
  sitemap --input https://example.com/sitemap.xml
```

Compare two saved audit reports:

```bash
cargo run --quiet --locked --manifest-path <claude-seo-manifest> -- \
  drift --before baseline.json --after current.json
```

Check honest capability boundary:

```bash
cargo run --quiet --locked --manifest-path <claude-seo-manifest> -- doctor
```

Runtime covers bounded static evidence. It does not render JavaScript, crawl a
site recursively, query search engines, inspect backlinks, or authenticate to
Google/Bing/DataForSEO/Moz/maps. Label those `setup required` until observed.

## Analyze

Group evidence by mechanism, not tool:

1. discovery and crawl access;
2. canonicalization and index eligibility;
3. rendering, response behavior, and performance;
4. page intent, content usefulness, internal links, and media;
5. structured data and entity consistency;
6. language/region targeting;
7. authority, mentions, reviews, and local signals;
8. search experience and conversion path;
9. AI-search citability: direct answers, extractable passages, provenance, and
   stable entity facts.

Correlate signals before claiming cause. A traffic drop needs deployment,
indexation, query/page, seasonality, tracking, and SERP evidence—not one chart.

## Prioritize

For every recommendation include:

- stable finding ID and severity;
- observed evidence and affected scope;
- mechanism and confidence;
- smallest safe fix;
- owner/dependency;
- verification command or measurement;
- rollback or monitoring plan where risk exists.

Prioritize blockers and broad templates before cosmetic metadata. Avoid totals
that mix executed checks with unavailable evidence. State coverage beside any
score.

## Output

Return:

1. executive summary with scope and coverage;
2. evidence ledger: observed, inferred, setup required;
3. prioritized findings with evidence, fix, and verification;
4. page/template examples where useful;
5. 30/60/90-day plan or smallest rollout sequence;
6. measurement plan and drift monitors;
7. limitations and unresolved questions.

This skill is adapted under MIT; see [NOTICE.md](NOTICE.md) and
[LICENSE.txt](LICENSE.txt).
