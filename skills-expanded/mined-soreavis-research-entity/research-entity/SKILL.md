---
name: research-entity
description: Generate a comprehensive competitive-intelligence / due-diligence dossier on any legal entity (company, startup, or vendor). Produces a board-ready MD document with Executive Briefing (BLUF, Scorecard, SWOT, Threat Heat Map, Strategic Playbook, Monitoring Watchlist), full company profile (founders, funding, product, tech, customers, competition, risks), portrait-oriented mermaid diagrams, clickable source URLs, quote bank, glossary, and optional HTML/PDF export. Every datapoint cross-validated against multiple free public sources; aggregator-only data labeled as such; hallucination audited; mermaid render-validated. Use when the user asks to research, audit, profile, or analyze any legal entity.
user-invocable: true
argument-hint: "<entity|path-to-md> [--about] [--validate-skill-sources] [--url=<url>] [--type=competitive|due-diligence|partnership|investment|research] [--depth=quick|standard|deep] [--audience=c-suite|technical|investor|board|operator] [--stage=seed|series-a|series-b|series-c|growth|pe|public] [--vertical=healthcare|fintech|govtech|edtech|legaltech|devtools|consumer|saas|deeptech] [--framework=swot|pestel|porter5|vrio|value-chain|all] [--analytic-rigor=standard|high] [--source-rating=admiralty] [--agents=solo|validation|parallel|max] [--output=<path>] [--export=md|html|pdf|exec|battle-card|vc-memo|json|expert-call-questions|customer-reference-questions|both] [--publish=notion|confluence|gdocs|coda] [--compare=A.md,B.md] [--year-over-year] [--benchmark[=cohort]] [--audit=pricing|tech-stack|customer-concentration|ai-maturity] [--data-sources=sec,wayback,github,linkedin,uspto,pacer] [--mcp-serve] [--no-reddit] [--no-competitors] [--no-glossary] [--no-risk-scan] [--language=en|de|...] [--dry-run]"
---

# Research Entity — Competitive / Due-Diligence Dossier

Generate a board-ready research report on any legal entity. Modular skill: this entrypoint defines the workflow + arguments; segment files contain the heavy reference content (registers, review platforms, mermaid validation, exports, voice rules, persona library, lessons).

## Modular skill structure

**Core (always or commonly loaded):**

| File | Loaded when |
|---|---|
| **SKILL.md** (this file) | Always — entrypoint |
| **registers.md** | Entity is non-US OR has international subsidiaries OR §3.4 Related Entities needs verifying any non-US legal entity |
| **reviews-platforms.md** | Step 2 (source gathering) + Step 4 (drafting §11 Community Reception) + §16 negative-review evidence + persona-specific Playbook (talent, customer-renewal, press) |
| **mermaid-validation.md** | After Step 4 (Draft) + before any HTML/PDF export + after post-draft edits to mermaid |
| **exports.md** | `--export=html\|pdf\|both` set OR convert-only mode |
| **voice-and-style.md** | Step 4 (Draft) + any post-draft revision |
| **citations.md** | Step 4 (Draft) — to know `--citations=inline\|footnotes\|endnotes` style + when user asks to convert between styles |
| **playbook-personas.md** | Writing §0 Strategic Response Playbook |
| **lessons.md** | Reviewing draft for failure-mode patterns + user pushback on aggregator-derived data |
| **confidence-scoring.md** | Step 8 — writing the §23 Appendix — Confidence & Methodology section |
| **glossary-catalog.md** | Step 4 — writing §22 Glossary; pre-defined catalog of ~100+ canonical entries across funding / standards / security / AI / sales / business-registers categories. Use as a menu against the body scan, not as a literal copy-paste. |
| **risk-scan.md** | Always at Step 2 — produces §16.X Red-Flag Scan unless `--no-risk-scan`. 8 patterns: layoffs, exec departures, lawsuits, breaches, regulatory, Glassdoor, status outages, leadership controversy. |

**Stage / vertical / template modifiers:**

| File | Loaded when |
|---|---|
| **stage-templates.md** | `--stage=` set OR auto-detected from /about + funding rows (seed / series-a / series-b / series-c / growth / pe / public) |
| **vertical-templates.md** | `--vertical=` set OR auto-detected from /about keywords (healthcare / fintech / govtech / edtech / legaltech / devtools / consumer / saas / deeptech) |

**Modes:**

| File | Loaded when |
|---|---|
| **comparison-mode.md** | `--compare=A.md,B.md` OR `--year-over-year` set — produces side-by-side or YoY-diff dossier instead of single-entity |
| **stale-detection.md** | Convert-only mode (always — to flag freshness before exporting) OR after Step 8 in full-research mode OR user asks "is this still accurate?" |
| **mcp-server.md** | `--mcp-serve` set OR user asks "expose dossiers as MCP" / "make this queryable" |

**Extended data sources & deep-dives:**

| File | Loaded when |
|---|---|
| **data-sources-extended.md** | `--data-sources=` set OR auto-activated (US-incorporated → SEC EDGAR; devtool → GitHub; deeptech → USPTO; always cheap → Wayback + LinkedIn + PACER) |
| **benchmarks.md** | `--benchmark` set OR `--stage=series-b\|growth\|pe\|public` (auto). Adds §X Industry Benchmarks comparing to public cohort medians (Bessemer / OpenView / KeyBanc / ICONIQ / Battery / Sapphire). |
| **audits.md** | `--audit=pricing\|tech-stack\|customer-concentration\|ai-maturity` set (composable) — adds focused deep-dive subsections beyond the default 23 |

**v2.2 Professional methodology layer (gold-standard intelligence-community + Big 4 CDD techniques):**

