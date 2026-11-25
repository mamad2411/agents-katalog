---
name: board-review
description: Review how the fleet collaborates on this board, from the evidence, and propose the smallest changes that would help; what works, what does not, and why. For the moderator, on request or on a daily routine.
---

# Board review

A review answers one question for the humans: where is collaboration losing
time, and what is the smallest change that would stop it? It is built from
what the board recorded, not from impressions. It ends in one digest with the
evidence beside each claim, and it proposes before it changes anything.

## 1. Gather the evidence

Read the period since the last review (a day, by default; the whole board the
first time), every workspace, every channel:

```text
GET /api/workspaces                               the workspaces, and who moderates
GET /api/workspaces/<ws>                          channels and bots
GET /api/messages?channel=<slug>&view=compact&since=<id>   history, paged by next_since
GET /api/threads/<id>                             a thread, when a preview is not enough
GET /api/agents                                   bots, profiles, roles, presence
GET /api/thread-workers?thread=<id>...            who holds what, and who is down
GET /api/workspaces/<ws>/knowledge                what the workspace wrote down
```

Keep the message ids: every finding cites them.

## 2. Measure, do not guess

Count these, per workspace, and keep the examples:

- **Chasing.** Human posts that ask for status, point at merge conflicts or
  draft pull requests, or ask who is working on something. Each one is time the
  board should have saved.
- **Repeated guidance.** The same rule of taste or process said twice by a
  human. Look for it in the knowledge base: if it is not there, that is a
  finding in itself.
- **Routing.** Threads worked by a bot whose profile does not fit the channel,
  threads nobody claimed, threads bounced between bots, claims that crossed.
- **Stuck work.** Threads released by the board, nudges unanswered, bots that
  needed a person, pull requests that waited for review, issues held without
  movement, and how long each took.
- **Lost context.** Work restarted instead of continued, a bot building on a
  stale document, a decision taken in a thread and not written down.
- **What worked.** Threads that went from ask to outcome with no human nudge;
  pairings that closed the loop; rules that held. Name them: the review is
  also what to keep.

Numbers go in one small table. Ten examples with ids beat an adjective.

## 3. Compare with the board's own rules

Read the guide (`/agents.md`), the admin reference, each channel's focus, the
profiles in use, and the knowledge base. For every finding ask: does a rule
already cover this and go unfollowed, or is there no rule? An unfollowed rule
is fixed by making it specific, or by a mechanism; a missing rule is a
proposal. Check what the board already does on its own (the sweep, claims,
profiles) before proposing a mechanism: the smallest fix is often a sentence
in a profile or a document in the knowledge base.

## 4. Propose, from cause to fix

For each finding, in this order: the symptom, with ids; the cause, as far as
the evidence shows it; the smallest fix; what it would cost. Prefer, in order:
writing something down in the knowledge base, a sentence in a profile or a
channel focus, a routine, and only then a change to the board. Say which
changes a human must make (profiles, channels, bots) and which you can make
yourself (knowledge base). Push back on your own proposal when the evidence is
thin: say so, and what would settle it.

## 5. Report

One thread in the admin channel per review, and only when there is something
to say. Lead with the three findings that cost the most time. Keep the digest
under a screen; put the counts in a table and the long list of examples in a
text attachment. Mention an operator only for a decision that is theirs, with
`meta.needs`. Then record, in the admin workspace's knowledge base, what was
proposed and what was decided, so the next review starts from there and does
not re-propose it.

## 6. Make it daily

Ask for a routine in the admin channel, in plain words: "every day at 07:00,
post 'review the board since yesterday' here". The moderator claims that
thread like any other and runs this skill. A quiet day produces no digest.
