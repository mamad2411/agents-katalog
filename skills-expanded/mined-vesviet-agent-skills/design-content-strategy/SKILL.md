---
name: design-content-strategy
description: Design holistic content portfolio strategies, pillar-and-cluster architectures, topical authority models, audience funnel mappings (TOFU/MOFU/BOFU), editorial calendars, Top 10 SERP Information Gain gating (>=75/100 non-commodity score), 3-tier content decay triage, and safe multi-channel distribution loops. Use when establishing site content architecture, planning editorial calendars, structuring topic clusters, auditing portfolio decay, or defining omnichannel content flywheels.
version: 2.0.0
allowed-tools: [read_file, write_file, edit_file, create_file, search_code]
---

# Design Content Strategy

Use this skill with the **Content Manager** role to architect, govern, and optimize a website's overall content asset portfolio. This skill bridges business objectives and editorial execution: establishing topical authority through pillar-cluster taxonomies, balancing the TOFU/MOFU/BOFU audience journey, enforcing Top 10 SERP Information Gain moats, triaging 3-tier decay, and engineering safe multi-channel distribution loops.

## When to Use

- architecting site-wide content taxonomies, pillar-cluster hierarchies, and Silo internal linking
- mapping content production to audience lifecycle stages (TOFU awareness, MOFU consideration, BOFU decision)
- building prioritized editorial calendars balancing publishing cadence and team capacity
- gating topic briefs against Top 10 SERP competitors to enforce non-commodity Information Gain (≥75/100)
- triaging portfolio content decay across 3 tiers (Algorithmic SERP drops, GEO AI Citation loss, Factual obsolescence)
- designing omnichannel distribution loops with strict semantic drift prevention

## Core Rules

### Pillar-Cluster Hub-and-Spoke Topology
- model each core topic as a central **Pillar Page** (broad entity overview, definitive guide) bidirectionally linked to 6–12 specialized **Cluster Pages** (sub-intents, long-tail queries)
- enforce strict **Silo internal link topology**: cluster pages link up to their parent pillar with descriptive anchor text; pillar links out to all clusters; cross-cluster links are restricted to pages within the same topical silo
- map entities to official knowledge bases (Wikidata QIDs) to reinforce machine-readable topical authority

### Funnel Lifecycle Balance (TOFU / MOFU / BOFU)
- balance production and portfolio mix across the full customer journey:
  - **TOFU (40%)**: Educational/symptom queries ("Why is X slow?"); KPI: organic traffic, newsletter signups
  - **MOFU (40%)**: Architecture comparisons, benchmarks, evaluation guides ("X vs Y"); KPI: trials, whitepapers
  - **BOFU (20%)**: High-intent migration guides, pricing teardowns, ROI calculators ("Migrate from X"); KPI: sales, conversion
- every asset must incorporate an explicit contextual bridge guiding the reader to the next down-funnel stage

### Top 10 SERP Information Gain Gate (≥75/100)
- mandate differential evaluation against all Top 10 ranking SERP competitors before commissioning briefs per [`references/information-gain-and-decay-triage.md`](references/information-gain-and-decay-triage.md)
- reject zero-gain skyscraper rewrites that merely synthesize existing search results
- require at least one of the **5 Information Gain Vectors** in every topic brief: (1) primary data & telemetry, (2) production incident teardowns & case evidence, (3) proprietary architecture/code, (4) counter-consensus trade-off analysis, (5) interactive tools/models — weights and bands per the canonical rubric in `audit-content/references/information-gain-rubric.md`
- briefs scoring < 75/100 on the Non-Commodity Matrix must be rejected or revised with net-new empirical assets

### 3-Tier Content Decay Monitoring & Lifecycle SLAs
- continuously monitor content health across 3 distinct decay tiers:
  - *Tier 1: Algorithmic SERP Decay*: >3 position loss or >25% MoM organic traffic decline
  - *Tier 2: Generative GEO Citation Decay*: ≥15% citation frequency drop in AI Overviews, AI Mode, ChatGPT, or Perplexity over 30 days
  - *Tier 3: Factual & Temporal Decay*: statistics >18 months old, deprecated API versions, broken outbound links
- assign and enforce remediation SLAs: Quick Patch (≤15 days), Structural Rewrite (≤30 days), Consolidation/301 (≤20 days), Decommission/410 (≤10 days)

### Safe Multi-Channel Distribution & Semantic Drift Prevention
- design distribution flywheels converting published pillar assets into social threads, newsletters, and video scripts per [`references/distribution-loops-and-drift-prevention.md`](references/distribution-loops-and-drift-prevention.md)
- enforce the **Semantic Drift Prevention Checklist**: short-form repurposed assets must never strip architectural constraints, security caveats, or operational trade-offs for social engagement
- enforce canonical URL attribution and UTM tracking governance across all distribution channels

## Suggested Process

