---
name: confluence-page-authoring-and-governance
description: >
  Guides authoring well-structured Confluence pages (clear heading
  hierarchy, table of contents, templates for runbooks/design docs/
  postmortems), organizing them within a space, keeping version/page
  history discipline, and labeling/linking for discoverability — plus the
  underlying Confluence REST API shape (`POST /wiki/rest/api/content`)
  for creating/updating pages programmatically. Use when the user asks
  to "create a Confluence page", "update a Confluence page", "document a
  runbook in Confluence", "write a design doc", "write a postmortem",
  "organize this space", or "why can't anyone find this page".
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: enterprise-collaboration
  maturity: stable
---

# Confluence Page Authoring and Governance

## Purpose

Confluence pages that lack structure, ownership, or a place in the
space's hierarchy don't stay useful — they go stale because no one is
responsible for updating them, they go undiscoverable because nothing
links to them, and they get duplicated because the next person couldn't
find the original and wrote a new one instead. This skill covers how to
structure a page so it's actually readable (hierarchy, table of
contents, purpose-built templates for runbooks/design docs/postmortems),
how to organize a space so pages have a findable home, the version/
history discipline that keeps concurrent edits and audit trails sane,
and how to do page creation/update programmatically via the Confluence
REST API. It assumes the underlying work is already tracked in Jira —
see
[jira-ticket-best-practices-and-workflow](../jira-ticket-best-practices-and-workflow/SKILL.md)
and
[jira-comments-and-tracking-automation](../jira-comments-and-tracking-automation/SKILL.md)
for that half of the workflow, and link back to the originating ticket
from any page this skill produces.

## When to use

- Creating a new runbook, design doc, postmortem, or reference page.
- Updating an existing page and deciding whether/how to preserve history.
- Organizing or auditing a space's page hierarchy (parent/child
  structure, landing/index pages).
- Adding labels or cross-links so a page is actually discoverable later.
- Creating or updating pages programmatically via the Confluence REST
  API (Cloud or Data Center).
- Investigating why a page (or an entire topic area) has gone stale,
  duplicated, or orphaned.

## Prerequisites & environment

- A Confluence space with edit permission for the target parent page(s).
- API access: for **Confluence Cloud**, an API token
  (`${CONFLUENCE_API_TOKEN}`) tied to an Atlassian account, used against
  `${CONFLUENCE_BASE_URL}/wiki/rest/api/...`. For **Confluence Data
  Center/Server**, a Personal Access Token against
  `${CONFLUENCE_BASE_URL}/rest/api/...` (no `/wiki` prefix) — confirm
  which edition you're targeting before assuming the base path.
- Confluence's REST `content` body uses **storage format** — an
  XHTML-like markup (not raw Markdown, not ADF) — for the page body.
  Simple content maps closely to HTML (`<h2>`, `<p>`, `<table>`, `<ul>`),
  but macros (Table of Contents, Jira issue macro, status macro) use
  Confluence-specific `<ac:structured-macro>` XML elements. Exact
  supported macros vary by edition/version and installed apps — verify
  a macro exists on the target instance before relying on it.
- Updating an existing page requires knowing its **current version
  number** — Confluence rejects (`409 Conflict`) an update whose
  `version.number` doesn't match `current + 1`, by design, to prevent
  silently clobbering a concurrent edit.
- If no direct API/MCP access is available, the same structure/
  governance guidance applies when authoring through the Confluence
  editor UI directly or relaying content for someone else to paste in.

## Step-by-step guidance

1. **Decide where the page lives before writing it.** Pick the space and
   the parent page first — a page with no deliberate parent tends to end
   up either at the space root (invisible in any topical hierarchy) or
   nowhere anyone browses to. If a natural parent doesn't exist yet
   (e.g. no "Runbooks" index page in this space), create that index page
   first, or use the space's existing top-level structure.

2. **Search before creating.** Check the space (and likely-adjacent
   spaces) for an existing page on the same topic before writing a new
   one — a duplicate "Deployment Runbook" in two spaces is worse than no
   runbook, because neither is known to be authoritative.

3. **Use a purpose-built template outline, not a blank page:**
   - **Runbook** — see
     [references/runbook-template.md](references/runbook-template.md):
     owner, architecture/dependencies, common operations, alerts and
     what they mean, troubleshooting by symptom, escalation path.
   - **Postmortem** — see
     [references/postmortem-template.md](references/postmortem-template.md):
     summary, impact, timeline, root cause, detection, what went well/
     wrong, action items each linked to a real Jira ticket.
   - **Design doc** — outline: Problem statement → Goals/non-goals →
     Proposed approach → Alternatives considered (and why rejected) →
     Rollout/migration plan → Open questions. The "alternatives
     considered" section is what most first-draft design docs skip, and
     it's the part a future reader most needs to understand *why*.

