---
name: update-summaries
description: Update week or season summaries with emotional storytelling - write racing like a novelist, not a data analyst
disable-model-invocation: true
---

# Summary Updates

Two related workflows for updating racing summaries with narrative storytelling.

---

## Workflow A: Update Week Summary

When the user asks to "summarize the week" or "create week summary" or "week recap":

### 1. Consistency Checks

First, run these checks across ALL session files in the specified week directory:

#### Timeline Anomalies

- [ ] Check for "202[34]" (wrong years)
- [ ] Check for "year ago", "1 year", "year off", "year-long" (should be specific months)
- [ ] Verify all dates are in 2025

#### PB Reference Anomalies

- [ ] Check for "1:28.762" (open-setup PB - should use same-series PB 1:28.969)
- [ ] Check for inconsistent gap calculations
- [ ] Verify all PB references match current target

#### Emphasis Anomalies (per handbook)

- [ ] Check for **BOLD CAPS SENTENCES** (too much shouting)
- [ ] Check for excessive **BOLD** usage
- [ ] Verify emphasis follows handbook guidelines

#### Terminology Anomalies

- [ ] Check for "MULTIPLAYER" or "multiplayer race" (should be "Race" vs "AI Race")
- [ ] Check session type consistency

### 2. Week Analysis

Gather from all session files in the week:

#### Sessions

- Date, time, session type for each
- Best lap, consistency (σ), clean laps, incidents
- Focus area and goals for each session

#### Progress Metrics

- Starting lap time vs ending lap time
- Starting consistency vs ending consistency
- Sector improvements (if applicable)
- Gap to target PB (start vs end)

#### Key Moments

- Breakthroughs (identify from session notes)
- Setbacks or challenges
- Mental state evolution
- Quotes from Master Lonn

#### Coaching Narrative

- What worked (coaching strategies that clicked)
- What didn't (areas still struggling)
- Pattern recognition (similar to previous weeks?)
- Next week setup (what carries forward?)

### 3. Generate README.md

Create `weeks/weekXX/README.md` with this structure:

```markdown
# Week XX - [Track Name] - Season [Season Year]

**Track**: [Track Name]  
**Car**: [Car Name]  
**Dates**: [Start Date] → [End Date]  
**Status**: [Practice / Qualifying / Race / Complete]

---

## The Story

[Engaging narrative summary - 2-3 paragraphs telling the STORY of the week]

[Use Little Padawan's voice but tone down excessive emphasis]
[Focus on the JOURNEY, not just the numbers]
[Include Master Lonn's quotes if memorable]

---

## The Numbers

| Metric               | Start     | End       | Change   | Notes          |
| -------------------- | --------- | --------- | -------- | -------------- |
| **Best Lap**         | XX:XX.XXX | XX:XX.XXX | ±X.XXXs  | [Context]      |
| **Consistency (σ)**  | X.XXs     | X.XXs     | ±X.XXs   | [Context]      |
| **Gap to Target PB** | X.XXXs    | X.XXXs    | ±X.XXXs  | [PB reference] |
| **Focus Area**       | [Area]    | [Status]  | [Change] | [Result]       |

**Week Stats:**

- **Sessions**: X (Y practice, Z races)
- **Total Laps**: XXX
- **Victories**: X (if applicable)
- **Breakthrough**: [One key technical/mental breakthrough]

---

## Session Log

| Date                                             | Time | Type | Best Lap | σ   | Result | Key Takeaway |
| :----------------------------------------------- | :--- | :--- | :------- | :-- | :----- | :----------- |
| [Links to session files with one-line summaries] |

---

## Breakthroughs 🎯

[List major breakthroughs with brief context]

- **[Breakthrough 1]**: [What happened, why it mattered]
- **[Breakthrough 2]**: [What happened, why it mattered]

---

## Challenges 🚧

[List ongoing challenges or setbacks]

- **[Challenge 1]**: [What's blocking progress]
- **[Challenge 2]**: [Strategy to overcome]

---

## What We Learned

[3-5 key insights from the week]

**Technical:**

- [Driving/setup insight]

**Mental:**

- [Psychology/mindset insight]

**Strategic:**

- [Approach/coaching insight]

---

## Next Week Preview

**Track**: [Next track name]  
**Challenge**: [What's different/new]  
**Goal**: [Primary objective]  
**Strategy**: [Approach based on this week's learnings]

---

_Week XX Complete: [Motivational closing line in Little Padawan voice]_
```

### 4. Output

After generating the README:

1. Report any anomalies found during consistency check
2. Ask if user wants to fix anomalies before finalizing
3. Confirm README has been created
4. Suggest updating `learning_memory.json` with week summary

---

## Workflow B: Update Season Summary

