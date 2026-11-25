---
name: technical-seo-geo-audit
description: Run a developer-focused technical SEO and GEO (Generative Engine Optimization) audit on a live website or a codebase, and produce one per-page README report — covering crawlability, indexability, rendering/SSR, Core Web Vitals, structured data, metadata, semantic HTML, redirects/HTTP, AI-crawler access and llms.txt — with every finding rated by severity and carrying a concrete code-level fix. Use when asked to audit SEO, check technical SEO, run an SEO health check, audit AI/LLM visibility, GEO, generative engine optimization, answer engine optimization, Core Web Vitals, render-blocking, indexability, crawlability, structured data, or "why isn't this page ranking / showing up in AI answers." Technical only — do not use for content, keyword, or editorial advice.
license: MIT
compatibility: Node 18+ (native fetch). Rendered-DOM and Core Web Vitals checks prefer the chrome-devtools MCP server and fall back to optional Playwright + PageSpeed Insights; raw-HTML, robots/sitemap, metadata, structured-data, and semantic checks run with no dependencies. Designed for Codex and Claude Code using the Agent Skills open standard.
metadata:
  author: Ezzat Malak
  version: "1.0.0"
---

# Technical SEO & GEO Audit

Audit a website's **technical** SEO and **GEO** (Generative Engine Optimization) and write
all results to exactly one README-style Markdown report, with findings **grouped per page**.
Scope is strictly technical and developer-actionable:

- **SEO** — crawlability, indexability, rendering/SSR, Core Web Vitals, structured data,
  metadata, semantic HTML, HTTP/redirects, internal linking.
- **GEO** — how well AI assistants (ChatGPT, Claude, Perplexity, Gemini) can crawl, parse,
  and cite the site: AI-crawler access, `llms.txt`, SSR delivery to non-JS bots, machine-
  readable structured data, clean attribution.

**No content, keyword, or editorial recommendations.** If a check would drift into
copywriting, drop it.

This is a **hybrid** skill: deterministic checks run in `scripts/` (a Node engine) and emit
structured findings plus a baseline report; you orchestrate the rendered-DOM capture,
interpret results, and finalize the report. The single most important defect to catch is
**raw-vs-rendered divergence** — content that only exists after JS hydration is invisible to
non-JS search and AI crawlers.

## Non-negotiable output

- Produce **one** report. Default path `SEO-GEO-AUDIT.md` at the working-directory root,
  unless the user gives another.
- **Group findings per page, labeled by route** (`### \`/pricing\` — Pricing`). This is a hard
  requirement.
- Every finding carries a severity, a technical description (what + why), the evidence found,
  and a **copy-pasteable code-level fix**.
- Mark anything a check could not verify as `Info` / "not measured" — **never assert a
  pass/fail the checks did not actually confirm.**
- No content/keyword/editorial advice. Never reproduce secrets found in headers or markup.

Use [assets/SEO_GEO_AUDIT_REPORT_TEMPLATE.md](assets/SEO_GEO_AUDIT_REPORT_TEMPLATE.md) as the
required structure and [references/severity-rubric.md](references/severity-rubric.md) for
severities and scoring.

## Phase 0: Resolve inputs and mode

Determine these first, then echo them into the report's run-metadata table.

1. **Mode** (auto-detect): **Live URL** if a base URL is given (`--url`), **Codebase (static)**
   if a repo path is given (`--path`). URL mode is primary and the only mode that can measure
   rendering, headers, and Core Web Vitals. Both may be combined.
2. **Pages.** Pin specific routes with `--routes /a,/b,/c`, otherwise discover via
   `sitemap.xml` + robots `Sitemap:` directives, falling back to a same-origin link crawl.
   Cap with `--max-pages` (default 25).
3. **Report path.** `--out` (default `SEO-GEO-AUDIT.md`).
4. **Depth.** Default **Standard**. **Quick** = homepage + a few key routes, raw + metadata +
   crawlability only. **Deep** = full page set, rendered-DOM diff on every page, CWV on all,
   plus a self-audit pass.
5. **Optional CWV source.** `--psi-key <key>` for PageSpeed Insights (degrade gracefully if
   absent — chrome-devtools MCP Lighthouse is preferred).

## Phase 1: Discover pages and capture raw HTML

Resolve `<skill-directory>` from the loaded skill path.

- **URL mode:** run the crawler to discover pages and capture the **raw** HTML (what a non-JS
  bot / AI crawler sees) plus status, redirect chain, and headers:
  ```bash
  node <skill-directory>/scripts/crawl.mjs --url <base> [--routes /a,/b] [--max-pages 25] --out <work-dir>
  ```
  This writes `<work-dir>/crawl.json` and `<work-dir>/raw/<slug>.html`. (`run.mjs` in Phase 3
  re-runs discovery itself, so you may skip this and go straight to Phase 2 + 3.)
- **Codebase mode:** run `bash <skill-directory>/scripts/detect-stack.sh <repo>` to identify the
  framework, router (Next.js App vs Pages), and SEO source files for static analysis.

