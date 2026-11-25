---
name: flowmotion-skill
description: Turn messy brainstorming, spoken notes, SRT transcripts, or rough planning text into clear flow structures, designed flowchart briefs, motion diagram specs, and presentation-ready visual explanations.
---

# FlowMotion Skill

## Position

FlowMotion Skill turns messy thinking into clear visual structure.

It does two jobs:

1. gather scattered input into a readable flow
2. prepare that flow for static diagrams, motion diagrams, presentation slides, video explainers, or 3D follow-up work

It is not only a flowchart drawing helper. Its main job is to decide what should be shown, why it should be shown that way, and how the viewer should understand it.

## When To Use

Use this Skill when the user asks to:

- turn a messy brainstorm into a flow
- summarize spoken notes into a diagram
- convert an SRT transcript into a flowchart
- prepare a presentation-ready flowchart or motion diagram brief
- prepare a motion diagram for a video or presentation
- explain a system, mechanism, decision path, or workflow visually

Do not use it for:

- ordinary meeting minutes that do not need visualization
- full video scripts without a visual explanation segment
- static posters or cover images where there is no flow logic
- academic review diagrams with strict field-specific rules

## Workflow

### 1. Identify input type

Classify the input:

- `raw_brainstorm`: messy notes, conversation fragments, idea dumps
- `spoken_script`: spoken script, voice memo, SRT transcript
- `structured_note`: outline, article section, meeting summary
- `visual_request`: the user already asks for a flowchart or diagram
- `execution_request`: the user asks for HTML, SVG, PPT, video, or 3D specs

### 2. Gather the structure before drawing

Extract:

- core judgment in one sentence
- key nodes
- relationships between nodes
- main path
- branches, loops, feedback, blockers, or convergence points
- what should be shown in the diagram
- what should stay in notes, narration, or captions

For messy input, separate:

- facts
- opinions
- actions
- process steps
- emotions

Only process, relationships, mechanisms, and action paths enter the diagram layer.

### 3. Choose a diagram type

Pick one:

- `linear_flow`
- `decision_tree`
- `funnel`
- `system_map`
- `timeline`
- `causal_chain`
- `swimlane`
- `layer_stack`
- `motion_sequence`

### 4. Build four specs

Do not jump straight into visual polish.

Produce:

1. `flow_spec`: nodes, edges, main path, diagram type, core judgment
2. `layout_spec`: canvas, layout type, node positions, safe areas
3. `connection_spec`: ports, edge types, path strategy, label avoidance
4. `motion_timeline`: reveal order, path animation, emphasis, final frame

Core rule:

```text
Structure first. Layout second. Connections third. Motion last.
```

## Design Rules

1. Text-based diagram tools can be useful for structure sketches; this Skill focuses on the next step: presentation-ready visual and motion briefs.
2. One diagram should serve one core judgment.
3. If there are more than seven major nodes, split the diagram into multiple frames.
4. Node titles should be short.
5. Arrows must have meaning: progression, branch, feedback, convergence, expansion, or blockage.
6. Colors should support information hierarchy.
7. Motion diagrams should reveal the idea step by step instead of showing everything at once.
8. Do not sacrifice readability for decorative complexity.

## Connection Rules

Before implementing a diagram with lines or motion, define:

- source node
- target node
- source port
- target port
- edge type
- path strategy
- label avoidance
- whether the edge needs an orb
- whether the edge needs gray-to-green progress

Recommended edge types:

- `fan_in`: many fragments converge into one hub
- `main_flow`: main path progression
- `branch_out`: one structure branches into several outputs
- `internal_process`: a process inside a central engine

## Motion Rules

For motion flowcharts:

1. Use a stable layout.
2. Reveal nodes step by step.
3. Keep gray base lines visible only when their step begins.
4. If using an orb, bind it to the real path.
5. The part already traveled becomes green.
6. The part not yet traveled stays gray.
7. Do not create a short green segment that follows the orb like a worm.
8. Hide engineering ports in the final visual.

## Public Safety Rules

This public Skill should not contain private workflow traces.

Do not include:

- local absolute paths
- private transcripts
- private user chats
- internal score notes
- hidden project names
- API keys, tokens, cookies, emails, or phone numbers
- third-party screenshots or recordings
- copyrighted source material
- private scripts or local browser automation

Examples should use synthetic or public-safe text.

## Output Format

Default output:

```text
Core judgment:
Diagram type:
Nodes:
Main path:
Branches / convergence / feedback:
Not suitable for the diagram:
flow_spec:
layout_spec:
connection_spec:
motion_timeline:
Next handoff:
```

If the user only wants structure, stop at `flow_spec`.

If the user wants design execution, hand off to the relevant implementation layer.

## Standalone Execution Contract

This public Skill should still be useful even without the author's private local skills.

If no design, slide, video, or coding Skill is available, produce a complete implementation brief with:

```text
Canvas:
Visual style:
Node list:
Edge list:
Layout spec:
Connection rules:
Reveal order:
Motion rules:
Final frame:
Export suggestion:
```

## Minimal Motion Diagram Recipe

Use this recipe for a first motion-ready flow:

1. Start with a stable 16:9 canvas unless the user requests another format.
2. Place messy inputs on the left.
3. Place the central organizing engine in the middle.
4. Place the structured output or outputs on the right.
5. Reveal one node at a time.
6. Draw one path at a time.
7. Use a gray base path and green progress path when explaining transformation.
8. Keep labels away from paths.
9. End with a clean full-frame summary.

## Self-Check Before Final Output

Before returning the brief, check:

- Can a viewer understand the main path in five seconds?
- Is there one core judgment?
- Are there too many nodes for one frame?
- Do edges have real meaning?
- Are labels short enough?
- Does the motion reveal understanding instead of decoration?
- Can another designer or coder implement this without seeing the original conversation?
