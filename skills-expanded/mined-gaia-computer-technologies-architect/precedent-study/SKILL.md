---
name: precedent-study
description: "Build a structured precedent / case-study analysis for a design problem — comparative frames (plan, section, circulation, light, structure, climate) and the transferable rules you can reuse. Use when an architect wants \"precedents\", \"reference projects\", \"case studies\", or \"what have others done with [problem]\". CRITICAL: language models fabricate project names, architects, dates, and citations, so this skill grounds every precedent in retrieval or user-supplied projects, flags every specific attribution as needs-verification, and never invents a building."
license: MIT
metadata:
  author: Gaia Computer Technologies, Inc.
  version: "1.0.0"
---

# Precedent Study

Precedent is how architects think: you learn a strategy from a building that solved a related problem, and you carry the *rule*, not the picture. This skill produces a disciplined precedent analysis — comparative, structured, and honest about what it can and cannot vouch for.

## Read this first: the fabrication problem

Language models invent precedents with total confidence — real-sounding project names by real architects that don't exist, right buildings with wrong architects, plausible dates and areas that are simply made up. Studies of LLM citation find a large fraction of references fabricated or wrong. In architecture this is lethal to trust: an architect who repeats a confabulated precedent to a client or jury is embarrassed, and the tool that fed it to them is worthless.

So this skill runs on a strict discipline:

1. **Prefer projects the architect already named,** or that you can retrieve and verify. If web search / fetch tools are available in the session, use them to ground every project — confirm the name, architect, location, and date against a real source, and cite it.
2. **If you cannot verify a project, do not name it.** Describe the *strategy* generically ("a courtyard house that turns a blank street face and opens entirely inward") rather than risk a fabricated attribution.
3. **Flag every specific claim.** Architect, year, area, cost, span, client — mark each as `[verify]` unless it came from the user or a cited source. Better a study full of honest `[verify]` tags than one clean-looking lie.
4. **Never fabricate a citation, award, publication, or quote.** If you don't have the source, say so.

The architect's own knowledge is the backstop. Your job is to structure and extract, not to be the database of record.

## When to use

- Starting a project type the architect wants references for.
- Testing a design move against how others have handled it.
- Building the precedent page of a concept deck or competition board.

## Input

- The design problem or type ("naturally lit deep-plan library," "housing on a steep north slope," "adaptive reuse of a grain silo").
- Any precedents the architect already has in mind (best case — these are trusted).
- The lens that matters most (light? section? circulation? structure? climate?).

## Process

1. **Frame the problem** as a transferable question, not a style ("how do you get daylight to the centre of a deep plan?" not "modern library please").
2. **Assemble precedents** — user-supplied first, then retrieved-and-verified. Aim for 3–5 genuinely comparable projects, not a scrapbook. If you can only stand behind two, give two.
3. **Analyse each on a consistent frame** so they're comparable: parti, plan strategy, section, circulation, light, structure/material, relationship to context and climate.
4. **Extract transferable rules** — the point of the whole exercise. From each precedent, name the one or two moves an architect could actually reuse, and the condition under which they work.
5. **Note what does NOT transfer** — the site, budget, era, or code context that made it work there and might not here.
6. **Cite or flag everything.** Sources where you have them; `[verify]` where you don't.

## Analytic frame (per precedent)

- **Project** — name, architect, location, year — each `[verify]` unless sourced or user-given.
- **The move** — the one strategy this project is a precedent *for*.
- **Plan & section** — how space is organised in both dimensions.
- **Light** — where it comes from and what it does.
- **Circulation** — how you move through; the sequence.
- **Structure / material** — the tectonic logic, if relevant to the lesson.
- **Transferable rule** — what you'd carry to the current project.
- **What made it site-specific** — what you can't carry.

## Output format

```
## Precedent Study — [the problem, as a transferable question]

> Sourcing note: [which projects are user-supplied / retrieved-and-cited / described generically because unverifiable]

### [Project name [verify]] — [architect [verify]], [location, year [verify]]
- **Precedent for:** [the single move]
- **Strategy:** [plan / section / light / circulation, as relevant]
- **Transferable rule:** [what to reuse, and when it works]
- **Doesn't transfer:** [the site/budget/era condition that was local to it]
- **Source:** [citation, or "unverified — architect to confirm"]

### [next precedent] ...

### Rules to carry into the project
1. [transferable rule, attributed to the precedent it came from]
2. ...
```

## What you don't do

- Don't invent projects, architects, dates, areas, or citations. Ever. Describe the strategy generically before you risk a fabricated name.
- Don't present unverified specifics as fact. Tag them `[verify]`.
- Don't collect pictures. Extract rules. A precedent with no transferable lesson doesn't belong.
- Don't mimic the precedent's *style* — that's how precedent study degrades into pastiche. Carry the logic, not the look.
- Don't pad to a number. Three verified precedents beat six half-remembered ones.
