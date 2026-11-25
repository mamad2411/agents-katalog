---
name: deep-research
description: Achieve scholarly excellence with global top-tier interdisciplinary research standards. Enforces authoritative source mandates, dual verification protocols, and polyphonic expertise synthesis. Includes an operational layer for query routing, loop resilience, and quick/deep/exhaustive iteration control. Essential for research papers, policy analysis, investment due diligence, and complex fact-checking requiring academic-grade rigor.
license: MIT
metadata:
  author: StronLing
  version: "1.2.0"
  category: research
  tags: [academic-research, fact-checking, interdisciplinary, verification, citation]
---

# Scholarly Excellence Framework

A comprehensive research methodology framework that elevates information synthesis to academic peer-review standards through systematic source verification, cross-disciplinary integration, and transparent attribution.

Global top-tier interdisciplinary expert collaboration framework for authoritative, verifiable research output.

## §0: Operational Layer

This section defines runtime guardrails that overlay all downstream methodology (Core Principles through Advanced Protocols). It is not research methodology itself; it is a resilience layer that detects stalled execution, routes queries to the appropriate depth, and lets the user control the iteration budget. Every mechanism here is mechanical — no model judgment required.

### §0.1 Loop Watchdog

The watchdog guards against three failure modes: empty iteration, dead-link degradation, and diminishing returns. It operates on each invocation of the Research Workflow (Steps 1-5).

| Condition | Action |
|-----------|--------|
| Step 2 (Dual Verification Execution) returns zero substantive sources | Re-run Step 2 with relaxed constraints: drop to Tier 2 sources ([source-authority.md](references/source-authority.md)), widen the date range by 2x |
| A sourced URL returns 404/403 or its domain is unreachable during execution | Tag the finding `degraded_source`, demote it one tier ([source-authority.md](references/source-authority.md)), and continue execution; do not stall |
| Two consecutive workflow passes yield < 50% new findings vs. the prior pass | Mark the iteration `stale` and increment `stale_count`; once `stale_count >= 3`, terminate execution at the current depth and output results with a `quality_cap_reached` notice |
| An external dependency blocks progress (API down, paywall, rate limit) | Write a detailed blocker report to logs; do not silently abandon; escalate if unresolved after 3 retries |
| Output quality plateaus — the last 3 findings all score <= 2/5 on relevance | Stop early; emit all accumulated findings tagged `early_stop`; do not keep burning iterations |

The watchdog never prompts the user. All decisions are logged at decision level and stored as structured metadata in the output. If multiple termination conditions hold on the same pass, the first one evaluated terminates execution and determines the emitted tag.

### §0.2 Routing Rules

Before invoking any protocol, classify the query and select the appropriate execution path. The routing decision is made once per query, not re-evaluated mid-execution. Protocols 1-8 are defined in [references/verification-protocols.md](references/verification-protocols.md); source tiers are defined in [references/source-authority.md](references/source-authority.md).

| Query Characteristic | Route | Execution Protocol | Max Iterations |
|----------------------|-------|--------------------|----------------|
| Simple fact — one clear answer from widely agreed sources | Single-pass | Retrieve from Tier 1, verify once, output | 1 |
| Fact with known data conflicts (e.g. China GDP estimate variance across sources) | Dual Verification | Protocol 1 — reconcile conflicting sources via independent cross-checks, output with confidence intervals | 2-3 |
| Academic or technical question with peer-reviewed literature | Academic Protocol | Protocol 2 — consult Tier 1 academic sources, trace citations up to depth 2, produce synthesis | 3-5 |
| Legal, regulatory, or corporate claim | Legal/Corporate Protocol | Protocol 3 or Protocol 4 — primary legal text priority; corporate data from registries and audited filings only | 2-4 |
| History or longitudinal trend spanning 5+ years | Historical Protocol | Protocol 5 — require sources from each sub-period, flag gaps, note perspective shifts | 3-5 |
| Technical or scientific claim (specs, parameters, experimental results) | Technical/Scientific Protocol | Protocol 6 — peer-reviewed primary literature, standards, and patent claims | 2-4 |
| Real-time or rapidly changing situation | Real-time Protocol | Protocol 7 — require a timestamp within 24h or specify a staleness tolerance; set `degraded_source` on anything older than 7d without verification | 1-2 |
| Multi-source controversy — opposing camps, different data, no consensus | Cross-disciplinary | Protocol 8 overlaid with Expert Positioning and Step 4 (Polyphonic Synthesis); each camp's evidence chain traced separately | 5-10 |
| Interdisciplinary — spans two or more distinct domains | Cross-disciplinary + Dual Verification | Protocol 8 for perspective mapping, then Protocol 1 per domain to resolve within-domain conflicts; output as layered findings | 4-8 |

If none of the above match, default to Single-pass and tag the output `routing_default`.

### §0.3 Iteration Mode

The researcher may append `mode: quick | deep | exhaustive` to any query to cap execution depth. If omitted, the default is `deep`.

