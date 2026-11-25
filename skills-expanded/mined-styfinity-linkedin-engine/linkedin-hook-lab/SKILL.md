---
name: linkedin-hook-lab
description: Generate ten scored hook variants for one topic, one per formula, and recommend the strongest two. Use when you have a post topic and need the opening line that stops the scroll.
argument-hint: "[the topic + who it is for]"
---

# LinkedIn Hook Lab

The hook decides whether the post gets read. This skill writes ten openers across ten proven formulas, scores them, and hands you the two best.

## Inputs
- The topic and the audience it is for: $ARGUMENTS
- The brief (persona tone, pains, offer, voice profile) loads automatically.

## Do this
1. Write one hook for EACH of the ten formulas, in this order:
   - Pattern-Break (says the unexpected thing first)
   - Counter-Intuitive Insight (the truth most people get backwards)
   - Experience-Led Observation (what you noticed doing the work)
   - Direct Consequence (the cost of ignoring this)
   - Confession + Result (an admission plus what it produced)
   - Numbered Promise (a specific count of takeaways)
   - Enemy-Hero-Gasoline-Teaser (name the villain, the win, the open loop)
   - BREAKING / News (frame it as fresh signal)
   - Stat-Anchored (X% vs Y%, a real or clearly-illustrative contrast)
   - Mechanism-Reveal (the "here is how it actually works" angle)
2. Keep each hook under 235 characters so it survives the "see more" cut. Count them.
3. Score each hook 1-10 on the four value levers (dream outcome, perceived likelihood, time-to-result, effort-and-sacrifice) plus scroll-stop power.
4. Pick the top two. Say in one line why each beats the rest.

## Output
A table of the ten hooks: formula, hook text, character count, score. Then the recommended two, each with a one-line reason. End with a note: pass the chosen hook to the post draft, then run /linkedin-humanizer on the result.

## Rules
- Counter-intuitive and BREAKING hooks must still be true and defensible. No claim the body cannot pay off.
- No clickbait. If the hook over-promises, score it down and say so.
- Real numbers only with honest attribution: "a post that did 12,000 impressions", never a named person or company.
- No em-dashes. Draft only - the operator picks the winner and writes the post.
