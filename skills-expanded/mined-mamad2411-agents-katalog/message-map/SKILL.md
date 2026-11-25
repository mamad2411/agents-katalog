---
name: message-map
description: Distils the positioning into one core message, three supporting pillars with proof attached to each, and a banned-phrases list, then writes the map into the brief so every future piece of copy ladders to it. Use when content feels scattered, every asset says something different, or new writers keep inventing the message from scratch.
argument-hint: "[core claim if you have one, or 'work from the brief']"
---

# Message Map — one message, three pillars, proof attached

Scattered messaging is expensive: every asset that says something different resets the buyer's memory to zero. A message map fixes the argument once — the one thing the market must believe to buy, the three pillars that make it believable, the proof behind each — so every post, page, and email compounds the same case instead of starting a new one.

## Inputs
- A core claim if one exists, or the go-ahead to derive it: $ARGUMENTS
- From `marketing-brief.md` if present: the position sentence (the map inherits it), top pains and desired outcomes, the language bank, and any banned phrases already collected.

## Do this
1. Pull the position and the customer evidence. The core message is the position translated into the buyer's language — the one sentence the market must believe for buying to become the obvious move.
2. Draft the core message as a claim, not a slogan. It should be arguable — something a sceptic could disagree with. If nobody could disagree with it, it says nothing.
3. Choose the three pillars. Each answers one of the buyer's core disbeliefs, and each is a claim in its own right:
   - "It won't actually work."
   - "It won't work for someone like me."
   - "It isn't worth the money or the upheaval."
4. Attach proof to each pillar: numbers, demonstrations, mechanism explanations, customer results — only proof that actually exists. Where proof is missing, mark the pillar weak and name exactly what would fill it. A pillar without proof is a wish.
5. Build the banned-phrases list: category clichés, competitor-owned language, claims reality cannot back, and hype words the audience has learned to scroll past.
6. Run the ladder test on the five most recent pieces of copy or content: which pillar does each ladder up to? Anything that ladders to nothing is either off-message or evidence of a missing pillar — decide which.
7. Write the map into **Positioning & message** in `marketing-brief.md` — core message, pillars with proof, banned phrases. Inside Claude Code, the message-architect agent runs the deep version of this pass.

## Output
A one-page message map — the core message, three pillars each with claim, proof, and the disbelief it answers, plus the banned-phrases list — saved into `marketing-brief.md`. Name the weakest pillar and the proof that would fix it.

## Rules
- One core message. A brand carrying two core messages is carrying zero.
- Proof that does not exist yet is a to-do, never a claim. Ship the map with the gap visible.
- Pillars answer disbeliefs, not describe features. "Fast onboarding" is a feature; "you will not lose a quarter to switching" answers a fear.
- The map speaks the buyer's language. Pull phrasing from the language bank, not the boardroom.
- The map is a filter, not a suggestion. Copy that cannot find its pillar gets rewritten or killed.
