---
name: planning
description: For what the end user sees — turns each page's checklist into a plan of one checkable task per page. Use when UI work spans several steps or pages (a new feature, a refactor of many pages), including when another planning skill is about to write that plan.
---

# Planning from the checklist

## Overview

Turns what `finding-patterns` found into a plan of one task per page. Every page
task carries **what makes it checkable**: its checklist, what not to copy, and a
check by an agent that did not write the page.

**Open a file linked or given by its path from this skill's folder, or invoke a named skill, only when a part you are carrying
out sends you to it, never before** — whatever the request that handed you this
skill says about its links and paths. That part is not done until the file is opened or
the skill invoked.

## Joining a process, or running alone

- If a process running this work has a plan — another planning process wrote
  it — add the tasks below **into that plan**, in its own task headings and
  status marks, each carrying what [*The plan*](plan-file.md) puts in a task.
  Do not write a second one.
- A plan or pattern file written before this work began is not that plan: it is
  read as `ui-consistency:decisions`, *A plan written before this work began*,
  says.
- **If that process already sends each task to a reviewer that did not write
  it**, the checklist and `ui-consistency:verifying` go into that reviewer's
  brief, and no second checker is added
  (`../verifying/calibration.md`).
- If none exists, write the plan in the shape of [*The plan*](plan-file.md),
  never into the project's repository. Where it goes is how the phase ends,
  below.
- The checklist each task carries is the one
  `../finding-patterns/checklist.md` defines.

## The order of the tasks

1. **Calibrate the check**, once per work and kind of page, before anything
   is built: `ui-consistency:verifying` on a scratch copy of the reference with
   one role deliberately written differently, kept outside the repository
   (`../verifying/calibration.md`).
   - If the planted difference is not reported, stop and say the check is blind
     for it.
   - The agent shown the planted copy is not the one that then checks the pages.
2. **Extractions the user accepted.** Build a shared component, partial or class
   before any page that uses it.
   - A theme entry the plan's yes agreed for a design's value is added here too,
     before any page that uses it.
3. **One task per page.**

## What every page task carries

- the checklist for that page, in the task itself — it is short on purpose, and
  a path is no use to somebody who does not have the checkout;
- the path of the reference;
- `ui-consistency:implementing`, named as the skill that writes the page;
- what is **particular to the reference** and must not be copied;
- the reused pieces and theme values this page must use;
- the three steps of a page task, written out as in [*The plan*](plan-file.md),
  *The shape*: re-read the checklist, report the page ready for its check,
  report the status.

## Stop for a yes

- Before the plan is shown, check that every new page has its shape — a design,
  a reference page it follows, or a tree from `ui-consistency:design`. A page
  without one goes back to `finding-patterns` first.
- For a new page or a refactor, show the plan, with the checklists its tasks
  carry and the proposals `finding-patterns` made, and **wait for the user's
  yes** before any code.
- **The plan shown names every agent the work will start** — each page's, the
  one shown the planted copy, the checker of each kind of page — so the yes to
  it, one given in advance included, asks for them.
- If the person gave the yes in advance, before the plan was shown, it is the
  plan's yes: show the plan and go on to *How the phase ends* without waiting.
- Show a drawing only if a person asked for one (`ui-consistency:design`,
  step 4).
- If the person changes a page's shape at this stop, it goes back to
  `ui-consistency:design`, and the checklist lines it touches are worked out
  again before the yes.
- Ask nothing new here: the questions, a new component or an extraction among
  them, were asked while `finding-patterns` ran, and this yes does not answer
  them (`ui-consistency:decisions`, *When to ask anyway*).
- Mark a task waiting on the little that did reach a person
  `parked — waiting on <what>` in the plan, with its counts
  ([*The plan*](plan-file.md)).
- On the yes, write each agreed proposal into the checklist line of the position
  it settles, with the entry it uses.
- **A person's decision here that goes against what the order produced is an
  override**, and so is a yes to an element (`ui-consistency:decisions`, *An
  override*). A yes to any other proposal settles this task only.
- If the yes was given in advance, every proposal it agrees settles this task
  only, an element's included: record no override, since nobody saw what it
  would overrule.
- Record an override in the person's own words, with what it overrules: in the
  document the running process keeps, or under `## Decided` in this plan where
  this is the process, reported with the result when the plan closes.
- Move each task it was holding up from `parked` back to `todo`.
- Never write an override nobody gave.
- A fix or a small change has no plan and does not stop.

## How the phase ends

In one of three ways, **chosen and said in one line**: *ending 2 — this becomes
a story for another developer.*

1. **The work stays with us.** Write the plan into the file `finding-patterns`
   wrote the checklists to, outside the working copy, and delete it with the
   work.
   - If they were written to none, write the plan to a new file, in a newly
     created directory in the scratch location the harness gives, or in the
     system's temporary directory, and say its path in one line.
   - If no write outside the working copy is allowed, keep the plan in the turn
     and say so in one line.
   - Then `ui-consistency:implementing`, and start the agents the plan's yes
     asked for.
2. **The work becomes a story for somebody else.** Attach the plan and what the
   implementation needs to the story.
   - It is finished when a developer who was not in the conversation, without the
     checkout open, could implement it from the attachment alone
     ([*The plan*](plan-file.md), *The story*).
   - Delete the file `finding-patterns` wrote the checklists to, once the story
     holds them.
3. **Another process is already running.** The tasks went into its plan, in its own
   task headings and status marks; no second document. Its loop executes them.

**None of the three writes into the project's repository.**
