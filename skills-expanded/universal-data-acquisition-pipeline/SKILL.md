---
name: universal-data-acquisition-pipeline
description: Trigger when the user wants to collect, structure, evaluate, crawl, extract, refresh, or build reusable data acquisition pipelines from websites, APIs, portals, files, or rendered apps. Use for dataset design, source classification, feasibility, endpoint discovery, authorized/owned-session scraping plans, Patchright warm-session cookie generation, Playwright fallback, source probing, pagination analysis, scraper/pipeline architecture, sample validation, refresh design, and output contracts. Do not trigger for ordinary browsing, exploitative access, credential theft, CAPTCHA solving, auth bypass, rate-limit bypass, or non-data tasks.
---

# Universal Data Acquisition Pipeline

Act as the router for a data acquisition skill tree. Classify the request, select the narrowest child skill, and keep outputs aligned with shared core contracts. Design robust, refreshable scraping and API pipelines that are honest about source access, reliability, compliance, cost, and data quality.

Do not scrape immediately. First classify the source access, prove that a reliable data path exists, design a reusable pipeline, validate a small sample, and require approval before any full run.

For feasibility requests, do not stop at desk research when public probing is possible. Run a bounded pre-report probe ladder first, then generate the feasibility report from the observed evidence. Treat the probes as due diligence, not execution: 1 to 3 URLs, 20 rows maximum, no account pages, no CAPTCHA solving, no rate-limit bypass, and no broad collection.

## Skill Tree

Use the child skill that best matches the request:

- `data-acquisition-core`: shared contracts, access classes, compliance, scorecards, output schemas, and pipeline quality standards.
- `data-acquisition-design`: DatasetNeed, DatasetSpec, scope control, and "what data do we actually need?"
- `data-acquisition-feasibility`: feasibility scoring, source comparison, Green/Yellow/Red decisions, and approval gates.
- `data-acquisition-discovery`: endpoint discovery, public APIs, GraphQL, XHR/fetch, sitemaps, embedded JSON, and pagination probes.
- `data-acquisition-browser`: Patchright warm-session cookie/storage generation, browser network capture, Playwright rendered DOM fallback, and authorized owned-session probes.
- `data-acquisition-pipeline`: production pipeline architecture, `pipeline.yaml`, raw/staged/normalized layers, quality gates, and run reports.
- `data-acquisition-publish`: probe-backed case studies and publishable/non-publishable result packaging.

## Modes

Select the narrowest useful mode from the user's request. Default to `dataset-design` when the user is still unsure what data they need, and `feasibility` when they already named a dataset.

1. `dataset-design`: clarify the decision, entity grain, required fields, freshness, history, coverage, joins, exclusions, and uselessness criteria before source discovery.
2. `feasibility`: decide whether the requested dataset is collectible enough to justify a pipeline.
3. `endpoint-discovery`: hunt APIs, XHR/fetch routes, page-data, feeds, sitemaps, and embedded JSON.
4. `pagination-limits`: prove page size, cursor/offset depth, terminal behavior, caps, sort stability, and completeness ceiling.
5. `source-comparison`: compare official API, public XAPI, sitemap plus detail, embedded JSON, HTML, rendered DOM, and reject paths.
6. `pipeline-design`: convert known sources into a refreshable pipeline plan without broad collection.
7. `sample-validation`: run tiny probes and validate rows, fields, parsing, and diagnostics.
8. `compliance-boundary`: identify Green/Yellow/Red boundaries, stop conditions, and safer alternatives.
9. `owned-session`: use a user-provided, user-owned authenticated browser/session only for data the user is authorized to access; mark outputs non-public.
10. `execution`: collect only after explicit approval, with checkpoints, limits, validation, and incremental outputs.

## Core Workflow

Every request must move through:

1. `ModeSelection`
2. `SourceAccessClass`
3. `DatasetNeed`
4. `DatasetSpec`
5. `SourcePlan`
6. `EndpointPlan`
7. `HeaderProfile`
8. `ProbeResults`
9. `FeasibilityScorecard`
10. `DataAcquisitionMemo`
11. `FeasibilityReport`
12. `PipelineQualityPlan`
13. `PipelinePlan`
14. `SampleRows`
15. `ApprovalGate`

Never return raw code alone. The user wants a decision and an engineering design: what access class applies, whether the data is collectible, how complete it can be, the cheapest reliable path, the trapdoors, the quality gates, and the repeatable pipeline design.

## Autonomous Feasibility Probe Ladder

When mode is `feasibility`, `source-comparison`, `pagination-limits`, or `sample-validation`, run the narrowest safe probes before writing the report unless the user explicitly says "report only" or "do not browse/probe".

Default sequence:

