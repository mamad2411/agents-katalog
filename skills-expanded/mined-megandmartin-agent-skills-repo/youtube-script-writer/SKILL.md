---
name: youtube-script-writer
description: Writes retention-structured YouTube scripts — a cold-open hook inside 15 seconds, open loops seeded and paid off, timed segment beats, a b-roll/visual notes column, and one clear CTA. Use when the user asks to "write a YouTube script", "script this video", "outline my video", "hook for my video", or turns a topic/brief into a filmable script. Don't use for slicing a finished video into clips and posts — that's content-repurposer.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Content & Marketing, YouTube, Video, Scripts, Retention]
    related_skills: [content-repurposer, brand-voice-guardian, deep-research-brief, x-thread-builder]
---

# YouTube Script Writer

Produces a script built for the retention graph, not the writer's ego: the payoff is promised in the first 15 seconds, every segment earns the next, visual direction rides alongside every line, and the viewer leaves with exactly one thing to do. If a line doesn't hold attention or move the argument, it gets cut.

## When to Use

- The user has a video topic, brief, or rough notes and needs a filmable script.
- An existing script is bleeding viewers and needs a retention restructure.
- The user asks for "a hook", "video outline", "talking-head script", or "script with b-roll notes".
- **Not for:** repurposing a published video into clips, posts, or a newsletter (`content-repurposer`), or researching the video's claims from scratch (`deep-research-brief` first, then script from the brief).

## Quick Reference

| Action | Rule |
|---|---|
| Cold open | ≤15 seconds (~40 words). State or show the payoff. Never "hey guys, welcome back" |
| Open loops | Seed 2–3 early ("later I'll show you the one that failed"), pay off every one |
| Segment beats | 60–180 seconds each; every beat ends with a reason to keep watching |
| Visual column | Every script row pairs VO/on-camera line with a b-roll, screen, or graphic note |
| CTA | Exactly one, placed after the core payoff — not stacked in the outro |
| Word budget | ~150 words per minute of runtime; verify with `wc -w` against target length |

## Procedure

1. **Gather** — confirm: topic, target runtime, audience and what they already know, the single payoff (what the viewer can do/say after watching), the one CTA, and any source material. Missing payoff or CTA → ask before writing; a script without a payoff is a ramble.
2. **Write the hook first, three ways** — draft 3 cold opens (≤40 words each): a result shown, a stakes question, a pattern interrupt. Pick one, keep the others as alternates in the deliverable. Hard rule: no channel intro, no "in this video I'm going to", no greeting. First line is already the content.
3. **Beat out the spine** — list 3–6 segments with a working title, target timestamp, the claim or step each covers, and the curiosity handoff into the next. Seed 2–3 open loops here and note where each pays off. Success: reading only the beat list tells the whole story.
4. **Script each segment** — write in the two-column format below: spoken line left, visual note right. Spoken lines are conversational (contractions, short sentences, second person). Every 30–45 seconds the visual note must change — static talking head past that mark is a retention leak.
5. **Place the CTA** — one CTA, immediately after the core payoff lands, phrased as the natural next step ("grab the template", "watch X next"). Subscribe asks ride inside a segment transition at most once, in one sentence.
6. **Trim to runtime** — `wc -w` the spoken column; target = runtime minutes × 150. Over budget → cut whole tangents, not adjectives. Confirm every seeded loop is paid off (search the script for each loop's promise).
7. **Deliver** — full Output Template: hook alternates, beat map, two-column script, CTA, and a title/thumbnail-concept pair that matches the hook's promise.

## Output Template

```
# Script: [Working Title] — [target runtime]
**Payoff:** [what the viewer gets] | **CTA:** [the one action]
**Title options:** 1) ... 2) ... 3)  **Thumbnail concept:** [one line]

## Cold Open (0:00–0:15) — chosen
[≤40 words] | VISUAL: [what's on screen]
Alternates: A) ... B) ...

## Beat Map
| # | Segment | Time | Job | Loop seeded/paid |
|---|---|---|---|---|

## Script
| Spoken | Visual / B-roll |
|---|---|
| [line] | [b-roll / screen / graphic / on-camera] |

## CTA ([timestamp])
[exact wording] | VISUAL: [end screen / lower third]
```

## Pitfalls

- **Throat-clearing open** — the script sneaks in a greeting, channel intro, or "today we're going to talk about". Recovery: delete everything before the first line that contains the payoff or the stakes; if nothing survives, rewrite hook per step 2.
- **Orphaned open loops** — a promise seeded at 0:40 never pays off, and comments call it clickbait. Recovery: in step 6, list every seeded loop and its payoff timestamp; any orphan gets paid off or unseeded before delivery.
- **Empty visual column** — long stretches read "talking head" because the visual thinking was skipped. Recovery: walk the script in 30–45s windows; every window needs a visual change — b-roll, screen capture, text overlay, or camera angle note.
- **Essay voice** — long subordinate clauses that read fine and speak terribly. Recovery: read the spoken column aloud; any sentence you stumble on gets split into two.
- **CTA pile-up** — like, subscribe, comment, link, and a second video all crammed in the outro. Recovery: keep the one CTA from step 1; everything else is cut or reduced to a single mid-roll sentence.

## Verification

- [ ] Cold open ≤40 words, contains payoff or stakes, zero greeting/intro phrases
- [ ] Every seeded open loop has a marked payoff timestamp
- [ ] Every script row has a non-empty visual note; no 45s window without a visual change
- [ ] Spoken word count within ±10% of runtime × 150 (`wc -w` run, not eyeballed)
- [ ] Exactly one CTA, placed after the core payoff
- [ ] Title options promise the same thing the hook promises
