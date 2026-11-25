---
name: vc-diligence
description: An exhaustive, 1000-line enterprise-grade Venture Capital due diligence skill. Provides a massive, multi-stage workflow covering deep technical research, precise search methodologies, legal/commercial risk auditing, report synthesis, and advanced Excalidraw visual argumentation for any industry.
---

# VC Diligence Skill: The Ultimate Lead Partner Framework (V26 - Master Synthesis & Serper Edition)

This is the definitive handbook for executing the `vc-diligence` skill. It combines **Recursive Hypothesis-Driven Discovery** with **Hyper-Depth Content Harvesting**, **Specialized Architecture Auditing**, **Product-Market Fit (PMF) Leveling**, and **Excalidraw Visual Mastery**. The goal is to produce an **intimate, 30+ page master audit** that identifies the technical plumbing, commercial moats, and legal red-flags of any startup.

## 0. PREREQUISITES & SETUP (CRITICAL)
Before executing this skill, ensure the following dependencies are installed to support diagram rendering:
1. **Python Playwright**: `pip install playwright`
2. **Browser Binaries**: `npx playwright install chromium`
3. **Internal Renderer**: This skill depends on the `excalidraw-diagram` skill's renderer located at `/Users/harrisonluo/.agents/skills/excalidraw-diagram/references/render_excalidraw.py`.
4. **Specialized Agents**: 
    - Use `architecture-auditor` for Phase 4 & 10.5 (Technical Teardown).
    - Use `excalidraw-diagram` for Phase 12 (Diagram Generation).
5. **API Keys**: Ensure `SERPER_API_KEY` is available in the environment for high-fidelity image discovery.

---

## 1. THE "HYPER-DEPTH" ANALYST MINDSET

### 1.1 The 30-Page Master Mandate
A brief summary is a failure. You are building an exhaustive legal and commercial case.
- **The Isomorphism Principle**: Diagrams must convey business logic through structure, not just labels. If you remove the text, the shape should still be the meaning.
- **The Education Test**: Could someone learn something concrete from the diagram? It must show actual formats, real event names, and concrete examples.
- **The Traceability Rule**: Every claim MUST be backed by a link or raw finding file.
- **Fact-Dense Writing**: Omit fluff. Use metrics, specific library names, and exact pricing.
- **Exhaustive Extraction**: Use `web_fetch` on 10-20 sources per wave. **Snippets are insufficient.** You MUST extract full text to construct detailed feature breakdowns.
- **The Search-to-Fetch Ratio**: For every Turn that includes a `google_web_search`, you MUST execute a corresponding `web_fetch` Turn for the top 3-5 high-signal results.

### 1.2 The "Proxy Research" Principle
If direct information about a startup is scarce (e.g., stealth), you MUST research the **ecosystem proxies**:
- **Technology Proxies**: Research the benchmarks of the specific tools/frameworks they use.
- **Personnel Proxies**: Research the "Success Patterns" of the companies the founders came from.
- **Competitor Proxies**: Perform deep teardowns of incumbents to identify the *exact* "White Space" the startup is filling.

---

