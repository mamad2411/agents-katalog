---
name: ticket-digest
description: Turn a batch of tickets created or updated in a time window into one short, paste-ready message, one line per ticket, flagging the ones that need a decision. Use when the user asks what they filed today or this week, wants a recap or roundup for a product owner or team channel, or after filing three or more tickets in one sitting.
---

# Ticket digest

One message instead of a stream of notifications, readable in thirty seconds.

## Steps

1. **Collect.** By default, tickets the current user created today, across projects. Widen or narrow the window, project, epic or author as the user asks; for "updated" rather than "created", add the assignee. Fetch titles, types, statuses and parents only. If a title is too vague to summarize, say so; that is a title worth fixing.
2. **Group** by parent epic, then by a title prefix if the team uses one, then by project. Add headings only when there is more than one group.
3. **One line per ticket:**

   ```
   KEY  Type  What it does, in twelve words or fewer  [needs: decision | review | estimate]
   ```

   Add the bracket only when it applies: an open question someone must answer, a named reviewer, or ready for estimation.
4. **Up to three sentences of context**, and only ones that change what the reader does: why the batch exists, what you are asking for and by when, overlap you spotted with older tickets.
5. **Output plain text** ready to paste, with group headings in bold and nothing else formatted, under 150 words for up to ten tickets.

This skill writes the message. The user posts it.

## Example

```
New backlog items, Sep 15

**Media delivery audit** (WEB-120, epic)
WEB-121  Task  Measure PDF sizes and bandwidth
WEB-122  Task  Find pages still serving raw MP4 files
WEB-123  Task  Standardize video transformations  [needs: decision]

**Search**
WEB-130  Bug   Product pages drop structured data when descriptions contain links

Four items from the bandwidth review. WEB-123 needs a call on per-site presets before Thursday; the rest are ready to estimate.
```
