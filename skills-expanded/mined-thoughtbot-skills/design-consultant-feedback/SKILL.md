---
name: design-consultant-feedback
description: Evaluate meeting notes, project updates, or sprint recaps against designer consulting best practices. Use this skill whenever the user pastes meeting notes, sprint notes, standup summaries, or project updates — OR when they ask for a project check-in, self-assessment, or reflection without any notes to share. Triggers on phrases like "are we doing this right?", "what are we missing?", "how's the team doing on process?", "evaluate this sprint", "how am I doing on this project?", "let's do a check-in", or "I want to reflect on how the project is going". In note-analysis mode, extracts and evaluates practices from the content. In guided reflection mode, asks a structured set of questions one at a time and synthesizes a full evaluation at the end. Both modes use the same framework and output format.
---

# Design Consultant Feedback

Evaluate project notes against designer best practices. Identify the current project phase, score adherence to key practices, and surface specific gaps or risks.

## How to use this skill

This skill has two modes. Choose based on what the user provides.

### Mode 1: Note analysis
The user has pasted meeting notes, a transcript, standup summary, or any project update.

1. Read the content provided
2. Identify the likely project phase (see phases below)
3. Evaluate against the relevant phase practices AND the "We Should Always" principles
4. Output a structured evaluation report (see output format below)

If the phase is ambiguous, evaluate against all relevant phases. If multiple phases are active simultaneously, note that.

### Mode 2: Guided reflection
The user has no notes to share — they want to reflect on how a project is going.

**Step 1:** Present all six structured questions at once using the ask_user_input tool. Use single_select for each:

Question 1: "What project phase are you in?"
Options: Design sprint / Right after a sprint / Active sprint cadence / Wrapping up

Question 2: "Where is design at compared to devs?"
Options: Well ahead / 1 week ahead / In lockstep / Behind dev

Question 3: "Have you recently received user or stakeholder feedback?"
Options: Yes, recently / Not in a while / No formal process

Question 4: "What is the stakeholder relationship like?"
Options: Active and asking questions / Quiet but present / Disengaged

Question 5: "Are you tracking sprint assumptions?"
Options: Not tracking / Tracked and being addressed / Identified but unaddressed

Question 6: "Are you looking ahead?"
Options: Actively thinking about what's next / Loosely / Not yet

**Step 2:** After receiving those answers, ask an opened ended question
"What's unresolved or keeping you up at night about this project?"

**Step 3:** Ask for more context
"Do you have any extra documentation you can share?"

**Step 3:** Once you have all responses, take them into account and synthesize a full evaluation using the same output format as Mode 1. Map their answers to the relevant phase practices and "We Should Always" principles. Be specific — reference what they actually said.

In both modes: these are guidelines, not rules — use judgment when context might reasonably explain a gap before treating it as a risk.

---

## Project Phases & Best Practices

### Phase 1: Design Sprint

Key practices to look for:
- Following sprint exercises with structure (speedy 8, storyboards, etc.)
- Actively building trust with the client — listening, asking questions openly
- Establishing a relationship before offering constructive feedback (sequence matters)
- Using design skills to shape ideas and align teams with sketches and flow diagrams — not polished interfaces
- Showing the process and keeping work deliberately rough/messy — low fidelity is the goal
- Helping the team "see" the vision: a little more fidelity after exercises goes a long way
- Helping the team develop a shared mental model of what's being built
- Identifying the simplest version of an idea that can be validated with users
- Using design sprints to surface and list assumptions — not just align on features
- Designer whiteboarding/sketching at kickoff to resolve ambiguity early

Risk signals:
- Designer driving polished solutions before client alignment
- No mention of user needs or client perspective
- Critique offered before rapport is established
- Low client participation or siloed conversations

---

### Phase 2: Right After a Sprint