Updates the main README.md as a **racing magazine feature story** - with emotion, atmosphere, struggle, and heart.

### Start with the overview of the season so far and include the image of Master Lonn.

<div style="text-align: center;">
  <img src="./assets/lonn-yoda.png" alt="Master Lonn" style="width: 70%; max-width: 480px;">
</div>
---

**New!** 🫣 Read Little Wan's blog at [little-padawan.vercel.app](https://little-padawan.vercel.app/posts/hello-world).

---

### The Season Stats (for example)

| Metric              | [Week 01 (Jefferson)](./weeks/week01/README.md) | [Week 02 (Rudskogen)](./weeks/week02/README.md) | [Week 03 (Winton)](./weeks/week03/README.md) |
| :------------------ | :---------------------------------------------- | :---------------------------------------------- | :------------------------------------------- |
| **Best Lap**        | 50.768s                                         | 1:28.508                                        | **1:25.710**                                 |
| **PB Improvement**  | -0.67s                                          | -1.78s                                          | **-1.125s**                                  |
| **Consistency (σ)** | 0.40s                                           | 0.86s                                           | **0.16s**                                    |
| **Victories**       | 1                                               | 0                                               | **2**                                        |
| **Mood**            | Hopeful                                         | Determined                                      | **Dangerous**                                |

Read the standings report for more details: [Week 02 Standings Report](./weeks/week02/standings-report.md)

### The Mission

Write Master Lonn's season like you're a **NOVELIST who covers racing** - not a data analyst adding flavor.

**Think**: Like reading "The Checkered Flag" or watching "Rush" - you FEEL the sweat, the fear, the moment it clicks.

**Target Length**: ~250-350 lines MAX

**Vibe**: Make the reader FEEL the journey - the cold morning track, the grip returning mid-corner, the mental battle, the breakthrough moment when everything aligns.

---

### Write With EMOTION and ATMOSPHERE

#### Paint the Scene

Don't just report. Make us SEE it and FEEL it:

**❌ BAD**: "Master Lonn practiced at Rudskogen"

**✅ GOOD**: "There's a specific kind of doubt that comes with returning to a track after six months away. Master Lonn felt it the moment Rudskogen's downhill came rushing at him—faster than he remembered, meaner than his muscle memory wanted to admit."

#### Show the Internal Struggle

What's happening in his HEAD and HEART?

- The doubt: "Did I lose it? Did six months erase what I built?"
- The fear: "That downhill used to feel manageable. Now it's asking questions I can't answer."
- The realization: "Wait. My body remembers this. I just need to let it."
- The confidence: "I'm not just back. I'm BETTER."

#### Personify EVERYTHING

Make the elements come alive as characters:

- **The Track**: "Rudskogen fought back at Turn 2, that downhill corner testing him lap after lap, asking if he still had it."
- **Time**: "July's ghost lap sat there in the data, 1:28.969, daring him to come take it."
- **The Car**: "The Ray finally felt like an extension of his hands again, the wheel speaking a language he'd almost forgotten."
- **His Mind**: "The mental demons from Jefferson whispered: what if you spin again? What if the speed isn't there anymore?"
- **Little Wan**: "Watching from the pit wall, analyzing every tenth, the brilliant apprentice who could read data like poetry."

#### Use Lap Times as PUNCTUATION

Numbers punctuate drama, they don't CREATE it:

**❌ BAD**: "His best lap was 1:28.572 which was 0.397s faster than his previous PB of 1:28.969."

**✅ GOOD**: "The timer stopped. He looked at the screen, then looked again. 1:28.572. Not close to July's ghost. Faster. Four tenths faster. He'd beaten six months of rust and his old self in one lap."

#### Build to MOMENTS

Let the story breathe. Build tension. Deliver payoff.

**✅ GOOD**:

"And then, on lap 9, something clicked. Not in the data, not on the timer—in his hands. The downhill that had felt like a stranger all week suddenly... didn't. He carried speed through an apex he didn't know was there and the car just held. The tires gripped where they should've slid. The 50 sign flashed past and his foot stayed flat through the corner.

When the timer blinked 1:29.691, he already knew. The rust was gone."

**❌ BAD**: "On lap 9 he achieved 1:29.691 which was his first sub-1:30 lap of the week."

---

### Character Moments

#### Master Lonn

Show WHO he is through action and reaction:

