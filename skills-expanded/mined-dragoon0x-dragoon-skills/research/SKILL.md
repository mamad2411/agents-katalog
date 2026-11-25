---
name: research
description: Generate a structured research template for a topic. Use before deciding to build something - forces specific decision-driven research with sources, expert disagreement, and a steelman. dragoon does NOT fetch the web. Output goes to .dragoon/research/research-{slug}-{date}.md. Run as `node ~/.claude/skills/dragoon/skills/research/scripts/research.js "<topic>"`.
version: 1.0.0
---

# /research

Structured research template. dragoon does NOT call the web.

## When to use

- Before deciding to build something
- The user says "should we use X", "research Y", "what's the state of Z"

## Forces you to articulate

- the specific decision the research will inform
- existing solutions in a comparison table
- expert disagreement (cited)
- the strongest argument against doing this
- the gap between known and unknown

## Run it

```
dragoon research "should we move from rest to graphql"
dragoon research "should we move..." --apply
```
