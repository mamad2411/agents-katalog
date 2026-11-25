---
name: arkon-review
description: "Review, approve, request changes on, or reject pending wiki edit drafts in Arkon. Requires editor or admin role. Triggers on: review drafts, pending reviews, check draft queue, approve draft, reject draft, request changes, send draft back, review wiki changes."
allowed-tools: mcp__arkon__list_pending_drafts mcp__arkon__review_draft mcp__arkon__approve_draft mcp__arkon__reject_draft mcp__arkon__request_changes_on_draft mcp__arkon__read_wiki_page
---

# arkon-review: Review Wiki Drafts

Editor/admin only. If `list_pending_drafts` returns a permission error, you don't have the required role.

---

## Review Workflow

### 1. List pending drafts

```
list_pending_drafts()
```

Returns: draft ID, page slug, author, timestamp, note. Filter by workspace if needed:
```
list_pending_drafts(workspace_id="<uuid>")
```

### 2. Read a draft for review

```
review_draft(draft_id)
```

Returns side-by-side: **proposed content** and **current page content (vN)**. Read both carefully.

You may also call `read_wiki_page(slug)` independently for fuller backlink context.

### 3. Decide

**Approve as-is:**
```
approve_draft(draft_id, reviewer_note="optional feedback to author")
```

**Approve with your own edits** (you want to tweak before publishing):
```
approve_draft(draft_id, edited_content_md="...", reviewer_note="approved with minor edits")
```

**Request changes** (the draft is on the right track but needs fixes; preferred over reject when iteration is realistic):
```
request_changes_on_draft(draft_id, reviewer_note="20+ char explanation — what to change and why")
```
The draft moves to `needs_revision`; author can `resubmit_draft` after addressing the note. The original draft stays — `revision_round` increments each round and prior submissions are snapshotted for diffing.

**Reject** (only when the proposal is fundamentally wrong — out of scope, factually broken, or duplicates an existing page):
```
reject_draft(draft_id, reviewer_note="clear reason why — required")
```

`reviewer_note` is **required** for both reject and request_changes — the author needs to understand what to fix. **Prefer request_changes over reject** unless the proposal cannot be salvaged.

**Conflict on approve**: if the page advanced past the draft's `base_version` while you were reviewing, `approve_draft` returns a conflict error. Re-call with `allow_conflict=true` to overwrite, or supply `edited_content_md` after merging the latest content yourself.

**Self-approve is blocked**: the server rejects approve attempts where the reviewer is also the author. Ask another editor.

---

## Approving a create draft

When the draft was filed via `propose_wiki_create`, it has `draft_kind: "create"`
and no page exists yet — approval materialises a new page using the
contributor's suggested metadata. The reviewer may override before commit
via the REST endpoint body (in the portal UI):

- `final_slug` — adjust the URL slug
- `final_title` — adjust the display title
- `final_page_type` — change page_type
- `final_knowledge_type_slugs` — fix the taxonomy tags (matters for RBAC)

Why adjust metadata? RBAC visibility is driven by `knowledge_type_slugs`;
slug shapes the URL forever; page_type affects how the page renders in the
index. Contributors are often not aware of the conventions — quietly fixing
these at approve is cheaper than asking them to resubmit.

If the slug already exists in the target scope, approval returns
`409 slug_conflict` — override `final_slug` or send the draft back with a
`request_changes` note explaining why.

---

## AI pre-review signals

Every draft carries an AI verdict (`ai_check_status` plus a list of checks):

- **`passed`** — no warnings. Most likely safe to approve after a quick read.
- **`warned`** — soft issues: broken wikilinks, possible duplicates, tone
  drift, scope-fit doubts. Read them; some are noise, some matter.
- **`failed`** — at least one PII / secret regex match. Read each match
  carefully. The contributor may have meant to include it (look for a
  `<!-- pii-allow: ... -->` marker above the match). If not, that's a
  request_changes situation.

The AI never blocks approval — it's a checklist, not a gate. Trust your own
judgment.

---

## Review Checklist

Before approving, verify:

- [ ] Content is factually consistent with other wiki pages (check backlinks if unsure)
- [ ] No sensitive data (PII, credentials, confidential figures) exposed
- [ ] Wikilinks `[[slug]]` point to real pages, not broken references
- [ ] Tone matches the KB style (factual, neutral, encyclopedic)
- [ ] The change note from the author makes the intent clear

---

## Batch Review

For multiple drafts:

1. `list_pending_drafts()` — get the full queue.
2. Group by page type or workspace if useful.
3. `review_draft` each one in order.
4. Approve/reject individually — do not bulk approve without reading each.

Always confirm with the user before approving a batch of more than 3 drafts in one go.

---

## Notes

- Approving a draft writes directly to the wiki page and creates a revision in history.
- Rejected drafts stay in the system with `status: rejected` — they are not deleted.
- You cannot approve your own drafts (the server enforces this).
