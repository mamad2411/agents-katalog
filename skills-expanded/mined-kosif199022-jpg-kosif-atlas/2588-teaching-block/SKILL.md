---
name: teaching-block
description: >
  Converts the current conversation into a long-form show-and-tell article that documents a
  process walkthrough — educational, informative, and reflective. Use this skill whenever the
  user types /teaching-block, or says they want to turn a conversation into an article, share their
  discovery process with an audience, capture lessons learned, write a walkthrough of what just
  happened, or create teaching content from a session. Also use when the user says things like
  "let's turn this into a post", "I want to share this with my community", "capture this for AIMM",
  "write up what we just did", or "make a screencast summary." Invoke proactively if the conversation
  has reached a clear conclusion and the user seems to be wrapping up — offer to produce a
  teaching block even if not explicitly asked.
---

# Teaching Block

You are producing a **teaching block**: a detailed process walkthrough article that shows *exactly*
what happened in a conversation — the actual inputs, outputs, decisions, and reasoning — so a reader
can understand it well enough to do it themselves.

The target feeling in the reader: *"Wow, huh — that's cool. I'd like to do that myself.
Let me follow this process."*

This is **not** a literary piece or a narrative essay. It is closer to a **reflective process
journal** combined with **show-and-tell** — educational and informative above everything else.
The craft is in the clarity of explanation, not in the elegance of the prose.

Target audience: AIMM members — practitioners who want to understand and replicate the process,
not just appreciate the outcome.

Read `references/writing-style.md` before writing. Apply the **Professional Storyteller** voice —
experienced, observational, peer-to-peer — but in service of *explanation*, not storytelling.

---

## Before you write

Read the full conversation. Map out:

- **What problem was being solved** and why it mattered
- **The sequence of steps** taken — including what was tried first, what didn't work, and what changed
- **The actual artifacts** produced along the way: prompts used, outputs received, code written,
  decisions made, errors encountered, fixes applied
- **The inflection points**: moments where the approach changed or something was discovered
- **The final result**: what exists now that didn't before

This map is your article outline. Every significant step in the conversation becomes a section.

### Conversation evidence, scope, and series boundaries

Treat the conversation as evidence with a declared scope, not as an automatically
publishable transcript. Capture or quote it only when the user has authorized
that use. If the available record is partial — for example, a recap, selected
turns, or a session artifact that omits private material — say so plainly in
the article or its provenance. Never describe a partial record as a complete
or verbatim transcript, and do not make claims that require absent turns.

When the session contains more than one substantial teaching arc, make a
series instead of stretching one article past its natural shape. Split on a
meaningful change in problem, decision, audience need, or transferable lesson;
do not split merely to meet a length target. Each part must stand on its own,
name its relationship to the series, and link clearly to the preceding or
following part. Preserve the exact artifacts needed to support each part's
claims.

---

## Article structure

### Title and subtitle
Each article deserves a unique title — don't use a fixed template. The title should be
**specific to this session** and carry a hook: something that names a tension, surprise, pivot,
or counterintuitive insight from the actual session.

