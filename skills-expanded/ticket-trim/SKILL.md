---
name: ticket-trim
description: Shorten an existing ticket that is too long or too technical, moving the engineering detail into a Technical notes comment so nothing is lost. Use when the user gives a ticket key or link and asks to trim, condense, simplify or clean it up, or says a product owner or analyst found it hard to read.
---

# Ticket trim

Reshape one existing ticket to the `ticket-write` shape: a short plain-language description, the detail in a `Technical notes` comment. The budgets, the templates and the lint script are in the `ticket-write` skill's folder.

## Steps

1. **Read the ticket** in full, with its comments and any acceptance-criteria field. Note its type, its reporter, and whether it has images, mentions or checklists, which must survive the rewrite. If someone else reported it, say so before changing anything.
2. **Sort every sentence.**
   - **Keep**: the effect, why it matters, outcomes someone can check, scope, links. These become the new description.
   - **Move**: root causes, file paths, function names, config keys, phased plans, verification steps. These become the technical notes.
   - **Link out**: anything that is really a document, such as a multi-phase plan with a decision log. Do this only with the user's agreement, since it creates a page.

   Rewrite acceptance criteria that name an implementation ("retry with backoff") as the outcome ("a short outage shows no error to visitors"). Keep a long criterion when it is long because it is precise.
3. **Lint** the new description with `../ticket-write/scripts/ticket_lint.py`.
4. **Show before and after**: the numbers on one line ("612 → 131 words, identifiers 40 → 1, criteria 9 → 4"), the new description, and the technical notes. Editing notifies watchers, so wait for a go-ahead.
5. **Apply, in this order**:
   1. Post a comment titled `Original text (before trim)` containing the old description and any rich-text field you will change, word for word. Some trackers keep no history for custom fields, which would make this comment the only copy. If such a comment already exists from an earlier trim, leave it.
   2. Post or update the `Technical notes` comment.
   3. Replace the description, and the title if it was over 80 characters.
   4. Report the key and the numbers, and point to the original-text comment as the way back.

Leave tickets that are already done or closed alone; nobody is left to read them.
