---
name: research-pilot
description: >
  Interactive guided research assistant — iteratively refines a research question,
  builds a source list, and co-pilots the user through structured synthesis. Use
  when the user wants to conduct structured research interactively, refine a
  research question collaboratively, or produce a literature review or structured
  report with user steering at each step.
---

## Overview

ResearchPilot turns Claude into a research co-pilot. Rather than one-shot searching, it conducts research as a dialogue: scoping the question, suggesting angles, fetching sources incrementally, and letting the user steer which threads to pursue before synthesizing findings.

## Usage

Invoke with `/research-pilot` followed by a topic or question:

```
/research-pilot "LLM evaluation benchmarks for reasoning tasks"
/research-pilot "Climate adaptation strategies for coastal cities"
```

## Workflow

### Phase 1 — Scope
Asks 2–3 targeted questions to nail down scope, audience, and depth. Produces a one-paragraph research brief for user confirmation before searching.

### Phase 2 — Map
Generates a structured outline of sub-topics and suggests 4–6 search angles. User selects which to pursue (all by default).

### Phase 3 — Search & collect
Runs searches per approved angle. For each: fetches top 3 sources, extracts key claims, flags conflicting findings, and asks the user if they want to go deeper on any thread.

### Phase 4 — Synthesize
Writes a structured report (executive summary → sections per sub-topic → conflicts & gaps → conclusion) with inline citations. User can request rewrites per section before finalizing.

## Commands during a session

| Command | Effect |
|---------|--------|
| `go deeper on <topic>` | Adds another search round for that sub-topic |
| `skip <topic>` | Drops a sub-topic from the outline |
| `focus on <aspect>` | Narrows the next search batch |
| `draft now` | Skips remaining searches and synthesizes from what's collected |
| `restart scope` | Returns to Phase 1 with a revised question |

## Notes

Best for literature reviews, competitive analyses, and structured reports where the user wants to stay in control of direction. For fully autonomous one-shot research, use `deep-research` instead.
