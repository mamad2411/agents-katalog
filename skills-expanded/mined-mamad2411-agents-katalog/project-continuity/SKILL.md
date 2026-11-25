---
name: project-continuity
description: Leaves the project in a state another engineer or agent can resume: what was completed, what works now, decisions taken, concrete remaining work, known risks, verification performed and integration context, with no secrets. Use at the end of any session that changed the repository.
license: MIT
metadata:
  category: dev-skills
  version: 1.0.0
  depends_on: [engineering-core]
  outputs: [continuity-notes, handoff-report, follow-up-list]
---

# Project Continuity

The next person to open this repository should not have to reconstruct what
happened. That person is frequently the same agent, in a session with no
memory of this one.

Continuity is written at the end of every session that changed anything, and
it is short.

## 1. The seven sections

```
Completed      what was actually implemented, with paths
Current state  what works now, and what is knowingly incomplete
Decisions      choices taken, with the reason and the rejected option
Remaining      concrete unfinished work, each item actionable
Risks          known issues, limitations and their trigger conditions
Verification   what was run, and what it returned
Context        integration details and constraints a newcomer cannot deduce
```

Every section is present, even when its content is one line. An absent section
reads as forgotten, not as empty.

## 2. What belongs in each

**Completed.** Facts, with file paths. Not intentions.

```
Good  Added POST /api/teams/:id/invitations, app/api/teams/[id]/invitations/route.ts
Bad   Worked on the invitation feature
```

**Current state.** What a user can do today, and what looks finished but is
not. This is the section that prevents the next engineer from demonstrating a
half built path to a stakeholder.

**Decisions.** Only the ones that were expensive to reach or that look wrong
without their context. A decision without its rejected alternative will be
reversed by the next person who has the same idea.

**Remaining.** Each item is a task someone could start: what, where, and the
first step. `Improve error handling` is not an item. `Add a timeout to the
mail client in lib/mail.ts, currently unbounded` is.

**Risks.** What could break, under what condition, and how it would present.
Includes limits that are fine today with the volume that would change that.

**Verification.** Commands and results. This is what tells the next engineer
which claims are proven and which are assumed.

**Context.** What the repository does not say: which provider account is used,
why an unusual approach exists, what a partner system expects, what a previous
attempt failed at.

## 3. Never recorded

```
passwords, tokens, API keys, private keys, connection strings
session identifiers, cookies
personal data beyond what the work requires
internal credentials of any third party
the contents of a .env file, even partially
```

A continuity note is a tracked file. Everything in `engineering-core`
section 5 applies to it.

Reference secrets by name and location, never by value:

```
Good  STRIPE_WEBHOOK_SECRET must be set in the deployment environment
Bad   STRIPE_WEBHOOK_SECRET=whsec_...
```

## 4. Where it lives

Follow the project. In order of preference:

1. the file the project already uses for this;
2. a decision record or documentation directory, when the content is durable;
3. a pull request description, for work that will merge shortly;
4. a `CONTINUITY.md` or equivalent at the root, when nothing else exists and
   the work spans sessions.

Do not create a new convention when one exists. Do not create a file for a
session that finished cleanly and left nothing open, beyond what the commits
and the documentation already say.

## 5. Length

One screen for a normal session. Two for a large one.

Continuity notes that grow without bound stop being read, which defeats their
purpose. Completed work older than the current effort is deleted, not
archived in place: the git history already holds it.

## 6. Protocol

1. List what changed, from the commits of this session.
2. Fill the seven sections.
3. Convert every vague statement into a concrete one.
4. Remove any secret or personal data.
5. Delete stale entries that this session resolved.
6. Verify that a reader with no context could resume from it.
7. Commit as `docs:`, or include it in the pull request description.

## 7. The resumption test

Read the note as if arriving with no memory. Answerable without opening
anything else:

```
What state is the work in
What can I run to see it
What is definitely finished
What is definitely not
What should I do next
What will surprise me
```

A note that fails any of these questions is rewritten before it is committed.

## 8. Auto-critique

Score from 0 to 5: all seven sections present, concreteness of the remaining
items, decisions carry their rejected alternatives, verification quotes real
results, no secret, stale content removed, passes the resumption test, length
under control.

Threshold: no axis below 3, average at least 4. A secret in the note is an
automatic failure and requires rotation, not only deletion.

## 9. Interfaces

- Upstream: every skill in the suite.
- Downstream: the next session, `release-readiness`, `git-workflow`.
- Related: `technical-documentation` for durable documentation, which is a
  different artefact with a different lifetime.