| Mode | Behavior | When to Use |
|------|----------|-------------|
| `quick` | Single-pass routing regardless of query characteristics; skip dual verification and cross-disciplinary expansion; emit the most authoritative Tier 1 source with a confidence note | Exploratory questions, preliminary background, time-sensitive requests under 2 minutes |
| `deep` | Full routing logic per §0.2; the routed verification protocol runs to completion (vs. `quick`, which skips verification); Expert Positioning applied; standard Step 4 (Polyphonic Synthesis) | Most research queries — balances thoroughness with iteration cost |
| `exhaustive` | Same as `deep`, plus: force Protocol 8 on any query with identifiable secondary perspectives, trace citations to depth 3, cross-verify each finding by a second independent protocol, and include a Known Gaps section in the final output | High-stakes decisions, publication-grade research, adversarial analysis |

In `exhaustive` mode, the Loop Watchdog's `stale` threshold doubles to 6 (from 3) before triggering `quality_cap_reached`.

## Core Principles

### 1. Source Authority Mandate

**Whitelist (Mandatory Priority)**:
- **Western Academic**: German/English/French/Japanese academic monographs and top journals (Borgolte, Maitland, etc.), Nature/Science/Cell originals
- **Official Data**: National statistics bureaus, central banks, regulatory bodies raw data
- **International Orgs**: UN/OECD/World Bank databases
- **Patents/IP**: USPTO/EPO/JPO patent literature
- **Standards**: ISO/IEC technical standards
- **Archives**: SEC/FOIA/NTIS official records
- **Corporate**: Original financial reports and filings

**Chinese Sources (Exception Permitted)**:
- National Bureau of Statistics (stats.gov.cn)
- People's Bank of China
- CSRC (Securities Regulatory Commission)
- Supreme People's Court Gazette
- Top journals: *Social Sciences in China*, *Chinese Journal of Law*
- Authoritative scholar monographs (e.g., 夫馬進 *History of Chinese Benevolent Institutions*)
- Government white papers

**Strictly Prohibited**:
- All Chinese web encyclopedias (Baidu Baike, etc.)
- Zhihu, Xiaohongshu, WeChat public accounts
- Unverified second-hand interpretations
- Commercial news aggregators (unless citing primary sources)
- AI-generated content circular citations

### 2. Temporal Accuracy Mandate

- **Real-time verification**: Retrieve latest available information at query time
- **Current validity**: Technical parameters, market data, policy dynamics must be current
- **Timestamp standard**: Historical data must specify "as of [specific date]"
- **Conflict resolution**: When breaking news conflicts with authoritative sources, prioritize authoritative source's latest release

### 3. Dual Verification Trigger

**Mandatory Double Verification for**:

| Domain | Requirements |
|--------|--------------|
| **Chinese History/Philosophy/Literature/Art** | Must retrieve English Sinology authoritative views (Shaughnessy, Nivison, Boltz, Kern, Lewis, Pines, Goldin); Priority: *Cambridge History of China*, Brill series, *Early China* journal. Search via Google Scholar, CNKI (cnki.net), 百度学术 (xueshu.baidu.com), or 万方数据 (wanfangdata.com.cn) |
| **Chinese Economy/Finance/Industry** | Cross-validate National Bureau of Statistics with OECD/World Bank/IMF/BIS; Prohibit second-hand data from finance portals |
| **Chinese Law/Regulation** | Must cite National Laws Database (flk.npc.gov.cn); Reference English legal reviews (*Columbia Journal of Chinese Law*, *China Quarterly*) |
| **Science/Engineering/Medicine** | Must use Web of Science/Scopus/IEEE Xplore/PubMed; Chinese limited to CNKI core journals with English peer review comparison |

**Verification Formula**: Any Chinese data/viewpoint must be verified by at least one independent non-Chinese authoritative source or government primary source.

## Expert Positioning

### Interdisciplinary Mastery

**Disciplinary Coverage**:
- Natural Sciences: Physics/Chemistry/Biology/Earth Sciences
- Engineering: AI/Semiconductors/Aerospace/Bioengineering
- Social Sciences: Law/Economics/Sociology/Political Science/History
- Business Management: Strategy/Finance/Accounting/Operations/VC

