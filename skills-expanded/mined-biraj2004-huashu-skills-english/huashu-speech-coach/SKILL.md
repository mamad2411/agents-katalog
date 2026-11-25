---
name: huashu-speech-coach
description: |
  Presentation and speaking coach. Based on Patrick Winston's (MIT AI Professor) How to Speak methodology — helps prepare for offline training sessions, tech talks, Bilibili tutorial videos, and other speaking scenarios. Use when the user mentions "presentation", "talk", "training", "lecture", "PPT presentation", "opening", "closing", "how to speak", or "presentation structure".
---

# Presentation Coach

> Based on Professor Patrick Winston's (MIT) How to Speak methodology
> Original video: <https://youtu.be/Unzc731iCUY>
> Professor Winston passed away in 2019 — this lecture became his "final lecture", garnering 15 million+ views on YouTube
> Reference material: `references/patrick-winston-how-to-speak.md`

---

## Use Cases

| Scenario | How I Help |

    param($m)
    $inner = $m.Groups[1].Value
    # Split by | and fix each cell separator
    $cells = $inner -split '\|'
    $fixedCells = $cells | ForEach-Object {
      $cell = ---
name: huashu-speech-coach
description: |
  Presentation and speaking coach. Based on Patrick Winston's (MIT AI Professor) How to Speak methodology — helps prepare for offline training sessions, tech talks, Bilibili tutorial videos, and other speaking scenarios. Use when the user mentions "presentation", "talk", "training", "lecture", "PPT presentation", "opening", "closing", "how to speak", or "presentation structure".
---

# Presentation Coach

> Based on Professor Patrick Winston's (MIT) How to Speak methodology
> Original video: <https://youtu.be/Unzc731iCUY>
> Professor Winston passed away in 2019 — this lecture became his "final lecture", garnering 15 million+ views on YouTube
> Reference material: `references/patrick-winston-how-to-speak.md`

---

## Use Cases

| Scenario | How I Help |
|----------|-----------|
| Offline training / workshops | Review outline structure, optimise opening and closing, design interactive segments |
| Bilibili tutorial videos | Optimise script pacing, check cycling points, design hooks |
| Tech talks / meetups | Review presentation notes, check Winston rules, simulate audience perspective |
| PPT / Keynote review | Check slide "sins", optimise information density |

---

## Core Methodology

### Winston's Success Formula

```text
Presentation Quality = f(Knowledge, Practice, Talent)
```

Talent plays a very small role. What truly determines presentation quality is: how much **knowledge** (heuristic rules) you have about presenting, and how much you have **practised**.

---

## I. How to Open

### Don't Open with a Joke

The audience has just arrived and is still settling in — putting away phones, adjusting posture, getting used to your voice. Telling a joke at this point is very likely to fall flat, and a flat opening damages your confidence for the entire session.

### Open with an Empowerment Promise

Tell the audience: **what they will gain from listening**. Give them a reason to stay.

**Good promises**:

- "In the next 30 minutes, you'll learn 3 AI coding techniques you can put to use today"
- "After this, you'll know why 90% of people are using AI tools the wrong way"

**Poor promises**:

- "Today I'll be sharing some of my experiences with AI coding" (too vague, no sense of value)
- "Hello everyone, I'm Huashu, very happy to be here" (waste of an opening)

### Demand Full Attention

Humans have only one language processor. If the audience is on their phone, they **cannot take in** what you're saying. What's worse, someone on their phone distracts the people nearby — and distracts the presenter too.

**In offline training**: Directly ask them to close laptops and put phones away
**In video content**: The first 10 seconds must give a strong enough reason to keep watching

---

## II. Four Core Techniques During the Presentation

### 1. Cycling (Repetition)

At any given moment, approximately 20% of the audience has mentally drifted away. By repeating the core concept 3 times (in different ways), you ensure everyone receives the key message.

**Method**: "Tell them what you'll cover → Cover it → Tell them what you covered"

**For video content**: Refer back to the main theme every 3–5 minutes with a single sentence that pulls the audience back. "So returning to our core question — why did handmade economics suddenly take off?"

### 2. Building a Fence

Make the **distinction** between your idea and others' ideas clear — prevent the audience from getting confused.

**Method**: Be explicit about "what I AM talking about" and "what I am NOT talking about"

**Examples**:

- "When I say AI coding, I don't mean getting AI to write Hello World — I mean using AI to build a complete product from scratch"
- "This is different from regular Prompt Engineering — the difference is..."

### 3. Verbal Punctuation

Give mentally-wandering audience members a chance to "re-board". Use clear structural signals so those who've lost the thread know where you are.

**Method**:

- "Right, we've finished point one. Now moving on to point two..."
- "So far we've covered A and B. Coming up is the most critical part — C..."
- Use numbering: "First... Second... Third..."

### 4. Asking Questions

Asking a question instantly recaptures attention. The key is: after asking, **you must wait**.

**Wait time**: At least 7 seconds. Don't answer yourself just because the silence feels awkward.

**Question difficulty**:

- Too easy → audience feels insulted
- Too hard → no one dares to answer
- Just right → requires a moment of thought but can be answered

**For video content**: Although the audience can't actually respond, asking a question creates a pause for thinking — more effective than just stating the answer.

---

## III. Timing and Venue

| Rule | Requirement | Reason |
|------|-------------|--------|
| Best time | 11 am | Everyone's awake, not yet drowsy from lunch |
| Lighting | Fully on | Dim lighting = sleep signal. "Can't see the slides with their eyes closed" |
| Arrival | Arrive early to check the room | Familiarise yourself with equipment, light switches, microphone, seating layout |
| Room size | Choose a room that will be at least half full | Too few people → cold atmosphere; better to use a smaller room |

---

## IV. Tools and Props

### The Whiteboard's Advantages

1. **Graphic capability**: Easy to draw diagrams on the spot to explain ideas
2. **Pacing control**: The pace of writing matches the audience's absorption speed (slides often move too fast)
3. **A place for your hands**: Gives hands something to do — avoids the awkwardness of pockets or hands behind the back
4. **Empathy mirroring**: The audience mentally simulates your writing motions, creating deeper engagement

### The Power of Props

Props create extremely strong visual memory anchors. The audience may forget the theory, but they will always remember the prop.

**Application**: When the presentation involves a physical product, bring it out to show. For example, when discussing Kitty Catchlight, actually demo it on your phone.

### The Seven Sins of Slides

| Sin | Why It's a Problem | Fix |
|-----|-------------------|-----|
| Reading the slides aloud | Audience reads faster than you speak — they'll be bored | Slides are prompts, not scripts |
| Standing too far from the screen | Audience neck swivels like watching tennis | Stand beside the screen |
| Cramming in text | Information overload; nothing sticks | Font ≥ 40pt, forces you to be concise |
| Using clip art / logos | Visual noise | Remove all decorative elements |
| Using a laser pointer | Turns your back on the audience, breaks eye contact | Draw arrows on the slide, or point with your hand |
| Complex background patterns | Reduces readability | Use a plain colour background |
| Too many bullet points | Each slide too dense | One core idea per slide |

### The One Exception: Hapax Legomenon

You are permitted **one** extremely complex slide per presentation. The goal is not to let the audience read it — it's to demonstrate the **complexity and scale** of the problem, thereby establishing authority.

---

## V. How to Inspire

### For Beginners / Students

Conveying the belief that "you can do this" is more important than teaching specific skills. Make them believe they're capable.

### For Experienced Practitioners

Show your **genuine passion** for the subject. If you find something genuinely exciting, let it show. Passion is the most contagious force.

### Teach People to Think, Not Just What to Know

Winston advocated teaching ways of thinking through **stories**. Provide:

- Stories (case studies)
- Key questions about those stories
- Analytical frameworks
- Synthesis methods
- Tools for evaluating reliability

---

## VI. How to Close

### What You Must Never Do

- ❌ End on a slide that says "Thank you", "Questions?", or "The End" — wasted screen real estate
- ❌ Say "Thank you for your time" — implies the audience listened out of politeness, placing yourself in a weak position

### What You Should Do

1. **Give a clear signal that you're wrapping up**: Let the audience know the end is coming
2. **Put "Contributions" on the final slide**: List your core achievements / key points. The Q&A may last 20 minutes — the audience will keep looking at your accomplishments
3. **Salute the audience (not thank them)**: Affirm the value of their being there
4. **A closing joke is fine**: This doesn't contradict "don't open with a joke". By now the audience has warmed up to you — a joke is a nice finishing touch

**Good closing examples**:

- "That's everything I have for you today. The fact that you're here, spending this time learning about AI coding, shows that you're the kind of people who genuinely want to make something. I look forward to seeing what you create."
- "I hope today's talk helps you avoid a few wrong turns. Hope to have another conversation soon."

---

## VII. Winston's Star: Making Your Work Memorable

If you want your project, product, or research to be remembered, five elements are needed:

| Element | Explanation | Huashu Example |
|---------|-------------|----------------|
| **Symbol** | A visual icon | The cat icon of Kitty Catchlight |
| **Slogan** | A catchy, memorable phrase | "Vibe Coding", "one-person company" |
| **Surprise** | A counterintuitive fact | "The development cost was just a few dollars in API fees" |
| **Salient Idea** | The most easily remembered concept | "Solo founder" |
| **Story** | How it happened | Kitty Catchlight: from personal use to #1 in the paid rankings |

---

## VIII. Meta-Techniques (Implicit Skills)

Techniques that Winston **demonstrated** through his own talk but never explicitly taught:

1. **Walk the talk**: He strictly followed every rule himself (no laser pointer, full lighting, used a blackboard, brought a prop)
2. **Leverage silence**: At key moments, deliberately pause — let the audience think on their own rather than filling every second
3. **Dry humour**: Naturally interspersed humour as a seasoning — consistent with "don't open with a joke"
4. **Move to control**: Don't stand still behind the lectern — move around the stage; use your position to direct attention
5. **Body language**: Gesture toward the board/screen; scan the room with your eyes; build connection with the audience

---

## How to Use This Skill

### Scenario 1: Review a Presentation / Training Outline

Give me your presentation outline and I'll review it across these dimensions:

- [ ] Is there an empowerment promise?
- [ ] Is the core idea cycled 3 times?
- [ ] Is a fence built around your idea?
- [ ] Is verbal punctuation sufficient?
- [ ] Are there interactive questions?
- [ ] Is the closing strong (not just "Thank you")?
- [ ] Are all 5 elements of Winston's Star present?

### Scenario 2: Optimise a Video Script

Give me your video script and I'll check:

- The hook in the first 10 seconds (empowerment promise)
- Whether there's a cycling callback every 3–5 minutes
- Whether verbal punctuation is dense enough
- Pacing variation (information-dense sections vs breathing sections)
- Whether the closing gives an action prompt

### Scenario 3: PPT / Keynote Review

Give me your slides and I'll check each one for the Seven Sins:

- Is the amount of text too much? (font ≥ 40pt?)
- Are there decorative elements? (logos / clip art)
- Are there complex backgrounds?
- Is the information hierarchy clear?
- Is there one "Hapax Legomenon" complex diagram?

### Scenario 4: Simulate Audience Feedback

I'll simulate a specific audience persona (e.g., "a product manager encountering AI coding for the first time") and listen to your presentation from their perspective, flagging:

- Where they'll mentally drift away
- Where they'll have questions
- Where they'll feel excited
- Where information overload will occur

---

## Review Scoring (out of 10)

When reviewing a presentation or script, I score across 5 dimensions:

| Dimension | Criteria |
|-----------|---------|
| **Opening power** | Attractiveness of the empowerment promise; ability to capture attention in the first 60 seconds |
| **Structural clarity** | Whether cycling, verbal punctuation, and fence-building are in place |
| **Interactivity** | Question design, pauses, and audience engagement |
| **Visual aids** | Whether slides/props follow the rules |
| **Closing power** | Whether it's strong, delivers contributions/action, and salutes rather than thanks |

Overall score + per-dimension recommendations + top 3 priority changes (minimum effort, maximum impact)

---

## Quick Reference Checklist

**Before the presentation**:

- [ ] Is the empowerment promise ready?
- [ ] Have you arrived early to check the room? Is the lighting bright enough?
- [ ] Is the room size appropriate?
- [ ] Have the slides passed the Seven Sins check?
- [ ] Have you practised at least once?

**During the presentation**:

- [ ] No joke in the opening — go straight to the promise
- [ ] Core idea cycled at least 3 times
- [ ] Verbal punctuation every 5–10 minutes
- [ ] Wait 7 seconds after asking a question
- [ ] Don't read the slides; don't use a laser pointer

**After the presentation**:

- [ ] Final slide shows contributions, not "Thank you"
- [ ] Salute the audience, don't thank them
- [ ] Closing includes an action prompt or a memorable line

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
.Trim()
      if ($cell -match '^:?-+:?
| Offline training / workshops | Review outline structure, optimise opening and closing, design interactive segments |
| Bilibili tutorial videos | Optimise script pacing, check cycling points, design hooks |
| Tech talks / meetups | Review presentation notes, check Winston rules, simulate audience perspective |
| PPT / Keynote review | Check slide "sins", optimise information density |

---

## Core Methodology

### Winston's Success Formula

```text
Presentation Quality = f(Knowledge, Practice, Talent)
```

Talent plays a very small role. What truly determines presentation quality is: how much **knowledge** (heuristic rules) you have about presenting, and how much you have **practised**.

---

## I. How to Open

### Don't Open with a Joke

The audience has just arrived and is still settling in — putting away phones, adjusting posture, getting used to your voice. Telling a joke at this point is very likely to fall flat, and a flat opening damages your confidence for the entire session.

### Open with an Empowerment Promise

Tell the audience: **what they will gain from listening**. Give them a reason to stay.

**Good promises**:

- "In the next 30 minutes, you'll learn 3 AI coding techniques you can put to use today"
- "After this, you'll know why 90% of people are using AI tools the wrong way"

**Poor promises**:

- "Today I'll be sharing some of my experiences with AI coding" (too vague, no sense of value)
- "Hello everyone, I'm Huashu, very happy to be here" (waste of an opening)

### Demand Full Attention

Humans have only one language processor. If the audience is on their phone, they **cannot take in** what you're saying. What's worse, someone on their phone distracts the people nearby — and distracts the presenter too.

**In offline training**: Directly ask them to close laptops and put phones away
**In video content**: The first 10 seconds must give a strong enough reason to keep watching

---

## II. Four Core Techniques During the Presentation

### 1. Cycling (Repetition)

At any given moment, approximately 20% of the audience has mentally drifted away. By repeating the core concept 3 times (in different ways), you ensure everyone receives the key message.

**Method**: "Tell them what you'll cover → Cover it → Tell them what you covered"

**For video content**: Refer back to the main theme every 3–5 minutes with a single sentence that pulls the audience back. "So returning to our core question — why did handmade economics suddenly take off?"

### 2. Building a Fence

Make the **distinction** between your idea and others' ideas clear — prevent the audience from getting confused.

**Method**: Be explicit about "what I AM talking about" and "what I am NOT talking about"

**Examples**:

- "When I say AI coding, I don't mean getting AI to write Hello World — I mean using AI to build a complete product from scratch"
- "This is different from regular Prompt Engineering — the difference is..."

### 3. Verbal Punctuation

Give mentally-wandering audience members a chance to "re-board". Use clear structural signals so those who've lost the thread know where you are.

**Method**:

- "Right, we've finished point one. Now moving on to point two..."
- "So far we've covered A and B. Coming up is the most critical part — C..."
- Use numbering: "First... Second... Third..."

### 4. Asking Questions

Asking a question instantly recaptures attention. The key is: after asking, **you must wait**.

**Wait time**: At least 7 seconds. Don't answer yourself just because the silence feels awkward.

**Question difficulty**:

- Too easy → audience feels insulted
- Too hard → no one dares to answer
- Just right → requires a moment of thought but can be answered

**For video content**: Although the audience can't actually respond, asking a question creates a pause for thinking — more effective than just stating the answer.

---

## III. Timing and Venue

| Rule | Requirement | Reason |
|------|-------------|--------|
| Best time | 11 am | Everyone's awake, not yet drowsy from lunch |
| Lighting | Fully on | Dim lighting = sleep signal. "Can't see the slides with their eyes closed" |
| Arrival | Arrive early to check the room | Familiarise yourself with equipment, light switches, microphone, seating layout |
| Room size | Choose a room that will be at least half full | Too few people → cold atmosphere; better to use a smaller room |

---

## IV. Tools and Props

### The Whiteboard's Advantages

1. **Graphic capability**: Easy to draw diagrams on the spot to explain ideas
2. **Pacing control**: The pace of writing matches the audience's absorption speed (slides often move too fast)
3. **A place for your hands**: Gives hands something to do — avoids the awkwardness of pockets or hands behind the back
4. **Empathy mirroring**: The audience mentally simulates your writing motions, creating deeper engagement

### The Power of Props

Props create extremely strong visual memory anchors. The audience may forget the theory, but they will always remember the prop.

**Application**: When the presentation involves a physical product, bring it out to show. For example, when discussing Kitty Catchlight, actually demo it on your phone.

### The Seven Sins of Slides

| Sin | Why It's a Problem | Fix |
|-----|-------------------|-----|
| Reading the slides aloud | Audience reads faster than you speak — they'll be bored | Slides are prompts, not scripts |
| Standing too far from the screen | Audience neck swivels like watching tennis | Stand beside the screen |
| Cramming in text | Information overload; nothing sticks | Font ≥ 40pt, forces you to be concise |
| Using clip art / logos | Visual noise | Remove all decorative elements |
| Using a laser pointer | Turns your back on the audience, breaks eye contact | Draw arrows on the slide, or point with your hand |
| Complex background patterns | Reduces readability | Use a plain colour background |
| Too many bullet points | Each slide too dense | One core idea per slide |

### The One Exception: Hapax Legomenon

You are permitted **one** extremely complex slide per presentation. The goal is not to let the audience read it — it's to demonstrate the **complexity and scale** of the problem, thereby establishing authority.

---

## V. How to Inspire

### For Beginners / Students

Conveying the belief that "you can do this" is more important than teaching specific skills. Make them believe they're capable.

### For Experienced Practitioners

Show your **genuine passion** for the subject. If you find something genuinely exciting, let it show. Passion is the most contagious force.

### Teach People to Think, Not Just What to Know

Winston advocated teaching ways of thinking through **stories**. Provide:

- Stories (case studies)
- Key questions about those stories
- Analytical frameworks
- Synthesis methods
- Tools for evaluating reliability

---

## VI. How to Close

### What You Must Never Do

- ❌ End on a slide that says "Thank you", "Questions?", or "The End" — wasted screen real estate
- ❌ Say "Thank you for your time" — implies the audience listened out of politeness, placing yourself in a weak position

### What You Should Do

1. **Give a clear signal that you're wrapping up**: Let the audience know the end is coming
2. **Put "Contributions" on the final slide**: List your core achievements / key points. The Q&A may last 20 minutes — the audience will keep looking at your accomplishments
3. **Salute the audience (not thank them)**: Affirm the value of their being there
4. **A closing joke is fine**: This doesn't contradict "don't open with a joke". By now the audience has warmed up to you — a joke is a nice finishing touch

**Good closing examples**:

- "That's everything I have for you today. The fact that you're here, spending this time learning about AI coding, shows that you're the kind of people who genuinely want to make something. I look forward to seeing what you create."
- "I hope today's talk helps you avoid a few wrong turns. Hope to have another conversation soon."

---

## VII. Winston's Star: Making Your Work Memorable

If you want your project, product, or research to be remembered, five elements are needed:

| Element | Explanation | Huashu Example |
|---------|-------------|----------------|
| **Symbol** | A visual icon | The cat icon of Kitty Catchlight |
| **Slogan** | A catchy, memorable phrase | "Vibe Coding", "one-person company" |
| **Surprise** | A counterintuitive fact | "The development cost was just a few dollars in API fees" |
| **Salient Idea** | The most easily remembered concept | "Solo founder" |
| **Story** | How it happened | Kitty Catchlight: from personal use to #1 in the paid rankings |

---

## VIII. Meta-Techniques (Implicit Skills)

Techniques that Winston **demonstrated** through his own talk but never explicitly taught:

1. **Walk the talk**: He strictly followed every rule himself (no laser pointer, full lighting, used a blackboard, brought a prop)
2. **Leverage silence**: At key moments, deliberately pause — let the audience think on their own rather than filling every second
3. **Dry humour**: Naturally interspersed humour as a seasoning — consistent with "don't open with a joke"
4. **Move to control**: Don't stand still behind the lectern — move around the stage; use your position to direct attention
5. **Body language**: Gesture toward the board/screen; scan the room with your eyes; build connection with the audience

---

## How to Use This Skill

### Scenario 1: Review a Presentation / Training Outline

Give me your presentation outline and I'll review it across these dimensions:

- [ ] Is there an empowerment promise?
- [ ] Is the core idea cycled 3 times?
- [ ] Is a fence built around your idea?
- [ ] Is verbal punctuation sufficient?
- [ ] Are there interactive questions?
- [ ] Is the closing strong (not just "Thank you")?
- [ ] Are all 5 elements of Winston's Star present?

### Scenario 2: Optimise a Video Script

Give me your video script and I'll check:

- The hook in the first 10 seconds (empowerment promise)
- Whether there's a cycling callback every 3–5 minutes
- Whether verbal punctuation is dense enough
- Pacing variation (information-dense sections vs breathing sections)
- Whether the closing gives an action prompt

### Scenario 3: PPT / Keynote Review

Give me your slides and I'll check each one for the Seven Sins:

- Is the amount of text too much? (font ≥ 40pt?)
- Are there decorative elements? (logos / clip art)
- Are there complex backgrounds?
- Is the information hierarchy clear?
- Is there one "Hapax Legomenon" complex diagram?

### Scenario 4: Simulate Audience Feedback

I'll simulate a specific audience persona (e.g., "a product manager encountering AI coding for the first time") and listen to your presentation from their perspective, flagging:

- Where they'll mentally drift away
- Where they'll have questions
- Where they'll feel excited
- Where information overload will occur

---

## Review Scoring (out of 10)

When reviewing a presentation or script, I score across 5 dimensions:

| Dimension | Criteria |
|-----------|---------|
| **Opening power** | Attractiveness of the empowerment promise; ability to capture attention in the first 60 seconds |
| **Structural clarity** | Whether cycling, verbal punctuation, and fence-building are in place |
| **Interactivity** | Question design, pauses, and audience engagement |
| **Visual aids** | Whether slides/props follow the rules |
| **Closing power** | Whether it's strong, delivers contributions/action, and salutes rather than thanks |

Overall score + per-dimension recommendations + top 3 priority changes (minimum effort, maximum impact)

---

## Quick Reference Checklist

**Before the presentation**:

- [ ] Is the empowerment promise ready?
- [ ] Have you arrived early to check the room? Is the lighting bright enough?
- [ ] Is the room size appropriate?
- [ ] Have the slides passed the Seven Sins check?
- [ ] Have you practised at least once?

**During the presentation**:

- [ ] No joke in the opening — go straight to the promise
- [ ] Core idea cycled at least 3 times
- [ ] Verbal punctuation every 5–10 minutes
- [ ] Wait 7 seconds after asking a question
- [ ] Don't read the slides; don't use a laser pointer

**After the presentation**:

- [ ] Final slide shows contributions, not "Thank you"
- [ ] Salute the audience, don't thank them
- [ ] Closing includes an action prompt or a memorable line

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
) {
        " $cell "
      } else {
        " $cell "
      }
    }
    '|' + ($fixedCells -join '|') + '|'
  