4. **Structure headings so the Table of Contents macro is actually
   useful.** Use `H2`/`H3` consistently for section structure (not `H1`
   repeated per section), keep heading text scannable, and place a
   Table of Contents macro near the top of any page longer than ~4
   sections so a reader can jump to the relevant part instead of
   scrolling a runbook during an incident.

5. **Label for discoverability, using a controlled vocabulary.** Reuse
   existing labels (service name, `runbook`/`postmortem`/`design-doc`,
   owning team) rather than inventing near-duplicates (`run-book` vs.
   `runbook`) — check the space's existing label list first. Labels
   drive both search filtering and label-based index pages/macros.

6. **Link the page from an index/parent page at creation time**, not as
   a follow-up — an unlinked page only reachable by direct search is
   effectively orphaned for anyone browsing the space. Also link back to
   the originating Jira ticket (and vice versa, via a comment or the
   Jira issue macro) so the two systems stay connected.

7. **Assign an explicit owner and review cadence for anything
   operational** (runbooks especially). A page with no named owner is a
   page nobody notices has gone stale. Track review-due dates with a
   label (`review-2026-q4`) or a "Last reviewed" line at the top of the
   page, and audit periodically for pages past due.

8. **Create a page via the REST API:**

   ```http
   POST /wiki/rest/api/content
   Host: ${CONFLUENCE_BASE_URL}
   Authorization: Basic base64(${CONFLUENCE_USER_EMAIL}:${CONFLUENCE_API_TOKEN})
   Content-Type: application/json
   ```

   ```json
   {
     "type": "page",
     "title": "Auth Service Runbook",
     "space": { "key": "ENG" },
     "ancestors": [{ "id": "123456" }],
     "body": {
       "storage": {
         "value": "<h2>Owner</h2><p>Team: Auth Platform. Last reviewed: 2026-07-28.</p><ac:structured-macro ac:name=\"toc\"/><h2>Overview</h2><p>Handles SSO and session token issuance.</p>",
         "representation": "storage"
       }
     }
   }
   ```

   `ancestors[0].id` sets the parent page — omit it and the page lands
   at the space root, which is the "orphaned by default" failure mode
   from step 1. A successful response is `200 OK`/`201 Created` with the
   new page's `id`, `title`, and a `_links.webui` URL.

9. **Update an existing page — always fetch the current version
   first:**

   ```http
   GET /wiki/rest/api/content/789012?expand=version,body.storage
   ```

   Read `version.number` from the response (e.g. `4`), then submit the
   update with `version.number` incremented by exactly one:

   ```http
   PUT /wiki/rest/api/content/789012
   Content-Type: application/json
   ```

   ```json
   {
     "id": "789012",
     "type": "page",
     "title": "Auth Service Runbook",
     "space": { "key": "ENG" },
     "body": {
       "storage": {
         "value": "<h2>Owner</h2><p>Team: Auth Platform. Last reviewed: 2026-07-28.</p>...",
         "representation": "storage"
       }
     },
     "version": { "number": 5, "message": "Update alert thresholds after AUTH-2231 incident" }
   }
   ```

   Populating `version.message` gives page history a meaningful audit
   trail — "Update alert thresholds after AUTH-2231 incident" is far
   more useful than the default blank entry when someone is scanning
   history for what changed and why.

10. **Add labels via the labels endpoint** (or inline in the create/
    update payload if the integration supports it):

    ```http
    POST /wiki/rest/api/content/789012/label
    Content-Type: application/json
    ```

    ```json
    [{ "prefix": "global", "name": "runbook" }, { "prefix": "global", "name": "auth-service" }]
    ```

## Best practices

- One authoritative page per topic; if a second draft starts, merge it
  into the original and redirect/delete the duplicate rather than
  letting both persist.
- Prefer updating the existing page's history over copying it to a new
  page for "v2" — Confluence's version history already gives you
  before/after diffs; a `v2` page just splits the audit trail.
- Every page should be reachable by clicking from its space's home page
  through no more than a few hops — if it isn't, add the missing link
  rather than relying on search alone.
- Give runbooks and design docs an explicit owner and review date;
  postmortems should be "Final" with tracked action items, not left in
  "Draft" indefinitely.
- Use the Table of Contents macro instead of a hand-maintained list of
  links — a hand-written TOC drifts out of sync with headings the first
  time someone edits the page.
- When a page's content is superseded, mark it clearly (a banner/status
  macro: "Superseded by <link>") instead of silently leaving stale
  content live and discoverable.

## Common pitfalls

