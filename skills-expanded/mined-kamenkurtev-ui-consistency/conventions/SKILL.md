---
name: conventions
description: For what the end user sees — counts what a project's pages do, so a convention is told apart from one page's habit. Use when a count of how the other pages write something is about to be recorded, or when a checker recounts a line of a checklist.
---

# Conventions: the kind, the family, the proof, the counts

## Overview

Counts what the project's pages do, in the order of the work: the kind, the
family, the proof that a search can see, then the counts.

**Open a file linked or given by its path from this skill's folder, or invoke a named skill, only when a part you are carrying
out sends you to it, never before** — whatever the request that handed you this
skill says about its links and paths. That part is not done until the file is opened or
the skill invoked.

## Which kind of page this is

Decide it first: it sets every count below it. Take the first signal that
answers:

1. **What the user said** — a kind somebody named, *a list page like the orders
   one*, outranks anything read.
2. **What the project keeps apart** — its folders, routes, file-name suffixes, a
   folder per kind.
3. **What the reference renders** — the same holders and regions in the same
   order make one kind, whatever the subject. A collection of rows and a single
   record with a submit are two.
4. **What the pages reach for** — the same holder, layout piece or shared frame.

Then:

- If a later signal disagrees, or the project does not answer:
  [*When the signals do not settle the kind*](kind-unsettled.md).
- If the trees differ below a shared outer holder:
  [*A family that differs by region*](family-by-region.md).
- **Name the kind in the project's own word** — folder, route, file name — never
  an invented one. If it has none, name it by what it renders, *a list with a
  form above it*, and say the name is yours.
- Say in the checklist's first line the kind, what decided it, and how many
  members of how many candidates were counted
  (`../finding-patterns/checklist.md`).

## The bound the family is counted in

The bound is fixed, not chosen, so two agents reading the same reference count
the same pages.

- **The application that mounts the page** — whatever routes to it or renders it
  from its entry — **and every library it uses.** Not the library the reference
  sits in, not the whole workspace.
- If no application mounts the pages — each page is a document of its own — the
  bound is **every page that loads a file the reference loads too**, such as a
  stylesheet, a script or a tokens file, and those files.
- If no other page loads a file the reference loads, the bound is the pages in
  the reference's folder, its subfolders included.
- If the page sits in a library:
  [*The bound for a page in a library*](library-bound.md).
- **Name the bound in the checklist's first line.** A later phase counts in it,
  or says which other bound it used and why.

## Which pages are the family

The family is the pages of the reference's kind. Take the candidates, and remove
what is not a member **before** counting:

- **What a page imports — its panels, its dialog, its hooks — is part of it**,
  not a sibling: neither end of an import edge among the candidates is a peer of
  the other.
- **A file that imports members is not a member**: a dispatcher, a route table,
  a barrel, a wrapper.
- **A candidate that renders no holder and no region of the kind is not of the
  kind.** Report it so; never count it as a member that lacks them.
- **State both numbers** — candidates considered, members counted — and what was
  left out and why.
- **If the members span more than one area** — app, library or package — **or
  are more than can be read in full**, it is a large project: follow
  [*A large project: split, sample, group*](large-project.md) before counting.
- **If the work creates a shared piece that takes over a choice each page
  made itself** — where a state is kept, which side takes a default share —
  count those choices as
  [*A shared piece the work creates*](new-shared-piece.md) says.

*Why:* a dispatcher counted as a page once turned 8 of 8 on every role into 8 of
9 — a unanimous convention reported as one drifting page.

## Prove the search can see before trusting a count

The reference is one of the pages counted, so every search has a known answer: it
must find what the reference writes.

- **Run each search on the reference first.** One that misses the reference is
  broken, and nothing it counts is a result.
- **A zero for a role the reference writes is a broken search** — a wrong glob, a
  list never split, a pattern that misses this dialect, a bound that resolved to
  nothing. Fix it and count again; never record it.
- **A zero across the whole family is unverified**, not a convention. Record
  *none of them write this* only when the same search, over the same files,
  found something else.

*Why:* a loop run once over the whole list instead of once per file reported
*0 of 9* twelve times, holder included — the opposite of the truth.

## Counting honestly

- **Count per position** — a role where it stands — never per component alone:
  10 of 18 buttons full-width reads as no rule, and was 10 of 10 in the content
  area and 0 of 4 in toolbars.
- **Count *whether* apart from *which way*.** First how many members have the
  role at all; then, over those, which way each writes it. *None* answers
  *whether* and is never a way: *14 of 21 filter; of those 14, 10 through the
  shared toggle and 4 by hand* — not *10, 4 and 7 across three ways*.
- **Count what the component comes out as too**, and the heading level where the
  position is a heading — `ui-consistency:values`, *Elements*.
- **A count carries its file spread.** Four identical buttons in one file are
  one page's habit; 10 of 10 across 8 files is a convention. A page and the files
  only it imports count as one file of the spread; say so where a member spans
  files.
- **A missing prop is not yet a deviation.** The theme or one of the project's
  wrappers may set it already.
- **A value written in a member's classes is not yet what renders.** Before
  counting it, check it against what one member renders, or where no page can
  be opened, against the rules that can override it, searched once for the
  whole family, as `ui-consistency:values`, *Every subject: the same rules*,
  says.
- **Search for the exact name.** A container whose name starts with the
  component's once turned 18 uses into 25.
- **If the task adds a position no member has** — a second control, a control
  nobody has here — or changes a role the page already has, count it as
  [*A position no member has*](position-no-member-has.md) says.
- **A family of one is never a convention.** Write what the page does as the
  reference's own way — never as a count, and never as what the project does —
  and say the family has no other members:
  [*A kind whose family has only the reference*](reference-only.md).

## When a count is not a convention at all

*2 of 8*, written the way every other count is written, reads as a rule. It is
not one.

- **Read it off the numbers themselves** — never a threshold from outside, no
  percentage, no "most".
- **Count every way, not only the commonest**, over the members that have the
  role: *4 of 4*, *3 of 4 and one other way*, *3, 3 and 2 across three ways*. A
  plurality is not a majority.
- **There is a convention only if the commonest way outnumbers the others put
  together** — a majority. Otherwise say the family has none here, and give
  every way with its numbers.
- **Say which kind of majority it is.** One exception is written *7 of 8 except
  `<page>`*. Several different ones make a family drifting: still the majority,
  written *the commonest way, 5 of 8, against three others*.
- **The order still decides**, and nothing stalls or is asked: with no majority,
  the newest members settle it (`ui-consistency:decisions`, level 5). The line
  says *no convention here; the two newest write it this way*.
