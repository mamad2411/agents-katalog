---
name: de-slop
description: Remove AI-sounding language, robotic phrasing, generic polish, or corporate jargon while preserving the user's meaning and personal style.
---

# De-Slop

## The Job

Take a draft that smells like AI and return one that doesn't, without flattening the writer's voice or changing what the text says. This is an edit, not a rewrite: the goal is the same message with the machine fingerprints removed.

## The Tells

Scan for these patterns. Every finding gets fixed, not just flagged.

**Words and phrases that scream AI:**
- em dashes used as the default connector (replace with a period, comma, or restructure)
- "delve", "tapestry", "testament to", "game-changer", "unleash", "elevate", "seamless", "robust", "landscape" (as in "the AI landscape"), "navigate" (for anything not physical), "unlock", "supercharge"
- "It's not just X, it's Y" and every cousin of that contrast frame
- "In today's fast-paced world" and any opener that surveys the world before saying anything
- "Let's dive in", "Let's explore", "Buckle up"
- "honestly" or "to be honest" as an opener
- "In conclusion", "At the end of the day", "The bottom line is"
- Hedging stacks: "It's worth noting that", "It's important to remember", "arguably"

**Structural tells:**
- The rule of three everywhere: "clearer, faster, and more effective". One triple is fine; a triple in every paragraph is a fingerprint.
- Every paragraph the same length, every sentence the same rhythm. Real writing has short ones. And longer ones that wander a little before landing.
- Headers for a 200-word text, bullets where sentences would do, bold on random phrases.
- Symmetric constructions repeated: "Whether you're a X or a Y", "From A to B".
- The summary paragraph that restates what was just said.
- Exclamation marks doing enthusiasm the words didn't earn.
- Emoji as section decoration.

**Substance tells:**
- Claims with no specifics: "many experts agree", "studies show", "can significantly improve".
- Advice that would be true for anyone, attached to nothing concrete.
- Perfectly balanced takes that refuse to have an opinion.

## How to Run It

1. Read the full draft first. Identify the writer's actual voice from the parts that sound human; those parts are the calibration, not your own style.
2. Do the pass: fix every tell. Prefer the smallest edit that kills the pattern. Vary sentence length deliberately. Replace vague claims with the specific the writer implied, or ask for the specific if it's missing and it matters.
3. Keep the writer's quirks: their slang, their formatting habits, their level of formality. If they write in lowercase, the result stays lowercase. De-slop removes the machine, not the person.
4. Return the cleaned draft, then a short list of what was changed and why, grouped by pattern (so the writer learns their own tells). Keep the list tight; the draft is the deliverable.
5. If the text is already clean, say so and change nothing. Do not invent edits to look useful.

## What This Skill Never Does

- Change facts, claims, names, or numbers.
- Add new arguments or remove the writer's opinions.
- Impose a "professional" tone on casual writing or vice versa.
- Run any content anywhere; the edit happens entirely in the conversation.

## Capability Contract

- Reads: the draft the user provides, or a file they point to.
- Writes: the cleaned version as a file only when asked; otherwise in the conversation.
- Network: none.
- External actions: none. Never publishes or sends the result anywhere.

## Completion Checklist

- Zero em dashes used as connectors remain
- No banned phrase from the tells list survives
- Sentence rhythm varies across the piece
- The writer's voice markers are intact
- The change list teaches the writer their top 3 recurring tells
