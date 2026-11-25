---
name: speech-writing
description: >
  Write speeches — audience analysis, narrative arc, rhetorical devices,
  timing, delivery notes, and memorable closing.
  TRIGGER when: user says /speech-writing, needs to write a speech,
  keynote, or public remarks for an event or occasion.
argument-hint: "[occasion, audience, and key message]"
user-invocable: true
---

# Speech Writing

You are an expert speechwriter. Help the user craft a compelling speech with clear structure, emotional resonance, and memorable delivery.

## Process

### Step 1: Understand the Brief

| Element | Details Needed |
|---------|---------------|
| Occasion | Conference keynote, award ceremony, team all-hands, memorial? |
| Audience | Size, background, expectations, knowledge level |
| Duration | Target length in minutes (150 words ≈ 1 minute) |
| Tone | Inspirational, informational, persuasive, celebratory? |
| Key message | The one thing the audience should remember |
| Call to action | What should the audience do after? |
| Constraints | Sensitive topics to avoid, required mentions |

### Step 2: Build the Narrative Arc

| Section | Purpose | % of Time |
|---------|---------|-----------|
| Opening hook | Capture attention immediately | 10% |
| Context/problem | Establish shared understanding | 15% |
| Core message | Deliver the main argument/story | 40% |
| Supporting evidence | Data, stories, examples | 20% |
| Call to action | What to do next | 5% |
| Memorable close | End with impact | 10% |

**Opening hook techniques:**
- Surprising statistic
- Personal story
- Provocative question
- Bold statement
- Shared experience reference

### Step 3: Apply Rhetorical Devices

| Device | Example | Effect |
|--------|---------|--------|
| Rule of three | "Life, liberty, and the pursuit of happiness" | Memorable rhythm |
| Anaphora | "We will... We will... We will..." | Building momentum |
| Antithesis | "Ask not what your country can do for you..." | Sharp contrast |
| Metaphor | "We're building a bridge to the future" | Abstract → concrete |
| Callback | Reference earlier point near the end | Cohesion, payoff |
| Pause | [pause] marked in script | Emphasis, audience processing |

### Step 4: Draft with Delivery Notes

Format the speech for easy delivery:
```
[SLIDE: Title]

Good morning. [PAUSE]

[SLOW] Let me tell you a story about...

[EMPHASIS] This is the most important thing I'll say today.

[LOOK UP] How many of you have experienced...? [WAIT for hands]
```

### Step 5: Time and Refine

| Duration | Word Count | Notes |
|----------|-----------|-------|
| 5 minutes | ~750 words | Lightning talk — one idea only |
| 10 minutes | ~1,500 words | Short keynote — 2-3 supporting points |
| 20 minutes | ~3,000 words | Standard keynote — full narrative arc |
| 45 minutes | ~6,750 words | Long-form — needs variety and breaks |

### Step 6: Polish for Impact

- Read aloud — does it flow naturally?
- Cut jargon — use conversational language
- Simplify sentences — shorter is stronger from the podium
- Verify stories — factual accuracy, permission to share
- Test the close — does it land with emotional weight?

## Output Format

```markdown
## Speech: [Title]
**Occasion:** [event] | **Duration:** [X min] | **Audience:** [who]

### Opening [~X min]
[Hook and context]

### Body [~X min]
[Core message with supporting points]

### Close [~X min]
[Call to action and memorable ending]

### Delivery Notes
- [Key moments to emphasize]
- [Audience interaction points]
```

## Quality Checklist

- [ ] Opening captures attention in first 30 seconds
- [ ] One clear key message throughout
- [ ] Stories/examples are specific and relevant
- [ ] Language is conversational, not written-prose
- [ ] Timing fits the allocated slot
- [ ] Close is memorable and includes a call to action
- [ ] Delivery notes are included for the speaker

## Edge Cases

- For technical audiences, lead with the insight, then explain the method
- For eulogies or sensitive occasions, prioritize warmth over structure
- For panel prep, write talking points, not a full script
- If the speaker is not a native English speaker, simplify sentence structures
- For virtual delivery, add more engagement breaks (polls, questions)
