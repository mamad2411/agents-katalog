---
name: gtm-reverse-engineer
description: |
  Reverse-engineer any company's public go-to-market into an evidence-graded, multi-file playbook (copy / adapt / skip). Use whenever the user wants competitor GTM teardown, growth forensics, channel analysis (Instagram, X/Twitter, LinkedIn, ads, Reddit/community, SEO, jobs, pricing), "how did X grow", unicorn/breakout GTM playbook, modular GTM research, or to install a 90-day motion plan from public signals. Trigger even if they say "spy on their GTM", "tear down their acquisition", or name a single channel (ads only, X only, community only). Prefer this skill over ad-hoc web search when a structured pack or playbook is desired.
argument-hint: <company URL or name> [modules=full|quick|standard|ads,social_x|...] [depth=quick|standard|max]
version: 1.0.0
---

# GTM Reverse Engineer

General, **company-agnostic** skill. Nothing about a specific brand is hardcoded in runtime logic. The target company is always supplied by the user (or clarified before run).

## Defaults (override if user already chose otherwise)

| Setting | Default |
|---------|---------|
| Skill id | `gtm-reverse-engineer` |
| Output root | `./outputs/gtm-playbook-<slug>/` under current workspace |
| Depth | `standard` unless user says quick/max/full |
| Modules | user-selected; if user says "full" / "in-depth" / "everything" → all modules |
| Collectors | auto-detect (see below); never require Kimi or any browser bridge |
| Extra vs base research | **Channel Completeness Contracts** on every gather + scorecard |

If product choices are still ambiguous after reading the user message, ask before spending a large run. Do not invent the target company.

## When this skill triggers

- Competitor / company GTM, growth, acquisition, positioning teardown
- Single-channel asks: "only Instagram", "only X", "only ads", "only community"
- Full playbook / 90-day copy plan / what not to copy
- Modular or full-depth GTM research workflows

## Non-goals / honesty fence

- Not insider or "stolen secrets." Public and user-session-visible signals only.
- Not audited financials. Company-claimed ARR/users/valuation stay labeled.
- Not equal depth for every company. Thin public exhaust → thin pack + explicit coverage.
- Do not hardcode example companies as the run target. Examples in docs are illustrations only.

## Required inputs

1. **Target** (required): company name and/or website URL.
2. **Modules** (required unless full): list or preset (`full`, `quick`, or explicit module ids).
3. **Optional:** geo focus, B2B vs B2C emphasis, output directory, depth (`quick` | `standard` | `max`).

If target is missing or ambiguous (multiple entities share the name), **stop and disambiguate** (entity lock) before gather.

## Module catalog (v1)

Compose any subset. `full` enables all gather modules + analyze bundle + verify + playbook.

| Module id | Purpose |
|-----------|---------|
| `entity` | Company lock, founders/team surface, timeline anchors |
| `press_funding` | Press, launches, funding claims (graded) |
| `product_pricing` | Site, pricing, packaging, enterprise/affiliates pages |
| `jobs` | Careers/jobs as GTM org proxy |
| `social_x` | X/Twitter official + founders (archives/web first) |
| `social_linkedin` | LinkedIn company (+ founders if reachable) |
| `social_instagram` | Instagram official |
| `ads` | Meta/Google ad library and paid creative angles |
| `community` | Reddit/community sentiment and objections |
| `seo_distribution` | SEO content, PH, affiliates, distribution surfaces |
| `youtube_interviews` | Talks/interviews index + transcripts when available |
| `analyze` | Analysis suite (scoped to enabled evidence) |
| `verify` | Adversarial review + claim audit + confidence/gaps |
| `playbook` | Copyable playbook chapters (scoped) |

Presets (resolved by `scripts/init_run.py` into concrete module ids):

- `quick` → `entity`, `product_pricing`, `press_funding`, `analyze`, `verify`
- `standard` → all gather modules + `analyze`, `verify`, `playbook`
- `full` / `max` → same module set as standard; **depth** controls effort/browser willingness, not a different module list

**Scorecard is not a module.** After any gather, always run completeness rollup (phase), then optional analyze slices.

**Depth vs modules:** modules = what runs; depth = how hard (query volume, browser enrich only if confirmed).

Read `references/modules.md` for per-module outputs, done-when, and analyze scope.

## Pipeline (always) — load order

```
0. Parse args → resolve modules (init_run.py) → output paths
1. Detect collectors (detect_collectors.py) — browser_enrich_possible defaults false
2. Entity lock (serial; stop if ambiguous)
3. Gather enabled modules in parallel (each returns completeness_contract)
4. Orchestrator rollup COMPLETENESS-SCORECARD + RUN-CONFIG contracts
5. validate_run.py --phase post_gather  (block on FAIL)
6. Analyze (only dimensions supported by evidence)
7. Verify if enabled (claim audit + adversarial)
8. Playbook if enabled (only if module enabled)
9. validate_run.py --phase final; index + confidence map + gaps
```

For large multi-module runs, prefer Claude Code **Workflow** orchestration (`dynamic-workflow` patterns): `phase`, `parallel`, `pipeline`, structured `agent` returns. Pass **modules_resolved**, not preset strings. For single-module asks, inline agents are enough — Completeness Contracts remain mandatory.

## Collector auto-detect (never hardcode Kimi)

