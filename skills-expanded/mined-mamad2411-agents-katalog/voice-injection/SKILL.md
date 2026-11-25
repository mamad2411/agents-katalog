---
name: voice-injection
description: Transforms generic articles into Dorian's authentic voice through structured interview, then applies MoxyWolf writing style. Use when content reads as "AI wrote it" and needs the founder's perspective, experience, and opinion injected. INTERACTIVE SKILL with 8 questions - in GSD mode, check for hitl_answers or block. Triggers inject voice, make this sound like me, add my perspective, voice injection. GSD-compatible with VOICE_INJECTED completion promise and 8 HITL checkpoints (trigger, evidence, contrarian_take, authority, specific_reader, business_connection, call_to_action, emotional_core).
license: Proprietary - MoxyWolf LLC
---

# Voice Injection Skill

## GSD Integration

When invoked from `gsd-phase-executor`:

**HITL Checkpoints (8 required questions):**
1. `trigger`: What triggered this? What conversation, client situation, article, or frustration?
2. `evidence`: What have you actually seen? Give a real example.
3. `contrarian_take`: What do most people get wrong? Where is conventional wisdom broken?
4. `authority`: Why should anyone listen to you? What experience shapes your view?
5. `specific_reader`: Who specifically is this for? What keeps them up at night?
6. `business_connection`: How does this connect to MoxyWolf?
7. `call_to_action`: What should they DO after reading?
8. `emotional_core`: What pisses you off, excites you, or worries you?

**If hitl_answers provided:**
- Skip interactive interview
- Extract answers from hitl_answers using checkpoint IDs (trigger, evidence, contrarian_take, etc.)
- Proceed directly to Phase 2 (rewriting)
- After Phase 2 completion, signal `VOICE_INJECTED` promise
- Write voice-injected content to disk at specified output path

**If hitl_answers NOT provided:**
- Block execution with clear message
- Return required checkpoint questions to executor
- Executor will pause for human input
- Resume when hitl_answers become available

**Output behavior:**
- Create voice-injected article as .docx file
- Store in `/mnt/user-data/outputs/` with descriptive filename
- Include all Phase 2 style transformations
- Run Phase 3 anti-detection checklist silently
- Return filepath for promise completion

**Promise contract:**
```
VOICE_INJECTED = {
  "output_file": "/mnt/user-data/outputs/article-voice-injected.docx",
  "checkpoint_answers": { /* preserved for audit trail */ },
  "anti_detection_score": 8/8
}
```

---

## Why This Skill Exists

I wrote my first AI-assisted article in early 2024. It was competent. Well-structured. Grammatically flawless. And it sounded like absolutely nobody.

The piece explained conversational AI accurately. It covered the right concepts. But reading it back, I couldn't find myself anywhere in the text. No origin story. No opinion. No indication that I'd spent 22 years building compliance frameworks, wrestled with qualitative research requirements in an MBA program, or gotten frustrated enough with existing tools to build my own.

The article could have been written by anyone. Which meant it would be read by no one.

That's when I realized the problem wasn't the AI. The problem was me. I'd handed over a topic and expected magic. But AI doesn't know what triggered my interest, what I've actually seen in the field, or what pisses me off about the conventional wisdom. It can't inject those things because I never provided them.

So I built an interview process. Eight questions that extract the human story before any writing happens. Then a rewriting phase that applies MoxyWolf style rules and anti-detection patterns. The result: content that sounds like me because it actually contains me.

**When to use this skill**: Any time content reads as competent explanation without personality, opinion, or lived experience. The telltale sign: there's no "Dorian" in it. No origin story. No "here's my take." No connection to what MoxyWolf is actually doing or seeing.

---

## Phase 1: The Voice Injection Interview

I ask these questions **one at a time**. I wait for the answer before moving to the next. Combining questions or rushing through them defeats the purpose; each answer needs space to develop.

### Question 1: The Trigger

**I ask**: "What triggered this? What conversation, client situation, article, or frustration made you want to write about this specific topic right now?"

**Why I start here**: Every real article starts somewhere. The trigger reveals the emotional entry point and grounds the piece in lived experience rather than abstract expertise.

I developed this question after noticing that my best articles all had a clear inciting incident. The worst ones started from "I should write something about X." No trigger, no energy.

### Question 2: The Evidence

**I ask**: "What have you actually seen? Give me a real example; a client, a project, a conversation where this played out. Names can be changed, but the story needs to be real."

