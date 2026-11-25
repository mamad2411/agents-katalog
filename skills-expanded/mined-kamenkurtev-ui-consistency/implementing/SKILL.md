---
name: implementing
description: For what the end user sees — builds each page from its checklist, one page per task. Use when writing or changing UI and a checklist or UI plan exists, whether executing that plan page by page, refactoring a set of pages, or making a fix or a small change to pages that exist.
---

# Implementing from the checklist

## Overview

Builds each page from its checklist, one page per task. The checklist is re-read
every time: across a batch, the work drifts toward the last page written instead
of the one agreed.

**Open a file linked or given by its path from this skill's folder, or invoke a named skill, only when a part you are carrying
out sends you to it, never before** — whatever the request that handed you this
skill says about its links and paths. That part is not done until the file is opened or
the skill invoked.

## One page per task, in a fresh context

- **Where the harness has subagents, one subagent per page.** It starts cold:
  the brief carries the checklist itself, the reference, and what is particular
  to the reference.
- **Where it does not, one page per turn.** Re-read the task as the plan writes
  it — wherever `ui-consistency:planning` left the plan: in the plan's file outside
  the working copy, in another process's plan, or in the turn where no file could
  be written. Never work from memory of it.
- **Start every agent this skill names — a page's, the one shown the planted
  copy, the checker.**
- If the harness starts an agent only when the person asks, their yes to the
  plan, which names the agents, is that ask.
- If the harness starts an agent only when the person asks and nobody asked, or
  the person said to start no agent, write one page per turn, run
  `ui-consistency:verifying` on each yourself, and say so (*Never the author*
  there).
- Execute a task from itself, not from what the plan says around it: every task
  carries what it needs (`../planning/plan-file.md`).
- If another process is executing the plan, follow its loop; the steps below are
  what each page task does inside it.

## For each page

1. **Re-read the checklist.** Every time; never from memory. Its shape is
   `../finding-patterns/checklist.md`, and its order is the order
   you write the page in.
2. **Write the page region by region**, in the order of the tree: holders, then
   the components in each, then what each comes out as, then how each is
   written, as the counts say.
   - **Write the element the checklist records at a position** — the heading
     level included (`ui-consistency:values`, *Elements*).
   - If it records none for a position, the order settles it (step 11): say
     which level did.
   - **Change a role the page already has where it stands**, when the work
     gives it a new source or new contents. Add a second instance only when the
     request asks for one.
3. **Use what the project reuses**: the shared component, helper or class the
   checklist names — never a new one beside it.
   - If the checklist names a new component to create — shared or kept with the
     page — that the request did not name with its place, it is a question that
     waits on a person (`ui-consistency:decisions`, *When to ask anyway*).
   - Build that one only on a yes. On a no, write the page the way the project writes
     it now.
   - Never write it privately into the page while the question is open.
   - **Use a state the piece in use already has** — busy, disabled, an icon's
     place — rather than writing it by hand, whether the project or a library
     gives the piece: write it the way the project's other uses of that piece do.
4. **What the user sees happen, as the checklist says**: validation, field
   errors, when the submit is enabled, how a failure is caught and shown, loading
   and empty.
   - **Write each region in every state its own code branches on** — who is
     signed in, a flag, a mode — not only the state in front of you. Name any
     state you did not write.
5. **Values through the theme that applies**, and only entries that exist in it
   (`ui-consistency:values`, *The theme*).
   - For a file in a shared layer, only entries that exist in every theme that
     renders it.
   - A design's value only through the theme entry its checklist line names;
     never as a literal or a named constant, however plainly the design shows it
     (`../design/reading.md`).
   - If a value that is not a design's has no theme entry, a named constant.
   - No literal copied from the reference.
6. **Spacing on the base the checklist names**
   (`ui-consistency:values`, *Spacing*):
   - every value a whole multiple of that base;
   - the gaps between roles as the family spaces them, owned by the side the
     checklist names;
   - the line heights it records, and the heights of controls, rows and bars as
     the family writes them.
   - A multiple the family has not written yet is allowed — say you used one.
