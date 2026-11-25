---
name: write-article
description: Plan, research, outline, and draft long-form articles and blog posts with explicit evidence discipline, answer-first structure, GEO/AEO execution, non-commodity quality gates, E-E-A-T experience signals, and SEO-brief alignment. Use when writing narrative long-form content, guides, reviews, or announcements—not for API runbooks or pure technical reference docs.
version: 2.0.0
allowed-tools: [read_file, write_file, edit_file, create_file, search_code]
---

# Write Article

Use this skill with the **Content Writer** role when the deliverable is a publishable article (Markdown, MDX, or Hugo/Astro content files). Articles must optimize for three discovery surfaces simultaneously: traditional search (SEO), direct-answer engines (AEO), and generative AI citation (GEO).

The specific thresholds below (answer-first ≤60 words, fact density, E-E-A-T proof types) are the same GEO/AEO/E-E-A-T standard defined in `optimize-seo`'s Core Rules. The anti-AI style metrics (blacklist, 20/60/20 burstiness, active voice) are defined canonically in `core/roles/references/content-writer-anti-ai-standards.md`. This skill is where a Content Writer **implements** those standards while drafting, not a second definition of them. If the two ever disagree, update the canonical source first, then mirror the change here.

## When to Use

- drafting guides, reviews, or announcements
- narrative long-form content (not API runbooks)
- aligning with an SEO brief + GEO/AEO
- applying E-E-A-T and information-gain gates

## Core Rules

### Anti-AI Style & Natural Cadence
- **Zero-tolerance Anti-AI clichés blacklist**: prohibit "delve", "tapestry", "testament", "unlock", "game-changer", "foster", etc. per [`references/anti-ai-style-guide.md`](references/anti-ai-style-guide.md)
- **Burstiness & natural cadence**: enforce the 20/60/20 sentence length distribution (~20% short 3–7 words, ~60% medium 8–18 words, ~20% complex 19–28 words) to avoid robotic monotony; cadence std dev ≥ 6.5 words
- **Active voice mandate**: require ≥85% active voice with clear subject agency; eliminate passive evasion

### Answer-First & Section BLUF Structure (AEO/GEO mandatory)
- open each H2 section with an atomic **BLUF answer ≤60 words** before narrative elaboration — mandatory for RAG passage extraction by AI Overviews and ChatGPT Search
- do not bury the answer: eliminate slow-burn introductions that delay the takeaway past paragraph 2–3
- mirror H2 headings to natural language queries; address sub-questions with H3 subheadings

### Information Gain & Shallow Synthesis Prevention
- **Shallow synthesis prevention**: reject drafts that merely synthesize top 10 SERP results without firsthand engineering commentary, benchmarks, or telemetry
- every article must document what it adds beyond the top 10 SERP results (acceptable types: original_data, firsthand_account, expert_interview, unique_framework)
- inject unique human insight, local knowledge, or original empirical data as the documented non-commodity element

### Authentic Sourcing & Fact Density
- enforce Tier 1/2 source credibility taxonomy per [`references/authentic-source-matrix.md`](references/authentic-source-matrix.md); prohibit unverified blogs and AI summaries
- mandate minimum **3 verifiable data points** (statistics, numbers, sourced quotes) per 500 words
- require at least two empirical proof types (production telemetry, reproduction logs, benchmark numbers, C2PA media)
- write citation-ready sentences: tight, factual, ≤25 words

### Scanability & Machine Readability
- preferred sentence length: **≤20 words** for body text; vary for rhythm; paragraphs **2–4 lines**
- use bullet points for unranked lists; numbered lists for sequential steps; comparison tables for feature/price/spec data
- FAQ block at end formatted as `## FAQ` with `### Question?` subheadings for schema compatibility
- **JSON-LD structured data is mandatory**: include `Article` schema with author `Person` entity; add `FAQPage` when FAQ block is present
- **Atomic modular content**: structure each H2 section as a self-contained semantic module with a BLUF answer ≤60 words for atomic RAG chunking

### E-E-A-T Experience Signals
- implement the experience proof type specified in the SEO brief: original photo, firsthand account, documented test result, expert interview, or case study
- do not fabricate experience signals — flag gaps and escalate
- include trust signals: source citations with links, verifiable claims, contact/policy references