## Phase 2: Capture the rendered DOM (prefer MCP) — highest priority

For each discovered page, obtain the **fully rendered DOM** so the engine can diff it against
the raw HTML. Order of preference:

1. **chrome-devtools MCP** (preferred, no install): `navigate_page` to the URL, then
   `evaluate_script` returning `document.documentElement.outerHTML`. Save each result to
   `<work-dir>/rendered/<slug>.html` where `<slug>` matches the crawler's slug (the path with
   `/` → `-`, home → `home`). Capture Core Web Vitals with `lighthouse_audit` and write them to
   `<work-dir>/cwv.json` as `{ "/route": { "lcp": ms, "cls": n, "inp": ms, "ttfb": ms, "source": "lighthouse" } }`.
2. **Playwright fallback** (if MCP is unavailable and Playwright is installed): pass
   `--playwright` to `run.mjs` and it renders each page itself.
3. **Neither available:** skip rendered checks. The engine still runs every raw-HTML check and
   marks rendering/CWV as **not measured** (`Info`). Warn the user that SSR parity was not
   confirmed.

## Phase 3: Run the check engine

```bash
node <skill-directory>/scripts/run.mjs \
  --url <base> [--routes …] [--max-pages 25] \
  --rendered-dir <work-dir>/rendered \
  [--cwv-file <work-dir>/cwv.json] [--psi-key <key>] [--playwright] \
  --out SEO-GEO-AUDIT.md --work <work-dir>
```
Codebase mode: `node <skill-directory>/scripts/run.mjs --path <repo> --out SEO-GEO-AUDIT.md`.

The engine runs all checks (catalogs: [references/seo-checks.md](references/seo-checks.md),
[references/geo-checks.md](references/geo-checks.md)), writes `<work-dir>/findings.json`, and
renders a baseline `SEO-GEO-AUDIT.md`. Check categories:

- **A. Crawlability & indexability** — robots, sitemap, canonical, noindex, redirects, status.
- **B. Rendering / SSR** — raw-vs-rendered diff (the top defect for SEO *and* GEO).
- **C. Performance / Core Web Vitals** — LCP/CLS/INP/TTFB, render-blocking, images, fonts.
- **D. Metadata & structured data** — title/description, OG/Twitter, viewport, JSON-LD, attrs.
- **E. Semantic HTML & linking** — one `<h1>`, heading order, landmarks, orphan pages.
- **F. GEO** — AI-crawler access, `llms.txt`, SSR-to-non-JS-bots, machine-extractable answers.

## Phase 4: Core Web Vitals

Map each metric to severity against Google's thresholds (in
[references/severity-rubric.md](references/severity-rubric.md)). Prefer chrome-devtools
`lighthouse_audit`; PSI is the fallback. When no CWV source is available, the metric is
reported as `Info` ("not measured") — do not guess values.

## Phase 5: Interpret and verify (guidance layer)

Read `<work-dir>/findings.json` and refine, do not rubber-stamp:

1. Drop false positives (e.g. a heuristic flag the source disproves) and anything that drifts
   into content/keyword advice.
2. Confirm each kept finding's evidence is real (the selector/header/measurement exists).
3. Add findings the static engine cannot see but the rendered DOM reveals, keeping the same
   deterministic ID scheme.
4. For codebase mode, label findings as **static** and note that URL mode is needed for
   rendering/CWV/live HTTP.

## Phase 6: Score

The engine computes two deterministic 0–100 scores (SEO and GEO) per the rubric. Confirm they
follow the evidence, then write the 5–8 line executive verdict, keyed off the lower score and
any critical/high counts.

## Phase 7: Write and validate the report

1. Finalize `SEO-GEO-AUDIT.md` from
   [assets/SEO_GEO_AUDIT_REPORT_TEMPLATE.md](assets/SEO_GEO_AUDIT_REPORT_TEMPLATE.md):
   run-metadata → executive summary (both scores) → site-wide findings → **per-page sections
   labeled by route** → quick-win checklist → appendix/methodology.
2. Validate the structure:
   ```bash
   python3 <skill-directory>/scripts/validate-report.py SEO-GEO-AUDIT.md
   ```
   Fix any structural errors before finishing.
3. Self-audit (always in Deep, briefly in Standard): every finding has a concrete location,
   real evidence, and a code-level fix; nothing asserts an unverified pass; not-measured items
   are `Info`; no content/keyword advice slipped in; no secrets reproduced.
4. In chat, return only a concise summary: the two scores, counts by severity, the top fixes,
   and the report path. Do not paste the whole report.

## Guardrails

- The report must be trustworthy: never claim a status a check did not verify. Missing optional
  deps (Playwright, PSI, MCP) reduce coverage with a clear warning — they never fabricate a
  result and never crash the run.
- Every recommendation ships a concrete code/config snippet, not "improve X."
- Deterministic IDs (stable strings) so reports diff cleanly across runs.
- Do not modify the audited project's code unless the user explicitly asks for fixes afterward.
