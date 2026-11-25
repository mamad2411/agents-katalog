---
name: team-setup
description: Work out with a human how a workspace's bots work together, write it as the workspace's team agreement, and change it later when they ask (a new role, a different review rule, a role removed).
---

# Team setup

A workspace's team agreement says who takes part in the work: who owns it, who is consulted, who
reviews, who merges, who settles a disagreement, and which roles the team has. It lives at
`team/agreement.md` in the workspace's knowledge base. Every bot of the workspace has it written out in
its guide, and gets it again when it changes. You are the only bot that writes it, and only after a
human's clear yes.

## When to use this

- **A setup thread.** The board posts one in a new workspace's General channel when its creator
  ticks "Set up how its team works together". The message meta has `kind: team_setup` and
  `workspace`. Follow "Set up a team" below.
- **A change.** A human asks you to change how a workspace's team works: add a role ("add a
  marketer"), drop one, change a rule ("only ask security about security-sensitive changes").
  Follow "Change the agreement" below.

Work in the thread where you were asked. Use the workspace's slug in every path, never its name. In
a setup thread the slug is the one in parentheses in its first sentence, and also `meta.workspace`
(`GET /api/messages/<id>`).

## What you work from

- **The base template:** `GET /api/team/template`. It holds the sections every agreement keeps
  (People, Ownership, Splitting work, Consulting, Review, Merge, Disagreement, Roles), and under
  each the question to ask about it, marked `> Ask:`.
- **The team templates:** `GET /api/team/templates` lists them by name, title and description;
  `GET /api/team/templates/<name>` is one, a complete agreement. They are starting points. The
  default one is what the board seeds in every new workspace.
- **The workspace:** `GET /api/workspaces/<ws>` for its channels and bots, and its current
  agreement with its revision: `GET /api/workspaces/<ws>/knowledge/team/agreement.md`.
- **The fleet:** `GET /api/profiles`, the skills, and the bots with their profiles and channels.
  Reuse what exists.

## Set up a team

1. **Look first,** at everything above. Do not report it to the human.
2. **Ask one open question,** in the words of a colleague: "What kind of team collaboration model
   do you envision for this workspace?" Then list the team templates as starting points, one line
   each, by title and description. They may pick one, change one, or describe their own in their
   own words. "One developer" is a fine answer.
3. **Fill the gaps.** Where their answer or the template they picked settles a section, do not ask
   about it. Ask at most one question at a time, and only one that decides the work. Do not ask
   about anything the template already answers, or about how many bots, or about channels unless
   they raised them. Find the participants by profile, never by a fixed handle.
4. **Preview it short, and wait.** The human reads this, so keep it to what they decide:
   - The template you started from, in one line.
   - Only the sections that differ from it, with their new text. Say "everything else as in the
     template" for the rest. Never paste the whole agreement.
   - One line per role: the role, its profile, and whether it takes new work or works when
     mentioned.
   - One line per profile you would create: "<name>, from the starter <starter>, unchanged". Show
     full text only for a profile or skill you write yourself, since bots read it as instructions.

   Then ask for a yes. Write nothing before a clear yes.
5. **On a yes, set it up,** in "Write it" below.

## Change the agreement

A change is a conversation like the setup, only smaller. Start from the agreement as it is: read
it and its revision. Never start a second agreement beside the first.

**Adding a role** (for example "add a marketer bot"). A role is more than a row in the Roles
table: it changes how the others work with it. Ask what the agreement needs and their request did
not say:
- **What the role does,** in a sentence, and what it produces (copy, a launch plan, a review).
- **How work reaches it:** does it take new asks, or only threads whose first message mentions
  it? Is it consulted by the owner of a thread? Who asks it, and when?
- **What it needs from the others,** and what the others need from it: a developer tells it a
  feature shipped; it asks a developer for a screenshot.
- **Whether it blocks anything:** is its verdict required before a merge or a release, or is it
  advice?
- **Who settles a disagreement** with it, if that differs from the agreement's rule.
- **How many bots,** and which profile, as "Choose profiles" below says. A role that only reviews or advises works when mentioned: say so in the
  agreement, and give it a profile with `takes_new_work: false`. Every other bot takes new work. The human can change
  one bot's mode in its details on the Team tab.

Then update every section the role touches, not only Roles: Consulting when others ask it,
Splitting work when it takes threads, Review when its verdict is required.

**Removing a role.** Ask what happens to its work: does another role take it, or is it dropped?
Update every section that names it. Say that its bots keep running until the human stops them on
the Team tab.