Run `scripts/detect_collectors.py` (or follow `references/collector-matrix.md`) at start of every run.

**Priority order for raw collection:**

1. **Always:** web search skill (if present), `curl`/HTTP fetch, public APIs/archives  
2. **If present:** YouTube transcript scripts/skills  
3. **If browser bridge available** (chrome-session-bridge / Capy browser bridge online): optional logged-in enrich for login-walled surfaces  
4. **If Kimi webbridge skill + daemon/extension available:** optional; **one session per agent**, max 2 tabs; never default bulk  
5. **If nothing beyond web:** proceed web-only; document limits in completeness contracts  

**Rules:**

- Detection must be runtime, not baked into module lists as "requires Kimi."
- If user is not logged in and wall blocks, set contract `blockers` to include `login_wall` and list `login_required_surfaces` — do not invent engagement.
- Never open mass tabs. Prefer one tab reused per browser agent.
- Omit browser tools from prompts when `browser_enrich_possible` is false.

## Channel Completeness Contracts (mandatory)

Every gather agent (including `entity` and single-module/inline runs) MUST emit a full canonical contract. Schema + enums: `references/completeness-contracts.md`.

All required keys: `module`, `channel`, `method` (`web`|`archive`|`browser`|`mixed`), `claimed_complete` (default **false**), `items_captured`, `date_span`, `sample_note`, `what_was_not_covered`, `grade_of_collection`, `login_required_surfaces`, `blockers`.

**Rollup:** orchestrator writes `00-meta/COMPLETENESS-SCORECARD.md` and `RUN-CONFIG.completeness_contracts` after gather. Missing contract for an enabled gather module = QA fail (`scripts/validate_run.py`).

Analyze/playbook must not imply full channel history/census when `claimed_complete` is false.

## Evidence grades

- **A** primary (official site/app, official social, filings, careers, primary founder post/transcript)
- **B** strong secondary with attribution
- **C** pattern from multiple weaker signals (list them)
- **D** single weak source — never playbook foundation
- **UNKNOWN** missing — do not invent

Company-claimed metrics: always label. See `references/evidence-grades.md`.

## Output tree (generic)

```
outputs/gtm-playbook-<slug>/
  00-meta/     README, SOURCE-INDEX, CONFIDENCE-MAP, GAPS, COMPLETENESS-SCORECARD, RUN-CONFIG
  01-entity/   COMPANY-LOCK, ...
  02-raw-evidence/<module>/...
  03-analysis/...
  04-playbook/...   (if enabled)
  05-verification/... (if enabled)
```

`<slug>` from target domain or normalized company name. Init via `scripts/init_run.py` when available.

Templates: `references/output-tree.md`.

## RUN-CONFIG.json

Written by `init_run.py` at start (update at end). Important fields:

```json
{
  "target_input": "<user string>",
  "entity_locked": null,
  "slug": null,
  "modules_preset": "standard",
  "modules_resolved": ["entity", "…"],
  "gather_modules": ["entity", "…"],
  "synthesis_modules": ["analyze", "verify", "playbook"],
  "depth": "standard",
  "collectors_detected": {},
  "output_dir": "",
  "started_at": "",
  "completed_at": null,
  "completeness_contracts": []
}
```

No default target company field. Never set target to an example output path.

## Modular execution examples

User: "only X GTM for https://example.com"  
→ modules: `entity`, `social_x`; completeness rollup phase; light `analyze` slice (social scorecard only); skip full playbook unless asked.

User: "Instagram ads only"  
→ modules: `entity`, `social_instagram`, `ads` (IG-relevant), completeness contracts, ads/social scorecards.

User: "full in-depth GTM playbook for Acme"  
→ all modules; Workflow recommended; verify + full playbook.

## Workflow templates

- `workflows/README.md` — how to compose  
- `workflows/modular-gather.md` — gather agent prompt patterns (parameterized)  
- `workflows/full-run.md` — full depth phase map  
- Do not ship company-specific JS. Any Workflow script must take `args`: `{ target, modules, outputDir, depth, collectors }`.

## QA expectations while using this skill

Before final handoff:

1. Entity lock file exists and matches user target  
2. Every enabled gather module has a completeness contract  
3. No invented metrics  
4. SOURCE-INDEX lists sources  
5. GAPS-AND-UNKNOWNS honest  
6. If playbook enabled: recommendations cite grades  

## References to load as needed

| File | When |
|------|------|
| `references/modules.md` | Module plan / dependencies |
| `references/completeness-contracts.md` | Every gather |
| `references/collector-matrix.md` | Start of run |
| `references/output-tree.md` | Init outputs |
| `references/evidence-grades.md` | Analysis / verify / playbook |
| `references/playbook-chapters.md` | Playbook module |
| `references/agent-prompt-templates.md` | Spawning subagents |
| `references/guardrails.md` | Browser/safety |

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/detect_collectors.py` | Print JSON of available collectors |
| `scripts/init_run.py` | Expand presets, create tree + RUN-CONFIG |
| `scripts/validate_run.py` | Fail-closed QA (`--phase post_gather|final`) |

## Anti-patterns

- Hardcoding a demo company’s handles as defaults  
- Requiring Kimi/browser to run at all  
- One tab per post / mass navigation  
- Claiming complete social history without contract proof  
- Turning company-claimed ARR into playbook foundation  