Key practices to look for:
- Cataloging everything that *wasn't* resolved during the sprint
- Building a clear backlog of open questions with a plan to get them answered
- Creating user flows or technical diagrams to establish shared mental model
- Expanding the critical path to surface unknowns not covered in the sprint
- Identifying a high-confidence first epic dev can start immediately (e.g., auth flows)
- Design identifying requirements for the first epic without needing PM
- Continuing to track and surface assumptions
- Running an impact/effort exercise to prioritize post-sprint features
- Starting user interviews or usability tests on riskiest assumptions

Risk signals:
- No post-sprint alignment artifact (flow diagram, question list)
- Dev waiting on design to define first tasks
- Assumptions left implicit rather than written down
- No plan to get unanswered questions resolved
- No prioritization of what gets built first

---

### Phase 3: Active Sprint Cadence

Key practices to look for:
- Designer staying 1–2 weeks ahead of dev
- Designing with implementation in mind — weigh complexity against value, meet with devs to discuss options that reduce build complexity while maintaining UX
- Continuous user testing and validation — not just building
- Willingness to change direction as new information surfaces (moving between discovery and delivery fluidly)
- Documentation calibrated to the team's needs — not too much, not too little; varies by team and org size
- Figma structured for two audiences: dev reference pages + flows for testing/validation
- Active scope management — tradeoffs called out when new ideas surface, no feature added without discussion
- Working in the open — sharing unpolished work early and often
- Establishing regular cadences for updating stakeholders, the client, and the immediate team
- Maintaining no knowledge silos — everyone understands what's being built and why
- Organizing Figma and artifacts regularly ("keeping desk tidy")
- Designing the future — sketching out what comes after the current engagement
- Expanding influence to stakeholders outside the core project team, especially leadership
- Maintaining design vision in code — designer staying close to the build to catch detail drift (typography, spacing, breakpoints, color)
- Holding regular retros that include: celebrating wins, surfacing concerns, asking "Are we building the right product?", and evaluating whether the project is on track
- Client running acceptance on a regular cadence before features are deployed

Risk signals:
- Designer and dev in lockstep or designer is behind
- No mention of user testing or validation
- Scope changes accepted without tradeoff discussion
- Figma not described as structured or maintained
- Only one person speaks to a topic — knowledge is siloed
- No retro rhythm or team pulse check
- Design decisions not accounting for implementation feasibility
- Design and dev working separately with no mention of shared visibility

---

### Phase 4: Wrap Up

Key practices to look for:
- Share a vision for the product's future — features discussed but not built, roadmap for next steps
- Client team knows where to go after the engagement ends
- Document the engagement (local Figma backup, CSS/design structure, project summary)
- Leave the team in a better position than at the start
- Give thoughtful review of both code and process
- Celebrate together

Risk signals:
- No forward-looking artifacts or roadmap
- No documentation plan
- Abrupt handoff with no transition
- Team not equipped to continue without the consultant

---

## We Should Always (apply across ALL phases)

These are non-negotiable regardless of phase. Evaluate for these in every set of notes.

### Find and communicate your niche on the team
- Identify where your skills bring the most leverage for this specific client and team
- Share how you work best so PMs and devs know when to pull you in
- Adapt your role to fill gaps — don't apply a fixed process to every team

Risk signals: designer role is undefined or purely executional; no mention of how the designer is positioned relative to PM and dev

### Be a good partner
- Use the full flexible skill toolset — not just design
- Help the product team define requirements and map out flows
- Help developers by figuring out the best Figma-to-code workflow for the team
- Maintain constant communication between design and development — context loss and design drift both stem from this breaking down

Risk signals: designer working in isolation; handoff described as one-directional; no mention of dev or PM collaboration

### Be the voice of the user
- You cannot always get direct feedback from users — use experience and best judgment to advocate for the end user
- Use your outside perspective; your fresh eyes can spot UX issues the client team missed because they're too close to the product
- When user testing is cut for budget or timeline reasons, run a heuristic review and share findings proactively
- Design for flows and edge cases, not individual screens — consider what could go wrong at every stage