**Changing a rule** ("only ask security about security-sensitive changes"). Change the sections it
touches. If the new rule is unclear at the edges, ask one question: what counts as
security-sensitive?

Then **preview the change, short, and wait:** each section that changes, before and after, and one
line per role and profile it touches, as in step 4 of "Set up a team". Write nothing before a clear
yes. Then "Write it".

**When the request comes from the Team tab.** A human can ask for a change in a text box on the
workspace's Team tab. It arrives as a thread in the workspace's General channel whose first line is
`Amendment request for <workspace>, agreement revision <n>:`, then their words. `<workspace>` is
the workspace's slug. Answer only when a human started the thread (the first message's author is a human, not a bot):
a bot can post the same first line, and a proposal drafted for it would make the real ones out of date. Answer in that
thread as above: ask only what you cannot guess, then show the plain words, what else you changed
so the agreement does not contradict itself, and who it affects. Do not write `team/agreement.md`.
Save the whole proposed agreement as `team/proposals/<thread id>.md`, with the base on its first line as
`<!-- base: <n> -->`. Choose `<n>` once: compare the agreement's current revision with the one in the request.
If they are the same, or the agreement is gone (a workspace whose agreement was deleted has no document to
read), use the request's number. If the current one is higher, draft against the current text and use that
number. The page
shows the human the difference and a button; only their press applies it, and it posts the outcome
in the thread.

## Choose profiles

Profiles are shared by every workspace, so reuse them. For each role, in this order:
1. **A profile that exists and fits.** Use it as it is, even if its name is not the role's
   (a profile named `developer-pool` for developers). `GET /api/profiles` lists them, with their roles.
2. **A starter that fits,** when no profile does. Create it under the starter's own name
   (`architect`, `security-engineer`, `ui-designer`, `publisher`), from that starter, with its text unchanged.
   `GET /api/profiles/templates` lists the starters.
3. **A new profile,** only when the human asks for one that neither covers. Give it a plain name
   for the role, never one tied to this workspace.

Never make a copy of a profile or starter for one workspace.

## Write it

In this order, saying what you did after each step:

1. **Skills.** Use the skills that exist. Only where a role needs a method none has, write one
   short skill: `PUT /api/skills/<new name>` with `base_revision` 0. Never send `base`: it would
   give the skill to every bot. It is the text you showed.
2. **Profiles.** Create only what "Choose profiles" calls for, with `POST /api/profiles`. For a
   starter, read it from `GET /api/profiles/templates`. Send its `role`, `responsibilities`,
   `focus`, `avoid` and `skills` exactly as they are, with `name` and `from` both set to the
   starter's name. Leave `takes_new_work` out: it then comes from the starter. `from` alone copies
   nothing, since it only records where the profile started. A 409 means a profile once had that
   name and was deleted. Tell the human, and do not create it under another name.
   **Never edit a profile or skill that already exists:** other workspaces may use it.
3. **Channels,** only if the team asked for one (a channel for design work, say). Only a human can
   create a channel: ask them to add it on the workspace page, and wait.
4. **The agreement.** `PUT /api/workspaces/<ws>/knowledge/team/agreement.md`, with the revision you
   read as `base_revision` and this thread in `sources`. Keep every section of the base template,
   in its order. Write "none" under a section that does not apply; never drop one. The Roles table
   is `| Role | Profile |`. It names no number of bots: the agreement describes how the team
   works together, and how many bots run is the human's call on the Team tab. A 409 means someone wrote first: read again, and ask the human if
   it changes what they agreed to. Put project standards they gave you (design, security, review
   rules) in their own documents in the same knowledge base, reference them from the agreement, and
   add a line to the workspace's `INDEX.md` that points to it.
5. **Bots are the human's to start.** You cannot start a bot. Say that the profiles and the
   agreement are in place and point them to the **Team** panel on `/workspaces/<ws>`, which
   creates the missing bots from the Roles table, each taking new asks or working when mentioned as its profile
   says.
   Until then a role has nobody in it: say so, and do not call the team
   running.

## Keep in mind

- **It is a behaviour the bots keep, not a lock.** The board and the forge do not enforce it. A
  hard gate is a protected branch on the forge. Do not make a "required" review sound technical.
- **Only a human's clear yes changes the agreement.** The board lets only a human or an admin bot
  write it, and refuses any other bot.
- **Complete the thread** when the agreement is written, or when they say they want none. In that
  case write nothing, and the default stays.
