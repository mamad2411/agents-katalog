---
name: review-issues
description: Read every open issue in this repository, group them by theme, and name the best next piece to pick up. For a maintainer deciding what to work on. Reports only; it never edits an issue or applies a label. Load it by its path when you want it.
---

# Review issues

The kit's own `/implement` and `/what-now` read `plan.local.md`, which sorts a
backlog by the labels a project built with the kit uses. This repository uses
its own labels, so that printout drops almost everything into a single heap.
This is the maintainer's read of the same backlog.

It answers one question. Given everything open, what is worth picking up next.

## Read

Ask GitHub directly. `gh issue list --state open --json
number,title,body,labels,url` gives the text and the labels. `gh api
"repos/OWNER/REPO/issues?state=open"` gives two things the first call leaves
out: `sub_issues_summary`, which says whether an issue is a parent and how many
of its parts have closed, and `issue_dependencies_summary`, which says whether
anything open is holding it up.

Read the bodies, not only the titles. A backlog this size is small enough to
read properly, and titles alone will put two unrelated pieces in one theme.

If GitHub cannot be reached, say so and stop. A recommendation drawn from a
list that failed to load is worse than no recommendation.

The two calls must agree on how many pieces are open. An empty list is a valid
answer meaning nothing is open, and it is also what a passing fault looks like.
The second call returned an empty list once while this skill was being tried
out, with thirteen pieces open at the time, and recovered on the next attempt.
So compare the counts, and where they disagree, say the backlog could not be
read and stop. Telling somebody their backlog is empty when it is not is the one
wrong answer that looks like a right one.

### What makes a piece ready

A piece is shaped when its body carries a `## Done when` section, which is a
condition somebody can check. `docs/MAINTAINING.md` owns that shape. The
`ready` label says a person judged it shaped. Those two signals do not always
agree here. Where they disagree, say so rather than quietly picking one, because
a piece labelled ready with nothing checkable in it is usually worth a second
look.

A piece is unshaped when it carries `needs-answers`, or when it has neither a
checkable condition nor the ready label. Never recommend an unshaped
piece as the next thing to build. It can be the next thing to shape, which is a
different recommendation and worth making when little else is ready.

A piece is held up when something open is named in its `blocked_by`, or when it
is one part of a parent whose other parts come first.

### Themes

Work the themes out from what the issues say. Do not read them off the `area:`
labels. Several issues carry no area label at all, so that grouping does not yet
exist, and reading it back would only repeat the gap.

Where a theme you found matches an area label already in use, say so, since that
is a sign the label is doing its job. Where a theme has no label, say that too
and leave it there. Applying a label is somebody's decision, not this read's.

## Say

The answer is a printout with a fixed shape, not an essay. Read what you have
written back against this before you send it:

```
<n> open · <n> themes

WHAT THIS WORK IS ABOUT, IN PLAIN WORDS          #<n> #<n> #<n>
What these pieces have in common, said the way the maintainer would
say it out loud. Then where the theme stands: how many are shaped,
and what holds the rest. Two to four sentences.

THE NEXT THEME, NAMED THE SAME WAY               #<n> #<n>
The same again.

ON ITS OWN                                       #<n>
The same, for the piece no theme fits.

WORTH PICKING UP
  #<n>  the issue title
        Why this one, in a line or two.

SMALL AND SEPARATE
  #<n>  the issue title, and what makes it one small change

NEEDS YOU TO DECIDE
  #<n>  the question only the maintainer can answer
```

A piece appears as its number. That is what the maintainer types next, and a
theme carrying four numbers reads faster than a theme carrying four titles. The
title comes back wherever the printout recommends something, because a
recommendation nobody can recognise is no use. The rule against numbers governs
a tracked file, where the reader cannot follow a pointer and the numbering
shifts underneath it once the material is public. A printout is read once,
beside the backlog it came from. Do not write one into a file.

A heading names what the work is. The test is that the maintainer can read the
heading on its own and say which pieces fall under it. "Reaching beyond the
thirteen" fails that test. It is a phrase that needs the paragraph under it to
decode, and a reader who does not carry the count of skills in their head gets
nothing from it. "Asks for a capability the kit does not have" passes. Say the
plain thing and let the heading run long. A heading that stays cryptic in order
to stay short has kept the wrong thing.

The paragraph under a heading does two jobs, and it is two to four sentences.
First, what the pieces share, in the words somebody would use to say it out
loud. Second, where the theme stands: how many of its pieces are shaped, and
what holds the rest. The second job is what turns a grouping into something the
maintainer can act on. This paragraph has gone wrong in both directions. A read
written against a looser rule ran to three paragraphs a theme and buried the
grouping in the explaining. A read written against a one-line rule produced "a
new agent, a default design plugin, and a hosting companion", which is a list
of nouns, and a list of nouns says neither what the theme is nor what to do
about it.

Where no theme fits a piece, leave it on its own rather than pushing it into the
nearest one. A theme of one is an honest answer. A theme of two unrelated things
is worse than no theme at all.

Order the themes largest first. A count is not a judgement, so ordering by one
ranks nothing.

Worth picking up names one thing, with the reason in ordinary words. The reason
is the useful half. "It is the only shaped piece in the largest theme" tells
somebody something. "It seems important" does not.

The two lists under it hold the work that needs no ranking. Small and separate
is the piece somebody could finish and send on its own, which is what a person
with a spare hour is looking for. Needs you to decide is the piece waiting on an
answer nobody else has. Each list names at most three pieces, because a list of
everything hands the decision straight back to the person who asked for help
making it.

Where nothing is shaped, say that plainly and recommend what to shape first,
rather than dressing unshaped work up as ready.

Where the themes give no honest reason to rank one above another, say that
instead of inventing an order. This repository has not yet written down what
finished enough for 1.0 would mean, so there are backlogs where the truthful
answer is that the choice rests on grounds this read cannot see.

This command reports and changes nothing. It does not edit an issue, apply a
label, link a part to a parent, or open anything. Where the read turns up
something worth changing, such as two pieces covering the same ground, say it
under the printout and leave it with the maintainer.

## Done when

The maintainer can see the backlog grouped by what the work is about, has one
recommended next piece and the reason for it, and can see at a glance which
pieces would go on their own as one small change and which are waiting on an
answer only they can give. Nothing on GitHub has changed.
