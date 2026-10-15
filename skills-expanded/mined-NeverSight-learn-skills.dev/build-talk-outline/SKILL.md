---
name: build-talk-outline
description: Turn a CFP submission into a structured talk outline with section timings, theory/practical balance, demo risk assessments, fallback plans, and Patrick Winston opening/close principles applied throughout.
---

Before doing anything else:
1. Check if `~/.devadvokit.md` exists.
2. If it does, read it silently and use it throughout this skill.
3. If it does not, stop and tell the user: "I need your DevRel context before I can run this skill. Please run /setup-devadvokit first."

Read `reference/winston-talk-principles.md` silently before starting. Apply these principles throughout — they are not optional polish, they are structural requirements.

---

## Q&A

Ask these questions one at a time. Wait for each answer before moving on.

1. Paste your CFP abstract or talk description. If you don't have one yet, describe the talk in a few sentences — the problem it addresses, the angle you're taking, and what you want the audience to leave with.

2. What's the session format and length? (e.g. talk / 30 min, workshop / 90 min — include whether Q&A is expected and if so, how long it typically runs at this event)

3. Any specifics about this particular audience beyond your general context? (e.g. expected seniority mix, whether this is a specialist or general-track event, anything you know about what they've already seen at this conference)

4. Where does this talk sit on the theory-to-practical spectrum?
   - **Theory-heavy** — concepts, mental models, arguments. Code or tooling appears as illustration, not instruction.
   - **Balanced** — roughly equal time on ideas and hands-on material.
   - **Practical-heavy** — mostly code, tooling, or process. Concepts are introduced only as needed to support the practical work.

5. Are you planning any live demos? If yes: describe each one — what you're showing, what it depends on (network, auth, third-party services, local tooling), and roughly how long you'd expect each to take.

6. Are there any audience interaction moments planned? (e.g. polls, show-of-hands questions, short exercises, pair discussions) If so, describe them.

7. Is there anything that absolutely cannot be cut if you run short on time — a specific point, demo, or moment that the talk doesn't work without?

8. How do you want to end? (e.g. clear call to action, open question for the audience, resources slide, straight into Q&A)

---

## Building the outline

Use the CFP material, the Q&A answers, and the speaker context from `~/.devadvokit.md` to construct the outline. Before generating, consult `reference/outline-structure-patterns.md` to select the most appropriate structural pattern for the talk type and format.

### Timing rules

- Reserve Q&A time first if the user indicated it. A standard allowance is 5 min for a 30-min slot, 10 min for a 45–60 min slot, unless the user specified otherwise.
- The opening section is always 2–3 minutes. The close is always 2 minutes. These are fixed.
- For live demos, add a 20% time buffer on top of the user's estimate. Demos always run longer than expected.
- Flag if the total content the user described won't fit the format. Suggest what to cut or defer rather than silently compressing everything.

### Section format

Present the outline as a structured sequence. For each section:

```
[START TIME–END TIME] Section title
Content notes: what happens in this section, key points covered
Type: [concept / demo / interaction / transition / close]
```

Use cumulative timestamps from 0:00. Be precise — "5:00–9:00" not "about 5 minutes in".

---

## Winston requirements — apply to every outline

Read `reference/winston-talk-principles.md` and apply the following before finalising the outline. These are structural checks, not suggestions.

### Opening (Winston)

The opening section must contain an empowerment promise — a specific statement of what the audience will be able to do by the end that they can't do now. Write it out in the content notes for the opening section. It must be specific enough that a person in the audience could evaluate at the end whether the promise was kept.

Flag and remove any of the following if the user's described opening contains them:
- Opening with a joke
- "Thank you for having me" or any variant
- Apologies (for anything)
- Extended self-introduction before the promise is made

### The Winston Star — memorable moment

Before writing the outline, identify where the following land. Include them as content notes in the relevant sections:

- **Slogan** — the short phrase that becomes the handle for the talk's core idea. If one doesn't emerge naturally from the CFP material, note where in the outline it should be introduced and suggest a candidate.
- **Surprise** — the counterintuitive point. The assumption the audience holds that this talk challenges. Name it in the content notes for the section where it lands.
- **Salient idea** — the single thing. State it explicitly in the outline. If the CFP material implies more than one salient idea, flag this: the talk will be harder to remember.
- **Symbol** — a concrete visual or physical object that represents the core idea. Suggest one based on the talk content. If nothing physical fits, note the closest verbal equivalent.

### Structure check (Winston)

If the talk is persuasive (making a case, recommending a change, arguing a position):
- Vision must be established within the first 5 minutes. Note this in the outline.
- Every section must either advance the vision or provide proof of work. Flag any section that does neither — it's a cut candidate.

### Close (Winston)

The close section must end with a contributions slide — what the audience now has that they didn't have when they walked in. Write out what that slide should contain in the content notes for the close.

The close must mirror the opening promise. Check that the empowerment promise made at the start is directly answered by the contributions at the end.

Flag if the user described ending with "Questions?" or "Thank you" as the final slide.

### Slide density check (Winston)

Based on the number of sections and the content in each, estimate whether the slide count is likely to exceed the Winston threshold (20 slides for a 30-min talk is the warning level). Flag it if so and note which sections are most likely to produce dense slides.

---

## Demo risk assessment

For each live demo identified in the Q&A, produce a risk block immediately after the section it appears in. Consult `reference/demo-risk-patterns.md` to assess each demo's risk profile.

Format each risk block as:

```
⚠️ Demo risk: [demo name]
Risk level: [Low / Medium / High / Critical]
Dependencies: [list what this demo requires to work]
Failure modes: [what is most likely to go wrong]
Fallback: [specific fallback for this demo — see below]
Prep checklist: [what to do before the talk to reduce risk]
```

**Fallback hierarchy — apply in order:**
1. **Pre-recorded video** — record the demo running successfully the day before. Keep it under the demo's time budget. Play it if live fails.
2. **Screenshots with narration** — a deck of screenshots showing the key steps and outputs, talked through live.
3. **Code walkthrough** — open the finished code or config in an editor and walk through it statically, explaining what it would do.
4. **Audience imagination** — only for low-complexity demos. Describe the expected output verbally and move on. Never use this for demos where the visual result is the point.

**Winston's demo rule:** Note in every demo's risk block what the speaker should say if the demo fails mid-run. The failure should teach something — prepare a sentence that frames it as illustrative rather than broken.

State explicitly which fallback applies and what the speaker needs to prepare in advance to have it ready.

---

## Risk summary

After the full outline, produce a consolidated risk section:

**Overall risk level:** [Low / Medium / High] — based on the number and type of live demos, the proportion of the talk that depends on them, and how much of the content can survive if they fail.

**Critical path:** identify which section, if it goes wrong, most damages the talk. This is usually the demo or moment the user said they can't cut.

**Time risk:** flag if the outline is tight. A talk with no slack is a talk that runs over. Recommend where to trim if needed — be specific about which section and by how much.

**Contingency plan:** a one-paragraph description of what the speaker should do if things start going wrong — too slow, demo fails, audience engagement drops. Make it concrete and actionable, not generic advice.

---

## Output order

Present in this order:
1. Structured outline with timestamps and Winston annotations inline
2. Demo risk blocks (inline, after each relevant section)
3. Risk summary
4. Offer: "Want me to adjust the balance, restructure a section, or build out speaker notes for any part of this?"

---

Before presenting any output, read `../../shared/ai-antipatterns.md` and silently rewrite any flagged patterns. Do not mention this step to the user.