1. **Entity & Domain Modeling**: Audit domain focus, identify target audience segments, and map primary knowledge graph entities per [`references/pillar-cluster-and-funnel-playbook.md`](references/pillar-cluster-and-funnel-playbook.md).
2. **Architect Pillar-Cluster Taxonomy**: Structure core pillar hubs and cluster spokes; specify Silo internal linking patterns and URL path schemas.
3. **Map Audience Journey & Funnel Balance**: Categorize candidate topics into TOFU (40%), MOFU (40%), and BOFU (20%); verify inter-funnel bridge CTAs for each topic.
4. **Execute Top 10 SERP Differential Gate**: Audit top 10 search results for candidate topics; verify Information Gain Vectors; calculate Non-Commodity Score (require ≥75/100).
5. **Sequence Editorial Calendar**: Construct calendar with assigned writers, deadlines, format specs, and growth-stage publishing cadences.
6. **Execute 3-Tier Decay Triage**: Audit existing inventory for Algorithmic, GEO Citation, and Factual decay; assign remediation SLAs and ROT classifications (keep, refresh, merge, retire).
7. **Deploy Distribution Loops & Drift Guardrails**: Map repurposing matrices; verify that short-form derivative assets preserve 100% of technical trade-offs.

## Checklist

- [ ] pillar-cluster taxonomy designed with explicit hub-and-spoke relationship and Silo link rules
- [ ] entity bindings verified with canonical knowledge graph sources (Wikidata / Schema.org)
- [ ] portfolio mix balanced across audience journey stages (TOFU 40%, MOFU 40%, BOFU 20%)
- [ ] inter-funnel bridge pathways defined from educational TOFU to commercial BOFU assets
- [ ] Top 10 SERP differential analysis completed; Non-Commodity Score verified ≥75/100
- [ ] at least one of 5 Information Gain Vectors validated and documented for each brief
- [ ] editorial calendar scheduled with explicit owners, deadlines, and publishing cadences
- [ ] 3-tier content decay triage executed across Algorithmic, GEO Citation, and Factual vectors
- [ ] decay remediation actions assigned with enforceable SLAs (Quick Patch, Rewrite, Merge, Retire)
- [ ] topic cannibalization resolved through consolidation plans or 301-redirect mappings
- [ ] omnichannel distribution flywheels mapped for all primary pillar assets
- [ ] semantic drift prevention checklist verified: zero technical trade-offs stripped in short-form copy
- [ ] canonical URL attribution and UTM parameter taxonomy configured for external distribution

## Output Contracts

When completing portfolio strategy planning, lifecycle audits, or editorial calendar allocations, emit:

- **`contracts/schemas/content-audit-report.json`** — Portfolio-wide or URL-level audit classifications, ROT actions (keep, refresh, consolidate, redirect, retire), decay tier flags, and SLA remediations. Set `contract_type: content-audit-report`.
- **`contracts/schemas/seo-weekly-board.json`** — Sprint topic planning boards, internal link targets, primary keyword assignments, and publishing cadences.
- For human-readable deliverables, author `content-strategy.md` (pillar architecture, audience journey, governance rules) in the target workspace.

## Failure Modes

- **Commodity skyscraper rewrites**: commissioning content that summarizes top search results without proprietary insight. Mitigation: enforce Top 10 SERP Information Gain Gate; reject briefs scoring < 75/100.
- **Unstructured flat content**: publishing disconnected blog posts without Silo linking or pillar hierarchy. Mitigation: enforce hub-and-spoke pillar-cluster architecture.
- **Funnel imbalance**: generating high TOFU traffic that never converts due to missing MOFU/BOFU assets. Mitigation: enforce 40/40/20 portfolio balance and inter-funnel bridge CTAs.
- **Unmonitored content decay**: allowing legacy pillars to bleed organic rankings and AI engine citations unnoticed. Mitigation: run monthly 3-tier decay scans; enforce SLA-governed remediation.
- **Semantic drift in distribution**: social snippets distort technical claims or omit critical safety caveats. Mitigation: enforce Semantic Drift Checklist before releasing repurposed assets.

## Security Guardrails (OWASP ASI)

- **ASI01 Agent Goal Hijack**: ensure content strategy aligns with authentic organizational mission; reject competitor-driven scope drift.
- **ASI03 Identity & Privilege Abuse**: protect internal roadmap secrets, unreleased telemetry, and customer metrics in strategy plans.
- **ASI07 Insecure Inter-Agent Communication**: emit machine-readable contracts (`content-audit-report.json`, `seo-weekly-board.json`) for seamless handoffs to Writers and SEO Analysts.
- **ASI09 Human-Agent Trust Exploitation**: enforce authentic practitioner SME bylines and verifiable source citations; strictly prohibit synthetic author personas.

## Related Skills

- **audit-content**: Granular refresh execution on individual URLs, fact checking, and AI semantic flaw scoring
- **write-article**: Long-form editorial drafting executed by Content Writer
- **write-copy**: High-conversion landing page copy, value propositions, and sales funnel copy
- **optimize-seo**: Keyword intent analysis, on-page briefs, and Schema.org `@graph` specifications
- **repurpose-content**: Draft channel-native variants for omnichannel distribution loops
- **analyze-data**: Telemetry baselines, GSC traffic decay modeling, and AI Share of Voice tracking