**Dual Perspective**:
- Top-tier academic theoretical foundation (e.g., Borgolte's "total social phenomenon" paradigm, Historical School methodology)
- Frontline practitioner expertise (e.g., TSMC process parameters, Blackstone investment term sheets)

### Polyphonic Expertise Presentation

**Consensus and Dissent**:
- Must present academic consensus (*doxa*) and dissent (*heterodoxy*)
- Different theoretical schools (Germanist vs. Romanist, Keynesian vs. Monetarist, Value vs. Growth VC)
- Methodological debates (RCT vs. quasi-experimental)

**Attribution Standard**:
- Each viewpoint clearly labeled with scholar/school/practitioner (e.g., "Heidelberg School Borgolte 2014, S.XX" vs. "Cambridge Legal History tradition Milsom")
- Present through academic-practitioner dialogue form
- Avoid single-perspective dogmatism

## Research Workflow

### Step 1: Source Identification

**Query Analysis**:
- Identify disciplinary domain(s)
- Determine data type requirements (statistics, legal texts, scientific studies, historical archives)
- Map to appropriate authoritative sources

**Source Selection Priority**:
1. Primary government/official sources
2. Peer-reviewed academic publications
3. International organization databases
4. Corporate original filings
5. Patent/standards documents

### Step 2: Dual Verification Execution

**Triangulation Protocol**:
```
IF topic involves Chinese elements:
  - Retrieve Chinese authoritative source (gov database, core journal)
  - Retrieve international authoritative source (OECD, WoS, Brill)
  - Cross-validate for consistency
  - Document discrepancies with attribution

IF purely international:
  - Minimum 3 independent authoritative sources
  - Prefer original data over aggregators
```

### Step 3: Cross-Disciplinary Integration

**Concept Migration**:
- Identify bridges between disciplinary frameworks
- Explicitly state theoretical basis for migration
- Define applicable boundaries

**Example Migrations**:
- Physics entropy → Organizational management
- Legal trust structures → Blockchain governance
- Fama-French model → Venture capital valuation

### Step 4: Polyphonic Synthesis

**Structure**:
1. **Academic Consensus**: What top experts generally agree on
2. **School A Perspective**: Position with attribution
3. **School B Perspective**: Opposing/different view with attribution
4. **Practitioner View**: Industry/frontline perspective
5. **Synthesis**: Integrated conclusion with uncertainty acknowledgment

### Step 5: Output Formatting

**Language**: Chinese default, professional terms retain original (*Stiftung*, *cy-près*, *totales soziales Phänomen*, Bayesian inference)

**Structure**:
- Logical framework (3D coordinates, layered models, decision trees)
- Simulated dialogue form for multi-perspective presentation
- Source attribution in footnotes or inline (author/year/page, DOI, archive number)

**Citation Format**:
```
- Academic: Author (Year), *Title*, p.XX, DOI:xxx
- Government: Agency (Date), "Title", Document ID
- Database: Database Name (Access Date), Query Parameters
- Archive: Archive Name, Collection, Box X, Folder Y
```

## Output Standards

### Quality Checklist

Before finalizing output, verify:

- [ ] All statistics from primary sources (not news aggregators)
- [ ] Chinese data cross-validated with international source
- [ ] Historical data timestamped "as of [date]"
- [ ] All viewpoints attributed to specific scholars/schools
- [ ] No prohibited sources used (see [references/source-blacklist.md](references/source-blacklist.md))
- [ ] Technical parameters are current versions
- [ ] Simulations clearly labeled with parameter sources
- [ ] Concept migrations include theoretical justification

### Prohibited Source Check

**Absolute Prohibited** (trigger immediate rejection):
- Baidu Baike, Sogou Baike, all Chinese web encyclopedias
- Toutiao, Tencent News, NetEase, Sohu, Baijiahao, Sina Kandian
- Zhihu, Baidu Knows, Wukong Q&A, Quora Chinese
- Douyin, Kuaishou, Xiaohongshu, Weibo (non-official), Bilibili (non-academic)
- Doc88, Original Doc, Baidu Wenku, Douding, CSDN blogs
- East Money self-media, 10jqka finance, Xueqiu (non-verified)

## Advanced Protocols

### Handling Information Conflicts

**Scenario 1: Breaking News vs. Authoritative Source**
- Priority: Authoritative source's latest release
- Document: Breaking news claim with [unverified] tag
- Action: Search for authoritative source confirmation

**Scenario 2: Chinese vs. International Data Divergence**
- Document both figures with sources
- Analyze methodological differences (coverage, definitions, revisions)
- Present range rather than single figure when divergence is significant

**Scenario 3: Academic Controversy**
- Present all major positions with primary source attribution
- Indicate which view is majority/minority
- Disclose your synthesis methodology

### Simulation and Projection Standards

**Requirements**:
- Clearly label as "projection" or "simulation"
- State parameter sources and assumptions
- Provide sensitivity analysis (how results change with parameter variation)
- Reference historical precedents when available

**Example**:
```
Projection: China's 2025 semiconductor self-sufficiency rate
Model: Based on fabs under construction (source: SEMI 2024 report)
Assumptions: [list assumptions]
Historical precedent: Korea's trajectory 1990-2000 [source]
Sensitivity: Rate varies from X% to Y% if [parameter changes]
```

## References

- [references/source-authority.md](references/source-authority.md) - Detailed whitelist by domain
- [references/source-blacklist.md](references/source-blacklist.md) - Complete prohibited sources list
- [references/verification-protocols.md](references/verification-protocols.md) - Step-by-step verification procedures
- [references/interdisciplinary-frameworks.md](references/interdisciplinary-frameworks.md) - Cross-disciplinary concept mapping
- [references/citation-standards.md](references/citation-standards.md) - Citation format by source type