| File | Loaded when |
|---|---|
| **analytic-techniques.md** | `--type=due-diligence\|investment` (always) OR `--analytic-rigor=high` set. Implements ACH (Heuer/CIA Analysis of Competing Hypotheses), SATs (Devil's Advocate, Pre-mortem, Key Assumptions Check), and ICD 203 expressed-uncertainty discipline. |
| **source-rating.md** | `--source-rating=admiralty` set OR `--type=due-diligence\|investment` AND `--validation=max`. Applies the formal NATO/Five Eyes A-F × 1-6 source rating notation alongside our existing ad-hoc labels. |
| **frameworks.md** | `--framework=` set with anything beyond `swot` (e.g. `pestel`, `porter5`, `vrio`, `value-chain`, `all`) OR auto-activated by `--vertical=` (PESTEL for govtech/healthcare/fintech/edtech/legaltech; Porter5 for consumer; VRIO for devtools/deeptech). |
| **expert-calls.md** | `--export=expert-call-questions\|customer-reference-questions` set OR `--type=due-diligence\|investment` AND `--depth=deep` (auto). Generates Tegus/GLG/Third Bridge expert-call question batteries + 3 variants of customer reference call templates (current, churned, lost-deal-prospect). |
| **competitor-verification.md** | **MANDATORY** for `--type=competitive\|due-diligence\|investment` before §10 Market Positioning ships. Pre-publication verification protocol for competitor-row data — lead-investor identity (≥3 sources, named-partner attribution preferred), HQ city (press release dateline canonical), bundled-announcement round structure (Bloomberg/TC primary breakdown), numeric-figure attribution drift (verify cited number is in cited source). Codifies lessons #41-45 from `lessons.md` into an executable checklist. |

**v2.6 Public-source verification + ARR triangulation + regulatory overlay layer:**

| File | Loaded when |
|---|---|
| **source-hierarchy.md** | **MANDATORY** for `--type=competitive\|due-diligence\|investment`. Codifies a 4-tier source hierarchy (T1 primary registers/filings/press-release-datelines · T2 named-byline financial press · T3 structured analyst databases · T4 aggregator paraphrase). Adds Wayback Machine forensic source-dating (verify what page said when claim applied) and customer-logo round-trip verification (catch logo-wash). Citations: SPJ Code of Ethics, AICPA AT-C 105, ICIJ standards, Bellingcat handbook, Reuters Handbook of Journalism. |
| **marketplace-signals.md** | Auto-load when entity has any marketplace listing (Salesforce AppExchange / HubSpot Marketplace / Atlassian Marketplace / Microsoft AppSource / Slack App Directory / Chrome Web Store / AWS Marketplace / npm / PyPI / GitHub Marketplace). Marketplace install counts are often the only public usage signal for B2B SaaS. Atlassian Marketplace is the gold standard (exact daily-refreshed install counts). |
| **osint-public.md** | `--depth=deep` AND any of: `--vertical=security\|fintech\|govtech` (auto-load MITRE ATT&CK / KEV / NVD CVE) OR `--data-sources=` includes `dns`, `trademark`, `mitre`, `linkedin-velocity`, `job-velocity`. Five OSINT layers — job-posting velocity (Greenhouse/Lever/Ashby), MITRE ATT&CK + CISA KEV + NVD, DNS / passive DNS / SSL transparency (crt.sh, SecurityTrails), trademark (USPTO TM Search / EUIPO / WIPO), founder LinkedIn velocity. |
| **arr-triangulation.md** | `--type=investment\|due-diligence` AND entity is private SaaS without disclosed audited ARR. ARR-proxy math via Bessemer / OpenView / KeyBanc / ICONIQ / Sapphire $/FTE benchmarks; AE-quota × attainment; marketplace-install conversion; web-traffic conversion. |
| **regulatory-overlay.md** | Auto-load when entity has international operations OR `--vertical=healthcare\|fintech\|govtech\|legaltech\|edtech` OR `--type=due-diligence`. Combines Ghemawat CAGE Distance Framework (HBR 2001) + regulatory exposure (GDPR, EU AI Act, OFAC, HIPAA, PCI DSS, FedRAMP, ISO 27001, etc.). |
| **press-analysis.md** | Always for `--type=due-diligence\|investment` and `--depth=deep`. Three layered analyses: earned-vs-paid press distinction (PRovoke EMI + AMEC Barcelona Principles), conference / event presence (marketing-budget proxy), trust-center auditor verification (Drata/Vanta/Secureframe-hosted vs. self-published; AICPA Peer Review + IAF accreditation lookups). |

**v2.12 SaaS-CXO layer (NEW — Tier S high-leverage outputs for SaaS executives):**

| File | Loaded when |
|---|---|
| **win-loss.md** | `--win-loss` flag set OR `--type=competitive` AND `--audience=c-suite\|operator\|investor` (auto-suggest) OR user asks "where do they win?" / "what's their win rate?" / "why do we lose to them?". Codifies public-source win/loss inference (G2/TrustRadius "switched from / switched to" verbatim mining, Reddit thread mining, comparison-page narrative analysis, Glassdoor sales-team commentary) + with-input-data mode (`--win-loss=<csv>` integrates user's own deal data as ground-truth). Industry validation: [Klue](https://klue.com/blog/win-loss-analysis-guide), [Crayon G2 category](https://www.g2.com/categories/win-loss-analysis-services), [Monetizely](https://www.getmonetizely.com/articles/mastering-competitive-intelligence-how-to-track-winloss-rates-in-the-saas-landscape). Win-rate benchmarks: 20-35% average / 40-50% high-growth / >50% category-defining. Adds Cat J techniques #73, #83, #89 (win-rate-without-denominator rule, win-driver-needs-3-reviews, verbatim-quote discipline). |
| **saas-economics.md** | Auto-load when `--audience=board\|investor` set OR `--type=investment\|due-diligence` AND entity is private B2B SaaS without disclosed audited financials, OR `--unit-economics` flag set. Multi-method estimation rubrics for NRR / CAC / LTV / CAC Payback. **Bessemer canonical tiers (the language SaaS boards speak):** 100/110/120 = Good/Better/Best. ICONIQ at-$10M-ARR portfolio: bottom 105% / median 140% / top >145%. Methods: expansion-team inference, case-study upgrade narrative density, investor-disclosure mining, churn-signal inverse-correlation. Adds Cat J techniques #74, #75, #84 (Bessemer-canonical-tier discipline, multi-method estimate band rule, cohort-benchmark citation). |
| **moat-scoring.md** | Auto-load when `--audience=board\|investor` OR `--type=due-diligence\|investment` AND `--depth=deep`, OR `--moat=helmer` flag set. Implements [Hamilton Helmer's 7 Powers framework](https://7powers.com/) — the SaaS-investor-class moat lexicon validated by Helmer's 22-year **41.5% CAGR vs 14.9% S&P 500**. Each of 7 powers (Scale Economies / Network Economies / Counter-Positioning / Switching Costs / Branding / Cornered Resource / Process Power) scored 0-3 with explicit public-source evidence. **Powers don't sum** — any single power of 3+ can sustain a business. Adds Cat J techniques #76, #77, #78, #85, #86 (Helmer no-aggregation rule, switching cost friction mechanism, network effect degree-N evidence, counter-positioning incumbent-paralysis, process power 5+ year evidence). |
| **roadmap-inference.md** | Auto-load when `--depth=deep` AND `--type=competitive\|due-diligence\|investment`, OR `--roadmap` flag set. Five-channel public-source inference: job postings (3-9mo horizon), GitHub commits (1-3mo), patents (12-36mo, 40-60% abandonment), conference talks (6-18mo), beta-program leaks (variable). Critical caveat: patent filing ≠ product shipping. Industry validation: [Rathvane](https://rathvane.ai/blog/patent-analysis-competitive-intelligence.html), [Aqute](https://www.aqute.com/blog/patent-search-tools-for-competitor-analysis), [Visualping](https://visualping.io/blog/what-is-competitive-intelligence). Adds Cat J techniques #79, #80, #81, #82, #87, #88 (patent ≠ product, job-posting horizon, conference ≠ shipping, GitHub ≠ direction, multi-channel convergence, counter-evidence check). |

**v2.7-v2.11 Internal-consistency + framing-discipline + claim-coverage layer:**

| File | Loaded when |
|---|---|
| **internal-consistency.md** | **MANDATORY** at Step 5 (Validate) for `--type=competitive\|due-diligence\|investment` AND for any dossier edited across multiple revisions. Codifies Cat J anti-hallucination techniques (#50-72) across 23 failure patterns. **v2.7 (#50-57):** internal-consistency cross-reference scan, version-label sweep, audit-completion-rate honesty, numeric-precision discipline, tier-generosity check, triangulation-independence test, default-outcome probability check, two-dimension confidence rule. **v2.9 (#58-60):** count-vs-enumeration reconciliation, terminology-rename residue sweep, duplicate-paragraph scan. **NEW v2.11 (#61-72)** caught by reader-side validation 2026-04-27 on AcmeCRM brief: speaker-vs-founder identity discipline (#61 — press-release quote attributions ≠ founder list), aggregator-data freshness sweep (#62 — T3 citations >12mo need refresh search), parent-network multiplier acknowledgement (#63 — headcount-velocity claims must include parent-network from same source), comprehensive comparison-directory probe (#64 — `<entity>/comparison/` is the highest-leverage source for `--type=competitive`), "not publicly disclosed" verification ladder (#65 — check legal-firm + deal-database + regulatory-filings before claiming privacy), single-feature → category-claim guard (#66 — slot-filling pressure), negation-evidence rule (#67 — "no X" claims need surface + date + searched-strings), quasi-deterministic-claim guard (#68 — "categorically beyond / cannot trivially / will never" → Tetlock-rewrite), comparator-pricing source rule (#69 — competitor prices must link to that competitor's /pricing), subagent-audit blindspot rule (#70 — Step 6 audit shares writer's blindspots; require fresh-fetch sample), load-bearing claim N-source rule (#71 — claim repeated 3+ times needs ≥2 sources), round-number / no-methodology vendor-metric labeling (#72). |

**v2.8 Skill maintenance + sources-of-record layer:**

| File | Loaded when |
|---|---|
| **sources-of-record.md** | `--validate-skill-sources` flag set OR maintainer is updating skill citations OR onboarding new maintainer. Central registry of every load-bearing external source cited by the skill — primary URL, backup/mirror, last-verified date, update cadence (frozen / annual / continuous / irregular), decay-risk flag (STABLE / ANNUAL / CONTINUOUS / URL-PRONE / REGULATORY / SHUTDOWN-RISK), cited-in file list, migration notes. Single source of truth for skill maintenance — when a source migrates, update one row instead of search-and-replacing across 39 files. Organized into 11 categories (A-K). Includes monthly/quarterly/annual maintenance protocols. |
| **about.md** | `--about` flag set — print self-documentation (5 methodology layers, 35 anti-hallucination techniques, comparison to Big 4 / Klue / Forrester / Gartner standards, version history, invocation examples, cost/runtime). **Mutually exclusive with dossier generation** — when `--about` is set, do NOT run any research/draft steps. |
| **multi-agent.md** | `--agents=` flag set OR auto-activated by `--depth=deep` (parallel) / `--type=due-diligence\|investment` (max). Defines 4-level parallelism strategy (solo / validation / parallel / max) with which workstreams delegate to subagents at each level. Max-mode adds independent ACH agent (blind to main draft), Devil's Advocate, Pre-mortem, Key Assumptions Check, per-pattern risk-scan, fact-check. |

**v2.4 Strategic-analysis layer (futures + valuation + strategy classics):**

| File | Loaded when |
|---|---|
| **scenarios.md** | `--scenarios=2x2\|cone-of-plausibility\|both` set OR `--type=due-diligence\|investment` AND `--depth=deep` (auto). Implements Royal Dutch Shell scenario-planning (2x2 axes) + Hancock & Bezold Cone of Plausibility for 3-5 year forward-looking analysis. |
| **valuation.md** | `--valuation=dcf\|comps\|public-multiples\|lbo\|all` set OR `--type=investment` AND `--depth=deep` (auto). Implements 4 canonical valuation methodologies: DCF, Comparable Transactions, Public-Comp Multiples, LBO Modeling. Required for `--export=vc-memo`. |
| **strategy-classics.md** | `--framework=` includes `christensen\|moore\|rumelt\|jtbd\|wardley\|classics\|all`. Implements 5 strategy classics: Christensen Disruption Theory, Moore Crossing the Chasm, Rumelt Strategy Kernel (alternative to SWOT for synthesis), Christensen/Ulwick Job-to-be-Done, Wardley Mapping. Auto-loads JTBD + Christensen for `--type=investment`; Rumelt Strategy Kernel for `--type=due-diligence` + `--depth=deep`. |

**Output formats & publishing:**

| File | Loaded when |
|---|---|
| **output-formats.md** | `--export=` includes `exec`, `battle-card`, `vc-memo`, or `json` — alternate condensed/repurposed views |
| **output-publish.md** | `--publish=notion\|confluence\|gdocs\|coda` set — direct publish to collaborative platforms via API |

The model loads each segment via the `Read` tool when its trigger condition is met. SKILL.md stays lean; segments are loaded on demand.

## Arguments

- `$1` (required, positional) — **Entity name** (e.g. `"Stripe"`, `"Acme Corp"`, `"Example Co"`) **OR** a **path to an existing `.md` dossier** to convert. If the positional arg is a path ending in `.md` and the file exists, the skill switches to **convert-only mode** and skips all research/draft steps.
- `--convert=<path>` — explicit convert-only mode: take an existing MD dossier and produce HTML/PDF only.
- `--url=<url>` — primary company URL if known. Discovered via search if omitted. (Ignored in convert-only mode.)
- `--type=<mode>` — `competitive` (default) / `due-diligence` / `partnership` / `investment` / `research` (neutral self-portrait, e.g., when researching the user's own employer)
- `--depth=<quick|standard|deep>` — source count + agent parallelism. Default: `standard`.
- `--audience=<audience>` — `c-suite` (default) / `technical` / `investor` / `board` / `operator`. Determines which Playbook personas appear.
- `--stage=<seed|series-a|series-b|series-c|growth|pe|public>` — stage modifier; tunes section emphasis + adds stage-specific subsections (load `stage-templates.md`). Auto-detects from /about + funding rows if not set.
- `--vertical=<healthcare|fintech|govtech|edtech|legaltech|devtools|consumer|saas|deeptech>` — vertical modifier; surfaces vertical-specific compliance, integrations, regulators, review platforms (load `vertical-templates.md`). Auto-detects from /about keywords if not set.
- `--compare=<A.md,B.md[,C.md]>` — side-by-side comparison of 2+ existing dossiers; produces 15-section comparison output rather than single-entity dossier (load `comparison-mode.md`).
- `--year-over-year` — auto-detect prior dossier in same directory; generate "what changed" diff after full re-research (load `comparison-mode.md`).
- `--benchmark[=cohort]` — add §X Industry Benchmarks comparing to cohort medians (Bessemer / OpenView / KeyBanc / ICONIQ / Battery / Sapphire); cohort defaults to `public-saas` (load `benchmarks.md`). Auto-activates for `--stage=series-b` and later.
- `--audit=<scope[,scope]>` — focused deep-dive audits beyond the default 23 sections; composable. Scopes: `pricing` / `tech-stack` / `customer-concentration` / `ai-maturity` (load `audits.md`).
- `--data-sources=<list>` — explicit additional source families: `sec` (EDGAR), `wayback` (Wayback Machine), `github` (devtools), `linkedin` (hiring velocity), `uspto` (patents), `pacer` (court records). Auto-activated by entity context (load `data-sources-extended.md`).
- `--no-risk-scan` — skip the always-on §16.X Red-Flag Scan (8-pattern automated scan). NOT recommended; risk findings are highest-ROI dossier output (load `risk-scan.md`).
- `--mcp-serve` — start the self-MCP server exposing the user's dossier library to future Claude sessions (load `mcp-server.md`).
- `--about` — print the skill's self-documentation (load `about.md` and output its template content). Shows: 5 methodology layers (Foundational / Source-provenance / Strategic-frameworks / IC-tradecraft / Industry-CI / SaaS-CXO), **89 anti-hallucination techniques** (organized into 10 categories — A-J), comparison to Big 4 / Klue / Forrester / Gartner / Helmer standards, version history (v1 → v2.0 → v2.1 → v2.2 → v2.3 → v2.4 → v2.5 → v2.6 → v2.7 → v2.8 → v2.9 → v2.10 → v2.11 → v2.12), invocation examples, cost/runtime expectations. **Mutually exclusive with dossier generation** — when `--about` is set, do NOT run any research/draft steps; print the about content and exit.
- `--validate-skill-sources` — **maintenance mode** (NEW v2.8). Run URL-validation across all skill segment files + cross-reference `sources-of-record.md` last-verified dates + flag URLs >12 months unverified + flag known-shutdown-risk vendors + flag URL migrations (404 / persistent 5xx). Outputs a remediation plan to terminal — does NOT modify skill files. **Mutually exclusive with dossier generation** — when set, do NOT run any research/draft steps; run maintenance and exit. Recommended cadence: monthly (via `/schedule`).
- `--framework=<list>` — strategic frameworks to apply. **Porter-era** (load `frameworks.md`): `swot` (default in §0) / `pestel` / `porter5` / `vrio` / `value-chain`. **Strategy classics** (load `strategy-classics.md`): `christensen` (Disruption) / `moore` (Crossing the Chasm) / `rumelt` (Strategy Kernel) / `jtbd` (Job-to-be-Done) / `wardley` (Wardley Mapping). **Aggregates**: `classics` (loads strategy-classics.md only) / `all` (loads both files, all 10 frameworks). Composable. Auto-activated by `--vertical=` (PESTEL for govtech/healthcare/fintech/edtech/legaltech; Porter5 for consumer; VRIO for devtools/deeptech). Auto-loads JTBD + Christensen for `--type=investment`; Strategy Kernel for `--type=due-diligence` + `--depth=deep`.
- `--scenarios=<method>` — scenario planning: `2x2` (Royal Dutch Shell/GBN matrix) / `cone-of-plausibility` (Hancock & Bezold futures-fanning) / `both`. Auto-activated for `--type=due-diligence|investment` with `--depth=deep`. Load `scenarios.md`.
- `--valuation=<method>` — valuation methodologies for `--type=investment`: `dcf` (Discounted Cash Flow) / `comps` (Comparable Transactions) / `public-multiples` / `lbo` (LBO Modeling) / `all`. Auto-activated for `--type=investment` AND `--depth=deep`. Load `valuation.md`.
- `--analytic-rigor=<level>` — `standard` (default) / `high`. When `high`, loads `analytic-techniques.md` and inserts ACH (Analysis of Competing Hypotheses), SATs (Devil's Advocate, Pre-mortem, Key Assumptions Check), and ICD 203 expressed-uncertainty discipline into the dossier. Auto-activated for `--type=due-diligence|investment`.
- `--win-loss[=<csv>]` — **NEW v2.12.** Add §10.X Win/Loss Intelligence subsection (load `win-loss.md`). With `=<csv>` argument, integrates user's own deal data as ground-truth alongside public-source inference. Without csv, runs public-source inference only (G2/TrustRadius/Reddit/comparison-page mining). Auto-suggested for `--type=competitive` + `--audience=c-suite|operator|investor`.
- `--unit-economics` — **NEW v2.12.** Add §X SaaS Economics subsection with NRR / CAC / LTV / CAC-Payback estimates (load `saas-economics.md`). Multi-method estimation against Bessemer canonical tiers (100/110/120 = Good/Better/Best). Auto-activated for `--audience=board|investor` and for `--type=investment|due-diligence` when entity is private B2B SaaS without disclosed audited financials.
- `--moat=<framework>` — **NEW v2.12.** Add §17.X Moat Scoring subsection (load `moat-scoring.md`). `helmer` applies Hamilton Helmer's 7 Powers framework (the SaaS-investor-class moat lexicon — 41.5% CAGR vs 14.9% S&P 500 over 22 years). Each power scored 0-3 with public-source evidence; powers don't sum. Auto-activated for `--audience=board|investor` AND `--depth=deep`.
- `--roadmap` — **NEW v2.12.** Add §7.X Roadmap Inference subsection (load `roadmap-inference.md`). Five-channel public-source inference (job postings, GitHub, patents, conference talks, beta leaks). Auto-activated for `--depth=deep` AND `--type=competitive|due-diligence|investment`.
- `--source-rating=<scheme>` — `admiralty` applies the formal NATO/Five Eyes A-F × 1-6 source rating notation alongside our existing ad-hoc labels. Load `source-rating.md`. Auto-activated for `--type=due-diligence|investment` AND `--validation=max`.
- `--agents=<level>` — multi-agent parallelism: `solo` (1 agent, default for `--depth=quick`) / `validation` (2-3 agents, default for `--depth=standard`) / `parallel` (5-7 agents, default for `--depth=deep`) / `max` (10-12 agents, default for `--type=due-diligence|investment`). Higher levels = faster wall-clock + higher cost + better independent-perspective quality. `max` adds INDEPENDENT analytic-technique agents (ACH agent that doesn't see the main draft, Devil's Advocate, Pre-mortem, Key Assumptions Check, per-pattern risk-scan, fact-check) for true confirmation-bias resistance. Load `multi-agent.md`.
- `--output=<path>` — MD output path. Default: `./<entity-slug>-research.md` (CWD root — the directory the skill was launched from). Do NOT auto-create or write into a `./research/` subfolder unless the user explicitly passes `--output=./research/...` or asks for a subfolder.
- `--export=<format[,format]>` — `md` (default) / `html` / `pdf` / `both` (canonical formats; load `exports.md`) OR `exec` (1-page summary) / `battle-card` (sales card) / `vc-memo` (investment memo) / `json` (structured data) (alternate condensed/repurposed views; load `output-formats.md`). Composable.
- `--publish=<destination>` — direct publish via API: `notion` / `confluence` / `gdocs` / `coda`. Requires env-var auth (load `output-publish.md`).
- `--citations=<style>` — `inline` (default) / `footnotes` / `endnotes`. See `citations.md` for format rules and conversion between styles. Default `inline` is best for digital reading; `footnotes` is best for source-heavy `--depth=deep` dossiers (deduplicates the same URL cited many times) and for print.
- `--no-wizard` — skip the interactive wizard even if no flags were provided. Useful for CLI / scripted invocations.
- `--validation=<level>` — validation rigor. `light` (1 agent, 1-source acceptable) / `standard` (2 agents, 2-source rule, hallucination audit) / `max` (3 agents, ≥2 sources for §0/§2 + ≥3 for headline claims, full audit, dynamic mermaid render). Default: `standard` for `--depth=standard`, `max` for `--depth=deep`.
- `--no-confidence-score` — skip writing §23 Appendix — Confidence & Methodology. Default: include.
- `--no-model-warning` — suppress the model + effort warning at Step 1. Default: warn if model is not Opus 4.7 OR effort is not max.
- `--no-reddit` / `--no-competitors` / `--no-glossary` / `--no-watchlist` / `--no-cost-math` / `--no-mermaid` / `--no-validate-urls` / `--no-hallucination-audit` / `--no-cross-validation` / `--no-revalidate-urls` (convert-only) — opt-out flags.
- `--language=<code>` — output language. Default: `en`.
- `--dry-run` — print the plan without writing.

## Required tools

The skill prefers Tavily MCP tools when available, falls back to WebSearch + WebFetch:

- `mcp__tavily__tavily_search` / `mcp__tavily__tavily_extract` — primary, fall back on HTTP 432 / quota
- `WebSearch` / `WebFetch` — always-available fallback
- `Bash` — URL validation, file writes, mkdir, mermaid validation, pandoc/xelatex for export
- `Agent` — REQUIRED for `--depth=deep`; spawn 2–3 parallel cross-validation agents
- `Read` / `Edit` / `Write` — file operations (incl. loading segment files)

## Convert-only mode

When `$1` is a path to an existing `.md` file (or `--convert=<path>` is set), skip Steps 1–4 and 6 entirely. Run mermaid validation + URL revalidation (default ON; `--no-revalidate-urls` to skip) + Step 7 (Export). Output paths derive from input: `/path/to/<entity>-research.{html,pdf}`.

## Output structure (23 sections — stable numbering)

**Front matter:** `title`, `subject`, `research_date`, `researcher`, `validation`, `report_type`, `depth`.

**§0 Executive Briefing** — BLUF (≤200 words) + Scorecard (15 rows; **every Signal cell is a dot PLUS a one-or-two-word label — `🟢 Strong`, `🟡 Unverified`, `🔴 Absent`, `⚪ N/A` — never a bare dot**, per the signal-label discipline in `voice-and-style.md`) + SWOT (2×2) + Strategic Position Heat Map + Strategic Response Playbook (load `playbook-personas.md`) + Monitoring Watchlist (10–12 signals) + framework disclaimer.

**§1** Executive Summary · **§2** Company Fundamentals (with conflict-flagged sources) · **§3** Founders & Senior Leadership (incl. mandatory `§3.4 Related Entities` mermaid distinguishing founded / employed / contracted relationships) · **§4** Funding & Investors · **§5** Product Architecture · **§6** Technical Architecture · **§7** Feature Catalog · **§8** Pricing · **§9** Customer Base · **§10** Market Positioning & Competition (incl. `§10.5 [Capability] Adoption Across [Market]` for first-mover claims) · **§11** Community Reception (load `reviews-platforms.md`) · **§12** Data Asset · **§13** Integrations · **§14** Security & Trust · **§15** Content Marketing & Analyst Coverage · **§16** Risks & Weaknesses (incl. mandatory `§16.X Data Verifiability` subsection) · **§17** Strategic Analysis · **§18** Full Ecosystem View · **§19** Sources · **§20** Quote Bank · **§21** Final Assessment · **§22** Glossary.

## Workflow

### Step 0 — Early-exit modes (highest priority)

#### Step 0a — `--about` early exit
If `--about` is set, **load `about.md` and print its template content directly to the user**. Do NOT run any research, draft, or export steps. The skill is in informational-only mode. Exit cleanly. This check runs before mode detection.

#### Step 0b — `--validate-skill-sources` maintenance mode (NEW v2.8)

If `--validate-skill-sources` is set, run skill-maintenance audit:

1. **Load `sources-of-record.md`** — the canonical registry of cited external sources.

2. **Extract all URLs from skill files**:
```bash
# Collect every URL the skill files reference, deduplicated
grep -rhoE 'https?://[a-zA-Z0-9.-]+(/[a-zA-Z0-9._/?=&%~+#-]*)?' ~/.claude/skills/research-entity/ \
  | sed 's/[.,;)"]*$//' \
  | sort -u > /tmp/skill-urls.txt
```

3. **Run URL validation**:
```bash
# Resolve each one, following redirects, with a browser user-agent
while read -r url; do
  code=$(curl -s -o /dev/null -w "%{http_code}" -L --max-time 15 \
    -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36" \
    "$url" 2>/dev/null)
  echo "$code $url"
done < /tmp/skill-urls.txt | sort -n > /tmp/skill-url-check.txt
```

4. **Cross-reference with `sources-of-record.md`**:
   - Parse the registry rows; extract `last-verified` date and decay-risk for each source
   - Compute "months since last verified" for each
   - Flag any source with `>12 months unverified` AND risk in [URL-PRONE, REGULATORY, ANNUAL]
   - Flag any source flagged `SHUTDOWN-RISK` regardless of last-verified date
   - Flag any URL returning HTTP 404 / persistent 5xx
   - Flag any HTTP 301/302 redirects (URL has migrated — registry should be updated)

5. **Cross-check skill files for URLs NOT in registry** — surfaces newly-added citations that haven't been registered

6. **Output remediation plan** (to terminal, does NOT modify skill files):

```markdown
## Skill-source maintenance report — YYYY-MM-DD

### URL validation summary
- ✅ HTTP 200 (resolved): X URLs
- ⚠️ HTTP 301/302 (redirect — update registry): Y URLs
- ❌ HTTP 404 (broken): Z URLs
- ⚠️ HTTP 403/999 (bot-blocked, likely valid): W URLs

### Last-verified staleness
- Sources >12 months unverified: <list with category + remediation note>
- Sources >24 months unverified: <list — high priority>

### Shutdown-risk monitoring
- Confirmed shutdown (already flagged in registry): <list>
- Sustainability concerns: <list>

### Registry drift
- URLs in skill files NOT in sources-of-record.md: <list — need to register>
- URLs in registry NOT in any skill file: <list — may be obsolete>

### Recommended actions (ranked by priority)
1. <Highest priority — broken URLs blocking dossier generation>
2. <Migrated URLs needing registry update>
3. <Stale verifications needing manual review>
4. <Optional clean-up — registry deduplication>
```

7. **Output the report and exit cleanly.** The skill is in maintenance-only mode. Do NOT run any research/draft/export steps.

**Recommended cadence:** Monthly via `/schedule`:
```
/schedule "0 9 1 * *" "/research-entity --validate-skill-sources"
```

This runs the validation on the 1st of each month at 09:00. Adjust cadence as needed:
- **Monthly** for active maintenance
- **Quarterly** for low-touch maintenance
- **Annually** for archived skill

### Step 1 — Plan & mode detection

1. **Mode detection (first):**
   - If `$1` matches `/\.md$/` AND file exists, OR `--convert=<path>` is set with existing file → **convert-only mode**. Announce: "Convert-only: reading {path}. Skipping research; exporting to {format}." Jump to Step 5 (mermaid + URL revalidation) → Step 7 (Export) → Step 8 (Report).
   - Otherwise → **full research mode**. Continue.

2. **Model + effort pre-flight (REQUIRED unless `--no-model-warning`):**
   This skill produces highest-fidelity output with **Claude Opus 4.7 + MAX effort**. Lower configurations introduce specific failure modes (see below). At Step 1, check the active model + effort and if the user is below recommended config, surface a clear warning:

   > ⚠️ **Model & effort check:** This skill produces highest-quality output with **Claude Opus 4.7 + MAX effort** (`/effort max`).
   >
   > **Currently detected:** `<model>` with `<effort>` effort.
   >
   > If you're on:
   > - **Sonnet / Haiku / older Opus** — substantially higher hallucination risk on competitive funding figures, founder-exit narratives, and temporal claims ("first mainstream X"). Cross-source corroboration discipline is harder to maintain. Mermaid syntax errors more likely.
   > - **Effort below max** — shorter reasoning chains; multi-step validation may be skipped; subagent cross-validation may not be invoked.
   > - **`/fast` mode (Opus 4.6)** — slightly faster output; reasoning depth comparable but specifically designed for shorter conversations.
   >
   > **Recommendation for board / regulated / due-diligence dossiers:** Opus 4.7 + `/effort max`. The composite confidence score will reflect the configuration in §23 Methodology.
   >
   > Continue anyway? (User can dismiss with `--no-model-warning` for repeat invocations.)

   The warning must be:
   - **Specific** about what fails at lower configs (not generic "results may vary")
   - **Tier-mapped** so user knows the exact failure modes per tier
   - **Dismissable** via flag for repeat use
   - **Reflected in §23** confidence-score methodology disclosure

3. **Wizard check:** if user invoked the skill with **only the entity name** (no `--type`, `--depth`, `--audience`, `--export`, `--citations`, `--validation`, `--url`, etc.) AND `--no-wizard` is not set → run the **interactive wizard** below.

4. Resolve canonical URL via search if `--url` not provided.
5. **Self-research detection**: if user's email domain matches entity's domain (per CLAUDE.md), auto-suggest `--type=research`.
6. Announce plan + dry-run check.

### Step 1b — Interactive wizard (when invoked without flags)

When the user runs `/research-entity "Some Company"` with no other parameters, do NOT silently default everything. Instead, run a friendly Q&A using `AskUserQuestion` (load via ToolSearch if needed). Present each question as a multiple-choice card with sensible defaults pre-explained.

**Question 1 — Research goal (`--type`):**
> What's the goal of this research?
- 🎯 **Competitive analysis** — comparing vs. your business (default for B2B competitive context)
- 🔍 **Due-diligence** — investment, acquisition, or partnership evaluation
- 💼 **Investment thesis** — VC / PE / strategic-buyer evaluation
- 🤝 **Partnership evaluation** — channel, integration, co-sell consideration
- 📚 **Neutral research** — self-portrait, no directional slant (auto-selected if your email domain matches the entity's)

**Question 2 — Audience (`--audience`):**
> Who's reading this?
- 👔 **C-suite** — leads with BLUF, Scorecard, SWOT (default for general-purpose)
- 💰 **Investor** — leads with funding, ARR signals, exit scenarios
- 🏛️ **Board** — short BLUF, single-page strategic summary, risk-heavy
- 🔧 **Operator** — leads with pricing, integrations, tool-consolidation math
- 🛠️ **Technical** — leads with architecture, stack, security posture

**Question 3 — Depth (`--depth`):**
> How deep should I go?
- ⚡ **Quick** (~5–10 minutes, ~500 lines, ~10 sources) — for scoping or quick brief
- 📊 **Standard** (~20–35 minutes, ~1000 lines, ~30–50 sources) — default; full 23 sections
- 🔬 **Deep** (~45–75 minutes, ~1500–1800 lines, ~80+ sources, 2–3 parallel cross-validation agents) — board-ready, max accuracy

**Question 4 — Export format (`--export`):**
> Output format?
- 📝 **Markdown only** (default) — for editing, sharing as text
- 🌐 **HTML** — sticky-sidebar TOC + scrollspy + print-ready CSS
- 📄 **PDF** — pandoc + xelatex (or browser print)
- 📦 **All three** (MD + HTML + PDF)

**Question 5 — Citation style (`--citations`):**
> How to handle source citations?
- 🔗 **Inline links** (default) — every claim links directly; click to jump to source
- 📚 **Footnotes** — sources at the bottom, referenced by tag; cleaner body for source-heavy dossiers
- 📖 **Endnotes** — academic style, sources only at §19; minimal body markup

**Question 6 — Validation rigor (`--validation`):**
> How thorough should the validation pipeline be?
- 🔬 **Maximum** — 3 parallel cross-validation agents (business-register + reviews + competitor-funding), ≥3 sources for §0 headline claims, ≥2 sources for §2 facts, full hallucination audit, dynamic `mmdc` mermaid render. Best for board / legal / regulated / due-diligence dossiers. **+15–20 min runtime.** (Default for `--depth=deep`.)
- 📊 **Standard** (default for `--depth=standard`) — 2 cross-validation agents, ≥2 sources for §0/§2, single-source claims labeled, full hallucination audit, mermaid static render. **+5–10 min runtime.**
- ⚡ **Light** — 1 validation agent, ≥1 source acceptable with explicit `single-source` labels, basic hallucination audit. For quick scoping briefs only. **No additional runtime.**
- ❌ **Off** (`--no-cross-validation`) — skips validation entirely. NOT recommended; downgrades the §23 confidence score significantly.

**Question 7 — Skip anything? (opt-out flags):**
> Anything to skip? (multi-select; defaults to no opt-outs)
- ⬛ Reddit research (`--no-reddit`)
- ⬛ Competitor landscape (`--no-competitors`)
- ⬛ Glossary (`--no-glossary`)
- ⬛ Cost-consolidation math (`--no-cost-math`)
- ⬛ Confidence-score appendix (`--no-confidence-score`)
- ⬛ Risk/red-flag scan (`--no-risk-scan`) — **NOT recommended; highest-ROI dossier output**
- ⬛ Hallucination audit (`--no-hallucination-audit`) — **NOT recommended**
- ⬛ Cross-validation pass (`--no-cross-validation`) — **NOT recommended**

**Question 8 — Stage (`--stage`):**
> What stage is the entity at? (auto-detected if you skip)
- 🌱 **Seed** — under $5M raised, <15 employees
- 🚀 **Series A** — $5–20M raised, 10–50 employees
- 📈 **Series B** — $20–60M raised, 50–200 employees
- 🏢 **Series C+** — $60M+ raised, late-stage / pre-IPO
- 💰 **Growth** — bootstrap + profitable, $20M+ ARR
- 🏦 **PE-owned** — mature, PE-backed
- 📊 **Public** — has ticker symbol on a major exchange
- 🤖 **Auto-detect** (default; reads /about + funding rows)

**Question 9 — Vertical (`--vertical`):**
> What industry vertical? (auto-detected if you skip)
- 🏥 **Healthcare** — HIPAA, EHR, hospital, telehealth
- 💳 **Fintech** — bank, lending, payment, KYC, AML
- 🏛️ **GovTech** — federal/state agency, FedRAMP, GSA
- 📚 **EdTech** — K-12, higher ed, LMS, FERPA
- ⚖️ **LegalTech** — law firm, e-discovery, legal AI
- 🛠️ **DevTools** — developer, API, SDK, CI/CD
- 🛍️ **Consumer** — DTC, mobile, subscription, marketplace
- ☁️ **SaaS** — generic B2B SaaS (default)
- 🔬 **DeepTech** — AI/ML model, hardware, biotech
- 🤖 **Auto-detect** (default; reads /about keywords)

**Question 10 — Add focused audit modules? (`--audit`)**
> Want any deep-dive audits beyond the default 23 sections? (multi-select; default: none)
- ⬛ **Pricing audit** — vs 5 competitors, hidden costs, Wayback price evolution
- ⬛ **Tech-stack audit** — BuiltWith + GitHub + job-posting inference
- ⬛ **Customer-concentration audit** — sample analysis, vertical/geo distribution
- ⬛ **AI-maturity audit** — model + safety + defensibility (recommended for AI vendors)

**Question 11 — Industry benchmarks? (`--benchmark`)**
> Compare to public benchmark medians? (Bessemer / OpenView / KeyBanc / ICONIQ — adds §X Industry Benchmarks)
- ✅ **Yes** — auto for `--stage=series-b` and later
- ❌ **No** — skip
- 🎯 **Yes, specific cohort**: public-saas / growth-stage / early-stage / ai-native / vertical-saas / devtools

**Question 12 — Multi-agent parallelism? (`--agents`)**
> Higher = faster wall-clock + higher API cost + better independent-perspective quality. Each level adds specific subagents that operate independently from the main session.
- 🤖 **Solo** (1 agent, sequential) — single Claude session does everything inline. **Best for**: quick scoping, throwaway research, cost-constrained runs. **~$2-5 cost · 30-60min**.
- 👥 **Validation** (2-3 agents) — spawns subagents for cross-validation (Step 3) + hallucination audit (Step 6). Each gets its own context window so the main session stays clean. **Default for `--depth=standard`**. **~$10-20 cost · 20-35min**.
- 🚀 **Parallel** (5-7 agents) — also spawns subagents for source gathering (Step 2) + per-audit-module (Step 4) + per-framework (Step 4). **Default for `--depth=deep`**. **~$25-50 cost · 25-45min**.
- 🌟 **Max** (10-12 agents) — adds **INDEPENDENT analytic-technique agents**: ACH agent that doesn't see the main draft (true confirmation-bias resistance), Devil's Advocate, Pre-mortem, Key Assumptions Check, per-pattern risk-scan (8 patterns × 1 agent), independent fact-check. **Default for `--type=due-diligence|investment`**. **~$60-120 cost · 30-60min** (parallelism balances against more agent calls).

The "max" mode is the only level that produces genuinely confirmation-bias-resistant analysis (the ACH agent generates competing hypotheses BLIND to the main session, so its hypotheses can't be biased by the draft narrative). For board / IC-grade outputs this is the load-bearing differentiator.

**After collecting answers**: confirm the resolved config back to the user in one summary line including the model+effort pre-flight result, then proceed to Step 2.

> Example confirmation:
> "✓ Researching **Acme Corp** | competitive analysis | C-suite audience | standard depth (~30 min) | inline citations | export: HTML + PDF | validation: standard (2 agents, ≥2 sources) | model: Opus 4.7 + max effort (✅ recommended). Starting source gathering now."
>
> Or if model is below recommended:
> "✓ Researching **Acme Corp** | ... | ⚠️ model: Sonnet 4.6 + standard effort. Hallucination risk elevated for competitive-funding figures + temporal claims. §23 confidence score will reflect this. Continuing in 5s; press Ctrl-C to abort and switch to Opus + /effort max."

**Skip wizard when:**
- `--no-wizard` flag set
- ANY non-default flag was provided (model infers user knows what they want)
- Convert-only mode (different code path)
- User explicitly typed all flags
- `--dry-run` is set (announce defaults instead)

### Step 1c — Stage + Vertical auto-detect (after wizard / before search)

If `--stage=` or `--vertical=` not set explicitly, run the auto-detection routines from `stage-templates.md` (stage detection) and `vertical-templates.md` (vertical detection) on the canonical /about + /products page. Surface the inference: "Detected `--stage=series-b --vertical=fintech` from page text. Use flags to override." Load the relevant template files for the rest of the run.

### Step 2 — Parallel source gathering

Run searches in parallel (one message). Respect `--depth`:

1. Extract canonical URL + sub-pages (`/about`, `/team`, `/careers`, `/blog`, `/pricing`, `/trust`, `/security`, `/products`, `/customers`, `/integrations`, `/press`)
2. `<entity> founder name`
3. `<entity> funding raised investors`
4. `<entity> review` (skip if `--no-reddit`) site-scoped to reddit.com
5. `<entity> vs alternatives comparison` (skip if `--no-competitors`)
6. `<entity> customer case study`
7. `<entity>` site-scoped to g2.com, capterra.com, trustpilot.com, glassdoor.com, gartner.com (load `reviews-platforms.md`)
8. `<entity> podcast interview`
9. **Risk scan (always-on; load `risk-scan.md`)** — 8 patterns in parallel: layoffs (layoffs.fyi + thelayoff.com), exec departures (LinkedIn role changes), lawsuits (CourtListener + PACER), data breaches (haveibeenpwned + databreaches.net), regulatory actions (SEC + FTC + CFPB + GDPR enforcement tracker), Glassdoor rating delta vs 12 months ago, status-page outage history, leadership controversy. Skip only if `--no-risk-scan`.
10. Aggregators: sacra.com, crunchbase.com, pitchbook.com, tracxn.com, craft.co, owler.com, cbinsights.com, getlatka.com, leadiq.com, rocketreach.co, zoominfo.com
11. **For non-US entities**: load `registers.md` + search the relevant country's free public business register
12. **For vertical-specific sources (load `vertical-templates.md`)**: per-vertical search additions (e.g., FedRAMP marketplace for govtech, KLAS for healthcare, GSA Schedule for govtech, IL ratings for defense)
13. **For extended data sources (load `data-sources-extended.md` if conditions met)**: SEC EDGAR (US-incorporated), Wayback Machine (always — cheap), GitHub (devtools), LinkedIn hiring (always — cheap), USPTO (deeptech / regulated), PACER (always — cheap)
14. **NEW v2.10 — Competitive comparison-page scan (MANDATORY for `--type=competitive` when user-employer-domain is known via CLAUDE.md memory).** Probe `<entity-domain>/comparison/`, `<entity-domain>/vs/`, and `<entity-domain>/alternatives/` directories AND specifically `<entity-domain>/comparison/<user-employer-slug>-vs-<entity-slug>/` (and the inverse slug ordering) for any page that names the user's employer. Pages found in this probe are T1 self-disclosed competitive-positioning artifacts and become a required §10.X "Active competitive positioning vs. <user-employer>" subsection in the dossier. Per `lessons.md` #70 — this is the single highest-leverage source-gathering step for users at competing entities; the failure mode is missing it entirely. For `--type=competitive` without user-employer-domain known, probe still runs against named Tier-A peers (Step 5 §10) — every Tier-A peer's `/comparison/<entity>-vs-<peer>/` URL is a high-yield T1 competitive intel source.
15. **NEW v2.10 — Parent-organization scale freshness sweep (MANDATORY when entity is a portfolio company / subsidiary / division).** When the entity has a known parent (acquirer, holding company, conglomerate division), search the **parent's most recent milestone announcement / press release** before citing any aggregator (T3) figure for parent scale. T3 aggregator data ages quickly for serial acquirers and fast-moving SaaS — a 2024 figure for a 2026 parent is structurally stale (per `lessons.md` #68). Confirm: parent ARR, acquisition count, employee count, country count, current AI/operating-strategy initiatives. Cross-check against parent's `/about` or `/leadership` page for **current founder/leadership identity** — never trust the deal-announcement signatory list as the founders list (per `lessons.md` #67).

For results > 30K chars, delegate extraction to `Agent` subagent.

### Step 3 — Cross-validation pass (REQUIRED)

**Two-source rule:** every Scorecard / §1 / §2 datapoint needs ≥2 independent sources OR a `single-source` / `aggregator-derived` / `vendor-claimed` / `founder-self-reported` label.

**Aggregator failure modes:** see `lessons.md`. Every aggregator (Latka, RocketReach, PitchBook, Crunchbase, Tracxn, Owler, Craft.co, LeadIQ, ZoomInfo) has known failure modes that must be flagged.

**Founder-claim verification:** any narrative implying a founder achieved an exit / built a $XXX million company MUST be cross-checked against Wikipedia + acquirer press + investor exit announcement. Don't repeat misframed narratives.

**Subagent cross-validation (REQUIRED for `--depth=deep`):** spawn 2–3 parallel agents:
1. **Business-register agent** — verify legal entities in free public registers (load `registers.md` for the relevant region)
2. **Reviews + community agent** — multi-platform review counts, verbatim quotes, lawsuit/breach/layoff search (load `reviews-platforms.md`)
3. **Competitor-validation agent** — verify every named competitor's funding/founding/pricing from ≥2 sources. **For `--type=competitive|due-diligence|investment` MUST load `competitor-verification.md`** and run the four-class verification protocol on every Tier B/C/D peer row: (a) lead-investor identity ≥3 sources with named-partner attribution preferred, (b) HQ city per press release dateline, (c) round structure per primary financial press (Bloomberg/TC) when bundled-announced, (d) numeric-figure attribution drift — confirm cited number is in cited source.

### Step 4 — Draft

Write to `--output` path in the 23-section structure (or comparison-mode 15-section if `--compare=` set; load `comparison-mode.md`).

**Load core voice/style/playbook files:**
- `voice-and-style.md` for voice/tone rules (single source of truth; declarative; no editorial trail) + mermaid portrait-printable rules
- `citations.md` for citation-style rules; apply per `--citations=<style>`
- `playbook-personas.md` for §0 Strategic Response Playbook content (12 personas, audience-mapped)

**Load stage / vertical / focused-audit overrides:**
- `stage-templates.md` (if `--stage=` set or auto-detected) — applies stage-specific section emphasis
- `vertical-templates.md` (if `--vertical=` set or auto-detected) — applies vertical-specific compliance / integrations / regulators / review platforms
- `audits.md` (if `--audit=` set) — adds focused subsections (pricing / tech-stack / customer-concentration / ai-maturity)
- `benchmarks.md` (if `--benchmark` set or `--stage=series-b+`) — adds §X Industry Benchmarks comparing to Bessemer / OpenView / KeyBanc / ICONIQ medians
- `risk-scan.md` — adds §16.X Red-Flag Scan from Step 2 findings (8 patterns)
- `data-sources-extended.md` (if `--data-sources=` set or auto-activated) — incorporates SEC EDGAR, Wayback, GitHub, LinkedIn hiring, USPTO, PACER findings into relevant sections

**Source-backing rule (non-negotiable):** every claim that can be backed by a public source MUST have a citation. Numbers, names, dates, quotes, competitor stats, certifications, customer logos — all need a clickable URL trail. The only exceptions: analyst opinion (SWOT/Heat-Map/Playbook content, bucketed under §0 framework disclaimer) and explicit synthesis ("reading these together suggests..."). If you can't find a source for a claim, **drop the claim** rather than publish unsourced.

### Step 5 — Validate (URLs + mermaid + glossary-completeness + depersonalization)

**Mermaid validation (load `mermaid-validation.md`):** run static check (no deps) on every mermaid block. Optionally run dynamic mmdc render for higher confidence. Fail the export if any diagram violates portrait-printable rules.

**Glossary-completeness scan (load `voice-and-style.md` Glossary discipline section + `glossary-catalog.md` for canonical definitions):** scan the body for all-caps acronyms and known jargon terms; cross-check against §22 Glossary entries. Report any used-but-undefined terms.

**Signal-label scan (REQUIRED, every dossier; load `voice-and-style.md` Signal-label discipline section):** run the bare-dot scan. Any signal cell that is a colour dot with no word label is a **hard gate** — fix before ship. Also run the repetition check: a label appearing more than ~3× in a 15-row Scorecard means the labels are not differentiating, so re-read those rows and pick dimension-specific words. Reading the Signal column top-to-bottom in isolation must produce a coherent summary of the entity; if it reads as a run of identical words, the column is decorative and has failed.

```bash
# Hard gate: every signal cell needs a word label, not a bare dot
BARE=$(grep -nE '\|[[:space:]]*(🟢|🟡|🔴|⚪)[[:space:]]*\|' "$OUTPUT")
[ -n "$BARE" ] && { echo "❌ bare signal dots:"; echo "$BARE"; } || echo "✓ all signal cells labelled"
grep -oE '(🟢|🟡|🔴|⚪) [A-Z][A-Za-z/-]+' "$OUTPUT" | sort | uniq -c | sort -rn | awk '$1>3 {print "⚠️  over-used:", $0}'
```

**Depersonalization / leak scan (REQUIRED for `--type=competitive|due-diligence`; load `voice-and-style.md` Anti-leak section):** run the 12-category leak scan on the dossier. The scan must pass before ship — any HIT is a hard gate, not a soft warning. Common leaks in production runs: lens-qualified labels ("Outsider verdict"), skill-tool references ("/schedule cron", "the skill that produced this"), editorial trail markers ("in this revision"), and lens comparisons ("insider lens scored X"). Substitute the author's identity placeholders (`<firstname>` / `<lastname>` / `<userhandle>` / `<entity-domain>`) before running, so personal-name patterns hit if the author accidentally name-leaks. **Do not ship a competitive/DD dossier with any leak unresolved** — the dossier is supposed to read as a third-party external evaluation with no traceable provenance to its author.

**Two-pass workflow:**
1. **Pre-include from catalog (Step 4 / Draft):** when writing §22, scan the catalog (`glossary-catalog.md`) for every entry whose term appears in the body. Add those to §22 with the canonical definition (adapted to the entity where useful).
2. **Post-write scan (Step 5):** run the bash scan from `voice-and-style.md` Glossary discipline section. Any term flagged as "used in body, not in glossary" must be added — either from the catalog or hand-written.

**Add missing entries before shipping** — every term in the body must have a glossary entry. Common gap categories: framework terms (BLUF, SWOT, Heat Map, Scorecard, Watchlist), funding rounds (Seed, Series A/B/C), business-register codes (FN, HRB, ICO, KvK, CVR, RUC, etc.), compliance (FedRAMP, PCI DSS, Schrems II), entity-specific products (placeholder names), and modern AI terminology (agentic, MCP Server, AI agent).

**Target: 40+ glossary entries on `--depth=deep` dossiers.** Production runs typically reach 55–75 entries; the canonical catalog has 240+ pre-defined entries spanning all common categories.

**URL validation (unless `--no-validate-urls`):**
```bash
# Extract the dossier's URLs, then check each one resolves
grep -oE 'https://[][:alnum:]._/?=#&%+:~@-]+' "$OUTPUT" | sed 's/[.,;)"]*$//' | sort -u > /tmp/urls.txt
while read -r url; do
  code=$(curl -s -o /dev/null -w "%{http_code}" -L --max-time 15 \
    -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36" \
    "$url" 2>/dev/null); echo "$code $url"
done < /tmp/urls.txt | sort -n > /tmp/url_check.txt
```

- HTTP 200 → keep
- HTTP 404 → fix or remove
- HTTP 301/302 → update to final
- HTTP 403/999/000 → bot-blocks on valid URLs (LinkedIn, Crunchbase, BusinessWire, Cloudflare-protected); verify visually with WebFetch

### Step 6 — Hallucination audit (unless `--no-hallucination-audit`)

Delegate to `Agent`:

> Read `<path>`. For every factual claim in §0–§1, verify it is supported by §2–§22. Flag any claim that is (a) new in §0 without body support, (b) a specific number without citation, (c) a competitor stat from a single analyst source not labeled, (d) a temporal claim ("first mainstream X", "earliest", "only") not verified across the market, (e) a founder-exit narrative not cross-checked, (f) an inferred date / metric, (g) **a competitor lead-investor identity not cross-validated against ≥3 sources OR not confirmed by named-partner attribution**, (h) **a competitor HQ city sourced from a single secondary outlet rather than a press release dateline**, (i) **a bundled-announcement funding figure ($Xm seed) without primary financial press breakdown of the seed-vs-Series-A structure**, (j) **a specific number cited to a specific article without confirming the number is actually in that article**, (k) **v2.6 — any T4-only-sourced claim (aggregator paraphrase without T1/T2 corroboration) per `source-hierarchy.md`**, (l) **v2.6 — any time-sensitive claim sourced to a current page without Wayback verification of the historical state**, (m) **v2.6 — any customer-logo cited in §9 without round-trip verification (no customer-side reciprocal evidence)**, (n) **v2.6 — any vendor-claimed customer count contradicted by triangulated ARR-proxy math (per `arr-triangulation.md`)**, (o) **v2.6 — any forward-looking claim with ICD 203 qualitative term but no Tetlock-compatible point probability**, (p) **v2.6 — any compliance claim (SOC 2 / ISO / HIPAA / FedRAMP) without auditor name + audit period + scope verification per `press-analysis.md` §3**, (q) **NEW v2.7 — pricing / headcount / customer / revenue / year value in one section that contradicts canonical value in another section without explicit reconciliation note (per `internal-consistency.md` §2)**, (r) **NEW v2.7 — any version reference (vX.Y) in body or closing footer that doesn't match the header / front-matter version**, (s) **NEW v2.7 — sample-audit headline "X% verified" that bundles partial-evidence items into the rate (must report fully-verified separately from light-evidence + pending)**, (t) **NEW v2.7 — two-decimal numeric precision on synthesized / inferred / estimated values when underlying analysis is text-pattern inference rather than measurement**, (u) **NEW v2.7 — a tier or label assignment that is at the more-generous end of the plausible range when no evidence supports the higher tier (e.g., press-release-republish outlet labeled as "earned" T2)**, (v) **NEW v2.7 — methods labeled "triangulation" that share >50% of their underlying assumption stack (must relabel as "multi-method estimation" or "plausibility-range bounds")**, (w) **NEW v2.7 — status-quo persistence forecast (rebrand sticks / exec stays / customer logo remains) at probability materially below the base-rate prior without specific contrary evidence**, (x) **NEW v2.7 — single composite confidence score for a dossier with single-source / vendor-claimed / aggregator-derived headline metrics (must split into epistemic-discipline + headline-fact-confidence two-dimension framing)**, (y) **NEW v2.9 — `**N <label>**` paired with parenthesized name list where the count does not match the number of names listed (per `internal-consistency.md` §10 — within-section count-vs-enumeration mismatch)**, (z) **NEW v2.9 — deprecated terminology surviving a mid-revision rename (e.g., "triangulated" / "triangulating" remaining after a "triangulation" → "multi-method estimation" rename); sweep ALL inflections of the deprecated term per `internal-consistency.md` §11**, (aa) **NEW v2.9 — adjacent paragraphs sharing the same lead-in marker (`**Note:**`, `**Important:**`, etc.) within 3 lines that contain overlapping content from iterative re-edits (per `internal-consistency.md` §12)**, (bb) **NEW v2.11 — founder identity inferred from press-release quote attribution rather than entity's own /about / /leadership / /team page (per `internal-consistency.md` §13 technique #61)**, (cc) **NEW v2.11 — T3 aggregator citation with publication date >12 months old in fast-moving category cited as if current; freshness sweep against entity's most recent milestone announcement was not run (per `internal-consistency.md` §14 technique #62)**, (dd) **NEW v2.11 — headcount-velocity claim about a portfolio company / subsidiary that doesn't acknowledge parent-network resources disclosed on the same source page (per `internal-consistency.md` §15 technique #63)**, (ee) **NEW v2.11 — `--type=competitive` dossier without comprehensive `<entity-domain>/comparison/` directory probe AND without `<entity-domain>/comparison/<user-employer>-vs-<entity>/` probe when user-employer-domain is known (per `internal-consistency.md` §16 technique #64)**, (ff) **NEW v2.11 — "not publicly disclosed" / "exact <X> private" / "publicly unavailable" claim without verification ladder (legal firms / PrivSource / Pitchbook / regulatory filings checked before publishing) (per `internal-consistency.md` §17 technique #65)**, (gg) **NEW v2.11 — single-feature observation extrapolated to category-level claim (e.g., "X has only basic AI") without enumerating entity's full feature surface AND parent / sibling-portfolio context (per `internal-consistency.md` §18 technique #66)**, (hh) **NEW v2.11 — negation claim ("no X") without specifying surface where absence was observed + snapshot date + strings searched (per `internal-consistency.md` §19 technique #67)**, (ii) **NEW v2.11 — quasi-deterministic verb usage ("categorically beyond" / "cannot trivially" / "will never" / "must / always / impossible / guaranteed") without Tetlock probability + resolution criterion (per `internal-consistency.md` §20 technique #68)**, (jj) **NEW v2.11 — competitor pricing in §8 or §10 without inline link to competitor's own /pricing page or Wayback snapshot (per `internal-consistency.md` §21 technique #69)**, (kk) **NEW v2.11 — Step 6 hallucination audit must include fresh-fetch sample of ≥3 cited URLs (not just citation-existence check); audit shares writer's blindspots and must explicitly probe for source-coverage gaps (per `internal-consistency.md` §22 technique #70)**, (ll) **NEW v2.11 — claim repeated across 3+ sections of dossier without ≥2 independent underlying sources (amplification illusion — repetition ≠ corroboration) (per `internal-consistency.md` §23 technique #71)**, (mm) **NEW v2.11 — vendor-claimed metric with suspicious precision (96.4%) or round magnitude (40,000+) without "methodology not disclosed" label (per `internal-consistency.md` §24 technique #72)**, (nn) **NEW v2.12 — win-rate claim without denominator (N) and source citation (per `win-loss.md` technique #73)**, (oo) **NEW v2.12 — NRR claim using non-Bessemer terminology ("strong NRR" instead of "Better tier per Bessemer 100/110/120"), or NRR/CAC/LTV/Payback as point estimates rather than multi-method bands (per `saas-economics.md` techniques #74, #75)**, (pp) **NEW v2.12 — Helmer 7-Powers scores aggregated into a single composite "moat score" (per `moat-scoring.md` technique #76 — powers don't sum)**, (qq) **NEW v2.12 — Switching Cost / Network Economies / Counter-Positioning / Process Power scored 2+ without specific friction mechanism / degree-N evidence / incumbent-paralysis evidence / 5+ year continuous-improvement evidence (per `moat-scoring.md` techniques #77, #78, #85, #86)**, (rr) **NEW v2.12 — patent filing presented as "<entity> is shipping X" without 12-36mo lag + 40-60% abandonment-rate caveat (per `roadmap-inference.md` technique #79)**, (ss) **NEW v2.12 — job-posting count → roadmap inference without 3-9mo time-horizon caveat (per `roadmap-inference.md` technique #80)**, (tt) **NEW v2.12 — conference-talk topic or GitHub-commit pattern presented as future-feature commitment (per `roadmap-inference.md` techniques #81, #82)**, (uu) **NEW v2.12 — single-channel roadmap inference; "Medium" confidence requires ≥2 channels, "High" ≥3 channels (per `roadmap-inference.md` technique #87)**, (vv) **NEW v2.12 — counter-evidence ignored (e.g., "5 ML engineers / 0 ML features over 24mo" presented as ML signal — actually LOW signal per technique #88)**, (ww) **NEW v2.12 — win-driver claim from <3 corroborating reviews (anecdote ≠ pattern; per `win-loss.md` technique #83)**, (xx) **NEW v2.12 — review-quote paraphrased rather than verbatim with attribution (paraphrase = synthesis = loss of source-discipline; per `win-loss.md` technique #89)**, (yy) **NEW v2.12 — cohort benchmark cited as "industry standard" without naming Bessemer / OpenView / KeyBanc / ICONIQ / Pavilion explicitly (per `saas-economics.md` technique #84)**. Return ✅/⚠️/❌ feedback under 500 words.

**Special focus: temporal claims** — when entity claims "first mainstream X to ship Y", verify by searching Y across top 5 competitors. See `lessons.md` for examples.

**Special focus: competitor-row error classes (g, h, i, j)** — these are the 4 highest-frequency post-publication corrections in production runs. Load `competitor-verification.md` for the full pre-publication checklist; the audit step verifies the checklist was applied.

Apply fixes. Repeat if critical items remain.

### Step 7 — Export (load `exports.md` + `output-formats.md` + `output-publish.md`)

If `--export=html|pdf|both` (or in convert-only mode), follow the export pipeline in `exports.md`. Pre-flight checks for `xelatex` / `mermaid-filter` / Chrome; fall back to HTML-only if PDF deps missing.

If `--export=` includes `exec`, `battle-card`, `vc-memo`, or `json` — load `output-formats.md` and produce the alternate condensed/repurposed views from the canonical MD.

If `--publish=notion|confluence|gdocs|coda` is set — load `output-publish.md` and push to the platform via API. Surface the destination URL.

If `--mcp-serve` is set — load `mcp-server.md` and start the self-MCP server exposing the user's dossier library.

### Step 8 — Report + Confidence Scoring + Freshness

**Load `confidence-scoring.md` to write §23 Appendix — Confidence & Methodology** (unless `--no-confidence-score`).

**Load `stale-detection.md` to add §23.X Freshness Decay** (always when prior dossier exists; in convert-only mode this is the primary §23 output). Computes per-source decay using TTL-by-source-type, decays composite confidence, and recommends soft / hard / none refresh. Optionally suggests `/schedule` cron for auto-refresh.

The §23 section produces a 6-dimension confidence score with date-stamp, methodology version, "what this does NOT mean" disclaimer, comparison-band table, and improvement table. The composite score reflects the active model + effort + validation level:

| Configuration | Typical composite (well-executed dossier) |
|---|---:|
| Opus 4.7 + max effort + `--validation=max` + `--depth=deep` | 85–92 |
| Opus 4.7 + max effort + `--validation=standard` + `--depth=standard` | 78–88 |
| Sonnet 4.6 + standard effort + `--validation=standard` | 70–82 |
| Lower model OR lower effort OR `--validation=light` | 55–75 |
| `--no-cross-validation` + `--no-hallucination-audit` | 40–60 |

Print to user:
- Output paths (MD, HTML, PDF)
- Line count, sections, mermaid count, table count
- URL validation summary (`X × 200, Y × 403 bot-protected, 0 × 404`)
- Mermaid validation summary
- Cross-validation summary (X facts dual-sourced, Y single-source-flagged)
- Hallucination audit summary (audit pass rate %)
- **Composite confidence score from §23** (e.g., "Confidence: 87/100 as of 2026-04-27")
- Active model + effort (so user understands the baseline)
- Any residual warnings

## Quality checklist (before ship)

**Source-backing (apply regardless of `--citations` style):**
- [ ] Every numeric fact (dates, dollar amounts, counts, %) has a citation
- [ ] Every proper noun used as a fact (company, person, product) has a citation
- [ ] Every quoted statement has attribution + citation
- [ ] Every competitor / customer / investor name links to a canonical URL
- [ ] Every certification / compliance / regulatory claim has a citation
- [ ] If `--citations=footnotes|endnotes`: same source = same tag (deduplication working); all `[^tag]` references have matching `[^tag]: ...` definitions; no orphan footnotes

**Voice & format:**
- [ ] §0 BLUF reads as a single declarative paragraph (no "we corrected this")
- [ ] §0 Scorecard: every row has source + signal column
- [ ] **Every signal cell is `<dot> <Label>`, never a bare dot** — §0 Scorecard, Heat Map, §16 Red-Flag Scan, negative-space scan, benchmarks, freshness decay. Labels are dimension-specific, 1–2 words, ≤14 chars, and consistent with the Assessment cell; `⚪ N/A` used where a dimension genuinely does not apply (per `voice-and-style.md` signal-label discipline). Reading the Signal column alone must yield a coherent summary
- [ ] All 23 sections (§0–§22) present and numbered
- [ ] Every datapoint in §0–§2: dual-sourced OR labeled `single-source` / `vendor-claimed` / `founder-self-reported` / `aggregator-derived`
- [ ] §3.4 Related Entities mermaid distinguishes founded / employed / contracted
- [ ] All mermaid diagrams pass `mermaid-validation.md` static check (and optional dynamic check)
- [ ] §11 includes ≥10 review platforms; Reddit/HN absence flagged; verbatim negative + positive quotes with dates; lawsuit/breach/layoff search result
- [ ] §16 includes a Data Verifiability subsection
- [ ] No "first mainstream X" claim without market-wide verification
- [ ] Founder exit narratives cross-checked against Wikipedia + acquirer press
- [ ] No promotional language in analytical voice
- [ ] No editorial trail markers in final document

**Validation:**
- [ ] URL validation: 0 × 404
- [ ] Hallucination audit run; flagged items addressed
- [ ] Cross-validation pass run at the level set by `--validation` (subagents spawned, findings applied)
- [ ] **Glossary-completeness scan run; every acronym + jargon term used in body has a §22 entry** (no orphaned acronyms; per `voice-and-style.md` Glossary discipline section). Catalog (`glossary-catalog.md`) consulted for canonical definitions. **Target: ≥40 entries on `--depth=deep` dossiers.**
- [ ] **Depersonalization / leak scan run for `--type=competitive\|due-diligence`**; ALL 12 categories clean (per `voice-and-style.md` Anti-leak section). Common leaks: lens-qualified labels (Outsider/Insider), skill-tool refs (/research-entity, /schedule), editorial trail (in this revision), lens comparisons (insider score). Hard gate before ship.
- [ ] **Competitive dossier voice rules applied** for `--type=competitive\|due-diligence`: neutral verdict labels (Verdict / Observation / Conclusion — NOT Outsider Verdict / Outsider Observation), no lens comparisons, no skill self-references, no editorial trail
- [ ] **External Verification Penalty (-5)** applied to §23 composite for `--type=competitive\|due-diligence` (per `confidence-scoring.md`); composite caps in 70–82 band rather than 80–92
- [ ] If `--export=html|pdf|both`: mermaid validation passed, file generated, file opens cleanly
- [ ] §23 Confidence & Methodology written (unless `--no-confidence-score`); per-dimension breakdown + disclaimer + comparison band present
- [ ] Model + effort warning shown at Step 1 if config below recommended (or `--no-model-warning` was set)

## Usage examples

**Full research mode (with wizard auto-triggered for the first one):**
```
/research-entity "Stripe"                                                     # → wizard asks for type/depth/audience/export/citations/stage/vertical/audits/benchmarks
/research-entity "Acme Corp" --type=due-diligence --audience=investor --depth=deep --export=both --citations=footnotes
/research-entity "Example Co" --type=competitive --audience=operator --depth=deep
/research-entity "<our-own-company>" --type=research --depth=deep
/research-entity "Acme Corp" --no-wizard                                      # uses all defaults silently
```

**Stage + vertical templates:**
```
/research-entity "Healthtech Co" --vertical=healthcare --stage=series-b
/research-entity "DeepTech Inc" --vertical=deeptech --data-sources=uspto,sec --depth=deep
/research-entity "DevTool X" --vertical=devtools --data-sources=github,linkedin --audit=tech-stack
/research-entity "Public SaaS Y" --stage=public --benchmark --data-sources=sec
```

**Comparison / diff mode:**
```
/research-entity --compare=./<entity-A>-research.md,./<entity-B>-research.md
/research-entity "Acme Corp" --year-over-year                                 # auto-finds prior dossier, generates delta
```

**Focused audits:**
```
/research-entity "Acme Corp" --audit=pricing                                  # adds §8.X Pricing Audit subsection
/research-entity "Acme Corp" --audit=ai-maturity                              # adds §7.X AI Maturity Audit
/research-entity "Acme Corp" --audit=pricing,tech-stack,customer-concentration,ai-maturity --depth=deep
```

**Industry benchmarks:**
```
/research-entity "Stripe" --benchmark                                         # auto-cohort by stage
/research-entity "Acme Corp" --benchmark=ai-native --stage=series-b
```

**Alternate output formats:**
```
/research-entity "Acme Corp" --export=md,html,exec                            # full + HTML + 1-page summary
/research-entity "Acme Corp" --export=battle-card                             # sales battle card
/research-entity "Acme Corp" --export=vc-memo --depth=deep --validation=max   # VC investment memo
/research-entity "Acme Corp" --export=json                                    # structured data dump
```

**Direct publish to collaboration platforms:**
```
/research-entity "Acme Corp" --export=md --publish=notion                     # requires NOTION_TOKEN env var
/research-entity "Acme Corp" --export=md,html --publish=confluence            # requires CONFLUENCE_TOKEN + URL + SPACE
/research-entity "Acme Corp" --publish=gdocs                                  # requires GOOGLE_SERVICE_ACCOUNT_JSON
```

**Skill self-MCP server (expose dossier library to future Claude sessions):**
```
/research-entity --mcp-serve                                                  # starts local MCP server
```

**Convert-only mode (existing MD → HTML / PDF):**
```
/research-entity ./<entity>-research.md --export=html
/research-entity ./<entity>-research.md --export=pdf
/research-entity ./<entity>-research.md --export=both
/research-entity --convert=./path/to/dossier.md --export=html
/research-entity ./<entity>-research.md --export=html --no-revalidate-urls
```

## Anti-patterns — see `lessons.md` for the canonical list

Most-cited:
- ❌ Treat aggregator data as fact without cross-validation
- ❌ Repeat misframed founder-exit narratives
- ❌ Claim "first mainstream X" without market-wide verification
- ❌ Use side-by-side mermaid subgraphs (always portrait, vertical chain)
- ❌ Use `**bold**` inside mermaid nodes (use `<b>...</b>`)
- ❌ Use paid business registers when free covers the case
- ❌ Leave editorial trail in final document
- ❌ Skip mermaid validation before export

## Notes

- This skill has been refined across multiple real-world vendor-research dossiers.
- Expected runtime on `--depth=standard`: 20–35 minutes.
- Expected runtime on `--depth=deep`: 45–75 minutes (with 2–3 parallel cross-validation subagents).
- Convert-only mode: <2 minutes (mermaid + URL re-check + export).
- Expected output size on `--depth=deep`: 1500–1800 lines, 150+ cited URLs, 9–10 mermaid diagrams.
- HTML export renders perfectly in any modern browser and prints to PDF via the browser's native print dialog with `Save as PDF` — use this when xelatex/mermaid-filter aren't installed.
- For self-research case (user's email matches entity domain), default to `--type=research` and save a project-memory note about the affiliation.
