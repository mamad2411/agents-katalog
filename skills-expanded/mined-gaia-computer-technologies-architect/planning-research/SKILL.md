---
name: planning-research
description: Research a site's planning history, designations and applicable planning policy, and explain them in plain language with every item linked to its source and dated. Works across jurisdictions — UK (planning.data.gov.uk API, local authority planning portals and local plans), US (municipal zoning codes and open-data portals), EU and elsewhere (cadastres, zoning/land-use plans, municipal portals) — and asks which applies. Use when the architect wants "planning history", "site constraints", "is it in a conservation area", "what's the zoning", "which policies apply", "planning due diligence" or a "pre-app research pack". Extends site-context (which designs from supplied facts) with sourced retrieval; hands to regulation-navigator for building regulations and objection-response for consultation responses.
license: MIT
metadata:
  author: Gaia Computer Technologies, Inc.
  version: "1.0.0"
---

# Planning Research

Find out what the planning system already says about a site, and what it will ask of a proposal, before the design commits to anything. Every finding links to where it came from and when that source was last updated. A planning fact with no source is a rumour.

## When to use

- Feasibility or pre-application stage, before a design direction is set.
- Due diligence for a client buying or appraising a site.
- Preparing the planning context section of a design and access statement or planning statement.
- When site-context needs designations and policy it doesn't have yet.

## Input

- **Address, parcel/title reference, or coordinates** (and a site boundary if available).
- **Jurisdiction:** country, region/state, local planning authority or municipality. Ask; don't infer from a postcode alone.
- **Proposal in outline:** use, scale, height, number of units. Policy relevance depends on it.
- **What the architect already has:** previous applications, pre-app advice, title constraints.

## Process

1. **Confirm the jurisdiction and the planning system.** Plan-led discretionary (UK), zoning by-right with variances (much of the US), land-use plan plus building permit (many EU states), or other. The system decides which questions matter.
2. **Retrieve, don't recall.** Use web access or tools to query actual sources (see [references/sources.md](references/sources.md)). If you cannot retrieve a source, list it under "To retrieve" with where to find it. Never state a designation, zone, or policy from memory.
3. **Designations and constraints.** For each: what it is, whether the site is in or near it, the source and dataset date, and what it means for design. Typical families: heritage (listed buildings, conservation areas, historic districts, monuments), environmental (flood zones, protected habitats, tree protection), land-use zoning and overlays, height/view protection, Article 4 or equivalent removal of permitted development, airport/infrastructure safeguarding.
4. **Planning history.** Previous applications on the site and close neighbours: reference, description, decision, date, and why it matters (refusal reasons are design briefs in disguise). Link each record.
5. **Applicable policy.** The adopted development plan or zoning code, plus emerging plans and supplementary guidance. For each relevant policy: reference, plain-language summary, the requirement it places on this proposal, and the link and adoption date. Quote short policy wording only when retrieved.
6. **Implications for the design.** Translate the findings into moves and risks: what is likely acceptable, what needs justification, what would need a variance or departure, what evidence the authority will ask for (heritage statement, flood risk assessment, daylight study, transport statement).
7. **Flag what needs a planning professional or the authority.** Interpretation of policy weight, the status of emerging plans, and anything contested.

## Domain knowledge

- **Datasets lag reality.** National aggregated datasets (such as planning.data.gov.uk in England) depend on what each local authority has published. Always show the dataset date and say "confirm with [authority]" for anything decisive.
- **Policy weight varies.** An adopted plan outranks emerging policy and guidance; national policy may override local policy in some systems. Don't rank weight yourself. Present the hierarchy as the jurisdiction defines it and flag it for a planner.
- **Refusals teach more than approvals.** Read refusal reasons and appeal decisions on and near the site; they show what the authority cares about.
- **Zoning numbers need their definitions.** FAR/FSI, height, setbacks, and coverage depend on how the code measures them (from grade, to the eaves or ridge, gross or net). Quote the definition with the number.

## Output format

```
## Planning Research — [Address], [Authority], [Country]
Researched: [date]. Planning system: [discretionary / zoning / land-use plan + permit / other]

### Summary
[3–5 lines: the constraints that will shape the design most, and the main risk.]

### Designations and constraints
| Constraint | Site in / near / clear | Source (link) | Dataset date | Design implication |
|---|---|---|---|---|

### Planning history
| Reference | Description | Decision | Date | Why it matters | Link |
|---|---|---|---|---|---|

### Applicable policy
| Policy ref | Plan / code (adopted date) | Plain-language requirement | Relevance to proposal | Link |
|---|---|---|---|---|

### Zoning / envelope numbers (where applicable)
| Control | Value | How it's measured (per code) | Source |
|---|---|---|---|

### Implications for the design
- ...

### Likely submission requirements
- ...

### To retrieve / confirm with the authority
- [item] → [where / who]

> **Disclaimer:** AI-generated analysis for preliminary purposes only. All figures, standards, and references must be verified by a qualified professional before use in design, permitting, costing, contracts, or regulatory submission.
<!-- architect:requires-disclaimer -->
```

Copy the disclaimer exactly as shown, including the `<!-- architect:requires-disclaimer -->` line. That line is the machine-readable marker the plugin checks for, so keep it even in a chat reply.

## What you don't do

- Don't state any designation, zone, height limit, policy or application record you haven't retrieved or been given. Unknowns go under "To retrieve".
- Don't predict the outcome of an application or tell the client "this will be approved".
- Don't interpret contested policy weight or legal status. That belongs to a planning consultant, lawyer, or the authority.
- Don't present a dataset as current without its date.
