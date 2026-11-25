---
name: linkedin-story-miner
description: Mine a description of recent work into ranked, anonymised proof stories ready to become posts. Use when you have wins or builds but no idea what to post about.
argument-hint: "[a description of recent work, wins, or builds]"
---

# LinkedIn Story Miner

Your work is full of posts you haven't written yet. This skill pulls the proof stories out of what you just did, strips the identifying details, and ranks them by how hard they prove you can do the job.

## Inputs
- A description of recent work, wins, or builds: $ARGUMENTS
- The brief (persona, offer, the operator's positioning as a Revenue Partner) loads automatically.

## Do this
1. Read the raw work and pull out every candidate that carries proof. A proof story has one of: a before/after number, a hard-won lesson, or a contrarian result that goes against the obvious play.
2. Anonymise each one. Strip names, company names, and any detail that identifies a person or client. Keep the real numbers. "Took a client from X to Y" stays as a number with no name attached.
3. Score each story on proof strength: how strongly it shows the operator can produce the outcome the ICP wants. A measured before/after outranks a vague lesson.
4. Rank them strongest proof first.
5. For each, name the angle (the single point it makes) and suggest the hook formula that fits: the contrarian take, the before/after, the mistake-I-made, the counterintuitive number, or the behind-the-build.

## Output
A ranked list of story seeds. For each: the anonymised proof (one or two lines, numbers intact), the angle, and the suggested hook formula. Top seed first. End with a one-line note on which seed to turn into a post next, and a pointer to draft it.

## Rules
- Keep numbers, drop names. This is for public posts, so no real person, company, or client is identifiable.
- Never fabricate a result or round a number up. If a story has no real proof, mark it as a softer "lesson" seed, do not invent a metric.
- Attribute every number to "a post", "a client", or "an operator", never a named entity.
- No em-dashes. This is a seed list, not a finished draft. Hand the chosen seed to a drafting skill, then run /linkedin-humanizer before it goes live.
