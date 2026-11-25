---
name: groom
description: Go through merl's open issues with the owner, one at a time, until each is `agent-ok` or parked. Use when the owner wants to sort, triage or prepare issues (for a night run, for a release), asks what needs them, or asks which issues have questions.
---

# Grooming issues with the owner

The owner sits down for an hour and wants to leave with a batch of issues an agent can build
without them. Each issue costs them one read and one answer: what they decide is written into
the issue at once, so nobody asks again. `AGENTS.md` `## Merging` says what the labels mean.

## 1. Pick

The owner names the issues or a number of them; without either, take 10. Order: `needs-owner`
by priority, then open issues with no readiness label, then `to-think` the owner asked about.
Leave `in-progress` ones out. Read each with its comments: the owner's latest comment overrides
the body.

Show the list as one table and wait for the owner's word: number, one line in the user's terms,
`Visible`, how many questions you have. An issue with no question left is not discussed: say it
will get `agent-ok` and label it.

## 2. Prepare what needs a picture

An issue whose question is how something looks or moves gets its `## Proposal` first
(`.claude/skills/proposal/SKILL.md`), in the background while the others are discussed. The
owner does not pick a look from a description; such an issue is asked about once its pictures
are up, or stays `needs-owner` with the proposal for their next pass.

## 3. Put the questions on the desk

Every question becomes a card on the decision desk, the owner's page for picking
(`desk.md` beside this file: the link, the card fields, the pictures). One card per question;
an issue with two questions gets two cards, `#N q1` and `#N q2`.

- Every question has options, one of them recommended. A question you can answer from the code,
  the forges or an earlier decision is not a question: answer it in the issue instead.
- The user's terms: keys, screens, messages. Code only when the owner asks how.
- A card whose question is a look waits for its proposal's pictures (step 2).

Send the owner the desk's link once, with how many cards are new, and wait for their word
(`готово`, done). Then read the answers: `pick` is the chosen options (the recommendation when
they pressed it), `later` parks the card, `note` is their own words. A new question in a note is
answered in chat before step 4.

## 4. Write it down, then move the label

For every answered card: the decisions go into the issue as a `## Decided` section at the top
of the body (the question, the pick, the owner's reason when they gave one), in English. Then:

- nothing left to ask, and nothing visible without a picked proposal: `agent-ok`;
- parked: `backlog`, with the reason in a comment;
- still open: stays `needs-owner`, the open question first in the body.

## 5. Close

Archive the cards you wrote down (`desk.md`), so the desk holds only what still waits. One
table: what became `agent-ok`, what waits for the owner and for what, what was parked. The
owner starts the build themselves (`.claude/skills/batch/SKILL.md`).
