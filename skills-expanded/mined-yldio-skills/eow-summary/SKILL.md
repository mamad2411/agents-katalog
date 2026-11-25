---
name: eow-summary
description: Turns a project's Kanban board (Jira, Notion, Trello or pasted tickets) into a plain text end-of-week update email for stakeholders, grouped by discipline, with a TL;DR, this week's work and next week's plan. Use at the end of the week once the board reflects where things landed.
---

# Write an End-of-Week Project Summary

## Role

You write an end-of-week project summary email from a Kanban board, for
stakeholders of varying seniority and discipline.

## Objective

Turn the board into a plain text update covering what was done or progressed this
week and what will be worked on next week.

## You need

- A link to the project Kanban board, or pasted ticket content. The board may be
  in Jira, Notion, Trello or another tool. If a board link is given and a
  connector for that tool is available, read the board directly; otherwise ask the
  user to paste the relevant tickets.
- Who the stakeholders are.

## Steps

1. Identify tickets that moved into In Progress or Done over the past week. Write
   a brief summary of each task and its progress.
2. Identify tickets in To Do that will be worked on next week. Write a brief
   summary of each.
3. Group all of the above by discipline (for example Design, Engineering).
4. Draft the email following the Output format below.

## Constraints

- Depth per task: default to one or two sentences. Expand only where a task is
  significant or the user asks.
- Technical jargon: match the stakeholders. For senior or cross-discipline
  readers, lead with outcome and impact and keep terms plain. For an engineering
  audience, more specific terms are fine.
- No em dashes or en dashes.
- Short, direct sentences. Do not over-tighten; expand only when asked.
- Keep introductory prose separate from any lists.
- Consistent Oxford comma usage and label casing throughout.
- Off-board work: tasks may be in progress without a ticket. Flag this and ask the
  user whether anything happened this week that the board does not show.
- No board set up: if there is no Kanban board, ask the user to describe or paste
  the week's work, then follow the same steps.

## Output format

A plain text email, structured as follows:

1. Introduction. Always open with this exact message:

   Hello everyone,
   This weekly update is intended to keep everyone aligned on progress, share
   early insights, and highlight where your input can help shape the work as we
   move forward.
2. TL;DR. A short summary of the week, a few sentences, readable at a glance.
3. This week. The body. Group by discipline, with each discipline as a heading.
   Under each, separate tasks into Done and In Progress, each task as a bullet
   point.
4. Next week. A separate section summarising what will be worked on next week.
5. Sign off. Always close with a sign-off message.

## Before it goes out

- Re-check the status of the tasks against the board, in case it is out of date,
  and add any context the board does not reflect.
- The intro came through word for word.
- The discipline grouping matches how the team is actually split.

This output is a draft to edit, never sent as-is.