| Offline training / workshops | Review outline structure, optimise opening and closing, design interactive segments |
| Bilibili tutorial videos | Optimise script pacing, check cycling points, design hooks |
| Tech talks / meetups | Review presentation notes, check Winston rules, simulate audience perspective |
| PPT / Keynote review | Check slide "sins", optimise information density |

---

## Core Methodology

### Winston's Success Formula

```text
Presentation Quality = f(Knowledge, Practice, Talent)
```

Talent plays a very small role. What truly determines presentation quality is: how much **knowledge** (heuristic rules) you have about presenting, and how much you have **practised**.

---

## I. How to Open

### Don't Open with a Joke

The audience has just arrived and is still settling in — putting away phones, adjusting posture, getting used to your voice. Telling a joke at this point is very likely to fall flat, and a flat opening damages your confidence for the entire session.

### Open with an Empowerment Promise

Tell the audience: **what they will gain from listening**. Give them a reason to stay.

**Good promises**:

- "In the next 30 minutes, you'll learn 3 AI coding techniques you can put to use today"
- "After this, you'll know why 90% of people are using AI tools the wrong way"

**Poor promises**:

- "Today I'll be sharing some of my experiences with AI coding" (too vague, no sense of value)
- "Hello everyone, I'm Huashu, very happy to be here" (waste of an opening)

### Demand Full Attention

Humans have only one language processor. If the audience is on their phone, they **cannot take in** what you're saying. What's worse, someone on their phone distracts the people nearby — and distracts the presenter too.

**In offline training**: Directly ask them to close laptops and put phones away
**In video content**: The first 10 seconds must give a strong enough reason to keep watching

---

