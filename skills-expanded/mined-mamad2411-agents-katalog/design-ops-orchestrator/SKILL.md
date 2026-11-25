---
name: design-ops-orchestrator
description: Routes any UX/UI request to the right Design Ops skills in the right order, with stage gates and handoffs. Use when the user asks where to start, what comes next, what the process is, or wants a full design engagement run end to end — and whenever a request is broad enough to need more than one skill (redesign, launch, audit, new product, design system).
allowed-tools: Read, Grep, Glob
---

# Design Ops Orchestrator

## Overview

Design Ops holds 46 skills and 39 commands. Most real requests need three to six skills
in a particular order, and running them in the wrong order wastes work — you
cannot critique a flow before you know who it is for, and you cannot set metrics
before you know what good looks like.

This skill is the router. Identify the pipeline, run its stages in order, honour
the gate, hand off the named artifact, and name the command that produces it.

## Two bands: stages and depth

Not every skill is a stage. A **stage** is a decision that gates the next
decision. A **depth skill** is a library you open once you already know what you
are building — 500+ layout blocks, 1000+ microcopy templates, 200+ animation
recipes, 500+ palettes. Loading a library before you have a decision to make just
burns context.

So each pipeline below lists its core stages in order, then the depth skills to
pull in _inside_ a stage when the work gets that specific. Keep core stages at six
or fewer. If a pipeline seems to need more, one of them is depth.

## Routing

Match the user's request to a pipeline. If the request is vague ("help me with my
app"), ask the qualifying questions below before routing.

| The user wants to…                             | Pipeline        | Command                         |
| ---------------------------------------------- | --------------- | ------------------------------- |
| Find what's wrong with something that exists   | **Evaluate**    | `/audit`, `/roast`              |
| Fix AI-generated UI that works but looks wrong | **Fix**         | `/fix`                          |
| Design something that doesn't exist yet        | **Create**      | `/inspo` → `/style` → `/screen` |
| Build or ship an actual component              | **Implement**   | `/component`                    |
| Compose a whole page                           | **Compose**     | `/inspo` → `/page`, `/scroll`   |
| Generate design assets with AI                 | **Generate**    | `/generate`                     |
| Start or scale a design system                 | **Systematize** | `/tokens`                       |
| Move a design into code                        | **Handoff**     | `/figma`                        |
| Understand why people aren't finishing         | **Convert**     | —                               |
| Ship to new countries or languages             | **Localize**    | —                               |
| Design an AI or agent feature                  | **AI Surface**  | `/ai-audit`                     |
| Know whether any of it worked                  | **Measure**     | `/measure`                      |

### Qualifying questions

Ask at most three, and only what the request hasn't already answered:

1. **Does it exist yet?** Nothing built → Create. Something built → Evaluate.
   Built by an AI and looks off → Fix.
2. **What platform?** Web/desktop, mobile, native, or ambient/voice/spatial. This
   selects the platform skill layered into every pipeline.
3. **What decision hangs on this?** Ship/no-ship, roadmap priority, or a specific
   fix. This sets the depth — a ship gate needs the full pipeline; a specific fix
   usually needs one skill.

## Layers

### Platform

Layer the matching platform skill into whichever pipeline is running:

- Mobile or responsive → `mobile-ux-design` + `platform-visual-standards`
- Desktop, enterprise, dashboards, data-dense → `desktop-app-design` +
  `data-visualization-mastery`
- Ambient, wearable, automotive, screenless → `ambient-calm-zero-ui`
- Native iOS or Android specifically → `platform-visual-standards`

### Process

If the user asks what the process is called, wants a design sprint, or needs a
Double Diamond framing for stakeholders → `design-process-methods`.

### Packaging

If the artifact is leaving the team — client, executive, portfolio — package it
with `business-design-templates`.

### Memory

Any pipeline spanning more than one command relies on `.design-ops/` to carry decisions
between them. `design-memory` holds that contract — the canonical schema, which
command owns which subtree, and the merge rules. Load it whenever a stage reads
or writes design memory, which in practice is every Create, Compose, Systematize
and Fix run.

## How this relates to the commands

- **Commands do not invoke pipelines.** A command has a fixed output contract.
  Silently running a six-stage pipeline behind it would break that contract and
  spend context the user didn't ask for. Each command's own "Next Step" footer
  surfaces the pipeline one step at a time, which is the right pace.
- **This skill does not invoke commands.** It names skills, because skills carry
  the knowledge. But every pipeline above names the command that produces its
  artifact, and you should hand off to it by name.
- **The chain is `/start` → orchestrator → pipeline → command.** This is why
  `/start` never has to list 39 commands.
- **Convert and Localize have no command yet.** Run them as pipelines and say so.

## Operating rules

- **Announce the pipeline before running it.** The user should know which stages
  are coming and roughly what each costs them in time.
- **One stage at a time.** Each skill's content stays in context once loaded, so
  running six at once is both slower and worse than running them in sequence.
  This is also why depth skills are opened inside a stage, not up front.
- **Report gate failures.** "Stage 3 failed the gate — 12 findings have no
  severity rating" is useful. Silently continuing is not.
- **Short-circuit narrow requests.** "What's a good tap target size?" is one
  skill, not a pipeline. Don't run process for its own sake.
- **Stop when the decision is answerable.** The pipeline serves the decision, not
  the other way around.

## Cross-references

Each pipeline's stages have their own reference files, listed inside each skill.
Load references only when the stage's SKILL.md points to them — they are large
and they persist in context once read.

Further sections — read when the above is not enough: `references/details.md`.
