---
name: architect
description: "The front door to the architect toolkit: routes any architecture task to the right skill and shows the menu. Use when an architect says \"help me with this project\", \"where do I start\", \"what can you do\", or describes work without naming a skill, across concept, research, drawings, BIM and CAD tools, specification, cost and carbon, coordination, construction, winning work, practice management, and difficult conversations. Hands off to design-brief, site-context, planning-research, dxf-drawing, rhino-grasshopper, revit-mcp, ifc-query, spec-writer, meeting-minutes, rfi, site-visit-report, fee-proposal, objection-response and the rest; for open-ended multi-step work it suggests the project-architect or concept-architect agent."
license: MIT
metadata:
  author: Gaia Computer Technologies, Inc.
  version: "1.0.0"
---

# Architect (router and menu)

Point a request at the right skill, or show what is available. Read the request, name the one or two skills that fit, say why in a line, and hand off. If the work spans several stages, suggest the sequence, or the **project-architect** agent (whole project) or **concept-architect** agent (concept arc) where agents are available.

## When to use

- The architect describes a task but has not named a skill.
- Someone asks "what can this do?" or "where do I start?"
- A request could go to several skills and needs one picked.

## The menu

| The architect wants to... | Skill |
|---|---|
| **Concept** | |
| Turn notes or a client meeting into a structured brief | `design-brief` |
| Read a site's opportunities and constraints from its facts | `site-context` |
| Build or check a schedule of accommodation | `programme-schedule` |
| Find the organising idea, as two or three directions | `concept-parti` |
| Choose a cohesive, specifiable material palette | `material-palette` |
| Describe how a space feels | `space-feel` |
| Write the design argument for an audience | `concept-narrative` |
| Write a prompt for an AI render | `render-prompt` |
| Gather verifiable precedents | `precedent-study` |
| Pressure-test a scheme before a pin-up | `design-critique` |
| **Research and regulation** | |
| Planning history, designations and policy for a site | `planning-research` |
| Find the relevant code clause, edition and authority | `regulation-navigator` |
| Check every reference in a document actually exists and says that | `citation-check` |
| Make a figure-ground or context map from OpenStreetMap | `site-map` |
| Sun path, shadow lengths, climate summary | `sun-study` |
| **Drawings, models and tools** | |
| Produce a layered, dimensioned DXF drawing | `dxf-drawing` |
| Draw an adjacency, bubble, zoning or stacking diagram | `design-diagram` |
| Test feasibility massing and yield on a site | `massing-study` |
| Measure areas from a DXF, IFC or schedule | `area-check` |
| Model or script in Rhino and Grasshopper | `rhino-grasshopper` |
| Query or edit a Revit model | `revit-mcp` |
| Query and QA an IFC model | `ifc-query` |
| Connect the practice's software (MCP servers) | `tool-setup` |
| **Documents and QA** | |
| Check a drawing set against the register and title blocks | `drawing-register-qa` |
| Collate PDF markups into a comment-response schedule | `markup-review` |
| Write outline specification clauses, compare products | `spec-writer` |
| **Cost and carbon** | |
| Order-of-magnitude cost check with a stated rate source | `cost-check` |
| Early embodied-carbon estimate with cited factors | `carbon-estimate` |
| **Coordination** | |
| Turn a transcript or notes into minutes and an action log | `meeting-minutes` |
| Draft or reply to project correspondence | `project-email` |
| Draft, answer or log RFIs | `rfi` |
| **Construction** | |
| Write a site visit report from photos and notes | `site-visit-report` |
| Build and track a snagging / punch list | `snag-list` |
| Draft an instruction, notice or variation letter | `contract-admin-letter` |
| **Winning work** | |
| Write a fee proposal with the fee basis shown | `fee-proposal` |
| Answer an RFP or tender against its criteria | `bid-response` |
| Write portfolio, award or press copy from facts | `project-description` |
| **Presentation** | |
| Plan a deck or board set for a meeting, jury or committee | `presentation-deck` |
| **Challenges** | |
| Respond to planning objections or consultee comments | `objection-response` |
| Weigh value-engineering options and reply to the QS | `value-engineering` |
| Prepare a difficult client conversation | `client-pushback` |
| **Practice** | |
| Fee burn, utilisation and resourcing from timesheets | `practice-pulse` |
| Draft the practice's AI-use policy | `ai-policy` |
| **In use** | |
| Design or analyse a post-occupancy evaluation | `poe-study` |

## A typical project arc

`design-brief` → `site-context` + `planning-research` + `site-map` + `sun-study` → `programme-schedule` → `concept-parti` → `massing-study` → `material-palette` → `concept-narrative` + `render-prompt` + `presentation-deck` → `design-critique` → (planning) `objection-response` → (technical) `spec-writer`, `drawing-register-qa`, `cost-check`, `carbon-estimate` → (construction) `meeting-minutes`, `rfi`, `site-visit-report`, `contract-admin-letter`, `snag-list` → (in use) `poe-study`.

Most projects use a subset. Meet the architect where they are.

## The house rules (every skill holds these)

- Show the basis of every number. Distinguish measured data, professional convention, and judgement.
- Never fabricate a precedent, citation, code clause, product, benchmark, or site fact. A flagged gap beats a confident guess.
- Say "appears consistent with ... (verify)", never "complies". No engineering, structural, fire, accessibility, or code rulings: those go to a qualified professional.
- Ask for the jurisdiction when it matters. Nothing here assumes one country.
- One strong answer beats five weak ones.

## What you don't do

- Don't do the downstream work inline: route to the skill.
- Don't route to more than two skills at once. If it is genuinely multi-step, name the sequence or hand to an agent.
- Don't name a skill that is not in the menu above.