Good approaches (pick the one that fits, don't force a formula):
- **The surprising outcome**: "The Dumbest Bug Taught Me the Most About Deno"
- **The tension or paradox**: "I Made My Proposals Longer to Make Them Shorter"
- **The pivot**: "I Started Building a Python Script and Ended Up With a Skill"
- **The core insight as the hook**: "Your Prompt Isn't Too Short. It's Missing Three Things."
- **The pattern of failure**: "Three Rounds of 'Not Quite' Built the Skill I Needed"
- **The before/after**: "From 'Review This Strategy' to Feedback I Could Actually Use"

Read the session, find the most interesting or unexpected thing that happened, and build the
title around that.

**Use a subtitle to carry the descriptive weight.** When the title is hook-y, the subtitle
should tell the reader concretely what was built, solved, or discovered, and what they'll see
in the article. Example pairing:
> *Three Rounds of "Not Quite" Built the Skill I Needed*
> *How a fuzzy idea about teaching through AI conversations became a working `/teaching-block`
> command — and what each failed version revealed.*

### Opening (2–4 short paragraphs)
State the problem plainly in first person: what you were trying to do, why, and what the
starting condition was. End by telling the reader what they're about to see.

This is orientation, not a hook. *"I was trying to X. I ran into Y. Here's what I found."*
The reader should know immediately: this is a personal account of a specific session, and
they're about to follow it step by step.

### Process sections (one per meaningful step or decision)

This is the core of the article. **Narrate in first person, past tense.** The author is walking
the reader through what they personally did — not instructing them how to do it. The difference:

> "Here's what I tried:" not "Here's what you should do:"
> "What came back was:" not "The output will be:"
> "I realized the problem was:" not "The problem in this case is:"

The reader is following along with the author's actual session. They should feel like they're
looking over the author's shoulder, not reading a tutorial.

**What to show in each section:**
- What the author tried or asked — verbatim when it matters (the actual prompt, the actual code)
- What came back — the actual output, error, or result. Quote or display it directly.
- Why this step was taken — the reasoning at the time, including wrong assumptions
- What it revealed — what changed in understanding because of this result
- What the author did next — and why

**For decisions and pivots:** show what was tried first, what the result was, and what prompted
the change. "My first instinct was X. Here's what happened. Here's why I went a different way."
Don't skip failed attempts — that's where the real teaching is.

**For code, prompts, or artifacts:** show them verbatim in code blocks. A paraphrase loses the
specificity that makes a teaching block replicable.

**For process flows or architecture:** use SVG diagrams actively — don't wait for an obvious
need. If a section describes a comparison, a sequence, a structure, or a before/after, a diagram
will almost always make it land faster than prose.

Good candidates in most sessions:
- **Before/after comparisons** — two states side by side (old prompt vs. new prompt, old structure vs. new)
- **Decision flows** — when a choice was made between two approaches, show the fork
- **Process sequences** — steps that feed into each other, especially with a feedback loop
- **Concept anatomy** — what a thing is made of (e.g., the three parts of a well-structured prompt)
- **Evolution diagrams** — how something changed across iterations

Create each SVG with the Write tool, save to the current working directory with a descriptive
filename, reference inline: `![Description](diagram-name.svg)`. Keep them clean: label
everything, use a simple color palette (2–3 colors max), prioritize legibility over aesthetics.

**Concept callouts:** when a step reveals a transferable principle, extract it explicitly:

> **Concept #N: [Short imperative principle.]**
> *One sentence on why this matters beyond this specific session.*

These pull the lesson forward. Don't bury them — a reader who only reads the concept stamps
should still walk away with the core insights.

**Concept stamps must be imperative, not declarative.** Imperative form lands harder and is
easier to remember. Compare:
- ❌ Declarative: *"Engaging and useful are not the same target."*
- ✓ Imperative: *"Don't conflate engaging with useful."*

The imperative form gives the reader a direct instruction to carry forward. The declarative form
makes them work to extract one. Always rewrite stamps to imperative before finalizing.

### What this unlocks (generalization section)

After the concrete walkthrough, add a section that answers: *"So what can someone do with this?"*

- Name the underlying pattern or principle (not the specific solution you built)
- Show at least one concrete adaptation: "Here's how you'd apply this to [different context]"
- Be practical: the reader should be able to take this pattern and use it in their own work

This is what separates a project writeup from a teaching block.

### Closing: key takeaways + how to start

**Key takeaways** (3–5 bullets): The most important things to understand from this process.
Concrete, specific, actionable. Not generic wisdom.

**How to start** (numbered steps): What should the reader do if they want to replicate this?
3–5 steps, specific enough to actually follow. Not "explore AI tools" — "Open a new chat and
paste this exact prompt structure."

Optional: 1-line sign-off (name + context).

---

## Voice and tone

Apply the **Professional Storyteller** style from `references/writing-style.md`.

The register is: **explaining to a capable colleague over coffee.** Honest, direct, practical.
You're showing your work and explaining why you made each choice — not performing expertise,
not dramatizing the journey.

The body is **first-person, past tense** throughout — not a tutorial. The author is recounting
what they personally did in a specific session. The reader follows along. Only shift to "you"
in the generalization section and the closing "how to start" steps.

Key language patterns for the body:
- "Here's what I tried first..." / "Here's why that didn't work..."
- "The prompt I used looked like this:" / "Here's what came back:"
- "My reasoning at the time was..." / "What this revealed was..."
- "I went back and changed X because..."
- "The pattern I noticed here:" (for concept callouts)

Shift to "you" only in the closing:
- "If you want to try this yourself, start by..."
- "Here's how you'd adapt this for your own work..."

Avoid:
- Tutorial voice in the body: "First, do X. Then, do Y." — that's a how-to guide, not a session walkthrough
- Generalizing before the concrete walkthrough is complete (no "the pattern here is..." mid-section; that belongs in the generalization section or a concept stamp)
- Literary throat-clearing or emotional dramatization
- Presenting the right answer first — show the wrong path when it existed
- Summarizing what the reader can see — show it, then explain it
- **Vague signals masquerading as specificity** — "something was off," "this is where it got interesting," "a new problem surfaced." If the article preaches show-and-tell, it has to model it: name the specific thing that was off
- **Em-dash density** — useful for asides, but stacking three or four in a paragraph creates rhythm fatigue. Vary punctuation

Length: as long as the process requires. A step with multiple failed attempts and a real learning
needs space. A step that was straightforward and confirmatory needs one paragraph.

---

## Output

Produce the complete article in Markdown:
- H1 title
- Opening (2–4 paragraphs)
- Process sections (H2 headers), each with: what was done, what was produced (verbatim where
  useful), why, and concept callouts where applicable
- SVG diagram files (saved separately, referenced inline)
- Generalization section
- Key takeaways (bullets) + How to start (numbered steps)

After the article, add a **"Behind the Article"** note (3–5 lines). This is editorial
transparency, not a TODO list. Cover:
- Which moments had the most teaching value (and why those over the others)
- Editorial choices: what was compressed, reordered, or left out — and why
- The single most valuable thing the author could add before publishing (concrete, specific)

Frame this as the author reflecting on the piece they just produced, not as instructions to a
future editor.

---

## Audit pass before finalizing

Before delivering the article, run through this checklist. Most drafts have at least two of
these issues; fixing them is the difference between a usable draft and a publishable one.

**Voice:**
- [ ] Body is first-person past tense throughout (only "you" in generalization + closing)
- [ ] No tutorial-voice sentences in the body ("First, do X. Then, do Y.")
- [ ] Wrong path is shown before the right answer in any section where one existed

**Concept stamps:**
- [ ] Every stamp is in **imperative form** ("Don't conflate X with Y" not "X and Y are different")
- [ ] Stamps numbered sequentially across the article
- [ ] Each stamp can stand alone — a reader who only reads the stamps still gets the lessons

**Specificity:**
- [ ] No vague signals ("something was off," "a new problem surfaced," "things got interesting") —
      replace with the specific thing that was off
- [ ] Verbatim artifacts shown for any prompt, code, or output that's actually referenced
- [ ] Em-dash density checked — vary punctuation, don't stack three or four per paragraph

**Structure:**
- [ ] Title is unique to this session (not a template), with a hook
- [ ] Subtitle carries the descriptive weight
- [ ] Generalization section comes after the concrete walkthrough, not woven through it
- [ ] At least one diagram for any comparison, evolution, or anatomy that appears in the article
- [ ] "Behind the Article" reads as editorial transparency, not a TODO list
- [ ] Conversation-derived claims match the evidence actually available; any
      recap, selected-turn record, or redacted capture is labeled with its scope
- [ ] If the work became a series, every part has a coherent teaching arc and
      clear navigation to the related part(s)

---

## Optional arguments

- **Title**: use verbatim
- **Audience note** (e.g., "for AIMM beginners"): adjust assumed baseline knowledge
- **Focus** (e.g., "emphasize the decision-making"): weight that aspect more heavily
