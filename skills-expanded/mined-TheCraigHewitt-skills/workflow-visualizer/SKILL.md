---
name: workflow-visualizer
description: "Generate an interactive HTML diagram of the user's business systems, workflows, or tooling — showing how everything connects, where data flows, which AI agents / scheduled tasks run when, and how processes hang together. Use this whenever the user says 'visualize my workflow,' 'map my systems,' 'show me how this all connects,' 'business OS,' 'system diagram,' 'workflow map,' or wants to see the architecture of their work as a picture rather than a list. Output is a single self-contained HTML file with clickable nodes and progressive disclosure of detail."
---

# Workflow Visualizer

You produce an interactive HTML diagram of how the user's work actually flows — across tools, automations, AI agents, scheduled tasks, and the human steps in between. The goal: the user can open this once a month, see the shape of their system, and decide what to add, remove, or simplify.

This is meta-skill territory. It works best when there's actually something to visualize — a folder full of skills, a set of scheduled tasks, a documented set of workflows, a known tool stack.

## Before you start

Identify what to visualize. Possibilities:

- **The user's full Cowork setup** — skills, scheduled tasks, connectors, agents, content folders
- **A specific business workflow** — e.g., "from lead in to invoice paid"
- **A content pipeline** — e.g., "from idea to YouTube upload to repurposing"
- **A team's tool stack** — what apps connect to what, who uses what

Ask: "What are we mapping?" If the user just says "my workflow" without scope, default to: their current Cowork folder + a scan of `~/Coding/skills/` + scheduled tasks.

## Gather the inputs

Scan the relevant folders. For Cowork-wide visualization, that's:

- All installed skills (and what they trigger on)
- Scheduled tasks (and when they run)
- Connector list (Gmail, Calendar, Slack, etc.)
- Recent task / chat history if accessible (what the user actually uses)
- Any `BUSINESS_CONTEXT.md`, `README.md`, or system documentation in the folder

For a specific workflow, ask the user to walk through it once — capture the steps, the tools used, the inputs and outputs of each step, the decision points.

## The diagram structure

Use a node-and-edge interactive diagram. Each node is a discrete thing — a skill, an app, a person, a scheduled task, a data store. Each edge is a relationship — data flow, trigger, dependency.

Group nodes by phase or domain. Common groupings:

- **Triggers** (scheduled tasks, manual prompts, incoming emails, etc.)
- **Inputs** (data sources, connectors, file folders)
- **Processing** (skills, agents, scripts)
- **Outputs** (artifacts produced — dashboards, emails, content)
- **Storage** (where things end up)

Use clear visual differentiation:

- **Color by type** — triggers one color, skills another, data stores a third
- **Shape by category** — circles for triggers, rectangles for processes, cylinders for storage
- **Edge style** — solid for explicit flow, dashed for optional, arrows showing direction

## Interactivity

The diagram should let the user:

- **Click a node** — open a detail panel with: what this is, what triggers it, what it does, what it produces, related files
- **Hover an edge** — show what data/event flows between the nodes
- **Filter by domain** — show only the content pipeline, only the financial workflows, etc.
- **Zoom / pan** — for larger diagrams
- **Search** — find a node by name

Optional but powerful:

- **Activity overlay** — if usage data is available, color or size nodes by how often they're actually used. Surface the "I installed this 6 months ago and never used it" zombies.
- **Toggle planned vs. live** — if the user has aspirational nodes (something they're planning to add), let them toggle visibility.

## Technical implementation

Single self-contained `.html` file saved as `workflow-map-YYYY-MM-DD.html`.

Use a force-directed graph library (Mermaid for simple cases, or Cytoscape.js / vis-network for richer interaction). Embed the data as a JS object. No external dependencies that require network access at view time.

Layout tips:

- Allow manual layout — auto-layouts get cluttered fast
- Save layout positions back into the file so re-opens are consistent
- Keep the diagram navigable on a laptop screen; complex maps need pan/zoom

## The companion summary

Alongside the HTML, produce a `workflow-summary.md` that explains the map in prose:

```markdown
# Workflow map — [date]

## What this is
One paragraph: what this diagram represents.

## The shape
3-5 paragraphs walking through the system from triggers to outputs. Not a list — a narrative. "Every morning at 7am, the morning-briefing skill fires, which pulls from Gmail and Calendar connectors, and writes both to chat (for me) and to Slack. By 9am I've usually responded to a few flagged emails, which feeds into..."

## What's working
The pieces of the system that are humming.

## What's stale
Nodes that exist but aren't used. Candidates for removal.

## What's missing
Gaps you noticed — workflows the user has alluded to but no clear node handles, or obvious next-step automations.

## Suggestions
Specific moves: add this scheduled task, retire this skill, reorganize this folder.
```

The summary is what the user actually reads. The diagram is what makes them want to read it.

## Rules

1. **Don't visualize the imaginary.** Map what actually exists, not what's planned. Aspirational nodes (clearly labeled) are fine for a separate "planned" overlay but shouldn't be mixed in by default.
2. **Less is more.** A diagram with 60 nodes is unreadable. If the system is genuinely complex, break it into 3-4 sub-diagrams and link between them.
3. **Naming matters.** Use the user's actual names for things. If their skill is called `morning-briefing`, that's the node label — not "AI-powered daily summary generator."
4. **Surface the zombies.** The most valuable insight from a workflow map is usually "you built this thing 4 months ago and haven't used it since." Don't be polite — flag them.
5. **Regenerate, don't patch.** When the user adds new skills or tasks, regenerate the whole map. Trying to keep a diagram in sync incrementally is a losing battle.
