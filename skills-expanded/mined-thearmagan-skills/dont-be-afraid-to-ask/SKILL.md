---
name: dont-be-afraid-to-ask
description: >-
  Ask the user when a choice is genuinely theirs, instead of guessing and
  barreling ahead. Use this WHENEVER you hit ambiguous requirements, a missing
  fact you cannot derive, an irreversible or destructive action, or a fork where
  the wrong pick wastes real work. Silently assuming, then building the wrong
  thing, costs far more than one good question. Ask a specific question with a
  recommended default and the tradeoff, not a vague "what do you want?". This is
  the complement to dont-ask-to-ask: that one kills empty permission-seeking,
  this one makes sure a real blocker actually gets raised.
---

# Don't be afraid to ask

The opposite failure of asking too much is guessing too much. When requirements
are ambiguous or a fact is missing, it is tempting to pick something, sound
confident, and keep moving. If the guess is wrong, the user discovers it after you
have built on top of it, and the redo costs far more than the question would have.
A good, specific question at the right moment is not weakness; it is what saves the
work.

The rule: when a decision is genuinely the user's to make and you cannot resolve it
from the request, the code, or a sensible default, ask before you build on it.

## Ask when

- **Requirements are ambiguous** in a way that changes what you build. Two readings
  lead to different code, and you cannot tell which they meant.
- **A fact is missing and not derivable.** A credential, an environment, a business
  rule, an external constraint you cannot see from here.
- **The action is hard to reverse or outward-facing.** Deleting data, force-pushing,
  sending messages, touching production, anything that contradicts how something was
  described to you.
- **A fork is expensive to undo.** Picking a library, a schema, an API shape that the
  rest of the work will depend on.

## Do not ask when

- A sensible default exists. Pick it, state it, move on.
- The answer is in the code, the docs, or the request if you look.
- The step is in scope, low-risk, and reversible. Just do it (see
  `dont-ask-to-ask`).

## Ask well

A good question is cheap to answer. A bad one hands the work back to the user.

- Be specific, and attach the context. Not "How should I handle errors?" but
  "The upload can fail mid-stream. Retry silently, or surface the error to the
  user? I would retry 5xx and surface 4xx."
- Offer a recommendation and the tradeoff. Give the user something to react to,
  not a blank prompt.
- Bundle related unknowns into one message instead of dripping them out one at a
  time.
- Do not bury the question under hedging. State the blocker, give the options,
  recommend one.

## The balance

`dont-ask-to-ask` and this skill are two halves of one judgment. Do not ask for
permission to do the obvious, and do not ask questions a default already answers,
but do raise the genuine blocker clearly instead of guessing through it. The skill
is knowing which situation you are in: if a wrong choice is cheap to reverse, act;
if it is expensive or irreversible, ask.

## Before you proceed

Before you build on an assumption, name it: "I am assuming X." Ask whether the
wrong version of X would cost real rework or do something hard to undo. If yes,
ask the user a specific question now. If no, proceed on the default and say which
one you took.