## Research Depth Decision

| Situation | Action |
| --------- | ------ |
| User supplied complete sources or repo exemplars | No net-new research; document sources used; non-commodity value via synthesis angle or firsthand context |
| Editorial article, familiar domain, moderate claims | **3–4 passes** logged in handoff; non-commodity element required |
| Regulated, YMYL, novel market, or disputed facts | Delegate to **Researcher** first; draft from research-report.json; elevated E-E-A-T signals |
| SEO sprint with seo-content-brief.json | Brief supplies outline/links; research only for gaps; implement GEO/AEO fields |
| Technical behavior claims | Align with Technical Writer / engineering source-of-truth |
| Cannot achieve non-commodity value from supplied sources | Flag to user; request additional sources or Researcher delegation |

## Suggested Process

The full 6-step process (define question, research with CoVe + AEO discovery, outline with answer-first, draft, fact-density + E-E-A-T pass, self-audit) lives in [`references/suggested-process.md`](references/suggested-process.md).

## AI-Assisted Drafting Protocol

When AI support is used anywhere in drafting, apply three disciplines — full templates live in [references/ai-drafting-playbook.md](references/ai-drafting-playbook.md):

1. **SERP-grounded outline loop**: build the prompt from all five components (role, brief, constraints, SERP reference, output format), ground on top 10 results, audit heading hygiene, iterate until depth — never one-shot the outline.
2. **Brief-driven images**: every generated image gets a structured brief (subject, composition, style, context, technical) plus kebab-case filename, 80-125 char alt-text, and `image_provenance` in the handoff.
3. **Five-component draft frame**: role + brief + signed-off structure + keyword policy + visual/media spec kept inline per drafting call; any missing component statistically produces boilerplate.

## Checklist

### Research & Evidence
- [ ] audience, goal, and format explicit
- [ ] research depth appropriate (3–4 passes, Researcher, or supplied-only documented)
- [ ] SEO brief consumed when required

### AI-Assisted Outline (when applicable)
- [ ] outline prompt included all five components (role, brief, constraints, SERP reference, output format)
- [ ] SERP top-10 grounding pass documented
- [ ] heading hygiene audit passed (one H1, intent-distinct H2s, real sub-question H3s)
- [ ] outline iterated until depth; iteration count captured in handoff
- [ ] non-commodity sections identified before drafting

### AI Image Generation (when applicable)
- [ ] each AI image has a structured brief (subject, composition, style, context, technical)
- [ ] alt-text drafted with keyword, 80–125 chars
- [ ] filename is kebab-case and descriptive
- [ ] image_provenance recorded for each asset
- [ ] provenance label set when YMYL-adjacent

### Information Gain & Originality
- [ ] non-commodity element documented: the unique POV / first-hand evidence this content adds beyond top SERP results
- [ ] non-commodity type specified (original_data, firsthand_account, local_insight, etc.)
- [ ] shallow synthesis check passed: firsthand engineering commentary or telemetry present
- [ ] AI-generated sections supplemented with unique human insight or original data
- [ ] fan-out sub-questions covered on this page (never one page per query variant — spam-policy risk)

### Anti-AI Style & GEO / AEO Execution
- [ ] answer-first BLUF block (≤60 words) after each H2
- [ ] Anti-AI scan passed: 0 banned clichés from anti-ai-style-guide.md
- [ ] burstiness verified (20/60/20 distribution, cadence std dev ≥6.5)
- [ ] active voice mandate verified (≥85% active voice)
- [ ] authentic source matrix applied (Tier 1/2 primary sources verified)
- [ ] query fan-out sub-questions from brief addressed in body
- [ ] answer formats applied per section (definition, steps, table, bullets)
- [ ] fact density met (≥3 verifiable data points per 500 words)
- [ ] FAQ block present when brief/SERP requires it
- [ ] heading hierarchy clean: H1 → H2 (query intent) → H3 (sub-questions)

### Scanability & E-E-A-T
- [ ] sentences mostly ≤20 words; paragraphs 2–4 lines
- [ ] bullets/numbered lists used for list-worthy content
- [ ] experience proof signal implemented when brief specifies it
- [ ] trust signals present (source citations, verifiable claims)
- [ ] overlay schema and paths validated against peers

