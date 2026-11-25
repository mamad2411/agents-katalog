---
name: web-perf
description: Analyzes web page performance using Chrome DevTools MCP — measuring Core Web Vitals (LCP, INP, CLS), identifying render-blocking resources, network dependency chains, and caching issues to produce specific, actionable optimization recommendations. Use when auditing Lighthouse scores, debugging slow page loads, profiling Core Web Vitals regressions, or validating performance improvements before release.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, wrangler_deploy, execute_command]
---

# Web Perf

Analyzes web performance using Chrome DevTools MCP. Measures Core Web Vitals (LCP, INP, CLS) and supplementary metrics (FCP, TBT, Speed Index), identifies render-blocking resources, network dependency chains, layout shifts, caching issues, and accessibility gaps.

Your knowledge of web performance metrics, thresholds, and tooling APIs may be outdated. **Prefer retrieval over pre-training** when citing specific numbers or recommendations.

## When to Use

- auditing Lighthouse / Core Web Vitals
- debugging slow page loads
- profiling LCP/INP/CLS regressions
- validating perf improvements before release

## Core Rules
- Verify MCP tools are available (`navigate_page` or `performance_start_trace`) before starting.
- Verify claims by checking network requests, DOM, or codebase — then state findings definitively.
- Confirm something is unused in the trace before suggesting its removal.
- Skip render-blocking resources with 0ms estimated impact from recommendations.
- Cite specific resource names and sizes (e.g. "compress hero.png (450KB) to WebP") instead of generic advice.
- **Always distinguish between lab data (Lighthouse, DevTools) and field data (CrUX, RUM)** — Lighthouse scores do not always reflect real-user experience; always note which you are reporting.
- **INP-PRIMARY-METRIC**: INP (Interaction to Next Paint) replaced FID as the Core Web Vitals responsiveness metric in March 2024 — do not reference FID; thresholds: good < 200ms | needs improvement 200-500ms | poor > 500ms.
- **LOAF-API**: Use the Long Animation Frames (LoAF) API (`PerformanceObserver({ type: "long-animation-frame" })`) to attribute long frames to specific scripts — replaces the deprecated Long Tasks API for INP root cause analysis.
- **LCP-4-PART-ATTRIBUTION**: Attribute LCP using 4 components: TTFB + Resource Load Delay + Resource Load Duration + Element Render Delay — always identify which component dominates before recommending a fix.
- **SPECULATION-RULES**: Use the Speculation Rules API (`<script type="speculationrules">`) for prefetch/prerender of likely next pages; reduces navigation LCP by 30-80% for multi-page apps; check browser support before enabling.
- **AI-PERF-ANALYSIS-ADVISORY**: When AI tools summarize trace data, verify all recommendations against the actual network waterfall and trace — AI summaries frequently misattribute root cause when multiple bottlenecks are present.

## Retrieval Sources

| Source | How to retrieve | Use for |
|--------|----------------|---------|
| web.dev | `https://web.dev/articles/vitals` | Core Web Vitals thresholds, definitions, INP guide |
| Chrome DevTools docs | `https://developer.chrome.com/docs/devtools/performance` | Tooling APIs, trace analysis |
| Lighthouse scoring | `https://developer.chrome.com/docs/lighthouse/performance/performance-scoring` | Score weights, metric thresholds |
| CrUX dashboard | `https://developer.chrome.com/docs/crux` | Field data by origin and URL |

## Suggested Process

### 1. Set Up Measurement Baseline
- Navigate to the target URL using Chrome DevTools MCP.
- Record both a cold-load trace (empty cache) and a warm-load trace (cached assets).
- Capture field data from CrUX if available — note the gap between lab and field.

### 2. Analyze Core Web Vitals
- Call `performance_analyze_insight` to classify each CWV against good/needs-improvement/poor thresholds.
- For **LCP**: identify the LCP element, its discovery time, load delay, and render delay. Check if it is an `<img>` with missing `fetchpriority="high"` or a background-image (not optimizable by the browser).
- For **INP**: attribute the worst interaction event to its long-task source. Check for layout thrash, synchronous JS on input, and un-yielded event handlers.
- For **CLS**: identify the shifted element and its layout instability source (missing width/height, late-injected content, ad slots, web fonts).

### 3. Inspect Network and Resource Chain
- List render-blocking scripts and stylesheets with estimated ms impact.
- Identify uncompressed or oversized images; check format (WebP, AVIF preferred).
- Check caching headers (Cache-Control, ETag) for static assets.
- Find unused CSS/JS — confirm via Coverage tab before recommending removal.