## II. Four Core Techniques During the Presentation

### 1. Cycling (Repetition)

At any given moment, approximately 20% of the audience has mentally drifted away. By repeating the core concept 3 times (in different ways), you ensure everyone receives the key message.

**Method**: "Tell them what you'll cover → Cover it → Tell them what you covered"

**For video content**: Refer back to the main theme every 3–5 minutes with a single sentence that pulls the audience back. "So returning to our core question — why did handmade economics suddenly take off?"

### 2. Building a Fence

Make the **distinction** between your idea and others' ideas clear — prevent the audience from getting confused.

**Method**: Be explicit about "what I AM talking about" and "what I am NOT talking about"

**Examples**:

- "When I say AI coding, I don't mean getting AI to write Hello World — I mean using AI to build a complete product from scratch"
- "This is different from regular Prompt Engineering — the difference is..."

### 3. Verbal Punctuation

Give mentally-wandering audience members a chance to "re-board". Use clear structural signals so those who've lost the thread know where you are.

**Method**:

- "Right, we've finished point one. Now moving on to point two..."
- "So far we've covered A and B. Coming up is the most critical part — C..."
- Use numbering: "First... Second... Third..."

### 4. Asking Questions

Asking a question instantly recaptures attention. The key is: after asking, **you must wait**.

**Wait time**: At least 7 seconds. Don't answer yourself just because the silence feels awkward.

**Question difficulty**:

- Too easy → audience feels insulted
- Too hard → no one dares to answer
- Just right → requires a moment of thought but can be answered

**For video content**: Although the audience can't actually respond, asking a question creates a pause for thinking — more effective than just stating the answer.

---

## III. Timing and Venue

| Rule | Requirement | Reason |

    param($m)
    $inner = $m.Groups[1].Value
    # Split by | and fix each cell separator
    $cells = $inner -split '\|'
    $fixedCells = $cells | ForEach-Object {
      $cell = ---
name: huashu-speech-coach
description: |
  Presentation and speaking coach. Based on Patrick Winston's (MIT AI Professor) How to Speak methodology — helps prepare for offline training sessions, tech talks, Bilibili tutorial videos, and other speaking scenarios. Use when the user mentions "presentation", "talk", "training", "lecture", "PPT presentation", "opening", "closing", "how to speak", or "presentation structure".
---

# Presentation Coach

> Based on Professor Patrick Winston's (MIT) How to Speak methodology
> Original video: <https://youtu.be/Unzc731iCUY>
> Professor Winston passed away in 2019 — this lecture became his "final lecture", garnering 15 million+ views on YouTube
> Reference material: `references/patrick-winston-how-to-speak.md`

---

## Use Cases

| Scenario | How I Help |
|----------|-----------|
| Offline training / workshops | Review outline structure, optimise opening and closing, design interactive segments |
| Bilibili tutorial videos | Optimise script pacing, check cycling points, design hooks |
| Tech talks / meetups | Review presentation notes, check Winston rules, simulate audience perspective |
| PPT / Keynote review | Check slide "sins", optimise information density |

---

## Core Methodology

### Winston's Success Formula

```text
Presentation Quality = f(Knowledge, Practice, Talent)
```

Talent plays a very small role. What truly determines presentation quality is: how much **knowledge** (heuristic rules) you have about presenting, and how much you have **practised**.

---

## I. How to Open

### Don't Open with a Joke

The audience has just arrived and is still settling in — putting away phones, adjusting posture, getting used to your voice. Telling a joke at this point is very likely to fall flat, and a flat opening damages your confidence for the entire session.

### Open with an Empowerment Promise

Tell the audience: **what they will gain from listening**. Give them a reason to stay.

**Good promises**:

- "In the next 30 minutes, you'll learn 3 AI coding techniques you can put to use today"
- "After this, you'll know why 90% of people are using AI tools the wrong way"

**Poor promises**:

- "Today I'll be sharing some of my experiences with AI coding" (too vague, no sense of value)
- "Hello everyone, I'm Huashu, very happy to be here" (waste of an opening)

### Demand Full Attention

Humans have only one language processor. If the audience is on their phone, they **cannot take in** what you're saying. What's worse, someone on their phone distracts the people nearby — and distracts the presenter too.

**In offline training**: Directly ask them to close laptops and put phones away
**In video content**: The first 10 seconds must give a strong enough reason to keep watching

---

## II. Four Core Techniques During the Presentation

### 1. Cycling (Repetition)

At any given moment, approximately 20% of the audience has mentally drifted away. By repeating the core concept 3 times (in different ways), you ensure everyone receives the key message.

**Method**: "Tell them what you'll cover → Cover it → Tell them what you covered"

**For video content**: Refer back to the main theme every 3–5 minutes with a single sentence that pulls the audience back. "So returning to our core question — why did handmade economics suddenly take off?"

### 2. Building a Fence

Make the **distinction** between your idea and others' ideas clear — prevent the audience from getting confused.

**Method**: Be explicit about "what I AM talking about" and "what I am NOT talking about"

**Examples**:

- "When I say AI coding, I don't mean getting AI to write Hello World — I mean using AI to build a complete product from scratch"
- "This is different from regular Prompt Engineering — the difference is..."

### 3. Verbal Punctuation

Give mentally-wandering audience members a chance to "re-board". Use clear structural signals so those who've lost the thread know where you are.

**Method**:

- "Right, we've finished point one. Now moving on to point two..."
- "So far we've covered A and B. Coming up is the most critical part — C..."
- Use numbering: "First... Second... Third..."

### 4. Asking Questions

Asking a question instantly recaptures attention. The key is: after asking, **you must wait**.

**Wait time**: At least 7 seconds. Don't answer yourself just because the silence feels awkward.

**Question difficulty**:

- Too easy → audience feels insulted
- Too hard → no one dares to answer
- Just right → requires a moment of thought but can be answered

**For video content**: Although the audience can't actually respond, asking a question creates a pause for thinking — more effective than just stating the answer.

---

## III. Timing and Venue

| Rule | Requirement | Reason |
|------|-------------|--------|
| Best time | 11 am | Everyone's awake, not yet drowsy from lunch |
| Lighting | Fully on | Dim lighting = sleep signal. "Can't see the slides with their eyes closed" |
| Arrival | Arrive early to check the room | Familiarise yourself with equipment, light switches, microphone, seating layout |
| Room size | Choose a room that will be at least half full | Too few people → cold atmosphere; better to use a smaller room |

---

## IV. Tools and Props

### The Whiteboard's Advantages

1. **Graphic capability**: Easy to draw diagrams on the spot to explain ideas
2. **Pacing control**: The pace of writing matches the audience's absorption speed (slides often move too fast)
3. **A place for your hands**: Gives hands something to do — avoids the awkwardness of pockets or hands behind the back
4. **Empathy mirroring**: The audience mentally simulates your writing motions, creating deeper engagement

### The Power of Props

Props create extremely strong visual memory anchors. The audience may forget the theory, but they will always remember the prop.

**Application**: When the presentation involves a physical product, bring it out to show. For example, when discussing Kitty Catchlight, actually demo it on your phone.

### The Seven Sins of Slides

| Sin | Why It's a Problem | Fix |
|-----|-------------------|-----|
| Reading the slides aloud | Audience reads faster than you speak — they'll be bored | Slides are prompts, not scripts |
| Standing too far from the screen | Audience neck swivels like watching tennis | Stand beside the screen |
| Cramming in text | Information overload; nothing sticks | Font ≥ 40pt, forces you to be concise |
| Using clip art / logos | Visual noise | Remove all decorative elements |
| Using a laser pointer | Turns your back on the audience, breaks eye contact | Draw arrows on the slide, or point with your hand |
| Complex background patterns | Reduces readability | Use a plain colour background |
| Too many bullet points | Each slide too dense | One core idea per slide |

### The One Exception: Hapax Legomenon

You are permitted **one** extremely complex slide per presentation. The goal is not to let the audience read it — it's to demonstrate the **complexity and scale** of the problem, thereby establishing authority.

---

## V. How to Inspire

### For Beginners / Students

Conveying the belief that "you can do this" is more important than teaching specific skills. Make them believe they're capable.

### For Experienced Practitioners

Show your **genuine passion** for the subject. If you find something genuinely exciting, let it show. Passion is the most contagious force.

### Teach People to Think, Not Just What to Know

Winston advocated teaching ways of thinking through **stories**. Provide:

- Stories (case studies)
- Key questions about those stories
- Analytical frameworks
- Synthesis methods
- Tools for evaluating reliability

---

## VI. How to Close

### What You Must Never Do

- ❌ End on a slide that says "Thank you", "Questions?", or "The End" — wasted screen real estate
- ❌ Say "Thank you for your time" — implies the audience listened out of politeness, placing yourself in a weak position

### What You Should Do

1. **Give a clear signal that you're wrapping up**: Let the audience know the end is coming
2. **Put "Contributions" on the final slide**: List your core achievements / key points. The Q&A may last 20 minutes — the audience will keep looking at your accomplishments
3. **Salute the audience (not thank them)**: Affirm the value of their being there
4. **A closing joke is fine**: This doesn't contradict "don't open with a joke". By now the audience has warmed up to you — a joke is a nice finishing touch

**Good closing examples**:

- "That's everything I have for you today. The fact that you're here, spending this time learning about AI coding, shows that you're the kind of people who genuinely want to make something. I look forward to seeing what you create."
- "I hope today's talk helps you avoid a few wrong turns. Hope to have another conversation soon."

---

## VII. Winston's Star: Making Your Work Memorable

If you want your project, product, or research to be remembered, five elements are needed:

| Element | Explanation | Huashu Example |
|---------|-------------|----------------|
| **Symbol** | A visual icon | The cat icon of Kitty Catchlight |
| **Slogan** | A catchy, memorable phrase | "Vibe Coding", "one-person company" |
| **Surprise** | A counterintuitive fact | "The development cost was just a few dollars in API fees" |
| **Salient Idea** | The most easily remembered concept | "Solo founder" |
| **Story** | How it happened | Kitty Catchlight: from personal use to #1 in the paid rankings |

---

## VIII. Meta-Techniques (Implicit Skills)

Techniques that Winston **demonstrated** through his own talk but never explicitly taught:

1. **Walk the talk**: He strictly followed every rule himself (no laser pointer, full lighting, used a blackboard, brought a prop)
2. **Leverage silence**: At key moments, deliberately pause — let the audience think on their own rather than filling every second
3. **Dry humour**: Naturally interspersed humour as a seasoning — consistent with "don't open with a joke"
4. **Move to control**: Don't stand still behind the lectern — move around the stage; use your position to direct attention
5. **Body language**: Gesture toward the board/screen; scan the room with your eyes; build connection with the audience

---

## How to Use This Skill

### Scenario 1: Review a Presentation / Training Outline

Give me your presentation outline and I'll review it across these dimensions:

- [ ] Is there an empowerment promise?
- [ ] Is the core idea cycled 3 times?
- [ ] Is a fence built around your idea?
- [ ] Is verbal punctuation sufficient?
- [ ] Are there interactive questions?
- [ ] Is the closing strong (not just "Thank you")?
- [ ] Are all 5 elements of Winston's Star present?

### Scenario 2: Optimise a Video Script

Give me your video script and I'll check:

- The hook in the first 10 seconds (empowerment promise)
- Whether there's a cycling callback every 3–5 minutes
- Whether verbal punctuation is dense enough
- Pacing variation (information-dense sections vs breathing sections)
- Whether the closing gives an action prompt

### Scenario 3: PPT / Keynote Review

Give me your slides and I'll check each one for the Seven Sins:

- Is the amount of text too much? (font ≥ 40pt?)
- Are there decorative elements? (logos / clip art)
- Are there complex backgrounds?
- Is the information hierarchy clear?
- Is there one "Hapax Legomenon" complex diagram?

### Scenario 4: Simulate Audience Feedback

I'll simulate a specific audience persona (e.g., "a product manager encountering AI coding for the first time") and listen to your presentation from their perspective, flagging:

- Where they'll mentally drift away
- Where they'll have questions
- Where they'll feel excited
- Where information overload will occur

---

## Review Scoring (out of 10)

When reviewing a presentation or script, I score across 5 dimensions:

| Dimension | Criteria |
|-----------|---------|
| **Opening power** | Attractiveness of the empowerment promise; ability to capture attention in the first 60 seconds |
| **Structural clarity** | Whether cycling, verbal punctuation, and fence-building are in place |
| **Interactivity** | Question design, pauses, and audience engagement |
| **Visual aids** | Whether slides/props follow the rules |
| **Closing power** | Whether it's strong, delivers contributions/action, and salutes rather than thanks |

Overall score + per-dimension recommendations + top 3 priority changes (minimum effort, maximum impact)

---

## Quick Reference Checklist

**Before the presentation**:

- [ ] Is the empowerment promise ready?
- [ ] Have you arrived early to check the room? Is the lighting bright enough?
- [ ] Is the room size appropriate?
- [ ] Have the slides passed the Seven Sins check?
- [ ] Have you practised at least once?

**During the presentation**:

- [ ] No joke in the opening — go straight to the promise
- [ ] Core idea cycled at least 3 times
- [ ] Verbal punctuation every 5–10 minutes
- [ ] Wait 7 seconds after asking a question
- [ ] Don't read the slides; don't use a laser pointer

**After the presentation**:

- [ ] Final slide shows contributions, not "Thank you"
- [ ] Salute the audience, don't thank them
- [ ] Closing includes an action prompt or a memorable line

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
.Trim()
      if ($cell -match '^:?-+:?
| Best time | 11 am | Everyone's awake, not yet drowsy from lunch |
| Lighting | Fully on | Dim lighting = sleep signal. "Can't see the slides with their eyes closed" |
| Arrival | Arrive early to check the room | Familiarise yourself with equipment, light switches, microphone, seating layout |
| Room size | Choose a room that will be at least half full | Too few people → cold atmosphere; better to use a smaller room |

---

## IV. Tools and Props

### The Whiteboard's Advantages

1. **Graphic capability**: Easy to draw diagrams on the spot to explain ideas
2. **Pacing control**: The pace of writing matches the audience's absorption speed (slides often move too fast)
3. **A place for your hands**: Gives hands something to do — avoids the awkwardness of pockets or hands behind the back
4. **Empathy mirroring**: The audience mentally simulates your writing motions, creating deeper engagement

### The Power of Props

Props create extremely strong visual memory anchors. The audience may forget the theory, but they will always remember the prop.

**Application**: When the presentation involves a physical product, bring it out to show. For example, when discussing Kitty Catchlight, actually demo it on your phone.

### The Seven Sins of Slides

| Sin | Why It's a Problem | Fix |
|-----|-------------------|-----|
| Reading the slides aloud | Audience reads faster than you speak — they'll be bored | Slides are prompts, not scripts |
| Standing too far from the screen | Audience neck swivels like watching tennis | Stand beside the screen |
| Cramming in text | Information overload; nothing sticks | Font ≥ 40pt, forces you to be concise |
| Using clip art / logos | Visual noise | Remove all decorative elements |
| Using a laser pointer | Turns your back on the audience, breaks eye contact | Draw arrows on the slide, or point with your hand |
| Complex background patterns | Reduces readability | Use a plain colour background |
| Too many bullet points | Each slide too dense | One core idea per slide |

### The One Exception: Hapax Legomenon

You are permitted **one** extremely complex slide per presentation. The goal is not to let the audience read it — it's to demonstrate the **complexity and scale** of the problem, thereby establishing authority.

---

## V. How to Inspire

### For Beginners / Students

Conveying the belief that "you can do this" is more important than teaching specific skills. Make them believe they're capable.

### For Experienced Practitioners

Show your **genuine passion** for the subject. If you find something genuinely exciting, let it show. Passion is the most contagious force.

### Teach People to Think, Not Just What to Know

Winston advocated teaching ways of thinking through **stories**. Provide:

- Stories (case studies)
- Key questions about those stories
- Analytical frameworks
- Synthesis methods
- Tools for evaluating reliability

---

## VI. How to Close

### What You Must Never Do

- ❌ End on a slide that says "Thank you", "Questions?", or "The End" — wasted screen real estate
- ❌ Say "Thank you for your time" — implies the audience listened out of politeness, placing yourself in a weak position

### What You Should Do

1. **Give a clear signal that you're wrapping up**: Let the audience know the end is coming
2. **Put "Contributions" on the final slide**: List your core achievements / key points. The Q&A may last 20 minutes — the audience will keep looking at your accomplishments
3. **Salute the audience (not thank them)**: Affirm the value of their being there
4. **A closing joke is fine**: This doesn't contradict "don't open with a joke". By now the audience has warmed up to you — a joke is a nice finishing touch

**Good closing examples**:

- "That's everything I have for you today. The fact that you're here, spending this time learning about AI coding, shows that you're the kind of people who genuinely want to make something. I look forward to seeing what you create."
- "I hope today's talk helps you avoid a few wrong turns. Hope to have another conversation soon."

---

## VII. Winston's Star: Making Your Work Memorable

If you want your project, product, or research to be remembered, five elements are needed:

| Element | Explanation | Huashu Example |
|---------|-------------|----------------|
| **Symbol** | A visual icon | The cat icon of Kitty Catchlight |
| **Slogan** | A catchy, memorable phrase | "Vibe Coding", "one-person company" |
| **Surprise** | A counterintuitive fact | "The development cost was just a few dollars in API fees" |
| **Salient Idea** | The most easily remembered concept | "Solo founder" |
| **Story** | How it happened | Kitty Catchlight: from personal use to #1 in the paid rankings |

---

## VIII. Meta-Techniques (Implicit Skills)

Techniques that Winston **demonstrated** through his own talk but never explicitly taught:

1. **Walk the talk**: He strictly followed every rule himself (no laser pointer, full lighting, used a blackboard, brought a prop)
2. **Leverage silence**: At key moments, deliberately pause — let the audience think on their own rather than filling every second
3. **Dry humour**: Naturally interspersed humour as a seasoning — consistent with "don't open with a joke"
4. **Move to control**: Don't stand still behind the lectern — move around the stage; use your position to direct attention
5. **Body language**: Gesture toward the board/screen; scan the room with your eyes; build connection with the audience

---

## How to Use This Skill

### Scenario 1: Review a Presentation / Training Outline

Give me your presentation outline and I'll review it across these dimensions:

- [ ] Is there an empowerment promise?
- [ ] Is the core idea cycled 3 times?
- [ ] Is a fence built around your idea?
- [ ] Is verbal punctuation sufficient?
- [ ] Are there interactive questions?
- [ ] Is the closing strong (not just "Thank you")?
- [ ] Are all 5 elements of Winston's Star present?

### Scenario 2: Optimise a Video Script

Give me your video script and I'll check:

- The hook in the first 10 seconds (empowerment promise)
- Whether there's a cycling callback every 3–5 minutes
- Whether verbal punctuation is dense enough
- Pacing variation (information-dense sections vs breathing sections)
- Whether the closing gives an action prompt

### Scenario 3: PPT / Keynote Review

Give me your slides and I'll check each one for the Seven Sins:

- Is the amount of text too much? (font ≥ 40pt?)
- Are there decorative elements? (logos / clip art)
- Are there complex backgrounds?
- Is the information hierarchy clear?
- Is there one "Hapax Legomenon" complex diagram?

### Scenario 4: Simulate Audience Feedback

I'll simulate a specific audience persona (e.g., "a product manager encountering AI coding for the first time") and listen to your presentation from their perspective, flagging:

- Where they'll mentally drift away
- Where they'll have questions
- Where they'll feel excited
- Where information overload will occur

---

## Review Scoring (out of 10)

When reviewing a presentation or script, I score across 5 dimensions:

| Dimension | Criteria |
|-----------|---------|
| **Opening power** | Attractiveness of the empowerment promise; ability to capture attention in the first 60 seconds |
| **Structural clarity** | Whether cycling, verbal punctuation, and fence-building are in place |
| **Interactivity** | Question design, pauses, and audience engagement |
| **Visual aids** | Whether slides/props follow the rules |
| **Closing power** | Whether it's strong, delivers contributions/action, and salutes rather than thanks |

Overall score + per-dimension recommendations + top 3 priority changes (minimum effort, maximum impact)

---

## Quick Reference Checklist

**Before the presentation**:

- [ ] Is the empowerment promise ready?
- [ ] Have you arrived early to check the room? Is the lighting bright enough?
- [ ] Is the room size appropriate?
- [ ] Have the slides passed the Seven Sins check?
- [ ] Have you practised at least once?

**During the presentation**:

- [ ] No joke in the opening — go straight to the promise
- [ ] Core idea cycled at least 3 times
- [ ] Verbal punctuation every 5–10 minutes
- [ ] Wait 7 seconds after asking a question
- [ ] Don't read the slides; don't use a laser pointer

**After the presentation**:

- [ ] Final slide shows contributions, not "Thank you"
- [ ] Salute the audience, don't thank them
- [ ] Closing includes an action prompt or a memorable line

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
) {
        " $cell "
      } else {
        " $cell "
      }
    }
    '|' + ($fixedCells -join '|') + '|'
  