1. `Source boundary`: fetch or inspect robots/sitemaps/public docs when available; identify disallowed, auth-only, and reject paths.
2. `Cold structured probe`: try ordinary unauthenticated HTTP against one public seed URL and obvious public metadata files only; record status, redirects, schemas, and block pages.
3. `Static/embedded probe`: inspect HTML for JSON-LD, canonical links, meta tags, embedded state, product/listing cards, and pagination clues.
4. `Browser fallback`: if cold probes are blocked or incomplete and the data is visible in a normal browser, run a tiny browser probe using the `data-acquisition-browser` helper.
5. `Patchright visible fallback`: if headless browser probing is blocked but a normal visible browser context is acceptable, run Patchright non-headless with a persistent local profile for 1 URL. Mark the source as `owned_session`/`non_public_authorized_result` if the pipeline depends on that local browser state.
6. `Page-only option`: if the user asks for no API usage, use page-load DOM extraction only; do not discover, replay, or recommend API endpoints for execution.
7. `Stop`: stop and score Red when progress would require CAPTCHA solving, fingerprint evasion, auth bypass, private data, or rate-limit bypass.

The feasibility report must say which ladder steps were attempted, which succeeded, and which were intentionally not attempted.

## Reference Map

Load only the shared core references needed for the request from `skills/data-acquisition-core/references/`, or delegate mentally to the matching child skill:

- Overall process: `skills/data-acquisition-core/references/workflow.md`
- Mode selection: `skills/data-acquisition-core/references/modes.md`
- Source access and owned-session rules: `skills/data-acquisition-core/references/source-access.md`
- API/source discovery patterns: `skills/data-acquisition-core/references/pattern-library.md`
- Endpoint discovery: `skills/data-acquisition-core/references/endpoint-discovery.md`
- Probing and pagination: `skills/data-acquisition-core/references/probing.md`
- Playwright/rendered DOM: `skills/data-acquisition-core/references/playwright-rendered-dom.md`
- Warm sessions and execution adapters: `skills/data-acquisition-core/references/execution-adapters.md`
- Pipeline engineering: `skills/data-acquisition-core/references/pipeline-engineering.md`
- Feasibility scoring: `skills/data-acquisition-core/references/feasibility-scoring.md`
- Compliance: `skills/data-acquisition-core/references/compliance-boundaries.md`
- Source strategies: `skills/data-acquisition-core/references/source-strategies.md`
- Output contracts: `skills/data-acquisition-core/references/output-contracts.md`
- Examples: `skills/data-acquisition-core/references/examples.md`

## Default Posture

- Prefer structured endpoints over HTML parsing when allowed by the source access class.
- Prefer endpoint templates, pagination params, and stable IDs over browser automation.
- Use Playwright/rendered DOM only after public APIs, feeds, sitemaps, embedded JSON, and static HTML fail or are insufficient.
- If a site blocks cold/headless access but works in Patchright non-headless, treat the route as feasible only for a visible-browser/page-load pipeline and lower stability/runtime/compliance scores accordingly.
- If the user explicitly wants page loads only, skip API replay and endpoint harvesting; extract from rendered DOM, JSON-LD, meta tags, canonical links, and visible product/listing nodes.
- Treat every ask as due diligence before implementation: answer "should we do this?" before "how do we code it?"
- Treat vague "all data" requests as dataset-design problems before source discovery.
- Use normal browser-style headers only when needed for public unauthenticated responses.
- When a public page mints request context for public XHR/API calls, use Warm Session Capture: run the Patchright helper to generate user-owned local cookies/storage state and capture observed non-secret request templates, then replay tiny probes in that same authorized browser context.
- Detect rate limits and design within them using backoff, caching, checkpointing, sampling, and approval gates. Do not bypass rate limits or access controls.
- If cookies, credentials, or auth are involved, switch to `owned-session` or `licensed_api`, mark outputs non-public, avoid storing secrets, and require explicit approval.
- Stop escalation when a path requires auth bypass, credential extraction, CAPTCHA solving, fingerprint evasion, private third-party access, or rate-limit bypass.
- Before full execution, validate a small sample and present a clear approval gate.

## Output Contract

Always produce these sections unless the user explicitly asks for a narrower artifact:

- `DatasetSpec`
- `SourceAccessClass`
- `DatasetNeed`
- `SourcePlan`
- `EndpointPlan`
- `HeaderProfile`
- `ProbeResults`
- `FeasibilityScorecard`
- `DataAcquisitionMemo`
- `FeasibilityReport`
- `PipelineQualityPlan`
- `PipelinePlan`
- `SampleRows`
- `ApprovalGate`

For implementation tasks, generated pipeline artifacts should include `pipeline.yaml`, `report.json`, sample output, logs/diagnostics, and runnable collection logic appropriate to the repo and user environment.
