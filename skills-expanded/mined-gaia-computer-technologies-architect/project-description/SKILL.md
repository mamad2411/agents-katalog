---
name: project-description
description: Write portfolio, award entry, website, press release and social copy for a completed or ongoing architecture project, at 50, 150 and 400 words, from verified project facts only — credits, dates, location, areas, costs, photographers, collaborators. Asks for missing facts instead of inventing them and keeps a fact sheet that every sentence traces back to. Use when the architect wants a "project description", "portfolio text", "award submission", "press release", "website copy", "Dezeen/ArchDaily submission text", or "caption for a project post". Feeds bid-response with case-study copy; pairs with concept-narrative for the design argument.
license: MIT
metadata:
  author: Gaia Computer Technologies, Inc.
  version: "1.0.0"
---

# Project Description

Describe a real project so that a stranger understands what it is, why it matters, and who made it, without a single claim the practice can't stand behind. Project copy gets reused for years in bids, awards and press, so a wrong fact spreads.

## When to use

- A project is complete, or published at a milestone, and needs copy.
- An award entry, publication submission, or website update is due.
- A bid needs a short case study.

## Input

Build a fact sheet first. Ask for anything missing; never fill it in.

- **Identity:** project name, location (city, country), client (and whether they may be named), type, status (completed / on site / unbuilt), completion date.
- **Numbers:** area (state GIA/GFA/NIA and unit), number of units/rooms/seats, construction cost (only if the client permits), programme duration.
- **Credits:** architect, project team, structural, services, landscape, QS/cost consultant, contractor, photographer (with exact credit line), other collaborators.
- **Design facts:** materials, structural system, key moves, energy/carbon performance (with source and whether modelled or measured), certifications (only if awarded, with level).
- **The idea:** the one-sentence concept, ideally from the architect or from concept-narrative.
- **Audience:** portfolio, award jury (with criteria), press, website, social.

## Process

1. **Write the fact sheet** as a table, one fact per row, with its source (architect, drawings, client approval, certificate). Mark anything unconfirmed.
2. **Find the lead.** What is genuinely distinctive? A site condition, a client need, a constraint turned to advantage, a material, a performance result. One thing, not five.
3. **Write three lengths.**
   - **50 words:** what, where, for whom, the one idea.
   - **150 words:** add the site or brief problem, the key design response, one material or spatial detail.
   - **400 words:** add sequence and experience, construction and materials, performance (with basis), and credits.
4. **Tailor to the audience.** Award entries answer the jury's criteria in order. Press releases lead with news value and include a quotable line the architect has approved. Portfolio copy can be more personal. Social captions are one or two sentences plus credits.
5. **Trace every sentence.** Each factual claim must map to a fact-sheet row. Cut any that can't.

## Domain knowledge

- **Publications want facts in a standard block:** name, architect, location, completion year, area, client, photographer, and other credits. Supply it separately from the prose.
- **Performance claims need a basis.** "Designed to Passivhaus standard" differs from "certified Passivhaus". "Modelled EUI" differs from "measured EUI". Say which.
- **Photographer credits are contractual.** Use the exact credit line supplied.
- **Client confidentiality.** Some clients can't be named or costs can't be shown. Ask before including either.
- **Avoid archispeak.** "A dialogue with the landscape" says nothing. "The roof drops to 2.4 m at the boundary to keep the neighbour's garden in sun" says something.

## Output format

```
## Project Description — [Project name]

### Fact sheet
| Fact | Value | Source | Confirmed |
|---|---|---|---|

### Facts block (for publications)
Project: ... | Architect: ... | Location: ... | Completion: ... | Area: ... m² (GIA) | Client: ... | Photography: ...

### 50 words
...

### 150 words
...

### 400 words
...

### [Audience-specific variant: award / press / social]
...

**Missing facts (not used until confirmed):** ...
```

## What you don't do

- Don't invent any fact: no assumed area, cost, date, collaborator, award, certification, or performance figure.
- Don't put words in anyone's mouth. Quotes come from the architect or client, approved.
- Don't overclaim authorship. Credit collaborators as they were appointed.
- Don't use superlatives you can't prove ("the first", "the largest", "award-winning") without a source.