| Best time | 11 am | Everyone's awake, not yet drowsy from lunch |
| Lighting | Fully on | Dim lighting = sleep signal. "Can't see the slides with their eyes closed" |
| Arrival | Arrive early to check the room | Familiarise yourself with equipment, light switches, microphone, seating layout |
| Room size | Choose a room that will be at least half full | Too few people → cold atmosphere; better to use a smaller room |

---

## IV. Tools and Props

### The Whiteboard's Advantages

1. **Graphic capability**: Easy to draw diagrams on the spot to explain ideas
2. **Pacing control**: The pace of writing matches the audience's absorption speed (slides often move too fast)
3. **A place for your hands**: Gives hands something to do — avoids the awkwardness of pockets or hands behind the back
4. **Empathy mirroring**: The audience mentally simulates your writing motions, creating deeper engagement

### The Power of Props

Props create extremely strong visual memory anchors. The audience may forget the theory, but they will always remember the prop.

**Application**: When the presentation involves a physical product, bring it out to show. For example, when discussing Kitty Catchlight, actually demo it on your phone.

### The Seven Sins of Slides

| Sin | Why It's a Problem | Fix |

    param($m)
    $inner = $m.Groups[1].Value
    # Split by | and fix each cell separator
    $cells = $inner -split '\|'
    $fixedCells = $cells | ForEach-Object {
      $cell = ---
name: huashu-speech-coach
description: |
  Presentation and speaking coach. Based on Patrick Winston's (MIT AI Professor) How to Speak methodology — helps prepare for offline training sessions, tech talks, Bilibili tutorial videos, and other speaking scenarios. Use when the user mentions "presentation", "talk", "training", "lecture", "PPT presentation", "opening", "closing", "how to speak", or "presentation structure".
---

# Presentation Coach

> Based on Professor Patrick Winston's (MIT) How to Speak methodology
> Original video: <https://youtu.be/Unzc731iCUY>
> Professor Winston passed away in 2019 — this lecture became his "final lecture", garnering 15 million+ views on YouTube
> Reference material: `references/patrick-winston-how-to-speak.md`

---

## Use Cases

| Scenario | How I Help |
|----------|-----------|
| Offline training / workshops | Review outline structure, optimise opening and closing, design interactive segments |
| Bilibili tutorial videos | Optimise script pacing, check cycling points, design hooks |
| Tech talks / meetups | Review presentation notes, check Winston rules, simulate audience perspective |
| PPT / Keynote review | Check slide "sins", optimise information density |

---

## Core Methodology

### Winston's Success Formula

```text
Presentation Quality = f(Knowledge, Practice, Talent)
```

Talent plays a very small role. What truly determines presentation quality is: how much **knowledge** (heuristic rules) you have about presenting, and how much you have **practised**.

---

## I. How to Open

### Don't Open with a Joke

The audience has just arrived and is still settling in — putting away phones, adjusting posture, getting used to your voice. Telling a joke at this point is very likely to fall flat, and a flat opening damages your confidence for the entire session.

### Open with an Empowerment Promise

Tell the audience: **what they will gain from listening**. Give them a reason to stay.

**Good promises**:

- "In the next 30 minutes, you'll learn 3 AI coding techniques you can put to use today"
- "After this, you'll know why 90% of people are using AI tools the wrong way"

**Poor promises**:

- "Today I'll be sharing some of my experiences with AI coding" (too vague, no sense of value)
- "Hello everyone, I'm Huashu, very happy to be here" (waste of an opening)

### Demand Full Attention

Humans have only one language processor. If the audience is on their phone, they **cannot take in** what you're saying. What's worse, someone on their phone distracts the people nearby — and distracts the presenter too.

**In offline training**: Directly ask them to close laptops and put phones away
**In video content**: The first 10 seconds must give a strong enough reason to keep watching

---

## II. Four Core Techniques During the Presentation

### 1. Cycling (Repetition)

At any given moment, approximately 20% of the audience has mentally drifted away. By repeating the core concept 3 times (in different ways), you ensure everyone receives the key message.

**Method**: "Tell them what you'll cover → Cover it → Tell them what you covered"

**For video content**: Refer back to the main theme every 3–5 minutes with a single sentence that pulls the audience back. "So returning to our core question — why did handmade economics suddenly take off?"

### 2. Building a Fence

Make the **distinction** between your idea and others' ideas clear — prevent the audience from getting confused.

**Method**: Be explicit about "what I AM talking about" and "what I am NOT talking about"

**Examples**:

- "When I say AI coding, I don't mean getting AI to write Hello World — I mean using AI to build a complete product from scratch"
- "This is different from regular Prompt Engineering — the difference is..."

### 3. Verbal Punctuation

Give mentally-wandering audience members a chance to "re-board". Use clear structural signals so those who've lost the thread know where you are.

**Method**:

- "Right, we've finished point one. Now moving on to point two..."
- "So far we've covered A and B. Coming up is the most critical part — C..."
- Use numbering: "First... Second... Third..."

### 4. Asking Questions

Asking a question instantly recaptures attention. The key is: after asking, **you must wait**.

**Wait time**: At least 7 seconds. Don't answer yourself just because the silence feels awkward.

**Question difficulty**:

- Too easy → audience feels insulted
- Too hard → no one dares to answer
- Just right → requires a moment of thought but can be answered

**For video content**: Although the audience can't actually respond, asking a question creates a pause for thinking — more effective than just stating the answer.

---

## III. Timing and Venue

| Rule | Requirement | Reason |
|------|-------------|--------|
| Best time | 11 am | Everyone's awake, not yet drowsy from lunch |
| Lighting | Fully on | Dim lighting = sleep signal. "Can't see the slides with their eyes closed" |
| Arrival | Arrive early to check the room | Familiarise yourself with equipment, light switches, microphone, seating layout |
| Room size | Choose a room that will be at least half full | Too few people → cold atmosphere; better to use a smaller room |

---

## IV. Tools and Props

### The Whiteboard's Advantages

1. **Graphic capability**: Easy to draw diagrams on the spot to explain ideas
2. **Pacing control**: The pace of writing matches the audience's absorption speed (slides often move too fast)
3. **A place for your hands**: Gives hands something to do — avoids the awkwardness of pockets or hands behind the back
4. **Empathy mirroring**: The audience mentally simulates your writing motions, creating deeper engagement

### The Power of Props

Props create extremely strong visual memory anchors. The audience may forget the theory, but they will always remember the prop.

**Application**: When the presentation involves a physical product, bring it out to show. For example, when discussing Kitty Catchlight, actually demo it on your phone.

### The Seven Sins of Slides

| Sin | Why It's a Problem | Fix |
|-----|-------------------|-----|
| Reading the slides aloud | Audience reads faster than you speak — they'll be bored | Slides are prompts, not scripts |
| Standing too far from the screen | Audience neck swivels like watching tennis | Stand beside the screen |
| Cramming in text | Information overload; nothing sticks | Font ≥ 40pt, forces you to be concise |
| Using clip art / logos | Visual noise | Remove all decorative elements |
| Using a laser pointer | Turns your back on the audience, breaks eye contact | Draw arrows on the slide, or point with your hand |
| Complex background patterns | Reduces readability | Use a plain colour background |
| Too many bullet points | Each slide too dense | One core idea per slide |

### The One Exception: Hapax Legomenon

You are permitted **one** extremely complex slide per presentation. The goal is not to let the audience read it — it's to demonstrate the **complexity and scale** of the problem, thereby establishing authority.

---

## V. How to Inspire

### For Beginners / Students

Conveying the belief that "you can do this" is more important than teaching specific skills. Make them believe they're capable.

### For Experienced Practitioners

Show your **genuine passion** for the subject. If you find something genuinely exciting, let it show. Passion is the most contagious force.

### Teach People to Think, Not Just What to Know

Winston advocated teaching ways of thinking through **stories**. Provide:

- Stories (case studies)
- Key questions about those stories
- Analytical frameworks
- Synthesis methods
- Tools for evaluating reliability

---

## VI. How to Close

### What You Must Never Do

- ❌ End on a slide that says "Thank you", "Questions?", or "The End" — wasted screen real estate
- ❌ Say "Thank you for your time" — implies the audience listened out of politeness, placing yourself in a weak position

### What You Should Do

1. **Give a clear signal that you're wrapping up**: Let the audience know the end is coming
2. **Put "Contributions" on the final slide**: List your core achievements / key points. The Q&A may last 20 minutes — the audience will keep looking at your accomplishments
3. **Salute the audience (not thank them)**: Affirm the value of their being there
4. **A closing joke is fine**: This doesn't contradict "don't open with a joke". By now the audience has warmed up to you — a joke is a nice finishing touch

**Good closing examples**:

- "That's everything I have for you today. The fact that you're here, spending this time learning about AI coding, shows that you're the kind of people who genuinely want to make something. I look forward to seeing what you create."
- "I hope today's talk helps you avoid a few wrong turns. Hope to have another conversation soon."

---

## VII. Winston's Star: Making Your Work Memorable

If you want your project, product, or research to be remembered, five elements are needed:

| Element | Explanation | Huashu Example |
|---------|-------------|----------------|
| **Symbol** | A visual icon | The cat icon of Kitty Catchlight |
| **Slogan** | A catchy, memorable phrase | "Vibe Coding", "one-person company" |
| **Surprise** | A counterintuitive fact | "The development cost was just a few dollars in API fees" |
| **Salient Idea** | The most easily remembered concept | "Solo founder" |
| **Story** | How it happened | Kitty Catchlight: from personal use to #1 in the paid rankings |

---

## VIII. Meta-Techniques (Implicit Skills)

Techniques that Winston **demonstrated** through his own talk but never explicitly taught:

1. **Walk the talk**: He strictly followed every rule himself (no laser pointer, full lighting, used a blackboard, brought a prop)
2. **Leverage silence**: At key moments, deliberately pause — let the audience think on their own rather than filling every second
3. **Dry humour**: Naturally interspersed humour as a seasoning — consistent with "don't open with a joke"
4. **Move to control**: Don't stand still behind the lectern — move around the stage; use your position to direct attention
5. **Body language**: Gesture toward the board/screen; scan the room with your eyes; build connection with the audience

---

## How to Use This Skill

### Scenario 1: Review a Presentation / Training Outline

Give me your presentation outline and I'll review it across these dimensions:

- [ ] Is there an empowerment promise?
- [ ] Is the core idea cycled 3 times?
- [ ] Is a fence built around your idea?
- [ ] Is verbal punctuation sufficient?
- [ ] Are there interactive questions?
- [ ] Is the closing strong (not just "Thank you")?
- [ ] Are all 5 elements of Winston's Star present?

### Scenario 2: Optimise a Video Script

Give me your video script and I'll check:

- The hook in the first 10 seconds (empowerment promise)
- Whether there's a cycling callback every 3–5 minutes
- Whether verbal punctuation is dense enough
- Pacing variation (information-dense sections vs breathing sections)
- Whether the closing gives an action prompt

### Scenario 3: PPT / Keynote Review

Give me your slides and I'll check each one for the Seven Sins:

- Is the amount of text too much? (font ≥ 40pt?)
- Are there decorative elements? (logos / clip art)
- Are there complex backgrounds?
- Is the information hierarchy clear?
- Is there one "Hapax Legomenon" complex diagram?

### Scenario 4: Simulate Audience Feedback

I'll simulate a specific audience persona (e.g., "a product manager encountering AI coding for the first time") and listen to your presentation from their perspective, flagging:

- Where they'll mentally drift away
- Where they'll have questions
- Where they'll feel excited
- Where information overload will occur

---

## Review Scoring (out of 10)

When reviewing a presentation or script, I score across 5 dimensions:

| Dimension | Criteria |
|-----------|---------|
| **Opening power** | Attractiveness of the empowerment promise; ability to capture attention in the first 60 seconds |
| **Structural clarity** | Whether cycling, verbal punctuation, and fence-building are in place |
| **Interactivity** | Question design, pauses, and audience engagement |
| **Visual aids** | Whether slides/props follow the rules |
| **Closing power** | Whether it's strong, delivers contributions/action, and salutes rather than thanks |

Overall score + per-dimension recommendations + top 3 priority changes (minimum effort, maximum impact)

---

## Quick Reference Checklist

**Before the presentation**:

- [ ] Is the empowerment promise ready?
- [ ] Have you arrived early to check the room? Is the lighting bright enough?
- [ ] Is the room size appropriate?
- [ ] Have the slides passed the Seven Sins check?
- [ ] Have you practised at least once?

**During the presentation**:

- [ ] No joke in the opening — go straight to the promise
- [ ] Core idea cycled at least 3 times
- [ ] Verbal punctuation every 5–10 minutes
- [ ] Wait 7 seconds after asking a question
- [ ] Don't read the slides; don't use a laser pointer

**After the presentation**:

- [ ] Final slide shows contributions, not "Thank you"
- [ ] Salute the audience, don't thank them
- [ ] Closing includes an action prompt or a memorable line

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
.Trim()
      if ($cell -match '^:?-+:?
| Reading the slides aloud | Audience reads faster than you speak — they'll be bored | Slides are prompts, not scripts |
| Standing too far from the screen | Audience neck swivels like watching tennis | Stand beside the screen |
| Cramming in text | Information overload; nothing sticks | Font ≥ 40pt, forces you to be concise |
| Using clip art / logos | Visual noise | Remove all decorative elements |
| Using a laser pointer | Turns your back on the audience, breaks eye contact | Draw arrows on the slide, or point with your hand |
| Complex background patterns | Reduces readability | Use a plain colour background |
| Too many bullet points | Each slide too dense | One core idea per slide |

### The One Exception: Hapax Legomenon

You are permitted **one** extremely complex slide per presentation. The goal is not to let the audience read it — it's to demonstrate the **complexity and scale** of the problem, thereby establishing authority.

---

## V. How to Inspire

### For Beginners / Students

Conveying the belief that "you can do this" is more important than teaching specific skills. Make them believe they're capable.

### For Experienced Practitioners

Show your **genuine passion** for the subject. If you find something genuinely exciting, let it show. Passion is the most contagious force.

### Teach People to Think, Not Just What to Know

Winston advocated teaching ways of thinking through **stories**. Provide:

- Stories (case studies)
- Key questions about those stories
- Analytical frameworks
- Synthesis methods
- Tools for evaluating reliability

---

## VI. How to Close

### What You Must Never Do

- ❌ End on a slide that says "Thank you", "Questions?", or "The End" — wasted screen real estate
- ❌ Say "Thank you for your time" — implies the audience listened out of politeness, placing yourself in a weak position

### What You Should Do

1. **Give a clear signal that you're wrapping up**: Let the audience know the end is coming
2. **Put "Contributions" on the final slide**: List your core achievements / key points. The Q&A may last 20 minutes — the audience will keep looking at your accomplishments
3. **Salute the audience (not thank them)**: Affirm the value of their being there
4. **A closing joke is fine**: This doesn't contradict "don't open with a joke". By now the audience has warmed up to you — a joke is a nice finishing touch

**Good closing examples**:

- "That's everything I have for you today. The fact that you're here, spending this time learning about AI coding, shows that you're the kind of people who genuinely want to make something. I look forward to seeing what you create."
- "I hope today's talk helps you avoid a few wrong turns. Hope to have another conversation soon."

---

## VII. Winston's Star: Making Your Work Memorable

If you want your project, product, or research to be remembered, five elements are needed:

| Element | Explanation | Huashu Example |
|---------|-------------|----------------|
| **Symbol** | A visual icon | The cat icon of Kitty Catchlight |
| **Slogan** | A catchy, memorable phrase | "Vibe Coding", "one-person company" |
| **Surprise** | A counterintuitive fact | "The development cost was just a few dollars in API fees" |
| **Salient Idea** | The most easily remembered concept | "Solo founder" |
| **Story** | How it happened | Kitty Catchlight: from personal use to #1 in the paid rankings |

---

## VIII. Meta-Techniques (Implicit Skills)

Techniques that Winston **demonstrated** through his own talk but never explicitly taught:

1. **Walk the talk**: He strictly followed every rule himself (no laser pointer, full lighting, used a blackboard, brought a prop)
2. **Leverage silence**: At key moments, deliberately pause — let the audience think on their own rather than filling every second
3. **Dry humour**: Naturally interspersed humour as a seasoning — consistent with "don't open with a joke"
4. **Move to control**: Don't stand still behind the lectern — move around the stage; use your position to direct attention
5. **Body language**: Gesture toward the board/screen; scan the room with your eyes; build connection with the audience

---

## How to Use This Skill

### Scenario 1: Review a Presentation / Training Outline

Give me your presentation outline and I'll review it across these dimensions:

- [ ] Is there an empowerment promise?
- [ ] Is the core idea cycled 3 times?
- [ ] Is a fence built around your idea?
- [ ] Is verbal punctuation sufficient?
- [ ] Are there interactive questions?
- [ ] Is the closing strong (not just "Thank you")?
- [ ] Are all 5 elements of Winston's Star present?

### Scenario 2: Optimise a Video Script

Give me your video script and I'll check:

- The hook in the first 10 seconds (empowerment promise)
- Whether there's a cycling callback every 3–5 minutes
- Whether verbal punctuation is dense enough
- Pacing variation (information-dense sections vs breathing sections)
- Whether the closing gives an action prompt

### Scenario 3: PPT / Keynote Review

Give me your slides and I'll check each one for the Seven Sins:

- Is the amount of text too much? (font ≥ 40pt?)
- Are there decorative elements? (logos / clip art)
- Are there complex backgrounds?
- Is the information hierarchy clear?
- Is there one "Hapax Legomenon" complex diagram?

### Scenario 4: Simulate Audience Feedback

I'll simulate a specific audience persona (e.g., "a product manager encountering AI coding for the first time") and listen to your presentation from their perspective, flagging:

- Where they'll mentally drift away
- Where they'll have questions
- Where they'll feel excited
- Where information overload will occur

---

## Review Scoring (out of 10)

When reviewing a presentation or script, I score across 5 dimensions:

| Dimension | Criteria |
|-----------|---------|
| **Opening power** | Attractiveness of the empowerment promise; ability to capture attention in the first 60 seconds |
| **Structural clarity** | Whether cycling, verbal punctuation, and fence-building are in place |
| **Interactivity** | Question design, pauses, and audience engagement |
| **Visual aids** | Whether slides/props follow the rules |
| **Closing power** | Whether it's strong, delivers contributions/action, and salutes rather than thanks |

Overall score + per-dimension recommendations + top 3 priority changes (minimum effort, maximum impact)

---

## Quick Reference Checklist

**Before the presentation**:

- [ ] Is the empowerment promise ready?
- [ ] Have you arrived early to check the room? Is the lighting bright enough?
- [ ] Is the room size appropriate?
- [ ] Have the slides passed the Seven Sins check?
- [ ] Have you practised at least once?

**During the presentation**:

- [ ] No joke in the opening — go straight to the promise
- [ ] Core idea cycled at least 3 times
- [ ] Verbal punctuation every 5–10 minutes
- [ ] Wait 7 seconds after asking a question
- [ ] Don't read the slides; don't use a laser pointer

**After the presentation**:

- [ ] Final slide shows contributions, not "Thank you"
- [ ] Salute the audience, don't thank them
- [ ] Closing includes an action prompt or a memorable line

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
) {
        " $cell "
      } else {
        " $cell "
      }
    }
    '|' + ($fixedCells -join '|') + '|'
  
