---
name: confluence-jira-links
description: Link a Confluence page and the Jira tickets it is about, both ways, without duplicates - each ticket shown on the page as a Jira smart link, and a "mentioned in" web link on each ticket pointing back to the page. Use whenever you create or edit a Confluence page (draft or published) that discusses Jira issues, when you file an issue that a Confluence page already describes, when the user says "link the tickets", "add the Jira links", "make these smart links", or asks why a ticket shows the same page twice.
---

# Confluence ↔ Jira links

A page about ticketed work should let a reader jump to every ticket, and every ticket should
show the pages that discuss it. Confluence does half of this for you, and the order you work
in decides whether the other half produces duplicates.

**Requires:** the Atlassian MCP connector (`getConfluenceContent`, `updateConfluenceContent`
or `createConfluenceContent`, `getJiraIssue`, and the remote-link operations found through
`discover`: list and create remote issue links).

## Team defaults

| Setting | Value |
| --- | --- |
| Jira site | Yours, from the user's `CLAUDE.md` or the connector's `getAccessibleAtlassianResources`. `https://your-site.atlassian.net` below stands for it. |
| Smart link markup | `<a href="https://your-site.atlassian.net/browse/KEY" data-card-appearance="inline">https://your-site.atlassian.net/browse/KEY</a>` |
| Back-link relationship | `mentioned in` |

## The one fact that sets the order

**Saving a page that contains a Jira smart link makes Confluence add the "mentioned in" web
link on that ticket by itself, within seconds.** The back-link points at
`.../wiki/pages/viewpage.action?pageId=<id>`.

So if you create the back-link yourself *before* saving the smart link, the ticket ends up
with two links to the same page. The connector has no operation to delete a web link, so a
person has to remove the extra one by hand. Never create the back-link ahead of the page.

## Workflow

### 1. Write the ticket into the page as a smart link

Every mention of a ticket key in the page body becomes the smart link markup from Team
defaults: not plain text, and not a bare hyperlink with the key as its text. Edit pages in
HTML (`contentFormat: "html"` or the storage format) so the `data-card-appearance` attribute
survives; markdown drops it.

On a page you are editing, change only the mentions. Leave the rest of the body as it was
read.

### 2. Save, then wait

Save the page. Wait a few seconds before touching the ticket.

### 3. Check each ticket's web links

For every ticket on the page, list its remote links. Look for one whose URL carries this
page's id (`pageId=<id>`) or the page's `/pages/<id>/` path.

- **Found:** done for that ticket. Do not add another.
- **Not found after one more short wait:** create it, with the relationship from Team
  defaults, the page title as the link title, and the page URL. This happens when the page
  was saved without the smart link markup, or the save went through a path that does not
  trigger Confluence's automation.

### 4. Tickets filed after the page

When a ticket is created for work an existing page already describes, go back to the page,
turn the plain mention (or add a new mention) into a smart link, save, and run step 3 for
that ticket. Do not stop at linking from the ticket side.

### 5. Report

One line per ticket: `KEY: smart link on page; back-link present (auto)` or `(created)`. If a
ticket already had a duplicate before you started, say so; you cannot remove it.

## Shared pages

Edits made through the connector can show the agent's integration in the page's recent
viewers or history. If the page belongs to someone else, or the user prefers their own name
on every edit, hand them the smart link markup to paste and run only step 3 afterwards.
