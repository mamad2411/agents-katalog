---
name: consolidate-research
description: Consolidate and synthesize research outputs from multiple AI models or sources into a unified, pattern-aware, provenance-enriched report with quality metrics. Use when the user has research outputs to consolidate, wants to synthesize multiple reports, asks to "consolidate", "synthesize", or "merge" research findings, or needs to reconcile conflicting information from different sources. Works with outputs from Claude, Gemini, GPT-5.2, or any combination of AI/human sources. Supports manifest-driven (from create-research-brief) and standalone operation.
---

# Consolidate Research

Synthesize research outputs from multiple sources into a unified, confidence-tiered, pattern-aware report with provenance tracking and quality metrics. Works standalone or manifest-driven from `create-research-brief`.

**Shared references**: `consolidation-manifest-schema.md` (schema), `pattern-registry.md` (patterns + defaults)

## Workflow Overview

```
1. RECEIVE INPUTS ─── Manifest detection, source identification
2. NORMALIZE INPUTS ── Model-specific extraction → common claim format
3. TRIAGE CLAIMS ───── Atomic decomposition, dependency graphs, provenance
4. RECONCILE ───────── Provenance-weighted disagreement, citation dedup
5. SYNTHESIZE ──────── Cross-domain synthesis, structural artifact merging
6. GENERATE OUTPUT ─── Pattern-specific template, quality metrics, freshness
7. SELF-REVIEW ─────── 7 mandatory checks before finalizing
```

---

## Step 1: Receive & Validate Inputs

### Manifest Detection

```
Input contains YAML block with `consolidation_manifest:` label?
│
├─ YES (manifest-driven)
│   ├─ Parse manifest fields: research_id, pattern, models, coverage_matrix
│   ├─ Extract consolidation config: mode, verification_priorities
│   ├─ Load pattern-specific output template from Pattern Registry
│   ├─ Note research chain context (upstream_id, inherited_constraints)
│   └─ Use model identifiers from manifest — do NOT guess sources
│
└─ NO (standalone mode)
    ├─ Ask for or infer: topic, sources, consolidation mode
    ├─ Derive pattern from content using Pattern Registry decision tree
    ├─ Use pattern defaults from Quick Reference table
    └─ Confirm inferred pattern + mode with user before proceeding
```

### Source Identification Heuristics

When manifest is absent and source is unlabeled, apply capability-aware signals:

| Signal | Likely Source | Strength |
|--------|--------------|----------|
| Deep reasoning chains, cross-domain analogies, self-corrections, hedged nuance | Claude Opus 4.6 | primary_researcher |
| Structured tables with dense citations, systematic catalogs, source appendix | Gemini 3.1 Pro Deep Research | structured_cataloger |
| Site-specific citations, temporal progression ("as of [date]"), intervention markers | GPT-5.2 Deep Research | targeted_investigator |
| Quick facts, recent dates, sentiment language, short-form responses | GPT-5.2 Chat | recency_validator |
| Proprietary data, specific methodologies, organizational context | Human analyst | domain_expert |

If uncertain after heuristic check, ask user to confirm. When manifest is present, always use `manifest.models[].model_id`.

### Validation

```
Research outputs provided?
├─ NO → Ask: "Please share the research outputs to consolidate."
└─ YES → Sources identifiable?
         ├─ NO → Ask: "Which source produced each output?"
         └─ YES → ≥2 sources?
                  ├─ NO → Warn: single-source consolidation has limited value.
                  │        Offer: proceed as structured review, or add sources.
                  └─ YES → Proceed to Step 2.
```

---

## Step 2: Normalize Inputs

Convert heterogeneous model outputs into a common claim format before triaging.

### Extraction Patterns by Source

| Source | Extract | Tag |
|--------|---------|-----|
| **Claude Opus 4.6** | Reasoning chains (analytical steps, not just conclusions) | `type: reasoning_chain` |
| | Conclusions linked to their supporting chains | `type: factual/causal` |
| | Web search findings with source URLs | `channel: web_search` |
| | Cross-domain insights and analogies | `type: cross_domain_synthesis` |
| | Self-review corrections (higher-confidence refinements) | `type: factual` |
| **Gemini 3.1 Pro** | Tables — preserve structure, do not flatten | `type: structural_artifact` |
| | Prose claims with inline citation mapping | `type: factual/causal` |
| | Source appendix — map citations to claims, compute quality scores | provenance metadata |
| | Comparison matrices with per-cell provenance | `type: structural_artifact` |
| | file_search-grounded claims | `channel: internal_document` |
| **GPT-5.2 Deep** | Assertions with temporal markers ("as of [date]") | `provenance.temporal_marker` |
| | Site-specific findings with source domain | `channel: site_restricted` |
| | Intervention-adjusted findings (higher targeted confidence) | boosted weight |
| | Timeline/progression narratives | `type: structural_artifact` |
| **GPT-5.2 Chat** | Quick facts with recency dates | `channel: quick_validation` |
| | Sentiment signals | `type: recommendation` |
| | *All Chat claims default to lower provenance weight* | validation role |