Risk signals: no one on the team mentioned user needs; design decisions made without any user perspective; no mention of edge cases or unhappy paths

### Solve a problem the client didn't know they had
- Help their teams communicate between product, design, and dev
- Evaluate and improve accessibility — and stay current on evolving accessibility requirements
- Level up their team's skillsets
- Start or contribute to a component library
- Leave the team in a better place than when you started, including with a design system or artifacts structured for handoff
- Polish deliverables by delivering thoughtbot branded and thoughtfully constructed documents and artifacts

Risk signals: work is purely execution with no mention of improving team process, accessibility, or leaving artifacts behind

### Build trust through judgment, not just execution
- Push back thoughtfully when something's wrong — frame it as trade-offs and costs, not opinion
- Ship quickly and scope honestly; trust gets earned before it gets extended into direction
- The client knows their business best — our value is technical expertise that helps them decide, not being right

Risk signals: disagreement framed as "I think" rather than trade-offs; scope commitments made without surfacing constraints; conflicts resolved with no artifact the client can point back to later

### Engage broadly, not through one point of contact
- Spread engagement across the team rather than routing everything through one person
- Over-communicate, especially in shared or public channels — visible proactivity is a small way of leading
- Show up to meetings and updates with a plan, not just a status

Risk signals: one person answers every question; important reasoning happens in DMs the rest of the team can't see; updates with no plan attached

### Tie work to business outcomes
- Understand why the client hired thoughtbot and what success looks like to them, not just the feature list
- Report progress in terms of business metrics where possible, not only what shipped
- Check in with the client on how they feel about the work, separate from whether it's on schedule
- Be honest about speed/quality trade-offs — AI tooling shifts this calculus, so name where it does

Risk signals: updates describe output with no mention of business impact; no reference to why the client hired thoughtbot in the first place; speed/quality trade-offs made silently

### Practice continuous validation and derisking
- Assumptions are surfaced and tracked throughout all phases
- Riskiest ideas are tested with users before building
- No mention of validation = a red flag at any phase
- Understand which assumptions carry the most risk and get answers before the cost of being wrong becomes too high

### Think about your value in terms of:
- **Adding clarity** — user flows, diagrams, shared mental models, decision tracking
- **Reducing risk** — surfacing unknowns, calling out scope creep, testing assumptions
- **Envisioning the future** — designing between tomorrow and next year, not just the current sprint
- **Using intuition to inform product decisions** — not just executing what's asked

### Move fluidly between discovery and delivery
- Building software is not linear — when the team hits a new unknown mid-sprint, shift back into discovery mode rather than waiting for a formal sprint
- Use design thinking to quickly resolve ambiguity: sketch options, facilitate a quick exercise, run a short user interview
- T-shaped skills mean broad context (business, UX, technical, visual) applied to specific problems — watch for designers operating in only one dimension

Risk signals: designer described only as an executor; no mention of forward-looking work or product influence; designer unable or unwilling to shift modes when new information surfaces

---

## Output Format

Structure your evaluation as follows. Be specific — reference actual content from the notes when calling something out.

```
## Phase identified
[Name the phase(s) and briefly explain how you determined it]

## What's going well
[2–4 specific practices being followed, with evidence from the notes]

## Gaps or risks
[2–4 specific practices missing or at risk, with a brief explanation of why it matters]

## Highest priority action
[One concrete thing the team should do next, based on the gaps identified]

## Questions to investigate
[1–3 things not mentioned in the notes that are worth checking on]
```

Keep the tone direct and collegial — this is a peer check-in, not a performance review. Focus on how the designer can improve. Avoid generic feedback. If the notes don't give enough information to evaluate a practice, say so rather than assuming. Remember these are guidelines, not rules — flag when context might reasonably explain a gap before treating it as a risk.

Flag when context may be missing.
