---
name: create-research-brief
description: >
  Designs multi-model AI research strategies across 9 research patterns for
  Claude Opus 4.6, Gemini 3.1 Pro Deep Research, and optionally GPT-5.2 Deep
  Research (with site restrictions and mid-session intervention) or GPT-5.2
  Chat. Generates copy-pasteable prompts optimized per model with
  pattern-aware role assignment, a consolidation manifest for downstream
  synthesis, and a merge prompt for consolidating outputs. Accepts Research
  Request Specification from research-interviewer upstream. Triggers on
  "create research brief", "research plan", "multi-model research", "research
  prompts for Claude/Gemini/OpenAI", "design research strategy", "consolidate
  research outputs", "synthesize research results", "research best practices
  for...", "best practices for [technology]", "create a best practices guide
  for...", "research [technology] patterns", "document [technology] best
  practices", "compare X vs Y", "landscape of [domain]", "compliance
  requirements for [topic]", "ROI analysis for [decision]". Modes: DUAL
  (Claude+Gemini, default), FULL (3 models; GPT-5.2 Deep Research default),
  SINGLE (Claude only). 9 patterns: landscape_mapping,
  comparative_evaluation, implementation_pattern, best_practices,
  competitive_intelligence, market_research, user_research,
  economic_analysis, compliance_requirements. Outputs include consolidation
  manifest per consolidation-manifest-schema.md.
---

# Create Research Brief

Design multi-model research strategies for **Claude Opus 4.6**, **Gemini 3.1 Pro Deep Research**, and optionally **GPT-5.2 Deep Research** (site-restricted) or **GPT-5.2 Chat** across **9 research patterns**.

## Workflow

### Phase 1: Research Design

1. **Detect input type** -- Direct request OR Research Request Specification (from research-interviewer)
2. **Validate input** -- Clarify if vague (skip if Specification present)
3. **Detect model mode** -- DUAL (default) / FULL / SINGLE
4. **Detect OpenAI depth** -- Deep Research (default for FULL) or Chat
5. **Classify research pattern** -- Use decision tree from [references/pattern-registry.md](references/pattern-registry.md) to select one of 9 patterns
6. **If Best Practices** -- Load [references/best-practices-dimensions.md](references/best-practices-dimensions.md) and [references/technology-profiles.md](references/technology-profiles.md) for 8-dimension framework
7. **Assess topic risks** -- Recency, contestation, source availability, false confidence, coverage gaps
8. **Plan context budget** -- Estimate combined output size, select context tier
9. **Assign model roles** -- Load Pattern x Model Configuration Matrix from [references/model-profiles.md](references/model-profiles.md); assign roles, capabilities, thinking tiers, effort levels per pattern
10. **Configure GPT-5.2 site restrictions** -- If FULL mode, load site restriction library from [references/model-profiles.md](references/model-profiles.md) Section 6 and customize for topic
11. **Configure Gemini file_search** -- If user has relevant documents, load file search guidance from [references/model-profiles.md](references/model-profiles.md) Section 7 and recommend uploads
12. **Design consolidation strategy** -- Select pattern-default mode from Pattern Registry, allow user override
13. **Generate prompts** -- Use templates from [references/model-profiles.md](references/model-profiles.md) Section 5; for Best Practices, assemble dimension-specific fragments from [references/best-practices-dimensions.md](references/best-practices-dimensions.md)
14. **Generate consolidation manifest** -- Produce YAML manifest block per [references/consolidation-manifest-schema.md](references/consolidation-manifest-schema.md)
15. **Produce brief** -- Use output template from [references/output-templates.md](references/output-templates.md)
16. **Include merge prompt** -- Append merge prompt referencing the manifest from [references/output-templates.md](references/output-templates.md)

### Phase 2: Consolidation (after user executes prompts)

17. **Receive outputs** -- User pastes/attaches research results
18. **Consolidate** -- Follow workflow in [references/consolidation.md](references/consolidation.md)

---

## Model Overview

| Model | Role | Key Capabilities |
|-------|------|------------------|
| **Claude Opus 4.6** | Primary Researcher | 84% BrowseComp, 68.8% ARC-AGI-2, 1M context, 128K output, self-correction, cross-domain synthesis |
| **Gemini 3.1 Pro Deep** | Structured Cataloger | 85.9% BrowseComp, 77.1% ARC-AGI-2, 1M context, 64K output, file_search (uploaded docs as sources), autonomous 5-30 min agent |
| **GPT-5.2 Deep Research** | Targeted Investigator | Site-restricted search (unique), leading MRCR v2 at 128-256K, 5-30 min autonomous agent, mid-session intervention |
| **GPT-5.2 Chat** | Recency Validator | Quick recent developments, community signals |

