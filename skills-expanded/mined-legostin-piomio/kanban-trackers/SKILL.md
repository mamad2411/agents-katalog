---
name: kanban-trackers
description: Bring work from another tracker (Linear, GitHub issues, Notion, Jira…) onto the kanban board and keep the two in step. Use when the person wants issues from a tracker on the board, wants them synced on a schedule, or wants finished cards reported back to the tracker.
---

# The kanban board and other trackers

The board has no code for any tracker: you are the link. You have the tracker's tools (`linear_*` when Linear is
connected) and the board's (`kanban_*`). What keeps it sound is `external` on a card: its source and id there.

## First

1. Check you have the tracker's tools. If not, offer to connect it: `hub_integrations_list`, then
   `hub_integration_connect`. Do not ask for keys in the chat.
2. Ask only what you cannot find out: which team or project there, and which board project here. One tracker project to
   one board project is the plain choice. Make the board project with `kanban_project_save` if it does not exist.

## Bringing issues in

Read the issues with the tracker's tools, then one `kanban_card_import` call per up to 200 cards. Every card carries
`external: { source, id, url }`, with `source` the tracker's name in lowercase and `id` its human name (`ENG-123`).
Importing again updates the same cards and leaves them in their columns, so it is always safe to repeat.

Map what it says to the board:

- **Status**, by what it means, not its name. In Linear a state's `type`: `backlog` → backlog, `unstarted` → backlog
  (the person decides what goes to the queue), `started` → active, `completed` → done, `canceled` → cancelled. Pass it
  as the card's `status`. Skip closed issues unless the person wants them.
- **Priority:** Linear's 1 urgent, 2 high, 3 medium, 4 low, 0 none.
- **Labels** as they are. **Due date** as `YYYY-MM-DD`.
- **Description** as Markdown. Do not copy comments unless they are asked for.

Do not set `assignee` from the tracker: people there are not agents here.

Say in one line how many came and in which project. Then tell the person how it works: imported cards hold outside text,
so no agent takes one until they allow it. They can move cards to the queue on the board, or tell you which ones, and you
call `kanban_allow`.

## Keeping it in step

For a regular sync, use an ordinary schedule (`trigger_*` tools), with a prompt like "bring new and changed Linear issues
of team ENG onto the kanban project Site (skill kanban-trackers)". Ask how often; once an hour is plenty. The agent running
it needs initiative Acts.

## Reporting back

Writing to the tracker acts outside the hub, so do it when the person asked for it, and each write goes through their
approval as usual. To make it standing, put it in the project's notes with `kanban_project_save`, for example "when a
card from Linear is finished, comment the result on the issue and move it to In Review". Every run on the project reads
those notes.
