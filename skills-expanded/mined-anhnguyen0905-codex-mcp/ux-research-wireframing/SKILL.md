---
name: ux-research-wireframing
description: UX research and early-stage design — user personas, jobs-to-be-done, user interviews and usability testing protocols, heuristic evaluation (Nielsen), user flows and task analysis, information architecture, wireframes and low-fidelity prototypes, prototype test plans, research synthesis and insight reporting. Use for user research, usability testing, personas, user flows, wireframing, or UX audits.
---

# UX Research & Wireframing (evidence → flows → wireframes → test)

## Method — research before pixels

1. **Frame the question.** What decision will this research change? If no decision depends on it,
   don't run it.
2. **Gather evidence** — interviews, analytics, support tickets, usability tests. Behavior beats
   opinion: what users *did* outranks what they *say* they'd do.
3. **Synthesize** into jobs, personas, and journey pain points backed by quotes/observations.
4. **Design flows and IA** for the top jobs, then wireframe, then test the wireframes — cheapest
   possible artifact that can fail.

## Interviews and usability tests

- **Interviews** (5–8 per segment reaches saturation for most questions): ask about past behavior
  ("walk me through the last time you…"), never hypotheticals ("would you use…?" — answers are
  worthless). Open questions, no leading, silence is a tool. Record and tag verbatims.
- **Usability test protocol**: 5 users per iteration finds most severe issues (Nielsen's curve —
  run more rounds, not bigger ones). Script = realistic task scenarios ("book a room for next
  Friday"), not feature tours ("click the booking button"). Think-aloud; facilitator never helps
  or explains; define task success criteria *before* the session.
- **Metrics per task**: completion rate, time-on-task, error count, and a severity rating per
  observed issue:

```
Severity 0 = not a problem        Severity 3 = major — struggled, workaround found
Severity 1 = cosmetic             Severity 4 = blocker — task failed
Severity 2 = minor irritation
Issue priority ≈ severity × frequency (how many participants hit it)
```

## Synthesis artifacts

- **Persona**: goals, contexts, behaviors, top frustrations — each attribute traceable to data.
  Name/photo/hobbies are garnish; a persona with demographics but no behavior is fiction.
- **Jobs-to-be-done**: "When [situation], I want to [motivation], so I can [outcome]." One job per
  statement; jobs are stable, solutions churn.
- **Insight report**: finding → evidence (count + representative quote) → implication → recommended
  action → confidence. Separate observations from interpretations explicitly.

## Flows, IA, wireframes

- **User flow**: one flow per job — entry point, steps, decisions, error/empty states, exit.
  Count the steps; every step must earn its place. Map the current (as-is) flow before drawing
  the ideal one.
- **Information architecture**: derive grouping from user language (card sorting) and validate
  findability (tree testing) rather than mirroring the org chart or the database schema.
- **Wireframes**: low fidelity on purpose — boxes, real hierarchy, *realistic content* (never
  lorem ipsum for labels, headings, or data: content is the interface). Annotate behavior
  (what each control does, where it goes, error/empty/loading states). No colors, no branding —
  polish invites feedback on the wrong things.
- **Prototype test plan**: hypothesis per screen ("users will find X in ≤2 clicks"), task list,
  success criteria, participant profile, and what result changes the design.

## Heuristic evaluation (Nielsen's 10)

Visibility of system status · match to real world · user control/freedom (undo) · consistency ·
error prevention · recognition over recall · flexibility/efficiency · minimalist design · help
users recognize and recover from errors · help/documentation. Method: 2–3 evaluators walk the key
tasks independently, log each violation with heuristic + location + severity, then merge. A
heuristic audit finds *likely* problems; only user testing confirms them.

## Failure modes

- Personas invented in a workshop with zero user contact — laundering assumptions as research.
- Asking users what they want, then building it ("would you use this?" → "sure").
- Leading tasks in usability tests that name the UI element being tested.
- Testing once at the end instead of every iteration — findings arrive too late to matter.
- High-fidelity mockups presented as "wireframes": stakeholders debate colors, structure ships
  unexamined.
- Wireframes missing empty, error, and loading states — the states where products actually fail.
- Insight reports that are quote dumps with no severity, frequency, or recommended action.
- IA copied from internal team structure instead of user mental models.

## Reviewer checklist

- [ ] Research question tied to a real decision; method matches the question
- [ ] Interview/test scripts ask about behavior, contain no leading prompts
- [ ] Task success criteria defined before testing; severity × frequency prioritization used
- [ ] Every persona/JTBD attribute traceable to evidence
- [ ] Flows cover error/empty/edge states, not just the happy path
- [ ] Wireframes use realistic content and annotate all interactive behavior
- [ ] Heuristic findings labeled as expert judgment, distinct from user-test evidence
- [ ] Report separates observation from interpretation and states confidence

## Provenance

Standard UX research practice (Nielsen Norman heuristics and sample-size guidance, JTBD framing).
Sample sizes and thresholds are **derived, unverified** defaults — adjust for risk and audience
diversity.