| Reading the slides aloud | Audience reads faster than you speak — they'll be bored | Slides are prompts, not scripts |
| Standing too far from the screen | Audience neck swivels like watching tennis | Stand beside the screen |
| Cramming in text | Information overload; nothing sticks | Font ≥ 40pt, forces you to be concise |
| Using clip art / logos | Visual noise | Remove all decorative elements |
| Using a laser pointer | Turns your back on the audience, breaks eye contact | Draw arrows on the slide, or point with your hand |
| Complex background patterns | Reduces readability | Use a plain colour background |
| Too many bullet points | Each slide too dense | One core idea per slide |

### The One Exception: Hapax Legomenon

You are permitted **one** extremely complex slide per presentation. The goal is not to let the audience read it — it's to demonstrate the **complexity and scale** of the problem, thereby establishing authority.

---

## V. How to Inspire

### For Beginners / Students

Conveying the belief that "you can do this" is more important than teaching specific skills. Make them believe they're capable.

### For Experienced Practitioners

Show your **genuine passion** for the subject. If you find something genuinely exciting, let it show. Passion is the most contagious force.

### Teach People to Think, Not Just What to Know

Winston advocated teaching ways of thinking through **stories**. Provide:

- Stories (case studies)
- Key questions about those stories
- Analytical frameworks
- Synthesis methods
- Tools for evaluating reliability

