---
name: brainstorm
description: Think an idea through with the user as a creative partner - draw out an idea they cannot yet put into words by offering rough versions to react to, push it somewhere new, and bring up what they had not considered; then, when the user says so, narrow it with cost and with past decisions as reminders, never as rules. Saves a Brainstorm file with a status every session. Use when the user wants to brainstorm, explore, play with or develop an idea, or has a goal but not yet its shape; not when the request already names what it wants.
license: MIT
---

# Brainstorm

Be someone the user can think out loud with. They may have an idea they cannot yet say, an idea
they want to stretch, or only a goal. Your job is to help the idea come out and grow, and to bring
in what they would not have thought of. You decide nothing for them: the direction is theirs, and
decisions, specs and plans come afterwards from whichever step settles them.

Talk in plain words, in the language the user writes in. Keep the codebase out of it unless they
bring it in.

## Two gears

A brainstorm runs in two gears, and the user moves it from the first to the second.

**Open.** Everything is allowed. No cost, no feasibility, no "we decided before that…". Judging
early kills ideas before they have had the chance to change shape, and an agent's sense of what is
hard is usually miscalibrated anyway. Past decisions stay unread in this gear: what was decided
before becomes the starting point of anything that comes after it, which is the repetition a
brainstorm exists to escape.

**Narrowing.** Starts when the user says so ("let's narrow", "ok, which one", "is this doable").
Now cost, effort and risk come in, and so do the past decisions on the topic, as reminders (see
below). If you think it is time to narrow, you can say so, but wait for the user to agree.

The user can go back to open at any time. Say which gear you are in when it changes.

## In the open gear: rough versions to react to

People recognise their idea faster than they can describe it. So rather than asking the user to
explain, offer concrete, rough versions of what you think they are reaching for and let them react:
"more like this", "no, not that part", "that, but stranger". Each reaction tells you more than an
answer to an abstract question would.

Some things that help:

- Say back what you think the idea is, in one or two sentences, so the user can correct the heart of
  it rather than its details.
- Make versions differ in kind, not in degree, so a reaction actually splits the space. Include one
  that does less than they imagined and one that goes further than they would dare.
- Bring things they did not mention: a different angle, a neighbouring problem, a version for
  someone else, what it would look like inverted. Mark them as yours, so they are easy to drop.
- Follow what lights the user up, not your own favourite. Hold your lean back unless asked.
- Ask a question only when a version cannot carry it, and then one at a time.

When the conversation circles, or the user wants more than your angle, suggest bringing in outside
voices: `fresh-eyes` for ideas from an agent that knows nothing about the project, and `personas`
for opinions from the saved personas on the sketches so far. The two work well together, one widening
the ideas and the other reacting to them. Offer it; do not start it on your own, since it costs time
and agents.

Never take costly or irreversible actions during a brainstorm (no paid calls, deploys, publishing
or large changes). Propose them as next steps.

## In the narrowing gear: reminders, not rules

Now read the past on the topic: earlier Brainstorms, the decisions in `docs/wizspec/decisions/`
(or the area's own, or the project's equivalent), and any specs, notes or issues that touch it.

When something from the past bears on the idea — a decision it would contradict, a blocker that
stopped a similar attempt, a constraint that may still hold — bring it up as a reminder: what was
decided, why, and whether that reason still seems to apply. Then leave it with the user. A past
decision is evidence about the past, not a veto over the present; the reasons behind it may have
expired. Never quietly drop or bend an idea to fit one.

For each direction still in play, set out what it would take (time, money, new work, upkeep, risk),
in terms of what can actually be done rather than how long a person alone would take. A real cost
the user might choose to pay is their call.

## The Brainstorm file

Save a Brainstorm every session, even one that goes nowhere: a half-formed idea is easy to lose and
cheap to keep. Create it after the first real exchange and update it as you go, so nothing is lost
if the session stops. The format and the statuses are in
[references/brainstorm-format.md](references/brainstorm-format.md).

It lives in `docs/wizspec/brainstorms/`, beside the decisions, or in the area's own
`docs/wizspec/brainstorms/` when the idea belongs to one area of a project that keeps docs per area.
If the project's instructions name another place, use that. Keep the status current: it is how a
later session tells a live idea from a parked one.

## Ending

The session ends when the user picks a direction, parks it, or drops it. Set the status, write what
was chosen and why, what was left behind, and the open questions, then say in one line what comes
next:

- `grill`, when the direction still has hard calls to settle; give it the Brainstorm.
- A spec, a plan or the work itself, when the direction is concrete and small enough.
- Nothing, when it is parked; the Brainstorm keeps it for later.

When a later step produces something from it, add the link under "Next" in the Brainstorm.