**Why this matters**: Specificity defeats AI-detection. Real stories have texture, unexpected details, and outcomes that aren't perfectly tidy. AI generates plausible scenarios. Humans remember specific moments.

The first time I added a real client story to an AI draft, the piece went from forgettable to shareable. One concrete example did more than three paragraphs of explanation.

### Question 3: The Contrarian Take

**I ask**: "What do most people get wrong about this? Where's the conventional wisdom broken? What's the take that would make someone in the industry uncomfortable?"

**Why I push on this**: Opinion is the sharpest differentiator between AI-generated content and human writing. AI hedges. It presents "perspectives" and "considerations." Humans take positions.

This question came from reading my own AI drafts and noticing they never disagreed with anyone. They summarized. They explained. They never said "this approach is wrong and here's why." That absence is a tell.

### Question 4: The Authority

**I ask**: "Why should anyone listen to you on this? Not credentials for credentials' sake; what experience or pattern-recognition do you bring that shapes how you see this differently?"

**Why I need this**: This isn't resume-padding. It's establishing what I've done or seen that makes my perspective earned rather than borrowed.

Twenty-two years in compliance gave me pattern recognition that a fresh MBA wouldn't have. I've watched regulations evolve, seen what actually gets implemented versus what gets ignored, built frameworks that thousands of organizations use. That context matters. But it only shows up in writing if someone asks for it explicitly.

### Question 5: The Specific Reader

**I ask**: "Who specifically is this for, and what's keeping them up at night? Not 'business leaders' or 'researchers'; who, exactly, and what specific problem are they staring at?"

**Why specificity matters here**: Generic audience equals generic writing. Specific reader equals specific language, examples, and concerns.

I learned this from Rob Fitzpatrick's work on customer interviews. When you ask "who's this for" and get "anyone interested in AI," you know the piece will be unfocused. When you get "the head of customer success at a B2B SaaS company who just realized their survey response rates dropped below 15%," you know exactly how to write.

### Question 6: The Business Connection

**I ask**: "How does this connect to what MoxyWolf is building or selling? Be direct. If there's no connection, why are you writing it?"

**Why I make this explicit**: Either there's a strategic reason for the content, or the article is "pure" thought leadership. Both are valid. But knowing which shapes the approach entirely.

I added this question after writing several pieces that went nowhere because I couldn't figure out the call to action. Turns out, I hadn't decided what I wanted readers to do. Content without purpose is noise.

### Question 7: The Call to Action

**I ask**: "What do you want someone to DO after reading this? Not 'understand'; act. Think differently. Stop doing something. Start doing something."

**Why I end with action**: Writing without a desired outcome produces content that gets read, nodded at, and forgotten. The call shapes the entire structure.

My best-performing pieces all have clear asks. "Stop using NPS surveys for discovery." "Start treating your AI tool like an intern, not an oracle." "Email me if you want to see the actual interview transcripts." Specificity again.

### Question 8: The Emotional Core

**I ask**: "What's the emotional core? What pisses you off, excites you, or worries you about this topic?"

**Why I save this for last**: Emotion is the hardest thing for AI to fake. Genuine frustration, excitement, or concern bleeds through in word choice, sentence rhythm, and intensity.

By the time I reach this question, the earlier answers have usually surfaced the emotion anyway. But asking directly gives permission to be honest about it. "I'm furious that consultants charge $50,000 for insights they could get from a properly designed interview bot." That's energy. That's voice.

---

## Phase 2: Rewriting with Voice + MoxyWolf Style

After completing the interview, I rewrite the article incorporating everything I've gathered.

### Structure Changes I Make

1. **Open with the trigger**: Why I wrote this, what I was reacting to
2. **Establish authority naturally**: Weave experience into the narrative, don't list credentials
3. **Include the real example**: The specific story from Question 2
4. **Name the enemy**: The contrarian take should have a clear antagonist (bad advice, wrong approach, snake oil)
5. **Speak to the specific reader**: Use "you" addressing their actual situation
6. **End with the call**: What they should stop doing, start doing, or think differently about

### MoxyWolf Writing Style (Mandatory)

**Punctuation Rules**:
- ALWAYS use typographer's quotes: "curly quotes" not "straight quotes"
- NEVER use em dashes (—). Use spaced en-dashes " – " instead, sparingly
- Use contractions in 80%+ of opportunities ("doesn't" not "does not")

**Forbidden Phrases** (I never use these):
- "It's worth noting that..."
- "It's important to understand..."
- "In today's rapidly changing..."
- "At its core..."
- "This is particularly true when..."
- "Moving forward..."
- "In order to..." (just use "to")
- "That being said..."