### Normalized Claim Format

```yaml
claim: {id: "C-{seq}", text: "...", type: factual|causal|quantitative|recommendation|unique|reasoning_chain|structural_artifact,
  source_model: claude-opus-4-6|gemini-3.1-pro|gpt-5.2-deep|gpt-5.2-chat|human,
  provenance: {channel: web_search|file_search|site_restricted|quick_validation|internal_document,
    site_restrictions: [], context_documents: [], citation_quality: 0-5, temporal_marker: "YYYY-MM-DD"|null},
  depends_on: [claim IDs]}
```

### Citation Quality Scale

| Score | Source Type | Examples |
|-------|------------|---------|
| 5 | Primary | SEC filings, peer-reviewed, official stats, vendor docs |
| 4 | High-quality secondary | Gartner, Forrester, named-source journalism |
| 3 | General secondary | News, press releases, industry publications |
| 2 | Tertiary | Wikipedia, blogs, aggregators |
| 1 | Unsourced assertion | No citation trail |
| 0 | Unverifiable | Contradicts known facts or cites non-existent sources |

---

## Step 3: Triage Claims

Decompose normalized claims into an atomic claims matrix with dependency tracking.

### Claim Types

| Type | Handling |
|------|----------|
| **Factual assertions** | Cross-validate; trace to primary sources |
| **Causal claims** | Map reasoning chains; note mechanism divergence |
| **Quantitative data** | Flag discrepancies >10%; verify primary source agreement |
| **Recommendations** | Tag as interpretation; link to supporting facts |
| **Unique insights** | Preserve with provenance flag; do not discard |
| **Reasoning chains** | Preserve structure; validate logical steps; compare across sources |
| **Structural artifacts** | Preserve format (tables, matrices, timelines); merge in Step 5 |

### Claims Matrix

Rows = claims, columns = sources. `(qN)` = citation quality. Flag same-primary-source convergence separately.

```
             │ Claude │ Gemini │ GPT-5.2D│ GPT-5.2C│ Status
─────────────┼────────┼────────┼─────────┼─────────┤
Claim A      │ ✓ (q4) │ ✓ (q5) │  ✓ (q3) │         │ Convergent (diff sources)
Claim B      │ ✓ (q4) │ ✓ (q4) │         │         │ Convergent (same primary?)
Claim C      │ ✓ (q3) │        │         │         │ Unique
Claim D      │ ✓ (q4) │ differ │  differ │         │ Contested
```

### Claim Dependency Graphs

`Claim A (factual) ──supports──► Claim B (causal) ──supports──► Claim C (recommendation)`

**Rules**: Recommendation confidence CANNOT exceed supporting facts. If a fact drops tiers, propagate to ALL dependents. Document chains in output.

---

## Step 4: Reconcile

### Provenance-Weighted Disagreement Protocol

Execute in order — stop at first resolution:

| Step | Test | Resolution |
|------|------|-----------|
| 1 | **Coexist?** Different scope/timeframe/definition? | Preserve both with clarifying context |
| 2 | **Provenance?** Higher channel? (`site_restricted` > `web_search` > `quick_validation`; `internal_document` > `web_search` for proprietary) | Favor higher provenance; note alternative |
| 3 | **Citation dedup?** Same primary source(s)? | Treat as SINGLE-SOURCE (Tier 2 cap), not independent |
| 4 | **Specificity?** One more specific or better sourced? | Favor specificity; note alternative |
| 5 | **Majority?** Most sources agree? | Lead with majority; preserve dissent |
| 6 | **All diverge** | Flag "unresolved." Agentic mode: web search. Else: present all views |

### Confidence Tier Assignment

| Tier | Threshold | Criteria |
|------|-----------|---------|
| **1** (High) | >75% | Cross-model from DIFFERENT primaries + avg quality ≥4 + falsifiable |
| **2** (Moderate) | 50-75% | Same-primary cross-model (cap) OR single quality ≥4 OR majority w/ avg 3 |
| **3** (Low) | <50% | Single-source quality <4 OR contested OR unsourced |

