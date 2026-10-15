---
name: pr-discipline
description: >-
  Shape a change so it can actually be reviewed, not just merged. Decide before writing code whether the work is one pull request or a stack of them, keep the title and body describing the diff as it exists right now, not the plan you started with, group commits by concern in dependency order, give every review comment an explicit disposition, and only call a change ready after re-checking the real state of checks and threads instead of trusting that a push or a reply worked. Use this whenever a change is being opened, split, described, updated, or readied as a pull request or merge request, including deciding how many PRs a piece of work needs, planning or syncing a stack of dependent branches, writing or refreshing a PR description, shaping commit history before requesting review, triaging review feedback, or judging whether a PR is actually mergeable. Reach for it any time work is about to leave a branch and become something someone else has to read.
---

# PR discipline

A pull request is not the code. It is the unit a reviewer has to hold in their head while deciding whether to trust it. A diff can be entirely correct and still fail at that job: too large to review in one sitting, described by a story the diff no longer tells, or claimed ready when a check is still red. This is a working rule about the container, not the contents, alongside [no-scripted-editing](../no-scripted-editing/SKILL.md): how a change gets shaped so review actually works, independent of whether the code inside it is any good.

## The shape of a mergeable change

Decide how many pull requests a piece of work needs before writing any of it. A change that mixes concerns a reviewer would naturally judge by different standards, schema against UI, backend against frontend, a mechanical rename against a behavior change, asks one reviewer to hold two mental models at once, and asks review to happen at the lower of the two bars.

When a change does not fit in one reviewable diff, stack it: an ordered chain of branches, each based on the one before, each carrying exactly one concern, each reviewable on its own. Foundational work goes at the bottom; whatever depends on it goes above. Plan the layers before writing code. Restructuring a stack after the fact costs more than starting split, since there is rarely a clean in-place reorder once commits already exist on the wrong branch.

A stack should read as one coherent story: a reviewer walking it bottom to top watches the feature get built. Unrelated work, a different feature, an incidental fix that has grown past incidental, gets its own stack rather than riding along because it happened at the same time.

## The description matches the diff, not the intent

Write the title and body from everything the change currently does, not from the first commit or the plan it started as. A description is a claim about the diff, and the moment the two diverge, the reviewer is reviewing the wrong thing without knowing it.

Refreshing a description is not rewriting it from scratch. Anything a person added to it, a screenshot, a linked discussion, context that only ever existed in someone's head, survives the refresh untouched. Rewrite the prose around it, never over it.

An oversized, hard-to-follow diff does not get fixed by writing a longer description or annotating the risky parts. Notes can guide a reviewer through a diff that is already reviewable; they cannot make an unreviewable one reviewable. When the honest fix is splitting the change, say so instead of writing around the problem.

## Shape the commits, not just the final diff

A commit history is part of what gets reviewed, not an implementation detail behind the diff. Group commits by concern in dependency order: schema and generated definitions, then core logic, then wiring, then surface behavior, then tests. A reviewer follows a change that grows outward in that order instead of reconstructing one from an arbitrary save history. [commit-discipline](../commit-discipline/SKILL.md) covers what each of those commit messages should say; this section only covers where the boundaries between them go.

Polish before shaping. Clean the diff first, cut dead code, debug logging, anything that will not ship, and only then split it into commits. Committing first and cleaning after means the commit boundaries describe code that has since been thrown away, and the history stops being a reliable account of what happened.

## Every review comment gets a disposition

A thread left neither answered nor resolved is not neutral; it reads as ignored. Give each one an explicit outcome. Valid: fix it and resolve the thread. Wrong or based on stale code: say why and resolve it. A real nit outside the current scope: ask once rather than deciding unilaterally in either direction.

Weight matters. A comment from whoever owns the area, or whoever is blocking the merge, does not get resolved by going quiet on it. It gets a fix, or an explicit, visible reason it will not be addressed. Silence is not a rebuttal.

## Ready means re-checked, not remembered

Passing checks and resolved threads are states of the world, not states of memory. A push does not confirm CI turned green. A reply does not confirm a thread resolved. Before calling a change ready, re-query both rather than trusting that the action taken had the intended effect. Fail closed: one red check or one open thread that cannot be accounted for means the answer is still no.

Clearing a change to mergeable is a narrow job. Fix what the base change or the review actually broke, and leave unrelated improvements for their own change, however tempting they look on the way past.

## Keep a stack honest

When a lower layer changes, the fix belongs on the branch that owns that concern, and everything above it gets rebased onto the change. Merging the trunk into the top branch instead is not a substitute: it resolves the immediate conflict while leaving every PR in the stack diffed against a base it no longer matches, which quietly undoes the reason the stack was split in the first place.

Sync bottom-up, in the stack's own order, the same way it was designed. The change ripples upward through each layer once, rather than getting patched independently into whichever branches happen to conflict first.

## When one PR is the right call

Not everything benefits from splitting. A change that is genuinely small, a fix that cannot wait behind a multi-layer review, or work too tightly coupled to divide without producing a layer that fails to build on its own, is one PR. Forcing a stack onto it adds process without adding reviewability. The test is the same one that justifies splitting in the first place: would a reviewer actually judge these concerns by different standards, or is the split just ceremony.

## Using this well

**Splitting has a cost too.** A five-layer stack for a change a reviewer would have understood in one pass trades one failure mode for another, scattering review across five contexts instead of concentrating it in one dense one. Split until concerns stop being reviewable at different standards, not further.

**A stale description is a worse failure than no description**, because it actively misleads instead of leaving a gap the reviewer knows to fill themselves.

**Fail-closed done-conditions feel slow and are not optional.** The entire value of re-checking rather than remembering is catching the case where the push failed silently or the check lagged behind, the case that only shows up once in twenty times and is exactly the one worth catching.

**None of this substitutes for the change being right.** A well-shaped PR around the wrong fix is still the wrong fix, reviewed efficiently. This is the container; [think-like-a-staff-engineer](../think-like-a-staff-engineer/SKILL.md) and [think-like-a-design-engineer](../think-like-a-design-engineer/SKILL.md) judge the contents.
