---
name: fibery-entities
description: Create, update, and delete Fibery entities and their content - field values, rich-text documents, collection links, workflow states, comments, and file attachments. Use when writing anything into Fibery, bulk-updating records, filling in a Description, linking entities together, moving items through a workflow, or attaching files.
---

# Writing to Fibery

Writes in Fibery are deliberately split across several tools. `create_entities`
and `update_entities` handle plain scalar fields only; four categories of field
each have their own tool, and using the general tool on them always errors.

## The split, memorized

| Field kind | Tool |
|---|---|
| Text, number, bool, date, date-range, location, single relation, single select | `create_entities` / `update_entities` |
| Rich-text document (`Collaboration~Documents/Document`) | `set_document_content` / `append_document_content` |
| Collection (one-to-many, many-to-many) | `add_collection_items` / `remove_collection_items` |
| Workflow state (`workflow/state`) | `set_state` |
| Comments | `add_comment` |
| Files | `add_file_from_url` |

Read-only fields can never be written: `fibery/id`, `fibery/public-id`,
`fibery/creation-date`, `fibery/modification-date`, `fibery/created-by`,
`fibery/modified-by`, and every formula field. `schema_detailed` marks
read-only fields explicitly. Respect the marks.

## Before any write

1. `schema` to confirm the database exists and its exact `Space/Database` name.
2. `schema_detailed` on that database to get field names, types, read-only
   marks, and enum option ids.
3. `query` or `search` to resolve any entity or option you are referencing into
   a `fibery/id` UUID.

Every write tool takes `fibery/id` (the UUID), not `fibery/public-id`.

## Value formats

```json
{
  "database": "Product Management/Feature",
  "entities": [{
    "Product Management/Name": "Advanced Search",
    "Product Management/Pain Level": 5,
    "Product Management/Is Critical": true,
    "Product Management/Release Date": "2026-12-31",
    "Product Management/Dates": {"start": "2026-12-31", "end": "2027-01-10"},
    "Product Management/Parent Feature": "<uuid>",
    "Product Management/Priority": "<option-uuid>"
  }]
}
```

Two format traps worth stating plainly:

**Relations and selects take a bare UUID string.** Passing an object is
rejected.

- Wrong: `{"Product Management/Priority": {"id": "<uuid>"}}`
- Right: `{"Product Management/Priority": "<uuid>"}`

**Date-range end dates are exclusive.** The end day itself is not included. If
the user asks for July 31 through August 2, write
`{"start": "2026-07-31", "end": "2026-08-03"}`. Getting this wrong silently
produces a range one day short, which nobody notices until it matters.

**Never pass an array as a field value.** That is always a collection, and
collections need `add_collection_items`.

## Creating an entity with everything filled in

Creation is a sequence, not one call. `create_entities` returns the new
`fibery/id`, which the follow-up calls need.

1. `create_entities` with the scalar fields.
2. `set_document_content` for the Description or any other document field.
3. `add_collection_items` for each collection field.
4. `set_state` if the database has a workflow and the default state is wrong.

Do not try to fold steps 2 through 4 into step 1. Each will error.

## Updating

`update_entities` is a partial update: only the keys you send change,
everything else is left alone. `fibery/id` is required in each entity object.

```json
{
  "database": "Product Management/Feature",
  "entities": [{"fibery/id": "<uuid>", "Product Management/Is Critical": false}]
}
```

Both `create_entities` and `update_entities` take an array, so batch related
changes into one call rather than looping.

To clear a scalar field, send `null`.

## Documents

`set_document_content` replaces the whole document. `append_document_content`
adds to the end. Prefer append when you are adding a note to something a human
wrote; use set only when you intend to overwrite, and read the current content
first (via `query` for the secret, then `get_documents_content`) so you know
what you are replacing.

Content is Markdown, plus Fibery callouts:

```
> [//]: # (callout;icon-type=icon;icon=info-circle;color=#199EE3)
> Body line one
> Body line two
```

`icon-type` is `icon` for FontAwesome names or `emoji`. Useful colors:
`#199EE3` blue, `#E53935` red, `#43A047` green, `#FB8C00` orange.

To empty a document, `set_document_content` with `content: ""`.

## Collections

`add_collection_items` and `remove_collection_items` both take the parent
`entityId`, the collection `field`, and an array of related entity UUIDs. Use
`query` with a sub-query first to see what is already linked so you do not
duplicate or remove the wrong thing.

## Workflow state

`set_state` takes the state title as it appears in `enum/name`, not a UUID:

```json
{"database": "SoftDev/Task", "entityId": "<uuid>", "state": "Done"}
```

Only one workflow field exists per database, which is why no field name is
needed. Read the legal state names from `schema_detailed` before calling;
a title that does not exist is an error.

## Comments

`add_comment` posts Markdown as the authenticated user. There is no way to
comment as someone else.

The database must actually support comments, meaning it has a
`comments/comments` collection. Check `schema_detailed` first.

For a reply, pass `parentCommentId`. That parent **must belong to the same
entity** as `entityId`; a parent from a different entity is rejected server
side. Inline comments on document text ranges and whiteboard comments are not
supported.

To read existing comments, sub-query them:

```json
{"query": {
  "q/from": "Product Management/Feature",
  "q/select": {
    "Id": "fibery/id",
    "Comments": {"q/from": "comments/comments",
                 "q/select": {"Id": "fibery/id", "Secret": "comment/document-secret"},
                 "q/limit": 100}
  },
  "q/where": ["=", ["fibery/public-id"], "<public-id>"],
  "q/limit": 10
}}
```

Then pass the secrets to `get_documents_content`.

## Files

`add_file_from_url` makes the Fibery server download a publicly reachable URL
and attach it to a file field. There is no retry: if the URL is not fetchable
the call fails with an upload error. Verify the URL is public before calling.
The target must be a file field (`create_files_fields` makes them); document
fields are not valid targets.

## Deleting

`delete_entities` permanently removes records and cannot be undone.

Before calling it: state which database, how many entities, and enough
identifying detail (names or public ids) that the user can tell you are about
to delete the right things. Then wait for an explicit yes. Never delete as a
speculative cleanup step, and never widen a delete beyond what was asked.

If the user's real intent is "get this out of my way", check whether archiving
suits them better and say so, since archive is recoverable and delete is not.

## After writing

Report what changed with links. Select `fibery/public-id` on the affected
entities and pass them to `get_entity_links` so the user can click straight to
the result.