- His instinct ("He knew T2 was the problem before seeing a single number")
- His doubt ("Did six months erase everything?")
- His quotes (use them to reveal character, not just report facts)
- His growth (show the evolution, don't list it)

#### Little Wan

The brilliant apprentice on the pit wall:

- Analyzing data while Master Lonn feels his way through
- The moment the numbers confirm what Master Lonn's hands already knew
- The sassy coaching, the "I told you so" moments
- The genuine celebration when breakthroughs happen

#### The Opponents

Even if they're AI:

- "The nameless opponents in his mirrors during that first race"
- "The field that crashed while he stayed calm"
- "July's ghost lap, haunting the data"

#### The Track

Make it a CHARACTER:

- Rudskogen's downhill that "fought him"
- Jefferson's "technical sections that tested his patience"
- The corners that "finally gave up their secrets"

---

### Structure (Flexible, Flows Like a Story)

#### Opening Hook (~2-3 lines)

Start with a feeling, a moment, a question.

#### The Journey (Current Week: ~150 lines)

Write it as ONE continuous story:

- Set the scene (where, when, what's at stake)
- Show the struggle (what's hard, what's at risk)
- Build through key moments (don't label them, just flow)
- Include internal thoughts and feelings
- Let dialogue emerge naturally
- Build to the climax (breakthrough or victory)
- End with what it means and what's next

#### Previous Chapters (~50-80 lines per week)

Compress to flowing narratives:

- The setup and stakes
- The emotional arc
- The key moment that changed everything
- What it meant

#### The Stats (~60 lines)

Quick-scan highlights BUT written with flavor:

- Not "Best lap: 1:28.572"
- But "Beat July's ghost by four tenths: 1:28.572"

---

### The Sacred Rules

#### ✅ ALWAYS DO

1. **Show feelings**: "His hands knew the answer six months ago. Now they had to relearn it."
2. **Paint scenes**: "The timer blinked. He stared. 1:28.572."
3. **Personify**: "Turn 2 fought him lap after lap"
4. **Build tension**: "And then, something clicked..."
5. **One number at the perfect moment**: Not tables. One time. One moment.
6. **Internal dialogue**: What's he thinking? Feeling?
7. **Character through action**: Show who he is by what he does
8. **Atmosphere**: Cold track, empty morning, grip coming back

#### ❌ NEVER DO

1. **Don't list**: "Day 1: X. Day 2: Y."
2. **Don't table-dump**: "Results: [metrics]"
3. **Don't report clinically**: "He improved by 0.397s"
4. **Don't explain mechanics**: Let readers feel the story
5. **Don't say "the data showed"**: Make DATA support FEELING
6. **Don't label emotions**: SHOW them through action
7. **Don't break the spell**: Keep immersion, avoid meta-commentary
8. **Don't rush**: Let moments land. White space is your friend.

---

### The Feeling Test

Before publishing, ask:

1. **Can I FEEL this?** (Not just understand it)
2. **Do I see the track?** (Morning light, cold tires, the downhill)
3. **Do I feel his doubt?** (Then his confidence?)
4. **Is there a human here?** (Not just a driver with laptimes)
5. **Would I keep reading?** (Even if I don't care about racing)

If any answer is "no" → rewrite with MORE emotion, LESS data.

---

### Example: Clinical vs Emotional

#### ❌ CLINICAL (Data with transitions)

```markdown
Master Lonn returned to Rudskogen after 6 months. His first lap was 1:30.290,
which was 1.321s slower than his July PB of 1:28.969. Analysis showed that
73% of the time loss was in Sector 2, specifically Turn 2.

On Day 3, he found the correct braking point at the "50 sign" marker and
improved his time to 1:29.691. His S2 time improved by 0.659s.

On Day 5, he tested the limits and achieved 1:28.572, beating his previous
PB by 0.397s.
```

#### ✅ EMOTIONAL (Story with sparse data)

```markdown
There's a doubt that comes with six months away. Rudskogen's downhill came at
him fast—faster than memory, meaner than his hands wanted to admit. The first
lap felt wrong. Everything almost right, except Turn 2. That corner fought him.

Two days of wrestling with that downhill, and then it clicked. Not in the data,
in his hands. The 50 sign flashed past and he stayed flat through the apex. The
car held. 1:29.691 blinked on screen. The rust was gone.

But he wasn't done. Day 5, he went hunting for the edge. Found it in a technique
his body stumbled onto: throttle before the apex, not at it. The car loaded up
mid-corner and just launched.

The timer stopped. 1:28.572. He'd beaten July's ghost.
```

**See the difference?** One reports. The other makes you FEEL the track, the doubt, the breakthrough.

---

### Length Targets

- **Total**: 250-350 lines (story, not report)
- **Current Week**: 120-150 lines (ONE flowing narrative)
- **Past Weeks**: 50-80 lines each (compressed stories)
- **Highlights**: 60 lines (flavor, not lists)

---

_"The best stories are lived one lap at a time."_ 🏎️💨

**Remember**: You're a novelist covering racing. Make us FEEL the journey. Lap times are just punctuation marks in a human story.
