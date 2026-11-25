---
name: brainstorm-lenses
description: Book-sourced thinking lenses for the brainstorm phases — Frame (Ackoff mess and dissolve, Checkland CATWOE, Minto SCQA), Map (Meadows stocks, flows, feedback loops, delays, leverage points; Senge archetypes and iceberg), Reason (pyramid, MECE, ladder of inference, second-order effects, challenge types), and a feasibility-only check.
---

# Brainstorm lenses (embed into Codex prompts)

Use the lenses in order: frame before map, map before reason, and feasibility last.
Keep observations, interpretations, assumptions, options, and recommendations distinct.

## Standards block

### Frame lens

```
Frame lens
- Classify the topic as a mess or a single problem; a mess is an interacting system of problems. (Ackoff, Redesigning the Future)
- Ask the dissolve question first, then name the treatment: absolve, resolve, solve, or dissolve. (Ackoff, Creating the Corporate Future)
- Complete CATWOE: Customers, Actors, Transformation, Worldview, Owner, Environmental constraints; state at least two worldviews when stakeholders disagree. (Checkland, Systems Thinking, Systems Practice)
- Draw the system boundary: list what is inside, outside, and crossing it; include the loop producing the symptom. (Checkland, Systems Thinking, Systems Practice; Meadows, Thinking in Systems)
- Rewrite the topic as SCQA: Situation, Complication, Question, Answer; leave Answer empty until Reason. (Minto, The Pyramid Principle)
- Do not introduce options or recommendations in Frame. (derived)
```

### Map lens

```
Map lens
- Name stocks and the flows that fill or drain them. (Meadows, Thinking in Systems)
- Trace each feedback loop, label it R or B, name the dominant loop, and state what could shift dominance. (Meadows, Thinking in Systems)
- Mark delays between cause and effect, including perception, response, and delivery delays. (Meadows, Thinking in Systems; Senge, The Fifth Discipline)
- Describe the iceberg at four depths: events, patterns, structure, and mental models. (Senge, The Fifth Discipline)
- Check Senge's nine archetypes: Balancing process with delay, Limits to growth, Shifting the burden, Eroding goals, Escalation, Success to the successful, Tragedy of the commons, Fixes that fail, Growth and underinvestment; state “none fits” when appropriate. (Senge, The Fifth Discipline)
- Cross-check Meadows' eight traps: policy resistance, tragedy of the commons, drift to low performance, escalation, success to the successful, shifting the burden to the intervenor, rule beating, seeking the wrong goal. (Meadows, Thinking in Systems)
- Rank candidate leverage points from weakest to strongest: 12 numbers and parameters; 11 buffer sizes; 10 stock-and-flow structure; 9 delay lengths; 8 strength of balancing loops; 7 gain of reinforcing loops; 6 information flows; 5 rules; 4 power to self-organize; 3 goals of the system; 2 the paradigm behind the system; 1 the power to transcend paradigms. (Meadows, Thinking in Systems)
- Treat a leverage point as a place to intervene, not yet as an option. (Meadows, Thinking in Systems)
- Do not introduce options or recommendations in Map. (derived)
```

### Reason lens

```
Reason lens
- State one governing answer to the SCQA question, then give three to five MECE supports; each support answers why or how. (Minto, The Pyramid Principle)
- Attach checkable evidence to every support or mark it unverified; trace observable data, selected data, interpretation, assumption, and conclusion, naming the divergent rung. (Argyris, in Senge et al., The Fifth Discipline Fieldbook)
- For each option, state the immediate effect, then each mapped loop's response, including intended and unintended second-order effects, and any trap or archetype the option risks triggering. (derived; traps and archetypes from Meadows, Thinking in Systems, and Senge, The Fifth Discipline)
- Classify objections as LOGIC: the conclusion does not follow or grouping is not MECE. (derived)
- Classify objections as SYSTEM: a loop, stock, delay, boundary, or archetype is missing. (derived)
- Classify objections as ASSUMPTION: an unstated belief or worldview drives the claim. (derived)
- Classify objections as EVIDENCE: a claim lacks checkable support. (derived)
- Add contributions: new, supported ideas that strengthen the analysis. (derived)
- When a support has no checkable evidence, mark it unverified and do not count it toward the governing answer. (derived)
- When two options tie on the supports, say so and name the observation that would break the tie; do not pick one silently. (derived)
```

### Feasibility lens

```
Feasibility lens
- Assess only the surviving recommendation. (derived)
- When no recommendation survives Reason, give no verdict and state why; when several survive, assess the top-ranked one and name the others. (derived)
- Record order-of-magnitude effort as S, M, L, or XL; list dependencies and main risks. (derived)
- Record reversibility as yes, partly, or no, and name the first concrete step. (derived)
- Judge whether the recommendation is systemically desirable and culturally feasible. (Checkland, Systems Thinking, Systems Practice)
- Give exactly one verdict: FEASIBLE, FEASIBLE-WITH-CONDITIONS, or NOT-FEASIBLE. (derived)
- Do not include rollout, rollback, or task-list content. (derived)
```
