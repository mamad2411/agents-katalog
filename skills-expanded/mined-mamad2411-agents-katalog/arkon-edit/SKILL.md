---
name: arkon-edit
description: "Propose or directly apply edits to Arkon wiki pages, including proposing brand new pages. Contributors create drafts for review; editors/admins can edit/create directly. Triggers on: update wiki, fix this page, propose edit, edit wiki page, correct the KB, improve wiki, resubmit my draft, withdraw my draft, create new wiki page, propose new page."
allowed-tools: mcp__arkon__search_wiki mcp__arkon__read_wiki_index mcp__arkon__read_wiki_page mcp__arkon__propose_wiki_edit mcp__arkon__edit_wiki_page mcp__arkon__propose_wiki_create mcp__arkon__create_wiki_page mcp__arkon__resubmit_draft mcp__arkon__withdraw_draft
---

# arkon-edit: Edit the Knowledge Base

Always read the current page before proposing changes. Always confirm with the user before submitting.

---

## Permission Tiers

| Role | Tool to use | Review required |
|------|------------|----------------|
| Contributor | `propose_wiki_edit` | Yes — goes to editor queue |
| Editor | `edit_wiki_page` | No — writes directly |
| Admin | `edit_wiki_page` | No — writes directly |

If you try `edit_wiki_page` and get a permission error, fall back to `propose_wiki_edit`.

---

## Workflow: Propose an Edit (Contributor)

1. **Find the page** — `search_wiki(query)` or `read_wiki_index()` to locate the slug.
2. **Read current content** — `read_wiki_page(slug)`. Never propose without reading first.
3. **Draft the edit** — produce the full updated Markdown (not a diff — the tool takes full content).
4. **Confirm with user** — show the diff or summary of changes. Get explicit approval.
5. **Submit** — `propose_wiki_edit(slug, content_md, note="one-line explanation")`.
6. Report the draft ID to the user so they can track it.

Do not submit a draft without user confirmation. The note field is important — editors need context.

---

## Workflow: Direct Edit (Editor/Admin)

Same steps 1-4 above, then:

5. **Submit** — `edit_wiki_page(slug, content_md, change_note="one-line explanation")`.
6. Report the new version number returned.

---

## Content Rules

- Submit **full page content** — these tools replace, not patch.
- Max 50,000 characters per submission.
- Cannot edit reserved pages: `_index`, `_log`.
- Preserve existing wikilinks `[[slug]]` unless intentionally removing them.
- Keep the page's existing frontmatter fields (title, type, knowledge_type_slugs, etc.) unless the change specifically needs to update them.

---

## When NOT to edit

- Do not edit without user instruction — even if you spot an error while querying.
- Do not create new pages via these tools (they only update existing pages).
- If the target slug doesn't exist, tell the user — new page creation is an admin/pipeline operation.

---

## Iteration loop: when a reviewer sends changes back

If a reviewer used `request_changes_on_draft`, the draft moves to status
`needs_revision`. The original draft is preserved; you (or the user) can fix
it without creating a fresh proposal.

1. `read_wiki_page(slug)` — make sure the page hasn't moved on while you waited.
2. Read the reviewer note attached to the draft (visible in the in-app
   notification). Address every point they raised.
3. Confirm the rewrite with the user.
4. `resubmit_draft(draft_id, content_md, note="what I changed in this round")`.
   - Bumps `revision_round` and notifies reviewers.
   - The prior submission is snapshotted to history (rounds) so the reviewer
     can diff your changes against the previous round.

## Withdrawing your own draft

If you no longer want a pending or needs_revision draft to be reviewed:

```
withdraw_draft(draft_id)
```

Only the original author may withdraw (admins can override via the REST API).
Withdrawn drafts are terminal and disappear from reviewer queues. Confirm with
the user before withdrawing — it cannot be reversed via MCP.

## Scope disambiguation

When `propose_wiki_edit` or `edit_wiki_page` finds the same slug in multiple
scopes (global + project, for example), the call fails with a list of the
candidate scopes. Re-call with `scope_type` and `scope_id` to target the
specific page the user means.

---

## Creating a brand-new page

**First check whether one already exists.** Always run `search_wiki(query)`
and inspect the top hits before proposing a new page — duplicates waste
reviewer time and trigger the AI duplicate check.

| Role | Tool | What happens |
|------|------|-------------|
| Contributor+ | `propose_wiki_create` | Draft enters reviewer queue; page materialised on approve |
| Editor+ (workspace) or `wiki:write:all` (global) | `create_wiki_page` | Page created immediately |

Required fields for both tools:
- `slug` — unique inside the chosen scope, no whitespace, not `_index`/`_log`
- `title` — display title
- `content_md` — full Markdown
- `page_type` — one of `entity` | `concept` | `source` | `topic`
- `scope_type` — `global` | `department` | `project` (with `scope_id` for the latter two)
- `knowledge_type_slugs` — taxonomy tags that drive RBAC visibility; ask the
  user which categories apply rather than guessing

Workflow:
1. `search_wiki` to confirm nothing similar exists.
2. Show the user the suggested slug, page_type, knowledge_type_slugs, scope and the full content. Confirm.
3. Call the appropriate tool. Report the returned draft ID (propose path) or
   the created page version (direct path).

If approve later returns a slug conflict, the reviewer or the contributor must
override `final_slug` (reviewer side) or rename and resubmit (contributor side).

---

## AI pre-review

Every draft you submit is annotated by an AI pre-review layer that flags:
- **PII / secrets** (emails, phone numbers, API keys, JWTs, ...)
- **Broken wikilinks** to slugs that don't exist
- **Possible duplicates** with existing pages (embedding similarity)
- **Tone / scope fit / factual concerns** (LLM judgment)

The flags are **advisory only** — they do not block submission and reviewers
make the final call. But: address obvious ones (broken links, accidental PII)
before submitting to save the reviewer time.

If a regex flags a legitimate contact email or hotline that you intentionally
included in the page, add a suppression comment on the line above:

```markdown
<!-- pii-allow: contact-email -->
Email team: compliance@example.com
```

The marker covers regex matches on the same or next non-blank line. Choose a
short, honest reason — it shows up in the reviewer's audit trail.