Key rule: Same-primary-source agreement caps at Tier 2 — prevents "3 models citing same blog" inflation.

### Dependency Propagation

After reconciling individual claims: (1) Walk dependency graph root-to-leaf. (2) Supporting claim dropped → dependent drops too (floor: Tier 3). (3) Recommendations on Tier 3 facts → flag: "requires independent verification." (4) Document all propagation in Methodology Notes.

### False Confidence Audit

Apply to all Tier 1 candidates (mandatory in Adversarial mode):

| Check | Question |
|-------|---------|
| Citation diversity | Different primary sources, or all citing same 2-3? |
| Specificity test | Falsifiable claim, or vague enough to be unfalsifiable? |
| Recency check | Could this have changed? Source publication dates? |
| Contrarian search | Credible dissent? What would skeptics say? |
| Mechanism check | Same mechanism = shared bias risk. Different mechanisms converging = higher confidence. |

If concerns → downgrade to Tier 2 with explicit note.

---

## Step 5: Synthesize

Transforms reconciled claims into integrated insights. Mandatory — not optional.

### Cross-Domain Synthesis Pass (4 Required Prompts)

| # | Prompt | Seeks |
|---|--------|-------|
| 1 | "Which findings, when combined, imply something neither source stated?" | Emergent insights |
| 2 | "Which constraints interact with findings from another domain?" | Constraint interactions |
| 3 | "Which consensus views look different through an unrelated domain's lens?" | Frame-breaking |
| 4 | "What would need to be true for the consensus to be wrong?" | Contrarian check |

Tag all outputs `claim_type: cross_domain_synthesis`. Document pass execution even if yield is zero.

### Structural Artifact Merging

| Artifact | Merge Strategy |
|----------|---------------|
| Tables | Union rows/columns; per-cell provenance; highlight conflicts |
| Timelines | Interleave chronologically; flag disputed dates with both versions |
| Decision trees | Merge branches; note divergent recommendations at same decision point |
| Matrices | Union dimensions; per-cell provenance; highlight scoring disagreements |

---

## Step 6: Generate Output

### Template Selection

Manifest present with pattern → use directly. No manifest → infer from content via Pattern Registry decision tree; confirm with user.

### Universal Sections (All Patterns)

| # | Section | Content |
|---|---------|---------|
| 1 | Executive Summary | 2-3 paragraphs: key findings, implications, overall confidence |
| 2 | Tier 1 Findings | High-confidence claims: claim + support + implication |
| 3 | Tier 2 Findings | Moderate-confidence: claim + support + caveat |
| 4 | Contested Areas | Per-source views + assessment + resolution path |
| 5 | Coverage Gaps | Expected vs actual coverage table with recommended actions |
| 6 | Unique Insights | Per-source single-source findings with provenance |
| 7 | Cross-Domain Synthesis | Emergent insights, constraint interactions, frame-breaking observations |
| 8 | For Downstream | Pattern-specific actionable outputs |
| 9 | Quality Metrics | Computed metrics block |
| 10 | Freshness Model | Staleness detection + refresh recommendations |
| 11 | Methodology Notes | Mode, sources, conflicts resolved, chain context, limitations |
| 12 | Self-Review Results | 7-check outcomes summary |

### Pattern-Specific Sections

In addition to universal sections, each pattern adds:

| Pattern | Additional Sections |
|---------|-------------------|
| `landscape_mapping` | Taxonomy + Player Inventory per category, White Space Map |
| `comparative_evaluation` | Weighted Decision Matrix (options x criteria), Sensitivity Analysis, Recommendation with flip conditions |
| `implementation_pattern` | Architecture Decision Catalog, Pattern Catalog by phase, Anti-Pattern Register |
| `best_practices` | 8-Dimension Knowledge Base sections, Quick Reference Card |
| `competitive_intelligence` | Per-Competitor Strategic Profile, Competitive Dynamics Analysis |
| `market_research` | TAM/SAM/SOM with ranges, Segmentation Framework, Demand Drivers/Inhibitors |
| `user_research` | Persona Cards, JTBD Map (functional/emotional/social), Unmet Needs Hierarchy |
| `economic_analysis` | Financial Model (cost + value + ROI), Sensitivity Table, Benchmark Comparison |
| `compliance_requirements` | Requirements Register, Constraint Map, Governance Recommendations |

### "For Downstream" Actionability