## 2. TABLE OF CONTENTS
1. [Phase 0: Workspace Architecture & Initialization](#3-phase-0-workspace-architecture--initialization)
2. [Phase 1: Objective-Oriented Recursive Search & Content Harvesting](#4-phase-1-objective-oriented-recursive-search--content-harvesting)
3. [Phase 2: MCP Service Discovery & Third-Party Intelligence](#5-phase-2-mcp-service-discovery--third-party-intelligence)
4. [Phase 3: The Founder Alpha & Team Audit](#6-phase-3-the-founder-alpha--team-audit)
5. [Phase 4: Specialized Technical Teardown (Architecture Auditor)](#7-phase-4-specialized-technical-teardown-architecture-auditor)
6. [Phase 5: Product-Market Fit (PMF) Audit & Leveling](#8-phase-5-product-market-fit-pmf-audit--leveling)
7. [Phase 6: Commercial, Financial & Unit Economic Diligence](#9-phase-6-commercial-financial--unit-economic-diligence)
8. [Phase 7: Market Dynamics, Competitive Moats & Exit Benchmarks](#10-phase-7-market-dynamics-competitive-moats--exit-benchmarks)
9. [Phase 8: The 2025-2026 AI Impact & Industry Trend Analysis](#11-phase-8-the-2025-2026-ai-impact--industry-trend-analysis)
10. [Phase 9: The Master VC Diligence Questionnaire (Exhaustive)](#12-phase-9-the-master-vc-diligence-questionnaire-exhaustive)
11. [Phase 10: Legal, Regulatory & Governance Risk Auditing](#13-phase-10-legal-regulatory--governance-risk-auditing)
12. [Phase 11: Visual Asset Acquisition (Serper Image Search)](#14-phase-11-visual-asset-acquisition-serper-image-search)
13. [Phase 11.5: Formal Visual Design Specification](#145-phase-115-formal-visual-design-specification)
14. [Phase 12: Synthesis - Master Deliverables Protocol](#15-phase-12-synthesis---master-deliverables-protocol)
15. [Phase 12.5: The Iterative Master Expansion Step](#155-phase-125-the-iterative-master-expansion-step)
16. [Phase 12.6: Technical Context Gap-Filling (Deep Dive Expansion)](#156-phase-126-technical-context-gap-filling-deep-dive-expansion)
17. [Phase 13: Advanced Visual Argumentation (Skill Delegation)](#16-phase-13-advanced-visual-argumentation-skill-delegation)
18. [Phase 13.1: Visual Quality Assurance & Refinement Loop](#161-phase-131-visual-quality-assurance--refinement-loop)
19. [Phase 14: Formatting Audit (Tables vs. Bullets)](#17-phase-14-formatting-audit-tables-vs-bullets)
20. [Phase 15: Final Holistic Synthesis & Conviction Scoring](#18-phase-15-final-holistic-synthesis--conviction-scoring)
21. [Phase 16: Final Quality Assurance & Hand-off](#19-phase-16-final-quality-assurance--hand-off)

---

## 3. PHASE 0: WORKSPACE ARCHITECTURE & INITIALIZATION

```bash
mkdir -p diligence_[startup_name]/raw_findings/team
mkdir -p diligence_[startup_name]/raw_findings/tech
mkdir -p diligence_[startup_name]/raw_findings/market
mkdir -p diligence_[startup_name]/raw_findings/legal
mkdir -p diligence_[startup_name]/diagrams
mkdir -p diligence_[startup_name]/deliverables
mkdir -p diligence_[startup_name]/assets
```

---

## 4. PHASE 1: OBJECTIVE-ORIENTED RECURSIVE SEARCH & CONTENT HARVESTING

### 4.1 The Wave-Based Discovery Objectives (Hyper-Depth)

**Wave 0: Product DNA & User Persona (The Foundation)**
- **Central Question**: "What exactly is the product, how does it function for the end-user, and who are the core personas it serves?"
- **Guiding Mandate**: Understand the 'Jobs to be Done' before auditing the 'Right to Win'.
- **Discovery Specifics**: Feature inventory, user personas (Economic Buyer vs. Daily User), UX/Workflow mapping, and core value prop.
- **Example Evidence**: A 'How it Works' page; a user manual; onboarding tutorials; detailed customer testimonials.

**Wave 0.5: Product-Market Fit (PMF) Audit**
- **Central Question**: "At what level of PMF is this startup currently operating (Level 1–4), and what are the signals of satisfaction, demand, and efficiency?"
- **The PMF Method (First Round Framework)**:
    - **Level 1 (Nascent)**: Solving a problem for 3-5 customers. Qualitative: "The Grind."
    - **Level 2 (Developing)**: Scalable sales channel emerging. Qualitative: "Lite PMF."
    - **Level 3 (Strong)**: Floodgates open. Efficiency + GTM refinement. Qualitative: "The Geyser."
    - **Level 4 (Extreme)**: Categorical dominance. Global expansion.
- **Discovery Specifics**: Retention/Usage depth (Satisfaction), Sales velocity/Inbound (Demand), Magic Number/Burn Multiple (Efficiency).

**Wave 1: Identity, Trajectory & Capital Structure**
- **Central Question**: "Who is this company at its core, how much capital have they consumed, and what is their growth velocity?"
- **Discovery Specifics**:
    - **Legal Structure**: Identify parent entity, DBAs, and former names.
    - **Cap Table Proxies**: Hunt for funding announcements and SEC Form D filings.
    - **Hiring Velocity**: Search for "LinkedIn Headcount Growth" patterns or historical job postings.
- **Example Evidence**: A Press Release confirming funding rounds; a Crunchbase entry showing round intervals.

**Wave 2: Founder Alpha & Talent Density**
- **Central Question**: "Why is this specific team uniquely qualified to win this category, and what are their individual 'superpowers'?"
- **Discovery Specifics**:
    - **The 'Spike'**: Identify the world-class expertise of each founder (Academic, Serial, BigTech).
    - **Social Graph**: Search for testimonials, board seats, or past managers.
    - **Conflict/Cohesion**: Find evidence of past collaboration (worked together at X for Y years).
- **Example Evidence**: Google Scholar profiles; LinkedIn recommendations; academic publication history.

**Wave 3: Technical Architecture & Product Moat**
- **Central Question**: "Exactly how is this built, where are the structural bottlenecks, and is it a defensible moat or a thin wrapper?"
- **MANDATORY**: Use `web_fetch` on all technical docs, API references, and engineering blogs found. Build a component-by-component feature teardown.
- **Discovery Specifics**:
    - **Infrastructure Stack**: Identify the 'Plumbing' (AWS/GCP, DBs, LLM providers).
    - **Proprietary IP**: Search for internal project names, custom protocols, or patents.
    - **Performance Benchmarks**: Hunt for latency, throughput, or accuracy metrics.
- **Example Evidence**: API references; GitHub dependency audits; technical whitepapers.

**Wave 4: Market Dynamics & Competitive Displacement**
- **Central Question**: "Which $B+ market is being eaten, who are the incumbents being displaced, and what are the exit benchmarks?"
- **The Synthesis Mandate**: Do NOT search for "TAM SAM SOM." Search for **Atomic Facts**:
    - **Market Size Proxies**: "Total number of [Target User Profile]" or "Total addressable market of [Industry Sector]".
    - **Pricing Proxies**: "[Competitor] pricing" or "[Incumbent] revenue per user".
    - **Adoption Proxies**: "[Competitor] customer count".
- **Hypothesis-First (MANDATORY)**: Based on Waves 1-3, define the *disrupted market* and name the *likely incumbents* and *emerging challengers*.
- **Discovery Specifics**:
    - **Incumbent Vulnerability**: Search for "Negative Reviews" or "Integrations Issues" with incumbents.
    - **Category Pricing**: Hunt for competitor pricing pages or 'Talk to Sales' leakages.
    - **Exit Comps**: Find 3-5 recent M&A deals in the sector.
- **Example Evidence**: A Forrester Wave report showing the incumbent's market share is declining; an M&A deal at a 12x revenue multiple.

### 4.2 Query Fanout Mandate
For every Central Question or Hypothesis, you MUST generate a **fanout of 3-5 distinct, multi-angle queries**.
- **Angle 1: Direct Discovery**: (e.g., `\"[Startup] [Topic]\"`)
- **Angle 2: Proxy Signals**: Search for indirect evidence (e.g., `\"[Topic] reviews\"`, `"hiring for [Topic]"`).
- **Angle 3: Technical/Source-Specific**: Target deep sources (`site:github.com`, `filetype:pdf`).
- **Angle 4: Competitive/Market Context**: (e.g., `\"[Startup] vs [Competitor]\"`).

### 4.3 The Search Critic & Intent SOP (Least-to-Most Protocol)
Before executing ANY query, apply **Least-to-Most Prompting**:
1. **Decomposition**: "Break the Central Question down into the fundamental sub-questions that need to be answered first."
2. **Sequential Solving**: "Solve each sub-question one by one, using the answer from the previous step to inform the next search angle."
3. **The 'Reasonable Searchability' Check**: Search for the **atomic ingredients** instead of the **finished meal**.
4. **The Search-to-Fetch Mandate**: For each query fanout, identify the top high-signal URLs and execute `web_fetch`.

---

## 5. PHASE 4: SPECIALIZED TECHNICAL TEARDOWN (ARCHITECTURE AUDITOR)

**CRITICAL DELEGATION**: For this phase, you MUST activate the `architecture-auditor` skill.

1.  **Harvest Ingredients**: Collect real API names, JSON schemas, and method calls to prove the depth of integration.
2.  **Audit Moat**: Use the `architecture-auditor` specialist to perform the "Wrapper vs. Moat" test.
3.  **Feature Teardown**: Draft the detailed component-by-component analysis for the final report.

---

## 6. PHASE 5: PRODUCT-MARKET FIT (PMF) AUDIT & LEVELING

You MUST apply the **First Round Capital PMF Method** to determine the company's trajectory.

### 6.1 The 3 Dimensions of PMF
1. **Satisfaction**: Audit customer reviews, developer forums (Discord/Reddit), and case studies. Are they "Friend-zoned" (like but don't need) or is it a "Painkiller"?
2. **Demand**: Search for inbound interest signals, waiting lists, and pricing power (ability to raise prices without churn).
3. **Efficiency**: Calculate/Model the Magic Number, Burn Multiple, and CAC Payback based on revenue vs. headcount growth.

### 6.2 The 4 Levers (The 4Ps) Evaluation
If the company is stuck between levels, identify which lever they are pulling:
- **Persona**: Moving upmarket or changing the ICP.
- **Problem**: Pivoting to a more urgent/important problem.
- **Promise**: Refining the unique value prop.
- **Product**: Feature iteration to meet the promise.

---

## 7. PHASE 10.5: FORMAL VISUAL DESIGN SPECIFICATION (FACT-DENSE)

Before creating Excalidraw diagrams, you MUST write a **Visual Design Specification** that formalizes the argument. Use the `architecture-auditor` skill to ensure the spec is technical and accurate.

### 7.1 The Research Mandate (Visual Ingredients)
For each diagram, you must list the **Evidence Artifacts** discovered in research:
- **Architecture**: List the actual API endpoints, event names, and model names.
- **Market**: List the specific market share percentages and incumbent names.
- **Economic**: List the exact ARR milestones and gross margin percentages.

---

## 8. PHASE 11: VISUAL ASSET ACQUISITION (SERPER IMAGE SEARCH)

If `google_web_search` fails to provide direct image URLs, you MUST use the **Serper API** for high-fidelity image discovery.

### 8.1 Serper Image Discovery SOP
1. **Search Protocol**: Use `run_shell_command` to call the Serper Images API.
2. **Command Template**:
```bash
curl -X POST 'https://google.serper.dev/images' \
  -H "X-API-KEY: $SERPER_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"q": "[Founder Name] [Company] headshot", "num": 10}'
```
3. **URL Extraction**: Identify the `imageUrl` from the JSON response.
4. **Download & Verification**: Follow the standard `curl -Lfg` and `file` check protocol.

---

## 9. PHASE 12: SYNTHESIS - THE MASTER DELIVERABLES PROTOCOL

### 9.1 `full_diligence_report.md` (The 30+ Page Master Audit)
- **Header 1: Executive Summary** (3-paragraph distillation).
- **Header 2: Company Profile & Core Product** (Legal names, pivots, exhaustive feature list with sub-bullets).
- **Header 3: Product-Market Fit Audit** (Satisfaction/Demand/Efficiency dimensions, PMF Level 1-4 verdict).
- **Header 4: The Founder Alpha Audit** (Complete histories, social graphs, citations, and links).
- **Header 5: Financing & Capital Structure** (Round-by-round partners, valuations, board composition).
- **Header 6: Detailed Technical Architecture** (Plumbing, stack choices, bottlenecks, "Wrapper vs. Moat" test).
- **Header 7: Market & Competitive Landscape** (TAM/SAM/SOM synthesis, incumbent weaknesses, displacement economics table).
- **Header 8: Commercials & Unit Economics** (GTM strategy, LTV/CAC modeling, churn analysis).
- **Header 9: Legal, Regulatory & Governance** (IP provenance, compliance status).
- **Header 10: Master Research Appendix** (Categorized links and full source citations).
- **Header 11: Final Investment Verdict** (Detailed rationale explaining the "Why").

---

## 10. PHASE 12.5: THE ITERATIVE MASTER EXPANSION STEP (MANDATORY)

Once the initial draft of the `full_diligence_report.md` is complete, you MUST execute this iterative expansion cycle:
1. **Section Elaborator**: Add at least 3-5 verbose paragraphs per major section.
2. **Structural Depth**: Convert flat lists into hierarchical structures with H3/H4 sub-headings and nested sub-bullets.
3. **Citation Check**: Ensure every factual claim has a corresponding source link (3-5 links per section).

---

## 11. PHASE 12.6: TECHNICAL CONTEXT GAP-FILLING (DEEP DIVE EXPANSION)

After generating the initial draft of the `technical_commercial_deep_dive.md`, you MUST perform a **Technical Gap Audit**:

1.  **Identify "Thin" Sections**: Scan the document for generic technical descriptions (e.g., "They use cloud infrastructure").
2.  **Reissue Deep Searches**: Execute 3-5 high-resolution queries specifically targeting missing primitives identified in research:
    - **Specific Algorithms**: "Does [Startup] use [Specific Algorithm X] or [Variant Y]?"
    - **Infrastructure Quirks**: "Is [Startup] on AWS Bedrock or using raw EC2 H100s?"
    - **Data Flow Detail**: "What is the specific JSON payload for the [X] endpoint?"
3.  **Future Diligence Mapping**: Add a "Technical Diligence Roadmap" section at the end of the Deep Dive, suggesting exactly where a future technical auditor should look (e.g., "Audit the specific weights of the Layer 4 aggregator").
4.  **Inject Detail**: Expand the document by integrating these new findings into verbose paragraphs.

---

## 12. PHASE 13: ADVANCED VISUAL ARGUMENTATION (SKILL DELEGATION)

**CRITICAL MANDATE**: Do NOT attempt to generate Excalidraw JSON manually. Use the `activate_skill` tool to invoke the `excalidraw-diagram` skill.

1. **Invoke the Skill**: Pass your detailed `Visual Design Specification` to the `excalidraw-diagram` skill.
2. **Rendering**: After the skill generates the `.excalidraw` files, use the internal renderer to convert them to PNGs:
   - **Command**: `python3 ~/.agents/skills/excalidraw-diagram/references/render_excalidraw.py diligence_[startup]/diagrams/[filename].excalidraw`

---

## 13. PHASE 13.1: VISUAL QUALITY ASSURANCE & REFINEMENT LOOP

Once diagrams are initially generated and rendered as PNGs, you MUST perform a **Visual Audit**:

1.  **Rendering Check**: Inspect the PNG (or use `file` and `ls -lh`) to ensure it rendered correctly and contains text.
2.  **Logic Consistency**: Does the diagram match the **Isomorphism Principle**? Does the structure make sense without reading labels?
3.  **Refinement Round**: If the diagram is too crowded or lacks technical detail (failing the **Education Test**):
    - Update the **Visual Design Specification** with more granular box labels and specific technical primitives.
    - Re-delegate to the `excalidraw-diagram` skill.
    - Re-render the PNG.
4.  **Label Verification**: Ensure the **Two-Way Binding Rule** is strictly followed in the new version.

---

## 14. PHASE 15: FINAL HOLISTIC SYNTHESIS & CONVICTION SCORING

Before finalizing the hand-off, perform a **Holistic Global Analysis** across all generated documents.

### 14.1 The Conviction Scorecard
Assign a score (1-10) to the following dimensions based on the *entire* output:
1.  **Technical Moat**: (Is it a physics-based moat or a commodity wrapper?)
2.  **Founder Alpha**: (Do they have the "Right to Win" and "Grit Signals"?)
3.  **Market Urgency**: (Is this a "Painkiller" or a "Vitamin"?)
4.  **Capital Efficiency**: (What is their ARR-to-Burn ratio?)
5.  **Regulatory/Platform Resilience**: (Can they survive OpenAI or shifting laws?)

### 14.2 The "Red Team" Critique
Force the AI to argue *against* the investment for one paragraph. What is the single most likely reason this company fails?

### 14.3 Synthesis Statement
Construct a 3-paragraph final argument that weaves together the Architecture, PMF Level, and Capital Structure into a definitive Lead Partner verdict.

---

## 15. PHASE 16: EXCALIDRAW TECHNICAL REFERENCE & JSON PROTOCOL

To ensure diagrams are high-quality and correctly rendered, follow these strict JSON schema rules.

### 15.1 The Two-Way Binding Rule (CRITICAL)
Every text element inside a container MUST be bound correctly to prevent empty boxes.
1.  **Container (Rectangle/Ellipse/Diamond)**: Must have a `boundElements` array containing the text element's ID.
2.  **Text Element**: Must have a `containerId` property pointing to the parent shape's ID.

### 15.2 Semantic Color Palette
Use colors to encode meaning from `references/color-palette.md`:
- **AI/LLM**: Fill `#ddd6fe`, Stroke `#6d28d9`
- **Start/Trigger**: Fill `#fed7aa`, Stroke `#c2410c`
- **Success/End**: Fill `#a7f3d0`, Stroke `#047857`
- **Decision**: Fill `#fef3c7`, Stroke `#b45309`
- **Primary/Neutral**: Fill `#3b82f6`, Stroke `#1e3a5f`

---

## 16. FINAL QUALITY ASSURANCE & HAND-OFF

### 19.1 Hand-off
"Diligence complete. Overview Memo, Deep Dive, and 30+ page Master Audit (with full feature teardowns, iteratively expanded details, and specialized visual diagrams) are in `deliverables/`."

---
*End of VC Diligence Skill Masterclass V26.*