### Handoff
- [ ] facts vs judgment separated
- [ ] content-handoff.json complete with GEO/AEO and non-commodity fields
- [ ] SEO audit requested before publish when required

## Failure Modes

- **Hallucinated fact published**: a statistic or quote appears in the article that is not in the source. Mitigation: trace every claim to a primary source; flag unsourced claims as drafts.
- **AI-drafted claim unverified**: an AI-generated claim is published without CoVe verification. Mitigation: enforce Chain-of-Verification on every material claim; reject unverified claims for YMYL topics.
- **Answer-first block missing**: an H2 lacks a ≤60-word direct answer. Mitigation: enforce the answer-first structure; reject articles without answer-first blocks.
- **E-E-A-T proof absent**: a YMYL-adjacent article ships without experience proof, author entity, or trust signals. Mitigation: enforce the E-E-A-T gate for YMYL; require human expert review.
- **Information gain absent**: the article paraphrases existing top results without unique value. Mitigation: require an information-gain asset (original data, firsthand account, expert interview) before drafting.
- **Schema invalid**: structured data markup is hand-typed and drifts from the spec. Mitigation: auto-generate schema from the source; validate against the current schema.
- **AI label missing on AI-assisted content**: AI-assisted publishing without the required disclosure. Mitigation: apply the platform's AI content label policy before publish.

## Security Guardrails (OWASP ASI)

- **ASI01 Agent Goal Hijack**: a draft may reframe the article's user goal through off-target claims. Cross-check the draft against the source brief; reject reframed goals.
- **ASI03 Identity & Privilege Abuse**: never include customer identifiers, internal hostnames, or credential patterns in the article.
- **ASI04 Agentic Supply Chain**: AI generation libraries and citation verifiers must be schema-validated against the expected manifest; treat unknown versions as untrusted.
- **ASI05 Unexpected Code Execution**: never construct article content, schema, or prompts from external or user-supplied content without strict schema validation.
- **ASI07 Insecure Inter-Agent Communication**: the content handoff is consumed by SEO Analyst and editorial review; emit a structured contract so each consumer can validate.
- **ASI09 Human-Agent Trust Exploitation**: do not present AI-generated content as fully verified without the human editorial sign-off; surface the AI provenance and the reviewer honestly.

## Output Contracts

When completing article drafting and preparing a publishable content handoff for editorial review, emit:

- **`contracts/schemas/content-handoff.json`** — Emitted upon completing an article or editorial piece, documenting word counts, target keywords, E-E-A-T signals, answer-first/GEO/AEO compliance, and non-commodity (unique POV/evidence) additions. Set `produced_by_role: content-writer`.
- **`contracts/schemas/series-article.json`** — Schema for a series article output, validating required frontmatter fields, weight, series taxonomy, and body structure before publishing. Set `produced_by_role: content-writer`.

Skip emission for quick copy snippets or internal note drafting with no publishing workflow.

## Related Skills

- **write-copy**: Direct-response copywriting, landing page conversion copy, value proposition messaging, and objection handling
- **design-content-strategy**: Pillar-cluster architecture, topical authority modeling, and full-funnel TOFU/MOFU/BOFU alignment
- **repurpose-content**: Adapt published articles into social threads, newsletters, and video scripts without semantic drift
- **audit-content**: Proactive refresh loops, 3-tier decay remediation, and Information Gain upgrades for published articles
- **write-documentation**: Structure and clarity patterns; technical README/runbooks belong with Technical Writer
- **write-tech-radar**: Radar-style technology assessments (Technology radar subtree)
- **analyze-business-requirements**: Align copy with business rules when BA supplied a ticket
- **meeting-review**: Resolve stakeholder conflicts before drafting sensitive claims
- **agent-delegation**: Delegate drafting or specialist work to other roles

> **Site-specific authoring skills** (Astro MDX for Real Estate/HVAC, Hugo for Authority Blog/Learn) live in overlays — see `overlays/real-estate-content/` and `overlays/hugo-authority-content/` README for the skill names to activate.
