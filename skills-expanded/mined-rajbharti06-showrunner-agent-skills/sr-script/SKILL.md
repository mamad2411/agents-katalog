---
name: sr-script
description: Writes and times scripts for short vertical video and long YouTube videos. Structures the hook, the promise, the beats with open loops, the payoff and the loop back, writes for the ear in the creator's voice, then times it and flags a hook that runs long, beats that sit still, filler runs, an early call to action and a missing loop. Use when someone needs a script, a talking-points outline, a voiceover, a faceless video, or asks "how long will this run" or "why do people leave my videos".
license: MIT
compatibility: Any agent that loads Agent Skills. Python 3.9+ for the timing tool; the by-hand method below works without it.
metadata:
  author: Raj Bharti
  version: "0.1.2"
  family: showrunner
---

# Scripts

Write for the ear. People will hear this once, at speed, with a thumb ready to swipe.

## Ask first

- The chosen hook and idea (from `sr-hook`, `sr-ideas`).
- Format and rough length: a short (15 to 60 seconds), a longer short, or a long video.
- On camera, voiceover over b-roll or screen recording, or text on screen only.
- What should the viewer do or feel at the end? One thing.

## Short video structure

Think in beats of two to four seconds. A new beat means something changes: a cut, a new line of text, a new angle, a new fact.

1. **Hook** (0 to 3 s). The chosen hook.
2. **Context in one line.** Why this matters to them, or the setup. Skip it if the hook already did it.
3. **Three beats.** Each gives one new fact, step or turn. Open a loop early ("the third one cost me a month") and close it late.
4. **Payoff.** The thing the hook promised, stated plainly.
5. **Loop or ask.** End on a line that echoes the hook so a second watch costs nothing, or make one small ask. One, not three.

## Long video structure

1. **Cold open** (first 15 to 30 seconds). Deliver a taste of what the title promised. No logo, no channel intro, no "before we start".
2. **The map.** One sentence on what is coming, so people can decide to stay.
3. **Sections of 60 to 120 seconds**, each with its own small hook ("here's where it gets tricky"), its own payoff, and a visual change.
4. **Re-hook at every dip.** After reading retention (`sr-audit`), put a reason to stay where people tend to leave.
5. **Close** that pays off the title and points to one next video.

## Write like speech

Short sentences. Contractions. Words you would say to a friend. Numbers as you would say them. Read it aloud once. Anything you stumble over, rewrite. Keep the creator's own phrasing and rhythm (`sr-voice`).

## Faceless variant

Mark each line with what is on screen: screen recording, b-roll, text, diagram. A line with nothing changing on screen for more than about four seconds needs a visual change or a cut.

## Time it

Tool `script_beats` with the script as `text`, optionally `target_seconds` and `wpm` (their speaking pace; 150 to 180 is normal). CLI: `python scripts/sr.py beats --file script.txt --target-seconds 40`.

It splits into beats, estimates seconds, and flags: a hook over three seconds, beats over four seconds, dense beats, three beats in a row with no number, name or turn, no echo of the hook at the end, a call to action before the halfway point, and distance from the target length. Fix every flag or decide on purpose to keep it.

By hand: words divided by speaking pace in words per minute gives minutes. Mark every sentence end and check no stretch runs past four seconds without a change.

Estimates are text-only. The first real read-through and the first retention graph beat any estimate.

## Gate

`approve`. They read it aloud and say what does not sound like them.

## Do not

- Pad to hit a length. Shorter and tight beats longer and slack.
- Put the call to action at the start.
- Write anecdotes the creator did not live.