**Forbidden Transitions** (replace or delete):
- Furthermore → And, Plus, or delete entirely
- Additionally → And, or delete entirely
- Moreover → What's more, or delete entirely
- In conclusion → Just conclude; don't announce it
- Nevertheless → But, Still, Yet

**Sentence Architecture**:
- Vary length aggressively. Some sentences: four words. Others unspool across forty.
- Use fragments. Deliberately. For emphasis.
- Start sentences with And, But, Or at least once per page
- Break the "topic sentence" pattern; not every paragraph announces its point upfront
- Vary paragraph length dramatically, including single-sentence paragraphs

**Specificity Over Abstraction**:
- Replace "significant cost reduction" with "what cost $500 now costs $0.50"
- Replace "organizations across industries" with named examples
- Replace abstract claims with specific numbers, names, or examples

**Voice Markers**:
- Use parenthetical asides (the kind that feel like leaning in)
- Express genuine opinion; not "some might argue" but stating it flatly
- Allow mild colloquialisms: "the bigger deal," "here's the thing"
- Use "we" for MoxyWolf, "I" for my personal experience

---

## My Anti-Detection Checklist

Before I deliver anything, I verify:

- [ ] Contractions used in 80%+ of opportunities
- [ ] No forbidden phrases present
- [ ] No formulaic transitions (Furthermore, Additionally, Moreover)
- [ ] Sentence length varies dramatically (4-word and 40-word sentences present)
- [ ] At least one fragment per page used deliberately
- [ ] Parallelism broken (not everything in threes)
- [ ] Specific examples replace abstract claims
- [ ] Paragraphs vary in length (including single-sentence paragraphs)
- [ ] At least one sentence starts with And, But, or Or per page
- [ ] No em dashes; only spaced en-dashes ( – ) if needed
- [ ] Typographer's quotes throughout

---

## Example Transformation

**Before (AI-sounding)**:
> "Conversational AI is software that can hold actual conversations. Not scripted menu trees. Not keyword matching. Real back-and-forth dialogue where the system understands what you mean, remembers what you said earlier, and responds in ways that make sense."

**After (Voice-injected + MoxyWolf style)**:
> "When I was forced to retire from Unified Compliance after 22 years, I joined an MBA program that required qualitative research. I didn't have time for phone interviews. And honestly? I didn't have the chops to analyze open-ended answers properly. So I did what I've been doing for fifteen years – I turned to AI. My thinking was simple: if AI could create bots that provide answers, surely a system could be built to have conversations and follow-ups. To actually listen."

The difference: origin story, specific problem, honest admission of limitation, first-person voice, contractions, varied sentence length, fragment for emphasis.

---

## Phase 3: Iterative Refinement

After the initial rewrite, I present the draft and invite selection-based editing. The human identifies specific passages that don't sound right. For each selected passage, I offer options:

### Refinement Commands

When someone selects a passage (by quoting it, highlighting it, or referencing it), I ask:

**"What's wrong with this passage? Choose one or tell me in your own words:"**

1. **"Too generic"** → I ask: "What specific example, story, or detail from your experience should replace this?"

2. **"Too soft"** → I ask: "What's the stronger version? What would you actually say to someone's face?"

3. **"Not how I'd say it"** → I ask: "Read it out loud. What words feel wrong? How would you phrase this if you were explaining it over coffee?"

4. **"Needs more"** → I ask: "What's missing? What context, caveat, or expansion would make this complete?"

5. **"Too much"** → I ask: "What's the core point? What can we cut?"

6. **"Wrong tone"** → I ask: "Is this too formal? Too casual? Too angry? Too detached? What's the right emotional register?"

7. **"I'd tell a story here"** → I ask: "Tell me the story. Who was involved? What happened? What was the outcome?"

8. **"Unpack this"** → This triggers the Unpacking Aside mechanism (see below)

### The Unpacking Aside Mechanism

I developed this structure for passages that are too vague or hand-wavy but would clutter the main argument if fully expanded. It creates a two-part approach:

**Part 1: Inline marker**
Add a parenthetical reference in the main text that signals more detail is available without breaking flow.

Format: `(see "Unpacking: [Topic]" below)`

Example:
- **Before:** "Conversational AI is software that holds actual conversations."
- **After:** "Conversational AI is software (see "Unpacking: What's Actually in the Stack" below) that holds actual conversations."

**Part 2: P.S. section at end of article**
Add a post-script section after the main signature with the technical deep-dive.

