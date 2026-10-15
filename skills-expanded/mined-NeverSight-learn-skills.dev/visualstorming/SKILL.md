---
name: visualstorming
description: Adds an optional browser-based visual companion for brainstorming with mockups, diagrams, wireframes, and side-by-side visual choices. Use when a discussion would be easier to resolve visually, especially for UI layouts, flows, architecture diagrams, spatial relationships, visual hierarchy, or design direction comparisons.
---

# Visualstorming

Use a browser as a visual companion during brainstorming. This is a tool, not a mode: use it only for questions the user can answer better by seeing options than by reading text.

Do not invoke writing-plans, create implementation plans, or start coding because this skill was used. Visualstorming ends when the visual question is answered or the user declines visual help.

## Consent Gate

When upcoming work likely benefits from visual treatment, offer visualstorming once before creating browser artifacts.

The offer must be its own message, with no context summary or clarifying question mixed in:

> Some of this may be easier to discuss visually. I can open a local browser view with mockups, diagrams, comparisons, or layout options as we go. It can use extra tokens and may require a local URL. Want to use visualstorming?

Wait for the user response. If they accept, use browser visuals only when useful. If they decline, continue text-only. If they already asked for visualstorming, browser mockups, visual options, wireframes, diagrams, or a visual comparison, treat that as consent.

## Browser Or Text

Use browser visuals when the content itself is visual:

- UI mockups, wireframes, navigation structures, component layouts
- Side-by-side layout, color, typography, density, or design direction comparisons
- Architecture, data-flow, relationship, state-machine, or process diagrams
- Spatial questions where arrangement, grouping, or hierarchy matters
- Design polish questions about spacing, emphasis, rhythm, or look and feel

Use text when the answer is mainly words:

- Requirements, scope, constraints, success criteria
- Conceptual tradeoffs, pros/cons, API choices, data model choices
- Naming, copy, terminology, acceptance criteria

A UI topic is not automatically visual. "What should this wizard do?" is text. "Which wizard layout works better?" is visual.

## Workflow

1. Decide if the current question is visual.
2. If not already approved, ask the consent gate question and stop.
3. Create a local visual artifact in the current project, usually HTML.
4. Open or serve it in a local browser using the environment's browser capability.
5. Ask one focused visual question.
6. On the next user turn, combine their text response with any browser interaction data.
7. Continue with another visual artifact only if the next question benefits from seeing it.

## Artifact Rules

- Prefer small HTML fragments or simple self-contained HTML files.
- Use stable filenames that describe the screen, such as `layout-options.html`.
- Do not reuse filenames for materially different screens; preserve previous options.
- Keep each screen focused on one decision.
- Label choices clearly with stable IDs such as `layout-a` or `flow-minimal`.
- Make visuals legible at desktop and mobile widths.
- Avoid decorative complexity unless visual style is the decision being tested.

## Interaction Pattern

For choice-based screens, make options selectable and record the selection when the environment supports it. If structured browser events are unavailable, ask the user to reply in chat with the option label.

Recommended option markup:

```html
<section class="options">
  <button data-choice="layout-a" aria-label="Choose layout A">
    <strong>Layout A</strong>
    <span>Compact sidebar with dense controls</span>
  </button>
  <button data-choice="layout-b" aria-label="Choose layout B">
    <strong>Layout B</strong>
    <span>Top navigation with wider content area</span>
  </button>
</section>
```

Ask focused questions:

- "Which layout feels easier to scan?"
- "Which diagram matches your mental model?"
- "Which visual direction should we refine?"

Avoid broad questions like "Thoughts?", "What do you think?", or "Is this good?"

## Browser Session Notes

Use the best browser mechanism available:

- If an in-app browser tool exists, open the local file or localhost URL there.
- If a visual companion server exists, write the screen to its content directory and read its event log on the next turn.
- If no browser tool is available, create the HTML artifact and provide the local path or URL.

For server-backed companions: save `screen_dir`, `state_dir`, URL, and session directory; confirm the server is alive before each new screen; read interaction events only after the user responds in chat. Chat text is primary feedback; browser events are supporting data.

## Stop Conditions

Stop using visualstorming when the user declines, remaining decisions are conceptual, the visual choice has enough signal, or browser setup costs more than the decision warrants.