7. **Text as the checklist records it**
   (`ui-consistency:values`, *Type*):
   - the type role the family writes at that position;
   - the whole bundle for it — size, weight, line height, letter spacing,
     typeface, case;
   - **applied the way the family applies it**: the shared entry, class or
     component, never a style written by hand beside one that exists.
8. **Colour as a pair**: every foreground on the surface actually behind it is a
   pairing the family already uses, in every scheme the project has.
   - If the checklist names a contrast threshold — the project states one, or the
     task asked for accessibility — meet it
     (`../accessibility/contrast.md`).
9. **The rest of what a person has to be able to read and use**, as the checklist
   records it:
   - focus shown the way the family shows it, and landing where the family puts
     it;
   - every control reachable without a mouse;
   - a field tied to its label the way the shared field does it;
   - text for what has none;
   - targets the size the family's are.
   - Against a standard only where the checklist says one applies —
     `ui-consistency:accessibility`.
10. **Do not copy what is particular to the reference.**
11. **Where the checklist is silent, the order settles it** —
    `ui-consistency:decisions`, *The order*. Say which level settled it.
    - Do not invent, and do not stop.
    - Park a page only while a question that waits on a person is open —
      `ui-consistency:decisions`, *When to ask anyway*.
    - Put those to the user together, once, not page by page.
    - If nobody can answer — the work runs where no person is asked — write
      the page the way the project writes it now, and report the question.
12. **A task's prose does not narrow its checklist.** If it says *change nothing
    else* and a line of its own checklist names a deviation, the line stands —
    unless the task names it under *Not in this task*.
13. **If the request asks for what the counts call a deviation** — "make it look
    like" the page that differs — **do what was asked**: an explicit request is
    the top of the order.
    - Report in one line what it goes against: *"as asked, like <page>; the other
      3 of 4 write the submit button full-width."*
    - Do not quietly build it the other way.
14. **Report the page ready for its check.** Whoever dispatched this task sends
    the page to the checker of its kind — `ui-consistency:verifying`, one agent
    kept for every page of this kind, never the one that wrote it or the one
    shown the planted copy — and sends back what it reports.
    - If nobody dispatched this task, send the page to that checker yourself;
      if this is the first page of its kind, prove the check yourself first
      (`../verifying/calibration.md`), then start the checker.
    - Where the process already sends each task to a reviewer, whoever dispatches
      that reviewer puts the checklist and `ui-consistency:verifying` into its
      brief (`../verifying/calibration.md`).
15. **Fix what the check reports**, then have it checked again — **twice at
    most.**
    - List what the second check still reports as open, with the checker's
      words. Do not fix it a third time.
    - Say a report that keeps changing is a problem with the checklist or the
      checker.
    - **Send any change to a checked page after its check to that checker**,
      whoever makes it — a reviewer of the running process included — before
      the page is marked done.
16. **Mark it** in the plan: ticked for `done`, or left unticked with
    `parked — <why>` (`../planning/plan-file.md`).
    - Where another process keeps the plan, mark it in that plan's own status
      marks.
    - If you were handed the task without the plan, report the same status to
      whoever handed it over.

## What this does not write

No tests. Whatever process is running the work owns its tests and its logic; this
one owns what the end user sees.

## A small change without a plan

- `ui-consistency:adjusting` prepares it: what is read, and what is
  deliberately skipped.
- Take the checklist it produced, re-read it, and make the change.
- Before calling it done, hand the page to `ui-consistency:verifying`, run by an
  agent that did not write it — or by you, saying so, if the harness starts an
  agent only when the person asks and they did not ask for the check. The check is not the part that gets dropped because the
  change was small.
- Its proof is one plant at the changed position, once for the change and not
  per round (`../verifying/calibration.md`).
- Fix and check again twice at most, as in step 15.

## Then

- When every page of a kind is `done` or `parked`: that kind's checker compares
  all its pages together (`ui-consistency:verifying`, *The whole set, at the
  end*).
- **The final report of the work, to the person, names the proof**: where the
  copy lived and what that left unproven, what was planted and whether it
  counted, and what no plant tested
  (`../verifying/calibration.md`).