**Capability uniqueness**: Claude = self-correction + cross-domain synthesis. Gemini = file_search. GPT-5.2 Deep = site-restricted search. Web research is a shared capability (Claude 84%, Gemini 85.9%); differentiate by approach, not access.

For detailed profiles, prompt templates, role assignment, and per-pattern configuration: [references/model-profiles.md](references/model-profiles.md)

---

## Mode Detection

### Model Mode

| User Signal | Mode |
|-------------|------|
| No model specification | **DUAL** (default) |
| "all three models" / "full research" / "include OpenAI" / "comprehensive" | **FULL** |
| "without OpenAI" / "skip OpenAI" / "Claude and Gemini only" | **DUAL** (confirm) |
| "dual model" / "two model" | **DUAL** |
| "Claude only" / "quick research" / "fast analysis" | **SINGLE** |

### OpenAI Depth (FULL mode only)

GPT-5.2 **Deep Research is the default** for FULL mode. Site-restricted search is its unique differentiator -- use Chat only when explicitly downgraded.

| User Signal | Depth |
|-------------|-------|
| No specification | **Deep Research** (default) |
| "quick OpenAI" / "lite" / "lightweight" / "skip deep research" | **Chat** |
| "OpenAI deep research" / "comprehensive OpenAI" / "site-restricted" | **Deep Research** (confirm) |

---

## Research Pattern Classification

Use the decision tree in [references/pattern-registry.md](references/pattern-registry.md) to classify. Summary table:

| Pattern | Trigger Signals | Primary Deliverable | Default Consolidation |
|---------|----------------|--------------------|-----------------------|
| **Landscape Mapping** | "map the landscape", "who's out there", "ecosystem overview" | Taxonomy + player inventory + white space map | breadth_first |
| **Comparative Evaluation** | "compare X vs Y", "which should I choose", "trade-offs" | Weighted decision matrix + sensitivity analysis | confidence_weighted |
| **Implementation Pattern** | "how do I implement", "architecture patterns", "reference architecture" | Architecture decision catalog + pattern catalog + anti-pattern register | depth_first |
| **Best Practices** | "best practices for", "idiomatic patterns", "gotchas", "anti-patterns" | 8-dimension technology knowledge base | gap_driven |
| **Competitive Intelligence** | "competitive moat", "positioning analysis", "competitive dynamics" | Per-competitor strategic profile + dynamics analysis | adversarial |
| **Market Research** | "market size", "TAM", "segments", "entry strategy" | TAM/SAM/SOM + segmentation framework + dynamics | standard |
| **User Research** | "user needs", "JTBD", "persona", "pain points" | Persona profiles + JTBD map + ranked unmet needs | depth_first |
| **Economic Analysis** | "ROI", "TCO", "cost-benefit", "business case" | Financial model + sensitivity analysis + benchmarks | confidence_weighted |
| **Compliance & Requirements** | "compliance", "regulatory", "GDPR", "audit requirements" | Requirements register + constraint map + governance | gap_driven |

### Best Practices Pattern

When pattern = **Best Practices**, activate the 8-dimension framework:

1. **Environmental Context** -- Runtime, config, auth, secrets, project structure
2. **Idiomatic Patterns** -- How practitioners write it vs. how it merely works
3. **Anti-Patterns & Guardrails** -- What fails at scale, root cause reasoning
4. **Testing & Validation** -- Emulators, mocks, integration tests, gaps
5. **Dependencies & Versions** -- Compatibility matrices, packages to avoid
6. **Operational Awareness** -- Cost drivers, scaling, cold starts, monitoring
7. **Decision Trees** -- When to use which approach, architectural boundaries
8. **Escape Hatches** -- Known bugs, workarounds with expiration, when to eject

Weight dimensions by technology family from [references/technology-profiles.md](references/technology-profiles.md). Assemble prompts using dimension fragments from [references/best-practices-dimensions.md](references/best-practices-dimensions.md).

---

## Input Detection

### Research Request Specification (from research-interviewer)

Detect by: YAML block with `research_request:` root containing `objective:`, `questions:`, `scope:`, `constraints:`.

