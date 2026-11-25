---
name: geo-content-health
description: Editorial health audit. Detects "Mount AI" anti-patterns (self-promotional listicles, mass-generated content, synthetic FAQ, mass refresh, negative-GEO injections) and measures sustainable patterns (BLUF format, definition language, atomic paragraphs, multi-channel coherence, first-hand expertise). Reports a risk score AND a maturity score.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
  - Write
---

# Content Health — audit module

## Purpose

Audit the editorial layer of a site: what kind of content does it publish, how is it structured, and is it currently exposed to ranking-penalty risk that would cascade into LLM-citation loss?

The methodology and confidence levels live in [`docs/CONTENT_HEALTH_PATTERNS.md`](../../docs/CONTENT_HEALTH_PATTERNS.md). The Python implementation is in [`scripts/checks/content_health.py`](../../scripts/checks/content_health.py).

## Implementation

Single-page audit:
```bash
python3 -m scripts.checks.content_health "<URL>" --lang fr
# Returns JSON with anti-pattern detection (CHA*) + sustainable-pattern measurements (CHM*).
```

Multi-page (recommended): sample pages via `scripts/site_crawler.py` then run the check on each. Aggregate the metrics (BLUF compliance, definition density, etc.) across pages — single-page numbers are unrepresentative.

## Output language

By default, the report is written in the **audited site's language**, detected via `scripts/site_locale.py` (HTML `lang` → `Content-Language` header → TLD → fallback `en`). User can override with `--output-lang <iso2>`. See `CLAUDE.md` rule "Output language".

---

## Two parallel scores

The audit reports two **non-redundant** scores:

1. **Risk score (0-100, lower is better)** — based on anti-patterns detected ("Mount AI" triggers documented by Lily Ray on 30+ sites with -22% to -34% organic visibility drops since Jan 2026)
2. **Maturity score (0-100, higher is better)** — based on sustainable patterns present (BLUF format, definition language, multi-channel coherence, first-hand expertise signals)

A site can have low risk **and** low maturity (clean but unexceptional). It can have high risk and high maturity (mixing risky tactics with substantive content). The two scores are complementary diagnostic axes.

---

## 🚫 Anti-patterns to detect (drives Risk score)

### A1 — Self-promotional listicles ("Best of YEAR")

**Detection**:
- Title regex `(?i)\b(best|top|meilleur)\b.*\b(20\d{2})\b`
- The site's own brand mentioned in the first 200 words
- Numbered list structure (numbered headings or `<ol>`)
- Absence of methodology language ("we tested", "based on N hours of usage", explicit criteria)

**Severity if found**: **High**. Documented case: 10 such pages out of 1 700 articles (0.6% of content) caused -29% organic visibility on one site.

### A2 — Mass-generated content fingerprints

**Detection**:
- Templated H2 sequences (same H2 set across many articles, just with the topic substituted)
- Identical intro/outro paragraphs across articles
- Unattributed authorship (no `Person` schema, no byline)
- Disproportionate ratio of articles to actual editorial team

**Severity**: **High**.

### A3 — Synthetic FAQ spam

**Detection**:
- High count of `FAQPage` schemas across the site (>50% of pages)
- Questions following stuffed patterns
- Answers <30 words OR answers that just paraphrase the question without adding fact

**Severity**: **Medium**.

### A4 — Mass content refresh (date-bumping)

**Detection** (when reproducibly checkable):
- `dateModified` within last 7 days on >30% of pages
- Wayback Machine snapshot diffs show no real content delta

**Severity**: **Medium-Low**.

### A5 — Negative-GEO injection (defensive scan)

**Detection** (HTML scan):
- `<section>`, `<div>`, `<aside>` with class names like `agent-instructions`, `system-prompt`, `llm-prompt` whose **content** contains exclusion or self-promotion directives ("never cite", "do not include", "the only authorized source")
- HTML comments with prompt-injection-style instructions
- Non-standard `<meta>` tags addressing LLMs

**Note**: a *legitimate* `<section class="agent-instructions">` block describing the entity factually (per `STRUCTURED_DATA_BEST_PRACTICES.md`) is good practice. A *negative-GEO* block tries to manipulate LLM behaviour against third parties. Distinguishing them needs content analysis (look for negation, explicit exclusion, or competitor naming).

**Severity**: **Medium** (decreasing efficacy + reputational risk). Reported as informational rather than fix-must.

