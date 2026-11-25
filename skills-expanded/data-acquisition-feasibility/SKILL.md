---
name: data-acquisition-feasibility
description: Use when the user wants to know whether a dataset/source is worth pursuing, compare routes, score feasibility, identify trapdoors, classify Green/Yellow/Red, or decide whether to stop, sample, narrow, license, use owned-session access, or build a pipeline.
---

# Data Acquisition Feasibility

Act as the feasibility analyst. Be direct about what works, what is partial, what requires authorization, and what should stop.

Default to evidence-backed feasibility. If a public source URL or target site can be safely probed, run a bounded probe ladder before writing the final score. Do not produce a purely speculative feasibility report unless probing is impossible, disallowed by the user, or blocked by compliance boundaries.

## Shared Core

Read from `../data-acquisition-core/references/`:

- `source-access.md`
- `feasibility-scoring.md`
- `source-strategies.md`
- `compliance-boundaries.md`
- `output-contracts.md`
- `workflow.md`

## Output

Return:

- `ModeSelection`
- `SourceAccessClass`
- `SourcePlan`
- `ProbeResults` when probes were run
- `FeasibilityScorecard`
- `DataAcquisitionMemo`
- `FeasibilityReport`
- `ApprovalGate`

Never approve full execution without explicit user approval.

## Required Pre-Report Probe Ladder

For public web datasets, attempt these steps in order and record the result in `ProbeResults`:

1. Public boundary check: robots/sitemaps/public docs or obvious terms/access boundaries.
2. Cold HTTP check: one public seed URL plus obvious sitemap/feed/metadata URLs where applicable.
3. Static page metadata check: status, final URL, title, canonical, meta description, JSON-LD, embedded app state, visible listing/product hints.
4. Browser check: use Playwright or Patchright for a tiny rendered sample if the data is user-visible but cold probes fail or omit the rows.
5. Patchright non-headless check: when headless returns a block page but a normal visible browser context may load the page, run one visible Patchright probe with a persistent local profile. Mark as `owned_session` if local cookies/storage are required.
6. Page-only check: when the user says no API, disable endpoint discovery/replay and extract only DOM/JSON-LD/meta/visible row data.

Bounds: 1 to 3 URLs, 20 rows maximum, 2 minutes per probe unless the user asks for more. No broad crawl before approval.

Stop and score Red when the next step would require CAPTCHA solving, fingerprint spoofing/evasion, auth bypass, private third-party data, or rate-limit bypass.

If a probe succeeds only in Patchright non-headless, classify the pipeline route as browser-context/page-load dependent. Lower stability and runtime scores, and call out that the route may not be publishable as a public unauthenticated pipeline.
