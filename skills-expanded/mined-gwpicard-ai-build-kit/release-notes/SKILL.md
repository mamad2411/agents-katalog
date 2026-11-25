---
name: release-notes
description: Write or revise a release's public notes from the changes it carries, to the maintainer's release-notes standard. For a maintainer before the stamp pull request, or when older notes need work. Load it by its path.
---

# Release notes

`references/framework.md` is the standard. Read it in full before you write.
It says how to establish each change from the evidence, which fourteen writing
problems to look for, how severe each one is, and when a note is acceptable.

## The reader

A person who builds internal tools with a coding agent and the kit. They may not
read code, but they are a capable professional. Write to an experienced
technical writer's standard: natural, precise and accessible. Use an established
word, such as confirmation, approval, configuration or branch protection, where
it is the right word. Keep a command, setting or check name where the reader
types it or sees it.

## Fixed constraints

These override the framework where the two conflict.

1. British spelling, no contractions, no em or en dashes.
2. No pull request or issue numbers, and no links to them. No cost or price
   figures. No attribution lines.
3. Keep every action an existing user must take. Give each command and each
   line to type word for word.
4. Add no fact the evidence does not support. Where the evidence cannot settle a
   meaning, ask the maintainer rather than guess.

## Evidence

For a new release, read the merged pull requests since the last tag: their
descriptions, their diffs and their tests. For an older release, read the
repository at its tag, `git log <previous-tag>..<tag>` and the merge commits,
which carry the pull request descriptions. A commit title alone is not enough.

## Shape

Write the version's file in `docs/release-notes/`, in this order:

1. One sentence on what the release does for the reader.
2. Who gets each change, where that is not every project. Say it early: an
   existing user who expects a change and does not get it will think the
   update failed.
3. `## Updating`: the command, whether to start a new session, any action the
   person must take, and whether their data changes.
4. `## What changes`: a numbered list, most important first. Each item has a
   short bold name, what changed and, where the evidence supports it, why it
   matters.
5. A short section on what was tested and what is not proven yet, where there is
   something real to say. Leave out conditions that exist only on the
   maintainer's computer.

When the notes are edited on the Release's web page, the drafted pull request
titles go under `## Pull requests in this release`, each rewritten to the same
standard.

## Steps

Do them in this order. The writing rules live in three places, and a step
skipped between them goes unnoticed until the notes are public.

1. Before drafting, delete the previous release's notes file so
   `docs/release-notes/` holds at most one versioned notes file. Then write the
   new file from the evidence, in the shape above.
2. Load `.agents/maintainer-skills/writing-review/SKILL.md` and run its
   embedded mode over the file.
3. Check the file against the house rules in `docs/MAINTAINING.md`: paragraph
   length, verbs that match what a check does, banned words, sentence shape.
4. Write the full text for the Release's page to
   `.agents/tmp/release-notes-review/<version>/page.md`: the file, then
   `## Pull requests in this release` with each drafted title rewritten.
5. Give `page.md` to one fresh reviewer with this skill and the evidence. Ask
   for findings by the framework's severity levels, each claim checked against
   the evidence, and a last line such as `Critical: 0 | Major: 0 | Minor: 1`.
   Save its reply as `review.md` beside `page.md`.
6. Fix each Critical and Major finding, rebuild `page.md`, and repeat step 5
   with another fresh reviewer until it reports none.
7. Run `.agents/tools/check-release-notes.py <version>`. `stamp-version.sh`
   runs it too and refuses to stamp until it passes.

## Done when

Every claim traces to the evidence, every required user action is present word
for word, the writing-review and house-rule passes are done, and the latest fresh
review of the final page text reports no Critical or Major finding.