- **Symptom:** A runbook was accurate when written but has no named
  owner; eighteen months later an on-call engineer follows steps that no
  longer match the deployed system, making an incident worse instead of
  better.
  **Fix:** Every operational page gets an explicit owner and a review-due
  label/date at creation (see the runbook template); audit for pages
  past their review date on a recurring cadence, not reactively during
  the next incident.

- **Symptom:** A new page is created and never linked from any parent/
  index page — it only surfaces if someone happens to search the exact
  right term, so most of the team doesn't know it exists and eventually
  someone writes a near-duplicate.
  **Fix:** Link every new page from its logical parent/index page at
  creation time (step 6), not as a follow-up task that's easy to skip.

- **Symptom:** Two people update the same page around the same time;
  the second `PUT` overwrites the first person's edit because it was
  built from a stale `version.number`, and the change silently
  disappears with no error visible to the user who made it.
  **Fix:** Always `GET` the current `version.number` immediately before
  `PUT`-ing an update (step 9); if the API returns `409 Conflict`,
  re-fetch and re-apply the intended change rather than retrying with
  the same stale version.

- **Symptom:** A team has two "Deployment Process" pages in different
  spaces (one from the original space, one someone wrote later because
  they couldn't find the first) with subtly different, partially
  contradictory steps — and neither is marked as canonical.
  **Fix:** Search the space (and adjacent spaces) before creating a new
  page on a topic (step 2); when a duplicate is found after the fact,
  merge content into one canonical page and mark the other superseded
  with a link, don't just delete it silently.

- **Symptom:** A postmortem page sits in "Draft" status indefinitely with
  action items that were never turned into tracked tickets, so none of
  the follow-up work happens and the same incident recurs.
  **Fix:** Require every postmortem action item to link a real Jira
  ticket at write time (see the postmortem template and
  [jira-ticket-best-practices-and-workflow](../jira-ticket-best-practices-and-workflow/SKILL.md)),
  and treat "Draft" as a short-lived state with a target date to reach
  "Final."

## Worked example

**Scenario:** After resolving `AUTH-2231` (the EU SSO `invalid_grant`
incident from the Jira ticket skill's worked example), the team needs to
(a) update the existing Auth Service runbook with a new troubleshooting
entry, and (b) publish a postmortem, both properly linked and labeled.

**Step 1 — fetch current runbook version before editing:**

```http
GET /wiki/rest/api/content/789012?expand=version,body.storage
```

Response shows `"version": { "number": 4 }`.

**Step 2 — update the runbook's Troubleshooting section, bump version:**

```http
PUT /wiki/rest/api/content/789012
```

```json
{
  "id": "789012",
  "type": "page",
  "title": "Auth Service Runbook",
  "space": { "key": "ENG" },
  "body": {
    "storage": {
      "value": "...<h3>Symptom: invalid_grant errors scoped to one region</h3><p>Check IdP/auth-service clock skew first — see AUTH-2231 postmortem.</p>...",
      "representation": "storage"
    }
  },
  "version": { "number": 5, "message": "Add clock-skew troubleshooting entry from AUTH-2231" }
}
```

**Step 3 — create the postmortem page as a child of the space's
"Postmortems" index page (id `654321`), using the template outline from
[references/postmortem-template.md](references/postmortem-template.md):**

```http
POST /wiki/rest/api/content
```

```json
{
  "type": "page",
  "title": "Postmortem: EU SSO invalid_grant Incident (2026-07-28)",
  "space": { "key": "ENG" },
  "ancestors": [{ "id": "654321" }],
  "body": {
    "storage": {
      "value": "<h2>Summary</h2><p>SSO logins failed for ~120 EU users for 40 minutes due to clock skew between the IdP and auth-service.</p><h2>Timeline</h2><table>...</table><h2>Action Items</h2><p>Add config validation to CI — AUTH-2240</p>",
      "representation": "storage"
    }
  }
}
```

**Step 4 — label both pages and link them to the Jira ticket:**

```http
POST /wiki/rest/api/content/789012/label
```

```json
[{ "prefix": "global", "name": "runbook" }, { "prefix": "global", "name": "auth-service" }]
```

The postmortem page links back to `AUTH-2231`, and — per
[jira-comments-and-tracking-automation](../jira-comments-and-tracking-automation/SKILL.md) —
a comment is posted on `AUTH-2231` pointing to the new postmortem page,
so the two systems reference each other instead of the resolution living
only in one place.

## Cross-references

- [jira-ticket-best-practices-and-workflow](../jira-ticket-best-practices-and-workflow/SKILL.md) —
  the ticket that this documentation should trace back to, including
  linking Jira and Confluence to each other.
- [jira-comments-and-tracking-automation](../jira-comments-and-tracking-automation/SKILL.md) —
  posting a comment on the originating ticket that points back to the
  Confluence page produced here.