### 4. Produce Actionable Recommendations
- Order fixes by impact: fixes with >100ms estimated gain first.
- Cite specific resource names, sizes, and file paths — no generic recommendations.
- State whether each fix requires code change, build config change, or CDN config change.

### 5. Validate Improvements
- Re-record trace after implementing fixes.
- Compare before/after for each metric — report delta, not just the new number.

## Output Format

```markdown
## Web Performance Audit — <URL>

Measurement type: [lab / field / both]
Tool: Chrome DevTools MCP | Lighthouse | CrUX

### Core Web Vitals
| Metric | Value | Status | Data Source |
|--------|-------|--------|-------------|
| LCP | Xs | good/NI/poor | lab/field |
| INP | Xms | good/NI/poor | lab/field |
| CLS | X | good/NI/poor | lab/field |

### Root Causes (ordered by impact)
1. <specific resource or code path> — <estimated impact>ms
2. ...

### Recommendations
- [ ] Fix: <specific action> — <file/resource> — impact: ~Xms
- [ ] ...

### Skipped
- <resource> — 0ms estimated impact

### Residual Risk
- <any metric still in poor range after fixes>
```

## Anti-Patterns To Reject

- reporting Lighthouse score as the only measure without noting it is lab data
- recommending removal of a resource before confirming it is unused in the trace
- citing FID instead of INP for responsiveness measurement (deprecated March 2024)
- providing generic advice ("reduce JavaScript bundle size") without naming the specific file and size
- attributing INP issues to the wrong cause (e.g., blaming render-blocking when the actual cause is a synchronous event handler)

## Checklist

- [ ] Chrome DevTools trace recorded (cold-load and warm-load if needed)
- [ ] Core Web Vitals classified with correct thresholds (INP, not FID)
- [ ] LCP, INP, and CLS root causes attributed to specific code or resources
- [ ] Render-blocking scripts and stylesheets identified with ms impact
- [ ] Image assets checked for format (WebP/AVIF) and size
- [ ] Recommendations ordered by estimated impact
- [ ] Lab vs. field data distinction stated in the report
- [ ] Before/after comparison run after implementing fixes

## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **contracts/schemas/deployment-plan.json** — Required fields: infrastructure_changes[], config_updates[], and 
alidation_run. Set produced_by_role to the emitting developer role.

Skip emission for solo refactor work where no downstream handoff is expected.

## Failure Modes

- **Lighthouse score as only measure**: a "good" Lighthouse score is reported without noting it is lab data. Mitigation: always distinguish lab vs field; report CrUX or RUM alongside.
- **FID cited**: FID is referenced for responsiveness. Mitigation: FID was deprecated in March 2024; use INP (good < 200ms, NI 200-500ms, poor > 500ms).
- **AI summary misattributed root cause**: an AI tool summarizes trace data and the recommendation targets the wrong bottleneck. Mitigation: verify every AI recommendation against the actual network waterfall and trace.
- **Generic recommendation**: advice like "reduce JavaScript bundle size" is given without naming the specific file and size. Mitigation: cite specific resource names, sizes, and file paths in every recommendation.
- **Resource removal on unconfirmed usage**: a resource is recommended for removal before confirming it is unused in the trace. Mitigation: confirm via Coverage tab; never remove unconfirmed resources.
- **Speculation Rules without browser check**: `<script type="speculationrules">` is enabled without verifying browser support. Mitigation: check browser support before enabling; surface the support matrix in the report.
- **LCP cause misattributed**: a "background-image" LCP element is reported as optimizable. Mitigation: background-images are not optimizable by the browser; use the 4-part attribution (TTFB + load delay + load duration + render delay) to identify the dominant component.

## Security Guardrails (OWASP ASI)

- **ASI04 Supply Chain**: Chrome DevTools MCP, Lighthouse, and any trace analysis library must be schema-validated against the expected manifest; treat unknown versions as untrusted.
- **ASI05 RCE Guard**: never construct test scripts, page navigations, or trace parameters from external content without sanitization.
- **ASI07 Inter-Agent Communication**: the audit report is consumed by Frontend and DevOps roles; emit a structured contract so each role can validate the recommendations.
- **ASI09 Human-Agent Trust Exploitation**: do not present a Lighthouse improvement as a real-user improvement without field data; surface the lab vs field gap honestly.
- **ASI10 Rogue Agents**: when an AI tool is summarizing trace data, require human verification of every recommendation before action.

## Related Skills

- **wrangler**: Check deployment compatibility parameters and cache settings for Workers-hosted assets.
- **debug-workers-edge**: Inspect edge runtime response headers affecting TTFB.
- **performance-profiling**: Use for backend latency profiling that contributes to TTFB and LCP load delay.