---

## VI. How to Close

### What You Must Never Do

- ❌ End on a slide that says "Thank you", "Questions?", or "The End" — wasted screen real estate
- ❌ Say "Thank you for your time" — implies the audience listened out of politeness, placing yourself in a weak position

### What You Should Do

1. **Give a clear signal that you're wrapping up**: Let the audience know the end is coming
2. **Put "Contributions" on the final slide**: List your core achievements / key points. The Q&A may last 20 minutes — the audience will keep looking at your accomplishments
3. **Salute the audience (not thank them)**: Affirm the value of their being there
4. **A closing joke is fine**: This doesn't contradict "don't open with a joke". By now the audience has warmed up to you — a joke is a nice finishing touch

**Good closing examples**:

- "That's everything I have for you today. The fact that you're here, spending this time learning about AI coding, shows that you're the kind of people who genuinely want to make something. I look forward to seeing what you create."
- "I hope today's talk helps you avoid a few wrong turns. Hope to have another conversation soon."

---

## VII. Winston's Star: Making Your Work Memorable

If you want your project, product, or research to be remembered, five elements are needed:

| Element | Explanation | Huashu Example |

    param($m)
    $inner = $m.Groups[1].Value
    # Split by | and fix each cell separator
    $cells = $inner -split '\|'
    $fixedCells = $cells | ForEach-Object {
      $cell = ---
name: huashu-speech-coach
description: |
  Presentation and speaking coach. Based on Patrick Winston's (MIT AI Professor) How to Speak methodology — helps prepare for offline training sessions, tech talks, Bilibili tutorial videos, and other speaking scenarios. Use when the user mentions "presentation", "talk", "training", "lecture", "PPT presentation", "opening", "closing", "how to speak", or "presentation structure".
---

# Presentation Coach

> Based on Professor Patrick Winston's (MIT) How to Speak methodology
> Original video: <https://youtu.be/Unzc731iCUY>
> Professor Winston passed away in 2019 — this lecture became his "final lecture", garnering 15 million+ views on YouTube
> Reference material: `references/patrick-winston-how-to-speak.md`

---

## Use Cases

| Scenario | How I Help |
|----------|-----------|
| Offline training / workshops | Review outline structure, optimise opening and closing, design interactive segments |
| Bilibili tutorial videos | Optimise script pacing, check cycling points, design hooks |
| Tech talks / meetups | Review presentation notes, check Winston rules, simulate audience perspective |
| PPT / Keynote review | Check slide "sins", optimise information density |

---

## Core Methodology

### Winston's Success Formula

```text
Presentation Quality = f(Knowledge, Practice, Talent)
```

Talent plays a very small role. What truly determines presentation quality is: how much **knowledge** (heuristic rules) you have about presenting, and how much you have **practised**.

---

## I. How to Open

### Don't Open with a Joke

The audience has just arrived and is still settling in — putting away phones, adjusting posture, getting used to your voice. Telling a joke at this point is very likely to fall flat, and a flat opening damages your confidence for the entire session.

### Open with an Empowerment Promise

Tell the audience: **what they will gain from listening**. Give them a reason to stay.

**Good promises**:

- "In the next 30 minutes, you'll learn 3 AI coding techniques you can put to use today"
- "After this, you'll know why 90% of people are using AI tools the wrong way"

**Poor promises**:

- "Today I'll be sharing some of my experiences with AI coding" (too vague, no sense of value)
- "Hello everyone, I'm Huashu, very happy to be here" (waste of an opening)

### Demand Full Attention

Humans have only one language processor. If the audience is on their phone, they **cannot take in** what you're saying. What's worse, someone on their phone distracts the people nearby — and distracts the presenter too.

**In offline training**: Directly ask them to close laptops and put phones away
**In video content**: The first 10 seconds must give a strong enough reason to keep watching

---

## II. Four Core Techniques During the Presentation

### 1. Cycling (Repetition)

At any given moment, approximately 20% of the audience has mentally drifted away. By repeating the core concept 3 times (in different ways), you ensure everyone receives the key message.

**Method**: "Tell them what you'll cover → Cover it → Tell them what you covered"

**For video content**: Refer back to the main theme every 3–5 minutes with a single sentence that pulls the audience back. "So returning to our core question — why did handmade economics suddenly take off?"

### 2. Building a Fence

Make the **distinction** between your idea and others' ideas clear — prevent the audience from getting confused.

**Method**: Be explicit about "what I AM talking about" and "what I am NOT talking about"

**Examples**:

- "When I say AI coding, I don't mean getting AI to write Hello World — I mean using AI to build a complete product from scratch"
- "This is different from regular Prompt Engineering — the difference is..."

### 3. Verbal Punctuation

Give mentally-wandering audience members a chance to "re-board". Use clear structural signals so those who've lost the thread know where you are.

**Method**:

- "Right, we've finished point one. Now moving on to point two..."
- "So far we've covered A and B. Coming up is the most critical part — C..."
- Use numbering: "First... Second... Third..."

### 4. Asking Questions

Asking a question instantly recaptures attention. The key is: after asking, **you must wait**.

**Wait time**: At least 7 seconds. Don't answer yourself just because the silence feels awkward.

**Question difficulty**:

- Too easy → audience feels insulted
- Too hard → no one dares to answer
- Just right → requires a moment of thought but can be answered

**For video content**: Although the audience can't actually respond, asking a question creates a pause for thinking — more effective than just stating the answer.

---

## III. Timing and Venue

| Rule | Requirement | Reason |
|------|-------------|--------|
| Best time | 11 am | Everyone's awake, not yet drowsy from lunch |
| Lighting | Fully on | Dim lighting = sleep signal. "Can't see the slides with their eyes closed" |
| Arrival | Arrive early to check the room | Familiarise yourself with equipment, light switches, microphone, seating layout |
| Room size | Choose a room that will be at least half full | Too few people → cold atmosphere; better to use a smaller room |

---

## IV. Tools and Props

### The Whiteboard's Advantages

1. **Graphic capability**: Easy to draw diagrams on the spot to explain ideas
2. **Pacing control**: The pace of writing matches the audience's absorption speed (slides often move too fast)
3. **A place for your hands**: Gives hands something to do — avoids the awkwardness of pockets or hands behind the back
4. **Empathy mirroring**: The audience mentally simulates your writing motions, creating deeper engagement

### The Power of Props

Props create extremely strong visual memory anchors. The audience may forget the theory, but they will always remember the prop.

**Application**: When the presentation involves a physical product, bring it out to show. For example, when discussing Kitty Catchlight, actually demo it on your phone.

### The Seven Sins of Slides

| Sin | Why It's a Problem | Fix |
|-----|-------------------|-----|
| Reading the slides aloud | Audience reads faster than you speak — they'll be bored | Slides are prompts, not scripts |
| Standing too far from the screen | Audience neck swivels like watching tennis | Stand beside the screen |
| Cramming in text | Information overload; nothing sticks | Font ≥ 40pt, forces you to be concise |
| Using clip art / logos | Visual noise | Remove all decorative elements |
| Using a laser pointer | Turns your back on the audience, breaks eye contact | Draw arrows on the slide, or point with your hand |
| Complex background patterns | Reduces readability | Use a plain colour background |
| Too many bullet points | Each slide too dense | One core idea per slide |

### The One Exception: Hapax Legomenon

You are permitted **one** extremely complex slide per presentation. The goal is not to let the audience read it — it's to demonstrate the **complexity and scale** of the problem, thereby establishing authority.

---

## V. How to Inspire

### For Beginners / Students

Conveying the belief that "you can do this" is more important than teaching specific skills. Make them believe they're capable.

### For Experienced Practitioners

Show your **genuine passion** for the subject. If you find something genuinely exciting, let it show. Passion is the most contagious force.

### Teach People to Think, Not Just What to Know

Winston advocated teaching ways of thinking through **stories**. Provide:

- Stories (case studies)
- Key questions about those stories
- Analytical frameworks
- Synthesis methods
- Tools for evaluating reliability

---

## VI. How to Close

### What You Must Never Do

- ❌ End on a slide that says "Thank you", "Questions?", or "The End" — wasted screen real estate
- ❌ Say "Thank you for your time" — implies the audience listened out of politeness, placing yourself in a weak position

### What You Should Do

1. **Give a clear signal that you're wrapping up**: Let the audience know the end is coming
2. **Put "Contributions" on the final slide**: List your core achievements / key points. The Q&A may last 20 minutes — the audience will keep looking at your accomplishments
3. **Salute the audience (not thank them)**: Affirm the value of their being there
4. **A closing joke is fine**: This doesn't contradict "don't open with a joke". By now the audience has warmed up to you — a joke is a nice finishing touch

**Good closing examples**:

- "That's everything I have for you today. The fact that you're here, spending this time learning about AI coding, shows that you're the kind of people who genuinely want to make something. I look forward to seeing what you create."
- "I hope today's talk helps you avoid a few wrong turns. Hope to have another conversation soon."

---

## VII. Winston's Star: Making Your Work Memorable

If you want your project, product, or research to be remembered, five elements are needed:

| Element | Explanation | Huashu Example |
|---------|-------------|----------------|
| **Symbol** | A visual icon | The cat icon of Kitty Catchlight |
| **Slogan** | A catchy, memorable phrase | "Vibe Coding", "one-person company" |
| **Surprise** | A counterintuitive fact | "The development cost was just a few dollars in API fees" |
| **Salient Idea** | The most easily remembered concept | "Solo founder" |
| **Story** | How it happened | Kitty Catchlight: from personal use to #1 in the paid rankings |

---

## VIII. Meta-Techniques (Implicit Skills)

Techniques that Winston **demonstrated** through his own talk but never explicitly taught:

1. **Walk the talk**: He strictly followed every rule himself (no laser pointer, full lighting, used a blackboard, brought a prop)
2. **Leverage silence**: At key moments, deliberately pause — let the audience think on their own rather than filling every second
3. **Dry humour**: Naturally interspersed humour as a seasoning — consistent with "don't open with a joke"
4. **Move to control**: Don't stand still behind the lectern — move around the stage; use your position to direct attention
5. **Body language**: Gesture toward the board/screen; scan the room with your eyes; build connection with the audience

---

## How to Use This Skill

### Scenario 1: Review a Presentation / Training Outline

Give me your presentation outline and I'll review it across these dimensions:

- [ ] Is there an empowerment promise?
- [ ] Is the core idea cycled 3 times?
- [ ] Is a fence built around your idea?
- [ ] Is verbal punctuation sufficient?
- [ ] Are there interactive questions?
- [ ] Is the closing strong (not just "Thank you")?
- [ ] Are all 5 elements of Winston's Star present?

### Scenario 2: Optimise a Video Script

Give me your video script and I'll check:

- The hook in the first 10 seconds (empowerment promise)
- Whether there's a cycling callback every 3–5 minutes
- Whether verbal punctuation is dense enough
- Pacing variation (information-dense sections vs breathing sections)
- Whether the closing gives an action prompt

### Scenario 3: PPT / Keynote Review

Give me your slides and I'll check each one for the Seven Sins:

- Is the amount of text too much? (font ≥ 40pt?)
- Are there decorative elements? (logos / clip art)
- Are there complex backgrounds?
- Is the information hierarchy clear?
- Is there one "Hapax Legomenon" complex diagram?

### Scenario 4: Simulate Audience Feedback

I'll simulate a specific audience persona (e.g., "a product manager encountering AI coding for the first time") and listen to your presentation from their perspective, flagging:

- Where they'll mentally drift away
- Where they'll have questions
- Where they'll feel excited
- Where information overload will occur

---

## Review Scoring (out of 10)

When reviewing a presentation or script, I score across 5 dimensions:

| Dimension | Criteria |
|-----------|---------|
| **Opening power** | Attractiveness of the empowerment promise; ability to capture attention in the first 60 seconds |
| **Structural clarity** | Whether cycling, verbal punctuation, and fence-building are in place |
| **Interactivity** | Question design, pauses, and audience engagement |
| **Visual aids** | Whether slides/props follow the rules |
| **Closing power** | Whether it's strong, delivers contributions/action, and salutes rather than thanks |

Overall score + per-dimension recommendations + top 3 priority changes (minimum effort, maximum impact)

---

## Quick Reference Checklist

**Before the presentation**:

- [ ] Is the empowerment promise ready?
- [ ] Have you arrived early to check the room? Is the lighting bright enough?
- [ ] Is the room size appropriate?
- [ ] Have the slides passed the Seven Sins check?
- [ ] Have you practised at least once?

**During the presentation**:

- [ ] No joke in the opening — go straight to the promise
- [ ] Core idea cycled at least 3 times
- [ ] Verbal punctuation every 5–10 minutes
- [ ] Wait 7 seconds after asking a question
- [ ] Don't read the slides; don't use a laser pointer

**After the presentation**:

- [ ] Final slide shows contributions, not "Thank you"
- [ ] Salute the audience, don't thank them
- [ ] Closing includes an action prompt or a memorable line

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
.Trim()
      if ($cell -match '^:?-+:?
| **Symbol** | A visual icon | The cat icon of Kitty Catchlight |
| **Slogan** | A catchy, memorable phrase | "Vibe Coding", "one-person company" |
| **Surprise** | A counterintuitive fact | "The development cost was just a few dollars in API fees" |
| **Salient Idea** | The most easily remembered concept | "Solo founder" |
| **Story** | How it happened | Kitty Catchlight: from personal use to #1 in the paid rankings |

---

## VIII. Meta-Techniques (Implicit Skills)

Techniques that Winston **demonstrated** through his own talk but never explicitly taught:

1. **Walk the talk**: He strictly followed every rule himself (no laser pointer, full lighting, used a blackboard, brought a prop)
2. **Leverage silence**: At key moments, deliberately pause — let the audience think on their own rather than filling every second
3. **Dry humour**: Naturally interspersed humour as a seasoning — consistent with "don't open with a joke"
4. **Move to control**: Don't stand still behind the lectern — move around the stage; use your position to direct attention
5. **Body language**: Gesture toward the board/screen; scan the room with your eyes; build connection with the audience

---

## How to Use This Skill

### Scenario 1: Review a Presentation / Training Outline

Give me your presentation outline and I'll review it across these dimensions:

- [ ] Is there an empowerment promise?
- [ ] Is the core idea cycled 3 times?
- [ ] Is a fence built around your idea?
- [ ] Is verbal punctuation sufficient?
- [ ] Are there interactive questions?
- [ ] Is the closing strong (not just "Thank you")?
- [ ] Are all 5 elements of Winston's Star present?

### Scenario 2: Optimise a Video Script

Give me your video script and I'll check:

- The hook in the first 10 seconds (empowerment promise)
- Whether there's a cycling callback every 3–5 minutes
- Whether verbal punctuation is dense enough
- Pacing variation (information-dense sections vs breathing sections)
- Whether the closing gives an action prompt

### Scenario 3: PPT / Keynote Review

Give me your slides and I'll check each one for the Seven Sins:

- Is the amount of text too much? (font ≥ 40pt?)
- Are there decorative elements? (logos / clip art)
- Are there complex backgrounds?
- Is the information hierarchy clear?
- Is there one "Hapax Legomenon" complex diagram?

### Scenario 4: Simulate Audience Feedback

I'll simulate a specific audience persona (e.g., "a product manager encountering AI coding for the first time") and listen to your presentation from their perspective, flagging:

- Where they'll mentally drift away
- Where they'll have questions
- Where they'll feel excited
- Where information overload will occur

---

## Review Scoring (out of 10)

When reviewing a presentation or script, I score across 5 dimensions:

| Dimension | Criteria |
|-----------|---------|
| **Opening power** | Attractiveness of the empowerment promise; ability to capture attention in the first 60 seconds |
| **Structural clarity** | Whether cycling, verbal punctuation, and fence-building are in place |
| **Interactivity** | Question design, pauses, and audience engagement |
| **Visual aids** | Whether slides/props follow the rules |
| **Closing power** | Whether it's strong, delivers contributions/action, and salutes rather than thanks |

Overall score + per-dimension recommendations + top 3 priority changes (minimum effort, maximum impact)

---

## Quick Reference Checklist

**Before the presentation**:

- [ ] Is the empowerment promise ready?
- [ ] Have you arrived early to check the room? Is the lighting bright enough?
- [ ] Is the room size appropriate?
- [ ] Have the slides passed the Seven Sins check?
- [ ] Have you practised at least once?

**During the presentation**:

- [ ] No joke in the opening — go straight to the promise
- [ ] Core idea cycled at least 3 times
- [ ] Verbal punctuation every 5–10 minutes
- [ ] Wait 7 seconds after asking a question
- [ ] Don't read the slides; don't use a laser pointer

**After the presentation**:

- [ ] Final slide shows contributions, not "Thank you"
- [ ] Salute the audience, don't thank them
- [ ] Closing includes an action prompt or a memorable line

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
) {
        " $cell "
      } else {
        " $cell "
      }
    }
    '|' + ($fixedCells -join '|') + '|'
  