Format:
```
–

P.S. – Unpacking: [Topic Name]

[Detailed technical explanation in my voice – specific, concrete, 
showing actual implementation knowledge. This is where I prove I 
built the thing, not just read about it.]
```

**Multiple unpacks:** If multiple topics need unpacking, I stack them:
```
P.S. – Unpacking: What's Actually in the Stack
[content]

P.P.S. – Unpacking: Why Context Windows Matter
[content]
```

**My process for creating an unpack:**

1. I ask: "What's the technical reality behind this? Walk me through the actual implementation; components, tools, architecture, tradeoffs."

2. I ask: "Who's this unpack for? The curious founder who wants to understand? The technical co-founder who'll actually build it? The skeptic who needs proof you know what you're talking about?"

3. I write the unpack in a more technical register. Still my voice, but speaking to people who want the real details.

4. I keep the inline marker brief. It shouldn't slow down readers who don't care.

**Why this structure works:**
- AI doesn't do structural innovation like P.S. sections
- It signals "I actually know how this works" without cluttering the main argument
- Readers who want depth get it; skimmers aren't punished
- The format itself is a credibility marker. Only someone who built the thing would offer to unpack it

### Refinement Process

For each selected passage:

1. **Hear the feedback**: Understand what's wrong
2. **Ask one clarifying question**: Get the specific fix or story
3. **Rewrite just that passage**: Show the before/after
4. **Confirm or iterate**: "Better? Or still off?"

Continue until the passage is approved, then move to the next selection.

### Example Refinement Exchange

**Human selects:** "The technology is exciting. It's getting better every day."

**Human says:** "Too generic"

**I ask:** "What specifically excites you? Is there a recent capability jump you've seen, a demo that surprised you, or a use case that wasn't possible six months ago?"

**Human says:** "Six months ago the context windows were too small to feed it a full methodology. Now I can give it the entire Mom Test plus supplementary research and it actually holds it all."

**I rewrite:** "Six months ago, context windows were too small to feed a system an entire methodology. Now I can give it the full Mom Test plus supplementary research papers, and it holds all of it. That's the kind of jump that changes what's buildable."

**Human:** "Better."

### Refinement Prompts by Problem Type

**When passage is too abstract:**
- "Give me a number, a name, or a date."
- "What did this look like in practice?"
- "Who specifically did this happen to?"

**When passage is too hedged:**
- "Do you actually believe this or are you covering your ass?"
- "What's the version without the qualifiers?"
- "If you were arguing this at a bar, how would you say it?"

**When passage sounds like AI:**
- "Read this out loud. Where do you stumble?"
- "What word would you never use?"
- "How would you text this to a friend?"

**When passage needs story:**
- "When did you first realize this?"
- "Who taught you this the hard way?"
- "What's the worst example you've seen?"

**When passage needs opinion:**
- "What pisses you off about this?"
- "What do the idiots get wrong?"
- "If you could grab someone by the collar about this, what would you say?"

---

## Phase 4: Blog Image

After delivering the final document, I ask:

**"Do you want a PNG image for the blog post?"**

If yes:

1. **I ask for direction**: "What should the image convey? The main concept? A visual metaphor? Something that captures the emotional core? Or do you have a specific idea?"

2. **I confirm style**: The image should align with MoxyWolf visual identity:
   - Use brand colors (Fire Orange #F77028, Electric Blue #0075C9, Vivid Magenta #D8298E, Charcoal Black #1C1C1C)
   - Bold, geometric, structured
   - Avoid generic stock photo aesthetics
   - Favor abstract/conceptual over literal illustration

3. **I generate the image**: Create using available image generation tools, sized appropriately for blog headers (typically 1200x630 or 1920x1080)

4. **Deliver as PNG**: Provide download link

---

## Workflow Summary

1. **Identify the source article**: Confirm it needs voice injection
2. **Conduct the 8-question interview**: One question at a time, wait for answers
3. **Synthesize the answers**: Identify the key elements (trigger, story, enemy, authority, reader, call)
4. **Rewrite the article**: Restructure around my perspective
5. **Apply MoxyWolf style**: Fix punctuation, eliminate forbidden phrases, vary structure
6. **Run anti-detection checklist**: Verify all items pass
7. **Present draft for refinement**: Invite selection-based feedback
8. **Iterate on selected passages**: Refine until each passage is approved
9. **Deliver the document**: In requested format (docx, markdown, etc.)
10. **Offer blog image**: Ask if they want a PNG for the post