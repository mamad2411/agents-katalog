---
name: learn-from-session
description: Turn today's coding session into a personal learning plan — find the best blogs/articles on what was built, verify their credibility via Hacker News/Reddit/Twitter mentions, give a plain-language rundown of what was built and why each approach was chosen, quiz the user conversationally to place their level, and order the reading. Use when the user says "find blogs about what we did today", "I want to learn what we just built", "go through our chat and get me reading material", "quiz me", or asks for learning resources tied to recent work.
---

# Learn From Session

The user learns by shipping first, studying after. This skill runs their exact loop: session recap → curated sources → credibility check → plain-language rundown → conversational placement quiz → ordered reading path.

## Workflow

### 1. Extract the topics

Review the current conversation (or the session the user points at) and list the 3-6 distinct technical topics actually exercised — not everything mentioned, the things where understanding them better would have changed a decision. Name each as a concrete, searchable phrase ("Chrome MV3 service worker lifecycle", not "extensions").

### 2. Find the best material

WebSearch per topic. Prefer, in order:

1. Writing by practitioners who built the thing (engineering blogs, framework authors, well-known independent bloggers).
2. Official docs *only* when they teach rather than merely reference.
3. Long-form explainers with real code.

**Favor interactive and educational blogs.** This user learns by doing, so among credible sources rank up the ones that teach actively — runnable code, embedded playgrounds/sandboxes, interactive diagrams or visualizations, "build it step by step" walkthroughs, animated or explorable explanations (e.g. the style of Josh Comeau, Amelia Wattenberger, Bartosz Ciechanowski, "explorable explanations"). A blog that lets you poke at the concept beats an equally-correct wall of prose. When two sources are comparable on credibility, pick the more interactive one and say so in the reading path ("has a live playground — change the values and watch the cap trip").

Reject: SEO listicles, AI-generated content farms, anything that doesn't say who wrote it. 2-3 sources per topic max — a shortlist gets read, a dump doesn't.

### 3. Credibility pass

The user explicitly wants this: for each recommended piece, search for mentions on Hacker News, Reddit, and Twitter/X. Report what you find ("400-point HN thread, mostly agreeing", "author is the maintainer of X", "no independent mentions found — judged on content alone"). Drop anything that got credibly debunked in comments.

### 4. Plain-language rundown

Before any quiz questions: give a short, jargon-free recap of what was actually built this session. Then, for each distinct technique or approach used, add one or two sentences on WHY that method was chosen over the alternative — name the rejected option and the tradeoff, in plain terms. Analogies welcome; genuinely simple beats precise-but-dense. Keep it tight: a few lines per concept, not an essay. This is teaching context that primes the quiz — it is not the 30-second recap in the output template, which stays.

Then pause and invite a reaction before testing: "does any of this feel shaky? tell me which and I'll go deeper before we quiz." Only move on once they've had the chance to flag something.

### 5. Placement quiz

5-8 questions across the topics, easy → hard, answerable in a sentence or two each — but ask them one or a few at a time, conversationally, not all at once as a wall. Grade and react as answers come in, adjusting difficulty if they're cruising or struggling. Grade honestly. For at least one concept, consider a concrete micro-prompt drawn from the actual session code — "predict the output" or "spot the bug" — concrete beats abstract for this user. The quiz decides where reading starts — no point recommending an intro piece for a topic they aced, or an advanced piece for one they missed.

### 6. Output: the reading path

```
## What you built today (30-second recap)

## Quiz results
topic → level (solid / shaky / new)

## Reading path (in order)
1. <title> — <author/source> · <time to read> · <why this one, and what to look for while reading>
   Credibility: <HN/Reddit/Twitter evidence>
...

## Skip for now
- <topic they already know / rabbit hole not worth it yet>
```

Order by: shaky-but-load-bearing topics first, then new topics, then depth on solid ones. Keep total first-pass reading under ~2 hours; offer a "going deeper" tier for later.
