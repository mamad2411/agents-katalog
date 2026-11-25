---
name: idea-storm-x4
description: Generate a large idea set with four parallel agents, then filter it down through two debate rounds. Use when the user wants to brainstorm or explore possibilities for a project, product, feature, or strategy.
---

# Idea storm

A wide-then-narrow brainstorm on the user's topic. Breadth comes from agents that can't see each other's output; quality comes from making the later rounds argue for what survives.

The topic is in `$ARGUMENTS`. If it's empty or too thin to brief an agent with, ask the user what they're brainstorming about before launching anything.

## Round 1 — Generate

Launch four agents in parallel, each working a different angle so their idea spaces barely overlap. For consumer product work the seams that divide cleanly are growth and virality, monetization, community and UX, and content and data. Pick the angles that actually fit this topic — a dev tool, an internal process, and a marketplace each split differently.

Give every agent the same context about the user's project and ask each for 50 numbered ideas, a short title and a line or two apiece. The volume target is real, not decorative: the tail of a long list is where the non-obvious ideas live.

## Round 2 — Semifinals

Launch two agents in parallel, each taking 100 ideas (agents 1+2 for one, 3+4 for the other) and arguing its set down to the strongest 50, merging near-duplicates along the way.

Judge on feasibility, real impact, originality, taste, and fit for the audience. An agent that deletes the bottom half without weighing these hasn't done the job.

## Round 3 — Final

One agent takes the 100 semifinalists, merges what overlaps across the two branches, applies the same criteria, and returns a final 50.

## Present

Show the final list, numbered and clean. Then ask which ones the user wants to pursue or turn into tasks.
