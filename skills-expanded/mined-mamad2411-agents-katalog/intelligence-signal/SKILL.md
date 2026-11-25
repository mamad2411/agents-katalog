---
name: intelligence-signal
description: |
  Methodology for broad horizon-scanning and signal detection.

  [WHAT] Defines WHAT to scan and HOW results are valued.
  Execution happens via the intelligence-researcher agent.

  [WHEN] Use when: horizon scanning, signal detection, weak signals,
  peripheral scanning, early warning, trend spotting.

  [EXPERTISE] Signal detection, peripheral scanning, weak signals, trend analysis.

  Workflow: SIGNAL = methodology | Agent = research | STRUCTURE/CONTEXT/SYNTHESIS = analysis
argument-hint: [topic or region]
allowed-tools: Read, Grep, Glob, WebFetch, WebSearch
---

Horizon scan on: $ARGUMENTS

# SIGNAL — peripheral scanning

**Role:** methodology for broad information gathering.
**Execution:** use the `intelligence-researcher` agent to perform collection.
**Core principle:** breadth before depth.

## What to scan

### Geographic breadth
Global perspective without limitation. Actively look beyond the usual centers.
Include: Global South, Asia, Middle East, Africa, Latin America, etc.

### Domain breadth
Politics, geopolitics, economics, trade, tech, security, defense, climate, demography, migration, culture, values, health, energy, commodities, legal developments, science, civil society.

### Source-type breadth

| Type | Examples |
|------|----------|
| Academic | Peer-reviewed, research reports |
| Policy | Think tanks, government reports |
| International | UN, OECD, World Bank, regional bodies |
| Media | Mainstream + niche, multiple countries |
| Industry | Trade journals, patents, standards |
| Primary | Official statements, press releases |

## What to look for

### Weak signals and anomalies

- What breaks pattern or deviates
- Early indicators before they become trends
- Changes in language/rhetoric/framing
- New actors or constellations
- **Silences** — what should be there but isn't
- Converging signals from different directions

### Patterns to recognise

- Connections between unrelated events
- Same actors/methods/narratives across contexts
- Spillover between sectors/regions
- Emerging consensus or dissensus

## Early warning indicators

| Category | Indicators |
|----------|------------|
| Economy | Capital flows, investment patterns |
| Military | Positioning, exercises |
| Diplomacy | Relationships, rhetoric |
| Legal | Legislation, regulation |
| Tech | Capacity, application |
| Alliances | New collaborations, broken ties |
| Opinion | Public opinion, protest movements |

### Structural shifts

- Power shifts between countries/regions
- Norm shifts in international institutions
- Technological breakthroughs with broad impact
- Demographic trends
- Climate-related security implications

## Cognitive principles

| Counter | Prioritise |
|---------|------------|
| Confirmation bias | Primary sources over secondary |
| Geographic tunnel vision | Original reports over summaries |
| Recency bias | Primary data over interpretations |
| Expert bias | Full documents over excerpts |

**Always acknowledge:** knowledge gaps, information shortfalls, uncertainty.

## Agent output

The agent delivers in this structure:

```
SIGNAL_OUTPUT:
Question: [question]
Scan coverage: [geographies, domains, source types]
Main findings: [with source and date]
Weak signals: [what, where, why relevant]
Anomalies: [what is unexpected]
Conflicting reports: [where sources differ]
Knowledge gaps: [what couldn't be found]
Suggested deep dives: [where more is needed]
```

## Input/Output

| | Specification |
|---|---|
| **Input** | Question/topic from the user |
| **Output** | `SIGNAL_OUTPUT` (see above) |
| **Consumer** | STRUCTURE (analysis), CONTEXT (validation) |

## System integration

```
SIGNAL (methodology) → intelligence-researcher (executes) → STRUCTURE/CONTEXT → SYNTHESIS
```

**Tone:** boundlessly curious, systematically broad, alert to the unexpected.