| Pattern | Downstream Content | Primary Target |
|---------|-------------------|---------------|
| `landscape_mapping` | Shortlist criteria + recommended evaluation set | `comparative_evaluation` |
| `comparative_evaluation` | Decision recommendation + selection rationale + ADR draft | Foundry / `implementation_pattern` |
| `implementation_pattern` | Architecture decision log + implementation checklist | Foundry (requirements) |
| `best_practices` | Skill-ready KB structure + Quick Reference Card | Claude Code skills |
| `competitive_intelligence` | Positioning strategy + differentiation matrix | Ignite (GTM) |
| `market_research` | Segment prioritization + entry strategy recommendation | Spark (ideation) |
| `user_research` | Persona cards + JTBD map + ranked unmet needs | Foundry + Spark |
| `economic_analysis` | Financial model summary + key assumptions + sensitivity ranges | Vantage |
| `compliance_requirements` | Requirements register + constraint map | Foundry |

### Quality Metrics

Compute and include in every output:

| Metric | Formula | Meaning |
|--------|---------|---------|
| `coverage_ratio` | claims addressed / total claims | Input coverage completeness |
| `conflict_resolution_rate` | resolved / identified | Disagreement handling |
| `provenance_depth` | % Tier 1 with multi-source from DIFFERENT primaries | Independent corroboration |
| `actionability_score` | % findings with downstream action | Output usefulness |
| `staleness_risk` | % claims with sources older than volatility threshold | Temporal reliability |
| `dependency_chain_integrity` | % recommendations with validated chains | Logical soundness |
| `cross_domain_synthesis_yield` | count of cross-domain insights | Synthesis value-add |

### Freshness Model

```yaml
freshness_model:
  research_id: "{from manifest or generated}"
  research_pattern: "{pattern_id}"
  topic_volatility: high|medium|low   # from Pattern Registry
  estimated_half_life: 3_months|6_months|12_months
  recommended_refresh: "YYYY-MM-DD"   # execution date + half-life
  staleness_indicators: ["signal 1", "signal 2", "signal 3"]  # 3-5 observable triggers
  source_dates: {oldest: "YYYY-MM-DD", newest: "YYYY-MM-DD"}
```

---

## Step 7: Self-Review (Mandatory)

Execute ALL checks before finalizing. Report results in the Self-Review Results section.

| # | Check | Procedure | If Failed |
|---|-------|-----------|-----------|
| 1 | **Contradiction scan** | Do claims in one section contradict another? | Reconcile or flag explicitly. |
| 2 | **Confidence tier audit** | Did any claim's tier shift during writing? | Update tier + propagate dependencies. |
| 3 | **Dependency chain validation** | Are all recommendation → fact chains consistent? | Flag broken chains; downgrade recommendations. |
| 4 | **Coverage check** | Compare actual coverage vs. manifest coverage_matrix (or inferred). | Document gaps in Coverage Gaps section. |
| 5 | **Cross-domain synthesis check** | Was the mandatory synthesis pass executed? Insights generated? | If skipped, execute now. If zero yield, document. |
| 6 | **Quality metrics validation** | Are metrics internally consistent? (e.g., denominator matches actual count) | Recompute. |
| 7 | **Freshness check** | Any source dates older than topic volatility threshold? | Flag in staleness_risk metric + Freshness Model. |

---

## Consolidation Modes (7)

### Mode Quick Reference

| Mode | Best For | Leads With | Key Differentiator |
|------|----------|------------|-------------------|
| **Standard** | General synthesis | Convergent findings | Balanced tiering |
| **Adversarial** | High-stakes decisions | Stress-tested claims | False confidence audit on ALL Tier 1 |
| **Gap-Driven** | Coverage completeness | Missing areas | Coverage matrix as primary frame |
| **Confidence-Weighted** | Executive / financial decisions | Evidence quality | Citation quality drives tiers |
| **Depth-First** | Strategic / analytical topics | Deepest reasoning | Reasoning chains featured |
| **Breadth-First** | Landscape / domain mapping | Comprehensive coverage | Completeness over depth |
| **Agentic** | Minimal-intervention consolidation | Full autonomous pipeline | Web search for gap-filling + verification |

### Mode Selection Logic

Priority: (1) User explicit > (2) Manifest recommended_mode > (3) Infer from context > (4) Pattern default.

**Context inference signals**: "high stakes"/"executive" → confidence_weighted | "due diligence"/"comprehensive" → gap_driven | suspiciously aligned outputs → adversarial | "quick synthesis" → standard | strategic/nuanced → depth_first | new domain/landscape → breadth_first | "agentic"/"hands-off" → agentic.