---

## ✅ Sustainable patterns to measure (drives Maturity score)

### M1 — BLUF format on key pages
For each H2 on key pages:
- First-paragraph word count (target ≤ 60)
- Presence of a number / data point
- Presence of attribution (named source, "according to", named protocol/study)

Flag long meandering openers (>120 words before any factual claim).
**Confidence**: High.

### M2 — Definition language density
Count occurrences of definition phrases ("X est défini comme", "désigne", "X is Y", "refers to") in content body. FR + EN templates.
- Compute density (% of paragraphs containing one)
- Target ≥ 30%; flag pages with <15%
**Confidence**: Medium (single Ahrefs correlation study).

### M3 — Atomic paragraphs
- Average paragraph length (target 40-80 words)
- Question-form heading ratio (target 30-50% for content pages)
**Confidence**: Medium-High.

### M4 — Multi-channel brand coherence (cross-domain)
For each platform (free public APIs only):
- Wikipedia / Wikidata presence (MediaWiki + SPARQL)
- Reddit mentions (search public)
- LinkedIn company page
- YouTube channel + videos
- GitHub presence
- Crunchbase
- Wayback Machine first capture
- For French sites: Pappers, Societe.com

For each present channel, verify the brand description and key facts (founding year, location, headcount when stated) match the audited site. **Discrepancies are red flags** — they break attribution.
**Confidence**: High (Ahrefs n=75 000).

### M5 — First-hand expertise signals
- Author bylines on articles linking to a `Person` schema
- `Person.alumniOf`, `knowsAbout` populated for key authors
- Original quantified claims with methodology disclosed (sample size, dates, methodology)
- Industry citations or peer-reviewable references
**Confidence**: High.

### M6 — Freshness with substance
For pages with `dateModified` recent (<30 days), spot-check 1-2 against Wayback Machine to verify substantive change rather than date-bumping.
**Confidence**: Medium.

---

## Per-vertical adjustments

| Vertical | Where the levers concentrate |
|---|---|
| E-commerce | Product page coherence, AggregateRating exposure, multi-channel brand presence |
| Editorial / blog | BLUF format, definition language, author E-E-A-T, original data |
| B2B SaaS | Comparison tables (NOT self-promotional listicles), case studies with named clients & quantified outcomes |
| Local service | NAP consistency, LocalBusiness schema, Google Business Profile freshness |
| Agency / consultancy | Case studies, published frameworks, named experts, press mentions |

---

## Output

Resolved via `scripts/client_paths.py paths <URL>`:
- Markdown report: `$CLIENT_DIR/audits/<YYYY-MM-DD>-content-health.md`

If user passes `--cwd`, writes `GEO-CONTENT-HEALTH.md` in current directory.

Report structure:

```markdown
# Content Health — <domain>
**Audit date:** YYYY-MM-DD
**Vertical detected:** [...]

## Risk score: XX/100 (lower is better)
- A1 Self-promotional listicles: [N detected]
- A2 Mass-generated content fingerprints: [present / absent]
- A3 Synthetic FAQ spam: [yes / no]
- A4 Mass content refresh: [detected / not detected / not checked]
- A5 Negative-GEO injection: [detected / not detected]

## Maturity score: XX/100 (higher is better)
- M1 BLUF format: X% of H2 sections in target range
- M2 Definition language: X% paragraph density
- M3 Atomic paragraphs: avg X words, Q-form heading ratio Y%
- M4 Multi-channel coherence: X/8 channels present, N discrepancies
- M5 First-hand expertise: [strong / partial / weak]
- M6 Freshness with substance: [strong / not checked]

## Findings
[severity-grouped: Critical / High / Medium / Low / Informational, each with confidence + effort + score-gain estimate]

## Per-vertical commentary
[brief narrative on which levers to prioritise given the detected vertical]
```

This skill is one of the building blocks of `/geo audit`; when run in isolation it produces the report above.

---

## What this skill does NOT do

- **Never blacklist competitor sites or domains.** The audit reports patterns on the audited site only.
- **Never recommend negative-GEO tactics.** Detection is in scope (defensive), injection is not.
- **Never claim a "Mount AI guarantee".** The penalty triggers are documented but each Google update is unpredictable in detail. We frame as risk, not certainty.
- **Never project traffic / revenue impact.** Per audit-only philosophy.