| **Symbol** | A visual icon | The cat icon of Kitty Catchlight |
| **Slogan** | A catchy, memorable phrase | "Vibe Coding", "one-person company" |
| **Surprise** | A counterintuitive fact | "The development cost was just a few dollars in API fees" |
| **Salient Idea** | The most easily remembered concept | "Solo founder" |
| **Story** | How it happened | Kitty Catchlight: from personal use to #1 in the paid rankings |

---

## VIII. Meta-Techniques (Implicit Skills)

Techniques that Winston **demonstrated** through his own talk but never explicitly taught:

1. **Walk the talk**: He strictly followed every rule himself (no laser pointer, full lighting, used a blackboard, brought a prop)
2. **Leverage silence**: At key moments, deliberately pause — let the audience think on their own rather than filling every second
3. **Dry humour**: Naturally interspersed humour as a seasoning — consistent with "don't open with a joke"
4. **Move to control**: Don't stand still behind the lectern — move around the stage; use your position to direct attention
5. **Body language**: Gesture toward the board/screen; scan the room with your eyes; build connection with the audience

---

## How to Use This Skill

### Scenario 1: Review a Presentation / Training Outline

Give me your presentation outline and I'll review it across these dimensions:

- [ ] Is there an empowerment promise?
- [ ] Is the core idea cycled 3 times?
- [ ] Is a fence built around your idea?
- [ ] Is verbal punctuation sufficient?
- [ ] Are there interactive questions?
- [ ] Is the closing strong (not just "Thank you")?
- [ ] Are all 5 elements of Winston's Star present?

### Scenario 2: Optimise a Video Script

Give me your video script and I'll check:

- The hook in the first 10 seconds (empowerment promise)
- Whether there's a cycling callback every 3–5 minutes
- Whether verbal punctuation is dense enough
- Pacing variation (information-dense sections vs breathing sections)
- Whether the closing gives an action prompt

### Scenario 3: PPT / Keynote Review

Give me your slides and I'll check each one for the Seven Sins:

- Is the amount of text too much? (font ≥ 40pt?)
- Are there decorative elements? (logos / clip art)
- Are there complex backgrounds?
- Is the information hierarchy clear?
- Is there one "Hapax Legomenon" complex diagram?

### Scenario 4: Simulate Audience Feedback

I'll simulate a specific audience persona (e.g., "a product manager encountering AI coding for the first time") and listen to your presentation from their perspective, flagging:

- Where they'll mentally drift away
- Where they'll have questions
- Where they'll feel excited
- Where information overload will occur

---

## Review Scoring (out of 10)

When reviewing a presentation or script, I score across 5 dimensions:

| Dimension | Criteria |

    param($m)
    $inner = $m.Groups[1].Value
    # Split by | and fix each cell separator
    $cells = $inner -split '\|'
    $fixedCells = $cells | ForEach-Object {
      $cell = ---
name: huashu-speech-coach
description: |
  Presentation and speaking coach. Based on Patrick Winston's (MIT AI Professor) How to Speak methodology — helps prepare for offline training sessions, tech talks, Bilibili tutorial videos, and other speaking scenarios. Use when the user mentions "presentation", "talk", "training", "lecture", "PPT presentation", "opening", "closing", "how to speak", or "presentation structure".
---

# Presentation Coach

> Based on Professor Patrick Winston's (MIT) How to Speak methodology
> Original video: <https://youtu.be/Unzc731iCUY>
> Professor Winston passed away in 2019 — this lecture became his "final lecture", garnering 15 million+ views on YouTube
> Reference material: `references/patrick-winston-how-to-speak.md`

---

## Use Cases

| Scenario | How I Help |
|----------|-----------|
| Offline training / workshops | Review outline structure, optimise opening and closing, design interactive segments |
| Bilibili tutorial videos | Optimise script pacing, check cycling points, design hooks |
| Tech talks / meetups | Review presentation notes, check Winston rules, simulate audience perspective |
| PPT / Keynote review | Check slide "sins", optimise information density |

---

## Core Methodology

### Winston's Success Formula

```text
Presentation Quality = f(Knowledge, Practice, Talent)
```

Talent plays a very small role. What truly determines presentation quality is: how much **knowledge** (heuristic rules) you have about presenting, and how much you have **practised**.

---

## I. How to Open

### Don't Open with a Joke

The audience has just arrived and is still settling in — putting away phones, adjusting posture, getting used to your voice. Telling a joke at this point is very likely to fall flat, and a flat opening damages your confidence for the entire session.

### Open with an Empowerment Promise

Tell the audience: **what they will gain from listening**. Give them a reason to stay.

**Good promises**:

- "In the next 30 minutes, you'll learn 3 AI coding techniques you can put to use today"
- "After this, you'll know why 90% of people are using AI tools the wrong way"

**Poor promises**:

- "Today I'll be sharing some of my experiences with AI coding" (too vague, no sense of value)
- "Hello everyone, I'm Huashu, very happy to be here" (waste of an opening)

### Demand Full Attention

Humans have only one language processor. If the audience is on their phone, they **cannot take in** what you're saying. What's worse, someone on their phone distracts the people nearby — and distracts the presenter too.

**In offline training**: Directly ask them to close laptops and put phones away
**In video content**: The first 10 seconds must give a strong enough reason to keep watching

---

## II. Four Core Techniques During the Presentation

### 1. Cycling (Repetition)

At any given moment, approximately 20% of the audience has mentally drifted away. By repeating the core concept 3 times (in different ways), you ensure everyone receives the key message.

**Method**: "Tell them what you'll cover → Cover it → Tell them what you covered"

**For video content**: Refer back to the main theme every 3–5 minutes with a single sentence that pulls the audience back. "So returning to our core question — why did handmade economics suddenly take off?"

### 2. Building a Fence

Make the **distinction** between your idea and others' ideas clear — prevent the audience from getting confused.

**Method**: Be explicit about "what I AM talking about" and "what I am NOT talking about"

**Examples**:

- "When I say AI coding, I don't mean getting AI to write Hello World — I mean using AI to build a complete product from scratch"
- "This is different from regular Prompt Engineering — the difference is..."

### 3. Verbal Punctuation

Give mentally-wandering audience members a chance to "re-board". Use clear structural signals so those who've lost the thread know where you are.

**Method**:

- "Right, we've finished point one. Now moving on to point two..."
- "So far we've covered A and B. Coming up is the most critical part — C..."
- Use numbering: "First... Second... Third..."

### 4. Asking Questions

Asking a question instantly recaptures attention. The key is: after asking, **you must wait**.

**Wait time**: At least 7 seconds. Don't answer yourself just because the silence feels awkward.

**Question difficulty**:

- Too easy → audience feels insulted
- Too hard → no one dares to answer
- Just right → requires a moment of thought but can be answered

**For video content**: Although the audience can't actually respond, asking a question creates a pause for thinking — more effective than just stating the answer.

---

## III. Timing and Venue

| Rule | Requirement | Reason |
|------|-------------|--------|
| Best time | 11 am | Everyone's awake, not yet drowsy from lunch |
| Lighting | Fully on | Dim lighting = sleep signal. "Can't see the slides with their eyes closed" |
| Arrival | Arrive early to check the room | Familiarise yourself with equipment, light switches, microphone, seating layout |
| Room size | Choose a room that will be at least half full | Too few people → cold atmosphere; better to use a smaller room |

---

## IV. Tools and Props

### The Whiteboard's Advantages

1. **Graphic capability**: Easy to draw diagrams on the spot to explain ideas
2. **Pacing control**: The pace of writing matches the audience's absorption speed (slides often move too fast)
3. **A place for your hands**: Gives hands something to do — avoids the awkwardness of pockets or hands behind the back
4. **Empathy mirroring**: The audience mentally simulates your writing motions, creating deeper engagement

### The Power of Props

Props create extremely strong visual memory anchors. The audience may forget the theory, but they will always remember the prop.

**Application**: When the presentation involves a physical product, bring it out to show. For example, when discussing Kitty Catchlight, actually demo it on your phone.

### The Seven Sins of Slides

| Sin | Why It's a Problem | Fix |
|-----|-------------------|-----|
| Reading the slides aloud | Audience reads faster than you speak — they'll be bored | Slides are prompts, not scripts |
| Standing too far from the screen | Audience neck swivels like watching tennis | Stand beside the screen |
| Cramming in text | Information overload; nothing sticks | Font ≥ 40pt, forces you to be concise |
| Using clip art / logos | Visual noise | Remove all decorative elements |
| Using a laser pointer | Turns your back on the audience, breaks eye contact | Draw arrows on the slide, or point with your hand |
| Complex background patterns | Reduces readability | Use a plain colour background |
| Too many bullet points | Each slide too dense | One core idea per slide |

### The One Exception: Hapax Legomenon

You are permitted **one** extremely complex slide per presentation. The goal is not to let the audience read it — it's to demonstrate the **complexity and scale** of the problem, thereby establishing authority.

---

## V. How to Inspire

### For Beginners / Students

Conveying the belief that "you can do this" is more important than teaching specific skills. Make them believe they're capable.

### For Experienced Practitioners

Show your **genuine passion** for the subject. If you find something genuinely exciting, let it show. Passion is the most contagious force.

### Teach People to Think, Not Just What to Know

Winston advocated teaching ways of thinking through **stories**. Provide:

- Stories (case studies)
- Key questions about those stories
- Analytical frameworks
- Synthesis methods
- Tools for evaluating reliability

---

## VI. How to Close

### What You Must Never Do

- ❌ End on a slide that says "Thank you", "Questions?", or "The End" — wasted screen real estate
- ❌ Say "Thank you for your time" — implies the audience listened out of politeness, placing yourself in a weak position

### What You Should Do

1. **Give a clear signal that you're wrapping up**: Let the audience know the end is coming
2. **Put "Contributions" on the final slide**: List your core achievements / key points. The Q&A may last 20 minutes — the audience will keep looking at your accomplishments
3. **Salute the audience (not thank them)**: Affirm the value of their being there
4. **A closing joke is fine**: This doesn't contradict "don't open with a joke". By now the audience has warmed up to you — a joke is a nice finishing touch

**Good closing examples**:

- "That's everything I have for you today. The fact that you're here, spending this time learning about AI coding, shows that you're the kind of people who genuinely want to make something. I look forward to seeing what you create."
- "I hope today's talk helps you avoid a few wrong turns. Hope to have another conversation soon."

---

## VII. Winston's Star: Making Your Work Memorable

If you want your project, product, or research to be remembered, five elements are needed:

| Element | Explanation | Huashu Example |
|---------|-------------|----------------|
| **Symbol** | A visual icon | The cat icon of Kitty Catchlight |
| **Slogan** | A catchy, memorable phrase | "Vibe Coding", "one-person company" |
| **Surprise** | A counterintuitive fact | "The development cost was just a few dollars in API fees" |
| **Salient Idea** | The most easily remembered concept | "Solo founder" |
| **Story** | How it happened | Kitty Catchlight: from personal use to #1 in the paid rankings |

---

## VIII. Meta-Techniques (Implicit Skills)

Techniques that Winston **demonstrated** through his own talk but never explicitly taught:

1. **Walk the talk**: He strictly followed every rule himself (no laser pointer, full lighting, used a blackboard, brought a prop)
2. **Leverage silence**: At key moments, deliberately pause — let the audience think on their own rather than filling every second
3. **Dry humour**: Naturally interspersed humour as a seasoning — consistent with "don't open with a joke"
4. **Move to control**: Don't stand still behind the lectern — move around the stage; use your position to direct attention
5. **Body language**: Gesture toward the board/screen; scan the room with your eyes; build connection with the audience

---

## How to Use This Skill

### Scenario 1: Review a Presentation / Training Outline

Give me your presentation outline and I'll review it across these dimensions:

- [ ] Is there an empowerment promise?
- [ ] Is the core idea cycled 3 times?
- [ ] Is a fence built around your idea?
- [ ] Is verbal punctuation sufficient?
- [ ] Are there interactive questions?
- [ ] Is the closing strong (not just "Thank you")?
- [ ] Are all 5 elements of Winston's Star present?

### Scenario 2: Optimise a Video Script

Give me your video script and I'll check:

- The hook in the first 10 seconds (empowerment promise)
- Whether there's a cycling callback every 3–5 minutes
- Whether verbal punctuation is dense enough
- Pacing variation (information-dense sections vs breathing sections)
- Whether the closing gives an action prompt

### Scenario 3: PPT / Keynote Review

Give me your slides and I'll check each one for the Seven Sins:

- Is the amount of text too much? (font ≥ 40pt?)
- Are there decorative elements? (logos / clip art)
- Are there complex backgrounds?
- Is the information hierarchy clear?
- Is there one "Hapax Legomenon" complex diagram?

### Scenario 4: Simulate Audience Feedback

I'll simulate a specific audience persona (e.g., "a product manager encountering AI coding for the first time") and listen to your presentation from their perspective, flagging:

- Where they'll mentally drift away
- Where they'll have questions
- Where they'll feel excited
- Where information overload will occur

---

## Review Scoring (out of 10)

When reviewing a presentation or script, I score across 5 dimensions:

| Dimension | Criteria |
|-----------|---------|
| **Opening power** | Attractiveness of the empowerment promise; ability to capture attention in the first 60 seconds |
| **Structural clarity** | Whether cycling, verbal punctuation, and fence-building are in place |
| **Interactivity** | Question design, pauses, and audience engagement |
| **Visual aids** | Whether slides/props follow the rules |
| **Closing power** | Whether it's strong, delivers contributions/action, and salutes rather than thanks |

Overall score + per-dimension recommendations + top 3 priority changes (minimum effort, maximum impact)

---

## Quick Reference Checklist

**Before the presentation**:

- [ ] Is the empowerment promise ready?
- [ ] Have you arrived early to check the room? Is the lighting bright enough?
- [ ] Is the room size appropriate?
- [ ] Have the slides passed the Seven Sins check?
- [ ] Have you practised at least once?

**During the presentation**:

- [ ] No joke in the opening — go straight to the promise
- [ ] Core idea cycled at least 3 times
- [ ] Verbal punctuation every 5–10 minutes
- [ ] Wait 7 seconds after asking a question
- [ ] Don't read the slides; don't use a laser pointer

**After the presentation**:

- [ ] Final slide shows contributions, not "Thank you"
- [ ] Salute the audience, don't thank them
- [ ] Closing includes an action prompt or a memorable line

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
.Trim()
      if ($cell -match '^:?-+:?
| **Opening power** | Attractiveness of the empowerment promise; ability to capture attention in the first 60 seconds |
| **Structural clarity** | Whether cycling, verbal punctuation, and fence-building are in place |
| **Interactivity** | Question design, pauses, and audience engagement |
| **Visual aids** | Whether slides/props follow the rules |
| **Closing power** | Whether it's strong, delivers contributions/action, and salutes rather than thanks |

Overall score + per-dimension recommendations + top 3 priority changes (minimum effort, maximum impact)

---

## Quick Reference Checklist

**Before the presentation**:

- [ ] Is the empowerment promise ready?
- [ ] Have you arrived early to check the room? Is the lighting bright enough?
- [ ] Is the room size appropriate?
- [ ] Have the slides passed the Seven Sins check?
- [ ] Have you practised at least once?

**During the presentation**:

- [ ] No joke in the opening — go straight to the promise
- [ ] Core idea cycled at least 3 times
- [ ] Verbal punctuation every 5–10 minutes
- [ ] Wait 7 seconds after asking a question
- [ ] Don't read the slides; don't use a laser pointer

**After the presentation**:

- [ ] Final slide shows contributions, not "Thank you"
- [ ] Salute the audience, don't thank them
- [ ] Closing includes an action prompt or a memorable line

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
) {
        " $cell "
      } else {
        " $cell "
      }
    }
    '|' + ($fixedCells -join '|') + '|'
  
| **Opening power** | Attractiveness of the empowerment promise; ability to capture attention in the first 60 seconds |
| **Structural clarity** | Whether cycling, verbal punctuation, and fence-building are in place |
| **Interactivity** | Question design, pauses, and audience engagement |
| **Visual aids** | Whether slides/props follow the rules |
| **Closing power** | Whether it's strong, delivers contributions/action, and salutes rather than thanks |

Overall score + per-dimension recommendations + top 3 priority changes (minimum effort, maximum impact)

---

## Quick Reference Checklist

**Before the presentation**:

- [ ] Is the empowerment promise ready?
- [ ] Have you arrived early to check the room? Is the lighting bright enough?
- [ ] Is the room size appropriate?
- [ ] Have the slides passed the Seven Sins check?
- [ ] Have you practised at least once?

**During the presentation**:

- [ ] No joke in the opening — go straight to the promise
- [ ] Core idea cycled at least 3 times
- [ ] Verbal punctuation every 5–10 minutes
- [ ] Wait 7 seconds after asking a question
- [ ] Don't read the slides; don't use a laser pointer

**After the presentation**:

- [ ] Final slide shows contributions, not "Thank you"
- [ ] Salute the audience, don't thank them
- [ ] Closing includes an action prompt or a memorable line

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
