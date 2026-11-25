---
name: sr-strategy
description: Builds a creator's positioning and content strategy as a one-page brief: who they help, the one-sentence promise, three content pillars, the proof they can actually show, the single call to action, and what to stop doing. Use when someone asks about niche, positioning, brand, pillars, content strategy, "what should my channel be about", a rebrand, or a launch or campaign brief. Works from the intake answers and the person's real experience, never from invented credentials.
license: MIT
compatibility: Any agent that loads Agent Skills. No scripts needed.
metadata:
  author: Raj Bharti
  version: "0.1.2"
  family: showrunner
---

# Strategy: the one-page brief

A channel without a promise is a diary. A channel with one is something a stranger can decide to follow in five seconds.

## Before you start

Read the profile (`profile_get`) and the intake result. If either is missing, run `sr-intake` first. Then ask for proof: **what have you actually done, made, learned or survived that this audience cares about?** The brief is built from the answer, so get specifics: numbers, names of places and projects, dates, outcomes they can show.

## Build it in this order

1. **The viewer.** One real person, in one sentence. Job or situation, what they are trying to do, what is in the way. Use their words if the creator has talked to such people.
2. **The promise.** Under 15 words: "I help [viewer] [get result] by [your way]." Read it aloud. If a stranger would ask "how?", it is a good start. If they would ask "what?", it is too vague.
3. **Three pillars.** Three recurring topics that all serve the promise, each answerable from real experience. Three is enough to stay varied and few enough to build a reputation.
4. **Proof inventory.** A list of things the creator can show or point to. This is what makes content specific. If the list is short, say so, and plan content that builds proof (documenting a 30-day project, interviewing practitioners, publishing a result).
5. **The call to action.** One thing a follower should do next: subscribe, join a list, book a call, apply, download. One only, and consistent across profiles.
6. **The stop list.** Things that dilute the promise. Topics, formats and platforms to leave alone for the next 90 days.
7. **The 90-day target.** Not followers. Something the creator controls: posts published, a number of experiments, a first 10 replies from the target viewer, a lead conversation. Followers follow from work done.

Use the template in `references/strategy-one-pager.md` to write it up.

## Check it

- **Specific:** could a competitor in the same niche have written the promise? If yes, sharpen it.
- **Provable:** does every pillar connect to something on the proof inventory?
- **Sustainable:** can they make 12 posts per pillar without running dry? (Run `ideas_matrix` with the pillars to find out.)
- **Aligned:** does the call to action serve the goal from the intake?

## Gate

`approve`. Show the one-pager and ask what feels wrong or untrue. Fix that before anything else. Offer to save the pillars and proof to the profile (`profile_save` with `pillars` and `proof`).

## Do not

- Invent credentials, results, client names or testimonials.
- Pick a niche because it is "hot". Pick one the creator can talk about for a year.
- Write three promises and let the creator choose without a recommendation. Recommend one and say why.
