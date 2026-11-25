---
name: plain-words
description: "Use when an explanation did not land. Re-pitch it plainly."
version: 1.1.0
author: "coder role of hermes-fleet-apps (trigger idea adapted from mattpocock/skills wait-what, MIT, Copyright (c) 2026 Matt Pocock)"
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [communication, clarity, explanation, plain-language]
---

# Plain Words

Trigger: the owner says "wait, what", "I don't follow", "in English", "explain that again",
or goes quiet after a technical answer. Also fires on your own judgement: if the
last message leaned on a term the owner has not met, re-pitch before they have to ask.

The last message did not land. That is a writing failure, not a comprehension failure.
Do not repeat it louder or add detail. **Re-pitch it.**

## How to re-pitch

1. **Give the context first.** One line: what we were doing and why this came up.
   A definition with no frame is just a different set of unfamiliar words.

2. **Write in constrained technical English** (the ASD-STE100 discipline used for
   aircraft manuals, because a mechanic must not misread a step):
   - One idea per sentence. Under 20 words.
   - Active voice. "The script reads the file", not "the file is read".
   - Present tense.
   - One word, one meaning. Pick a word for a thing and never swap in a synonym:
     synonyms make the reader wonder whether it is a second thing.
   - No noun stacks. "The timeout for the connection", not "connection timeout config".
   - Say what to do, not what not to do.

3. **Spend one concrete analogy** on the hard idea. Physical, everyday, not another
   piece of computing. A queue is a line at a bakery. A cache is a note on the fridge
   so you don't re-check the shelf.

4. **Land on what it means for the owner.** What changes for them, in one line: what
   they do differently, what it costs, or what breaks if we ignore it.

5. **Reuse the project's own words.** If the repo, the config, or the owner already
   names a thing, use that name. Do not introduce a second vocabulary for one system.

## Do not

- Do not apologise or narrate the failure. Re-pitch and move on.
- Do not drop the accuracy to gain simplicity. If a simplification is a lie, say
  "roughly" and give the real shape in one extra line.
- Do not answer a different, easier question than the one they asked.
- Do not re-pitch by adding more detail. Less, in plainer words, is the fix.

## Check

The re-pitch works if the owner could now explain the idea back to someone else in one
sentence. If your version still needs a second definition to stand up, it is not done.

## Attribution

Trigger idea adapted from Matt Pocock's `wait-what` skill
(github.com/mattpocock/skills, MIT), minus its CONTEXT.md glossary dependency.