**When detected**: Skip validation. Extract `objective`, `questions.primary/secondary`, `scope.in_scope/out_of_scope`, `constraints.model_mode`, `constraints.depth_vs_breadth`, `context.prior_knowledge`, `metadata.suggested_research_type` (verify, don't blindly accept).

### Direct Request Validation

**Required**: Research objective specific enough to derive key questions.

**Optional (with defaults)**: Research pattern (infer), context (none), timeline (standard), output use (general decision support), model mode (DUAL), OpenAI depth (Deep Research).

When insufficient and no Specification present:

> To design an effective research strategy, I need:
> 1. **Research objective**: What specific question(s) do you want answered?
> 2. **Research pattern** (optional): Landscape / Comparative / Implementation / Best Practices / Competitive / Market / User / Economic / Compliance?
> 3. **Context** (optional): Background, constraints, or intended use?
>
> **Alternatively**: Say "interview me about [topic]" to clarify your needs first.

---

## Risk Assessment

Rate each factor High / Medium / Low:

| Risk Factor | Assessment Criteria | Design Impact |
|-------------|---------------------|---------------|
| **Recency sensitivity** | How quickly does info change? | DUAL has reduced concern (Claude 84% + Gemini 85.9% BrowseComp). Flag only for live events, fast-moving regulation, or topics needing site-restricted precision (GPT-5.2). |
| **Contestation level** | Genuine disagreement? | May need adversarial consolidation |
| **Source availability** | Well-documented or sparse? | Affects coverage expectations |
| **False confidence risk** | Shared in LLM training? | Requires cross-validation |
| **Coverage gap risk** | Emerging/niche topic? | May need multiple search passes |

---

## Context Budget Planning

### Output Estimates by Model

| Model | Standard Output | Complex Output | Maximum |
|-------|----------------|----------------|---------|
| Claude Opus 4.6 | 15-40K tokens | 40-80K tokens | 128K tokens |
| Gemini 3.1 Pro | 30-60K tokens | 60-80K tokens | 64K tokens |
| GPT-5.2 Deep Research | 30-60K tokens | 60-80K tokens | ~80K tokens |
| GPT-5.2 Chat | 2-5K tokens | 5-10K tokens | ~15K tokens |

### Combined Budget by Mode

| Mode | Expected Combined | Tier | Strategy |
|------|-------------------|------|----------|
| SINGLE | 15-80K tokens | Standard | Single output, no consolidation needed |
| DUAL | 50-160K tokens | Standard | Both outputs unabridged, single consolidation pass |
| FULL | 100-240K tokens | Standard or Extended | All outputs unabridged |
| FULL (complex) | 150-300K+ tokens | Extended (beta) | Use 1M context, all unabridged |

**Principle**: Always prefer full unabridged outputs. Opus 4.6's 76% MRCR v2 long-context retrieval can attend throughout the window.

---

## Consolidation Modes

| Mode | When to Use |
|------|-------------|
| **Standard** | Moderate stakes, stable topics, quantitative findings reconcilable across sources |
| **Adversarial** | High stakes, contested topics, outputs seem too aligned, confirmation bias risk |
| **Gap-Driven** | Comprehensive requirements, explicit coverage checklists (e.g., 8-dimension BP framework) |
| **Confidence-Weighted** | Executive-facing, evidence quality paramount, selection decisions |
| **Depth-First** | Strategic decisions, insight > coverage, behavioral reasoning |
| **Breadth-First** | Landscape mapping, unfamiliar domains, completeness > depth |
| **Agentic** | All models completed, topic well-bounded, minimal human intervention needed |

### Pattern-Default Mapping

| Pattern | Default Mode | Override Trigger |
|---------|-------------|-----------------|
| `landscape_mapping` | breadth_first | User says "deep-dive on key players" -- depth_first |
| `comparative_evaluation` | confidence_weighted | User says "quick comparison" -- standard |
| `implementation_pattern` | depth_first | User says "comprehensive pattern catalog" -- breadth_first |
| `best_practices` | gap_driven | User says "focus on anti-patterns only" -- depth_first |
| `competitive_intelligence` | adversarial | User says "just the facts" -- standard |
| `market_research` | standard | User says "high-stakes investment decision" -- confidence_weighted |
| `user_research` | depth_first | User says "broad needs survey" -- breadth_first |
| `economic_analysis` | confidence_weighted | User says "rough estimate is fine" -- standard |
| `compliance_requirements` | gap_driven | User says "focus on highest-risk areas" -- depth_first |

For mode details and full consolidation workflow: [references/consolidation.md](references/consolidation.md)

---

## Effort & Thinking Directives

| Model | Directive | Values | Research Default | Consolidation Default |
|-------|-----------|--------|------------------|-----------------------|
| **Claude Opus 4.6** | effort | low / medium / high / max | max | max |
| **Gemini 3.1 Pro** | thinking | Low / Medium / High | High | -- |
| **GPT-5.2 Deep Research** | thinking_effort | low / medium / high / extended | extended | -- |
| **GPT-5.2 Chat** | mode | Instant / Thinking | Instant | -- |

Include in Claude Opus 4.6 prompts:
```yaml
# Claude API Configuration
model: "claude-opus-4-6"
thinking:
  type: "adaptive"
effort: "max"
max_tokens: 16000  # Up to 128000 for comprehensive output
```

If over-thinking detected: add "Use deep reasoning for strategic analysis; move efficiently through factual compilation."

---

## Consolidation Manifest

Every research brief must include a consolidation manifest YAML block generated per [references/consolidation-manifest-schema.md](references/consolidation-manifest-schema.md). The manifest travels from design through execution to consolidation.

Required fields: `research_id`, `pattern`, `topic`, `objective`, `model_mode`, `created_at`, `models[]` (per model: model_id, role, capabilities), `pattern_metadata`, `coverage_matrix`, `consolidation` (recommended_mode, pattern_default_mode, verification_priorities), `research_chain`, `freshness` (topic_volatility, confidence_half_life, staleness_indicators, recommended_refresh).

If this research follows prior research, populate `research_chain.upstream_id` with the previous manifest's `research_id`, `research_chain.upstream_pattern`, and `research_chain.inherited_constraints`.

---

## Quality Gates

### Before completing research brief:
- [ ] Input type detected (direct OR Specification)
- [ ] If Specification: fields extracted, interview_confidence noted
- [ ] If direct: objective is specific and actionable
- [ ] Model mode correctly detected (default: DUAL)
- [ ] Research pattern correctly classified (9 patterns, using decision tree)
- [ ] If Best Practices: 8 dimensions assessed, technology family identified, dimension weights applied
- [ ] Risk assessment completed (5 factors)
- [ ] Context budget estimated, tier selected
- [ ] Model roles assigned per Pattern x Model Configuration Matrix
- [ ] Claude prompt includes: effort directive, web search activation, cross-domain synthesis, self-review mandate
- [ ] Gemini prompt includes: thinking tier, structured data directives, citation requirements, table/matrix requests
- [ ] If FULL: GPT-5.2 site restrictions generated and customized for topic
- [ ] Gemini file_search recommendations included (if applicable)
- [ ] Consolidation mode matches pattern default (or documented override)
- [ ] Consolidation manifest generated with all required fields
- [ ] If sequential research: manifest includes research chain predecessors
- [ ] Freshness model populated (topic_volatility, confidence_half_life, staleness_indicators, recommended_refresh)
- [ ] Coverage matrix covers all key questions
- [ ] If from research-interviewer: prior_knowledge included in prompt context
- [ ] Merge prompt included at end of brief

### Before completing consolidation:
- [ ] All outputs processed (full, unabridged if within budget)
- [ ] Claims triaged by type with provenance tags
- [ ] Disagreements resolved per protocol
- [ ] False confidence audit applied to unanimous high-risk claims
- [ ] Confidence tiers assigned (Tier 1 >75%, Tier 2 50-75%, Tier 3 <50%)
- [ ] Self-review pass completed
- [ ] Cross-domain synthesis section populated
- [ ] Gaps documented with recommended actions
- [ ] Effort level set to "max"
- [ ] Context tier documented in methodology

---

## References

| File | Load When | Contents |
|------|-----------|----------|
| [references/model-profiles.md](references/model-profiles.md) | Generating prompts, assigning roles, configuring site restrictions, file_search guidance | Model capabilities, role assignments, Pattern x Model Configuration Matrix, prompt templates, site restriction library, file search guidance, effort/thinking directives |
| [references/pattern-registry.md](references/pattern-registry.md) | Classifying pattern, designing consolidation strategy, resolving compound intent | 9 pattern definitions, decision tree, trigger signals, deliverables, sequencing, pattern-default consolidation mapping, interrelationship matrix |
| [references/consolidation-manifest-schema.md](references/consolidation-manifest-schema.md) | Generating the consolidation manifest | Full YAML schema with required/optional fields, validation rules, examples |
| [references/output-templates.md](references/output-templates.md) | Producing the research brief | DUAL/FULL/SINGLE mode templates, pattern-specific output templates, merge prompt |
| [references/consolidation.md](references/consolidation.md) | Phase 2: consolidating research outputs | Consolidation workflow, disagreement protocol, self-review, output template, consolidation prompt |
| [references/best-practices-dimensions.md](references/best-practices-dimensions.md) | Pattern = Best Practices | 8-dimension framework, per-dimension Claude & Gemini prompt fragments, assembly instructions |
| [references/technology-profiles.md](references/technology-profiles.md) | Pattern = Best Practices | Pre-built scope templates and dimension weighting for technology families |
