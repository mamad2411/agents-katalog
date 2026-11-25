---
name: sr-hook
description: Writes and scores hooks, the first line, first three seconds or first frame that decides whether anyone keeps watching or reading. Drafts ten options in different shapes from 32 common structures, scores them on specificity, front-loading, who it speaks to, curiosity, stakes and brevity, fixes the weakest part, and returns the best three. Use for Reels, TikToks, Shorts, YouTube openers, LinkedIn or X first lines, and when someone says their videos get swiped away or asks "is this a good hook".
license: MIT
compatibility: Any agent that loads Agent Skills. Python 3.9+ for the scoring tool; the by-hand rubric below works without it.
metadata:
  author: Raj Bharti
  version: "0.1.2"
  family: showrunner
---

# Hooks

A hook has one job: earn the next three seconds. Everything else in the piece depends on it.

## Ask first

- What is the piece about, in one sentence?
- What is the most surprising or specific true thing in it? A number, a name, a cost, a result.
- Who is it for? (Name the person, not "everyone".)
- Where will it run: vertical video, YouTube, or a written post?

## Write ten, in different shapes

Open `references/hook-shapes.md` (or call `hook_formulas`). Pick five to six shapes that fit the piece and write one or two hooks in each. Fill the blanks only with **true** details the creator gave you. Vary the length. Write them the way the creator talks (`sr-voice`).

A strong video hook usually works on three layers at once. Write all three:

1. **Spoken:** the first sentence out loud.
2. **On screen:** the first text overlay, which should add to the spoken line, not repeat it.
3. **Visual:** the first frame. Movement, a face, or the thing itself. Not a logo or a title card.

## Score

Tool `hook_score`, one hook per line, with `platform` set to `short` (vertical video), `long` (YouTube) or `text` (written posts). CLI: `python scripts/sr.py hook --file hooks.txt --platform short`.

The six checks, which you can apply by hand:

| Check | What it rewards |
|---|---|
| Specificity | A number, name, place or time in the line |
| Front-loading | The claim comes first, with no greeting, preamble or "so today" |
| Address | It talks to someone ("you", or names who it is for) |
| Curiosity | A gap is opened and not closed in the line |
| Stakes | A cost, a gain, a risk |
| Brevity | About 10 to 12 spoken words for short video |

Dealbreakers cap the score: greetings ("hey guys"), asking for attention ("you won't believe"), begging to subscribe, announcing the video ("in this video"), and shouting. Warnings take points off.

Read the report for the **weakest part** and the one-line fix. Rewrite the top three using that fix and score again. Two rounds is enough.

## Be straight about the score

It is a text heuristic. It has not been validated against views. It cannot see delivery, the first frame, the edit or the audience. Use it to rank options and find the weak part. If the creator has 30 or more posts with views, offer `calibrate_run` (see `sr-growth-loop`) so they can see which checks hold for their audience.

## Hand back

The best three, each with its score, shape and the exact on-screen text and first frame. Say which you would pick and why in one sentence.

## Gate

`approve`. They pick one, or say what to change.

## Do not

- Fill a shape with a made-up number or story.
- Promise a payoff the piece does not deliver. The cost is retention and trust.
- Write the same hook for every platform. Rewrite the first line for each.