When inferred, confirm: "I'll use **[Mode]** based on [reasoning]. This will [brief description]. Proceed?"

### Pattern x Mode Defaults

| Pattern | Default Mode | Override Trigger |
|---------|-------------|-----------------|
| `landscape_mapping` | breadth_first | "deep-dive on key players" → depth_first |
| `comparative_evaluation` | confidence_weighted | "quick comparison" → standard |
| `implementation_pattern` | depth_first | "comprehensive catalog" → breadth_first |
| `best_practices` | gap_driven | "focus on anti-patterns only" → depth_first |
| `competitive_intelligence` | adversarial | "just the facts" → standard |
| `market_research` | standard | "high-stakes investment" → confidence_weighted |
| `user_research` | depth_first | "broad needs survey" → breadth_first |
| `economic_analysis` | confidence_weighted | "rough estimate" → standard |
| `compliance_requirements` | gap_driven | "highest-risk areas" → depth_first |

### Mode Procedures

**Standard**: (1) Identify convergent claims. (2) Flag divergent for reconciliation. (3) Apply disagreement protocol. (4) Tier by confidence (same-primary-source caps at Tier 2).

**Adversarial**: (1) Flag suspicious alignment on contested topics. (2) False Confidence Audit on ALL Tier 1. (3) Identify cross-source critique points. (4) Stress test: what falsifies aligned claims? (5) Downgrade where audit reveals concerns.

**Gap-Driven**: (1) Derive expected coverage from manifest or pattern template. (2) Audit actual vs expected. (3) Document total gaps (no coverage) + partial gaps (single-source). (4) Prioritize by downstream impact.

**Confidence-Weighted**: (1) Citation Quality Scale on every claim. (2) Per-claim confidence = `(sum scores) / (max possible)`. (3) Weight by quality, not source count. (4) Single quality-5 > three quality-1.

**Depth-First**: (1) Find deepest source (usually Claude/human). (2) Lead with reasoning chains. (3) Validate key chain claims via other sources. (4) Fill breadth gaps from cataloger (Gemini). (5) Feature strategic insights prominently.

**Breadth-First**: (1) Find most comprehensive source (usually Gemini). (2) Lead with coverage completeness. (3) Add depth on high-importance areas. (4) Update with recency from GPT-5.2. (5) Completeness is primary metric.

**Agentic**: Autonomous end-to-end with minimal user intervention. (1) Ingest all + manifest. (2) Execute Steps 2-5 autonomously. (3) Web search to resolve conflicts. (4) Targeted searches for coverage gaps. (5) Draft with cross-domain synthesis. (6) Full self-review with web verification. (7) Compute metrics; revise if needed. (8) Final output. Requires: `claude-opus-4-6`, `thinking: adaptive`, `effort: max`. Use when: all models done, topic bounded, manifest present, user wants hands-off.

---

## Research Chain Protocol

When `manifest.research_chain.upstream_id` is set: (1) Request upstream consolidated output if not provided. (2) Validate downstream vs upstream consistency. (3) Flag contradictions. (4) Propagate inherited_constraints. (5) Apply chain validations (below). (6) Note in Methodology: "Part of chain: [upstream] → [this]". If no upstream → standard consolidation.

### Chain-Specific Validations

| Chain Link | Validation |
|-----------|-----------|
| Landscape → Comparative | Do all evaluated options appear in upstream landscape? Flag new ones. |
| Comparative → Implementation | Does selected option match upstream recommendation? If different, document why. |
| Market → Landscape | Are market segments consistent with landscape scope? Flag scope drift. |
| Market → Competitive | Are market structure assumptions consistent? Flag divergence. |
| Compliance → Implementation | Do all patterns satisfy upstream constraint map? Flag violations. |
| User Research → Comparative | Do evaluation criteria map to identified user needs? Flag orphan criteria. |

### Constraint Propagation Rules

Upstream constraints are HARD by default — cannot contradict without explicit justification. If downstream evidence challenges an upstream constraint, flag as "constraint tension" (do not silently override). Document all propagated constraints in Methodology Notes.

---

## Integration Notes

**Manifest-driven** (after create-research-brief): Manifest provides ALL config — skip derivation. Pattern template pre-selected. Coverage matrix enables precise gap detection. Chain context available. Model capabilities known — provenance tagging is precise. Verification priorities pre-identified.

**Standalone**: Derive config from content + user input. User may paste a manifest manually. Pattern detection via Registry decision tree. Source ID via heuristic table. Coverage from pattern defaults. Works with any source types.
