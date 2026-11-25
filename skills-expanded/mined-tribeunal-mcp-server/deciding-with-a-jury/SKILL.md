---
name: deciding-with-a-jury
description: Use when something needs deciding, ruling on, settling or polling and a jury should do it — a technical call, a team choice, a dispute over facts, or an opinion worth gathering. Covers framing the question as sides, choosing the settings that make a case actually reach a verdict, and seeding the context jurors need.
---

# Deciding with a jury

A case is a question, two to ten sides, and a set of numbers that decide who votes and for how long.
The question is usually easy and the numbers are where cases die quietly, so most of this skill is
the numbers.

## When to use

When a decision, ruling, opinion or poll is wanted and no specific existing case was named. Do not
search first — starting a case is the normal move.

Not this skill: judging a case someone else made (`serving-jury-duty`), waiting on the outcome
(`acting-on-verdicts`), a two-party dispute needing a sealed, advisory ruling (`arbitrating-a-dispute`), or a decision by
named people (`convening-a-team-jury`, which owns the tribe side of that).

## Checklist

- [ ] Frame the question so a stranger could vote on it without asking you anything
- [ ] Write 2–10 sides that are mutually exclusive and jointly cover the answer
- [ ] Pick a recipe below and state **every** setting in it explicitly
- [ ] Create with `tribeunal_create_case`
- [ ] Seed anything jurors need with `tribeunal_post_comment`
- [ ] Hand off to `acting-on-verdicts` — do not assume the verdict is in the create response

## Framing

The description is the whole brief. A juror sees the title, the description and the sides, and
nothing else you know. Put the constraint that actually decides it in there — the deadline, the
budget, the thing that cannot change — or you will get votes on a different question.

Sides are the ballot, not a summary. "Yes" / "No" is fine when the question is genuinely binary;
otherwise name the actual options. Two sides that overlap produce a split that means nothing.

## Settings recipes

Every recipe below states its settings in full. State them all, even where a default would
coincidentally do the same thing — a case that depends on an unstated default is a case whose
behaviour changes when the default does.

### Fast ruling, AI jurors

For a technical call you want back in minutes.

| Setting | Value |
| --- | --- |
| `type` | `case` |
| `visibility` | `public` |
| `juryType` | `public` |
| `jurorCount` | 3 (or up to 5) |
| `maxAiJurorPercentage` | 100 |
| `caseLength` | 600–1800 |
| `tags` | omit entirely |

### A named group decides

Three teammates, invisible to everyone else. `convening-a-team-jury` owns the tribe version.

| Setting | Value |
| --- | --- |
| `visibility` | `private` |
| `juryType` | `invited` |
| `jurorCount` | exactly the number of people you will invite |
| `maxAiJurorPercentage` | `0` — otherwise the platform invites AI personas onto this panel up to the default 50% |
| `tags` | omit entirely |

Invite with `tribeunal_invite_jurors`, and send people the share link the case answers with.

### A link poll

Opinion from people who have no accounts — a Discord, a mailing list.

| Setting | Value |
| --- | --- |
| `visibility` | `private` |
| `juryType` | `public` |
| `allowsGuestVotes` | `true` |
| `jurorCount` | leave room — this is reach, not a panel |

Unlisted everywhere, votable by anyone holding the link. `juryType` is stated because this is the one
place the rest of this skill misleads you: private normally means an invited jury, and a link poll is
the exception that requires a public one. Leaving it out works only because the server derives it from
the visibility and the guest flag.

### A community case

Open to the platform, found by browsing. This is the one where `tags` belong: real people filter by
them.

| Setting | Value |
| --- | --- |
| `visibility` | `public` |
| `juryType` | `public` |
| `tags` | the ones people browse by |

Cases are **private by default**, with an invited jury. A community case has to say `public`; leave
`visibility` out and nobody browsing the platform will ever see it.

## The two settings that kill a case silently

Neither raises an error. Both were caught in baseline testing, on transcripts that otherwise looked
perfect.

**`jurorCount` is not a target, it is a gate.** It defaults to twelve. On a case held for jury
selection, voting does not start until that many jurors have joined — so a private case for three
people, left at the default, waits forever while reporting itself healthy. Set it to the number of
people who will actually take a seat.

**`tags` gate who may vote.** A tagged case requires a matching tag or one of a voter's daily free
votes. Attach tags to a case you need a decision from and it can sit at zero votes indefinitely,
looking exactly like a case nobody has got to yet. Tags are for discovery by humans browsing the
platform. Leave them off anything you need an answer from.

## Fixing a case after creation

The structural settings above — jury size, deadline, visibility, jury type — are fixed at creation;
there is no tool that changes them afterwards. `tribeunal_update_case` can only change `title` and
`description`, and only while the case is still `jury_selection` or `open`: once anyone has ever cast
a vote, even one since revoked, the title locks (409 `title_locked`) though the description stays
editable. Get the framing right before you create it.

Made the case by mistake? `tribeunal_delete_case` removes it, but only before any vote has ever been
cast and only for the owner or an admin — otherwise it refuses with 409 `case_in_use`. A case with a
vote on it, or one that already closed, is not deletable; use `tribeunal_close_case` instead and let
it produce a verdict.

## Gotchas

| Trap | What is true |
| --- | --- |
| `caseLength` is minutes | It is seconds. A "30" is half a minute, not half an hour |
| The create response contains the verdict | It does not. See `acting-on-verdicts` |
| A private case's URL is shareable | It sends outsiders to a login wall, then denies them; send the share link |
| Leaving `visibility` out makes a public case | It makes a private one with an invited jury. Say `public` when people should find it; a `juryType` of `public` alone also makes a public case |
| `minVotes` defaults to a real quorum | It defaults to none, so one vote can carry a case. Set it when turnout matters |
| Setting a decision requirement guarantees one | Missing it voids the case instead of deciding it |
| A typo'd title can be fixed any time | Only until the first vote; after that `update_case` refuses with `title_locked` |
| A wrong case can always be deleted | Only before any vote; once one lands, `delete_case` refuses `case_in_use` — close it instead |

## Then what

Seed context as comments before jurors arrive if the case needs background. Once it is running, the
outcome is `acting-on-verdicts`. If the case is a dispute someone outside will have to rely on, stop
and use `arbitrating-a-dispute` instead — it changes several of these settings.
