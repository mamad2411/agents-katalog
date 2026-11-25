---
name: write-generation-prompt
description: Write a prompt for an image or video generation model, as a document that justifies every word in it. Use when the user asks for a generation prompt, or brings back a rendered result that came out wrong.
---

# Writing a generation prompt

An image model is far more literal than you are, and it cannot ask what you meant. Every word lands somewhere. The prompt is closer to poetry than to prose: each word is a sculpting step at something already defined.

Two failures compete. Aim short and the requirements that were hard to satisfy fall out quietly, or the words thin until they stop holding together. Aim thorough and the prompt fills with your own map of meanings — the justifications, the hedges, the explanation of what you meant by the word you already wrote.

The four sections give that reasoning somewhere else to live, so the prompt itself can be measured. Answer in them.

## 1. Requirements

Bullets. What the picture has to achieve, written before the prompt exists.

This is what a trim is measured against. A shorter prompt that drops a requirement is a worse prompt, and the requirement that goes first is always the one that turned out hard to render — which is why it is written down before the drafting starts.

## 2. The prompt

The literal text, ready to paste. Everything in it is there to be rendered.

## 3. Every word, justified

One line per word, in order: what it does, what it connects to, which requirement it serves. Words, not phrases. Give the small connecting words as much room as they need and no more.

This **ledger** is the mechanism. Paying a line per word makes padding cost something, so it stops being free, and a word you cannot write a line for is a word to cut. The map of meanings lives here, which is how the prompt keeps none of it.

## 4. Notes

Free space: what was tried, what the image model keeps getting wrong, alternatives considered, what is still open.

## What moves a result

Held loosely. Each has exceptions.

- **Fewer words win.** Room to drift grows with length.
- **State the wanted condition.** A negation names the thing it forbids, and the model draws it: "no lettering" draws lettering. A described bare surface excludes the sign by itself.
- **A wrong result asks for a better positive sentence.** The pile-on — "with no wall, tower, buttress or building anywhere" — is the most expensive habit there is, and it arrives disguised as diligence.
- **Name what everybody pictures alike; describe the shape of everything else.** A shared name fixes a design in one word. A precise but obscure term resolves to something plausible and wrong, and four careful sentences each fetch the nearest common object instead.
- **Repetition is weight.** Saying a thing twice is counted twice, and it competes with the words that decide.
- **Some words carry a prior you lose to.** Where the image model holds a strong expectation about what belongs on a surface or in a role, describe the alternative and let it stand; arguing with the expectation feeds it.
- **Some words name an artefact rather than a subject.** "Character sheet" fetches a games-industry asset — flat vector fills, nothing drawn — and no amount of describing the character reaches past it. Two words came out and the picture arrived.

## Revising

A result that came back wrong is a fault in the ledger: some word did work nobody asked for, or a requirement never reached the prompt. Find it there, edit the document, and keep what the attempt taught in the notes.

The structure is the whole of the discipline. Prompt length, and whether the ledger lists or tabulates, stay the user's call.
