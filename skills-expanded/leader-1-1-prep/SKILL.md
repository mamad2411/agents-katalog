---
name: leader-1-1-prep
description: Build a prep brief for a recurring 1:1 with a skip-level or senior leader. Pulls the last meeting's notes, the tickets you touched since, recent chat threads with that leader and any drafts they are waiting on, then drafts a fixed five-block agenda with a carry-forward list and an after-action step. Use when the user says they have a 1:1 coming up, asks to prep for one, asks "what should I raise with <name>", or wants to review what is outstanding since the last one.
---

# 1:1 prep for a senior leader

A recurring 1:1 with a skip-level is thirty minutes that is easy to waste on a status list. Come with at most two decisions, one strategic thread and one question about yourself.

## When to run

- **The day before:** run this skill and leave the brief open for edits.
- **In the meeting:** work the agenda and take notes in the same place as last time.
- **Within the hour after:** run the after-action step below. It takes about ten minutes.

## Step 1: Gather

Pull each of these before drafting, from whatever tools the user has connected. Each answers a different question.

| Source | What to read | Answers |
| --- | --- | --- |
| Notes tool (Notion, Confluence, OneNote, a doc) | The leader's 1:1 folder or page: the two or three most recent dated entries | What was open last time? |
| Notes tool | Pages about feedback, reviews or offsites that name this leader | What has this leader asked me to work on? |
| Ticket tracker (Jira, Linear, GitHub) | Issues the user created or updated since the last 1:1 | What shipped? What slipped? |
| Chat (Teams, Slack) | The direct thread with this leader, and any channel with a live decision | What did they already ask me? |
| Drafts | Documents the user is writing that the leader has seen | What am I waiting on them to read? |

If a source cannot be reached, say so in the brief. An unchecked source is a gap the user needs to know about.

## Step 2: Check what carried forward

List every item from the last 1:1's notes and mark each one:

- **Closed:** the outcome in one clause.
- **Open:** who holds it and what happens next.
- **Dropped:** say so. An item that disappears without a word reads as unreliable.

An item open for two meetings in a row goes on the agenda or gets dropped on purpose.

## Step 3: Draft the five blocks

The structure is fixed and fits thirty minutes.

1. **Headline (2 min).** One sentence on where things stand.
2. **Decisions and asks (8 min).** At most two. Each says what is blocked, what you recommend, and what you need from the leader. An ask with no action for the leader is an update and belongs in the headline.
3. **People (8 min).** Pay, backfills, performance, growth, departures. Leaders follow up on these, so keep this block even when time is short.
4. **Strategy (7 min).** How the team's work connects to what the department is trying to do. If you have nothing here, that is the finding.
5. **Your growth (5 min).** One specific question, a different one each time. Rotate through: the gap to the next level, how a specific decision landed, who else should see your work, what they would do differently in your seat.

## Step 4: List what you will not raise

Prep turns up more than thirty minutes can hold. Name what stays out. Tool-level detail almost always goes here.

## Step 5: After the meeting

- Add the dated entry to the leader's 1:1 page. Record decisions, not a narrative.
- Turn every commitment into a ticket or an action item with an owner and a date.
- Write next time's growth question now, while the answer is fresh.

## Output

One Markdown file, `<leader>-1-1-<YYYY-MM-DD>.md`, with the carry-forward status, the five blocks, the list of what stays out, and the after-action checklist. Keep it to one screen. If it does not fit, the asks are not narrow enough yet.
